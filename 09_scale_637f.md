# Scale: Queues and Parallelism

## The claim

**More resources can degrade performance, and when they do help the gain is not linear.**

Intuition says the relationship is a straight line: twice the servers, twice the throughput; twice the traffic, twice the wait. In reality, you never get that perfect line. The shape is mostly a curve determined by the underlying laws.

This chapter works through four laws and the three shapes they produce.

Each law's grade is stated too, in the sense [chapter 04](04_grading-a-law_q5c6.md) defines. Which law you are up against, and what grade it carries, decides whether the fix is more hardware, less sharing, or a different design.

---

## Four Laws

### Amdahl's Law

First a clarification for two key terms: we use "parallel part" and "serial part" to denote splittable and no-splittable portions of a work.

**A theorem**: the fraction of the serial part sets a ceiling on how much faster the whole job can get, whatever the core count.

A nightly report takes 100 minutes on one machine. Twenty of those minutes are spent reading one file from start to finish — that part cannot be split, because you cannot read the second half before the first. The remaining eighty minutes process rows independently, so that part splits perfectly.

Add cores and only the eighty minutes shrink:

```text
   1 core     20 + 80      = 100 min      1.0x faster
   4 cores    20 + 80/4    =  40 min      2.5x
  16 cores    20 + 80/16   =  25 min      4.0x
1024 cores    20 + 80/1024 =  20.08 min   5.0x
```

Twenty minutes never goes away, so the whole job can never take less than that — and 100 minutes divided by 20 is a ceiling of **five times, forever.** Buying a thousand cores instead of sixteen improves this job by 20%.

**Amdahl's Law** is also expressed as a formula, with `s` for the serial part and `N` for the number of cores:

```text
speedup ≤ 1 / (s + (1 − s)/N)
```

The result is a multiplier: how many times faster the whole job runs. As `N` grows the second term vanishes, leaving `1/s` — so the ceiling is set entirely by the serial part.

```text
 fraction that      ceiling,        what you actually
 cannot be split    any hardware    get at 16 cores
       1%              100x              13.9x
       5%               20x               9.1x
      10%               10x               6.4x
      25%                4x               3.4x
```

The practical reading: **find the un-splittable fraction before you buy anything.** At 25% it barely matters what hardware you have.

So there are two moves and no others ([Ch. 04](04_grading-a-law_q5c6.md)). Falsify an assumption, or stop needing the conclusion. The assumption worth attacking is that `s` is fixed — usually it is a lock, a single writer, or a coordination step somebody chose ([Ch. 07](07_time_mdbn.md)), and making it smaller raises the ceiling in a way that hardware cannot.


**The famous attempt at the other assumption is worth knowing about, and worth being careful with.**  Amdahl assumes the *parallel part* is fixed. Decline that, let the parallel part grow with the machine, and the twenty minutes stops being a ceiling and becomes an overhead: sixteen cores then get through 1300 minutes of work in the same 100, a speedup of 13 rather than 4. That is **Gustafson's Law**, `speedup = s + N(1 − s)`, and it is usually introduced as the result that overturned Amdahl.

It did not, and the condition it rests on is the part that gets dropped. Gustafson assumes the serial part **does not grow with the problem** — his own examples are program loading, vector startup and I/O setup, which are fixed cost per run. Take a monthly report to a yearly one and that assumption fails immediately: reading twelve times the data from the file is 12x unsplittable work, `s` is unchanged, and the ceiling sits exactly where it was. Growing the job helps only if the parallel part grows faster than the serial part does.

So this is not a second law standing beside the first. Karbowski derives it from Amdahl in a page and concludes that it *"is nothing but a different form of Amdahl's law"*, and that the popular claim it overthrows Amdahl *"is a mistake"*. What is sold as a law is the theorem re-measured, resting on an empirical bet about your workload — advice that is good given certain Forces and wrong without them, which in this book's vocabulary makes it a **Principle** wearing a Law's name. The test before taking the bet: **is your serial part fixed like a startup, or is it work proportional to the data?**

### The Universal Scalability Law

**Empirical law:** Past some number of workers, adding more *reduces* throughput, because each worker contends with every other for whatever they share.

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

The coefficients being fitted rather than derived is what decides how much of this transfers. A measurement can falsify them, which means the shape is worth trusting and the location is not: where your peak sits is a property of your contention, and nobody else's benchmark can find it for you.

### Little's Law

**A definitional law:** the number of things inside a system at once is the arrival rate multiplied by the average time each one spends there.

It applies to everything — a queue, a thread pool, a warehouse, a motorway. For any system where things arrive, spend time inside, and leave:

```text
items inside = arrival rate × time each one spends inside
```

At 500 requests per second with 200 ms average response time, there are 100 requests inside your system at any moment. That number is worth having, because if your connection pool holds 50, then half of those requests are queuing for a connection and the pool is your bottleneck — a thing you can check this afternoon.

The law assumes essentially nothing, which makes it true by **definition** ([Ch. 04](04_grading-a-law_q5c6.md)) for any queue that is not growing without limit.

### The queueing curve

**A theorem.** *Utilization* is the fraction of time a server is busy: 0.8 means busy 80% of the time, idle 20%. For a single server handling irregular traffic, the time a request spends waiting grows as `1 / (1 − utilization)`:

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

Those caveats are the theorem's assumptions showing through: the curve is exactly true of the queue it describes, so the only question it admits is whether that queue is yours. Little's Law asks even less of you — only that its words describe your system, which for any queue not growing without limit they do.

## Why the claim holds

Three of the four laws produce a shape — Little's Law is the exception, being an identity rather than a curve — and each shape has a different cause. Applying the wrong fix is the common failure.

**Amdahl's ceiling** comes from work that cannot be divided. That is arithmetic on a fraction, needing no assumption about hardware, so no hardware changes it.

**The Universal Scalability Law's reversal** comes from pairs. Contention grows with the number of workers; coherency grows with the number of pairs of workers, which grows as the square. A quantity growing as the square eventually overtakes one growing in proportion, and where they cross is the peak. This is why the fix is never more workers — it is removing what they share, and [chapter 07](07_time_mdbn.md)'s single-writer design is that taken to its limit.

**The queueing curve's cliff** comes from variation, not from load. Idle capacity is what absorbs a burst; near saturation there is none left. This is also why average latency is such a poor measure here — the system is not slow on average, it is slow precisely when it is busiest.

---

## Where the claim doesn't apply

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

Which makes the familiar advice — *use a list under about twenty items* — a number quoted without the conditions that produced it, exactly the failure [chapter 04](04_grading-a-law_q5c6.md) describes — the pattern holds, but the threshold belongs to somebody else's data type and machine.

In practice, at these sizes the difference is nanoseconds. Use the map and spend the attention elsewhere.

### Systems nowhere near the bend

Every curve here is flat at the left-hand end.

At 20% utilization, requests wait 1.25 times the service time and no capacity planning is visible. On four cores, the difference between 1% and 5% un-splittable work is a rounding error. A program touching 10 MB, run once a day, does not need a layout decision.

The mistake is not ignoring the arithmetic when small. It is building for the right-hand end of a curve you are nowhere near — [chapter 03](03_forces_f4m5.md)'s case of a decision that both expires and is expensive, where the cost is paid now and the benefit arrives only in a future that may not come.

### When speed is not the constraint

All of this optimizes time. Plenty of systems are limited by something else.

A batch job that must finish by 6 a.m. and takes two hours has seven hours of slack, so making it faster buys nothing. A system whose cost is dominated by per-call charges to a third party is optimizing money. A battery-powered device is optimizing energy — where the cache-friendly version usually still wins, but for a different reason, and it is worth knowing which reason you are relying on.

---

## What the claim costs

**Column layouts cost cohesion.** Splitting a record into parallel arrays scatters one concept across many places. Adding a field means touching every array and every loop that walks them together. The 7× is real; so is the maintenance bill, and [chapter 05](05_dependency-and-hiding_agjy.md) works through what gets given up.

**Measuring is slow and easy to get wrong.** Every number here took several attempts. A benchmark whose data fits entirely in cache, or whose result the compiler discards as unused, produces a confident figure that describes nothing. Expect to throw away your first two.

**Queue models are wrong in two directions at once.** They assume irregular arrivals, which makes them pessimistic for steady traffic, and a single server, which makes them optimistic for a pool. Two errors pointing opposite ways is not the same as being right.

**The scalability curve cannot predict a system you have not built.** To draw it you need two numbers — how much workers contend, and how much they invalidate each other's caches — and the only way to get them is to run the real system at several worker counts and fit the curve to what you measure. So it will not tell you in advance where your peak will be. What it is good for is explaining a slowdown you can already see, and knowing to go looking for a peak at all.

**Optimizing the wrong shape is worse than doing nothing.** Adding workers past the peak makes throughput fall. Adding cores to mostly-serial work buys almost nothing. Both cost money and both look like progress.

---

## How to recognize the failure

**In a codebase:**

- **A worker count that was raised each time the system felt slow**, with no measurement of whether throughput rose too.
- **A connection pool smaller than arrival rate times response time.** Little's Law gives the number of in-flight requests; if the pool is smaller, requests are queuing somewhere you are not watching.
- **Capacity planned on average utilization**, which says nothing about the wait at peak.
- **A performance constant copied from an article**, with no measurement on the machine that runs the code.
- **A hash map holding six items**, chosen because it is `O(1)`, costing a hash and an allocation to avoid a scan that would have been faster.

**In a conversation:**

- **"We'll add more workers."** Did throughput go up last time, and did anyone check?
- **"It's only at 90%."** That is ten times the service time spent waiting. The graph looks fine until it does not.
- **"Average latency is fine."** Averages hide exactly the tail that queueing produces.
- **"It's O(1), so it's faster."** At what size, and against what constant?

The question that does the work: **which law am I up against?**

A ceiling means stop buying hardware and shrink the serial part. A reversal means stop adding workers and find what they share. A queue cliff means buy headroom rather than speed.

[Chapter 10](10_change_rjf9.md) moves to the timescale where the arithmetic is measured in years rather than milliseconds — how systems change, how the shape of an organization ends up in its software.

---

## About the numbers

Every measurement in this chapter was taken on the machine it was written on — an Apple M4 laptop, Go 1.26.5, ten cores and 32 GB of memory.

**Your numbers will differ, and that is the point.** The formulas are exact and hold everywhere. The measurements are empirical ([Ch. 04](04_grading-a-law_q5c6.md)), which means the *pattern* described by the law transfers and the *number* does not. Someone else's benchmark tells you a shape exists; only your own tells you where you are on it.

---

## Sources

- Gene M. Amdahl, *Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities* — AFIPS Spring Joint Computer Conference, April 1967. [PDF](https://inst.eecs.berkeley.edu/~n252/paper/Amdahl.pdf).
- Neil J. Gunther, *A General Theory of Computational Scalability Based on Rational Functions* — August 2008. [arXiv](https://arxiv.org/abs/0808.1431).
- John L. Gustafson, *Reevaluating Amdahl's Law* — Communications of the ACM 31(5), May 1988. [dl.acm.org](https://dl.acm.org/doi/10.1145/42411.42415).
- Andrzej Karbowski, *Amdahl's and Gustafson-Barsis laws revisited* — arXiv:0809.1177, September 2008. [arXiv](https://arxiv.org/abs/0809.1177).
- John D. C. Little, *A Proof for the Queuing Formula: L = λW* — Operations Research 9(3), May–June 1961.

---

[← Ch. 08](08_distribution_49yh.md)  ·  [Contents](00_toc.md)  ·  [Ch. 10 →](10_change_rjf9.md)
