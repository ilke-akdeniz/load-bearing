# The Scale Test

*Chapter 10 asked whether a pattern name carries information. This one asks a question the name cannot answer by itself: **at what size**. The same word describes a five-line convenience and a permanent translation layer with a maintenance budget, and nothing in the word distinguishes them.*

## The claim

**A pattern name tells you the shape. It does not tell you the scale, and the scale decides whether the shape costs you nothing or commits you to something you will maintain for years.**

The axis that matters is not how much code is involved. It is whether **you can change the other side**. When both sides are yours, a pattern is one fix among several and usually not the best one. When the other side belongs to someone else, most of the alternatives disappear and the pattern becomes the only move — at which point it stops being a shape and starts being an architectural commitment.

## What "scale" means here

Two scales, and the boundary between them is ownership rather than size.

**Class scale** — both sides are yours. Same repository, same deploy, same team. If two things do not fit together, you can change either one.

**System scale** — one side is not yours to change. A vendor's API, another team's service, a published format, a database somebody else's jobs also write to. You can adapt to it; you cannot edit it.

A "class-scale" pattern can involve thousands of lines and a "system-scale" one can be a fifty-line file. The size is not what changes the answer. **What changes is how many of your options survive**, and that is settled by chapter 03's control-of-the-callers Force and chapter 09's blunter version: you cannot deploy other people's software.

[claude this is a confusing intro that needs clarifications and simplification. It reads like this:
"size matters, five line convenience ..." => "Ok size of involved code is important I guess"
"the scale, scale decides" => "Oh it's not size of code but scale. What scale? Should be the load on system right?"
"is not how much code is involved. It is whether **you can change the other side**." => "Ok not size, not scale but wath matters is if you are on an integration point."
"two scales: class - system" => "Ok not integration point but the size of the component matters."
"the size is not what changes the answer" => "Does the author even know what his point is!?" ]

---

## The demonstration

### Adapter at class scale, where it can vanish entirely

**Adapter** is the pattern of wrapping something so it fits an interface it was not built for.

Here is a real case. FlowCore needs its storage helpers to work against either a connection pool or an open transaction. Those are two different types from a third-party library, and neither knows anything about FlowCore: [claude we used this ecact examples many times already for other claims, time to find something else. Also could be better to cover a simple coherent example in all this chapter as it will demonstrate the points better. So maybe something like: We own "fastSell" app and we have our own payment processor implementation ... Then we switch to stripe and ...  ]

```go
// The interface, declared where it is used — three methods, because
// that is all the calling code needs.
type querier interface {
	Exec(sql string) (int, error)
	Query(sql string) ([]int, error)
}

var a querier = VendorPool{} // no adapter, no registration
var b querier = VendorTx{}
```

```text
pool: 1  tx: 2  — both satisfy querier with zero wrapper code
```

Both types satisfy the interface because their method signatures happen to match. Go checks structurally: a type implements an interface if it has the methods, and nobody has to declare the relationship. So the Adapter here is **four lines of interface and no adapter at all.**

In a language where implementation is declared rather than inferred — C#, Java — the same requirement produces wrapper classes:

```csharp
class PoolQuerier : IQuerier {
    private readonly NpgsqlDataSource _source;
    public Task<int> ExecAsync(string sql) => /* forward */;
    public Task<int[]> QueryAsync(string sql) => /* forward */;
}

class TxQuerier : IQuerier { /* the same two methods again */ }
```

```text
 Go     4 lines of interface, 0 per type
 C#     4 lines of interface, 1 class + 2 forwarding methods per type,
        plus wrapping at every call site
```

**That is Adapter at class scale**: in one language it is real but trivial, and in another it does not exist as a thing you write. A name whose entire content evaporates when you change language is a name carrying very little — which is chapter 13's test, arriving early.

### The third option, which is what actually makes it trivial

The deeper reason Adapter is cheap here is not the line count. It is that **a third option exists.**

If two of your own types do not fit, you can wrap one — or you can change one so no wrapper is needed. Rename the method. Change the signature. Move the parameter. All of those are available because both files are yours, and most of the time one of them is simpler than an adapter. [claude when you describe an important point in an existing code example, it's better to show it with the code example rather than stating it. How would that simple than an adapter arrangement look in the code?]

That option is what disappears next.

### Adapter at system scale, where the option is gone

Now the thing on the other side is a payment provider. Their model has eleven status values, their own money representation, and their own vocabulary:

```go
// Theirs. You cannot edit it, and it changes on their release schedule.
type StripeCharge struct {
	Status string // "succeeded" "pending" "failed" "requires_action" ...
	Amount int64
	Cur    string
}
```

You cannot rename their field. You cannot reduce their eleven statuses to the three your business has. The only remaining move is to translate — and once translation is the only move, the question becomes **where** it happens.

Without a boundary, their vocabulary spreads to wherever it is convenient:

```go
func receiptDirect(c StripeCharge) string { if c.Status == "succeeded" { return "paid" }; ... }
func ledgerDirect(c StripeCharge) int64   { if c.Status == "succeeded" { return c.Amount }; ... }
func alertDirect(c StripeCharge) bool     { return c.Status == "failed" }
```

With one, it stops at the edge:

```go
func fromStripe(c StripeCharge) Payment {
	return Payment{Settled: c.Status == "succeeded", Minor: c.Amount, Cur: c.Cur}
}
```

Both versions work. The difference appears when the provider splits `succeeded` into `succeeded` and `settled`, which they are entitled to do without asking:

```text
 without a boundary   3 call sites test their vocabulary and must change
 with one             1 place changes, and it is the translation function
```

Three is a small number because this is a small example. The number is the point rather than its size: **the boundary converts a change that lands everywhere into a change that lands once**, which is chapter 05's argument about fan-in, applied to a dependency you do not control.

This is what the pattern literature calls an **Anti-Corruption Layer** — the name is Eric Evans's, and the "corruption" is another system's model leaking into yours. Note what it now commits you to. Somebody maintains that translation. Somebody notices when the provider adds a status and decides what it maps to. There is a test suite for a function that does nothing but rename fields, and it earns its keep.

**Same name, both times.** At class scale, four lines and possibly zero. At system scale, a file, an owner, a test suite, and a standing obligation to track someone else's release notes.

### The table, and what it is really tracking

| Name | Class scale | System scale | What appears at system scale |
|---|---|---|---|
| **Adapter** | a wrapper, or nothing at all | Anti-Corruption Layer | their model changes without asking (Ch. 09) |
| **Facade** | an object with fewer methods | a service boundary or public API | your surface becomes a commitment (Ch. 05, 09) |
| **Observer** | a list of callbacks | a message bus | delivery can fail, and repeat (Ch. 07) |
| **Proxy** | a wrapper adding behaviour | a network hop with retries and caching | latency floor, partial failure (Ch. 07, 08) |

Read the last column, because it is what the table is actually about. The pattern names in column one are shapes. The same shapes in column two have **acquired failure modes**, and the failure modes are the Laws of Part II arriving one at a time.

That is why the scale changes the answer so completely. At class scale, Observer is a slice of functions and calling them is calling them. At system scale, the observers are in other processes, so a notification can be lost, arrive twice, or arrive out of order — and every one of those is a design decision the word "Observer" does not mention.

Chapter 10 left a question here: **Facade** compresses well and rules nothing out, so what is it doing in a book about load-bearing claims? This is the answer. At class scale, nothing — it is a word for a wrapper. At system scale the facade is the thing other teams call, which means it is published, which means chapter 09's rule applies and you may add but never remove. The name did not change. The commitment did.

### Why pattern arguments do not converge

Two engineers argue about whether something "should be a Facade." One is thinking of a class in the same package and hears a suggestion about tidiness. The other is thinking of a service other teams will call and hears a proposal to publish an interface that can never be narrowed.

Both are reasoning correctly. They are answering different questions, and nothing in the word marks which one is on the table — so the argument runs on the shape, which they agree about, while the disagreement is entirely about the scale, which neither has stated.

The move that ends it is not a better argument about Facades. It is asking **who is on the other side, and can we change them** — which converts a pattern argument into a question with an answer.

---

## Why it holds

A pattern name describes a **shape**: what calls what, which way the dependencies point, where the indirection sits. Shapes are scale-free, which is what makes the vocabulary useful at all — it is the same picture on a whiteboard whether the boxes are classes or services.

What is not scale-free is everything the shape sits in. A call within a process cannot be lost; a call between processes can. A type you own can be changed; a vendor's cannot. A method your own package calls can be renamed this afternoon; a method other teams call cannot be renamed at all.

So the name carries the part that does not vary and omits the part that does. It transfers a picture and drops the constraints, and the constraints were the expensive half.

**This is chapter 02's mechanism in a new place.** There, advice arrived stripped of the Forces that made it good advice. Here, a shape arrives stripped of the Forces that make it costly — and it is the same loss, because a shape without its Forces is exactly as unusable as a Principle without its conditions.

---

## Where this doesn't apply

### Patterns that are trivial at every scale

Some names have no system-scale form at all, and the test is short: **try to state what the system-scale version would be.** If you cannot, the pattern is a code-organization device and the scale question does not arise.

**Strategy** — passing behaviour as a parameter. At class scale, a function argument. At system scale it is… configuration? A plugin? Nothing sharpens. No new failure mode appears, because nothing about passing a function becomes unreliable when the program gets bigger. The same goes for **Template Method** and, in most uses, **Decorator**.

These are patterns about arranging code inside one process, and they stay what they are. Chapter 13 takes the further step of asking whether they are patterns at all once the language has first-class functions.

**Contrast that with Singleton**, which does the opposite and is worth knowing about. At class scale it is one instance in one process. At system scale "exactly one" means one across a cluster, which is leader election, which needs consensus, which chapter 07 shows cannot be had cheaply. Singleton does not stay trivial; it becomes one of the hardest things in the list, under the same name.

### Where the scale is genuinely ambiguous

The two-scale split is a simplification, and the messy case is a boundary you own today and might not tomorrow.

An internal service consumed by two teams inside one company is neither class scale nor system scale. You *can* change both sides, and doing so requires a conversation, a coordinated deploy, and somebody's cooperation. The alternatives have not disappeared; they have become expensive.

That is the ordinary state of most large codebases, and the honest answer is that the scale question has a third setting: *can change it, but not unilaterally*. Treating that as class scale produces breakage; treating it as system scale produces versioning ceremony for two callers you could have emailed.

### When the pattern is load-bearing at class scale too

The chapter argues that class-scale patterns are cheap, which is usually true and not a rule.

A class-scale Adapter that isolates a fast-moving internal dependency can be worth exactly what an Anti-Corruption Layer is worth, if the thing behind it is churning and many places call it. The ownership axis is the dominant one, not the only one — chapter 05's fan-in and chapter 03's change-frequency Force both bear on it, and a volatile internal dependency with forty callers behaves more like a vendor than like a sibling file.

---

## What it costs

**Asking the scale question takes time that most naming does not deserve.** Applied to every noun, it is an obstacle. Applied when someone proposes a pattern as an architectural decision, it is the question that resolves it.

**Anti-Corruption Layers are real, permanent work.** A translation function, a set of mappings that encode judgements, tests for a function whose only job is renaming, and a person who reads the vendor's release notes. That is the correct price for keeping someone else's model out of yours, and it is a price — not a free consequence of good design.

**Choosing the boundary wrongly is expensive in both directions.** Translate too early and you have a mapping layer over a dependency that was never going to change. Translate too late and their vocabulary is already in forty files, and putting the boundary in afterwards means touching all of them.

**The two-scale model is coarse.** Real systems have shades of ownership: your team's code, your company's other team's code, an open-source library you could fork, a vendor you have a support contract with, a vendor you do not. Each behaves slightly differently, and this chapter compresses them into two buckets because two buckets are enough to catch the error the chapter is about.

---

## How to recognize the failure

**In a codebase:**

- **A vendor's type appearing in a function signature far from the integration** — their status enum in a reporting query, their error type in your domain logic. The corruption already happened; the question now is how many files.
- **An Anti-Corruption Layer around a library you could have forked**, where the alternative was never actually closed off.
- **An interface with one implementation, wrapping a type you own**, which is a class-scale adapter solving a problem you could have solved by changing the other file (Ch. 17 traces where this reflex comes from).
- **An in-process event bus with retry logic**, where nothing can be lost because nothing leaves the process — system-scale machinery on a class-scale problem.
- **A published API that grew by accretion** because nobody noticed it had crossed from class scale to system scale, and no removal has ever been possible since.
- **Version numbers on an internal interface with two callers, both yours.**

**In a conversation:**

- **"We should put an adapter there."** Between what and what, and can we change either one?
- **"It's just a facade."** Called by whom? If the answer includes anyone outside the deploy, it is not just anything.
- **"We already use that pattern elsewhere."** At the same scale? The same name at a different scale is a different decision.
- **Two people disagreeing about a pattern with increasing confidence.** Ask each what is on the other side of it. Very often the disagreement dissolves, because it was never about the pattern.

The question that does the work: **can I change the other side?**

If yes, the pattern is one option among several, and usually not the cheapest. If no, most of the alternatives were never available, and what looks like a design choice is the acknowledgment of a constraint.

---

**Next:** chapter 12 works through the patterns that survive translation between languages — the ones that describe a real shape rather than a workaround, grouped by what they are about and each with the Force that makes it worth its cost.
