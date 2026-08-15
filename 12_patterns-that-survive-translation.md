# Patterns That Survive Translation

## The claim

**The patterns that last are answers to Forces, or answers to the shape of the problem — and grouping them by the Force they answer tells you which one you need, where a catalogue organized by pattern shape cannot.**

Two halves, and the second is the practical one. A catalogue is arranged by what patterns look like, so it can only be searched by a name you already have. Arranged by Force, the same material can be searched from the situation, which is the direction you are actually travelling.

So this chapter sorts the field against chapter 03's seven Forces, in chapter 03's order. Forty-nine patterns fall into them, and a handful answer the shape of the problem instead — a state machine is right when the domain has states, which is a fact about the business rather than about your circumstances. What is left over after both is the interesting residue, and it is dealt with in the boundary section.

## How to read this chapter

Two kinds of pattern entry, and the difference matters.

**Worked patterns** — two per Force, with code, the constraint the pattern imposes, and what it costs. These carry the argument.

**Listed patterns** — the rest of each family, one line each. These are not explained, only placed. By now you have chapter 10's tests, so a one-line entry is something you can evaluate rather than something you have to accept.

Each worked pattern carries two labelled lines, and they answer different questions.

- ***The constraint*** — what the pattern **forbids** once you adopt it. This is chapter 10's second test applied: a name that rules nothing out carries no information, so a pattern with no constraint is not a pattern. It is not a list of prerequisites; it is what you may no longer do.
- ***The cost*** — what you pay for the constraint, in work, in performance, or in something you can no longer see.

Patterns another chapter owns appear with a pointer instead of a definition.

---

## The demonstration

### Force: Concurrency

> **Can two of these run at the same time and touch the same state?**

Chapter 06 owns the Law here and chapter 07 owns what happens across machines. These are the shapes that answer them.

The Force splits into two questions, and the patterns split with it. **What has to change together?** — and, separately, **what stops two writers changing it at once?** The first must be answered before the second can be applied, because you cannot lock a boundary you have not drawn.

**Pattern: Aggregate** — a group of objects with one entry point, where the whole group is the unit of consistency.

```go
// The order is the aggregate root. Nothing outside reaches a line item.
type Order struct {
	ID    uuid.UUID
	lines []Line // unexported: only Order may change these
}

func (o *Order) AddLine(sku string, qty int) error {
	// An invariant across the whole group: no line may take the order
	// over its credit limit, which is only checkable with every line in hand.
	if o.total()+price(sku)*qty > o.creditLimit {
		return ErrOverLimit
	}
	o.lines = append(o.lines, Line{SKU: sku, Qty: qty})

	return nil
}
```

*The constraint:* nothing outside the root may touch a line item, and the whole group is read and written as one. So a rule spanning two aggregates cannot be enforced in a single transaction — which is what makes aggregate boundaries the most consequential modelling decision in a transactional system.

*The cost:* draw the boundary too large and every operation contends on one row; too small and invariants leak out to the caller, where they cannot be enforced at all.

**It answers the first question only, and this is worth being exact about.** Two requests that both load order 42, both check the credit limit, and both add a line will both succeed — the aggregate did not stop them, and nothing in the pattern claims it would. That is chapter 06's lost update, and it needs a mechanism: a version column that refuses the stale writer, or a lock held across the read and the write.

What the aggregate contributes is the thing that mechanism needs. It says **order 42 and its lines are one unit**, so there is exactly one row to version and one boundary to lock. Without it you are left asking which of eleven tables to lock and in what order, which is how deadlocks are made.

So the two are not alternatives. One draws the boundary; the other defends it.

**Pattern: Identity map** — within one unit of work, a given row is loaded once and the same object is returned to everyone.

```go
// One map per unit of work, so two lookups of the same row give one object.
type IdentityMap struct {
	db     *sql.DB
	loaded map[uuid.UUID]*Order
}

func (m *IdentityMap) Order(ctx context.Context, id uuid.UUID) (*Order, error) {
	if o, ok := m.loaded[id]; ok { // comma-ok: ok reports whether the key was there
		return o, nil // the same pointer, not a second copy
	}
	o, err := loadOrder(ctx, m.db, id)
	if err != nil {
		return nil, err
	}
	m.loaded[id] = o
	return o, nil
}
```

The effect is at the call sites, where two parts of one operation each load what they need:

```go
shipping, err := m.Order(ctx, id)
billing, err := m.Order(ctx, id) // no second query

shipping.AddLine(1000)
billing.Total() // 3500 — includes the line shipping just added
```

One round trip, and no way for the two to disagree about what order 42 currently is.

*The constraint:* two parts of one operation cannot hold divergent copies of the same row, which is a lost-update race (Ch. 06) that no amount of care at the call sites removes.

*The cost:* it is a cache, so it needs a lifetime — and the lifetime must be the unit of work rather than the process, or it quietly becomes a source of stale data.

**The rest of this family**

- **Optimistic offline lock** — a version column; the writer whose version is stale is refused. Chapter 06 works it through.
- **Pessimistic offline lock** — take the lock for the duration; correct, and it holds a row across think-time, which is usually unaffordable.
- **Single writer** — remove the contention rather than manage it. Chapter 06 owns this, and chapter 08 shows what it does to throughput.
- **Idempotency key** — chapter 07 owns it; it is what makes at-least-once delivery survivable.
- **Saga** — chapter 07 owns it; the answer when the unit of consistency spans systems and no transaction can.

### Force: Durability of the medium

> **If this process dies right now, what must still be true when it comes back?**

It produces more patterns than any other Force.

**Pattern: Unit of Work** — collect every change a business operation makes, then commit them together.

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

*The constraint:* no part of the operation may write outside the transaction. Anything that does — a queue publish, an HTTP call, a log line someone later depends on — breaks the guarantee, and is the reason the outbox exists.

*The cost:* the transaction is open for the whole operation, so slow work inside it holds locks.

**Pattern: Append-only log** — never update a row; write a new fact and derive the current state.

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

### Force: Blast radius

> **When this breaks, what else stops working?**

The patterns are all forms of containment.

**Pattern: Bulkhead** — partition the resource so one consumer's failure cannot exhaust it.

```go
// One shared pool: a slow report starves checkout.
var db = pool(50)

// Separate pools: the report can exhaust its own and nothing else.
var checkoutDB = pool(40)
var reportingDB = pool(10)
```

*The constraint:* each partition has a hard ceiling and cannot borrow. That is the whole point — borrowing is what turns one component's bad day into everybody's.

*The cost:* utilization falls, because reserved capacity sits idle when its owner is quiet. You are buying isolation with efficiency, which is an uncomfortable trade to defend in a capacity review.

**Pattern: Result types** — make failure part of the return value rather than a separate channel.

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
- **Parse, don't validate** — worked under team size, where its distinctive value is; it belongs here too, because a value that cannot be invalid cannot spread an invalid one.
- **Make illegal states unrepresentable** — the same move in the type system: if the invalid combination has no representation, no code path can produce it.

### Force: Change frequency, and its shape

> **Which parts of this move at different rates?**

Every pattern here is a seam placed where two things move at different speeds — chapter 09's rate-of-change layers, made structural.

**Pattern: Ports and adapters** — the application defines the interfaces it needs; the outside world implements them.

```go
package billing

// The port: what billing needs, in billing's own words.
type Rates interface {
	For(ctx context.Context, country string) (Rate, error)
}

// The adapter lives elsewhere and depends on billing, not the reverse.
```

*The constraint:* the interface is declared by the consumer rather than the provider, which is what reverses the arrow — a provider-declared interface leaves the dependency pointing exactly where it was (Ch. 05).

*The cost:* an interface per boundary, and the reflex to add one everywhere is how a codebase acquires forty interfaces with one implementation each (Ch. 17).

**Pattern: Strangler fig** — route traffic through a facade, move one route at a time, delete the old system when the last route has moved.

```text
            ┌──────────────┐
 requests ─►│   facade     │─► new service   (routes migrated so far)
            │              │─► legacy        (everything else)
            └──────────────┘
```

*The constraint:* both systems run at once, and something must decide per request which one serves it. That decision point is the pattern.

*The cost:* two systems in production, two on-call rotations, and data that may have to be written to both during the overlap — for as long as the migration runs, which is usually longer than planned. What you buy is the ability to stop: every route moved is a route you can move back.

**The rest of this family**

- **Pipes and filters** — stages that transform and hand on, each replaceable without the others. Chapter 05 notes these are not layers, and the difference matters.
- **Parameter object** — one struct instead of a growing argument list, so adding a field is not a signature change at every call site.
- **Repository** — a collection-like interface over storage. Worth chapter 10's tests before adopting: it compresses well, and what it rules out is thinner than its reputation suggests.
- **Feature toggle** — separate deploying code from enabling it, so the two can move at different rates. Its cost is that every live toggle doubles the paths under test.
- **Anti-corruption layer** — chapter 11 owns it: what a translation boundary becomes when the thing on the other side is not yours to change.

### Force: Team size and turnover

> **How many people must agree to change this, and how many of today's people will still be here in two years?**

This Force is the odd one, and the shape of its answer is worth noticing. It does not change the invariants of the system: *amounts are in minor units, never floats*; *these two columns are set together or not at all*; *a visit may be completed once*. What the Force changes is **where the invariants are held**, along chapter 03's migration from a comment, to a review habit, to the type system.

So team size produces fewer patterns of its own than the others; mostly it relocates invariants the other Forces produced.

**Pattern: Parse, don't validate** — check once at the edge and return a type that cannot be invalid, instead of checking a plain value and passing it on.

The version where the invariants live in people's heads:

```go
func handleSignup(w http.ResponseWriter, r *http.Request) {
	email := r.FormValue("email")
	if !looksLikeEmail(email) {
		http.Error(w, "bad email", 400)
		return
	}

	signUp(email) // a plain string; the check did not travel with it
}

func signUp(email string) { /* trust it? re-check it? nobody knows */ }
```

`signUp` takes a `string`, so nothing distinguishes a checked email from any other text. The rule — *emails are validated before they get here* — exists in whoever wrote the handler. The next caller, added in a year by somebody else, may not know it.

The version where the rule lives in the compiler:

```go
// Email's only constructor is ParseEmail, so holding one is proof it parsed.
type Email struct{ addr string }

func ParseEmail(s string) (Email, error) {
	if !looksLikeEmail(s) {
		return Email{}, ErrBadEmail
	}

	return Email{addr: s}, nil
}

func signUp(e Email) { /* nothing to check; it could not have got here otherwise */ }
```

*The constraint:* `signUp` can no longer be called with an unchecked string — the code does not compile. So the check cannot be skipped, duplicated, or forgotten by someone who never heard of it.

*The cost:* a type and a constructor per rule, and a conversion at every boundary where raw input arrives. Go enforces this across packages rather than within one, so the guarantee is only as strong as the package boundary you put it behind.

**Pattern: Make illegal states unrepresentable** — the same move applied to combinations rather than to values.

A delivery has four fields, and most of their sixteen combinations are nonsense — delivered but not shipped, a signature with no delivery time:

```go
type Delivery struct {
	Shipped   bool
	ShippedAt time.Time
	Delivered bool
	SignedBy  string
}
```

Make each state its own type, and make the *transition* the only way to reach the next one:

```go
type Pending struct{}

func (Pending) Ship(at time.Time) Shipped {
	return Shipped{at: at}
}

type Shipped struct{ at time.Time }

// The only constructor for Delivered, and it needs a Shipped to exist.
func (s Shipped) Deliver(at time.Time, signedBy string) Delivered {
	return Delivered{shippedAt: s.at, at: at, signedBy: signedBy}
}

type Delivered struct {
	shippedAt time.Time // carried over, so it cannot be missing
	at        time.Time
	signedBy  string
}
```

From a caller in another package, the sequence is the only route through:

```go
// A Delivered can only be reached by shipping first. The compiler enforces it.
d := delivery.Pending{}.Ship(shippedAt).Deliver(deliveredAt, "A. Okonkwo")

// Will not compile: cannot refer to unexported field at
// in struct literal of type delivery.Delivered
d2 := delivery.Delivered{at: deliveredAt}
```

**Go stops one step short of the pattern's name, and it is worth being exact about where.** `delivery.Delivered{}` — the empty literal, naming no fields — compiles from anywhere. Go gives every struct type a zero value and offers no way to withhold it. So the state is not strictly unrepresentable; what is unreachable is a *populated* illegal state. Nobody outside the package can produce a `Delivered` carrying a signature and a delivery time without having held a `Shipped` first.

That is a weaker guarantee than the pattern promises, and a different one from what the original struct gave you. `Delivery{Delivered: true}` is a lie that reads as data. A zero `Delivered` has no times and no signature, so it fails at the first field anyone reads.

The languages this pattern comes from do not have the hole. A Rust `enum` or an F# discriminated union has no zero value to fall back to, and the compiler will not let a `match` ignore a case. Which is the chapter's own subject arriving in miniature: the shape crosses into Go, the guarantee does not, and the difference is invisible if you only carry the name across.

*The constraint:* the populated invalid combination has no representation, so it cannot be produced, tested for, or reintroduced.

*The cost:* more types, and consumers need a type switch rather than a field read. Plus the zero value above, and the fact that the wall is the package — inside it, every field is reachable and the guarantee is a convention again.

**The rest of this family**

- **Architecture decision record** — the reasoning written down when it was fresh, for the people who were not in the room. Its entire value is turnover; on a stable team of two it is overhead.
- **Composition root** — one place where the object graph is assembled, so a newcomer reads one file rather than tracing a graph (Ch. 05).
- **Golden test** — assert a whole recorded artifact rather than picked-out fields. Worth it where the output is too large or too structured to assert piecemeal — a rendered invoice, a generated migration — and where you want changes nobody anticipated to show up as a diff. It over-constrains by design, which is the trade.
- **Contract tests** — also a control-of-callers pattern, worked there. Same double duty: an agreement written down rather than remembered.

### Force: Latency budget

> **What is the budget, and what does one mechanism cost of it?**

Chapter 08 supplies the arithmetic underneath all of these.

**Pattern: Batching** — replace N round trips with one.

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

**Pattern: Cache-aside** — check the cache, fall through to the source, populate on the way back.

```go
if v, ok := cache.Get(k); ok {
	return v
}
v := source.Get(k)
cache.Set(k, v, ttl)
```

*The constraint:* the cached copy may be stale, so the design is not the lookup — it is the invalidation. A copy with no invalidation strategy is a copy that is allowed to be wrong (Ch. 04).

*The cost:* a second source of truth, a stampede when a popular key expires and every request misses at once, and a debugging surface where the answer depends on what happened earlier.

**The rest of this family**

- **Object pool** — reuse expensive-to-create things. Chapter 08's warning applies: measure, because a pool can easily cost more than the allocation it avoids.
- **Backpressure** — when the consumer cannot keep up, make the producer wait rather than growing a queue. The alternative is chapter 08's queue curve, and it ends in memory exhaustion.
- **CQRS** — separate the write model from the read model, so each can be shaped for its own access pattern. Its real cost is that they are now two models that can disagree.
- **Materialised view** — precompute the answer, and accept that it lags.
- **Data-oriented layout** — chapters 05 and 08 own it; the 7× that comes from where the bytes sit rather than what the algorithm does.

### Force: Control of the callers

> **Who else depends on this, and can I change them?**

Chapter 09's compatibility rule and chapter 11's ownership line both land here. The patterns are ways of making a boundary survivable.

**Pattern: Tolerant reader** — read only the fields you need, and ignore everything else.

The version that breaks when the other side improves:

```go
// Strict: rejects any field it does not know about.
dec := json.NewDecoder(body)
dec.DisallowUnknownFields()

var v OrderView
err := dec.Decode(&v) // the day they add "currency", this starts failing
```

Adding a field is the one change chapter 09 says is always safe, so a reader that fails on it has turned their safe change into your outage. The tolerant version simply does not look:

```go
// Only these three. Any other field in the payload is discarded silently.
type OrderView struct {
	ID     string `json:"id"`
	Total  int64  `json:"total_minor"`
	Status string `json:"status"`
}

var v OrderView
err := json.Unmarshal(body, &v) // unknown fields are skipped
```

*The constraint:* you may not fail on an unrecognized field, which means you cannot use strict schema validation on the inbound side.

*The cost:* a field that disappears reads as its zero value rather than as an error, which is the silent failure of chapter 09 and the price of the tolerance.

**Pattern: Consumer-driven contracts** — each consumer records the subset of your interface it actually uses, and your build replays those recordings against the real implementation.

The part that sounds impossible is that consumers hand-write a specification and send it to you. They do not. The contract is a **by-product of the consumer's own tests**, and the flow is mechanical:

```text
1  checkout-service writes a test against a mock of your API,
   declaring the request it sends and the response it needs
2  running that test emits a contract file — the interactions,
   as JSON, generated rather than written
3  the file is published to a shared broker
4  your CI fetches every consumer's file and replays the requests
   against the real service, checking the responses still match
5  a response that no longer satisfies a consumer fails YOUR build,
   before release rather than after
```

Pact is the widely used implementation of this, and the shape above is how it works. What makes it tractable is step two: nobody maintains a contract document, because the contract falls out of a test the consumer wanted anyway.

The payoff is knowing what is safe to change:

*Can we drop `status` from the orders endpoint? We do not need it internally any more, but something out there might.* Without contracts that question has no answer short of asking every team and believing them. With contracts you read it off the broker, which holds the union of what every consumer's tests actually asked for:

```text
 checkout-service uses:   POST /v1/orders  ->  id, total_minor
 reporting-service uses:  GET  /v1/orders  ->  id, total_minor, placed_at

 status is published, and no contract mentions it — so it can go
```

*The constraint:* the contract set becomes the real interface, and it is smaller than the published one. You may change anything nobody recorded.

*The cost:* both sides must adopt the tooling, and a broker is one more piece of infrastructure to run. More seriously, **a consumer who does not participate is invisible** — the green build says "no recorded expectation broke," not "nobody broke." The pattern is exactly as good as its coverage, and it converts chapter 05's unknowable dependency set into a known-but-incomplete one.

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

**Some answer what the problem is rather than what the situation is.** A state machine is the right shape when the domain genuinely has states and transitions — an order that is placed, then paid, then shipped. That is a fact about the business, not about your concurrency or your latency budget. The same goes for Transaction Script, which chapter 10 uses as its compression example: it is what you write when *no* Force is pushing you anywhere else, and it is right far more often than its reputation suggests.

That is the residue the claim leaves, and it is worth naming as a third category rather than folding into either. **A Force is a fact about your circumstances. The shape of the problem is a fact about the business. A goal is something you chose and could choose differently** — and only the first two generate patterns that sort.

[claude I noticed two paragraphs below are mainly a repetision of the previous paragraphs that start on line 513
My sugeestion: replace the paragraph on line 513 with the paragraph below this tag, keeping the **Some answer a goal...**
Remove "That is the residue..." paragraph. Adding "your circumstances" seems like a strecht with no real value to me.
Also replace the opening of "Confusing the three" paragraph with "Confusing the forces, goals and problem shapes in play is one way..." ]
A goal is a property you have decided to want in the system: testability, observability, portability, a particular standard of code review. The test that separates it from a Force is whether you can decide to want less of it and stay honest. You cannot decide that four teams will stop needing to agree, or that the network will stop dropping packets — those are true whatever you want. You can decide that a prototype does not need to be portable, or that a script does not need tests, and nothing has been denied. That is why the testing patterns will not sort: they answer *how will I know this works*, which is a question you elected to ask.

Confusing the three is one way people end up applying machinery to a question they were not asking: reaching for an event-sourced log because durability sounds important, when what the domain actually has is a state machine; or adopting a testing technique because it is rigorous, rather than because anything about the situation called for it.

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
