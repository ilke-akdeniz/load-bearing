# The Five Kinds of Claim

**Many claims you meet about software are one of five kinds: Law, Force, Principle, Idiom, Style. And the kind of a claim determines how much authority it has** — not the confidence of the person saying it, not their track record, not how widely it is repeated.

Four of them are advice, and form a ladder of authority:

> **Law → Principle → Idiom → Style**

The fifth, Force, is not advice at all. It is the input that decides where on that ladder you should be standing.

So the count is not five of one thing. **There are four levels and five kinds** — the levels are rungs on the ladder, and Force is the fifth kind precisely because it is not on it. That distinction matters more than it first appears, and the rest of the chapter turns on it.

## Law

True by the mechanics of computation. Violating one produces a **wrong program**, and the wrongness does not depend on your language, your team, or your taste.

*Exactly-once delivery is impossible.* You can arrange for a message to arrive at least once, or at most once, and there is no third option — not in a better language, not with a larger budget, because the sender cannot find out whether a message it got no answer to was received.

You do not get to disagree with a Law. You only get to be in a situation where its preconditions are absent — which is a different thing, and the subject of *How Forces relate to each kind of advice*, below.

## Force

A **property of your situation**: is there concurrency, does the data outlive the code, how large is the blast radius of a bug, do you control the callers, how often does this change.

*This table will outlive three rewrites of the code that reads it.* That is not advice and you cannot disagree with it. It is either true where you are or it is not, and it decides whether a rule about the data belongs in the application or in the schema.

Forces are not recommendations, and they are not negotiable by argument. They are facts about where you are standing. ([Chapter 02](02_forces_f4m5.md) is entirely about them.)

A Force is read before any pattern or technique is in view because that's the groundwork to decide whether a Law binds and whether a Principle inverts.

## Principle

Advice that is **good given certain Forces** and stops being good — sometimes reverses outright — when those Forces change.

*Don't repeat yourself.* Sound where the two copies really are one idea, and actively harmful where they only look alike — deduplicating them couples two things that were free to change separately, and the next change to one breaks the other.

The mark of a Principle is that it has conditions. A Principle stated without its conditions has been promoted, usually by accident, and that promotion is the failure this book exists to catch.

## Idiom

An **ecosystem convention**. Locally correct, non-transferable, and usually traceable to a language feature that is present or absent.

*Accept interfaces, return structs.* Good advice in Go and close to meaningless in Python, which has no compile-time interface to accept. Nothing about the problem changed on the way across; the language did.

An Idiom is not arbitrary — there is normally a real reason it grew where it did. But the reason is local, so the conclusion is local.

**What separates an Idiom from a Style is mechanical: the compiler or the runtime acts on an Idiom, and ignores a Style.** The visible behaviour of the software does not change because of an Idiom. *Visible behaviour* means what the program produces when it succeeds. That is a narrow definition on purpose, and it leaves out a great deal: failure modes, developer experience, maintainability.

Dependency injection shows how the compiler and the runtime can act on an Idiom. Wired by hand, the dependencies are constructor arguments, so getting one wrong is a type error and the program does not build. Through a container they are resolved at run time from a registration list, so the same mistake compiles and surfaces on the first request that needs the missing service.

## Style

Naming, formatting, file layout. **Arbitrary, but worth being consistent about.**

*Tabs or spaces.* The compiler cannot tell, the runtime cannot tell, and the program is the same program either way — which is why the argument has run for forty years without either side producing evidence.

Neither the compiler nor the runtime can tell which way you chose. Style has no authority at all, and the correct response to a Style argument is to pick one and stop discussing it.

---

## How Forces relate to each kind of advice

**A Force never makes a Law false.** Laws are true unconditionally. What a Force decides is whether a Law **has anything to act on** — whether it binds in your situation or sits inert.

Amdahl's Law bounds how much faster a program can get from more processors, given the fraction of it that cannot be split. It is true of a single-threaded script and has nothing to constrain there, because there is no parallel portion to bound ([Ch. 07](07_scale_637f.md) works the arithmetic).

**A Force can make a Principle wrong.** This is a stronger relationship. Principles do not merely go quiet when their conditions vanish; they can invert, so that following them produces worse software than ignoring them.

| Kind | What a Force changes |
|---|---|
| **Law** | whether it **binds** — true either way, sometimes inert |
| **Principle** | whether it is **right or wrong** — can reverse |
| **Idiom** | nothing; the ecosystem decides |
| **Style** | nothing; nothing decides |

So both Laws and Principles are Force-sensitive, in different ways. **A Law can be irrelevant but never wrong. A Principle can be wrong.**

Getting this backwards produces two recognizable errors:

- Treating an inert Law as a live constraint — building locking machinery for a program with one writer.
- Treating an inverted Principle as still binding — "we must not duplicate this" in a case where the duplication was the right call.

---

## The demonstration

Three pieces of code: a Law violation, an Idiom difference, and a Force rendering a Law inert.

### A Law violation: wrong in every language

```go
func Reserve(ctx context.Context, db *pgxpool.Pool, seatID string) error {
	var taken bool
	err := db.QueryRow(ctx, `select taken from seat where id = $1`, seatID).Scan(&taken)
	if err != nil {
		return err
	}

	if taken {
		return ErrSeatTaken
	}

	_, err = db.Exec(ctx, `update seat set taken = true where id = $1`, seatID)

	return err
}
```

Two customers click Book at the same moment:

```text
customer A: select → taken = false
customer B: select → taken = false      ← B read before A wrote
customer A: update → ok
customer B: update → ok
result: one seat, two tickets
```

Now translate it. C# with EF Core, Python with SQLAlchemy, Java with Hibernate, Rust with sqlx — **the bug survives every translation**, because it is not about the language. No reviewer's preference changes the outcome. No team convention makes it correct.

That is what a Law violation looks like: the program is wrong, and the wrongness is mechanical.

*(The Law being broken is check-then-act, which [chapter 05](05_time_mdbn.md) owns.)*

### An Idiom difference: same shape, opposite reception

```go
// Go — completely ordinary. Nobody comments on this in review.
func main() {
	pool, _ := pgxpool.New(context.Background(), os.Getenv("DATABASE_URL"))
	catalog := NewCatalog(pool)
	engine := NewEngine(pool)

	mux := http.NewServeMux()
	mux.Handle("/approve", approveHandler(engine, catalog))
	http.ListenAndServe(":8080", mux)
}
```

```csharp
// C# — the same shape. This gets flagged in review.
public class ApproveController : ControllerBase {
    private static readonly WorkflowCatalog Catalog =
        new(NpgsqlDataSource.Create(Environment.GetEnvironmentVariable("DATABASE_URL")!));

    [HttpPost]
    public async Task<IActionResult> Approve(Guid id) { /* uses Catalog */ }
}
```

The C# version **works**. It compiles, it runs, it serves requests correctly, it is thread-safe. It will still be sent back, because the ecosystem expects registration with the container and constructor injection.

Two facts sit side by side:

- The Go version is normal and the C# version is not.
- Neither is more *correct* than the other.

That is the signature of an Idiom. The rule is real, it is worth following, and it is **about the ecosystem rather than about the program**.

### A Force rendering a Law inert

Take the seat-reservation code again, unchanged, and put it somewhere else:

```go
// A one-off CLI tool. One process, one goroutine — Go's lightweight
// thread — run by one operator, on a database nothing else is touching.
func main() {
	if err := Reserve(ctx, db, os.Args[1]); err != nil {
		log.Fatal(err)
	}
}
```

Identical code. Now it is correct.

Be precise about why, because the sloppy version of this claim is where the model goes wrong.

**The Law did not bend.** Check-then-act is still not atomic — that remains true of this code, on this line, right now. What changed is that the Law's precondition is absent: non-atomicity only produces a wrong program when a second writer can interleave, and here there isn't one.

The Law is true and inert. The code is correct — not "correct despite breaking a rule."

This is why Force is its own kind rather than a footnote to Principle: **the same Law is decisive in one situation and silent in another, and only the Forces tell you which situation you are in.**

---

## The classification test

Five questions, in order. Stop at the first that answers.

**1. Is this a statement about my situation rather than a recommendation?** → **Force**. "Requests are handled concurrently." "This schema will outlive three rewrites." "We do not control the callers." These masquerade as advice surprisingly often, and mistaking one for advice is how arguments become unresolvable.

**2. When its preconditions hold, does violating it produce a wrong program — in any language, on any team?** → **Law**. The test is mechanical consequence, not severity: a slow program is not a wrong one. The clause about preconditions is doing real work; without it you will misclassify every Law that happens to be inert where you are standing.

**3. Can it become *wrong* advice if circumstances change?** → **Principle**. Follow-up worth asking every time: can I state those circumstances? If not, I do not yet understand the advice well enough to apply it.

**4. Does the compiler or the runtime act on the choice, while the program behaves the same either way?** → **Idiom**. It will usually also be specific to a language or ecosystem, and competent engineers elsewhere will often do the opposite — but that is a consequence of the answer rather than the test, because plenty of Style is local too.

**5. Does neither of them act on the choice?** → **Style**.

---

## Twenty-one claims, classified

| Claim | Kind | Note |
|---|---|---|
| "Exactly-once delivery is impossible" | **Law** | proven; [Ch. 06](06_distribution_49yh.md) |
| "Dependencies must be acyclic" | **Law** | near-tautology; [Ch. 04](04_structure_agjy.md) |
| "Check-then-act is not atomic" | **Law** | [Ch. 05](05_time_mdbn.md) |
| "A cache needs an invalidation strategy" | **Law** | without one it is a copy that goes wrong |
| "Requests are served concurrently" | **Force** | a fact wearing advice's clothing |
| "The schema outlives the code" | **Force** | decides where invariants belong |
| "We don't control our callers" | **Force** | the whole reason library design differs |
| "Prefer composition over inheritance" | **Principle** | conditions: variation on multiple axes |
| "Don't repeat yourself" | **Principle** | famously over-applied; duplication beats wrong coupling |
| "Validate input at the boundary" | **Principle** | behaves like a Law under an adversarial Force |
| "Functions should be short" | **Principle** | Force: working-memory limits |
| "Push invariants to the layer that can enforce them" | **Principle** | conditions: a layer that *can* |
| "Premature optimization is the root of all evil" | **Principle** | routinely quoted with Knuth's conditions removed |
| "Use dependency injection" | **Principle** | the technique |
| "Use a DI container" | **Idiom** | the tooling — a different kind of claim entirely |
| "Every repository gets an interface" | **Idiom** | C#/Java; [Ch. 16](16_tdd-and-mocks_u8eu.md) for why |
| "Accept interfaces, return structs" | **Idiom** | Go |
| "Exceptions are for exceptional cases" | **Idiom** | Go and Python disagree at the root |
| "Short local names" | **Style** | Go-specific, and still Style — nothing sees it; [Ch. 21](21_style_9rng.md) |
| "Prefer `var` / avoid `var`" | **Style** | pick one, stop talking |
| "Tabs vs spaces" | **Style** | genuinely arbitrary |

One row is worth pausing on.

**"Use dependency injection" and "use a DI container" are different claims of different kinds.** They get said in the same breath, and the Idiom is routinely defended with the Principle's arguments. Separating them dissolves most of the argument.

(The "validate input" row is the one claim in the table whose kind depends on the situation. The next section but one explains why.)

---

## Why the kinds get confused

Four mechanisms, none of them anyone's fault in particular.

**Tone does not vary with authority.** Confidence is a personality trait and a rhetorical choice. Someone stating a proven theorem and someone stating a formatting preference can sound identical — and frequently the formatting preference sounds *more* certain, because there is less to qualify.

**Advocacy compresses.** "Always do X" travels further than "do X when Y, unless Z." The conditions are the first thing lost, and they were the content. [Chapter 14](14_principle-loses-scope_b86v.md) traces this mechanism in detail.

**Monoculture makes Idioms look like physics.** If you have only worked in one ecosystem, its conventions are indistinguishable from necessity. You have never seen the counter-example, so you conclude there isn't one. This is the single most common source of confusion here, and the only reliable cure is working in a second ecosystem long enough to be fluent — long enough that its conventions stop feeling wrong and start feeling like conventions.

**Teaching leaves the training wheels on.** Beginners are given rules, because rules are teachable and judgement is not. "Never use global state." "Always write a test first." Nobody comes back later to say which parts were scaffolding.

---

## Where the model breaks down

Five boundaries, and the last is the important one.

**Claims that genuinely span kinds.** "Validate at the boundary" is partly a security Law, partly a feedback-speed Principle, partly an Idiom about *which* boundary. Forcing a single label loses information. Hold two labels and say which part you mean.

**A Principle whose Force cannot be read has to be followed as though it were a Law.** *Validate input at the boundary* is conditional in form: what would settle it is whether hostile input arrives. For most Principles you read the Force and act. Here you cannot, because there is no instrument for *is somebody trying* — and a question with no instrument is a risk rather than a Force ([Ch. 02](02_forces_f4m5.md)).

It is worse than merely unmeasured. An attacker is not sampling from your expected inputs; they are searching for the one that breaks you. So the frequency you would need in order to judge is the very thing being manipulated, and a reading taken today says nothing about tomorrow.

The classification is not wrong. *Validate at the boundary* really is a Principle, and there really are programs nothing hostile ever reaches. The classification is simply no use, because you cannot find out which program you have — and where the reading is unavailable and the cost of being wrong is unbounded, the only safe move is to drop the conditionality and treat it as absolute. That is the model failing in the most instructive way it can: correctly, and to no benefit.

**Arguing about the classification is itself the failure.** The model is a thinking aid, not a taxonomy to litigate. Two people debating whether something is a Principle or an Idiom have already extracted the value — they have agreed it is not a Law — and everything after that is the sort of dispute this book exists to end, not to relocate.

**Classifying is not deciding.** The model tells you what kind of claim you are holding. It does not tell you what to do about it. Recognizing something as an Idiom is not permission to ignore it — [chapter 20](20_idioms_7nkn.md) argues that following local convention is usually correct even when you can out-argue it, because reviewability and shared expectations are worth more than being interesting. The model narrows the question; it does not answer it.

**The model needs comparative experience it cannot supply.** This is the real limit, and it is uncomfortable.

Running the test requires having seen the alternative. Question 2 — *does violating it produce a wrong program in any language, on any team?* — is unanswerable if you have only ever worked in one ecosystem. You will classify its conventions as Laws, not out of carelessness but because you have no counter-example available, and a rule with no visible exception is indistinguishable from a rule with none.

The trap is that a single-stack shop is where this failure does the **most** damage and is **hardest** to detect. Nobody arrives with a contradicting habit. Conventions accumulate for reasons that stop applying, and nothing in the environment surfaces that. "We've always done it this way" is not evidence of anything, and in a uniform context it is the only evidence available.

So the honest version is not "in a monoculture you can skip this." It is: **in a monoculture you need this most and can execute it least.** The remedy is not analysis — you cannot reason your way to a counter-example you have never seen. It is deliberately acquiring contrast: reading the *source* of well-regarded projects in another ecosystem, not their blog posts; writing something small in a language whose defaults offend you; asking what a competent person who disagreed with your team would say.

Until then, follow the local convention — not because it is a good proxy for correctness, but because you do not yet have the standing to overrule it, and being idiosyncratic is worse than being conventionally wrong.

---

## What the model costs

**Analysis where a default would do.** Most decisions are small and the conventional answer is fine. Running a five-question test on a variable name is worse than picking a name.

**A licence to dismiss.** "That's just an Idiom" is available as a way to wave off any advice you dislike. The defence: a classification must come with its *mechanism*, not just its label. If you cannot say why something is an Idiom — which language feature it grew from, what the other ecosystem does instead — you have not classified it, you have dismissed it.

**Vocabulary nobody shares.** "That's an Idiom, not a Law" means little to colleagues who haven't read this. The model is for your own thinking; in conversation, say the content: *"that's a C# convention, and the reason it exists doesn't hold here."*

**False precision.** Five neat kinds imply the world has five neat kinds. It does not. The model is a sorting aid whose value is mostly in separating Law from Idiom — the finer distinctions matter far less than that one.

---

## How to recognize the failure

**In a codebase:**

- Interfaces with exactly one implementation and no plausible second one — an Idiom followed where the Principle behind it does not reach ([Ch. 17](17_abstraction-as-insurance_4jk6.md)).
- Layer directories where every feature change touches all of them.
- A style guide with correctness rules mixed into formatting rules, at the same emphasis.
- Defensive code guarding a condition the surrounding architecture makes impossible — an inert Law treated as live.
- A design document that cites an authority rather than a mechanism.

**In a conversation:**

- "That's not best practice," offered as a complete argument.
- "We always do it this way here," with no memory of why.
- Someone unable to answer *when would this rule be wrong?* — not because the answer is "never," but because the question has never come up.
- Two people making increasingly detailed arguments while disagreeing about a Force neither has stated.

That last one is the most expensive and the easiest to fix. When an architecture argument will not converge, stop arguing about the Principle and ask what each side believes about the situation. The disagreement is usually not about the advice at all, but about the situation both sides are applying it to.

---

## What this chapter assumed

Five kinds and their authority are assumed and not proven in this chapter. That is worth saying now, because every other chapter makes a claim and then demonstrates it. That the kind determines authority is true by construction, since the kinds are *defined* by their authority — there is nothing left to show.

[Chapter 02](02_forces_f4m5.md) takes Forces seriously — the properties of a situation that decide which Laws bind and which Principles hold, and why naming one is not the same act as evaluating it.

---

[← Introduction](README.md)  ·  [Contents](00_toc.md)  ·  [Ch. 02 →](02_forces_f4m5.md)
