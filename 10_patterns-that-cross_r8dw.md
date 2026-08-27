# Patterns That Cross the Line

## The claim

**The same pattern name describes a change you can make in an afternoon and a commitment you will maintain for years when it crosses the ownership line. What separates them is not size. It is whether you can change the other side.**

People usually call this a question of scale, and size does correlate with it, because systems acquire other owners as they grow. But size is not the cause, and the two come apart in a way worth being precise about.

A ten-thousand-line refactor inside your own repository is a large piece of work. It is not a large *commitment*: when it is done it is done, nobody else's release schedule bears on it, and if you get the design wrong you can change it again. A fifty-line integration with a payment provider is a small piece of work and a permanent obligation — it has to keep working through their changes, forever, and you will not be consulted about them.

Those are different kinds of expensive, and only the second is what this chapter is about.

The question that decides it is one sentence long:

> **Can I change the thing on the other side?**

If yes, a pattern is one option among several, and often not the cheapest. If no, most of the options were never available — and what looks like a design choice is really the acknowledgment of a constraint.

The rest of the chapter is one worked example crossing that line, and then what happens to the familiar pattern names when they cross it.

---

## The demonstration

Throughout: **FastSell**, a shop. It takes payments and it keeps a ledger.

### Both sides yours: the pattern is optional

FastSell started with its own payment code. Two internal packages, both written in-house, and their types do not quite line up:

```go
// package payments — what a completed charge hands back
type Receipt struct {
	Ref      string // the payment's identifier
	Cents    int64  // amount in cents; never a float (Ch. 02)
	Complete bool   // true once the money has actually moved
}

// package billing — what the ledger wants to store
type LedgerEntry struct {
	Ref   string // same identifier, so the two can be reconciled
	Minor int64  // amount in minor units — cents, pence, yen
	Final bool   // true when this entry will not change again
}
```

The two carry the same three facts under different names. That matters because of where they meet — the checkout handler, which takes one and must produce the other:

```go
func (h *Checkout) Complete(orderID string) error {
	receipt, err := h.payments.Charge(orderID)
	if err != nil {
		return err
	}

	return h.billing.Record( /* a LedgerEntry, from a Receipt */ )
}
```

**Adapter** is the pattern for exactly this: wrap a thing so it fits an interface it was not built for. Filling that gap:

```go
func adapt(receipt Receipt) LedgerEntry {
	return LedgerEntry{Ref: receipt.Ref, Minor: receipt.Cents, Final: receipt.Complete}
}

// h.billing.Record(adapt(receipt))
```

Three lines, works fine, and **it is the second-best answer.** Both files are yours, so there is another move available:

```go
// package payments — the fields renamed to match, and the adapter deleted.
type Receipt struct {
	Ref   string
	Minor int64
	Final bool
}
```

```go
// billing now takes it directly. No wrapper, no mapping, nothing to keep in step.
func Record(receipt payments.Receipt) { ... }
```

That is the whole fix: rename two fields and delete the adapter. It is smaller, there is no second representation to drift, and nothing has to be updated when a field is added.

**This is why the pattern is cheap here, and the line count is not the reason.** It is that a third option exists — change the other side — and it is usually better than adapting. The pattern is available and unnecessary.

*(Worth noting how completely this can evaporate. In Go, a type satisfies an interface by having the right methods, with no declaration required, so an adapter that exists only to announce conformance is not written at all. In C# or Java the same requirement produces a wrapper class per type. [Chapter 12](12_missing-language-features_esqm.md) takes up names whose content depends on the language that way.)*

### One side theirs: the option disappears

FastSell drops its own payment code and moves to Stripe. Nothing about the shape of the problem has changed — a payment result still has to become a ledger entry — but one thing has:

```go
// Theirs. You cannot edit it, and it changes on their schedule.
type StripeCharge struct {
	ID       string
	Amount   int64
	Status   string // "succeeded" "pending" "failed" "requires_action" ...
	Currency string
}
```

You cannot rename `Amount` to `Minor`. You cannot collapse their eleven statuses into the one boolean your ledger has. **The better answer from the previous section is not available**, and adapting is no longer one option among several — it is the only one.

Which turns the question into *where*. Without a boundary, their vocabulary goes wherever it is convenient:

```go
func receipt(charge StripeCharge) string   { if charge.Status == "succeeded" { ... } }
func ledger(charge StripeCharge) int64     { if charge.Status == "succeeded" { ... } }
func alert(charge StripeCharge) bool       { return charge.Status == "failed" }
func refundable(charge StripeCharge) bool  { return charge.Status == "succeeded" }
func reconcile(charge StripeCharge) bool   { return charge.Status == "succeeded" || charge.Status == "pending" }
```

With one, it stops at the edge and everything behind it speaks FastSell:

```go
func fromStripe(charge StripeCharge) LedgerEntry {
	return LedgerEntry{Ref: charge.ID, Minor: charge.Amount, Final: charge.Status == "succeeded"}
}
```

Both versions produce identical output today. The difference shows up when Stripe splits `succeeded` into `succeeded` and `settled`, which they may do without asking:

```text
 sites that test Stripe's vocabulary and must be revisited
   without a boundary   6
   with a boundary      1   (inside fromStripe)
```

Six is small because the example is small; a real integration reaches further. **The boundary converts a change that lands everywhere into a change that lands once** — [chapter 04](04_structure_agjy.md)'s argument about fan-in, applied to a dependency whose release schedule is not yours.

The pattern literature calls this an **Anti-Corruption Layer**, a name from Eric Evans, where the corruption is another system's model spreading into yours. Note what it costs: a translation function, a set of mappings that encode real judgements, tests for code that does nothing but rename fields, and somebody whose job includes reading Stripe's release notes.

**Same pattern, same shape, both times.** In the first case, three lines that were better deleted. In the second, a file, an owner, and a standing obligation.

### The names, and what crossing the line does to them

| Pattern | Both sides yours | The other side is theirs | What appears when it crosses |
|---|---|---|---|
| **Adapter** | a wrapper, or nothing at all | Anti-Corruption Layer | their model changes without asking ([Ch. 08](08_change_rjf9.md)) |
| **Facade** | an object with fewer methods | a service boundary or public API | your surface becomes permanent ([Ch. 04](04_structure_agjy.md), 09) |
| **Observer** | a list of callbacks | a message bus | delivery can fail, or repeat ([Ch. 06](06_distribution_49yh.md)) |
| **Proxy** | a wrapper adding behaviour | a network hop, with retries and caching | latency floor, partial failure ([Ch. 06](06_distribution_49yh.md), 08) |

Read the last column first. What changes across a row is not the amount of code — it is that something can now go wrong that could not go wrong before, and each of those is a Law from Part II.

**How solid is each row?** Worth answering, because the rows are not equally well supported and the chapter should not pretend otherwise.

- **Proxy** is in the original catalogue. The Gang of Four list a *remote proxy* — "a local representative for an object in a different address space" — as one of the pattern's named variants. Crossing the line is not an extension here; it was in the definition.
- **Adapter** is supported by the anti-corruption layer literature. Evans describes such a layer as containing translators, which is what an adapter is. The structure is genuinely the same on both sides; what is added is the obligation to maintain it.
- **Facade** is this book's extension. Nobody's catalogue says a facade becomes a public API. The observation is that the structure is identical — fewer methods over more machinery — and that once the callers are outside your deploy, [chapter 08](08_change_rjf9.md)'s rule attaches to it.
- **Observer is the weakest row, and it is worth saying why.** A message bus is not simply an observer with a network in the middle: a broker is genuinely new structure, and the publisher stops holding references to its subscribers, which is a change in the mechanism rather than only in what can fail. Treat the row as a family resemblance rather than the same pattern relocated. The point about failure modes still holds — delivery can be lost or repeated — but the "same shape" claim is looser here than in the rows above.

That distribution is itself informative. **The rows that survive best are the ones where nothing structural is added**, which is a hint about when this reading applies at all.

Observer makes it plainest. Among your own objects, notifying a listener is calling a function: it cannot be lost, cannot arrive twice, cannot arrive out of order. Across a process boundary all three become possible, and every one is a design decision the word "Observer" does not mention.

[Chapter 09](09_what-a-pattern-is-for_3xzc.md) left a question here. **Facade** compresses well and rules nothing out, so what is it doing in a book about load-bearing claims? This is the answer, and "published" is worth making concrete.

```go
// Called only from inside this repository. Nothing here is a promise.
type Orders struct{ ... }

func (o *Orders) Place(ctx context.Context, request PlaceRequest) (Order, error)
func (o *Orders) Cancel(ctx context.Context, orderID string) error
func (o *Orders) resolvePricing(...)   // unexported; nobody outside can call it
```

You can rename `Place`, merge `Cancel` into it, or change what `PlaceRequest` contains with reasonable effort. You just have to fix the call sites in the same commit.

Now imagine the same object reachable by two other teams, over HTTP:

```text
POST /v1/orders          -> Place
DELETE /v1/orders/{id}   -> Cancel
```

Nothing about the Go code changed, and it is worth being exact about what did. `Place` is still your method name — rename it tomorrow, adjust the routing line, and nobody outside notices. What is now in somebody else's source is `POST /v1/orders` and the shape of the JSON it accepts, deployed on a schedule you do not set.

So the line falls between the two, in a place the pattern name never mentioned:

```text
still yours     the method name, its parameters, everything behind it
now theirs      the route, the field names on the wire, which are optional
```

You may add `POST /v1/orders/{id}/hold`. You may not rename the route, remove `DELETE /v1/orders/{id}`, or make a field of the request body required — those are [chapter 08](08_change_rjf9.md)'s forbidden moves, and the client that breaks is one you cannot deploy.

The name of the pattern did not change. What it commits you to did.

### Why these arguments do not converge

Two engineers argue about whether something should be a Facade. One is picturing a class in the same package and hears a suggestion about tidiness. The other is picturing something other teams will call and hears a proposal to publish an interface that can never be narrowed.

Both are reasoning correctly. They agree about the shape, which is all the word conveys, and disagree about who is on the other side, which it does not — so the argument runs on the part they agree about.

What ends it is not a better argument about Facades. It is asking who is on the other side and whether we can change them, which replaces a matter of taste with a question that has an answer.

---

## Why the claim holds

A pattern name describes a **shape**: what calls what, which way the dependencies point, where the indirection sits. Shapes are genuinely independent of context, which is what makes the vocabulary useful at all — the same picture on a whiteboard works whether the boxes are classes or services.

Everything the shape sits *in* varies, and it varies exactly where the pattern's cost is decided. A call inside a process cannot be lost; a call between machines can. A type you own can be renamed this afternoon; a vendor's cannot be renamed at all. A method only your package calls can be deleted; a method other teams call is permanent.

So the name carries the part that transfers and silently drops the part that does not. **It gives you the picture and withholds the constraints, and the constraints were the expensive half.**

**And the axis this chapter turns on is not a new one.** *Can I change the other side* is [chapter 02](02_forces_f4m5.md)'s **control of the callers**, read from the other end: that Force asks whether you can change everyone who calls you, and this chapter asks whether you can change what you call. Same Force, same three settings, pointed the other way.

The other Forces arrive through the failure modes. A message that can be lost is [chapter 02](02_forces_f4m5.md)'s concurrency and [chapter 06](06_distribution_49yh.md)'s distribution; a call that can be slow is the latency budget; a field you can never remove is durability of the medium. So the general statement is:

> A pattern name transfers the **shape** and none of the **Forces**, and the Forces are what decide the cost.

That is [chapter 01](01_the-five-kinds_cjx4.md)'s mechanism in a new place. There, advice arrived stripped of the Forces that made it good advice. Here a shape arrives stripped of the Forces that make it expensive — the same loss, because a shape without its Forces is as unusable as a Principle without its conditions.

---

## Where the claim doesn't apply

### Patterns that stay the same wherever you put them

Some names do not have a version on the other side of the line, and the test is short: **try to state what it would be.** If you cannot, the pattern is a way of arranging code inside one program and the question does not arise.

**Strategy** — passing behaviour as a parameter — is the clearest. In your own code, it's passing a function or class as a parameter. Across a boundary is it… configuration? A plugin? Nothing sharpens, because nothing about passing a function becomes unreliable when the program grows. **Template Method** and most uses of **Decorator** are the same.

**Singleton is the notable exception to this section** — it changes more than anything else in the chapter when it crosses the line.

The invariant is the same on both sides, and stating it precisely is what makes the connection real rather than a play on words:

> **At most one holder of this role at a time, and everyone agrees which one it is.**

In one process, both halves are free. There is one memory space, so a single variable *is* the one instance, and "everyone agrees" is not a question anyone can ask — there is nothing that could disagree.

Across machines the same sentence becomes hard. Note what is *not* being claimed: the cluster obviously has many machines, and nobody is trying to prevent that. The singleton is in the **role**, not the hardware — exactly one machine may be running the nightly billing job, holding the write lease, or acting as primary, while the others stand ready.

Both halves now cost something. "At most one" needs a mechanism that stops a second machine from starting when the first is merely slow — and [chapter 06](06_distribution_49yh.md) shows you cannot tell a slow machine from a dead one, so that mechanism is a lease with a timeout and a guess. "Everyone agrees" is consensus, which [chapter 06](06_distribution_49yh.md) shows cannot be guaranteed to terminate.

So the name survives the crossing and its cost does not. In one process, `sync.Once` and a package variable. Across machines, a consensus protocol, a lease duration nobody is confident about, and a plan for what the old holder does when it wakes up believing it is still in charge.

### Where ownership is partial

The question has two answers in this chapter and three in reality, and the third is where most working code sits.

[Chapter 02](02_forces_f4m5.md) already sets it out: you control every caller; or you can see them but not change them; or you can neither see nor change them. The middle one is an internal service two other teams call. You *can* change both sides — it takes a conversation, a coordinated release, and somebody else's cooperation.

What that does to the pattern question is make the alternatives expensive rather than absent:

```go
// Fully yours: rename it, fix the callers, one commit.
func (o *Orders) Place(...) (Order, error)

// Partial: rename it, and you own the migration.
func (o *Orders) Submit(...) (Order, error)          // the new name
func (o *Orders) Place(...) (Order, error)           // kept, forwarding
// ... until both teams have moved, then delete Place
```

That middle version is not an adapter and not a permanent translation layer. It is a temporary forwarding method with a removal date, and it exists because the change is possible but not unilateral.

Treat the middle case as fully yours and you break people. Treat it as fully theirs and you build versioning ceremony for two callers you could have messaged.

### When a boundary is worth it inside your own code

The chapter argues that a pattern is cheap when both sides are yours. Usually true, and not a rule.

An internal dependency that changes weekly and is called from forty places behaves more like a vendor than like a sibling file: you *can* change it, and doing so is expensive enough that isolating it pays. Ownership is the dominant axis, not the only one — [chapter 04](04_structure_agjy.md)'s fan-in and [chapter 02](02_forces_f4m5.md)'s change-frequency Force both bear on it, and a volatile dependency with many callers earns a boundary on their arithmetic rather than this chapter's.

---

## What the claim costs

**The question is overhead on most naming.** Asked of every noun, it is an obstacle. Asked when someone proposes a pattern as an architectural decision, it is what settles it.

**Anti-Corruption Layers are permanent work.** A translation function, mappings that encode judgements, tests for code that only renames fields, and a person who reads someone else's release notes. That is the correct price for keeping another model out of yours, and it is a price rather than a free consequence of good design.

**Placing the boundary wrongly is expensive in both directions.** Too early and you have a mapping layer over a dependency that was never going to move. Too late and their vocabulary is already in forty files, and adding the boundary means touching all of them.

**Two settings is coarse.** Real systems have degrees of ownership — your team's code, another team's, a library you could fork, a vendor with a support contract, a vendor without. Each behaves a little differently. The chapter compresses them into two because two is enough to catch the error it is about, and the boundary section above says where that breaks.

---

## How to recognize the failure

**In a codebase:**

- **A vendor's type in a signature far from the integration** — their status enum in a reporting query, their error type in domain logic. The spread already happened; the only question left is how many files.
- **A translation layer around a library you could have forked**, where the option was never actually closed.
- **An interface with one implementation, wrapping a type you own** — a pattern solving a problem you could have solved by editing the other file ([Ch. 16](16_tdd-and-mocks_u8eu.md) traces where the reflex comes from).
- **An in-process event bus with retry logic**, where nothing can be lost because nothing leaves the process.
- **A published API that grew by accretion**, because nobody noticed when it stopped being internal and no removal has been possible since.
- **Version numbers on an interface with two callers, both yours.**

**In a conversation:**

- **"We should put an adapter there."** Between what and what — and can we change either one?
- **"It's just a facade."** Called by whom? If the answer includes anyone outside your deploy, it is not just anything.
- **"We use that pattern elsewhere."** With the same answer to the ownership question? The same name on the other side of the line is a different decision.
- **Two people disagreeing about a pattern with rising confidence.** Ask each what is on the other side of it. The disagreement often dissolves, because it was never about the pattern.

The question that does the work: **can I change the other side?**

If yes, you are choosing between options, and following the pattern is rarely the cheapest option. If no, you are not choosing — you are pricing a constraint, and the pattern is what the price looks like.

[Chapter 11](11_patterns-that-survive-translation_us2k.md) works through the patterns that survive translation between languages — the ones describing a real shape rather than a workaround, grouped by the Force each one answers rather than by shape, so you can find a pattern without already knowing its name.

---

## Sources

- Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* — Addison-Wesley, 2003.
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software* — Addison-Wesley, 1994.

---

[← Ch. 09](09_what-a-pattern-is-for_3xzc.md)  ·  [Contents](00_toc.md)  ·  [Ch. 11 →](11_patterns-that-survive-translation_us2k.md)
