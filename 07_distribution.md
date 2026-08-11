# Distribution: What's Impossible

*This chapter is **Law** of the strictest kind (Ch. 04): theorems, with proofs and stated assumptions. The material is therefore not advice, cannot be argued with, and leaves exactly two moves.*

- **Arrange for an assumption not to hold**, and the theorem does not apply to you.
- **Stop needing the conclusion**, and the theorem applies but costs you nothing.

Most of this chapter is the second one.

## The claim

**You cannot tell a slow machine from a dead one.**

That single fact is not a limitation of your monitoring, your language, or your budget. It is a property of asking questions over a network, and most of the impossibility results in distributed systems are consequences of it. The rest of the chapter is what people build because of it.

There is one other fact, which is arithmetic rather than epistemics: **availabilities multiply, and every one of them is less than one.** Multiplying numbers below 1 makes them smaller, so a chain of dependencies is always less available than its weakest link — and enough individually excellent dependencies produce a system that is not.

## When any of this applies to you

Most chapters in this book put the limits of their claim at the end. This one puts them first, and the reason is that this particular material does more damage by being applied than by being ignored. Outboxes, idempotency keys, sagas, and eventual consistency get built into systems that have one process and one database, where every one of them is pure cost. So it is worth knowing whether any of this is yours before you read what it costs.

You are in this chapter's territory when **two things that can fail independently must agree.** Two processes. A process and a queue. A service and somebody else's API. A database and a cache. If there is exactly one process and one database, almost nothing here binds, and the machinery below is cost with no purchase — chapter 06 is your chapter, and its coordination primitives are enough.

The test for whether you are distributed is not *do we deploy several services* — plenty of multi-service systems still have one database holding every invariant that matters. It is: **can one part of this be alive while another part cannot reach it?** If nothing can, you are not distributed for the purposes of this chapter, whatever the deployment diagram says.

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

This is the same shape as chapter 04's lost acknowledgement, generalized. There the reply was lost; here the reply is merely late. **The client cannot tell those apart either**, and it does not need to — from where it stands, silence is silence.

### The theorems, and what each one assumes

Three results. Each is given with its assumptions rather than its proof, because the assumptions are the part you can do something about.

**Two Generals.** Over a channel that can lose messages, no protocol can leave both parties certain the other received what was sent. *Assumes:* messages can be lost. *Consequence:* exactly-once delivery is impossible.

**FLP impossibility**, named for Fischer, Lynch, and Paterson, who proved it in 1985. In an asynchronous system where even one process may crash, no deterministic protocol can guarantee that all correct processes reach agreement. *Assumes:* no bound on message delay, no clocks, and a deterministic algorithm. *Consequence:* consensus algorithms in real use (Raft, Paxos) do not evade FLP — they add timeouts, which means they give up guaranteed *termination* and keep guaranteed *safety*. They may take longer; they will not decide two different things.

**CAP**, for Consistency, Availability, and Partition tolerance. In an asynchronous network, a linearizable register cannot also be available during a partition. *Assumes:* linearizability, and availability meaning every non-failed node answers. *Consequence:* during a partition you choose. Outside a partition you have both, which is why **PACELC** is the more useful statement: *if Partitioned, choose Availability or Consistency; Else, choose Latency or Consistency.* The second half applies every day, and the first half only during an outage.

All three share one root, which is the claim at the top. A lost message and a slow message look identical. A crashed process and a paused one look identical. A partitioned peer and a dead peer look identical. **The impossibility is always that you must act on information you cannot obtain.**

### Exactly-once is impossible, so stop wanting it

Given that the client cannot know, retrying is the only responsible thing it can do. So the effect must be safe to repeat on the server.

```go
// BAD, on the server: three deliveries of one request charge three times.
func chargeBad(l *Ledger, cents int) {
	l.charges = append(l.charges, cents)
}
```

```text
BAD  charges: [4200 4200 4200]
```

The fix is that the caller names the attempt, and the server remembers which names it has seen:

```go
// GOOD, on the server: the key identifies the attempt, not the delivery.
func chargeIdempotent(l *Ledger, key string, cents int) {
	if l.applied[key] { // already done — say so, change nothing
		return
	}

	l.charges = append(l.charges, cents)
	l.applied[key] = true
}
```

```text
GOOD charges: [4200]
```

Three deliveries, one charge. The delivery is still at-least-once — nothing fixed that, and nothing can. What changed is that **exactly-once *effect* no longer requires exactly-once *delivery***, which is the same move chapter 04 identified: the theorem holds, and you stopped needing its conclusion.

Two details decide whether this works in practice.

**The key must come from the client**, generated once before the first attempt and reused on every retry. A key the server generates identifies the *delivery*, which is precisely the thing you cannot count.

**The record of applied keys must be written in the same transaction as the effect.** If the charge commits and the key does not, the next retry charges again, and you have moved the bug rather than fixed it.

### Two systems cannot share a transaction

This is where the theorems stop being abstract. An order is placed: a row goes in the database, and an event goes on a queue so other services hear about it. Two systems, and no transaction spans them.

```go
func PlaceOrder(ctx context.Context, db *sql.DB, q Queue, o Order) error {
	if _, err := db.ExecContext(ctx,
		`insert into "order" (id, customer_id, total) values ($1, $2, $3)`,
		o.ID, o.CustomerID, o.Total); err != nil {
		return err // committed on success — the row is durable from here
	}

	// A crash on this line leaves an order nobody will ever hear about.
	return q.Publish(ctx, OrderPlaced{OrderID: o.ID})
}
```

Swap the two statements and the failure inverts: an event announcing an order that was never stored, and consumers acting on a purchase that does not exist. **There is no ordering of two commits to two systems that is safe**, because whichever goes first, the gap after it is where the process dies.

The **transactional outbox** removes the gap by removing the second system from the critical path. The event is not published — it is *written down*, in the same transaction as the order:

```go
func PlaceOrder(ctx context.Context, db *sql.DB, o Order) error {
	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer tx.Rollback() // no-op once Commit has succeeded

	if _, err := tx.ExecContext(ctx,
		`insert into "order" (id, customer_id, total) values ($1, $2, $3)`,
		o.ID, o.CustomerID, o.Total); err != nil {
		return err
	}

	if _, err := tx.ExecContext(ctx,
		`insert into outbox (id, topic, payload) values ($1, $2, $3)`,
		uuid.New(), "order.placed", o.JSON()); err != nil {
		return err
	}

	return tx.Commit() // both rows, or neither
}
```

Both inserts are inside one transaction against one database, so the commit is atomic by the same mechanism that makes any transaction atomic. Crash before `Commit` and neither row exists. Crash after it and both do. There is no interval in which one is true and the other is not, which is exactly what the two-system version could not offer.

A separate process then drains the table:

```go
func Drain(ctx context.Context, db *sql.DB, q Queue) error {
	rows, err := db.QueryContext(ctx,
		`select id, topic, payload from outbox order by id limit 100`)
	// ... scan into msgs ...

	for _, m := range msgs {
		if err := q.Publish(ctx, m); err != nil {
			return err // leave the row; the next pass retries it
		}

		// Deleted only after the queue has accepted it. A crash between
		// the two republishes on the next pass — which is why this is
		// at-least-once, and why the consumer must be idempotent.
		if _, err := db.ExecContext(ctx, `delete from outbox where id = $1`, m.ID); err != nil {
			return err
		}
	}

	return nil
}
```

**There is deliberately no transaction wrapping the publish and the delete**, and it is worth being clear why, because it is the same impossibility one level down. A transaction can only cover the database; the queue is the other system again. So you choose which way to fail:

- **Publish, then delete.** A crash in between means the message goes twice. At-least-once.
- **Delete, then publish.** A crash in between means the message never goes at all. At-most-once, and the event is gone.

The first is recoverable by an idempotent consumer. The second is unrecoverable — nothing anywhere records that the event was owed. So the outbox publishes first and deletes second, every time, and accepts duplicates as the price.

Notice the shape. **The impossibility was not defeated:** you still cannot tell a slow machine from a dead one, and the publisher still cannot know whether the queue received what it sent. What changed is that the *hard* half — an order existing without its event — moved inside one database, where atomicity is available, and the half left outside was reduced to duplicate delivery, which a consumer can absorb.

**Sagas** are the same manoeuvre for a longer sequence. When five services must each do a thing and there is no transaction across them, you do them in order and give each step a compensating action that undoes it. There is no rollback, because there was never a transaction; there is a sequence of forward steps and a sequence of undo steps, and the undo steps are ordinary business operations — refund, cancel, release — with all the visibility that implies. A customer may see a charge and then a refund rather than never seeing a charge.

### Availability is a product, not an average

The arithmetic one, and it is worth being slow about because the intuition is wrong.

Ask most people what happens to availability when you add dependencies, and they average: three services at 99.9% feel like a system at about 99.9%. Availability does not average, it multiplies — each dependency must be up *at the same time* as all the others, so you multiply their probabilities, and multiplying numbers below 1 always gives you something smaller than any of them.

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

That third one is why the outbox appears in a chapter about availability as well as one about correctness.

---

## Why it holds

Every result above is the same shape: **an actor must decide, and the information needed to decide correctly is on the other side of a link that may not deliver.**

The reason no cleverness escapes it is that the missing information is not merely absent, it is *unobtainable in principle*. To know whether a peer is dead you would have to distinguish "no message yet" from "no message ever," and those differ only in the future. No protocol reads the future, so every practical system substitutes a timeout, which is a guess with a number attached.

That is also why the successful patterns share a structure. Idempotency keys, outboxes, sagas, and consensus with timeouts do not acquire the missing information. They **rearrange the system so the missing information stops mattering** — by making repetition harmless, by making one commit stand for two, by making a partial sequence recoverable, by preferring to stall over deciding wrongly.

The arithmetic result is different and worth separating. p^N is not about knowledge; it is about independent events. You cannot rearrange your way out of multiplication, only remove terms from the product.

---

## Where this doesn't apply

### One process and one database

The important one, and the most frequently ignored.

A single application server talking to a single Postgres has no partition to survive, no consensus to reach, and no cross-system atomicity problem, because the database provides atomicity and the application has nothing to coordinate with. Two Generals is true and inert; CAP has no register to make unavailable; FLP has no agreement to reach.

Reaching for this chapter's machinery there produces real harm rather than mere waste:

- An outbox table where a single transaction already covers everything.
- Idempotency keys on operations that only ever run once, adding a table and a lookup to every write.
- Eventual consistency between two tables in the same database, which had strong consistency available for free.
- Retries around an in-process function call, which cannot suffer a lost message (Ch. 06).

The check is the one at the top: can one part be alive while another part cannot reach it? Within one process and one connection, no.

### Coordination you can afford

Distributed transactions are not impossible. Two-phase commit — 2PC — exists, works, and is used — in payment networks, in some databases, wherever the cost is justified. What it costs is availability: a participant that fails while holding a prepared transaction blocks the others until it returns or an operator intervenes.

So the honest statement is not "you cannot have cross-system atomicity." It is that you can, and the price is that a failure anywhere stops everything, which for most systems is a worse outcome than the inconsistency they were avoiding. When it is not — few enough participants, high enough stakes, an operator on call — 2PC is the right answer and the sagas are the cargo cult.

### Failures that are not independent

The p^N arithmetic assumes dependencies fail independently. Often they do not, and the assumption fails in both directions.

Two services in the same rack, on the same power, behind the same load balancer, sharing a certificate that expires on the same day, are not independent. Their combined availability is worse than the arithmetic suggests when the shared thing fails, and better when it does not, because they fail together rather than separately.

Which means p^N is a *lower bound on the problem* rather than a prediction. Use it to notice that ten dependencies is a different system from two. Do not use it to promise a number to anyone.

---

## What it costs

**Idempotency keys cost a table, a lookup, and a retention policy.** Keys must be stored to be checked, stored keys grow forever, and deleting them re-opens the window for any client slow enough to retry after the deletion. Nobody enjoys choosing that number.

**The outbox costs a polling loop and ordering questions.** Something must drain the table, which is a process to run and monitor. Messages arrive at least once and, without care, out of order — so consumers need to handle both, which is work in every consumer rather than once in the producer.

**Sagas cost the illusion of atomicity, visibly.** Compensations are business operations, so customers see them. A refund is not a rollback, and a cancelled booking that briefly existed is not the same as one that never did. Somebody has to decide whether that is acceptable, and it is not an engineering decision.

**Every one of these is a distributed problem you introduced by distributing.** The costs above buy back a fraction of what a single database gave away for free. That is sometimes worth it, and it is worth being clear-eyed that the trade was made rather than discovered.

**Timeouts are a tuning problem with no correct answer.** Too short and you retry work that succeeded; too long and failures take the caller down with them. The number is a guess informed by measurement, and it needs revisiting whenever the thing it points at changes.

---

## How to recognize the failure

**In a codebase:**

- **A write to a database followed by a publish to a queue**, in the same function, with no outbox. The gap between them is a lost event, and it fires on every deploy that restarts a process mid-request.
- **Retries with no idempotency key**, so the retry policy is also a duplication policy.
- **An idempotency key generated by the server**, which identifies the delivery rather than the attempt and therefore counts the thing that cannot be counted.
- **An applied-keys table written outside the transaction that performs the effect.**
- **A health check that reports a dependency up because a TCP connection opened**, which distinguishes nothing — a process can accept connections and answer none of them.
- **Retries without jitter**, which converts one failure into a synchronized stampede on recovery.
- **An availability target quoted for a service with thirty synchronous dependencies**, arrived at without multiplying anything.

**In a conversation:**

- **"We'll just make it exactly-once."** The correct response is to ask what happens on the retry, since there will be one.
- **"The timeout must be too short."** Sometimes. But if the peer completes the work after the timeout fires, no timeout is long enough, and the problem is the missing idempotency key.
- **"We need distributed transactions for this"** — said about two tables in one database.
- **"It's eventually consistent"** used as a description of a system where nothing reconciles, which makes it eventually wrong.
- **"Each service is 99.9%"**, offered as though the product were also 99.9%.

The question that does the work: **what does this code do when the reply never comes?**

Every distributed defect in the list above is an answer to that question that nobody wrote down. If the honest answer is *it retries and the work happens twice*, you need an idempotency key. If it is *it gives up and the work happened anyway*, you need reconciliation. And if the answer is *the reply always comes, we're in one process*, then none of this is yours and you should stop reading.

---

**Next:** chapter 08 turns from what is impossible to what is merely expensive — the arithmetic of queues, parallelism, and the memory hierarchy, where the numbers beat the intuition by several orders of magnitude.
