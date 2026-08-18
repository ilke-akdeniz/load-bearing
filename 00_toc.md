# Load-Bearing — Table of Contents

Twenty-three chapters in five parts.
Each entry states what the chapter argues, what it covers, and — per the book's own rule — where its claim stops.

Back to [README](README.md).

---

## Part I — Claims and Forces

### 01. Why good advice goes wrong
`01_why-good-advice-goes-wrong.md`

Two teams receive the same advice and get opposite outcomes.
The book's thesis, stated plainly: the problem is rarely that advice is wrong, it's that advice arrives without its conditions attached.

Contents: the anatomy of a misapplication; why "it depends" is an unsatisfying answer that happens to be correct; what this book gives you instead of a checklist.

*Where the claim doesn't apply:* some advice really is unconditional, and treating everything as contextual is its own failure mode.

### 02. The five kinds of claim
`02_the-five-kinds.md`

The book's premise, made precise, with a classification test you can run on any claim in under a minute.

Contents: the five kinds, named rather than numbered — four of them advice, forming a ladder of authority, and Force outside it, which is why there are four levels and five kinds; how Forces relate differently to Laws and to Principles — a Law can be inert but never wrong, a Principle can be wrong; the five-question classification test; twenty common claims classified; why the kinds get confused.

*Where the model breaks down:* claims that genuinely span two kinds, and why forcing one label is worse than holding both; and the fact that this chapter offers a lens rather than a claim it can demonstrate.

### 03. Forces: the inputs nobody names
`03_forces.md`

Forces, and the most underrated chapter in the book.

The claim: **evaluating the Forces acting on your situation is the groundwork** — a prerequisite, explicitly not sufficient.
Naming a Force is the cheap half and is not the same act: "we have concurrency" becomes a distributed lock in a program with one writer, and the chapter's cost section is about exactly that.

Contents: a Force is a dial rather than a switch, so the design changes several times across its range; then the seven — concurrency; durability of the medium (a schema outlives the code that writes it); blast radius of a bug; change frequency and its shape; team size and turnover; latency budget; whether you control the callers.
Each Force with a code demo of the same problem solved differently under different values of it, and the seven restated as questions.

*Where the claim doesn't apply:* Forces you cannot measure yet, where the reversibility rule decides whether to defer; a Force that is present and has no design consequence; and things that are risk rather than unmeasured Force, which have no instrument and so cannot be deferred *to*.

## Part II — The foundations

### 04. Three kinds of true
`04_grading-a-law.md`

Not every Law has the same standing.
Theorem, definition, and empirical law are three different kinds of true, and each admits exactly one move.

Contents: what makes Two Generals a different kind of claim from Conway's Law; what makes Conway's Law different from "prefer composition over inheritance"; the halting problem as a theorem whose folk version dropped a quantifier; how to check a claimed Law.

*Where the claim doesn't apply:* kind is not importance, so a theorem can be irrelevant at your scale — Amdahl on a single-threaded CLI — while an empirical number decides your architecture; one name covering both a theorem and a slogan; and claims that sit between kinds, where forcing one label loses the argument.

### 05. Structure: dependency and hiding
`05_structure.md`

The Direction Rule and its family.

Contents: acyclic dependency, and why it's a Law rather than a preference; layering as the line-shaped special case of a DAG; shapes that aren't layers (pipelines, DAGs, inversion of control, cross-cutting concerns); information hiding (Parnas 1972); **Hyrum's Law** — with enough users, every observable behavior becomes a dependency; the export surface as the real API design; cost of change scaling with dependents.

*Where the claim doesn't apply:* the Law goes inert when nothing is ever separated, which is the boundary for acyclicity itself; ECS architectures, where the memory hierarchy inverts hiding; inversion of control, where the call goes up and the dependency does not; and the case where the lower layer is the more capable one.

### 06. Time: concurrency and clocks
`06_time.md`

The chapter that turns "be careful" into a rule you can apply.

Contents: check-then-act is not atomic (the TOCTOU family, with the same bug in Go, Python, and SQL); **shared mutable state + concurrency = races**, and the two ways to remove it; only the lock-holder can enforce; the single-writer principle; clock skew and why timestamps don't order events, with the resolution measured rather than asserted; Lamport and vector clocks; coordination costs latency.

*Where the claim doesn't apply:* one writer, where the whole apparatus is dead weight (embedded loops, some game main-loops); windows that are cheaper to accept than to close; and single-machine ordering, which is often good enough.

### 07. Distribution: what's impossible
`07_distribution.md`

Theorems, and the engineering that exists because of them.

The claim: **you cannot tell a slow machine from a dead one**, and most of what is impossible in distributed systems follows from it.

Contents: every timeout is a guess; CAP and PACELC, where the else-branch is the half that applies daily; FLP impossibility; Two Generals, and its practical corollary that **exactly-once delivery is impossible** — you get at-least-once plus idempotency; two systems cannot share a transaction, which is where the outbox comes from; availability is a product rather than an average (p^N), so better components do not fix it.

*Where the claim doesn't apply:* one process and one database, where reaching for distributed-systems machinery is cargo cult; coordination you can simply afford; and correlated failures, where the p^N arithmetic assumes an independence you do not have.

### 08. Scale: queues, parallelism, memory
`08_scale.md`

Where the arithmetic beats the intuition.

Five shapes, and which one you are on decides the fix: ceiling, reversal, cliff-edge curve, step, floor.

Contents: Amdahl's Law as a ceiling; the Universal Scalability Law and why throughput can *decrease* with more workers; Little's Law; what queues do near capacity — **there is no threshold at 85%**, only a marginal cost that rises smoothly from the start, with the cost of one extra point tabulated at four places on the curve; **the memory hierarchy across six orders of magnitude**, with a measured 7.1x from array-of-structs versus struct-of-arrays and no algorithm change; the speed of light as a latency floor; big-O versus constants in both directions.

*Where the claim doesn't apply:* small collections, where the constant factor wins and the asymptotically better algorithm loses; systems nowhere near the bend, where the arithmetic is real and inert; and cases where speed is not the constraint.

### 09. Change: evolution, organization, compatibility
`09_change.md`

The laws that operate on the timescale of years rather than milliseconds.

Contents: Lehman's Laws of Software Evolution; Conway's Law, and the inverse manoeuvre; Brooks' Law and the n(n−1)/2 arithmetic underneath it; compatibility is forever once published; the durable-artifact question — schema, protocol, and public API outlive the code that touches them, which changes where invariants should live.

*Where the claim doesn't apply:* code with a known death date — a migration script, a spike, a one-off report; internal interfaces you can change atomically, where "published" does not yet apply; and small teams, where Brooks and Conway both go quiet.

## Part III — Patterns, graded

### 10. What a pattern is for
`10_what-a-pattern-is-for.md`

Two tests, applied throughout the rest of Part III.

Contents: **compression** — does naming it save more words than it costs? **constraint** — does it rule anything out? Patterns as vocabulary versus patterns as prescription; why catalogues get misread as checklists; the difference between describing a shape and recommending one.

*Where the claim doesn't apply:* a design too young to name, where a vague name is the honest one; local vocabulary that compresses for insiders and nobody else; and names kept because they are how you find the literature on a shape's failure modes.

### 11. Patterns that cross the line
`11_patterns-that-cross.md`

The chapter that rescues the useful half of the GoF material.

The core claim: **the same pattern name describes an afternoon's work or a permanent obligation, and what separates them is whether you can change the other side.**
Usually called a question of scale; size only correlates, because systems acquire other owners as they grow. The axis is chapter 03's control-of-callers Force, read from the other end.

Contents: one integration crossing the line, before and after; which rows of the pattern table are canonical and which are this book's reading; why most pattern arguments are two people answering different ownership questions.

*Where the claim doesn't apply:* patterns unchanged by the crossing (Strategy, Template Method); partial ownership, where the alternatives are expensive rather than absent; and Singleton, which changes more than anything else in the chapter.

### 12. Patterns that survive translation
`12_patterns-that-survive-translation.md`

Not a catalogue. The claim is that the patterns which last are answers to Forces, so grouping them by Force finds the name from the situation — which is the direction you actually need, and the one a catalogue organized by shape cannot serve.

Fifty-four patterns sorted against chapter 03's seven Forces, in chapter 03's order: forty-nine fall into them, five refuse. Two worked per Force with code, the constraint, and the cost; the rest of each family listed one line each, so the grouping can be checked against the whole field rather than the chosen cases. Patterns another chapter owns are cited, not re-explained.

The Forces are chapter 03's, named and ordered as that chapter names them, so the grouping can be checked against the definition rather than against a fresh set of labels.

*Where the claim doesn't apply:* the five that refuse to sort, which split into patterns answering a goal — a property you elected to want, and could decide to want less of — and patterns answering the shape of the problem (State Machine, Transaction Script); one Force with several answers, where only intensity decides; and the fact that a list places patterns without endorsing them.

### 13. Patterns that are missing language features
`13_missing-language-features.md`

The Gang of Four audit, worked rather than asserted.

The claim: **much of the catalogue is scaffolding that mimics a language feature** — build the same design in a language that has the feature and the scaffold disappears while the design stays.
Chapter 12 asked what a pattern answers; this asks what it is made of, and the two are independent.

Contents: Norvig's 1996 count read from the slides rather than from its retelling — 16 of 23 "invisible **or simpler**", "for at least some uses of each pattern", and three levels rather than two, none of which survives the folk version.
The centrepiece is Visitor written twice **in Java**: the 1994 double dispatch, and the same design in Java 26 with `sealed`, `record`, and pattern matching, which is a sum type in all but name.
The argument is the guarantee rather than the line count — both versions refuse to compile when a case is added and a consumer is not updated, at 28 lines against 11.
Then Strategy in four languages, with the policies kept named on both sides so the comparison is not rigged; and the rest of the catalogue placed compactly.

*Where the claim doesn't apply:* the same feature that dissolves Visitor leaves **Composite** standing in the same file, because containment is a claim about the domain; **Decorator**, where the test returns no — measured in Go the function form is *longer*, and interface width rather than language decides what decoration costs; Observer, which dissolves in one process and returns across a machine, so the test is scoped; and the fact that the test names the language you moved *to*, so "Visitor is a workaround" is true and useless if your compiler lacks the feature.

### 14. Smuggled verdicts
`14_smuggled-verdicts.md`

Vocabulary that arrives with its conclusion already attached.

The claim: **some vocabulary arrives with its verdict attached, so accepting the word concedes the argument** — and how much you conceded depends on whether the word also names something you can go and check.

Two independent questions, graded the way chapter 10 grades names rather than on a single ladder: does the term pick out something in the code, and does it carry a verdict.
All four cells are occupied, and the damaging one is **names a shape *and* convicts it** — the shape is checkable, so the term reads as description while the verdict rides along unexamined.

Contents: one invoice described twice, accurately, as a Transaction Script and as an anemic domain model; what Fowler actually wrote in 2003, read from the source — *"they incur all of the costs of a domain model, without yielding any of the benefits"* — and the antecedent that does not travel with the verdict; the third option the term cannot see, which is behaviour **placed by scope**, with sqlite enforcing the rule no Go code could; and the cell where a word names no shape at all, where *this smells* is a fact about the reader rather than about the file.

*Where the claim doesn't apply:* verdict nouns that name a Law violation — *SQL injection*, where the condition attached is *always* — against ones naming a Principle violation, like *premature optimization*, where the answer is a latency budget; refusing all judgment-laden vocabulary, which is a slogan of the same kind; and the fact that a term's cell is not fixed, shown by *monolith* crossing the verdict axis and partly back without ever leaving the top row.

## Part IV — Methodologies versus principles

### 15. How a principle loses its scope
`15_principle-to-movement.md`

The mechanism, stated once, so the case studies can be short.

The claim: **a compressed principle carries the scope of its key words only where the sentence names it** — and where it does not, a reader without the surrounding context supplies that scope, with the widest reading being the only one available.

One sentence followed from the talk that glossed it to the people who received it, the whole path on the record.
Pike borrows the proverb form from Segoe's *Go Proverbs Illustrated* and describes it as opaque by design; gives *don't communicate by sharing memory* a narrow reading — hand off the pointer and lose access to it; says the proverbs are for people who already know them, as tools for explaining; and predicts the wiki that now carries the nineteen sentences and none of that.
Then a reader resolving *sharing memory* outward, in their own words, about code that is race-clean.
Then the scope rebuilt by hand three times — the Go project's own wiki page reconstructing Pike's reading in a table, two commenters doing it again, and a meta-proverb improvised in a thread.

The finding the go-game collections supply: **scope lives inside the sentence or in apparatus around the collection, and where it is in neither the reader supplies it.**
Which exposes a control inside Pike's own list — four proverbs take a named package as their grammatical subject and have nowhere to drift to, so the test becomes checkable rather than hopeful.

*Where the claim doesn't apply:* advice with no scope to lose, where gofmt travelled intact; the domain gap between a fixed board game and software, which explains the lag without excusing it; and the fact that this chapter ends in repair rather than entrenchment, which is why the endpoint term belongs to 23.

### 16. OOP versus the Direction Rule
`16_oop-vs-direction.md`

The first case study, and the one with the most code.

Contents: bidirectional associations in domain models; how inheritance creates dependencies that point both ways in practice; "tell, don't ask" pushing toward object webs; ORMs materializing cyclic graphs; what cycles cost concretely — serialization, test setup, comprehension.
The alternative demonstrated: flat structures with explicit identifiers, and what you give up by choosing it.

*Where the claim doesn't apply:* domains with genuinely rich single-entity invariants, where behaviour on the object is the right answer and this chapter's advice would produce anaemia for real.

### 17. TDD, mocks, and what testing actually buys
`17_tdd-and-mocks.md`

The second case study, kept fair.

Contents: generated tests that pass without reaching the condition they name, and mutation as the only check that catches them (FlowCore's decision 37: five toothless tests in one iteration); what the empirical literature actually shows about test-first, where the controlled studies disagree with each other and most of them measure test-first against no tests rather than against test-after; the difference between "tests help" and "this ordering ritual helps"; **mocks assert that your code calls your mocks** — the argument, with a test that passes while the constraint it claims to verify has been deleted; how the mocking convention generates interface-per-class, which generates the DI container; what the testing pyramid assumes about where your logic lives, and what happens when your logic lives in a schema instead.

*Where the claim doesn't apply:* systems where the dependency genuinely cannot be run in a test — payment gateways, hardware, third-party APIs — and the honest version of test doubles for those.

### 18. Clean Architecture versus the language
`18_clean-architecture-vs-language.md`

The third case study: what happens when a structural idea is expressed as directories.

Contents: **layered packages force exports** — splitting a store into its own package requires making its helpers public, so the wall meant to hide them is what exposes them; the mapping tax of one entity type per layer; interfaces with one implementation; the `internal/` manoeuvre and what it's actually for; why the same architecture in Go, C#, and Python produces three different file layouts and only one of them needs the ceremony.

*Where the claim doesn't apply:* large teams and multi-module builds, where a compiler-enforced import boundary buys something a convention cannot.

## Part V — Contextual programming

### 19. The force-map method
`19_force-map-method.md`

The practical procedure the whole book has been building toward.

Contents: read the forces, derive the principles, then check the idioms — in that order, never the reverse; **grilling** as this method run with a generator in the loop — the interview that surfaces each decision before code exists, quoted in full, with its provenance and the limit that it is weakest where the training corpus is most uniform; a worked force-map for four systems from scratch; how to notice you have inherited a principle whose forces are absent; what to do when forces conflict.

*Where the claim doesn't apply:* situations where the conventional answer is good enough and the analysis costs more than the decision is worth.

### 20. Six domains, six inversions
`20_six-domains.md`

The longest chapter, and the payoff.
Each domain: which forces dominate, which standard advice inverts, and the code that shows it.

- **Line-of-business / data-durable** — the schema outlives the code; invariants belong in the database; the ORM question.
- **Games and simulations** — cache locality outranks encapsulation; ECS; data-oriented layout; why "a class per entity" loses to arrays.
- **Embedded and real-time** — no allocation, no exceptions, static everything; determinism over throughput; DI is meaningless when there is one of everything.
- **Compilers and language tooling** — pipelines rather than layers; a shared AST that everything touches, and why that isn't a violation.
- **UI frameworks and libraries** — inversion of control is the product; your code is the leaf; the framework calls you.
- **Distributed services** — no shared transaction, so idempotency and retries replace atomicity; the entire consistency toolkit changes shape.

*Where the claim doesn't apply:* systems that straddle two domains, which is most interesting systems — and how to decide which forces win at each boundary.

### 21. Idioms: why ecosystems diverge
`21_idioms.md`

Idioms, taken seriously rather than dismissed.

Contents: why Go grew free functions and C# grew containers, traced to language features rather than culture; an Idiom whose precondition failed because the reader stopped being the author (FlowCore's decision 18: short Go names, generated idiomatically, deviated from deliberately); why Python skipped DI except where per-request lifetime is real; the case *for* obeying local idiom even when you can argue against it — reviewability, hiring, the cost of being interesting; when to deviate, and how to pay for it (declare it, document the reason, keep it narrow).

*Where the claim doesn't apply:* idioms that encode a genuine mistake, and how to tell those from idioms you merely dislike.

### 22. Style: the level where being right doesn't matter
`22_style.md`

Short chapter, deliberately.

Contents: naming, formatting, file layout, comment density; why consistency beats correctness here; why style arguments consume energy disproportionate to their stakes; the one case where style becomes substance — when a naming convention encodes a real distinction the type system can't.

*Where the claim doesn't apply:* nothing, really — which makes this the one chapter whose counter-example section argues that its own subject barely matters.

### 23. Reading advice at the right level
`23_reading-advice.md`

The field guide, and the closing.

Contents: receiving a blog post; receiving a code review comment; receiving a book; receiving a colleague's strong opinion; receiving your own past decisions; **receiving generated code** — the sixth case, and the one the others rehearse for, where the artifact states no decisions at all because every branch was taken silently; the questions that do the work — *what forces does this assume? at what scale? what does it rule out? where does the author say it stops?*
The final answer to "is this load-bearing" as a repeatable procedure rather than a judgement call.

Also the **folk remedy** — the author's term, held back from chapter 15 because that chapter's evidence ends in repair rather than entrenchment.
A folk remedy is advice applied far outside the context it was made for, which stays misapplied because nobody rebuilds its scope; *drink two litres of water a day* is the pattern.
By 23 the Part IV case studies have supplied endpoints that earn the term, so this is where it belongs — and the receiving question it generates is *how wide is this advice, and who decided that?*

Also **the book's own conditions**, cut from chapter 15 as pre-emptive there and belonging here, where the method is actually delivered.
Two are not negotiable: chapter 02's classification model is a lens rather than a finding and cannot be proved, only used; and the review practice this book runs on requires the expertise it appears to replace, since a reviewer without depth in the material reads the same confident paragraph and approves it.

*Where the claim doesn't apply:* when you don't have time to analyse and must simply pick the conventional answer — which is usually the correct move, and knowing that is part of the skill.

---

## Status

*Not started* — no file yet.
*In progress* — the file exists and is being worked through review.
*Draft* — the author is satisfied and the chapter is behind us.
*Ready* — fit to publish.

| Chapter | File | Status |
|---|---|---|
| 01 | `01_why-good-advice-goes-wrong.md` | not started |
| 02 | `02_the-five-kinds.md` | **draft** |
| 03 | `03_forces.md` | **draft** |
| 04 | `04_grading-a-law.md` | **draft** |
| 05 | `05_structure.md` | **draft** |
| 06 | `06_time.md` | **draft** |
| 07 | `07_distribution.md` | **draft** |
| 08 | `08_scale.md` | **draft** |
| 09 | `09_change.md` | **draft** |
| 10 | `10_what-a-pattern-is-for.md` | **draft** |
| 11 | `11_patterns-that-cross.md` | **draft** |
| 12 | `12_patterns-that-survive-translation.md` | **draft** |
| 13 | `13_missing-language-features.md` | **draft** |
| 14 | `14_smuggled-verdicts.md` | **draft** |
| 15 | `15_principle-to-movement.md` | **in progress** |
| 16 | `16_oop-vs-direction.md` | not started |
| 17 | `17_tdd-and-mocks.md` | not started |
| 18 | `18_clean-architecture-vs-language.md` | not started |
| 19 | `19_force-map-method.md` | not started |
| 20 | `20_six-domains.md` | not started |
| 21 | `21_idioms.md` | not started |
| 22 | `22_style.md` | not started |
| 23 | `23_reading-advice.md` | not started |

### AI material

Chapters 02, 03, 15, 17, 19, 21 and 23 each owe a piece of this, noted in their contents lines above.
The worked argument — findings, FlowCore evidence, the grilling text with its provenance, and the traps — is in **`docs/ai-material.md`**.
Read that rather than re-deriving it, so the seven mentions agree with each other.

### Pending revisits

Chapters already at **draft** that are owed an addition. Listed here because a drafted chapter is not re-read on its own, and a decision entry is only consulted when reversing something.

| Chapter | Owed | Do it when |
|---|---|---|
| 02 | corpus monoculture as a new instance of *monoculture makes Idioms look like physics* | chapter 23 exists, so the mention can point at the synthesis |
| 03 | the generator cannot see your Forces; the team-size Force at its limit — no continuity, unbounded volume | as above |

The worked argument is in `docs/ai-material.md`; decision 24 records what was decided and why.

**Build order.** The original plan was 02, then 05, then 13. What happened instead was 02, 05, 03, 04 — Part I first, then the foundations in order — and the reason to continue that way is that the drafted chapters have accumulated debts to specific unwritten ones.

Forward references currently outstanding: **06** (six), **18** (five), **07** (four), **17** and **09** (two each). Chapter 06 is the most owed and the most immediate: chapter 03's concurrency Force defers its races to it, and chapter 05 defers the unclosable check-then-act window to it.

Chapter 01 remains easier to write once the rest exists.
