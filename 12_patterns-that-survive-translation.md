# Patterns That Survive Translation

## The claim

**The patterns that last are answers to Forces, and grouping them by the Force they answer explains which one you need better than any catalogue organized by shape.**

That is a stronger claim than it sounds, and it is checkable. If it holds, then naming your Force should mostly hand you the pattern — and a pattern whose Force you cannot name is one you should be suspicious of.

So this chapter sorts the field against chapter 03's seven Forces, in chapter 03's order. Forty-nine patterns fall into them. Five refuse, and those five are the most interesting part, because what they have in common says something about the limits of the book's own model.

## How to read this chapter

Two kinds of pattern entry, and the difference matters.

**Worked patterns** — two per Force, with code, the constraint the pattern imposes, and what it costs. These carry the argument.

**Listed patterns** — the rest of each family, one line each. These are not explained, only placed. By now you have chapter 10's tests, so a one-line entry is something you can evaluate rather than something you have to accept.

---

## The demonstration

### Concurrency

> **Can two of these run at the same time and touch the same state?**

Chapter 06 owns the Law here and chapter 07 owns what happens across machines. These are the shapes that answer them.

**Aggregate** — a group of objects with one entry point, where the whole group is the unit of consistency.

```go
// The order is the aggregate root. Nothing outside reaches a line item.
type Order struct {
	ID    uuid.UUID
	lines []Line // unexported: only Order may change these
}

func (o *Order) AddLine(sku string, qty int) error {
	if o.total()+price(sku)*qty > o.creditLimit {
		return ErrOverLimit // an invariant across the whole group
	}
	o.lines = append(o.lines, Line{SKU: sku, Qty: qty})

	return nil
}
```

*The constraint:* the boundary is the transaction boundary. One aggregate is locked, read, and written as a unit, and a rule spanning two aggregates cannot be enforced synchronously — which is why aggregate boundaries are the most consequential modelling decision in a transactional system.

*The cost:* draw it too large and every operation contends on one row; too small and invariants leak out to the caller, where chapter 06 shows they cannot be enforced.

**Identity map** — within one unit of work, a given row is loaded once and the same object is returned to everyone.

```go
func (m *IdentityMap) Order(id uuid.UUID) (*Order, error) {
	if o, ok := m.loaded[id]; ok {
		return o, nil // the same pointer, not a second copy
	}
	// ... load, store in m.loaded, return
}
```

*The constraint:* two parts of one operation cannot hold divergent copies of the same row, which is a lost-update race (Ch. 06) that no amount of care at the call sites removes.

*The cost:* it is a cache, so chapter 04's definitional claim applies — it needs a lifetime, and the lifetime must be the unit of work rather than the process, or it becomes a stale-data source.

**The rest of this family**

- **Optimistic offline lock** — a version column; the writer whose version is stale is refused. Chapter 06 works it through.
- **Pessimistic offline lock** — take the lock for the duration; correct, and it holds a row across think-time, which is usually unaffordable.
- **Single writer** — remove the contention rather than manage it. Chapter 06 owns this, and chapter 08 shows what it does to throughput.
- **Idempotency key** — chapter 07 owns it; it is what makes at-least-once delivery survivable.
- **Saga** — chapter 07 owns it; the answer when the unit of consistency spans systems and no transaction can.

### Durability of the medium

> **If this process dies right now, what must still be true when it comes back?**

> **If this process dies right now, what must still be true when it comes back?**

It produces more patterns than any other Force.

**Unit of Work** — collect every change a business operation makes, then commit them together.

```go
func (u *UnitOfWork) Do(ctx context.Context, fn func(tx *sql.Tx) error) error {
	tx, err := u.db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer tx.Rollback() // no-op after a successful Commit

	if err := fn(tx); err != nil {
		return err // nothing written
	}

	return tx.Commit() // everything, or nothing
}
```

*The constraint:* no part of the operation may write outside the transaction. Anything that does — a queue publish, an HTTP call, a log line someone later depends on — breaks the guarantee, which is chapter 07's territory and the reason the Outbox exists.

*The cost:* the transaction is open for the whole operation, so slow work inside it holds locks. Chapter 06's registration example puts the hashing outside the lock for exactly this reason.

**Append-only log** — never update a row; write a new fact and derive the current state.

```sql
-- Not: update account set balance = balance - 100
insert into ledger_entry (account_id, delta_minor, reason, at)
values ($1, -100, 'withdrawal', now());
```

*The constraint:* nothing is ever destroyed, so history is a query rather than an archaeology project. In exchange, "the current balance" stops being a column and becomes a computation.

*The cost:* the table grows without limit, reads need aggregation or a maintained projection, and correcting a mistake means appending a compensating entry rather than fixing the wrong one — which is the honest version of what happened, and also more work.

**The rest of this family**

- **Write-ahead log** — record the intention to change before changing anything, so a crash can be replayed forward.
- **Event sourcing** — the append-only log as the *only* store, with all state derived from it.
- **Snapshot / freeze-at-time** — record what a value was when a decision used it, because the source will change and the decision must not.
- **Bitemporal modelling** — two timelines, what was true and when you learned it, so corrections do not rewrite history.
- **Table Data Gateway** — one object per table, holding the SQL; the minimum structure that keeps schema knowledge in one place.
- **Data Mapper** — the object model and the tables are allowed to differ, and something translates. Its cost is the translation; its benefit is that neither side constrains the other.
- **Transactional Outbox** — chapter 07 owns this one, and it is what you reach for when Unit of Work's constraint cannot be met.

### Blast radius

> **When this breaks, what else stops working?**

The patterns are all forms of containment.

**Bulkhead** — partition the resource so one consumer's failure cannot exhaust it.

```go
// One shared pool: a slow report starves checkout.
var db = pool(50)

// Separate pools: the report can exhaust its own and nothing else.
var checkoutDB = pool(40)
var reportingDB = pool(10)
```

*The constraint:* each partition has a hard ceiling and cannot borrow. That is the whole point — borrowing is what turns one component's bad day into everybody's.

*The cost:* utilization falls, because reserved capacity sits idle when its owner is quiet. You are buying isolation with efficiency, which is chapter 08's arithmetic and a genuinely uncomfortable trade to defend in a capacity review.

**Result types** — make failure part of the return value rather than a separate channel.

```rust
fn parse_amount(s: &str) -> Result<Money, ParseError>
```

```go
func ParseAmount(s string) (Money, error)
```

*The constraint:* the caller cannot reach the value without confronting the error. In Rust the compiler enforces it; in Go the convention plus a linter does; in a language with unchecked exceptions, nothing does, and the failure travels up until someone catches it or nobody does.

*The cost:* every layer handles or forwards, which is noisier than exceptions at the call site and clearer at the boundary. Whether that trade is worth it depends on how far a failure can travel before someone is responsible for it.

**The rest of this family**

- **Circuit breaker** — stop calling a failing dependency, so its slowness stops consuming your capacity. Chapter 10 uses the name as its example of a term that is a mediocre description and an excellent search key.
- **Timeout with backoff and jitter** — bound the wait, and spread the retries so recovery does not arrive as a synchronized stampede (Ch. 07).
- **Dead-letter queue** — a message that cannot be processed goes somewhere a human will find it, instead of blocking the queue or vanishing.
- **Parse, don't validate** — do the check once at the edge and return a type that cannot be invalid, so nothing downstream re-checks or forgets to.
- **Make illegal states unrepresentable** — the same move in the type system: if the invalid combination has no representation, no code path can produce it.

### Change frequency, and its shape

> **Which parts of this move at different rates?**

Every pattern here is a seam placed where two things move at different speeds — chapter 09's rate-of-change layers, made structural.

**Ports and adapters** — the application defines the interfaces it needs; the outside world implements them.

```go
package billing

// The port: what billing needs, in billing's own words.
type Rates interface {
	For(ctx context.Context, country string) (Rate, error)
}

// The adapter lives elsewhere and depends on billing, not the reverse.
```

*The constraint:* the dependency points inward. Chapter 05 owns why that matters — the interface is declared by the consumer, which is the only version that actually reverses an arrow.

*The cost:* an interface per boundary, and the reflex to add one everywhere is how a codebase acquires forty interfaces with one implementation each (Ch. 17).

**Strangler fig** — route traffic through a facade, move one route at a time, delete the old system when the last route has moved.

```text
            ┌──────────────┐
 requests ─►│   facade     │─► new service   (routes migrated so far)
            │              │─► legacy        (everything else)
            └──────────────┘
```

*The constraint:* both systems run at once, and something must decide per request which one serves it. That decision point is the pattern.

*The cost:* two systems in production, two on-call rotations, and data that may have to be written to both during the overlap. The migration is cheaper than a rewrite because it is reversible at every step, and it is not cheap.

**The rest of this family**

- **Pipes and filters** — stages that transform and hand on, each replaceable without the others. Chapter 05 notes these are not layers, and the difference matters.
- **Parameter object** — one struct instead of a growing argument list, so adding a field is not a signature change at every call site.
- **Repository** — a collection-like interface over storage. Worth chapter 10's tests before adopting: it compresses well, and what it rules out is thinner than its reputation suggests.
- **Feature toggle** — separate deploying code from enabling it, so the two can move at different rates. Its cost is that every live toggle doubles the paths under test.
- **Anti-corruption layer** — chapter 11 owns it: what a translation boundary becomes when the thing on the other side is not yours to change.

### Team size and turnover

> **How many must agree to change this, and how many will still be here in two years?**

This Force is the odd one, and the shape of its answer is worth noticing. It does not change *what* the rule is. It changes **where the rule lives** — chapter 03's migration from a comment, to a review habit, to the type system. So it produces fewer patterns of its own than the others, and mostly relocates rules the other Forces already produced.

**Make illegal states unrepresentable** — give the invalid combination no representation, so no code path can produce it.

```go
// Before: four fields, and three of the sixteen combinations are nonsense.
type Delivery struct {
	Shipped   bool
	ShippedAt time.Time
	Delivered bool
	SignedBy  string
}

// After: the states are the type, and there is no "delivered but not shipped".
type Delivery interface{ isDelivery() }

type Pending struct{}
type Shipped struct{ At time.Time }
type Delivered struct{ At time.Time; SignedBy string }
```

*The constraint:* the invalid case cannot be written down, so it cannot be checked for, forgotten, or reintroduced by someone who never heard the rule.

*The cost:* more types, and every consumer needs a switch rather than a field access. Worth it when the rule matters more than the convenience, and overhead when it does not.

**Golden test** — record the current output, and fail when it changes.

```text
 testdata/invoice_v3.golden      the exact bytes this produced last time
 go test -update                 deliberately re-record, in a visible commit
```

*The constraint:* behaviour cannot change silently. Whoever changes it must either fix the code or re-record the file, and re-recording shows up in review as a diff someone has to defend.

*The cost:* it captures everything, including things nobody meant to promise — which is Hyrum's Law (Ch. 05) turned into a test file. Golden tests over-constrain, and the noise from irrelevant changes is the price of catching the relevant ones.

**The rest of this family**

- **Architecture decision record** — the reasoning written down at the time, for the people who were not there. Its whole value is turnover; on a stable team of two it is overhead.
- **Composition root** — one place where everything is assembled, so a newcomer has one file to read rather than a graph to trace (Ch. 05).
- **Parse, don't validate** — also a blast-radius pattern, and listed there. Its team-size value is separate: a parsed type carries the rule, so nobody downstream has to know it.
- **Contract tests** — also a control-of-callers pattern. Same double duty: the agreement is written down rather than remembered.

### Latency budget

> **What is the budget, and what does one mechanism cost of it?**

Chapter 08 supplies the arithmetic underneath all of these.

**Batching** — replace N round trips with one.

```go
// N round trips
for _, row := range rows {
	db.Exec("insert into t values ($1)", row)
}

// One
db.Exec("insert into t values " + placeholders(len(rows)), args...)
```

At one millisecond per round trip:

```text
1000 rows, one call each :   1145 ms
1000 rows, batches of 100:     11 ms   (100x)
```

*The constraint:* the batch is the unit of failure. One bad row can reject the whole batch, so you need a policy — fail all, skip and report, or retry individually — and choosing it is the actual design work.

*The cost:* latency for the first item rises, because it waits for the batch to fill. Throughput and latency trade against each other here, and which you want is a product decision rather than an engineering one.

**Cache-aside** — check the cache, fall through to the source, populate on the way back.

```go
if v, ok := cache.Get(k); ok {
	return v
}
v := source.Get(k)
cache.Set(k, v, ttl)
```

*The constraint:* the cached copy may be stale, so the design is not the lookup — it is the invalidation. Chapter 04 uses this exact claim as its example of something true by definition: a copy with no invalidation strategy is a copy that is allowed to be wrong.

*The cost:* a second source of truth, a stampede when a popular key expires and every request misses at once, and a debugging surface where the answer depends on what happened earlier.

**The rest of this family**

- **Object pool** — reuse expensive-to-create things. Chapter 08's warning applies: measure, because a pool can easily cost more than the allocation it avoids.
- **Backpressure** — when the consumer cannot keep up, make the producer wait rather than growing a queue. The alternative is chapter 08's queue curve, and it ends in memory exhaustion.
- **CQRS** — separate the write model from the read model, so each can be shaped for its own access pattern. Its real cost is that they are now two models that can disagree.
- **Materialised view** — precompute the answer, and accept that it lags.
- **Data-oriented layout** — chapters 05 and 08 own it; the 7× that comes from where the bytes sit rather than what the algorithm does.

### Control of the callers

> **Who else depends on this, and can I change them?**

Chapter 09's compatibility rule and chapter 11's ownership line both land here. The patterns are ways of making a boundary survivable.

**Tolerant reader** — read only the fields you need, and ignore everything else.

```go
// Only these three. Any other field in the payload is discarded silently.
type OrderView struct {
	ID     string `json:"id"`
	Total  int64  `json:"total_minor"`
	Status string `json:"status"`
}
```

*The constraint:* you may not fail on an unrecognized field, which means you cannot use strict schema validation on the inbound side.

*The cost:* a field that disappears reads as its zero value rather than as an error — chapter 09 shows that is the silent failure, and it is the price of the tolerance.

**Consumer-driven contracts** — each consumer publishes the subset of your interface it actually relies on, and your build fails if you break one.

```text
 checkout-service expects:  POST /v1/orders  ->  {id, total_minor}
 reporting-service expects: GET  /v1/orders  ->  {id, total_minor, placed_at}
                                                  ^ nobody depends on `status`
```

*The constraint:* the contract set is the real interface, and it is smaller than the published one — which tells you what you can change, a thing that is otherwise unknowable (Ch. 05's Hyrum's Law).

*The cost:* every consumer must maintain its contract, and a consumer that does not participate is invisible to the check. The pattern works exactly as well as its coverage.

**The rest of this family**

- **Bounded context** — one model per context, with translation between them, rather than one model everyone must agree on. Chapter 09's Conway material is why the boundaries end up where they do.
- **Composition root** — one place where the object graph is assembled, so nothing else needs to know how anything is built (Ch. 05).
- **Expand and contract** — add the new field, migrate readers, then remove the old one, in three deploys rather than one. Chapter 09's add-only rule is what forces the shape.
- **Contract tests** — verify both sides against the same shared expectation, rather than trusting a document.

---

## Why the claim holds

Two questions worth separating: why do these patterns last, and why does the grouping work?

**They last because a Force outlives a language.** Concurrency was a problem in 1970 and is a problem now. Data outlives code in COBOL and in Rust. Someone else always depends on your interface. A pattern answering one of those describes the shape of the problem rather than a gap in a toolchain — which is why it is still recognizable after being carried into a language its author never used. Chapter 13 takes the converse: a name that disappears when the language changes was answering the language, not the problem.

**The grouping works because a pattern is a Force with a shape attached.** If two patterns answer the same Force, they are alternatives, and knowing the Force tells you which question you are choosing between. Optimistic and pessimistic locking are not two techniques to learn; they are two answers to *how often do writers collide*, and the intensity of that Force picks one.

That is the practical use of the whole chapter. **Catalogues are organized by shape, so they let you look up what you already know the name of.** Grouping by Force lets you find the name from the situation, which is the direction you actually need.

---

## Where the claim doesn't apply

### The five that refuse to sort

Sorting the field left five patterns that do not answer a Force, and they fail in two distinct ways.

**Some answer a goal rather than a situation.** Property-based testing, the test-double taxonomy, and functional core / imperative shell all answer *how will I know this works* — which is something you want, not a property of your circumstances. Chapter 03 is explicit that a Force is a fact about where you are standing and is not negotiable by argument. Testability is negotiable: you may decide you want less of it.

That is a real gap in this chapter's method, not a defect in the patterns. Chapter 17 covers the testing material, and it is organized by what the techniques actually buy rather than by Force, for exactly this reason.

**Golden tests used to be in this list and no longer are**, which is worth recording because it shows the sort is doing work rather than confirming a guess. A first pass ran against six invented Force names and left golden tests homeless. Using chapter 03's actual seven — and so restoring *team size and turnover*, which the invented list had dropped — gave them an obvious home: a golden test exists so that behaviour cannot change silently under people who did not write it. **A pattern that will not sort is sometimes evidence about the categories rather than about the pattern.**

**Some answer what the problem is rather than what the situation is.** A state machine is the right shape when the domain genuinely has states and transitions — an order that is placed, then paid, then shipped. That is a fact about the business, not about your concurrency or your latency budget. The same goes for Transaction Script, which chapter 10 uses as its compression example: it is what you write when *no* Force is pushing you anywhere else, and it is right far more often than its reputation suggests.

So the honest form of this chapter's claim is narrower than the opening states it: **patterns that answer situational Forces sort by Force. Patterns that answer the shape of the problem, or a goal you have chosen, do not** — and confusing the three is one way people end up applying machinery that answers a question they were not asking.

### One Force, several answers, and no way to choose from here

Knowing the Force narrows the field; it rarely closes it. *Writers collide* gives you optimistic locking, pessimistic locking, single-writer partitioning, and a serializable transaction, and choosing between them needs the Force's **intensity** — chapter 03's dial — plus what you are willing to pay.

This chapter sorts. It does not decide. Chapter 19 is the one that turns a set of Forces into a design.

### The listed entries are not endorsements

The one-line entries above place each pattern; they do not recommend it. Repository and Active Record are both listed, and they are alternatives with opposite trade-offs. CQRS is listed and is wrong for most systems that adopt it.

Run chapter 10's tests before using any of them, and chapter 11's question before believing the cost estimate. A list is a map of what exists, which is a different thing from a set of instructions.

---

## What the claim costs

**The grouping is a lens, and lenses distort.** Several patterns answer two Forces — an outbox is both durability and concurrency, a bounded context is both change frequency and ownership — and filing each under one is a simplification. Where a pattern appears matters less than that it appears somewhere; do not read the placement as a claim about its essence.

**Naming the Force is genuinely hard, and this chapter makes it look easy.** In a real design the Forces arrive tangled, and half of them are estimates about the future (Ch. 03). The neat question at the head of each section is the output of the analysis, not the input.

**A grouped list still invites shopping.** Chapter 10's warning about catalogues applies here too: six well-organized shelves are still shelves, and *we should use a Saga* is as available a sentence after reading this as before. The defence is the same — say which Force, and at what intensity.

**Fifty names is more vocabulary than most systems need.** A great deal of good software uses four or five of these and nothing else. Breadth here is for recognizing what somebody else built, not a target to work through.

---

## How to recognize the failure

**In a codebase:**

- **A pattern whose Force you cannot name.** Ask what would break without it. If the answer is nothing concrete, it is structure that was applied rather than derived.
- **Two patterns answering the same Force, both present.** An optimistic version column *and* a pessimistic lock on the same rows means somebody added the second without removing the first, and the invariant now depends on which path ran.
- **A pattern from the durability family with no durable medium** — event sourcing over a cache, an append-only log that is truncated weekly.
- **Bulkheads that share a limit.** Two pools that both draw from the same connection ceiling are one pool with extra configuration.
- **A cache with no invalidation** and no note saying why none is needed (Ch. 04).
- **A strangler facade with no route ever migrated**, which is two systems and none of the benefit.

**In a conversation:**

- **"We should use X."** Which Force, and how intense? If neither can be answered, the proposal is a shape looking for a problem.
- **"That's the standard pattern for this."** Standard where, and answering which Force? Chapter 11's question applies to the recommendation too.
- **"We'll need CQRS eventually."** Eventually is chapter 03's territory: does the decision expire, and is it cheap today? For CQRS, both answers are unfavourable.
- **Someone reciting a list of patterns as a design.** A list of shapes is not a design until each one is attached to a Force.

The question that does the work: **which Force is this answering, and how strongly?**

A pattern with a Force behind it can be argued about on the merits — you can disagree about the intensity, and the disagreement is resolvable. A pattern with no Force behind it can only be argued about on taste, which is the argument this book exists to end.

---

**Next:** chapter 13 takes the converse of this chapter's test. If a pattern survives translation because it answers a Force, then a pattern that *disappears* when you change language was answering the language — and a surprising share of the best-known catalogue turns out to be exactly that.
