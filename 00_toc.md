# Load-Bearing — Table of Contents

Twenty-three chapters in five parts.
Each entry states what the chapter argues, what it covers, and — per the book's own rule — where its claim stops.

Back to [README](README.md).

---

## Part I — The five kinds

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
Principles are conditional on Forces; naming them is most of the work of choosing well.

Contents: concurrency; durability of the medium (a schema outlives the code that writes it); blast radius of a bug; change frequency and its shape; team size and turnover; latency budget; whether you control the callers.
Each Force with a code demo of the same problem solved differently under different values of it.

*Where the claim doesn't apply:* Forces you can't measure yet, and why guessing is worse than deferring.

## Part II — The foundations

### 04. Three kinds of true
`04_grading-a-law.md`

Not every Law has the same standing.
Theorem, definition, and empirical law are three different kinds of true, and each admits exactly one move.

Contents: what makes Two Generals a different kind of claim from Conway's Law; what makes Conway's Law different from "prefer composition over inheritance"; the halting problem as a theorem whose folk version dropped a quantifier; how to check a claimed Law.

*Where the claim doesn't apply:* Laws that are true but irrelevant at your scale — Amdahl on a single-threaded CLI.

### 05. Structure: dependency and hiding
`05_structure.md`

The Direction Rule and its family.

Contents: acyclic dependency, and why it's a Law rather than a preference; layering as the line-shaped special case of a DAG; shapes that aren't layers (pipelines, DAGs, inversion of control, cross-cutting concerns); information hiding (Parnas 1972); **Hyrum's Law** — with enough users, every observable behavior becomes a dependency; the export surface as the real API design; cost of change scaling with dependents.

*Where the claim doesn't apply:* ECS architectures, where cache layout outranks encapsulation; plugin systems where inversion makes calls legitimately go "up."

### 06. Time: concurrency and clocks
`06_time.md`

The chapter that turns "be careful" into a rule you can apply.

Contents: check-then-act is not atomic (the TOCTOU family, with the same bug shown in four languages); **shared mutable state + concurrency = races**, and the two ways to remove it; only the lock-holder can enforce; the single-writer principle; clock skew and why timestamps don't order events; Lamport and vector clocks; coordination costs latency.

*Where the claim doesn't apply:* genuinely single-threaded systems (embedded loops, some game main-loops), where the whole apparatus is dead weight.

### 07. Distribution: what's impossible
`07_distribution.md`

Theorems, and the engineering that exists because of them.

Contents: CAP and PACELC; FLP impossibility; Two Generals, and its practical corollary that **exactly-once delivery is impossible** — you get at-least-once plus idempotency; you cannot distinguish a slow node from a dead one, so every timeout is a guess; reliability compounds (p^N); the Transactional Outbox and Saga patterns as direct consequences.

*Where the claim doesn't apply:* a single process with one database — where reaching for distributed-systems machinery is cargo cult.

### 08. Scale: queues, parallelism, memory
`08_scale.md`

Where the arithmetic beats the intuition.

Contents: Amdahl's Law; the Universal Scalability Law and why throughput can *decrease* with more workers; Little's Law; queueing theory and why 85% utilization is a cliff rather than headroom; **the memory hierarchy across six orders of magnitude**, with a benchmark showing array-of-structs versus struct-of-arrays; the speed of light as a latency floor; big-O versus constants in both directions.

*Where the claim doesn't apply:* small-n, where the constant factor wins and the asymptotically better algorithm loses.

### 09. Change: evolution, organization, compatibility
`09_change.md`

The laws that operate on the timescale of years rather than milliseconds.

Contents: Lehman's Laws of Software Evolution; Conway's Law, and the inverse manoeuvre; Brooks' Law and the n(n−1)/2 arithmetic underneath it; compatibility is forever once published; the durable-artifact question — schema, protocol, and public API outlive the code that touches them, which changes where invariants should live.

*Where the claim doesn't apply:* code with a known short life — a migration script, a spike, a one-off report.

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

*Where the claim doesn't apply:* the seven that refuse to sort, which split into patterns answering a goal (the testing family) and patterns answering the shape of the problem (State Machine, Transaction Script); one Force with several answers, where only intensity decides; and the fact that a list places patterns without endorsing them.

### 13. Patterns that are missing language features
`13_missing-language-features.md`

The GoF audit, worked rather than asserted.

Contents: Strategy is a function; Command is a closure; Iterator is syntax now; Observer is channels or events; Factory is a function returning a thing; Template Method is passing a function; Visitor is pattern matching over a sum type; Decorator is function composition; Singleton is a package-level variable and usually a mistake.
Norvig's observation that most of the catalogue is invisible in a sufficiently expressive language, demonstrated in four languages side by side.
The diagnostic: **if the pattern disappears when you change language, it was a workaround, not an idea.**

*Where the claim doesn't apply:* languages that genuinely lack the feature — the pattern is the right answer in Java 6, and calling it obsolete is its own misclassification.

### 14. Patterns that smuggle a verdict
`14_smuggled-verdicts.md`

Vocabulary that arrives with its conclusion already attached.

Contents: "anemic domain model" as a diagnosis dressed as a description; "code smell" and the rhetoric of hygiene; how a term coined inside one argument (rich OO domain models versus J2EE entity beans) travels to contexts whose premises it doesn't fit; the third option such terms cannot see — behaviour placed by *scope* rather than by doctrine; how to spot the pattern in new vocabulary.

*Where the claim doesn't apply:* some pejorative terms name real defects, and refusing all judgment-laden vocabulary is over-correction.

## Part IV — Methodologies versus principles

### 15. How a principle becomes a movement
`15_principle-to-movement.md`

The mechanism, stated once, so the case studies can be short.

Contents: a true observation gets a name; the name gets a community; the community forgets the conditions; the conditions were the content.
The test applied to generated design, where the answer is not *the conditions were forgotten* but *there were none to forget* — the derivation never happened, so there is no one to ask.
Why practitioner credibility does not immunize anyone — Go proverbs quoted as law, Rob Pike's own complaint about it.
The test that survives: **does the idea come with the conditions under which it's wrong?**

*Where the claim doesn't apply:* movements that genuinely improved practice, and why dismissing all methodology is the mirror-image error.

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
| 12 | `12_patterns-that-survive-translation.md` | **in progress** |
| 13 | `13_missing-language-features.md` | not started |
| 14 | `14_smuggled-verdicts.md` | not started |
| 15 | `15_principle-to-movement.md` | not started |
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
