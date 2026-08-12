# Scale: Queues, Parallelism, Memory

*This chapter is **Law**, and the mix is unusual: two theorems, one near-definitional identity, and several empirical constants (Ch. 04). The grades matter more here than anywhere else in the book, because the empirical numbers are the ones people quote and the ones that have moved.*

## The claim

**Adding more of a resource has a shape, and the shape is arithmetic you can do before you build.**

Intuition assumes a straight line — twice the cores, twice the speed; twice the load, twice the wait. Nothing in this chapter is a straight line. There are ceilings you cannot pass, knees past which more makes things worse, discontinuities where one extra field costs a fourfold slowdown, and floors that no engineering removes.

The useful skill is not memorizing the formulas. It is knowing **which shape you are on**, because that decides whether the answer is more hardware, less contention, or a different design.

## A note on the numbers

Every measurement below was taken on the machine this chapter was written on: an Apple M4 laptop, Go 1.26.5, 128 KB L1 data cache, 16 MB L2, 32 GB of memory.

**They will not reproduce exactly on your machine, and that is the point.** These are empirical constants, not theorems — the regularity holds everywhere and the magnitude is local (Ch. 04). The formulas are exact; the numbers are an instance.

---

## The demonstration

### A ceiling: Amdahl's Law

If a fraction *s* of the work must run serially, the speedup from *N* processors is bounded:

```text
speedup ≤ 1 / (s + (1−s)/N)
```

Which produces a ceiling that does not care how many cores you buy:

```text
  1% serial -> ceiling  100.0x   (at 16 cores: 13.9x, at 1024: 91.2x)
  5% serial -> ceiling   20.0x   (at 16 cores:  9.1x, at 1024: 19.6x)
 10% serial -> ceiling   10.0x   (at 16 cores:  6.4x, at 1024:  9.9x)
 25% serial -> ceiling    4.0x   (at 16 cores:  3.4x, at 1024:  4.0x)
```

Read the last row carefully. At 25% serial, going from 16 cores to 1024 — sixty-four times the hardware — buys you 3.4× to 4.0×. **An 18% improvement for 6,400% of the machines.**

This is a theorem, so the only moves are chapter 04's two: falsify an assumption, or stop needing the conclusion. The assumption worth attacking is that *s* is fixed. It usually is not — the serial fraction is often a lock, a single writer, or a coordination point you chose (Ch. 06), and shrinking *s* raises the ceiling in a way that buying cores cannot.

### A knee, where the sign flips: the Universal Scalability Law

Amdahl says returns diminish. The Universal Scalability Law says they can go **negative**, because workers do not merely fail to help each other — they interfere.

It adds a second term for coherency: the cost of keeping *N* workers' views of shared state consistent, which grows with the number of *pairs*, so with N².

```text
   1 workers ->   1.00x
   4 workers ->   3.63x
   8 workers ->   6.32x
  16 workers ->   9.47x
  32 workers ->  10.95x
  64 workers ->   9.25x
 128 workers ->   6.08x
 256 workers ->   3.46x

 peak at 31 workers (10.95x); more workers is slower
```

Sixty-four workers are slower than thirty-two. Two hundred and fifty-six are slower than four.

The shape matters more than the coefficients, which are fitted rather than derived. **There is a peak, it is often lower than the core count, and past it every worker you add makes the system worse.** A team that responds to a slow system by raising the worker count can walk down the right-hand side of that curve for months, adding capacity and losing throughput, because the intuition says more workers cannot hurt.

### Superlinear cost: queues near saturation

Little's Law first, because it is the one you can always apply. For any stable system:

```text
L = λ × W
```

Items in the system equals arrival rate times time in the system. It assumes almost nothing — no distribution, no independence — which makes it near-definitional (Ch. 04) and always true of a stable queue. Its use is that knowing any two gives you the third: 500 requests a second and 200 ms average latency means 100 requests in flight, which is a number you can compare against your connection pool.

Then the part that surprises people. For a simple queue, the wait scales as `1/(1−ρ)` where ρ is utilization:

```text
  rho     queue length     wait (in service times)
  0.50        1.00              2.0x
  0.70        2.33              3.3x
  0.80        4.00              5.0x
  0.85        5.67              6.7x
  0.90        9.00             10.0x
  0.95       19.00             20.0x
  0.99       99.00            100.0x
```

A server at 99% utilization is not 4% busier than one at 95%. It is **five times slower.**

**On the "85% rule," which is worth correcting.** It is often taught as a cliff — stay below 85% and you are fine. The arithmetic shows no cliff at 85 or anywhere else:

```text
  50% -> 51%: wait  2.00x ->  2.04x  (+2.0%)
  70% -> 71%: wait  3.33x ->  3.45x  (+3.4%)
  85% -> 86%: wait  6.67x ->  7.14x  (+7.1%)
  95% -> 96%: wait 20.00x -> 25.00x  (+25.0%)
```

The curve is smooth. What rises is the *marginal* cost of one more point of utilization, continuously, from the very beginning. 85% is a convention chosen because that is roughly where the marginal cost becomes obvious to humans — not a threshold in the mathematics.

Two honest caveats. This model assumes random arrivals and variable service times; a system with perfectly regular arrivals queues far less, and one with bursty arrivals queues far more. And it is a single server — real systems with N servers degrade more gently. Use it for the shape and the order of magnitude, not for a capacity plan.

### A discontinuity: the memory hierarchy

The formulas above are about time. This one is about distance, and it is the one most likely to make a factor-of-four difference to code you have already written.

Pointer-chasing a shuffled ring, so no prefetcher can help, at four working-set sizes:

```text
working set       16 KB  ->   1.94 ns per dependent load
working set      256 KB  ->   7.61 ns per dependent load
working set     4096 KB  ->  14.79 ns per dependent load
working set   262144 KB  ->  196.55 ns per dependent load
```

**A hundredfold, on one machine, for the identical instruction.** The only thing that changed is how much memory the program is touching. Add a network hop and the span from register to remote service crosses roughly six orders of magnitude.

Now the consequence for code. A particle update, written the obvious way:

```go
type Particle struct {
	PosX, PosY, PosZ float32
	VelX, VelY, VelZ float32
	R, G, B, A       float32
	Lifetime, Mass   float32
	// ... plus whatever else an entity accumulates
}

for i := range particles {
	particles[i].PosX += particles[i].VelX * dt
}
```

That loop reads two floats — eight bytes — per particle. But memory does not move in bytes, it moves in **cache lines**, 64 bytes at a time, and this struct is 80 bytes. So every iteration drags in colour, mass, and lifetime that the loop never touches, and each particle straddles two lines.

The same computation over parallel arrays:

```go
posX, velX := soa.PosX, soa.VelX

for i := range posX {
	posX[i] += velX[i] * dt
}
```

Now a 64-byte line carries sixteen useful floats instead of parts of one particle. Over 1,048,576 particles:

```text
BenchmarkAoS-10    200    2628190 ns/op
BenchmarkAoS-10    200    2632114 ns/op
BenchmarkAoS-10    200    2707792 ns/op
BenchmarkSoA-10    200     611411 ns/op
BenchmarkSoA-10    200     610686 ns/op
BenchmarkSoA-10    200     609759 ns/op
```

**4.3×**, from rearranging fields. No algorithm changed, no work was removed, and the source of both loops is the same arithmetic.

This is why chapter 05's entity-component case gives up encapsulation deliberately: the layout *is* the interface there, and hiding it costs the margin the design exists for. Two things worth noticing about the shape. It is a **discontinuity** rather than a slope — nothing happens as the struct grows from 40 bytes to 60, and then crossing 64 costs you. And the fields that hurt are the ones the loop never mentions, which is why this defect is invisible in the code that suffers from it.

### A floor: the speed of light

Some latency is not an engineering problem.

```text
London <-> New York:  5,570 km  ->   54.62 ms round trip
London <-> Sydney:   16,990 km  ->  166.62 ms round trip
```

That is signal propagation in fibre — light at roughly two-thirds of *c* through glass — with no routers, no queueing, no TLS handshake, no processing. Real numbers are one and a half to two times these.

You cannot optimize past it, and the only moves are the ones chapter 04 names: change an assumption (put the data nearer the user), or stop needing the conclusion (make the operation asynchronous so nobody waits for the round trip). A synchronous cross-Atlantic call in a request path has a floor of 55 ms, and no amount of profiling will find it.

---

## Why it holds

Each shape has a different mechanism, and mistaking one for another is how the wrong fix gets applied.

**Ceilings come from work that cannot be divided.** Amdahl is arithmetic on a fraction, so it needs no assumptions about hardware and cannot be engineered around — only reduced by making the serial part smaller.

**Sign flips come from pairwise interaction.** Contention costs grow with *N*; coherency costs grow with the number of pairs, so with *N²*. Any quantity growing quadratically eventually beats one growing linearly, and that crossing is the peak. This is why the fix for a system past its knee is never more workers — it is removing shared state so the quadratic term shrinks (Ch. 06's single writer is the extreme case).

**Superlinear queueing comes from variance, not from load.** At 50% utilization a burst is absorbed by the idle half. At 95% there is no idle half, so a burst has nowhere to go but the queue, and the queue is what you wait behind. This is why the average tells you so little: the system is not slow on average, it is slow exactly when it is busy, which is when anyone notices.

**The memory discontinuity comes from a fixed transfer unit.** The hardware moves 64 bytes whether you asked for four or forty. So the question is never "how much data do I need" but "how much of each line I fetch will I use" — and that is decided by layout rather than by algorithm.

**The floor comes from physics.** There is no mechanism to explain, which is what makes it a different kind of constraint from everything else here.

---

## Where this doesn't apply

### Small n, where the constant beats the exponent

The asymptotically better algorithm loses when *n* is small enough, because big-O deliberately discards the constant and at small *n* the constant is all there is.

I set out to demonstrate this with a linear scan against a hash map, expecting the scan to win below some *n*. With string keys it never won:

```text
   n    linear scan    map lookup    winner
   4       12.5 ns        11.0 ns     map
   8       25.2 ns        13.5 ns     map
  16       24.5 ns         8.7 ns     map
```

**That is the more useful result.** The same test with integer keys:

```text
   n    linear scan    map lookup    winner
   2        1.27 ns       2.95 ns     SCAN
   4        2.16 ns       3.92 ns     SCAN
   8        4.08 ns       5.86 ns     SCAN
  12        7.08 ns       5.39 ns     map
  16        8.98 ns       5.46 ns     map
```

The crossover is at about eleven elements for integers and below four for strings. So the crossover is **not a property of the two algorithms.** It is set by the cost of one comparison against the cost of one hash, and string comparison is expensive enough to move the crossing point off the bottom of the chart.

Which means the widely repeated advice — *use a slice under about twenty items* — is a magnitude quoted without its conditions, exactly the failure chapter 04 describes. The regularity is real; the number belongs to somebody else's element type, language, and machine. Measure yours, or use the map and stop thinking about it, because at these sizes the difference is nanoseconds and your time costs more.

### Systems small enough that the shape never bends

Every curve here is flat at the left-hand end.

At 20% utilization the queueing term is 1.25× and the difference between good and bad capacity planning is invisible. At four cores, the gap between 1% and 5% serial is a rounding error. A working set of 10 MB in a program that runs once a day does not need a layout decision.

The mistake is not ignoring the arithmetic at small scale. It is *building for the right-hand side of a curve you are nowhere near*, which chapter 03 covers as the case where a decision expires and is expensive: the machinery is paid for now and the benefit arrives only in a future you may not reach.

### When throughput is not the thing you are optimizing

All of this optimizes throughput or latency. Plenty of systems are constrained by neither.

A batch job that must finish before 6 a.m. has one deadline and eight hours of slack; a system whose cost is dominated by a per-request charge to a third party is optimizing money; a device on a battery is optimizing joules, and the cache-friendly version usually wins there too but for a different reason. Reaching for these formulas when the binding constraint is elsewhere produces a faster system that is no better.

---

## What it costs

**Cache-friendly layouts cost readability and cohesion.** Parallel arrays scatter one concept across several places, and adding a field means touching every array, every constructor, and every loop that iterates in lockstep. The 4.3× is real and so is the maintenance bill (Ch. 05's boundary works through what is given up).

**Measuring is slow, and microbenchmarks lie.** Every number in this chapter took several attempts. Benchmarks that fit entirely in L1, or that the compiler optimizes away because the result is unused, produce confident numbers that describe nothing. Budget for getting it wrong twice.

**Queueing models are wrong in a specific direction.** The formula assumes random arrivals and one server. Real traffic is bursty, which makes waits worse than the model, and real systems have many servers, which makes them better. Two errors in opposite directions is not the same as being right — use the shape, not the value.

**The USL coefficients are fitted, not derived.** You get them by measuring a system at several concurrency levels and fitting the curve, which means you need the system before you can predict its knee. Its value is in explaining a measurement you already have, and in telling you the peak exists.

**Optimizing the wrong shape is worse than doing nothing.** Adding workers to a system past its USL peak makes it slower. Adding cores to a 25%-serial workload buys almost nothing. Both consume budget and both look like action.

---

## How to recognize the failure

**In a codebase:**

- **A struct that has grown past a cache line**, iterated in a hot loop that reads two of its fields. The cost is invisible at the loop and was added by whoever appended the last field.
- **A worker-pool size that was raised whenever things got slow**, with no measurement of whether throughput rose with it.
- **A connection pool smaller than `λ × W`.** Little's Law gives you the number of in-flight requests; if the pool is smaller, the queue moved into your application and the pool is the bottleneck you are not measuring.
- **A capacity plan expressed as average utilization**, which says nothing about the wait at peak.
- **A synchronous cross-region call in a request path**, where the floor exceeds the latency budget and no profiling will explain it.
- **A performance constant hard-coded from a blog post**, which is chapter 04's failure and belongs here too.
- **`O(1)` chosen over `O(n)` for a collection that has never held more than six items**, which costs a hash and an allocation to avoid a scan that would fit in a cache line.

**In a conversation:**

- **"We'll add more workers."** The right question is whether throughput went up last time, and whether anybody checked.
- **"It's only at 90% utilization."** That is ten times the service time in queue. There is no headroom left, and the graph looks fine right up until it does not.
- **"The average latency is fine."** Averages hide the distribution, and queueing pathology lives entirely in the tail.
- **"That's O(1), so it's faster."** For what *n*, and measured against what constant?
- **"We optimized the algorithm"** on a workload where the cost was memory layout, and the algorithm was never the bottleneck.

The question that does the work: **which shape am I on, and where is the knee?**

A ceiling means stop buying hardware and shrink the serial part. A knee means stop adding workers and remove shared state. A superlinear curve means the fix is headroom, not speed. A discontinuity means look at the layout, not the algorithm. And a floor means change the geography or stop waiting for the answer.

---

**Next:** chapter 09 moves to the timescale where the arithmetic stops being about milliseconds and starts being about years — how systems evolve, how organizations shape them, and why a published interface is a decision you cannot take back.
