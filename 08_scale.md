# Scale: Queues, Parallelism, Memory

*This chapter is **Law**, and it mixes all three kinds (Ch. 04): two theorems, one claim true by definition, and several empirical laws. Which kind a claim is matters more here than anywhere else in the book, because the empirical ones carry numbers — and a number is the part that belongs to somebody else's machine.*

## The claim

**Adding more of a resource has an arithmetic shape you can work out before you build.**

Intuition says the relationship is a straight line: twice the servers, twice the throughput; twice the traffic, twice the wait. It never is. This chapter works through five shapes, and the skill is recognizing **which one you are on**, because that is what decides whether the fix is more hardware, less sharing, or a different design.

| Shape | You will meet it as | The fix |
|---|---|---|
| **Ceiling** | more cores stop helping | make the un-parallelizable part smaller |
| **Reversal** | more workers make it *slower* | remove the shared thing they contend on |
| **Cliff-edge curve** | fine at 80% load, unusable at 95% | leave headroom |
| **Step** | one extra struct field costs 7× | change the memory layout |
| **Floor** | latency you cannot optimize away | move the data, or stop waiting for it |

## About the numbers

Every measurement here was taken on the machine this was written on — an Apple M4 laptop, Go 1.26.5, 128 KB of L1 data cache, 16 MB of L2, 32 GB of memory.

**Yours will differ, and that is the point.** The formulas are exact and hold everywhere. The measurements are empirical (Ch. 04), which means the *pattern* transfers and the *number* does not. Someone else's benchmark tells you a shape exists; only your own tells you where you are on it.

---

## The demonstration

### Ceiling: the part you cannot split

A nightly report takes 100 minutes on one machine. Twenty of those minutes are spent reading one file from start to finish — that part cannot be split, because you cannot read the second half before the first. The remaining eighty minutes process rows independently, so that part splits perfectly.

Add cores and only the eighty minutes shrink:

```text
   1 core     20 + 80      = 100 min      1.0x faster
   4 cores    20 + 80/4    =  40 min      2.5x
  16 cores    20 + 80/16   =  25 min      4.0x
1024 cores    20 + 80/1024 =  20.08 min   5.0x
```

Twenty minutes never goes away, so the whole job can never take less than that — and 100 minutes divided by 20 is a ceiling of **five times, forever.** Buying a thousand cores instead of sixteen improves this job by 20%.

That is **Amdahl's Law**. Written out, with `s` as the fraction that cannot be split and `N` as the number of cores:

```text
speedup ≤ 1 / (s + (1 − s)/N)
```

The result is a multiplier: how many times faster the whole job runs. As `N` grows the second term vanishes, leaving `1/s` — so the ceiling is set entirely by the part you could not split.

```text
 fraction that      ceiling,        what you actually
 cannot be split    any hardware    get at 16 cores
       1%              100x              13.9x
       5%               20x               9.1x
      10%               10x               6.4x
      25%                4x               3.4x
```

The practical reading: **find the un-splittable fraction before you buy anything.** At 25% it barely matters what hardware you have.

This is a theorem, so there are two moves and no others (Ch. 04). Falsify an assumption, or stop needing the conclusion. The assumption worth attacking is that `s` is fixed — usually it is a lock, a single writer, or a coordination step somebody chose (Ch. 06), and making it smaller raises the ceiling in a way that hardware cannot.

### Reversal: when more workers make it slower

Amdahl says extra workers stop helping. The next result is worse: they can start actively hurting, because workers do not merely fail to help each other — they get in each other's way.

Here is that measured rather than asserted. The same total work — two million small computations — spread across a growing pool of workers, in two versions. In the first, each worker updates one shared counter after each item. In the second, each worker keeps its own count and they are added up at the end. Nothing else differs.

```go
// Version A: every worker touches the same counter.
mu.Lock()
counter += result
mu.Unlock()

// Version B: every worker touches only its own.
local[workerID] += result
```

```text
workers   shared counter    private counters
     1      68.11 M/s         80.54 M/s
     2      72.54 M/s        179.54 M/s
     4      16.44 M/s        304.05 M/s
     8      13.23 M/s        477.29 M/s
    16      12.57 M/s        502.50 M/s
    32      12.98 M/s        604.56 M/s
    64      13.33 M/s        600.24 M/s
```

Look at the left column between two workers and four. Throughput does not merely stop rising — it **falls by more than four times**, and it never recovers no matter how many workers are added. The right column, doing identical arithmetic, keeps climbing.

Two things cause this, and both get worse as workers are added.

**Contention.** Only one worker can hold the lock, so the others wait. That cost grows with the number of workers.

**Coherency.** This is the one people miss. Each core keeps its own cached copy of frequently used data. When one core writes to the counter, every other core's copy must be thrown away and re-fetched. With more workers there are more pairs of cores that have to keep agreeing with each other, and the number of pairs grows as the *square* of the worker count. That is why the curve turns down rather than flattening.

The **Universal Scalability Law** is Amdahl with that second term added. Its coefficients are fitted from measurements rather than derived, so treat the curve as a description and not a prediction. What it tells you is that **a peak exists, it is often lower than your core count, and past it every worker you add costs throughput.**

The practical reading: when a system is slow and adding workers does not help, adding more is not an incomplete fix — it may be the cause. Find what they all touch.

### Cliff-edge curve: what queues do near capacity

Two results, and the first applies to everything.

**Little's Law.** For any system where things arrive, spend time inside, and leave:

```text
items inside = arrival rate × time each one spends inside
```

At 500 requests per second with 200 ms average response time, there are 100 requests inside your system at any moment. That number is worth having, because if your connection pool holds 50, then half of those requests are queuing for a connection and the pool is your bottleneck — a thing you can check this afternoon.

The law assumes essentially nothing, which makes it true by definition (Ch. 04) for any queue that is not growing without limit.

**Then the part that surprises people.** *Utilization* is the fraction of time a server is busy: 0.8 means busy 80% of the time, idle 20%. For a single server handling irregular traffic, the time a request spends waiting grows as `1 / (1 − utilization)`:

```text
 busy      requests waiting     a request takes
           in the queue         this many times longer
 50%            1.0                  2x
 70%            2.3                  3x
 80%            4.0                  5x
 90%            9.0                 10x
 95%           19.0                 20x
 99%           99.0                100x
```

A server that is busy 99% of the time is not 4% busier than one at 95%. Requests take **five times longer**.

The reason is idle time. At 50% utilization, half the capacity is spare, so a sudden burst of requests gets absorbed. At 95% there is almost no spare capacity, so a burst has nowhere to go except the queue — and everyone behind it waits. **Queues are not caused by load. They are caused by variation in load, and idle time is what absorbs it.**

**On the "85% rule."** It is often taught as a threshold: stay under 85% and you are fine. There is no threshold. Here is the cost of one extra percentage point at four places on the curve:

```text
 from 50% to 51%:  wait  2.00x ->  2.04x    +2%
 from 70% to 71%:  wait  3.33x ->  3.45x    +3%
 from 85% to 86%:  wait  6.67x ->  7.14x    +7%
 from 95% to 96%:  wait 20.00x -> 25.00x   +25%
```

The curve is smooth. What rises is the price of each additional point, continuously, from the beginning. 85% is a convention marking roughly where that price becomes obvious to a human watching a graph.

Two caveats before anyone plans capacity with this. It assumes irregular arrivals — a system with perfectly steady traffic queues far less, and a bursty one far more. And it describes one server; a pool of them degrades more gently. Use it for the shape.

### Step: what the machine actually fetches

The results above are about time. This one is about layout, and it can cost a factor of seven in code that looks fine.

Start with the hardware fact. Memory is not read a byte at a time. The processor always fetches a fixed-size block — a **cache line**, 64 bytes on most machines — and keeps recently used blocks in a small fast store near the core. Reading one byte that is already in that store takes about a nanosecond. Reading one that is not takes a hundred times longer, because the whole 64-byte block has to come from main memory.

That difference is the whole of this section:

```text
 total data being touched      time per read
        16 KB                    1.94 ns      fits in the fastest cache
       256 KB                    7.61 ns      fits in the second-level cache
     4,096 KB                   14.79 ns      still cached, mostly
   262,144 KB                  196.55 ns      main memory
```

Same instruction, hundredfold difference, decided only by how much memory the program is touching. Add a network call and the range from processor register to remote service spans roughly six orders of magnitude.

Now the consequence for ordinary code. Here is an order record of the kind any commerce system accumulates:

```go
type Order struct {
	ID            [16]byte
	CustomerID    [16]byte
	TotalMinor    int64      // the only field the loop below reads
	TaxMinor      int64
	ShippingMinor int64
	PlacedAt      time.Time
	ShippedAt     time.Time
	Currency      [3]byte
	Status        uint8
	Channel       uint8
	WarehouseID   int32
}
```

That is 120 bytes. Now total up two million of them:

```go
var sum int64
for i := range orders {
	sum += orders[i].TotalMinor
}
```

The loop needs 8 bytes from each order. The machine fetches 120 — every field, including two timestamps and a warehouse ID that this loop never mentions. **Fifteen times more memory crosses the bus than the calculation requires.**

Store that one field on its own and the arithmetic is unchanged:

```go
var sum int64
for i := range totals { // totals is just []int64
	sum += totals[i]
}
```
[claude we don't need this raw duplicate measurements, the naming "BenchmarkSumFromRecords-10" is also very weird. 
Maybe just remove the table below and start the next paragraph with: Our local benchmar was seven times faster ... ****]
```text
BenchmarkSumFromRecords-10    100    3414706 ns/op
BenchmarkSumFromRecords-10    100    3320516 ns/op
BenchmarkSumFromColumn-10     100     476261 ns/op
BenchmarkSumFromColumn-10     100     475311 ns/op
```

**Seven times faster**, from where the bytes sit. This is also why analytics databases store data in columns rather than rows: a query that sums one column should not have to read the other twenty.

Two things about this shape. It is a **step rather than a slope** — growing a struct from 40 bytes to 60 costs nothing, and crossing 64 costs you a second fetch per record. And the expensive fields are the ones the slow loop never names, which is why the cost is invisible at the place where it is paid.

Chapter 05 uses the same underlying fact for a different argument: in an entity-component system the memory layout is deliberately made public, because hiding it would cost exactly the margin measured here.

### Floor: distance

Some latency is not an engineering problem at all.

Light travels through fibre at about two-thirds of its speed in vacuum. That gives a hard minimum for a round trip, before any router, queue, handshake, or line of code:

```text
 London  <-> New York      5,570 km       54.6 ms round trip
 London  <-> Sydney       16,990 km      166.6 ms round trip
```

Real measurements run one and a half to two times these, because cables do not follow great circles and routers take time. A synchronous call from London to Sydney inside a request handler has a floor of 167 ms, and no profiler will ever show you why.

The moves are chapter 04's two. Change an assumption: put a copy of the data near the user. Or stop needing the conclusion: make the operation asynchronous, so nobody is waiting for the round trip to finish.

---

## Why it holds

Each shape has a different cause, and applying the wrong fix is the common failure.

**Ceilings** come from work that cannot be divided. That is arithmetic on a fraction, needing no assumption about hardware, so no hardware changes it.

**Reversals** come from pairs. Contention grows with the number of workers; coherency grows with the number of pairs of workers, which grows as the square. A quantity growing as the square eventually overtakes one growing in proportion, and where they cross is the peak. This is why the fix is never more workers — it is removing what they share, and chapter 06's single-writer design is that taken to its limit.

**Queue cliffs** come from variation, not from load. Idle capacity is what absorbs a burst; near saturation there is none left. This is also why average latency is such a poor measure here — the system is not slow on average, it is slow precisely when it is busiest.

**Steps** come from the fixed fetch size. The machine moves 64 bytes whether you wanted 8 or 64, so the question is never how much data you need but how much of each fetched block you use. That is decided by layout, not by algorithm.

**Floors** come from physics, and there is no mechanism to explain.

---

## Where this doesn't apply

### Small collections, where the constant wins

Big-O notation deliberately ignores constant factors, so at small sizes it can point the wrong way: a scan of a few items can beat a hash lookup, because hashing costs more than a handful of comparisons.

I set out to demonstrate that with a linear scan against a map, and with string keys the scan never won:

```text
  items   scan      map lookup    faster
     4    12.5 ns     11.0 ns      map
     8    25.2 ns     13.5 ns      map
    16    24.5 ns      8.7 ns      map
```

That failure is the more useful result. The same test with integer keys:

```text
  items   scan      map lookup    faster
     2     1.27 ns     2.95 ns     scan
     4     2.16 ns     3.92 ns     scan
     8     4.08 ns     5.86 ns     scan
    12     7.08 ns     5.39 ns     map
    16     8.98 ns     5.46 ns     map
```

Scanning wins up to about eleven integers, and never wins for strings. So the crossover point is **not a property of the two algorithms.** It is set by how expensive one comparison is against one hash, and comparing strings is expensive enough to move the crossing off the chart entirely.

Which makes the familiar advice — *use a list under about twenty items* — a number quoted without the conditions that produced it, exactly the failure chapter 04 describes: The threshold belongs to somebody else's data type and machine.

In practice, at these sizes the difference is nanoseconds. Use the map and spend the attention elsewhere.

### Systems nowhere near the bend

Every curve here is flat at the left-hand end.

At 20% utilization, requests wait 1.25 times the service time and no capacity planning is visible. On four cores, the difference between 1% and 5% un-splittable work is a rounding error. A program touching 10 MB, run once a day, does not need a layout decision.

The mistake is not ignoring the arithmetic when small. It is building for the right-hand end of a curve you are nowhere near — chapter 03's case of a decision that both expires and is expensive, where the cost is paid now and the benefit arrives only in a future that may not come.

### When speed is not the constraint

All of this optimizes time. Plenty of systems are limited by something else.

A batch job that must finish by 6 a.m. and takes two hours has seven hours of slack, so making it faster buys nothing. A system whose cost is dominated by per-call charges to a third party is optimizing money. A battery-powered device is optimizing energy — where the cache-friendly version usually still wins, but for a different reason, and it is worth knowing which reason you are relying on.

---

## What it costs

**Column layouts cost cohesion.** Splitting a record into parallel arrays scatters one concept across many places. Adding a field means touching every array and every loop that walks them together. The 7× is real; so is the maintenance bill, and chapter 05 works through what gets given up.

**Measuring is slow and easy to get wrong.** Every number here took several attempts. A benchmark whose data fits entirely in cache, or whose result the compiler discards as unused, produces a confident figure that describes nothing. Expect to throw away your first two.

**Queue models are wrong in two directions at once.** They assume irregular arrivals, which makes them pessimistic for steady traffic, and a single server, which makes them optimistic for a pool. Two errors pointing opposite ways is not the same as being right.

**The scalability curve needs the system before it can describe it.** Its coefficients come from measuring a running system at several worker counts. It explains a measurement you already have; it does not tell you in advance where your peak will be. [claude I don't get this, is there a way to formulate this idea more clearly?]

**Optimizing the wrong shape is worse than doing nothing.** Adding workers past the peak makes throughput fall. Adding cores to mostly-serial work buys almost nothing. Both cost money and both look like progress.

---

## How to recognize the failure

**In a codebase:**

- **A struct that has grown past 64 bytes**, walked by a hot loop that reads one or two of its fields. Whoever appended the last field paid nothing; the loop pays every time it runs.
- **A worker count that was raised each time the system felt slow**, with no measurement of whether throughput rose too.
- **A connection pool smaller than arrival rate times response time.** Little's Law gives the number of in-flight requests; if the pool is smaller, requests are queuing somewhere you are not watching.
- **Capacity planned on average utilization**, which says nothing about the wait at peak.
- **A synchronous cross-region call in a request path**, where the distance alone exceeds the latency budget.
- **A performance constant copied from an article**, with no measurement on the machine that runs the code.
- **A hash map holding six items**, chosen because it is `O(1)`, costing a hash and an allocation to avoid a scan that would fit in one cache line.

**In a conversation:**

- **"We'll add more workers."** Did throughput go up last time, and did anyone check?
- **"It's only at 90%."** That is ten times the service time spent waiting. The graph looks fine until it does not.
- **"Average latency is fine."** Averages hide exactly the tail that queueing produces.
- **"It's O(1), so it's faster."** At what size, and against what constant?
- **"We optimized the algorithm"** — on a workload whose cost was memory layout, where the algorithm was never the problem.

The question that does the work: **which shape am I on?**

A ceiling means stop buying hardware and shrink the serial part. A reversal means stop adding workers and find what they share. A queue cliff means buy headroom rather than speed. A step means look at the layout. A floor means move the data or stop waiting for it.

---

**Next:** chapter 09 moves to the timescale where the arithmetic is measured in years rather than milliseconds — how systems change, how the shape of an organization ends up in its software, and why a published interface is a decision you do not get to take back.
