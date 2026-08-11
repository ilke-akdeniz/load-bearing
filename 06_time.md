# Time: Concurrency and Clocks

*This chapter is **Law**, and mostly of the definitional kind (Ch. 04) — its claims are true by what the words pick out, which is why they cannot be argued with and why they are so easy to walk past. It has two halves that look like separate subjects and are not.*

## The claim

**A check tells you what was true, not what is true. And no clock tells you what happened first.**

Both halves are the same fact wearing different clothes: **there is no shared now.** Inside one machine that means your observation is already stale when you act on it. Across machines it means there is no agreed ordering of events at all, and the timestamps you would use to build one are not up to the job.

This is the chapter that turns *be careful with shared state* into something you can check.

## When this is actually a problem

Say the claim out loud and it sounds like every line of code is in danger. It is not, and it is worth fixing that before the alarming part, because the alarm is what makes people either ignore this material or over-apply it.

Reading state and then acting on it is only a problem when **all three** of these hold:

1. **Something else can write that state** between your read and your act.
2. **Your decision depends on what you read** — you are not just reporting it.
3. **The rule spans data you did not hold still** — other rows, other keys, other files.

Miss any one and there is nothing here to fix. Reading configuration at startup in a single-threaded process, reading a row you already hold a lock on, reading a value only you ever write, reading anything immutable — all safe, and all extremely common. Most read-then-act sequences in most programs are in this category.

When all three do hold, the fix is almost always one of three ordinary moves, and all three appear below:

- **Do the whole thing in one operation**, so nothing can happen in between.
- **Let the component holding the data enforce the rule**, usually the database.
- **Do not check at all** — attempt the thing, and handle the failure.

None of those is exotic, and none costs much. The reason this chapter is long is that recognizing the shape is harder than fixing it.

---

## The demonstration

### Check-then-act is not atomic

A registration handler. It refuses duplicate emails, and the code says so plainly:

```go
// Every step here is individually safe. The sequence is not.
func (s *Store) Register(email, password string) {
	if s.exists(email) { // CHECK
		return
	}

	hashPassword(password) // the work every real handler does here
	s.insert(email)        // ACT
}
```

`exists` and `insert` each take a mutex internally — a lock that lets one goroutine at a time touch the map, the way `synchronized` does in Java or `lock` in C#:

```go
func (s *Store) exists(k string) bool {
	s.mu.Lock()         // no other goroutine may touch rows until Unlock
	defer s.mu.Unlock() // defer runs this when the function returns
	_, ok := s.rows[k] // [claude I fail to grash how email reagistration works. Is there a rows map where each email has a count? And the count can only be 1 at most? Why? If this is just random code? Maybe try making this example more meaningful and recognizable, like an email saved to a csv file or db for example. Or if the point is to show how this issue is in play witohut even a db or file, just find a business that fits better with that in memory persistence case.] 

	return ok
}

func (s *Store) insert(k string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.rows[k]++
}
```

Neither can corrupt the map. Both are correct.

Fifty concurrent registrations for the same address:

```text
rows for one email, with a uniqueness check before every insert: 50
```

Not two. Fifty. Every request checked, every request found the address free, and every request was right at the moment it looked. Then each spent two milliseconds hashing a password, and by the time the first insert landed, the other forty-nine had already made their decision.

Three things are worth taking from that number.

**Locking each step protects each step and nothing else.** The map was never corrupted. What broke was a rule that spans two operations, and no amount of locking inside them can span them.

**The window is as wide as the work you do in it.** Remove the password hashing and the same code produces one row on this machine, most of the time — which is worse, not better, because the bug is still there and now it only appears under load, in production, when the machine is busy.

**Nothing in the code looks wrong.** There is no missing lock to spot in review. The defect is in the shape — a decision made from a reading, and an action taken later — and that shape is invisible if you are looking for unguarded variables.

And here is the whole fix, which is the first of the three moves:

```go
// One operation. The decision and the write are inseparable.
func (s *Store) RegisterAtomic(email, password string) bool {
	hashPassword(password) // slow work first, before taking the lock
	s.mu.Lock()
	defer s.mu.Unlock()

	if _, taken := s.rows[email]; taken { // CHECK
		return false
	}
	s.rows[email]++ // ACT, with nothing able to intervene

	return true
}
```

```text
BAD  register: 50
GOOD register: 1
```

Nothing was added and nothing became slower. The check moved *inside* the same lock as the write, so no other goroutine can act between them, and the hashing moved out so the lock is held for the length of a map lookup rather than two milliseconds.

That is the shape of the ordinary fix: **not more locking, but locking the right span.**

### The same bug, in whatever language you own

The shape does not belong to Go, or to databases. Here it is against the filesystem, which is where the name **TOCTOU** — time of check to time of use — comes from:

```python
if os.path.exists(path):    # CHECK
    time.sleep(0.005)       # any work at all
    open(path).read()       # ACT
```

Something deletes the file during those five milliseconds:

```text
BAD : check said it existed; open failed with FileNotFoundError
```

The fix is the third move — do not check at all:
[claude this example is really of the mark. 
I don't see any difference between bad and good version, I only see python's syntaxtic sugar that
gives you the FileNotFoundError in one statement. I'm tyring to imagine a code where this would make sense, maybe if you add true meaningfull work instead of "time.sleep" and show how that work spoiled and 
how the second version doesn't let that happen this could work.]

```python
try:
    data = open(path).read()   # ACT. The attempt is the check.
except FileNotFoundError:
    ...                        # handle the case you were checking for
```

```text
GOOD: handled cleanly — no window, because there was no check
```

There is no window because there is no gap: the operating system opens the file or does not, in one step, and tells you which. Python calls this style *easier to ask forgiveness than permission*, and this is the situation it exists for.

The same bug in SQL, where it is most common of all:

```sql
select count(*) from account where email = $1;   -- CHECK
-- application decides
insert into account (email) values ($1);         -- ACT
```

And the same fix, this time the second move — hand the rule to whoever holds the data:

```sql
-- Declared once, when the table is created.
create unique index ux_account_email on account (lower(email));

-- After which the insert is its own check.
insert into account (email) values ($1)
on conflict do nothing;
```

And in C#, Java, or anything else with two statements and a gap between them. **The bug survives every translation, because it is not about the language** — and so does the fix, because in every case it is the same move: make the decision and the action one thing.

### Shared mutable state plus concurrency equals races

The narrower, more famous case. A thousand goroutines, each adding one:

```go
count := 0

for i := 0; i < 1000; i++ {
	wg.Add(1)

	// `go` starts this function on its own goroutine — a thread, for
	// present purposes. All thousand of them share the one `count`.
	go func() {
		defer wg.Done()
		count++
	}()
}
```

```text
BAD  counter: 968
```

Run it again and it produces 961. The count is wrong, differently, every time. `count++` is not one operation — it reads, adds, and writes back, and two goroutines that read the same value both write the same result, so one increment vanishes.

The fix is one instruction, and it is the first move again — make the read, the add, and the write a single thing nothing can split:

```go
var safe int64

atomic.AddInt64(&safe, 1) // one indivisible operation
```

```text
GOOD counter: 1000
```

Exactly a thousand, every run. This is `Interlocked.Increment` in C# and `AtomicLong.incrementAndGet` in Java, and it is not a lock — the processor guarantees the read, the add, and the write happen as a unit.

That is the cheap fix for one number. For the general case, the equation in the heading has three terms, and you only have to remove one:

**Remove the sharing.** Each worker gets its own counter, and one place adds them up at the end. This is the fix that scales, because it removes contention as well as the race.

**Remove the mutability.** Nobody writes to anything anyone else can see. Values go in, new values come out.

The third term, concurrency, is usually the reason the program exists, so it is the one you cannot give up. That is why the practical advice is always about the other two — and why "just add a lock" is a fourth thing, which serializes the race rather than removing it, and brings the costs in the last section.

### Only the lock-holder can enforce

The registration fix above works because one mutex covered both steps. Two processes cannot share a mutex, so raise the same move up a level:

```sql
create unique index ux_account_email on account (lower(email));
```

The rule is now checked by the component that holds the row locks, at the instant of the write. There is no window, because there is no separate check — the decision and the write are one statement, and the loser of a race gets an error rather than a duplicate row.

**The general rule, and it is the useful one:** a rule about data can only be enforced by whatever can see all of that data and stop it changing. Application code cannot enforce uniqueness across rows it has not read and cannot hold still. It is not that the database is a *better* place for the rule — it is the only place the rule can be true.

There is a corollary worth stating separately, because it is the part people resist: **an application-level check is not wrong, but it is not the enforcement.** Keep it, because it produces a good error message and saves a round trip in the common case. Do not count it as the guarantee, and do not remove the constraint because the check is there.

### The single-writer principle

The strongest version of removing the sharing. If exactly one thread, process, or partition ever writes a piece of state, then no write can interleave with another, and the entire apparatus above becomes unnecessary — no locks, no atomics, no constraint to enforce.

This is why partitioned designs are fast. A queue consumer that owns its partition, an actor that owns its state, a shard that owns its key range — each is a single writer, and the coordination cost is zero because there is nothing to coordinate with.

The price is that the partition is now part of your design, permanently. Any operation spanning two partitions is back to needing coordination, and the boundaries are difficult to move once data has accumulated behind them (Ch. 03, on why that decision expires).

### Clocks do not order events

The second half, and it surprises people who accept the first half easily.

The intuition is that if event A has an earlier timestamp than event B, A happened first. Start with one machine — no network, no skew, one process — and ask whether the clock can even distinguish two adjacent events:

```go
a := time.Now().UnixNano()
b := time.Now().UnixNano()
```

Two hundred thousand times:

```text
consecutive Now() pairs with an identical wall-clock value: 189090 of 200000 (95%)
smallest non-zero gap observed: 1000 ns
```

Python agrees, to within a percent. **Ninety-five per cent of the time, two consecutive readings of the clock are the same number.** The wall clock on this machine advances in one-microsecond steps, and anything finer than that is invisible to it. Two events a hundred nanoseconds apart do not get an order — they get the same timestamp.

That is on one machine, before anything has gone wrong. Now add the things that do go wrong:

- **Skew.** Two machines' clocks disagree, typically by milliseconds under NTP and by far more when NTP is broken, which it silently is more often than anyone assumes.
- **Jumps.** The wall clock is corrected, and moves *backwards*. A timestamp taken after another can be smaller than it.
- **No relationship to causality.** Even with perfectly synchronized clocks, an earlier timestamp does not mean an earlier cause. It means the two events were stamped in that order.

Which is why comparing timestamps from two machines to decide what happened first is not a slightly imprecise technique. It is the wrong kind of instrument, and it fails in the direction that produces silent data loss: last-write-wins, where the loser is whoever had the slower clock.

The fix for most systems is smaller than the problem sounds. **Ask one component for the order, rather than asking each machine what time it thinks it is:**

```sql
-- BAD: whoever's clock is fast wins, and nobody is told.
update doc set body = $1, updated_at = $2   -- $2 from the client
 where id = $3;

-- GOOD: one clock, one sequence, and a stale writer is refused.
update doc set body = $1, version = version + 1
 where id = $2 and version = $3;            -- $3 is what the writer read
```

The second is optimistic concurrency control, and it needs no clock at all: the version number is a counter, the database is the single authority that increments it, and a writer working from a stale read matches zero rows and is told so. A database sequence, a monotonically increasing transaction id, or `now()` evaluated on the server all do the same job — **one source of order, rather than several sources of approximate time.**

That is enough for the large majority of systems, which have one database. The apparatus in the next section is for when you do not.

### What does order events

When there is no single authority to ask — several databases, several regions, offline clients that reconcile later — the answer is still counters rather than clocks.

A **Lamport clock** is a number per node, incremented on every event, and sent along with every message; a receiver takes the larger of its own value and the one it received, then adds one:

```go
func (n *Node) local() int { n.clock++; return n.clock }

func (n *Node) recv(stamp int) int {
	if stamp > n.clock {
		n.clock = stamp
	}
	n.clock++

	return n.clock
}
```

```text
lamport: A's write=1  B's receipt=2  B's next=3  (A before B, always)
```

Whatever the two machines' wall clocks say, B's receipt carries a number larger than A's write, because B saw A's message. Causality is preserved by construction rather than by hoping the clocks agree.

What a Lamport clock does *not* give you is the reverse reading: a smaller number does not prove an event came first, only that it did not come after. Two unrelated events can carry any numbers at all. **Vector clocks** — one counter per node, carried as a set — recover the missing information: they can tell you that two events are concurrent, meaning neither caused the other, which is exactly the case where last-write-wins is silently choosing a winner. The cost is a value that grows with the number of nodes.

---

## Why it holds

Both halves reduce to one property of the world: **an observation is a statement about the past.**

The moment you read a value, that reading describes a state that may already be gone. Nothing about being careful changes this — the gap between reading and acting is where instructions execute, and instructions take time. A lock does not abolish the gap; it stops anyone else from using it, which is a different and more expensive thing.

The clock half is the same property viewed from further away. To say two events happened in an order you need a shared reference, and a shared reference is exactly what independent machines lack. A clock is not a shared reference — it is a local approximation of one, and comparing two approximations gives you an answer that is usually right and fails in the case you built the comparison to handle.

This is why the material is definitional rather than empirical. There is no faster machine on which check-then-act becomes atomic, and no better NTP configuration that makes wall clocks order events. The claims follow from what "check," "act," and "clock" mean.

And it is why the failures are so hard to catch in review. **Every line of the broken registration handler is correct.** The defect lives between the lines, and reading for defects is a habit trained on lines.

---

## Where this doesn't apply

### One writer, and the whole apparatus is dead weight

A build script. A migration run once by one operator. A game loop that updates the world on a single thread and hands a finished frame to the renderer. An embedded controller in a `while(1)` loop with interrupts disabled in the critical section.

In each, there is exactly one thread of control touching the state. Check-then-act is not atomic there either — the Law is as true as anywhere — but nothing can interleave, so it has nothing to act on. Adding a mutex buys nothing and costs a lock acquisition, a reader's attention, and the suggestion to the next person that concurrency exists here.

This matters more than it sounds, because the defensive habit travels further than the danger. A distributed-systems reflex applied to a single-threaded program produces machinery that cannot help, and hides the fact that the program's real risks are elsewhere.

The check is chapter 02's: **name the second writer.** If you cannot, the Law is inert. If you can, it binds — and the number of writers is a Force whose intensity you should have read rather than assumed (Ch. 03).

### The window is sometimes cheaper than the fix

Not every race is worth removing.

A view counter that occasionally loses an increment is a defect. Whether it is a defect worth an atomic operation depends on what the number is used for — and if the answer is "a rough popularity sort on a dashboard," then the lost update costs nothing and the coordination costs something on every write.

This is not permission to leave races in. It is the observation that "remove the race" has a price, and the price is only obviously worth paying when the state is load-bearing. The way to tell is the same as ever: what happens when it is wrong, and who finds out (Ch. 03, blast radius).

### Single-machine ordering is often good enough

Clocks do not order events *across machines*. Within one process, a monotonic counter, a mutex-protected sequence, or the database's own transaction ordering gives you a real order at negligible cost, and a great many systems need no more than that.

The failure is importing distributed-systems machinery — vector clocks, causal metadata, conflict-free replicated types — into a system with one database that already provides ordering for free. Chapter 07 works through where that machinery genuinely becomes necessary.

---

## What it costs

**Coordination costs latency, and it is not optional.** Every lock, every transaction, every quorum is a point where one party waits for another. That wait is bounded by how far the signal has to travel — nanoseconds within a core, microseconds across a machine, milliseconds across a continent — and it is paid on every operation, forever. The cheapest correct design is the one that needs the least coordination, which is why single-writer partitions win where they fit.

**Coordination does not compose.** Two individually correct locked operations are not a correct combined operation, which is the whole content of the registration example. Building bigger safe things out of smaller safe things is exactly what this material forbids, and it is the intuition most engineers arrive with.

**Enforcement in one place means error messages in another.** Moving uniqueness into a database constraint gets you correctness and a constraint violation with a constraint name in it. Turning that back into something a user can read is real work, done in a place that has to know what every constraint means.

**Atomic operations are easy to make slower than locks.** A single mutex under low contention is frequently faster than a lock-free structure written to avoid it, because the lock-free version pays on every access what the mutex pays only when contended. Measure, and expect to be wrong (Ch. 04, on empirical constants).

**Causal ordering costs space that grows with the system.** Lamport clocks are an integer. Vector clocks are an integer per node, attached to every message, and pruning them safely as nodes come and go is its own problem.

---

## How to recognize the failure

**In a codebase:**

- **A read and a write to the same state, separated by anything at all** — a validation, a log line, an API call. That gap is the bug, and its width is how often it fires.
- **`if not exists: insert`** in application code, with no unique constraint underneath. The check makes the duplicate rarer, which means the report arrives later and from a customer.
- **Two individually locked operations composed into a business rule.** Each is safe; the rule is not.
- **`select … for update` missing from a read whose value is about to be written back.**
- **Last-write-wins on a wall-clock timestamp**, deciding which of two concurrent updates survives. The winner is whoever's clock was ahead.
- **A timestamp column used to order events from more than one machine**, especially one populated by the application rather than the database.
- **Retry logic without idempotency**, which turns one race into several (Ch. 07).
- **A mutex in a program with one goroutine**, which usually means the last person could not name the second writer either.

**In a conversation:**

- **"That's very unlikely to happen."** It is a statement about the width of a window, not about whether the window exists — and windows widen under load, which is when it matters.
- **"We check for that before inserting."** The right follow-up is: what stops something happening between the check and the insert?
- **"We'll use a timestamp to work out which one is newer."** From which machine, and by how much can those two clocks differ?
- **"It works in testing."** Testing on an idle machine is testing with the narrowest windows the code will ever have.
- **"Let's just add a lock"** — asked about a rule spanning two operations, where the lock will go around each of them and change nothing.

The question that does the work: **what could have changed between the moment I read this and the moment I act on it?**

If the answer is *nothing, because nothing else writes here*, the Law is inert and you are done. If it is *anything at all*, you do not have a check — you have a guess with good manners.

---

**Next:** chapter 07 takes the same problem across machines, where coordination stops being expensive and starts being impossible — and works through what has been proved unachievable, along with the engineering that exists because of it.
