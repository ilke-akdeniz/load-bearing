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

Contents: one invoice described twice, accurately, as a Transaction Script and as an anemic domain model; what Fowler actually wrote in 2003, read from the source — *"they incur all of the costs of a domain model, without yielding any of the benefits"* — and the antecedent that does not travel with the verdict; the third option the term cannot see, which is behaviour **placed by what the rule must see**, with sqlite enforcing the rule no Go code could; and the cell where a word names no shape at all, where *this smells* is a fact about the reader rather than about the file.

*Where the claim doesn't apply:* verdict nouns that name a Law violation — *SQL injection*, where the condition attached is *always* — against ones naming a Principle violation, like *premature optimization*, where the answer is a latency budget; refusing all judgment-laden vocabulary, which is a slogan of the same kind; and the fact that a term's cell is not fixed, shown by *monolith* crossing the verdict axis and partly back without ever leaving the top row.

## Part IV — Methodologies versus principles

### 15. How a principle loses its scope
`15_principle-loses-scope.md`

The mechanism, stated once, so the case studies can be short.

The claim: **a compressed principle carries its scope only when it names the situation it applies to** — and where it doesn't, the reader has to reconstruct that scope from the surrounding context, with only the widest reading available without it.

One sentence followed from the talk that glossed it to the people who received it, the whole path on the record.
Pike borrows the proverb form from Segoe's *Go Proverbs Illustrated* and describes it as opaque by design; gives *don't communicate by sharing memory* a narrow reading — hand off the pointer and lose access to it; says the proverbs are for people who already know them, as tools for explaining; and predicts the list that now carries the nineteen sentences and none of that.
Then a reader resolving *sharing memory* outward, in their own words, about code that is race-clean.
Then the scope rebuilt by hand three times — the Go project's own wiki page reconstructing Pike's reading in a table, two commenters doing it again, and a meta-proverb improvised in a thread.
Then the same mechanism twice more in Pike's 2023 GopherConAU retrospective: Ousterhout's *threads are bad*, whose situation was pthreads and which Google banned company-wide anyway, diagnosed by Pike as generalizing beyond the domain; and his own team's concurrency guidance, where he says the use cases were server software, that they should have said so, and that the confusion probably drove people away.

The finding the go-game collections supply: **scope lives inside the principle or in an apparatus around the collection it belongs to, and where it is in neither the reader reconstructs it — or fails to.**
Which exposes a control inside Pike's own list — four proverbs take a named package as their grammatical subject and have nowhere to drift to, so the test becomes checkable rather than hopeful.

*Where the claim doesn't apply:* a named situation is only a **proxy** for the conditions and can fit badly in either direction — syscall and cgo are two proverbs for one condition, so a third platform-specific case has none, and the test therefore measures whether you were given something checkable rather than whether the extent is right; advice with no scope to lose, where gofmt travelled intact; the domain gap between a fixed board game and software, which explains the lag without excusing it; and the fact that this chapter ends in repair rather than entrenchment, which is why the endpoint term belongs to 23.

### 16. Behaviour placement and OOP
`16_behaviour-placement.md`

The first case study.

**Chapter 15's mechanism, running on:** *behaviour belongs with the data it operates on.*
The scope was written down and did not travel. Riel's heuristic 2.9 says *related* data and behaviour, and glosses it as one key abstraction split across two places — which excludes a rule reading two entities, since 2.8 makes those two abstractions. His introduction adds that all sixty are *warning bells*, that it is *perfectly valid to state that the heuristic does not apply*, and that they conflict; he wrote it to avoid what happened to *goto considered harmful*.
The chapter shows the wide reading first and the source after it, so the exclusion arrives as a correction to something the reader has already watched go wrong.
The wide reading puts each rule on the entity whose data it reads, which is right for each rule taken alone and leaves a reference pointing each way.
The narrow reading already exists in this book — chapter 14's *what the rule must see*, where the location follows from how much data you must be looking at before you can tell whether a rule holds.

Contents: two rules over a customer and an order, each placed correctly, closing the cycle between them; the distinction the chapter turns on, between two classes that reference each other and a constructed value graph carrying a back-pointer; `HashSet.add` throwing `StackOverflowError`, with `json.Marshal`, `json.dumps` and a generated `equals` all refusing the same shape; and `isGold` as the control — a one-entity rule that does get moved into a service, often, but never by reading this sentence, which is what makes the pressure one-way.
The alternative demonstrated: identifiers instead of references, and FlowCore's decision 3 priced both ways — offline construction and working serialization bought, a query per route and cross-definition integrity moved into composite foreign keys, paid.

*Where the wide reading is right:* rules that read one entity, where the currency check belongs on the money value and moving it out puts it where a caller can skip it; and cycles nothing ever walks generically, where the exemption is structural unreachability rather than nothing having walked it yet.

### 17. TDD, mocks, and what testing actually buys
`17_tdd-and-mocks.md`

The second case study, kept fair.

**Chapter 15's mechanism, running on two principles:** *write the test first*, and *mock your dependencies* — neither of which is the settled default it travels as.
Fowler's definition names what test-first buys and does not claim the sequence improves the code; Beck's canon states the loop and mentions no mocking, no isolation and no speed requirement at all.
*Mock your dependencies* is the mockist half of a disagreement Fowler named in 2007 and came down against, so the position this chapter argues is the classical one, which has had a name for two decades.

Contents: **mocks assert that your code calls your mocks** — a registration service whose uniqueness rule is a schema constraint, the constraint then deleted, and only the database-backed test failing; a fixture that fabricates its precondition instead of establishing it — writing a row that resembles an account, in the state the assertion expects — so gutting the method under test changes nothing, with FlowCore's decision 37 as the same shape in a real system; and the ordering, taken from Fucci et al. read in full — sequencing predicted neither quality nor speed, and the paper's own conditions are the part that does not travel, including *provided that they keep writing tests* and a cycle defined as the interval between green bars.
The two principles are not separate: the loop runs at minutes, so the suite must answer in seconds, so the database leaves the test — which is where the test that cannot fail comes from.
Costs are priced for both halves, the ordering's from the study's own adherence numbers: no session ran purely test-first, after ten hours of training.

Not covered: the wider empirical literature, since the meta-analyses are paywalled and were not read; and interface-per-class and the DI container, which no chapter currently owns — chapter 18 reaches the testing half of it and no further.

*Where the wide reading is right:* dependencies that genuinely cannot be run in a test — payment gateways, hardware, third-party APIs — and the honest version of doubles for those; and a mock asserting a call where the call is the observable behaviour.

### 18. Abstraction as insurance

`18_abstraction-as-insurance.md`

The third case study, and the one that survives *but what if we do need it*.

**Chapter 15's mechanism, running on:** *depend on abstractions, not concretions.*
Martin's 1994 paper names the test as **stability**, and gives plurality as the reason an abstraction is stable: the more implementations depend on it, the harder it is to change.
The five words that travel keep the technique and drop the test, so an interface with one implementation carries the principle's name while failing it.
The chapter shows the wide reading first and the source after it, so the stability test arrives as a correction to an interface the reader has already watched fail.

Contents: the distinction everything rests on — **simultaneous plurality** (two implementations loaded at once, something dispatching between them) against **sequential replacement** (one engine, then another, forever), where only the first is a Force and the second is what people mean; **injection is not abstraction**, stated because chapter 05 otherwise refutes the claim in a sentence; four reasons the insurance cannot pay out, each leaning on a Law the book already owns; and the rollback objection answered with what actually does the job — replication, comparison, per-tenant cutover, a window where both engines run.

Also the paper's own last paragraph, in print since 1994 and still lost: the standard may suit only certain applications, and its author would regret unconditional conformance.

*Where the wide reading is right:* portability sold as a contract term, which is plurality and load-bearing; a funded and dated migration, where the objection changes from *this will never happen* to *this is not how to do it*; the testing case, which chapter 17 owns and answers; and the one-implementation interfaces chapter 05 defends for reasons that survive deleting the word *later*.

## Part V — Contextual programming

### 19. The force-map method
`19_force-map-method.md`

The practical procedure the whole book has been building toward, and the one thing about it that is checkable.

**The claim:** design advice is verified in one sequence — forces, then principles, then idioms. A principle followed where its forces are absent, and an idiom followed where its principles are not needed, are the two ways a design goes wrong while every decision in it still looks correct.
Read in that direction each step takes an input from the one before and every claim has a falsifier. Read backwards from a convention, the chain comes out consistent and unfalsifiable, because it was assembled from the answer.

Contents: the three steps, and then why step one is not instrument work — some forces are countable, most are judgements, and which facts count as forces depends on the decision in front of you, so all the method claims is that a force is the kind of thing that has an answer. Four systems given only as force readings — a migration script, a ledger, a published library, a real-time loop — with four pieces of the book's own advice run across them and changing verdict, every difference tracing to a cell.
Then the map itself, worked on FlowCore's decision 12: forces with values, the principle they license, two idioms checked and rejected, and the three lines nothing else records — **forced, chosen, deferred** — plus the trigger that would reopen it. Chapter 12 owns the architecture decision record; what this adds to Nygard's template is forced-against-chosen and a trigger written before rather than a status marked after.
Also: detecting an inherited principle by asking what would have to be true for it to be unnecessary; five moves for conflicting forces, ending in escalation with quantities named, which is chapter 03's debt discharged; and **grilling** under AI-assisted development — the frozen prompt in full, its provenance, a worked exchange where two corpus defaults are overridden by facts only the human has, and the limit that it surfaces contested choices and conceals settled ones.

*Where the claim doesn't apply:* the conventional answer is good enough and the analysis costs more than the decision; the forces are not knowable yet, so reading them is guessing with a table attached; and a decision with one live option, where mapping is theatre.
*What it costs:* it requires the expertise it appears to replace, most of which goes into step one.

### 20. Six profiles, six inversions
`20_six-profiles.md`

The longest chapter, and the payoff.
Each force profile: which force sits outside its ordinary range, which standard advice inverts, and what it becomes instead.
*Domain* keeps its ordinary meaning — what the software is about. **Force profile** is this book's term for the reading of every force bearing on a system, at least one of them outside its ordinary range; the chapter's claim is that the two are independent axes, and that the domain name on its own predicts nothing.
The demonstration runs both directions: three unrelated domains sharing one profile, and two sales systems — pizza ovens and marine-port security — with the same domain and opposite concurrency readings.
The business supplies that reading, though not in answer to the question usually put to it.

- **Line-of-business / data-durable** — durability, so *keep business rules out of the database* inverts because a rule enforced only in application code holds until the next application, *the database is a detail* inverts with it (Ch. 18), and the ORM question is argued from the force rather than from taste.
- **Games and simulations** — chapter 05 owns the entity-component inversion, so this section takes the two it does not: allocate before the loop rather than when a profiler says so, and buy reproducibility with accuracy and speed.
- **Embedded and real-time** — exceptions become status codes because unwinding has no worst case anyone can certify, buffers are sized at compile time because there may be no allocator, and dependency injection inverts since there is one sensor, one radio, one clock.
- **Compilers and language tooling** — *nothing should be depended on by everything* inverts for the syntax tree, and the finding that generalises out of it is that fan-in alone is not the smell — fan-in with fan-out is.
- **UI frameworks and libraries** — inversion of control is not a technique applied here but the product, since a framework whose control you kept would be a library, and its lifecycle is therefore a Force rather than a convention.
- **Distributed services** — chapter 07 owns the mechanism, and what this adds is that nothing weakens by a little: transactions become sagas, foreign keys become reconciliations, rollbacks become compensating operations a customer can see.

Then what the six have in common, which is chapter 02's distinction at scale: a Law holds throughout, a Principle turns over, and the inversion is predictable from the force reading alone.
And an asymmetry worth stating because it decides what to ask someone arriving from a domain you do not share — profile knowledge transfers, domain knowledge does not.

*Where the claim doesn't apply:* systems that straddle two profiles, which is most interesting systems, and where the seam goes; the ordinary case, where every force sits in its ordinary range — which is most software, and which the chapter treats as a finding with four consequences rather than a disappointment; a profile you are visiting rather than living in; and the domains not on the list, six being no enumeration.

*What it costs:* moving between profiles costs judgement you do not know you are losing; *it's a different profile* becomes an unfalsifiable excuse unless it names a force and its value; and six labels invite a lookup table when the point was the derivation.

### 21. Idioms: why ecosystems diverge
`21_idioms.md`

Idioms, taken seriously rather than dismissed.
The claim: **an Idiom rests on a condition about your surroundings rather than about your problem, and naming that condition is what separates deviating from an Idiom from merely ignoring one.**
A Principle's condition is a fact about your system, looked up by measuring it; an Idiom's is a fact about the language, the tooling, or who will read the code.
The condition framing is this book's own rather than standard vocabulary.

The demonstration runs the same package split in two languages, both executed.
Go refuses to compile, and the only fix publishes the helper the split was meant to hide; Python reaches that helper across the boundary and runs, because a leading underscore is a request no machine enforces.
C# is given as mechanism rather than output, the toolchain being unavailable.
Then two more: where the Idiom/Style line falls in each language, since Go makes an identifier's case an access modifier and Python makes indentation syntax, so the two things everyone files under Style are structural there; and one decision under three sets of conditions, which is the explanation for a demonstration chapter 02 already owns.

Why it holds: the condition does not travel, so an Idiom carried across arrives with nothing to check it against.
Obedience is the default because it rests on a condition too — *other people will read this and expect the convention* is a fact about your surroundings of the same kind as the rest, so winning the argument about whether the convention is good does not touch it.
The worked deviation is Pike's early Go compiler in C: conditions named, kept to one component, declared in public, offence taken, and the reason later expiring so that the deviation was reversed at Go 1.5.

*Where the claim doesn't apply:* naming the condition is necessary and not sufficient, which Pike's interfaces show — Ian Taylor pushed the problem from early on, from inside, and the convention held for more than a decade anyway; and an Idiom can be a bad inference from a true condition, which `defer file.Close()` shows by discarding an error that *cleanup belongs next to acquisition* never implied throwing away.

*What it costs:* most of the time the answer is obey, and the work of naming the condition returns nothing visible; *I can name the condition* becomes the licence chapter 20 records one level up; and deviations are individually cheap and collectively expensive.

### 22. Style: the level where being right doesn't matter
`22_style.md`

Short chapter, deliberately.

Contents: naming, formatting, file layout, comment density; why consistency beats correctness here; why style arguments consume energy disproportionate to their stakes; the one case where style becomes substance — when a naming convention encodes a real distinction the type system can't.
Also Go's short-name convention, which chapter 02's mechanical test sorts here rather than to Idiom because nothing but a reader can see it.
FlowCore's decision 18 and this book's decision 49 both deviate from it, for two different failed assumptions — a maintainer returning after a context switch, for whom decoding never amortizes, and a reader who sees a sample once and never returns.
Both wrote the reason down, which is this chapter's own oddity: where being right does not matter, being seen to have chosen still does.

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
| 15 | `15_principle-loses-scope.md` | **draft** |
| 16 | `16_behaviour-placement.md` | **draft** |
| 17 | `17_tdd-and-mocks.md` | **draft** |
| 18 | `18_abstraction-as-insurance.md` | **draft** |
| 19 | `19_force-map-method.md` | **draft** |
| 20 | `20_six-profiles.md` | **draft** |
| 21 | `21_idioms.md` | **draft** |
| 22 | `22_style.md` | not started |
| 23 | `23_reading-advice.md` | not started |

### AI material

Chapters 02, 03, 15, 17, 20, 22 and 24 each owe a piece of this, noted in their contents lines above.
The worked argument — findings, FlowCore evidence, the grilling text with its provenance, and the traps — is in **`docs/pending/ai-material.md`**.
Read that rather than re-deriving it, so the seven mentions agree with each other.

### Pending revisits

Chapters already at **draft** that are owed an addition. Listed here because a drafted chapter is not re-read on its own, and a decision entry is only consulted when reversing something.

| Chapter | Owed | Do it when |
|---|---|---|
| 02 | corpus monoculture as a new instance of *monoculture makes Idioms look like physics* | chapter 23 exists, so the mention can point at the synthesis |
| 03 | the generator cannot see your Forces; the team-size Force at its limit — no continuity, unbounded volume | as above |
| 02 | Pike on arguments about language features being opinion argued with certainty — a witness for *tone does not vary with authority*, in `docs/pending/pike-retrospective.md` | next time 02 is open |
| 09 | Pike pricing Go's compatibility promise: it costs, and it blocks feature-itis — the constraint adopted deliberately rather than suffered | next time 09 is open |
| 13 | possibly the async/await aside and *coloured functions*; check the fit before using it, it may belong to 20 or nowhere | next time 13 is open |

The worked argument is in `docs/pending/ai-material.md`; decision 24 records what was decided and why.

**Build order.** The original plan was 02, then 05, then 13. What happened instead was 02, 05, 03, 04 — Part I first, then the foundations in order — and the reason to continue that way is that the drafted chapters have accumulated debts to specific unwritten ones.

Forward references currently outstanding: **06** (six), **18** (five), **07** (four), **17** and **09** (two each). Chapter 06 is the most owed and the most immediate: chapter 03's concurrency Force defers its races to it, and chapter 05 defers the unclosable check-then-act window to it.

Chapter 01 remains easier to write once the rest exists.
