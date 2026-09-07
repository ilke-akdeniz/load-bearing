# The memory hierarchy, cut from chapter 09 and awaiting a home

**Status.** Cut from [chapter 09](../../09_scale_637f.md) on 2026-09-07. Not yet placed.

## Why it was cut

The chapter's axis is laws that shape what more resources buy you.
The memory hierarchy is not a Law in this book's sense — it is a **Force**, a property of the machine you are standing on, and [chapter 21](../../21_six-profiles_dnkz.md) already treats it as one: *"The Forces are the frame budget and the memory hierarchy."*
The section had been labelled an empirical law to justify its place, which was the draft's invention rather than a finding.

The author's test, which is the one that settled it: every attempt to fit it required either bending the chapter's claim or having the section explain why the chapter's *other* laws do not apply.

## Where it should probably go

[Chapter 05](../../05_dependency-and-hiding_agjy.md), whose entity-component-system section already makes this exact claim and then defers the evidence to chapter 09: *"it wins by a margin that has nothing to do with taste… ([Chapter 09] owns the arithmetic and the benchmark)."*
Moving the benchmark closes both ends — chapter 05 currently asserts a margin it does not show.
The particle arrays and the order records are the same demonstration at two scales, and the point demonstrated is chapter 05's: hiding is a Principle that inverts when the memory hierarchy dominates.

**Cost to weigh:** chapter 05 is already the book's longest at roughly 6,300 words.

## What is owed, and to whom

| Piece | Candidate home |
|---|---|
| The `Order` struct and the 7.2x record-versus-column benchmark | [Ch. 05](../../05_dependency-and-hiding_agjy.md), ECS section |
| The cache-line mechanism — cost is set by how much of each fetched block you use | [Ch. 05](../../05_dependency-and-hiding_agjy.md) |
| The latency ladder, 16 KB to 256 MB | unplaced; [ch. 04](../../04_grading-a-law_q5c6.md) uses the hierarchy as its example of an empirical law that drifts |
| The recognition item about a struct grown past a cache line | wherever the benchmark lands |

**Verified on 2026-09-07**, so the numbers do not need re-taking: `sizeof(Order)` is 120 bytes confirmed with the toolchain, and the benchmark reproduces at 3.46 ms against 0.48 ms, a ratio of 7.20 on an Apple M4 with a 128-byte cache line.

**A second measurement exists and is not in the text below**, taken while testing whether the section could be made to fit the resource claim. It shows the record loop is bandwidth-bound and the column loop is not — at four workers the record sum gains 1.03x and the column sum 2.32x. It is good evidence for the ECS argument if chapter 05 wants it.

---

## Ledger rows that came out with it

These were removed from `docs/LEDGER.md` when the section was cut, and go back under whichever chapter takes the material:

```text
| Memory hierarchy ~6 orders | 637f | Register to network spans about a million-fold | cite |
| The cache line is the transfer unit | 637f | Cost is set by how much of each fetched line you use, which is layout not algorithm | cite |
| Speed of light as a floor | 637f | Cross-region round trips have a floor no profiling removes; change geography or stop waiting | cite |
| Summing one field across 2M order records vs one column | 637f | 7.2x from where the bytes sit; 120-byte record, 128-byte cache line on the measuring machine, no algorithm change. agjy owns the encapsulation argument and keeps `Particle` |
```

## The section as it stood

### The memory hierarchy

**This law has no famous name, and it is empirical:** The machine moves memory in fixed-size blocks, so what a loop costs is decided by how much of each block it actually uses.

The results above are about time. This one is about layout, and it can cost a factor of seven in code that looks fine.

Start with the hardware fact. Memory is not read a byte at a time. The processor always fetches a fixed-size block — a **cache line** — and keeps recently used blocks in a small fast store near the core. The line is 64 bytes on x86-64 and 128 on Apple Silicon, including the machine every measurement here was taken on. Reading one byte that is already in that store takes about a nanosecond. Reading one that is not takes a hundred times longer, because the whole block has to come from main memory.

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
Summing two million orders took 3.4 milliseconds from the records and 0.48 milliseconds from the column — **seven times faster**, from where the bytes sit. This is also why analytics databases store data in columns rather than rows: a query that sums one column should not have to read the other twenty.

Two things about this shape. It is a **step rather than a slope** — growing a struct from 40 bytes to 60 costs nothing, and crossing the line size costs you a second fetch per record. And the expensive fields are the ones the slow loop never names, which is why the cost is invisible at the place where it is paid.

[Chapter 05](05_dependency-and-hiding_agjy.md) uses the same underlying fact for a different argument: in an entity-component system the memory layout is deliberately made public, because hiding it would cost exactly the margin measured here.

Even more machine-specific than the reversal: the line size, the cache sizes and every latency above are facts about one machine in one year. [Chapter 04](04_grading-a-law_q5c6.md) uses this material as its own example of a law that drifts. Seven times is not a constant you may quote — it is what this layout cost on this hardware.
