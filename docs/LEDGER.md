# Concept Ledger

Anti-repetition control.
Every concept, example, and code demonstration is **owned by exactly one chapter**.
Other chapters may reference it in a sentence and link — never re-explain it.

**Rule before drafting any chapter:** read this file.
If a concept is already owned, the new chapter gets one line and a cross-reference, not a recap.

**Rule after drafting any chapter:** add what it claimed here.

## Format

`concept` → owning chapter → the canonical one-line statement → how others may refer to it

---

## Concepts

| Concept | Owner | Canonical statement | Others may say |
|---|---|---|---|
| The five kinds of claim | 02 | A claim is one of five kinds — Law, Force, Principle, Idiom, Style — and the kind sets its authority. Four are advice and form a ladder; Force is not, so there are four levels and five kinds | "a Law / an Idiom (Ch. 02)" |
| Classification test | 02 | Five questions that place a claim in one of the five kinds | "run the test (Ch. 02)" |
| Why the kinds get confused | 02 | Tone doesn't vary with authority; advocacy compresses; monoculture makes Idioms feel universal | one clause, cite 02 |
| The Idiom/Style line is mechanical | 02 | The compiler or the runtime acts on an Idiom and neither can see a Style. What is held constant is narrow and named — what the program produces when it succeeds — so failure modes, setup effort and how much the compiler can check are all free to differ. Ecosystem-specificity does not discriminate, because plenty of Style is local. 21 owns the fact that the line falls in a different place in each language | "the machine can see it (Ch. 02)" |
| Law inert vs Principle wrong | 02 | A Force decides whether a Law *binds*; it decides whether a Principle is *right* | one clause, cite 02 |
| *Force* is a borrowed word | 02 | A named element in the literature on writing patterns, from Alexander — not in the Gang of Four template, which is what most readers mean by patterns. There it is a field describing the tensions one pattern resolves; here it is a property of your situation read before any pattern is in view, and a kind of claim rather than a template slot | "the word is the pattern-writing literature's (Ch. 02)" |
| Forces as inputs | 03 | Forces are properties of the situation, not advice | "the Force is X (Ch. 03)" |
| A Force is a dial, not a switch | 03 | A Force has an **intensity** — how hard it presses on the design, which is not how large the number is; the design changes several times across the range, each answer discarding the last | "read the intensity (Ch. 03)" |
| The seven Forces | 03 | Concurrency, durability of the medium, blast radius, change frequency and shape, team size and turnover, latency budget, control of callers | name the Force, cite 03 |
| Concurrency | 03 | How many at once, and do they touch the same state — it binds where writers collide, not where they coexist | cite 03; 06 owns the races |
| Durability of the medium | 03 | How long what this writes outlives the code that wrote it | cite 03; 09 owns published compatibility |
| Blast radius | 03 | When it is wrong, what happens and who finds out — decides how much prevention is worth | cite 03 |
| Change frequency and shape | 03 | How often, and how many places must change with it | cite 03; 05 owns fan-in pricing |
| Team size and turnover | 03 | How many must agree, and how many will still be here — the rule migrates comment → review → type system | cite 03 |
| Latency budget | 03 | What the budget is, and what fraction one mechanism costs | cite 03; 08 owns the arithmetic |
| Control of the callers | 03 | Can I change every call site, and would I know if I broke one — three values, not two | cite 03; 05 owns what it implies for exposure |
| Reversibility decides deferral | 03 | Two questions — does waiting spoil it, is it cheap today — giving three cases: defer, take it now, or admit you are betting | "the reversibility rule (Ch. 03)" |
| What `internal/` is, glossed | 03 | A package under `internal/` cannot be imported from outside its module, given while using FlowCore's decision 1 as the non-expiring deferral. 21 puts the same decision to the opposite use — what the directory is actually for — and cites this rather than re-explaining the mechanism | "`internal/` (Ch. 03)" |
| Strict is the undoable direction | 03 | Under uncertainty prefer the decision you can walk back, which is usually the stricter one | cite 03 |
| Risk vs unmeasured Force | 03 | An unmeasured Force has an instrument and a trigger; a risk has neither, so the answer is bounding the cost rather than estimating harder | cite 03 |
| Shape of scale | 03 | "High scale" names no design — steady load, bursts, and data volume are different situations sharing a vocabulary | cite 03 |
| Forces move on their own clock | 03 | Team size, client count, and row count change without a commit, invalidating Principles nobody revisits | cite 03 |
| The disagreement is about the Force, not the Principle | 03 | Two people arguing about a Principle have usually already agreed about it and differ about the situation it is conditioned on; stating the Force ends the argument or relocates it to something answerable. 02 introduces it in one sentence as a symptom and hands off; no other chapter restates the mechanism | "the disagreement is about the Force (Ch. 03)" |
| Three kinds of Law | 04 | Theorem, definition, empirical law — named, never lettered, and not ranked | "a theorem / a definitional claim (Ch. 04)" |
| One kind, its moves | 04 | Theorem: falsify an assumption, or stop needing the conclusion. Definition: check whether the words apply. Empirical: measure it where you are | cite 04 |
| Two escapes from a theorem | 04 | Arrange for one of its assumptions not to hold, or stop needing the theorem's conclusion — never argue with the conclusion | cite 04 |
| Regularity vs magnitude | 04 | A measurement is not a law; an empirical law is a regularity across systems whose magnitude varies between them | cite 04 |
| Kind is not importance | 04 | The kind says how firmly a claim is true, not how much it bears on your program | cite 04 |
| Describes vs prescribes | 04 | A Law describes what happens; a Principle prescribes. Only a Principle can become bad advice | "describes vs prescribes (Ch. 04)" |
| Theorem and folk version share a name | 04 | The folk version has usually dropped a quantifier or a condition — halting problem forbids a universal decider, not any decision | cite 04 |
| The falsification question | 04 | "What would have to be true for this to be false?" — nothing / nothing but it may not apply / a measurement | cite 04 |
| Acyclic dependency | 05 | A cycle makes two components one unit of comprehension, test, and change | "the Direction Rule (Ch. 05)" |
| What a cycle actually costs | 05 | The damage is denominated in future change, not in wrong output — which is why it accumulates unnoticed | cite 05 |
| Injection vs inversion | 05 | Injection decides who constructs; inversion decides who declares the interface, and only inversion turns an arrow around | cite 05 |
| Two-phase construction | 05 | `a := &A{}; b := &B{a}; a.b = b` is the construction site admitting the cycle | cite 05 |
| Dependency damage compounds | 05 | A missing test is a static cost; a cycle spreads to everything touching either end | one clause, cite 05 |
| Cycle detection is granularity-bound | 05 | Each toolchain checks the boundaries it happens to have; the damage exists at all of them | cite 05 |
| "Layered" is three claims | 05 | Acyclicity (Law) + the line shape (Principle) + the folder taxonomy (Idiom), under one name | "the three claims (Ch. 05)" |
| Layering as ranks | 05 | Strict layering assigns every part a rank and forbids reaching past the one beneath it | one clause, cite 05 |
| Layer ≠ directory | 05 | A layer is a rule about call direction; a folder is neither necessary nor sufficient for it | cite 05; 18 owns what folders *cost*, and no chapter may say the physical forms enforce the same thing — 18's claim is that they do not |
| Cost of change scales with dependents | 05 | Change cost is proportional to fan-in, and is paid on every change | cite 05 |
| Stability, not indirection | 05 | "Depend on abstractions" means put what changes least at the bottom; an interface is not automatically that | cite 05 |
| Internal vs external dependent count | 05 | Inside the repo `grep` gives you the number; once published it is unknown and growing | cite 05 |
| From direction to surface | 05 | Cycles are about which way edges point; hiding is about how many edges exist at all | cite 05 |
| Information hiding / Hyrum | 05 | What is observable will be depended upon | cite 05 |
| DI does not contradict hiding | 05 | Injection is a module declining to hold decisions that belong elsewhere; the composition root holds them instead | cite 05 |
| Hiding's condition | 05 | Information hiding is a Principle conditional on not controlling your callers | cite 05; the Force itself is 03's |
| Export surface as liability | 05 | Every exported identifier is a contract; the surface is an inventory of what you can no longer change | cite 05 |
| A disclaimer is not a boundary | 05 | An "unsupported" export is still an export — Hyrum's Law does not read comments | cite 05 |
| Claim two, loose vs strict | 05 | "Dependencies flow downward" is claim one restated; the strict rank rule is what most systems fail | cite 05 |
| Graph vocabulary | 05 | Arrow = depends on; fan-in = who breaks if you change; bottom = high fan-in, low fan-out | cite 05 |
| The graph exists at every size | 05 | Functions through services; size changes what detects a violation, not whether the Law binds | cite 05 |
| Four ways to break a cycle | 05 | Interface / event / third module / identifier — four different bills, chosen deliberately | cite 05 |
| Dependency inversion | 05 | The call may go up while the dependency goes down, because both parties point at an interface at the bottom | cite 05 |
| Lower layer more capable | 05 | Layering doctrine assumes the layer below is dumber; when it is more capable, "keep logic out" inverts | cite 05 |
| There is no shared now | 06 | A check reports the past; across machines there is no agreed ordering at all | "no shared now (Ch. 06)" |
| Three conditions for a race | 06 | Another writer, a decision that depends on the read, and a rule spanning data you did not hold still — all three, or nothing to fix | cite 06 |
| The three ordinary fixes | 06 | One operation; let the data-holder enforce; or do not check and handle the failure | cite 06 |
| Lock the span, not the steps | 06 | The fix is not more locking but locking the right span | cite 06 |
| One authority beats many clocks | 06 | Optimistic concurrency on a version counter needs no clock; the database is the single source of order | cite 06 |
| Check-then-act / TOCTOU | 06 | Between the check and the act, the world moved | "TOCTOU (Ch. 06)" |
| Locking each step is not locking the sequence | 06 | Individually safe operations do not compose into a safe rule | cite 06 |
| The window is as wide as the work in it | 06 | The same defect is rare on an idle machine and constant under load | cite 06 |
| Only the lock-holder enforces | 06 | A rule over rows you haven't read can't be enforced by code that hasn't read them | cite 06 |
| The app check is the message, not the guarantee | 06 | Keep it for the error text; never keep it as the enforcement | cite 06 |
| Two ways to remove a race | 06 | Remove the sharing or remove the mutability; concurrency is the term you cannot give up | cite 06 |
| Single-writer principle | 06 | One writer means nothing can interleave, so coordination cost falls to zero | "single writer (Ch. 06)" |
| Clocks do not order events | 06 | Wall clocks lack the resolution locally and agreement globally; counters order, clocks do not | cite 06 |
| Lamport vs vector clocks | 06 | Lamport preserves causality but cannot detect concurrency; vector clocks can, at a cost that grows with nodes | cite 06 |
| Coordination does not compose | 06 | Two correct locked operations are not one correct operation | cite 06 |
| Slow is indistinguishable from dead | 07 | The root of the impossibility results: you must decide on information you cannot obtain | "slow vs dead (Ch. 07)" |
| Exactly-once impossible | 07 | Two Generals ⇒ at-least-once plus idempotency | cite 07 |
| Every timeout is a guess | 07 | The observation is identical whether the peer is slow or dead, and the slow one may have committed | cite 07 |
| Idempotency key rules | 07 | The client generates it before the first attempt, and it commits in the same transaction as the effect | cite 07 |
| Two systems cannot share a transaction | 07 | No ordering of two commits is safe; the outbox makes the obligation to publish durable state, turning a permanent loss into a delay | cite 07 |
| Publish-then-delete, never the reverse | 07 | The drain loop chooses at-least-once over at-most-once, because duplicates are recoverable and a lost event is not | cite 07 |
| CAP, FLP, Two Generals by assumption | 07 | The proofs are not the point; the assumptions are the only negotiable part | cite 07 |
| PACELC over CAP | 07 | The else-branch — latency against consistency — applies every day; CAP's branch only during a partition | cite 07 |
| Availability is a product | 07 | Availabilities multiply rather than average; ten dependencies at three nines gives two nines, and better components do not fix it | "p^N (Ch. 07)" |
| Three ways to stop multiplying | 07 | Remove the dependency, make it optional, or make it asynchronous | cite 07 |
| Saga is not rollback | 07 | Compensations are business operations and are visible to customers | cite 07 |
| Five shapes of scale | 08 | Ceiling, knee, superlinear curve, discontinuity, floor — the shape decides the fix | "which shape (Ch. 08)" |
| Amdahl: a ceiling | 08 | The serial fraction bounds speedup regardless of core count; shrink s rather than buying cores | cite 08 |
| USL: returns go negative | 08 | Contention grows with workers and coherency with pairs, so past a peak each added worker lowers throughput | cite 08 |
| Little's Law | 08 | L = λW, near-definitional, true of any stable queue; two knowns give the third | cite 08 |
| Utilization is superlinear | 08 | Wait scales as 1/(1−ρ); there is no cliff at 85%, only a marginal cost that rises from the start | cite 08 |
| Memory hierarchy ~6 orders | 08 | Register to network spans about a million-fold | cite 08 |
| The cache line is the transfer unit | 08 | Cost is set by how much of each fetched line you use, which is layout not algorithm | cite 08 |
| Speed of light as a floor | 08 | Cross-region round trips have a floor no profiling removes; change geography or stop waiting | cite 08 |
| The crossover is not a property of the algorithms | 08 | Where O(n) loses to O(1) is set by comparison cost against hash cost — measure yours | cite 08 |
| Rate of change layers | 09 | Code, schema, published interface, organization — each slower than the last, and the slow ones set the terms | "rate layers (Ch. 09)" |
| Conway / Brooks / Lehman | 09 | Structure mirrors org; adding people to a late project; systems must change | cite 09 |
| Lehman's ratchet | 09 | Complexity rises because adding a case is cheap and local while removing one needs a project | cite 09 |
| Compatibility is add-only | 09 | You may add optional things and relax constraints; you may not remove, rename, retype, or tighten | "add-only (Ch. 09)" |
| A rename is a silent break | 09 | Removals and renames fail without an error; a type change at least fails loudly | cite 09 |
| You cannot deploy other people's software | 09 | The one constraint in the book that cannot be fixed by changing code you control | cite 09 |
| Inverse Conway is a strategy, not a finding | 09 | The observation is established; driving architecture by reshaping teams is not | cite 09 |
| Conway detects mismatch | 09 | Neither tight coupling nor a firm interface is better in itself; the failure is seams landing where the work was divided rather than where the problem divides | cite 09 |
| Conway as a homomorphism | 09 | Every subsystem maps to one design group and every interface to a negotiation; the direction gives many-services-per-team but never many-teams-per-service | cite 09 |
| Conway's mechanism is negotiation | 09 | His own wording: an interface exists where two design groups had to negotiate one. "Communication structure" means who must agree with whom, not who can reach whom | "the ownership asymmetry (Ch. 09)" |
| One team per service, read correctly | 09 | A constraint on who may own a service, not a recipe for how many to have | cite 09 |
| "Late" in Brooks's Law | 09 | Remaining work shorter than the time a new person takes to become useful — not the same as behind schedule | "what late means (Ch. 09)" |
| Long feedback loops | 09 | These decisions cannot be tested, because the evidence arrives after the cost is sunk | cite 09 |
| Compression + constraint tests | 10 | A pattern earns its name by saving words and ruling something out | "the two tests (Ch. 10)" |
| A pattern is not one of the five kinds | 10 | The kinds classify claims; a pattern is a name for a shape, and names are not true or false | cite 10 |
| The tests are independent | 10 | Facade compresses and constrains nothing — four outcomes, not a single axis | cite 10 |
| Compression needs a shared referent | 10 | The saving exists only for a reader who knows the term; a local coinage compresses nothing outside | cite 10 |
| The constraint test is mechanical | 10 | Try to write code the name forbids; if you can and still use the name, it constrains nothing | cite 10 |
| A catalogue is ethnography | 10 | It records shapes that were occurring; read as a checklist it becomes obligations. 04 owns describes-vs-prescribes | cite 10 |
| A name as a search term | 10 | Some names are mediocre descriptions and good indexes into the literature on their failure modes; this is also all a weak name gives a learner | cite 10 |
| Too young to name | 10 | The tests assume you can say what the code does; before that a vague name is honest, and the failure is losing track that it is provisional | cite 10 |
| Directories group by change, names group by shape | 10 | A folder named for a pattern collects code belonging to different features | cite 10 |
| Crossing the ownership line | 11 | The same pattern name is an afternoon's work or a years-long commitment, and "scale" is the wrong word for what separates them | "crossing the line (Ch. 11)" |
| Ownership, not size | 11 | The deciding question is whether you can change the other side; size only correlates, because systems acquire other owners as they grow | "can I change the other side (Ch. 11)" |
| The third option | 11 | At class scale you can change the other side instead of adapting; at system scale that option is gone | cite 11 |
| Shapes are scale-free, Forces are not | 11 | A pattern name transfers the picture and drops the constraints, which were the expensive half | cite 11 |
| Crossing the line adds failure modes | 11 | The same shape acquires loss, duplication, latency, and published commitment — Part II's Laws, one at a time | cite 11 |
| Unchanged by the boundary | 11 | If you cannot state what the pattern would be on the other side, it is a code-organization device — Strategy, Template Method | cite 11 |
| Singleton inverts | 11 | "Exactly one" across machines is leader election, which needs consensus (Ch. 07) | cite 11 |
| Patterns are Forces with a shape | 12 | The durable patterns answer a Force; grouping by Force finds the name from the situation, where a catalogue only finds it from the name | "the Force groups (Ch. 12)" |
| Patterns sorted by Force | 12 | Chapter 03's seven Forces, in chapter 03's order and names; 49 patterns sort, 5 refuse | cite 12 |
| Team size relocates rules | 12 | This Force changes where a rule lives rather than what it is, so it produces few patterns of its own | cite 12 |
| Goal vs Force vs problem shape | 12 | Some patterns answer a goal and some answer the problem's shape, and neither sorts by Force; the test for a goal is whether you can decide to want less of it and stay honest | "the three kinds of input (Ch. 12)" |
| The zero value is a hole in the pattern | 12 | Go gives every struct a zero value and no way to withhold it, so *make illegal states unrepresentable* reaches populated illegal states only; Rust and F# have no such fallback | "the zero-value hole (Ch. 12)" |
| Same Force, several answers | 12 | The Force narrows the field; the intensity picks the answer, and 19 does the choosing | cite 12 |
| Survives-translation test | 13 | Build the same design where the feature exists; the construction disappears and the design does not | "the translation test (Ch. 13)" |
| Norvig's count, with its qualifier | 13 | 16 of 23 "invisible **or simpler**", "for at least some uses" — and three levels, invisible/informal/formal, not two | cite 13; 04 owns dropped quantifiers |
| Constructed vs given | 13 | A pattern is something you construct, a feature something you get; the tell is parts with no counterpart in the problem | "constructed, not given (Ch. 13)" |
| Visitor expired in place | 13 | Java grew sealed types and pattern matching, so the pattern died in the language that entrenched it — not by translation elsewhere | cite 13 |
| The dissolving four are one request | 13 | Command, Strategy, Template Method and Visitor all ask the caller to supply behaviour; one feature answers all four | cite 13 |
| Composite outlives the feature that killed Visitor | 13 | Sum types dissolve one and not the other in the same file, because containment is a claim about the domain (Ch. 12) | cite 13 |
| The translation test is scoped | 13 | Observer dissolves in one process and returns across a machine; run at the wrong scope the test returns a confident wrong answer | cite 13 |
| The test names the target language | 13 | "Visitor is a workaround" is a claim about a pair, and is true and useless if your compiler lacks the feature | cite 13 |
| Decorator is where the test returns no | 13 | Measured in Go the function form is *longer* — 37 lines against 31 — because Go asks nothing for a one-method interface, so there is no ceremony to remove; what function values buy is composability at the call site | "the test returns no (Ch. 13)" |
| Interface width, not language, limits decoration | 13 | Five methods means four forwarding methods no feature removes, because they are not simulating anything (Ch. 05) | cite 13 |
| The scaffold's failure modes move to the feature | 13 | Not *you lose the literature* — decorator gotchas become function-composition gotchas, and order is the big one | cite 13 |
| Name the language, then the design | 13 | "Use Strategy" means an interface and three classes in one language and passing a function in another, so a design document that omits the language has underspecified the work | "name the language first (Ch. 13)" |
| Smuggled verdict | 14 | A term with its judgment inside the noun; using it asserts something while keeping a name's exemption from being defended | "a verdict noun (Ch. 14)" |
| The meaning test | 14 | Apply the term to your own code, then say the code is fine as it stands, and see whether the result means anything — this measures the verdict axis only | "run the meaning test (Ch. 14)" |
| Two axes, not one ladder | 14 | Does the term pick out something inspectable, and does it carry a verdict — independent questions giving four occupied cells | "the two axes (Ch. 14)" |
| Neither shape nor verdict | 14 | *Interesting approach* names nothing and asserts nothing, which is its function; a word from that cell means no design feedback was given | cite 14 |
| Shape-plus-verdict is the damaging cell | 14 | The shape is checkable so the term reads as description, and the verdict rides along unexamined; this is the pattern-vocabulary case | cite 14 |
| A no-shape term reports the reader | 14 | *This smells* is evidence about the reader's pattern-matching rather than a property of the file, and ch 02's classification test has nothing to grip | "no shape to check (Ch. 14)" |
| Marking a hunch makes it usable | 14 | Stated as the speaker's state and converted into a question about why this shape, a hunch becomes the Forces question; unmarked it is a verdict with no subject | cite 14 |
| Two axes give two orderings | 14 | By *can you dissent* the shape-plus-verdict cell is worse; by *is there anything to check* the no-shape cell is worse, and neither is the ordering | cite 14 |
| Anemic drops an antecedent | 14 | Fowler's argument is that you incurred a domain model's costs and got none of its benefits; without the mapping layer and object graph there is no wasted payment to complain about | cite 14 |
| Behaviour is placed, not absent | 14 | What the rule must see — how much data you must be looking at before you can tell whether it holds — decides where a rule can live; 06 owns why the widest case is not a preference | "placed by what the rule must see (Ch. 14)" |
| Verdict nouns are legitimate for Laws | 14 | SQL injection carries its verdict correctly because the condition attached is *always*; *premature optimization* does not, because whether it is premature is a latency-budget question | cite 14 |
| A term's cell is not fixed | 14 | *Monolith* crossed the verdict axis and back while never leaving the top row — the tests measure a term in a community at a time | cite 14 |
| Compressing well is why a verdict noun spreads | 14 | It passes 10's compression test easily, which is what carries it; 15 owns why the qualifier is the part that goes | cite 14 |
| Scope and conditions are one boundary | 15 | Conditions say what must be true (a fact about Forces); scope says which situations the advice reaches. Stating either gives the other, and 15 says scope because it tracks what the wording carries | "the same boundary (Ch. 15)" |
| Scope is carried only where named | 15 | A compressed principle carries its scope only when it names the situation it applies to; where it does not, the reader reconstructs it from surrounding context or takes the widest reading | "the scope does not travel (Ch. 15)" |
| What survives is the actionable half | 15 | Across a verdict noun and an imperative proverb the missing piece differs — an antecedent, a situation — but the survivor is always the part saying what to do, which is why the error never runs the other way | "the actionable half (Ch. 15)" |
| A proverb is a pointer, not a container | 15 | Segoe's form is opaque by design — Pike reads two out and says don't worry whether you understand them; the phrase indexes the teaching rather than replacing it | cite 15 |
| Board proverbs are predictive | 15 | They say what will happen and decline to say whether you want it; several of Pike's took imperative mood instead, and the change was unremarked | cite 15 |
| What proverb one actually means | 15 | Pike glosses rather than coins it — *there is already one proverb you all know* — and the gloss is ownership transfer: hand off the pointer and lose access, not a preference for channels | "the forty seconds (Ch. 15)" |
| Designed to be spoken, not published | 15 | *I think you know them already… ideas you might use to explain to somebody* — the speaker carries the scope, the sentence is the handle, and Pike predicted the page that would carry the handle alone | cite 15 |
| The reader resolves outward | 15 | *Sharing memory* has no fixed extent, so a reader resolved it to any memory two goroutines can reach; self-reported, and the code that prompted it is race-clean | cite 15 |
| Scope gets rebuilt by hand | 15 | `MutexOrChannel`'s table reconstructs Pike's gloss; commenters reconstruct it again; a meta-proverb gets improvised — the repair Sensei's Library institutionalised as a category | cite 15 |
| Scope lives inside or around | 15 | Either in the sentence, or in machinery around the collection; where it is in neither, the reader supplies it | "inside or around (Ch. 15)" |
| The property is in the wording, not the genre | 15 | The single responsibility principle and *don't repeat yourself* were never written to be memorable and name no situation anyway, so the reader answers a question the principle never asked; *money* and *cgo* name one | "past proverbs (Ch. 15)" |
| A named situation is a proxy | 15 | Naming a situation gives *a* scope, not necessarily the right one — syscall and cgo are two proverbs for one condition, so a third platform-specific case has none | "the proxy fits badly (Ch. 15)" |
| Ousterhout, threads, and Google's ban | 15 | Advice whose situation was pthreads in a particular domain arrived as *threads are bad* and held org-wide for years; Pike diagnoses it as generalizing beyond the domain | "the threads ban (Ch. 15)" |
| The source admits the omission | 15 | Pike's 2023 retrospective: the concurrency use cases were server software and they should have said so, and the concurrency/parallelism confusion drove people away | "the retrospective (Ch. 15)" |
| The reading does the damage, not the advice | 15 | Ousterhout was right about pthreads and the Go team right about concurrency; what harmed was a reading neither wrote — which is how the chapter says *harm* without asserting the advice caused it | "the reading, not the advice (Ch. 15)" |
| The test measures checkability, not fit | 15 | Passing it means the principle handed you something to compare your case against, not that it handed you the correct extent | cite 15 |
| Some sentences cannot lose scope | 15 | A proverb whose grammatical subject is a named package has nowhere to drift to — structural, not a claim that those are never misapplied | "check the subject (Ch. 15)" |
| Having the source does not fix it | 15 | Sometimes there is nothing to recover; but all three of Part IV's principles have a source in print and the compressed version travelled anyway, because it arrives complete enough to act on and nothing prompts a check | "having the source is not enough (Ch. 15)" |
| Unconditional advice loses nothing | 15 | gofmt travelled intact because there is no situation in which one consistent format is wrong; 14's boundary in a different costume | cite 15 |
| *Belongs with* names no scope | 16 | *Behaviour belongs with the data it operates on* does not say which entity owns a rule that reads two, so each rule goes to the entity it reads from and the references point both ways | "the sentence does not choose (Ch. 16)" |
| A value cycle is not a type cycle | 16 | Two classes referencing each other may cost nothing; a constructed graph with a back-pointer breaks serialization, equality, hashing and copying on the first call | "the value graph (Ch. 16)" |
| Generic walkers assume a tree | 16 | Serialization, structural equality, hashing and deep copy are written by somebody else and all assume every node is reached once — which is why the cost arrives from outside, late | "what walks this graph (Ch. 16)" |
| The instruction travels, the qualifier does not | 16 | Riel's 2.9 means one key abstraction split in two, which excludes a rule over two entities. The five words carry the instruction alone | "the qualifier stayed behind (Ch. 16)" |
| The author saw it coming and said so | 16 | Riel's introduction calls all sixty *warning bells*, says it is *perfectly valid to state that the heuristic does not apply*, and notes they conflict — written to avoid the fate of *goto considered harmful*, and compressed anyway | "warning bells, not rules (Ch. 16)" |
| Locally applicable, globally evaluable | 16 | The instruction can be followed one method at a time; the cohesion test measures every method at once and the cycle needs two rules resolved to opposite sides — so what compresses is exactly the part that survives being applied alone | cite 16 |
| Mocks assert about mocks | 17 | A mocked test passes when the real constraint has been deleted | cite 17 |
| A test fails only for reasons it can reach | 17 | Every double removes a region of the failure set deliberately; the instruction cannot say whether the rule under test lived in the removed region | "the reasons it can reach (Ch. 17)" |
| A dependency you must double is one you cannot run | 17 | The narrow reading of *dependency* — costs money, needs hardware, belongs to someone else — against the wide one, anything the unit does not compute. Khorikov's sharper version: replace unmanaged dependencies, keep managed ones real, because only the former are observable outside your system | "cannot run, not have not run (Ch. 17)" |
| Mocking is a school, not a default | 17 | Fowler names classical and mockist TDD in 2007 and takes the classical side; *mock your dependencies* is one position stated as if it were the only one, and this chapter argues the other, which has had a name for two decades | "the two schools (Ch. 17)" |
| The bundling is in the teaching, not the canon | 17 | Beck's own statement of the loop mentions no mocking, no isolation and no speed requirement; the fast-tests-therefore-doubles chain is attached to TDD elsewhere | cite 17 |
| A double encodes only known constraints | 17 | A fake is written by the same author as the real rule and agrees with it by construction, so it cannot disagree with a schema that is wrong | cite 17 |
| Mutation is the only mechanical check | 17 | Coverage says a line executed, not that an assertion could fail; breaking the code deliberately is what answers the actual question | "break it and see (Ch. 17)" |
| Ask it at release scope too | 17 | *If this broke in production tomorrow, could we say the cause is not ours because these tests would have caught it* — reaches the dependencies faked below production and the fixture data tidier than anything real | cite 17 |
| Sequencing dropped out of the model | 17 | Fucci et al. decomposed TDD into granularity, uniformity, sequencing and refactoring effort; the test-first fraction explained neither quality nor productivity, while short steady cycles did | "the ordering is not the part (Ch. 17)" |
| The paper states its own conditions | 17 | Every process measured wrote tests — *provided that they keep writing tests*; test-first and test-last are substitutes *at the same level of granularity and uniformity*; gains may be small or uncertain short-term; long-term test-first benefits were not measured. 15's mechanism running on a peer-reviewed finding | cite 17 |
| Granularity is pinned to a green bar | 17 | The study's cycle is the interval between passing test runs, one to forty-nine minutes; read as advice about how often to settle a design, the word has been resolved outward to a scope nobody measured — 15's mechanism running on this chapter's own evidence | "the unit is a green bar (Ch. 17)" |
| The two principles arrive as one practice | 17 | The loop runs at minutes, so the suite must answer in seconds, so the database leaves the test — the granularity carrying the measured benefit is the same granularity that produces the pressure to mock. Standard TDD teaching, not this book's observation | "the loop forces the mock (Ch. 17)" |
| The practice as performed is not the practice as described | 17 | No session in the study ran purely test-first — 87.5% was the maximum, the upper quarter managed about half, and a quarter of subjects refactored in under a tenth of their cycles | "mostly not done as described (Ch. 17)" |
| Test-first couples tests to structure | 17 | The test names an interface before it has settled, so it encodes shape as well as behaviour, and structural change costs test change in proportion | cite 17 |
| Layered packages force exports | 21 | A directory wall requires publishing the helpers it was meant to hide — verified: `undefined: store.scanOrder`, then `go doc` listing the exported helper | cite 21 |
| The same layout costs three amounts | 21 | A directory is a visibility boundary in Go, nothing in C# until assemblies split, and nothing enforced in Python — so *a folder per layer* has a price the instruction never names | "the layout's price varies (Ch. 21)" |
| `internal/` gives back what a split took | 21 | Lowercase already hides a type from clients; `internal/` solves the narrower problem of hiding a package from sibling packages, so reaching for it marks a wall drawn where the language charges | "what internal/ is for (Ch. 21)" |
| The mapping tax | 21 | Two packages cannot share an entity type without one owning the other's API, so each keeps its own and something converts — charged per field, per entity, per boundary, and where drift lives | "the mapping tax (Ch. 21)" |
| Plurality vs sequential replacement | 18 | Two implementations live at once is what an interface is for; replacing one engine with another forever is not, and only the first is a Force | "plurality, not replacement (Ch. 18)" |
| The criterion was dropped, not the scope | 18 | Martin's 1994 paper names stability as the test and an interface as one means; the five words that travel keep the technique and omit the test, because the technique is checkable in review and stability is a claim about the future | "the criterion, not the scope (Ch. 18)" |
| Stability comes from plurality | 18 | The source's reason an abstraction is stable is that many implementations depend on it — so a one-implementation interface fails the principle's own test while carrying its name | "stability needs dependents (Ch. 18)" |
| The caveat was printed and still lost | 18 | Martin's last paragraph says the standard may suit only certain applications and that he would regret unconditional conformance — 15's mechanism on advice whose scope was written down, not merely spoken | cite 18 |
| Insurance that cannot pay out | 18 | An abstraction bought against a future swap is shaped by the engine it was written against, sits in the code layer while the migration is a data problem, and costs the features you already run | "the premium is paid daily (Ch. 18)" |
| Injection is not abstraction | 18 | Passing a dependency in and hiding it behind an interface are two decisions; 05 argues for the first, and only the second is the speculative one | cite 18 |
| The interface publishes a capability | 18 | `GetForUpdate` is on the interface because Postgres has row locks; SQLite cannot implement it at all, so the abstraction promoted one engine's feature to a contract with its own callers | "the method names a capability (Ch. 18)" |
| The lowest common denominator is unknown | 18 | It is the intersection of feature sets for engines nobody has chosen, so it gets approximated by superstition — `for update` is absent from SQLite, `on conflict` is not | cite 18 |
| Premium continuous, payout singular | 18 | The cost is paid daily in small amounts by people who do not know they are paying; the payout is one future event that mostly does not occur, so experience never disconfirms the practice | "the cost and the payout arrive apart (Ch. 18)" |
| *Later* is the tell | 18 | An interface whose reason survives deleting the word *later* is one chapter 05 would defend | cite 18 |
| Force-map method | 19 | Read forces, derive principles, check idioms — in that order | cite 19 |
| FlowCore decision 12 as a worked map | 19 | Deep Get in a repeatable-read transaction: the transaction forced by concurrency and blast radius, four-queries-over-a-join chosen, completion-path locking deferred, and the trigger that would reopen it | cite 19 |
| The order is auditable one way | 19 | Idioms depend on principles, principles on forces, forces on nothing; read that way every step has an input and something that would falsify it, read backwards the chain is consistent and unfalsifiable because it was assembled from the answer | "one direction only (Ch. 19)" |
| The output is a record, not a design | 19 | What it preserves is which decisions were forced and which were chosen — same code either way, but only a forced decision says what would have to change for it to be revisited | "forced or chosen (Ch. 19)" |
| What would have to be true for this to be unnecessary | 19 | The reverse of the derivation, used to detect an inherited principle whose forces are absent; concrete answer means go and check, *it is just good practice* means it arrived without its conditions | "the reverse question (Ch. 19)" |
| Five moves for conflicting forces | 19 | Check the assumed values, look for the third option, prefer the reversible direction, bound the loss rather than estimate odds, then escalate with quantities named. The method converts a conflict into a stated trade; it does not decide it | "the five moves (Ch. 19)" |
| The seven are not a closed list | 19 | They are the forces that recur often enough to name; a situation can hand you a fact that settles a question without appearing on it, and what makes it a force is that it is checkable and says what would change | "not a closed list (Ch. 19)" |
| Reading a force is not measuring one | 19 | Some are countable and some are judgements, and which facts count as forces depends on the decision in front of you. The claim is only that a force is the kind of thing that has an answer — which makes a disagreement winnable, not easy | "forces have answers (Ch. 19)" |
| What a force map adds to an ADR | 19 | Nygard's Context already asks for *the forces at play*; the map adds forced-against-chosen, which says what is safe to touch, and *revisit if*, which is a trigger written before rather than a Status marked after | "what the map adds (Ch. 19)"; 12 owns the ADR pattern |
| Forced, chosen, deferred | 19 | The three lines a map records that code cannot: what had no alternative, what did and could go back, and what is scheduled against a trigger | "forced or chosen (Ch. 19)" |
| The method needs the expertise it looks like it replaces | 19 | Deriving from a force requires already knowing what the force implies and what the options cost; a map filled in by someone who cannot price them is confident and wrong | cite 19 |
| Inherited principles cluster | 19 | A codebase carries the whole set that travelled together, so finding one unforced principle is a reason to look at its neighbours | cite 19 |
| An Idiom's condition is about your surroundings | 21 | A Principle's condition is a fact about your system, looked up by measuring it; an Idiom's is a fact about the language, the tooling, or who will read the code. Both are conditional — they differ in where you look the condition up, which is why an Idiom carried across arrives with nothing to check it against | "the condition is local (Ch. 21)" |
| Obedience rests on a condition too | 21 | *Other people will read this and expect the convention* is a fact about your surroundings of the same kind as the rest, so winning the argument about whether a convention is good does not touch it. Deviation is licensed by a failed condition, not by a better design | "the readers are still there (Ch. 21)" |
| The Idiom/Style line moves by language | 21 | Go makes an identifier's case an access modifier and Python makes indentation syntax, so the two things everyone files under Style are structural there. 02 owns the mechanical test; 21 owns the fact that it lands in a different place per language | "where the line falls (Ch. 21)" |
| One decision, three ecosystems | 21 | Go owns `main` so a container buys nothing; C#'s framework constructs the controllers so it must resolve them; Python has both conditions in different projects and adopts injection where a per-request lifetime is real. 02 owns the demonstration, 21 the explanation | cite 21 |
| An Idiom can be a bad inference from a true condition | 21 | *Cleanup adjacent to acquisition* is true everywhere and does not imply discarding what `Close` returns. Naming the condition is half the test; the other half is checking the convention follows from it, which is what separates an Idiom encoding a mistake from one you merely dislike | "check the inference (Ch. 21)" |
| An Idiom bounds its own designers | 21 | Pike: interfaces coloured the team's thinking for more than a decade, so every proposed polymorphism had to be reconciled with them. Ian Taylor named the problem from early on and Pike ties the difficulty to interfaces being the bedrock — so naming the condition is necessary and not sufficient, which is the claim's boundary | "the Idiom bounded them (Ch. 21)" |
| A deviation, declared and dated | 21 | The early Go compiler in C: reason stated, offence taken, and the reason later expired and the deviation reversed | cite 21 |
| Force profile | 20 | The reading of every force bearing on a system, at least one of them at an intensity outside the ordinary range and staying there; this book's term, built on 03's intensity | "force profile (Ch. 20)" |
| Domain and force profile are independent axes | 20 | Unrelated domains can share a profile — flight simulator, video encoder, trading loop; and one domain can hold opposite profiles — two sales systems whose concurrency readings are nothing alike. The domain name predicts almost nothing, though the reading itself comes from knowing the business | "domain and profile (Ch. 20)" |
| Profile inversions | 20 | The forces a profile pins invert some standard advice | cite 20 |
| Style has no resolving evidence | 22 | A Law has a mechanical consequence, a Principle a Force with a value, an Idiom a machine that acts on the choice — Style has none, because two spellings of one program are the same program. So the argument has no terminating condition and ends by decision rather than conclusion | "nothing settles it (Ch. 22)" |
| A Style argument deposits nothing | 22 | A Force argument that runs six days can end in a measurement everyone now has; a Style argument cannot end that way, so "produces nothing" is literal rather than a complaint about waste | cite 22 |
| Formatting is automatable, naming is not | 22 | `gofmt` ends the brace argument language-wide and has no opinion on whether a parameter is `amounts` or `a`, so naming arguments outlive formatting ones and the enforcement has to keep coming from a person | "no tool picks the name (Ch. 22)" |
| Where being right doesn't matter, being seen to have chosen does | 22 | A short name with a recorded reason and one with nothing behind it are identical on screen; the second is indistinguishable from not having noticed. FlowCore's decision 18 and this book's 49 deviate from one convention for two different reasons, both written down | cite 22 |
| Check both options produce the same program | 22 | Before treating something as Style, confirm the two versions are the same program — if not, it was never Style and the discussion has a fact in it | "same program? (Ch. 22)" |
| Enforcing late costs more than early | 22 | A formatter run over an established codebase rewrites files nobody edited, so `git blame` on those lines names whoever ran it — the same decision is cheap on day one and expensive on day one thousand | cite 22 |
| A profile disagreement does not resolve | 20 | 03 owns the mechanism; 20 owns only the stability. An ordinary force disagreement ends when somebody measures, and two people reading different profiles are each reading a force that will not move in their own system | "stably different (Ch. 20)" |
| A force outside its ordinary range overturns a family | 20 | Not one piece of advice but every piece that depended on the same thing — which is the signature that distinguishes a profile from a special case | cite 20 |
| Fan-in alone is not the smell | 20 | A type depended on by everything is a problem when it also depends on things; an AST has fan-in with no fan-out, which is the stable position | "fan-in with fan-out (Ch. 20)" |
| For a framework, inversion of control is the product | 20 | Not a technique applied — a framework whose control you kept would be a library, and its lifecycle is a Force rather than a convention | "the lifecycle is a Force (Ch. 20)" |
| The seam goes where the profile changes | 20 | Straddling systems are the common case; the boundary belongs where the data crosses, each side keeps its own rules, and the seam is where the bugs are | "where the profile changes (Ch. 20)" |
| Profile knowledge transfers, domain knowledge does not | 20 | Readings and the moves that follow port to an unfamiliar business with the same profile; business knowledge is situational, which is why maritime and civil are different lawyers. Someone arriving carries conclusions — ask for the reading instead | "which transfers (Ch. 20)" |
| Corpus monoculture | 02 | A model has one training distribution and cannot acquire a second, so 02's prescribed cure is unavailable to it | cite 02; argument in `docs/pending-tasks/ai-material.md` |
| The generator cannot see your Forces | 03 | Forces are facts about your situation; a model has the prompt, so the groundwork is skipped by construction | cite 03; argument in `docs/pending-tasks/ai-material.md` |
| The scope was never set | 15 | For generated design nobody ever fixed an extent, so there is no author to ask and no talk to re-watch | "no scope was set (Ch. 15)"; argument in `docs/pending-tasks/ai-material.md` |
| The interview does not improve the answer | 19 | It makes the answer disagreeable-with. The same two decisions exist in generated code as a column default and a v4 constructor, taken by whatever is most common and unmarked; 23 owns that case | "answers somebody can disagree with (Ch. 19)" |
| Fact and decision have different owners | 19 | Grilling's load-bearing line: facts get looked up, decisions get put to the human — steps one and two of the method, separated and given owners, which is what makes the output auditable | "fact or decision (Ch. 19)" |
| Grilling | 19 | An interview that surfaces each decision, with a recommendation, before anything is written; the human supplies the Force that settles it | "grilling (Ch. 19)"; text, provenance and limits in `docs/pending-tasks/ai-material.md` |
| Grilling's limit | 19 | It surfaces decisions the model recognizes as decisions, so it is weakest where the corpus is most uniform | cite 19; argument in `docs/pending-tasks/ai-material.md` |
| Silent defaults | 23 | Generated code states no decisions at all — a taken branch leaves no mark, so review cannot catch what it never suspected | "silent default (Ch. 23)"; argument in `docs/pending-tasks/ai-material.md` |

## Code examples

Each example is used **once**, in its owning chapter.
Reuse requires a different point *and* an explicit callback, never a re-run of the same lesson.

| Example | Owner | What it shows |
|---|---|---|
| Seat reservation race (read-then-update) | 02 | A Law violation: wrong in every language; also reused *within* 02 to show a Force making it inert |
| Manual wiring in Go vs C# | 02 | An Idiom difference: same shape, opposite reception |
| Page-view counter at four concurrency values | 03 | The dial: the fourth position is a different data model, not a hardened third |
| `add column tip not null default 0` | 03 | Durability: a default is a claim about history, and it erases "unknown" permanently |
| `split(8.03, 3)` | 03 | Blast radius: literally the same function, correct behind a dashboard and defective on an invoice |
| Payment method: switch, registry, six layers | 03 | Change frequency plus shape; the six-file version stubbed out so the count is checkable. 18 owns what the boundaries cost |
| `Money` as a comment vs unexported fields | 03 | Team size: the same rule migrates from comment to type system. 12 owns the technique |
| 64-bit id in JSON, read by JavaScript | 03 | Control of callers: same defect, same fix, three different projects |
| Store helper taking `*Catalog` (the cycle) | 05 | One cycle, six detection outcomes across Go/C#/Python/CommonJS — the Law is granularity-blind, the tools are not |
| `querier` / `txQuerier` | 05 | Dependency direction enforced by the type system rather than by directories; `Begin` absent by design |
| Python partially-initialized module | 05 | The runtime face of a cycle: same code, outcome depends on which module was imported first |
| `billing` ↔ `accounts` | 05 | The chapter's running cycle: the change-cost scenario, two-phase construction, `PlanLookup`, and the four currencies |
| Compiler five parts, and three ways to force a line | 05 | An acyclic graph that is not a line; `ast` at the bottom with fan-in 4; and what options A/B/C each cost |
| `Money` vs `IUserService` | 05 | "Depend on abstractions" is about stability, not about the interface keyword |
| `Conn.Raw` vs a disclaimed accessor | 05 | Hiding's bill: the scoped callback keeps a promise the package can hold; the disclaimer does not |
| `LoggingOrderService` vs middleware | 05 | A cross-cutting concern made into a layer; per-method forwarding tax. 13 owns Decorator-as-composition |
| Mutually recursive `parseExpr`/`parseTerm` | 05 | A cycle that costs nothing, because the two were never separate units |
| `Particle` class vs ECS parallel arrays | 05 | Hiding inverted by cache layout — the Principle turns over while the Law holds. 20 may cite for the domain, 08 owns the arithmetic |
| `net/http` `Handler` | 05 | Call up, dependency down — the legitimate version of an apparent violation |
| `completed_at is null` gate | 05 | The lower layer is more capable, so layering doctrine inverts. 06 owns the race it closes |
| Sign-up handler, 50 accounts for one email | 06 | Check-then-act with realistic work in the window; every step individually locked |
| 1000 increments producing 967 | 06 | The lost-update race, and a different wrong answer each run |
| `os.path.exists` then `open` | 06 | TOCTOU in its original filesystem sense — same shape, no database involved |
| 95% of consecutive `Now()` calls identical | 06 | The wall clock cannot order two adjacent events on one machine, before any skew |
| `atomic.AddInt64` vs `count++` | 06 | The one-instruction fix: 1000 exactly, every run |
| Symlink swap between stat and open | 06 | TOCTOU in its original security sense: the bad version silently reads the wrong file; a descriptor binds to the object, a path does not |
| `on conflict do nothing` | 06 | The insert becomes its own check |
| Version-column optimistic update | 06 | Ordering from one authority instead of comparing clocks |
| Lamport counter exchange | 06 | What does order events, and what it still cannot tell you |
| Unique index vs application check | 06 | Only the enforcing layer closes the window |
| Timeout: slow peer vs dead peer | 07 | Identical observations, and the slow peer committed |
| Retry without vs with an idempotency key | 07 | Three deliveries, three charges; three deliveries, one charge |
| Order row then queue publish, vs outbox | 07 | The crash between two commits, and the write that removes the gap |
| p^N availability table | 07 | Ten dependencies at three nines is two nines |
| Outbox table | 07 | Cross-system atomicity is impossible, so you sequence + retry |
| In-process channel vs lost ACK | 04 | Two Generals' two assumptions, and the two different escapes: in-process falsifies one, idempotency drops the requirement. 07 owns the theorem |
| Halting problem vs its folk version | 04 | The theorem forbids a universal decider; termination checking for particular programs is routine |
| `rate` read once at startup | 04 | A definitional claim that either binds or has no cache to act on |
| Go map randomization vs Python dict order | 04 | One regularity, two opposite responses, and a magnitude that moved. 05 owns Hyrum's Law |
| Summing one field across 2M order records vs one column | 08 | 7.1x from where the bytes sit; 120-byte record, 64-byte cache line, no algorithm change. 05 owns the encapsulation argument and keeps `Particle` |
| Pointer-chase latency ladder | 08 | 1.94 ns to 196 ns across working-set sizes, same instruction |
| Nightly report, 20 of 100 minutes un-splittable | 08 | Amdahl worked concretely: a 5x ceiling, and 1024 cores beating 16 by 20% |
| Shared counter vs private counters, 1–64 workers | 08 | Negative scaling measured: throughput falls 4x between two workers and four |
| M/M/1 wait table and the marginal-cost table | 08 | The queue curve, with the 85% "cliff" shown not to exist |
| Linear scan vs map, ints and strings | 08 | The crossover moves with element type — the finding that the expected demo did not show |
| Word counts: Transaction Script, Singleton, Manager | 10 | Compression measured, and the two names with no referent to compress |
| Code each name forbids | 10 | Singleton and Transaction Script forbid something; Facade forbids nothing. 11 owns Facade at scale |
| FastSell: `Receipt` to `LedgerEntry`, both sides owned | 11 | The adapter is the second-best answer — renaming two fields deletes it |
| FastSell moves to Stripe | 11 | The rename is unavailable, so adapting is the only move; six call sites speak Stripe, or one |
| Partial ownership | 11 | An internal service two other teams call — changeable, but not unilaterally |
| Unit of Work / append-only log | 12 | Durability's two shapes, and what each constrains |
| Aggregate / identity map | 12 | The consistency boundary, and one row loaded once |
| Bulkhead / Result types | 12 | Containment in capacity and in the type system |
| Ports and adapters / strangler fig | 12 | Seams where two things move at different rates |
| Batching measured: 1145 ms to 11 ms | 12 | Latency's arithmetic; 08 owns the curve |
| Tolerant reader / consumer-driven contracts | 12 | Surviving a boundary you do not control |
| Delivery states as transition types | 12 | Illegal states in Go, and where the guarantee stops |
| Visitor: Java 1994 vs Java 26 | 13 | 28 lines to 11, same compile-time exhaustiveness |
| Strategy in four languages | 13 | Java class-per-algorithm vs named static methods, Go func field, Python callable — names kept on both sides |
| Fetcher, struct form vs function form | 13 | Decorator measured both ways; the function form is longer |
| loggingStore forwarding four methods | 13 | What decoration costs when the interface is not one function |
| WithLog/WithCache ordering | 13 | Composition order changes behaviour; both orders compile |
| Filesystem tree, Java and Go | 13 | Composite unchanged by the presence or absence of sum types |
| Old client against four API changes | 09 | Add is safe, retype fails loudly, rename fails silently with a zero amount |
| `io/ioutil`, deprecated 2021, running in 2026 | 09 | 175 deprecated declarations in Go's stdlib — the cost of a compatibility promise, kept |
| Brooks n(n−1)/2 and the weekly hours | 09 | A team of 20 spends a quarter of every week staying aligned |
| The 80h vs 988h remaining scenario | 09 | Same team, same hire, opposite answers; break-even sits at the ramp-up length |
| Invoice, named twice | 14 | One file, two accurate descriptions — one a shape, one a conviction |
| Invoice rules at three scopes | 14 | Value on the type, whole-object in the operation, cross-row in the schema, with sqlite refusing the duplicate |
| ParallelMap into a shared slice | 15 | The code a reader thought the proverb forbade; race-clean, because each goroutine writes one index |
| Pike's GopherConAU retrospective, 2023 | 15 | Two admissions of missing scope — Ousterhout's, and his own team's on concurrency |
| Pike's nineteen, split by grammatical subject | 15 | Named packages against ways of working — the control inside one talk |
| Bidirectional Order↔Customer, Java | 16 | Two rules, each placed correctly, leaving an edge each way; `HashSet.add` then throws `StackOverflowError` |
| The same pair flat, Go | 16 | `CustomerID uuid.UUID` instead of `*Customer`: `json.Marshal` refuses the first and encodes the second |
| FlowCore decision 3, pointer wiring rejected | 16 | The identifier trade priced both ways: `json.Marshal`, `reflect.DeepEqual` and offline construction bought; a query per route and cross-definition integrity moved to composite FKs, paid |
| `Money.plus` with a currency check | 16 | The boundary — a rule reading one entity, where the advice is right and moving it out would remove the enforcement |
| Deleted constraint, passing mock test | 17 | `unique` dropped from the schema: the database-backed test fails, the mocked one still passes |
| A fixture that starts at the asserted state | 17 | Account created `active`, so the verification test is satisfied before `verify` runs; gutting the method leaves it passing, and one word in the fixture restores the failure |
| FlowCore decision 37, as corroboration | 17 | The same shape in a real system — one status for both terminal actions, caught by mutation, the fifth in one iteration, with a comment above it recording the weakness |
| Fucci et al.'s four dimensions | 17 | GRA, UNI, SEQ, REF and which survived model selection |
| Store split into a package | 21 | One package with a private `scanOrder`, then split: `undefined: store.scanOrder`, exported to compile, and published by `go doc`. Paired with the same split in Python, which runs — `store._scan_order` reachable across the boundary, no bill |
| `defer file.Close()` | 21 | The convention discards an `error` return. Structural: `Close` reports a failed final write, and a network filesystem surfaces it there and nowhere earlier |
| One function, three formattings and two namings | 22 | All print 1745; `gofmt` rewrites the hand-formatted one and reports nothing about `a` versus `amounts`. Binaries differ, because Go's line table records position — which is why 02's test is about behaviour |
| `(order_id,)` versus `(order_id)` | 22 | The same trailing comma that is Style in a list is the tuple in a one-element tuple; sqlite3 answers `ProgrammingError: parameters are of unsupported type`. The boundary: one of the two apparent options never existed |
| Unindented Python function body | 21 | `IndentationError` — formatting as syntax, against Go and C# where the formatter settles it |
| `NewOrders(*sql.DB)` against `NewOrders(Repository)` | 18 | Injection and abstraction as two separable decisions, with 05 arguing only for the first |
| `select … for update` refused by SQLite | 18 | `OperationalError: near "for": syntax error`, beside `on conflict` succeeding — the second implementation cannot satisfy the interface, and the lowest common denominator is not the obvious list |

## Deliberate repetition

Only these ideas may appear more than once, because the book's structure depends on them:

- **The kind of the current material** — stated where it does work, in the claim or in *Why the claim holds*, not as a standing opener. Chapters no longer carry an epigraph.
- **The mandatory boundary section** — every chapter has one. It is a section, not a repeated argument.
- **FlowCore as running example** — appears across Parts II and V, but each appearance must show a *different* facet.
