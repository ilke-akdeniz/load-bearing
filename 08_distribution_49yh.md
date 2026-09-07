# Distribution: What's Impossible

## The claim

**You cannot tell a late reply from one that is never coming.**

That is not a limitation of your monitoring, your language, or your budget. Silence has two explanations — the answer is still coming, or it is never coming — and nothing available to you separates them.

The instinct at this point is to ask. Send a second message: *are you still there?* It does not help. A reply to your probe tells you the channel is working **now**. It tells you nothing about whether the first message was received, or acted on, or is about to arrive. And if nothing comes back from the probe either, you are in the position you started in, one message poorer. **Probing reports the present; your question is about the past.**

## Four words people get wrong

**A part** is anything that can stop working while the rest keeps going. A process, a machine, a database, a queue, somebody else's API. Not a class, not a module, not a layer — the test is whether it can be down on its own.

**A channel** is whatever carries messages between two parts. The property that decides everything below is whether **the channel can fail while both parts are still running.** A Unix socket between two processes on the same machine is such a channel. Shared memory between those same two processes is not, because there is no delivery step that can fail: if the memory is gone, both parts are gone with it. *Channel* rather than *network* deliberately — nothing here depends on Ethernet, and the theorems below are all stated over channels.

**Distributed** means you have two parts joined by such a channel — and that is almost everyone, including a single application server talking to a single database. Saying so is more useful than the usual test, because what varies between systems is not *whether* this chapter applies but *how much of it does*:

- **One part holding all the state.** One database, whatever is in front of it. You get atomicity and ordering for free, and there is no consensus to reach. What remains is the waiting problem: you send a request, the connection drops, and you do not know whether it was applied.
- **Two or more parts holding state that must agree.** A database and a queue. A service and a payment provider. Two databases. Now nothing is free, and the rest of this chapter is about what you build instead.

The mistake worth avoiding is not "thinking you are distributed when you aren't." It is reaching for the machinery of the second case while living in the first.

**A partition** is not necessarily a cut network cable or failed machine. **It is a period in which one part cannot reach another within the time the waiter is willing to wait** — which means the word has no meaning without a deadline attached. A garbage collector that stops the world for four microseconds partitions nothing, because nobody's timeout is four microseconds. The same collector pausing for four seconds partitions a caller whose deadline is one second, and does not partition a batch job happy to wait a minute. Cables are the rarest cause: exhausted connection pools, saturated thread pools, a machine that has started swapping and a peer that is merely busy all produce partitions, and all are indistinguishable from a severed cable, because the observable in every case is silence.

So *partition tolerance* is not insurance against a rare catastrophe. If you have ever seen a service time out under load, you have seen a partition.

---

## The demonstration

### Every timeout is a guess

A payments client calls a charge service, with a 100 ms deadline on the request:

```go
func charge(ctx context.Context, url, orderID string) error {
	ctx, cancel := context.WithTimeout(ctx, 100*time.Millisecond)
	defer cancel() // release the timer whichever way this returns

	req, _ := http.NewRequestWithContext(ctx, http.MethodPost, url+"?order="+orderID, nil)

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	return nil
}
```

Now call it twice, against two services in genuinely different states. One is alive and having a bad day — it will answer, in 150 ms. The other has stopped answering entirely:

```go
errSlow := charge(ctx, slowService, "order-1") // alive, overloaded
errDead := charge(ctx, deadService, "order-2") // process is gone
```

```text
slow service -> context deadline exceeded
dead service -> context deadline exceeded
identical observations: true
charges applied by the slow service after the client gave up: 1
```

The two observations are the same string. The client has no instrument that distinguishes them, and no longer timeout would help — a longer timeout just moves the boundary, and the slow case moves with it.

That last line is the expensive part. **The slow peer completed the work.** So the client's two options are both wrong: retry, and the work happens twice; give up, and the client reports a failure that did not occur. There is no third option available at the client, which is why the fix is never at the client.

### What the waiter can do

Everything in this chapter is built out of four responses to that silence. There are only four, and naming them is most of the design work.

**Wait forever.** Correct in exactly one situation: when the work has no deadline and nothing downstream is holding a resource while you block. In a request handler it is the worst option available, because your caller is now waiting too, and their caller after that. This is how one slow dependency takes down a system that was otherwise healthy.

**Wait a bounded time — a timeout.** The usual answer, and it does not tell you anything. When the timer fires you know only that you stopped waiting; the peer may have finished, may be about to finish, may be gone. The number is a guess informed by measurement, and it needs revisiting whenever the thing it points at changes.

**Do not wait at all — fire and forget.** Cheap, and honest about what it gives you, which is nothing. Correct when the message is genuinely advisory — a metric, a cache warm, a log line — and wrong the moment anybody would care that it was lost, because nothing anywhere records that it was owed.

**Ask again — retry.** The only option that can turn out well, and the only one that can make things worse. If the first attempt succeeded and its reply was lost, the retry does the work twice.

So retry is the option you want, and it is unsafe as it stands. What makes it safe is on the other end: **the answerer must recognise a retry of something it has already handled, and not do it again.**

```go
// BAD implementation on the server: three deliveries of one request charge three times.
func chargeBad(ledger *Ledger, cents int) {
	ledger.charges = append(ledger.charges, cents)
}
```

```text
BAD  charges: [4200 4200 4200]
```

The fix is that the caller names the attempt, and the server remembers which names it has seen:

```go
// GOOD implementation on the server: the key identifies the attempt, not the delivery.
func chargeIdempotent(ledger *Ledger, idempotencyKey string, cents int) {
	if ledger.applied[idempotencyKey] { // already done — say so, change nothing
		return
	}

	ledger.charges = append(ledger.charges, cents)
	ledger.applied[idempotencyKey] = true
}
```

```text
GOOD charges: [4200]
```

Three deliveries, one charge. The delivery is still at-least-once — nothing fixed that, and nothing can. What changed is that **exactly-once *effect* no longer requires exactly-once *delivery***, which is the same move [chapter 04](04_families-of-law_q5c6.md) identified: the theorem holds, and you stopped needing its conclusion. Systems advertising exactly-once delivery are doing this and not something else — discarding duplicates on arrival — which is why the guarantee holds inside their own boundary and stops at the edge of it.

Two details decide whether this works in practice.

**The key must come from the client**, generated once before the first attempt and reused on every retry. A key the server generates identifies the *delivery*, which is precisely the thing you cannot count.

**The record of applied keys must be written in the same transaction as the effect.** If the charge commits and the key does not, the next retry charges again, and you have moved the bug rather than fixed it.

### What the answerer can do

Those four options belong to whoever is waiting. Stand on the other side — you are the part being asked — and a different set appears, but only if you have more than one copy of the answer.

With one copy there is nothing to decide. The copy is reachable or it is not.

Replicate it and a choice arrives, and it arrives only during a **partition**. Some of your nodes can no longer reach the others, each side is still running, and each is still being asked questions it could answer from what it last knew. You can let them answer, or you can stop them.

**Answer from any node.** Nothing gets slower, no request is refused, and every node serves whatever it last saw. Two clients on opposite sides of the partition can be told different things about the same key, and neither is told that this happened. You are buying response time and paying in answers that are wrong and unmarked.

**Refuse on the minority side.** Reads and writes there hang or fail until the partition heals, so those clients get latency they cannot bound or an error. No client is ever handed a value that was untrue when it was served. You are buying correctness and paying in clients who get nothing.

That is the whole of CAP, and the words in it are narrower than they sound. **Consistency** there means **linearizability** — every read returns the most recent write, as though only one copy had ever existed — which is considerably narrower than the everyday word. **Availability** means every request received by a non-failing node results in a response, with no bound on how long that takes. A stale answer satisfies it.

The choice only exists during a partition, which is why **PACELC** is the more useful statement: *if Partitioned, choose Availability or Consistency; Else, choose Latency or Consistency.* The second half applies every day and the first half only during an outage.

The two branches are not the same trade, which is the part that confuses. During a partition you **cannot** reach the other replicas, so the choice is to answer from what you have or to refuse. Outside a partition you **can** reach them — it only costs time — so the choice is whether to wait for them. Both spend correctness to buy speed; only one of them still has waiting as an option.

**Eventual consistency** is what the first option is usually called, and the name promises less than people hear in it.

It does not mean *consistent soon*. The standard definition is Werner Vogels': **if no new updates are made to a given object, all accesses to that object eventually return the last value written.**

The condition is per object, and that is what makes it sensible rather than absurd. Whole systems never go quiet. Individual rows go quiet constantly — a customer changes their address once and nothing touches that row for a month, so it has converged long before anybody reads it again. For most of your data most of the time, the guarantee comes due and is met.

Where it does not come due is the row under continuous write load, which is usually the row you were worried about. There the quiet moment never arrives and the promise is never tested. So the useful thing is not the guarantee but the gap it leaves, which Vogels names the **inconsistency window**, which is Vogels' term for the period between an update and the moment any observer is guaranteed to see it. Under lazy replication that is simply how long it takes every replica to catch up. That turns the useful questions into measurable ones: how wide does the window get under load, and what is a reader allowed to do inside it. A system where nothing ever reconciles has not chosen eventual consistency. It is wrong, on a delay.

### Two systems cannot share a transaction

This is where it stops being abstract. An order is placed: a row goes in the database, and an event goes on a queue so other services hear about it. Two parts, and no transaction spans them.

```go
func PlaceOrder(ctx context.Context, db *sql.DB, queue Queue, order Order) error {
	if _, err := db.ExecContext(ctx,
		`insert into "order" (id, customer_id, total) values ($1, $2, $3)`,
		order.ID, order.CustomerID, order.Total); err != nil {
		return err // committed on success — the row is durable from here
	}

	// A crash on this line leaves an order nobody will ever hear about.
	return queue.Publish(ctx, OrderPlaced{OrderID: order.ID})
}
```

Swap the two statements and the failure inverts: an event announcing an order that was never stored, and consumers acting on a purchase that does not exist. **There is no ordering of two commits to two systems that is safe**, because whichever goes first, the gap after it is where the process dies.

The **transactional outbox** removes the gap by removing the second system from the critical path. The event is not published — it is *written down*, in the same transaction as the order:

```go
func PlaceOrder(ctx context.Context, db *sql.DB, order Order) error {
	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer tx.Rollback() // no-op once Commit has succeeded

	if _, err := tx.ExecContext(ctx,
		`insert into "order" (id, customer_id, total) values ($1, $2, $3)`,
		order.ID, order.CustomerID, order.Total); err != nil {
		return err
	}

	if _, err := tx.ExecContext(ctx,
		`insert into outbox (id, topic, payload) values ($1, $2, $3)`,
		uuid.New(), "order.placed", order.JSON()); err != nil {
		return err
	}

	return tx.Commit() // both rows, or neither
}
```

Both inserts are inside one transaction against one database, so the commit is atomic by the same mechanism that makes any transaction atomic. Crash before `Commit` and neither row exists. Crash after it and both do. There is no interval in which one is true and the other is not, which is exactly what the two-system version could not offer.

A separate process then drains the table:

```go
func Drain(ctx context.Context, db *sql.DB, queue Queue) error {
	rows, err := db.QueryContext(ctx,
		`select id, topic, payload from outbox order by id limit 100`)
	// ... scan into messages ...

	for _, message := range messages {
		if err := queue.Publish(ctx, message); err != nil {
			return err // leave the row; the next pass retries it
		}

		// Deleted only after the queue has accepted it. A crash between
		// the two republishes on the next pass — which is why this is
		// at-least-once, and why the consumer must be idempotent.
		if _, err := db.ExecContext(ctx, `delete from outbox where id = $1`, message.ID); err != nil {
			return err
		}
	}

	return nil
}
```

**There is deliberately no transaction wrapping the publish and the delete**, and it is worth being clear why, because it is the same impossibility one level down. A transaction can only cover the database; the queue is the other part again. So you choose which way to fail:

- **Publish, then delete.** A crash in between means the message goes twice. At-least-once.
- **Delete, then publish.** A crash in between means the message never goes at all. At-most-once, and the event is gone.

The first is recoverable by an idempotent consumer. The second is unrecoverable — nothing anywhere records that the event was owed. So the outbox publishes first and deletes second, every time, and accepts duplicates as the price.

Notice what actually changed, because it is stronger than a relocation.

**The core problem is gone, not moved.** An order existing without its event is now impossible — not unlikely, impossible — because the two rows commit together or not at all. The *obligation to publish* is itself recorded state rather than something held in a variable in a process that may die.

Before, a crash destroyed information: nothing anywhere knew an event was owed, so no amount of retrying could recover it, and the only repair was a human noticing the discrepancy later. Now a crash costs nothing but time — the row is still there, the next pass of the drain finds it, and the event goes out late rather than never. **A permanent loss became a delay.**

**Sagas** are the same manoeuvre for a longer sequence. When five parts must each do a thing and there is no transaction across them, you do them in order and give each step a compensating action that undoes it. There is no rollback, because there was never a transaction; there is a sequence of forward steps and a sequence of undo steps, and the undo steps are ordinary business operations — refund, cancel, release — with all the visibility that implies. A customer may see a charge and then a refund rather than never seeing a charge.

### Availability is a product, not an average

Parts that can fail independently must all be working at once, and that multiplies.

Ask most people what happens to availability when you add dependencies, and they average: three services at 99.9% feel like a system at about 99.9%. Availability does not average — each dependency must be up *at the same time* as all the others, so you multiply their probabilities, and multiplying numbers below 1 always gives you something smaller than any of them.

A service depending on N others, each independently available with probability p, is available with probability p^N:

```text
each dependency up 99.9%:
     1 dependencies ->  99.90%  (    526 min/yr down)
     5 dependencies ->  99.50%  (   2623 min/yr down)
    10 dependencies ->  99.00%  (   5232 min/yr down)
    50 dependencies ->  95.12%  (  25646 min/yr down)
   100 dependencies ->  90.48%  (  50041 min/yr down)
```

Ten dependencies at three nines gives you two nines. Fifty gives you 95%, which is eighteen hours of downtime a year, from components that are each individually excellent and none of which is at fault.

The fix is not better components — chase 99.99% on all fifty and you still land at 99.5%. The fix is to **stop multiplying**, and there are only three ways:

- **Remove the dependency.** Cache the answer, copy the data, or do without the feature.
- **Make it optional.** If recommendations are down, render the page without them. A dependency you can degrade past shouldn't block your core product.
- **Make it asynchronous.** A queue you write to is a dependency; a queue you write to *through an outbox* is not, because your transaction commits without it.

One caveat, because the arithmetic assumes the dependencies fail independently and often they do not. Two services in the same rack, on the same power, sharing a certificate that expires on the same day fail together rather than separately, which makes the real number worse than p^N when the shared thing goes and better when it does not. Use p^N to notice that ten dependencies is a different system from two. Do not use it to promise a number to anyone.

---

## Why the claim holds

Three theorems sit underneath all of it. CAP is the one already worked through above; all three are set out here with their assumptions rather than their proofs, because the assumptions are the only negotiable part.

**Two Generals.** Over a channel that can lose messages, no protocol can leave both parties certain the other received what was sent
- *Assumes:* messages can be lost.
- *Consequence:* exactly-once delivery is impossible, so at-least-once plus a repeatable effect is the best available.

**FLP impossibility.** In an asynchronous system where even one process may crash, no deterministic protocol can guarantee that all correct processes reach agreement.
- *Assumes:* no bound on message delay, no clocks, a deterministic algorithm — and, worth noticing, **a channel that delivers every message**. FLP does not need lost messages. It needs only that a message can be arbitrarily slow and that one process can crash.

That last point looks like it contradicts the definitions above, and it is worth seeing why it does not. A message that can be delayed without bound produces exactly what this chapter calls a partition — the waiter cannot reach the other part within the time it is willing to wait — without a single message being lost. FLP's channel is reliable only in the sense of *eventually*, and *eventually* with no bound on it is the thing the claim says you cannot tell from *never*. A perfect network is no rescue because perfection here means delivery, not punctuality.
- *Consequence:* **no consensus system can promise that it will decide.** In practice that is a cluster which cannot elect a leader and makes no progress, while every node is running and nothing is permanently broken. Raft and Paxos do not evade this — they add timeouts, which trades guaranteed *termination* for guaranteed *safety*. They may take longer; they will not decide two different things.

**CAP.** A replicated value held to linearizability cannot also be answered by every non-failing node during a partition.

- *Assumes:* linearizability, and availability as defined above.
- *Consequence:* the choice worked through earlier — answer from what you have, or refuse.

All three share one root, which is the claim at the top. A lost message and a late message look identical. A crashed process and a paused one look identical. A partitioned peer and a dead peer look identical. **The impossibility is always that you must act on information you cannot obtain**, and no protocol reads the future.

That is also why every fix in this chapter has the same shape, and naming it gives you a test for your own designs. **They convert uncertainty you can never resolve into uncertainty you can resolve later.**

- **An idempotency key.** You still cannot know whether the charge landed. You can ask again, and asking costs nothing.
- **The outbox.** You still cannot know whether the publish succeeded. The row is still there, so the next pass finds out.
- **A retry.** You cannot know, so you stop trying to know and find out by asking.
- **Consensus with timeouts.** You cannot know, so you stall rather than decide wrongly, and decide when you can.

None of these acquires the missing information. Each arranges for it to stop being final. So the question to ask of your own design is not *have I handled the failure* but: **after this fix, is the thing I cannot confirm something I can find out later, or is it gone?**

That test settles the outbox's drain order by itself. Publish-then-delete leaves a row you can retry. Delete-then-publish leaves nothing anywhere recording that the event was owed, and no amount of monitoring recovers information that was never written down.

---

## Where the claim doesn't apply

### One machine

The obvious case is a single process, where a function call cannot suffer a lost message. The sharper case is **two separate processes on one machine, communicating through shared memory** — genuinely two parts, each able to crash without the other, and Two Generals is still inert. A write to the shared segment is not a delivery that can fail. The reader acknowledges by writing back, and that cannot be lost either, so mutual certainty is reachable in a finite exchange, which is exactly what the theorem forbids over a lossy channel.

One machine escapes the waiting problem as well, and this is the part usually left out. Within one machine you *can* tell late from never, because the kernel knows. `waitpid` reports that a child has died. A robust mutex returns `EOWNERDEAD` to the next process that takes it when its previous holder died while holding it. **The operating system is a perfect failure detector for the processes it owns.** Both preconditions are absent, which is why one machine is not a smaller distributed system but a different situation.

**TCP is where people expect this exemption to extend and it does not**, which is worth stating here rather than leaving as an assumption. TCP gives you *delivered in order, or the connection breaks*. It converts message loss into connection failure, relocating the uncertainty instead of removing it: a client whose connection drops after sending a request still does not know whether the server processed it. A reliable transport over an unreliable network is still an unreliable channel between two parts.

Which is why **one connection is not an exemption**, and it is where the boundary gets drawn wrongly most often. An application and its database are two parts joined by a channel that can fail while both survive. Send a `COMMIT`, lose the connection before the reply arrives, and the transaction may have committed or may not have; the application cannot tell from where it stands. That is Two Generals, in the least distributed system anyone builds.

Be precise about when this bites, because it is narrower than it sounds. If the database is genuinely down, there is no decision to make — the request fails and you say so. The awkward case is the other one: **the database is fine and the connection is not**, so the write may well have committed while the application sits there unable to find out.

This is documented rather than theoretical. PostgreSQL's own position is that once `COMMIT` has been sent and the connection drops, there is no way to tell whether it succeeded, and a client library can do nothing but warn and decline to retry. Entity Framework documents the same case and ships a handler for it, and the mitigation the database vendors recommend where certainty is required is the one described earlier in this chapter: an identifier generated by the client, written inside the same transaction under a unique constraint, so a retry either applies once or collides with itself.

What you will rarely find is application code that checks. The rule most teams already follow — **do not blindly retry a write after a connection error** — is this problem handled by avoidance, which is why it seldom appears as a bug and seldom appears as code. Avoidance costs you the write: the outcome stays unknown and a human resolves it. That is affordable at one write and not at ten thousand.

What makes even avoidance possible is that the uncertainty here is **recoverable**. The database is durable and can be asked, whether by a person the next morning or by a client that reconnects. That is the whole difference between this and a lost message to a peer that kept no record of it.

### Coordination you can afford

Distributed transactions are not impossible. Two-phase commit — 2PC — exists, works, and is used — in payment networks, in some databases, wherever the cost is justified. What it costs is availability. Each participant is asked to vote first and commit second, and between those two steps it is holding its locks and has promised to be able to finish. If the **coordinator** fails in that gap, every participant that voted yes is stuck: it cannot commit, because the coordinator may have told the others to abort, and it cannot abort, because it promised to commit if asked. They hold their locks until the coordinator returns or an operator intervenes. A participant failing is the easy case by comparison — the coordinator aborts, tells everyone else, and the absentee learns the outcome when it comes back.

So the honest statement is not "you cannot have cross-system atomicity." It is that you can, and the price is that a failure anywhere stops everything, which for most systems is a worse outcome than the inconsistency they were avoiding. When it is not — few enough participants, high enough stakes, an operator on call — 2PC is the right answer and the sagas are the cargo cult.

---

## What the claim costs

**Idempotency keys cost a table, a lookup, and a retention policy.** Keys must be stored to be checked, stored keys grow forever, and deleting them re-opens the window for any client slow enough to retry after the deletion. Nobody enjoys choosing that number.

**The outbox costs a polling loop and ordering questions.** Something must drain the table, which is a process to run and monitor. Messages arrive at least once and, without care, out of order — so consumers need to handle both, which is work in every consumer rather than once in the producer.

**Sagas cost the illusion of atomicity, visibly.** Compensations are business operations, so customers see them. A refund is not a rollback, and a cancelled booking that briefly existed is not the same as one that never did. Somebody has to decide whether that is acceptable, and it is not an engineering decision.

**Every one of these is a problem you introduced by adding a part.** The costs above buy back a fraction of what a single database gave away for free. That is sometimes worth it, and it is worth being clear-eyed that the trade was made rather than discovered.

**Timeouts are a tuning problem with no correct answer.** Too short and you retry work that succeeded; too long and failures take the caller down with them. The number is a guess informed by measurement, and it needs revisiting whenever the thing it points at changes.

---

## How to recognize the failure

**In a codebase:**

- **A write to a database followed by a publish to a queue**, in the same function, with no outbox. The gap between them is a lost event, and it fires on every deploy that restarts a process mid-request.
- **Retries with no idempotency key**, so the retry policy is also a duplication policy.
- **An idempotency key generated by the server**, which identifies the delivery rather than the attempt and therefore counts the thing that cannot be counted.
- **An applied-keys table written outside the transaction that performs the effect.**
- **A health check that reports a dependency up because a TCP connection opened**, which distinguishes nothing — a process can accept connections and answer none of them.
- **A call with no deadline on it**, which is the wait-forever option chosen by not choosing.
- **Retries without jitter**, which converts one failure into a synchronized stampede on recovery.
- **An availability target quoted for a service with thirty synchronous dependencies**, arrived at without multiplying anything.

**In a conversation:**

- **"We'll just make it exactly-once."** The correct response is to ask what happens on the retry, since there will be one.
- **"The timeout must be too short."** Sometimes. But if the peer completes the work after the timeout fires, no timeout is long enough, and the problem is the missing idempotency key.
- **"We need distributed transactions for this"** — said about two tables in one database.
- **"It's eventually consistent"** used to describe a system where nothing reconciles, which makes it eventually wrong.
- **"Let's add a health check"** offered as the answer to a request that timed out, which reports the present about a question concerning the past.
- **"Each service is 99.9%"**, offered as though the product were also 99.9%.

The question that does the work: **what does this code do when the reply never comes?**

Every defect in the list above is an answer to that question that nobody wrote down. If the honest answer is *it retries and the work happens twice*, you need an idempotency key. If it is *it gives up and the work happened anyway*, you need reconciliation. And if it is *the reply always comes, we are in one process*, then none of this is yours.

[Chapter 09](09_scale_637f.md) turns from what is impossible to what is merely expensive — the arithmetic of queues, parallelism, and contention.

---

## Sources

- Michael J. Fischer, Nancy A. Lynch, Michael S. Paterson, *Impossibility of Distributed Consensus with One Faulty Process* — Journal of the ACM 32(2), April 1985. [PDF](https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf).
- Seth Gilbert, Nancy Lynch, *Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services* — ACM SIGACT News 33(2), June 2002. [PDF](https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf).
- Daniel J. Abadi, *Consistency Tradeoffs in Modern Distributed Database System Design* — IEEE Computer 45(2), February 2012. [PDF](https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf).
- Werner Vogels, *Eventually Consistent* — allthingsdistributed.com, December 2007; later in Communications of the ACM 52(1), January 2009. [allthingsdistributed.com](https://www.allthingsdistributed.com/2007/12/eventually_consistent.html).
- *Handling transaction commit failures* — Entity Framework 6 documentation, Microsoft Learn. [learn.microsoft.com](https://learn.microsoft.com/en-us/ef/ef6/fundamentals/connection-resiliency/commit-failures).

---

[← Ch. 07](07_time_mdbn.md)  ·  [Contents](00_toc.md)  ·  [Ch. 09 →](09_scale_637f.md)
