# The Scale Test

*Chapter 10 asked whether a pattern name carries information. This one asks what else you need to know before the name is usable — and answers that the received term for it, **scale**, is the wrong word for the thing that matters.*

## The claim

**The same pattern name describes a change you can make in an afternoon and a commitment you will maintain for years. What separates them is not size. It is whether you can change the other side.**

People usually call this a question of scale, and that is close enough to be misleading. Size correlates with the thing that matters, because systems tend to acquire other owners as they grow. But size is not the cause, and reasoning from it gives wrong answers in both directions: a fifty-line integration with a payment provider is a serious commitment, and a ten-thousand-line refactor inside your own repository is not.

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
// package payments — what it hands back
type Receipt struct {
	Ref      string
	Cents    int64
	Complete bool
}

// package billing — what it wants
type LedgerEntry struct {
	Ref   string
	Minor int64
	Final bool
}
```

**Adapter** is the pattern for exactly this: wrap a thing so it fits an interface it was not built for. Here it is:

```go
func adapt(r Receipt) LedgerEntry {
	return LedgerEntry{Ref: r.Ref, Minor: r.Cents, Final: r.Complete}
}
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
func Record(r payments.Receipt) { ... }
```

That is the whole fix: rename two fields and delete the adapter. It is smaller, there is no second representation to drift, and nothing has to be updated when a field is added.

**This is why the pattern is cheap here, and the line count is not the reason.** It is that a third option exists — change the other side — and it is usually better than adapting. The pattern is available and unnecessary.

*(Worth noting how completely this can evaporate. In Go, a type satisfies an interface by having the right methods, with no declaration required, so an adapter that exists only to announce conformance is not written at all. In C# or Java the same requirement produces a wrapper class per type. Chapter 13 takes up names whose content depends on the language that way.)*

### One side theirs: the option disappears

FastSell drops its own payment code and moves to Stripe. Nothing about the shape of the problem has changed — a payment result still has to become a ledger entry — but one thing has:

```go
// Theirs. You cannot edit it, and it changes on their schedule.
type StripeCharge struct {
	ID     string
	Amount int64
	Status string // "succeeded" "pending" "failed" "requires_action" ...
	Cur    string
}
```

You cannot rename `Amount` to `Minor`. You cannot collapse their eleven statuses into the one boolean your ledger has. **The better answer from the previous section is not available**, and adapting is no longer one option among several — it is the only one.

Which turns the question into *where*. Without a boundary, their vocabulary goes wherever it is convenient:

```go
func receipt(c StripeCharge) string   { if c.Status == "succeeded" { ... } }
func ledger(c StripeCharge) int64     { if c.Status == "succeeded" { ... } }
func alert(c StripeCharge) bool       { return c.Status == "failed" }
func refundable(c StripeCharge) bool  { return c.Status == "succeeded" }
func reconcile(c StripeCharge) bool   { return c.Status == "succeeded" || c.Status == "pending" }
```

With one, it stops at the edge and everything behind it speaks FastSell:

```go
func fromStripe(c StripeCharge) LedgerEntry {
	return LedgerEntry{Ref: c.ID, Minor: c.Amount, Final: c.Status == "succeeded"}
}
```

Both versions produce identical output today. The difference shows up when Stripe splits `succeeded` into `succeeded` and `settled`, which they may do without asking:

```text
 sites that test Stripe's vocabulary and must be revisited
   without a boundary   6
   with a boundary      1   (inside fromStripe)
```

Six is small because the example is small; a real integration reaches further. **The boundary converts a change that lands everywhere into a change that lands once** — chapter 05's argument about fan-in, applied to a dependency whose release schedule is not yours.

The pattern literature calls this an **Anti-Corruption Layer**, a name from Eric Evans, where the corruption is another system's model spreading into yours. Note what it costs: a translation function, a set of mappings that encode real judgements, tests for code that does nothing but rename fields, and somebody whose job includes reading Stripe's release notes.

**Same pattern, same shape, both times.** In the first case, three lines that were better deleted. In the second, a file, an owner, and a standing obligation.

### The names, and what crossing the line does to them

| Pattern | Both sides yours | The other side is theirs | What appears when it crosses |
|---|---|---|---|
| **Adapter** | a wrapper, or nothing at all | Anti-Corruption Layer | their model changes without asking (Ch. 09) |
| **Facade** | an object with fewer methods | a service boundary or public API | your surface becomes permanent (Ch. 05, 09) |
| **Observer** | a list of callbacks | a message bus | delivery can fail, or repeat (Ch. 07) |
| **Proxy** | a wrapper adding behaviour | a network hop, with retries and caching | latency floor, partial failure (Ch. 07, 08) |

The last column is what the table is about. Column two is not column one with more code in it. In each row the shape has **acquired a failure mode**, and the failure modes are Part II's Laws arriving one at a time.

Observer makes it plainest. Among your own objects, notifying a listener is calling a function: it cannot be lost, cannot arrive twice, cannot arrive out of order. Across a process boundary all three become possible, and every one is a design decision the word "Observer" does not mention.

Chapter 10 left a question here. **Facade** compresses well and rules nothing out, so what is it doing in a book about load-bearing claims? This is the answer. Among your own classes it is a word for a wrapper. Once other teams call it, it is published — chapter 09's rule applies, you may add to it and never narrow it, and removing a method is a breaking change for people you cannot deploy. The name did not change; what it commits you to did.

### Why these arguments do not converge

Two engineers argue about whether something should be a Facade. One is picturing a class in the same package and hears a suggestion about tidiness. The other is picturing something other teams will call and hears a proposal to publish an interface that can never be narrowed.

Both are reasoning correctly. They agree about the shape, which is all the word conveys, and disagree about who is on the other side, which it does not — so the argument runs on the part they agree about.

What ends it is not a better argument about Facades. It is asking who is on the other side and whether we can change them, which replaces a matter of taste with a question that has an answer.

---

## Why it holds

A pattern name describes a **shape**: what calls what, which way the dependencies point, where the indirection sits. Shapes are genuinely independent of context, which is what makes the vocabulary useful at all — the same picture on a whiteboard works whether the boxes are classes or services.

Everything the shape sits in is not. A call inside a process cannot be lost; a call between machines can. A type you own can be renamed this afternoon; a vendor's cannot be renamed at all. A method only your package calls can be deleted; a method other teams call is permanent.

So the name carries the part that transfers and silently drops the part that does not. **It gives you the picture and withholds the constraints, and the constraints were the expensive half.**

That is chapter 02's mechanism appearing somewhere new. There, advice arrived stripped of the Forces that made it good advice. Here a shape arrives stripped of the Forces that make it costly — the same loss, because a shape without its Forces is exactly as unusable as a Principle without its conditions.

---

## Where this doesn't apply

### Patterns that stay the same wherever you put them

Some names do not have a version on the other side of the line, and the test is short: **try to state what it would be.** If you cannot, the pattern is a way of arranging code inside one program and the question does not arise.

**Strategy** — passing behaviour as a parameter — is the clearest. Between your own functions it is an argument. Across a boundary it is… configuration? A plugin? Nothing sharpens, because nothing about passing a function becomes unreliable when the program grows. **Template Method** and most uses of **Decorator** are the same.

**Singleton does the opposite**, and the contrast is worth having. In one process it means one instance. Across several machines, "exactly one" means one *for the whole cluster*, which is leader election, which needs consensus, which chapter 07 shows cannot be had cheaply or reliably. It does not stay trivial. It becomes one of the hardest things on the list, under an unchanged name.

### Where ownership is partial

The two-sided question is a simplification, and the awkward case is a boundary you half-control.

An internal service used by two other teams in the same company is neither. You *can* change both sides; doing it takes a conversation, a coordinated release, and someone else's cooperation. The alternatives did not disappear — they became expensive.

That is the ordinary condition of most large codebases, and the honest answer is a third setting: *changeable, but not unilaterally*. Treat it as fully yours and you break people. Treat it as fully theirs and you build versioning ceremony for two callers you could have messaged.

### When a boundary is worth it inside your own code

The chapter argues that a pattern is cheap when both sides are yours. Usually true, and not a rule.

An internal dependency that changes weekly and is called from forty places behaves more like a vendor than like a sibling file: you *can* change it, and doing so is expensive enough that isolating it pays. Ownership is the dominant axis, not the only one — chapter 05's fan-in and chapter 03's change-frequency Force both bear on it, and a volatile dependency with many callers earns a boundary on their arithmetic rather than this chapter's.

---

## What it costs

**The question is overhead on most naming.** Asked of every noun, it is an obstacle. Asked when someone proposes a pattern as an architectural decision, it is what settles it.

**Anti-Corruption Layers are permanent work.** A translation function, mappings that encode judgements, tests for code that only renames fields, and a person who reads someone else's release notes. That is the correct price for keeping another model out of yours, and it is a price rather than a free consequence of good design.

**Placing the boundary wrongly is expensive in both directions.** Too early and you have a mapping layer over a dependency that was never going to move. Too late and their vocabulary is already in forty files, and adding the boundary means touching all of them.

**Two settings is coarse.** Real systems have degrees of ownership — your team's code, another team's, a library you could fork, a vendor with a support contract, a vendor without. Each behaves a little differently. The chapter compresses them into two because two is enough to catch the error it is about, and the boundary section above says where that breaks.

---

## How to recognize the failure

**In a codebase:**

- **A vendor's type in a signature far from the integration** — their status enum in a reporting query, their error type in domain logic. The spread already happened; the only question left is how many files.
- **A translation layer around a library you could have forked**, where the option was never actually closed.
- **An interface with one implementation, wrapping a type you own** — a pattern solving a problem you could have solved by editing the other file (Ch. 17 traces where the reflex comes from).
- **An in-process event bus with retry logic**, where nothing can be lost because nothing leaves the process.
- **A published API that grew by accretion**, because nobody noticed when it stopped being internal and no removal has been possible since.
- **Version numbers on an interface with two callers, both yours.**

**In a conversation:**

- **"We should put an adapter there."** Between what and what — and can we change either one?
- **"It's just a facade."** Called by whom? If the answer includes anyone outside your deploy, it is not just anything.
- **"We use that pattern elsewhere."** With the same answer to the ownership question? The same name on the other side of the line is a different decision.
- **Two people disagreeing about a pattern with rising confidence.** Ask each what is on the other side of it. The disagreement often dissolves, because it was never about the pattern.

The question that does the work: **can I change the other side?**

If yes, you are choosing between options and this one is rarely the cheapest. If no, you are not choosing — you are pricing a constraint, and the pattern is what the price looks like.

---

**Next:** chapter 12 works through the patterns that survive translation between languages — the ones describing a real shape rather than a workaround, grouped by what they are about, each with the Force that makes it worth its cost.
