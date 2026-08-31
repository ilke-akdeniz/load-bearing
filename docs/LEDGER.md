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
| The five kinds of claim | cjx4 | Many claims about software are one of five kinds — Law, Force, Principle, Idiom, Style — and the kind sets its authority. Four are advice and form a ladder; Force is not, so there are four levels and five kinds | "a Law / an Idiom" |
| Classification test | cjx4 | Five questions that place a claim in one of the five kinds | "run the test" |
| Why the kinds get confused | cjx4 | Four mechanisms: tone doesn't vary with authority; advocacy compresses; monoculture makes Idioms feel universal; teaching leaves the training wheels on | one clause, cite |
| The Idiom/Style line is mechanical | cjx4 | The compiler or the runtime acts on an Idiom and neither can see a Style. What is held constant is narrow and named — what the program produces when it succeeds — so failure modes, setup effort and how much the compiler can check are all free to differ. Ecosystem-specificity does not discriminate, because plenty of Style is local. 7nkn owns the fact that the line falls in a different place in each language | "the machine can see it" |
| Law inert vs Principle wrong | cjx4 | A Force decides whether a Law *binds*; it decides whether a Principle is *right* | one clause, cite |
| Forces as inputs | f4m5 | Forces are properties of the situation, not advice | "the Force is X" |
| A Force is a dial, not a switch | f4m5 | A Force has an **intensity** — how hard it presses on the design, which is not how large the number is; the design changes several times across the range, each answer discarding the last | "read the intensity" |
| The seven Forces | f4m5 | Concurrency, durability of the medium, blast radius, change frequency and shape, team size and turnover, latency budget, control of callers | name the Force, cite |
| Concurrency | f4m5 | How many at once, and do they touch the same state — it binds where writers collide, not where they coexist | cite; mdbn owns the races |
| Durability of the medium | f4m5 | How long what this writes outlives the code that wrote it | cite; rjf9 owns published compatibility |
| Blast radius | f4m5 | When it is wrong, what happens and who finds out — decides how much prevention is worth | cite |
| Change frequency and shape | f4m5 | How often, and how many places must change with it | cite; agjy owns fan-in pricing |
| Team size and turnover | f4m5 | How many must agree, and how many will still be here — the rule migrates comment → review → type system | cite |
| Latency budget | f4m5 | What the budget is, and what fraction one mechanism costs | cite; 637f owns the arithmetic |
| Control of the callers | f4m5 | Can I change every call site, and would I know if I broke one — three values, not two | cite; agjy owns what it implies for exposure |
| Reversibility decides deferral | f4m5 | Two questions — does waiting spoil it, is it cheap today — giving three cases: defer, take it now, or admit you are betting | "the reversibility rule" |
| What `internal/` is, glossed | f4m5 | A package under `internal/` cannot be imported from outside its module, given while using FlowCore's decision 1 as the non-expiring deferral. 21 puts the same decision to the opposite use — what the directory is actually for — and cites this rather than re-explaining the mechanism | "`internal/`" |
| Strict is the undoable direction | f4m5 | Under uncertainty prefer the decision you can walk back, which is usually the stricter one | cite |
| Risk vs unmeasured Force | f4m5 | An unmeasured Force has an instrument and a trigger; a risk has neither, so the answer is bounding the cost rather than estimating harder | cite |
| Shape of scale | f4m5 | "High scale" names no design — steady load, bursts, and data volume are different situations sharing a vocabulary | cite |
| Forces move on their own clock | f4m5 | Team size, client count, and row count change without a commit, invalidating Principles nobody revisits | cite |
| The disagreement is about the Force, not the Principle | f4m5 | Two people arguing about a Principle have usually already agreed about it and differ about the situation it is conditioned on; stating the Force ends the argument or relocates it to something answerable. 02 introduces it in one sentence as a symptom and hands off; no other chapter restates the mechanism | "the disagreement is about the Force" |
| Three kinds of Law | q5c6 | Theorem, definition, empirical law — named, never lettered, and not ranked | "a theorem / a definitional claim" |
| One kind, its moves | q5c6 | Theorem: falsify an assumption, or stop needing the conclusion. Definition: check whether the words apply. Empirical: measure it where you are | cite |
| Two escapes from a theorem | q5c6 | Arrange for one of its assumptions not to hold, or stop needing the theorem's conclusion — never argue with the conclusion | cite |
| Regularity vs magnitude | q5c6 | A measurement is not a law; an empirical law is a regularity across systems whose magnitude varies between them | cite |
| Kind is not importance | q5c6 | The kind says how firmly a claim is true, not how much it bears on your program | cite |
| Describes vs prescribes | q5c6 | A Law describes what happens; a Principle prescribes. Only a Principle can become bad advice | "describes vs prescribes" |
| Theorem and folk version share a name | q5c6 | The folk version has usually dropped a quantifier or a condition — halting problem forbids a universal decider, not any decision | cite |
| The falsification question | q5c6 | "What would have to be true for this to be false?" — nothing / nothing but it may not apply / a measurement | cite |
| Acyclic dependency | agjy | A cycle makes two components one unit of comprehension, test, and change | "the Direction Rule" |
| What a cycle actually costs | agjy | The damage is denominated in future change, not in wrong output — which is why it accumulates unnoticed | cite |
| Injection vs inversion | agjy | Injection decides who constructs; inversion decides who declares the interface, and only inversion turns an arrow around | cite |
| Two-phase construction | agjy | `a := &A{}; b := &B{a}; a.b = b` is the construction site admitting the cycle | cite |
| Dependency damage compounds | agjy | A missing test is a static cost; a cycle spreads to everything touching either end | one clause, cite |
| Cycle detection is granularity-bound | agjy | Each toolchain checks the boundaries it happens to have; the damage exists at all of them | cite |
| "Layered" is three claims | agjy | Acyclicity (Law) + the line shape (Principle) + the folder taxonomy (Idiom), under one name | "the three claims" |
| Layering as ranks | agjy | Strict layering assigns every part a rank and forbids reaching past the one beneath it | one clause, cite |
| Layer ≠ directory | agjy | A layer is a rule about call direction; a folder is neither necessary nor sufficient for it | cite; 4jk6 owns what folders *cost*, and no chapter may say the physical forms enforce the same thing — 18's claim is that they do not |
| Cost of change scales with dependents | agjy | Change cost is proportional to fan-in, and is paid on every change | cite |
| Stability, not indirection | agjy | "Depend on abstractions" means put what changes least at the bottom; an interface is not automatically that | cite |
| Internal vs external dependent count | agjy | Inside the repo `grep` gives you the number; once published it is unknown and growing | cite |
| From direction to surface | agjy | Cycles are about which way edges point; hiding is about how many edges exist at all | cite |
| Information hiding / Hyrum | agjy | What is observable will be depended upon | cite |
| DI does not contradict hiding | agjy | Injection is a module declining to hold decisions that belong elsewhere; the composition root holds them instead | cite |
| Hiding's condition | agjy | Information hiding is a Principle conditional on not controlling your callers | cite; the Force itself is 03's |
| Export surface as liability | agjy | Every exported identifier is a contract; the surface is an inventory of what you can no longer change | cite |
| A disclaimer is not a boundary | agjy | An "unsupported" export is still an export — Hyrum's Law does not read comments | cite |
| Claim two, loose vs strict | agjy | "Dependencies flow downward" is claim one restated; the strict rank rule is what most systems fail | cite |
| Graph vocabulary | agjy | Arrow = depends on; fan-in = who breaks if you change; bottom = high fan-in, low fan-out | cite |
| The graph exists at every size | agjy | Functions through services; size changes what detects a violation, not whether the Law binds | cite |
| Four ways to break a cycle | agjy | Interface / event / third module / identifier — four different bills, chosen deliberately | cite |
| Dependency inversion | agjy | The call may go up while the dependency goes down, because both parties point at an interface at the bottom | cite |
| Lower layer more capable | agjy | Layering doctrine assumes the layer below is dumber; when it is more capable, "keep logic out" inverts | cite |
| There is no shared now | mdbn | A check reports the past; across machines there is no agreed ordering at all | "no shared now" |
| Three conditions for a race | mdbn | Another writer, a decision that depends on the read, and a rule spanning data you did not hold still — all three, or nothing to fix | cite |
| The three ordinary fixes | mdbn | One operation; let the data-holder enforce; or do not check and handle the failure | cite |
| Lock the span, not the steps | mdbn | The fix is not more locking but locking the right span | cite |
| One authority beats many clocks | mdbn | Optimistic concurrency on a version counter needs no clock; the database is the single source of order | cite |
| Check-then-act / TOCTOU | mdbn | Between the check and the act, the world moved | "TOCTOU" |
| Locking each step is not locking the sequence | mdbn | Individually safe operations do not compose into a safe rule | cite |
| The window is as wide as the work in it | mdbn | The same defect is rare on an idle machine and constant under load | cite |
| Only the lock-holder enforces | mdbn | A rule over rows you haven't read can't be enforced by code that hasn't read them | cite |
| The app check is the message, not the guarantee | mdbn | Keep it for the error text; never keep it as the enforcement | cite |
| Two ways to remove a race | mdbn | Remove the sharing or remove the mutability; concurrency is the term you cannot give up | cite |
| Single-writer principle | mdbn | One writer means nothing can interleave, so coordination cost falls to zero | "single writer" |
| Clocks do not order events | mdbn | Wall clocks lack the resolution locally and agreement globally; counters order, clocks do not | cite |
| Lamport vs vector clocks | mdbn | Lamport preserves causality but cannot detect concurrency; vector clocks can, at a cost that grows with nodes | cite |
| Coordination does not compose | mdbn | Two correct locked operations are not one correct operation | cite |
| Slow is indistinguishable from dead | 49yh | The root of the impossibility results: you must decide on information you cannot obtain | "slow vs dead" |
| Exactly-once impossible | 49yh | Two Generals ⇒ at-least-once plus idempotency | cite |
| Every timeout is a guess | 49yh | The observation is identical whether the peer is slow or dead, and the slow one may have committed | cite |
| Idempotency key rules | 49yh | The client generates it before the first attempt, and it commits in the same transaction as the effect | cite |
| Two systems cannot share a transaction | 49yh | No ordering of two commits is safe; the outbox makes the obligation to publish durable state, turning a permanent loss into a delay | cite |
| Publish-then-delete, never the reverse | 49yh | The drain loop chooses at-least-once over at-most-once, because duplicates are recoverable and a lost event is not | cite |
| CAP, FLP, Two Generals by assumption | 49yh | The proofs are not the point; the assumptions are the only negotiable part. CAP's *Consistency* is linearizability — every read returns the most recent write, as though one copy had ever existed — which is much narrower than the everyday word | cite |
| PACELC over CAP | 49yh | The else-branch — latency against consistency — applies every day; CAP's branch only during a partition | cite |
| Availability is a product | 49yh | Availabilities multiply rather than average; ten dependencies at three nines gives two nines, and better components do not fix it | "p^N" |
| Three ways to stop multiplying | 49yh | Remove the dependency, make it optional, or make it asynchronous | cite |
| Saga is not rollback | 49yh | Compensations are business operations and are visible to customers | cite |
| Five shapes of scale | 637f | Ceiling, knee, superlinear curve, discontinuity, floor — the shape decides the fix | "which shape" |
| Amdahl: a ceiling | 637f | The serial fraction bounds speedup regardless of core count; shrink s rather than buying cores | cite |
| USL: returns go negative | 637f | Contention grows with workers and coherency with pairs, so past a peak each added worker lowers throughput | cite |
| Little's Law | 637f | L = λW, near-definitional, true of any stable queue; two knowns give the third | cite |
| Utilization is superlinear | 637f | Wait scales as 1/(1−ρ); there is no cliff at 85%, only a marginal cost that rises from the start | cite |
| Memory hierarchy ~6 orders | 637f | Register to network spans about a million-fold | cite |
| The cache line is the transfer unit | 637f | Cost is set by how much of each fetched line you use, which is layout not algorithm | cite |
| Speed of light as a floor | 637f | Cross-region round trips have a floor no profiling removes; change geography or stop waiting | cite |
| The crossover is not a property of the algorithms | 637f | Where O(n) loses to O(1) is set by comparison cost against hash cost — measure yours | cite |
| Rate of change layers | rjf9 | Code, schema, published interface, organization — each slower than the last, and the slow ones set the terms | "rate layers" |
| Conway / Brooks / Lehman | rjf9 | Structure mirrors org; adding people to a late project; systems must change | cite |
| Lehman's ratchet | rjf9 | Complexity rises because adding a case is cheap and local while removing one needs a project | cite |
| Compatibility is add-only | rjf9 | You may add optional things and relax constraints; you may not remove, rename, retype, or tighten | "add-only" |
| A rename is a silent break | rjf9 | Removals and renames fail without an error; a type change at least fails loudly | cite |
| Compatibility adopted rather than suffered | rjf9 | Pike prices Go's 1.0 lock-down from the inside: uptake, and it blocks feature-itis — a language accumulating features each defensible alone. Same irreversibility the chapter treats as a burden, working as a filter: anything added is added permanently, so a proposal must be worth keeping for the life of the language. The difference from the section above is timing, not the constraint | "bought rather than incurred" |
| You cannot deploy other people's software | rjf9 | The one constraint in the book that cannot be fixed by changing code you control | cite |
| Inverse Conway is a strategy, not a finding | rjf9 | The observation is established; driving architecture by reshaping teams is not | cite |
| Conway detects mismatch | rjf9 | Neither tight coupling nor a firm interface is better in itself; the failure is seams landing where the work was divided rather than where the problem divides | cite |
| Conway as a homomorphism | rjf9 | Every subsystem maps to one design group and every interface to a negotiation; the direction gives many-services-per-team but never many-teams-per-service | cite |
| Conway's mechanism is negotiation | rjf9 | His own wording: an interface exists where two design groups had to negotiate one. "Communication structure" means who must agree with whom, not who can reach whom | "the ownership asymmetry" |
| One team per service, read correctly | rjf9 | A constraint on who may own a service, not a recipe for how many to have | cite |
| "Late" in Brooks's Law | rjf9 | Remaining work shorter than the time a new person takes to become useful — not the same as behind schedule | "what late means" |
| Long feedback loops | rjf9 | These decisions cannot be tested, because the evidence arrives after the cost is sunk | cite |
| Compression + constraint tests | 3xzc | A pattern earns its name by saving words and ruling something out | "the two tests" |
| A pattern is not one of the five kinds | 3xzc | The kinds classify claims; a pattern is a name for a shape, and names are not true or false | cite |
| The tests are independent | 3xzc | Facade compresses and constrains nothing — four outcomes, not a single axis | cite |
| Compression needs a shared referent | 3xzc | The saving exists only for a reader who knows the term; a local coinage compresses nothing outside | cite |
| The constraint test is mechanical | 3xzc | Try to write code the name forbids; if you can and still use the name, it constrains nothing | cite |
| A catalogue is ethnography | 3xzc | It records shapes that were occurring; read as a checklist it becomes obligations. q5c6 owns describes-vs-prescribes | cite |
| A name as a search term | 3xzc | Some names are mediocre descriptions and good indexes into the literature on their failure modes; this is also all a weak name gives a learner | cite |
| Too young to name | 3xzc | The tests assume you can say what the code does; before that a vague name is honest, and the failure is losing track that it is provisional | cite |
| Directories group by change, names group by shape | 3xzc | A folder named for a pattern collects code belonging to different features | cite |
| Crossing the ownership line | r8dw | The same pattern name is an afternoon's work or a years-long commitment, and "scale" is the wrong word for what separates them | "crossing the line" |
| Ownership, not size | r8dw | The deciding question is whether you can change the other side; size only correlates, because systems acquire other owners as they grow | "can I change the other side" |
| The third option | r8dw | At class scale you can change the other side instead of adapting; at system scale that option is gone | cite |
| Shapes are scale-free, Forces are not | r8dw | A pattern name transfers the picture and drops the constraints, which were the expensive half | cite |
| Crossing the line adds failure modes | r8dw | The same shape acquires loss, duplication, latency, and published commitment — Part II's Laws, one at a time | cite |
| Unchanged by the boundary | r8dw | If you cannot state what the pattern would be on the other side, it is a code-organization device — Strategy, Template Method | cite |
| Singleton inverts | r8dw | "Exactly one" across machines is leader election, which needs consensus | cite |
| Patterns are Forces with a shape | us2k | The durable patterns answer a Force; grouping by Force finds the name from the situation, where a catalogue only finds it from the name | "the Force groups" |
| Patterns sorted by Force | us2k | Chapter f4m5's seven Forces, in chapter f4m5's order and names; 49 patterns sort, 5 refuse | cite |
| Team size relocates rules | us2k | This Force changes where a rule lives rather than what it is, so it produces few patterns of its own | cite |
| Goal vs Force vs problem shape | us2k | Some patterns answer a goal and some answer the problem's shape, and neither sorts by Force; the test for a goal is whether you can decide to want less of it and stay honest | "the three kinds of input" |
| The zero value is a hole in the pattern | us2k | Go gives every struct a zero value and no way to withhold it, so *make illegal states unrepresentable* reaches populated illegal states only; Rust and F# have no such fallback | "the zero-value hole" |
| Same Force, several answers | us2k | The Force narrows the field; the intensity picks the answer, and 19 does the choosing | cite |
| Survives-translation test | esqm | Build the same design where the feature exists; the construction disappears and the design does not | "the translation test" |
| Norvig's count, with its qualifier | esqm | 16 of 23 "invisible **or simpler**", "for at least some uses" — and three levels, invisible/informal/formal, not two | cite; q5c6 owns dropped quantifiers |
| Constructed vs given | esqm | A pattern is something you construct, a feature something you get; the tell is parts with no counterpart in the problem | "constructed, not given" |
| Visitor expired in place | esqm | Java grew sealed types and pattern matching, so the pattern died in the language that entrenched it — not by translation elsewhere | cite |
| The dissolving four are one request | esqm | Command, Strategy, Template Method and Visitor all ask the caller to supply behaviour; one feature answers all four | cite |
| Composite outlives the feature that killed Visitor | esqm | Sum types dissolve one and not the other in the same file, because containment is a claim about the domain | cite |
| The translation test is scoped | esqm | Observer dissolves in one process and returns across a machine; run at the wrong scope the test returns a confident wrong answer | cite |
| The test names the target language | esqm | "Visitor is a workaround" is a claim about a pair, and is true and useless if your compiler lacks the feature | cite |
| Decorator is where the test returns no | esqm | Measured in Go the function form is *longer* — 37 lines against 31 — because Go asks nothing for a one-method interface, so there is no ceremony to remove; what function values buy is composability at the call site | "the test returns no" |
| Interface width, not language, limits decoration | esqm | Five methods means four forwarding methods no feature removes, because they are not simulating anything | cite |
| The scaffold's failure modes move to the feature | esqm | Not *you lose the literature* — decorator gotchas become function-composition gotchas, and order is the big one | cite |
| Name the language, then the design | esqm | "Use Strategy" means an interface and three classes in one language and passing a function in another, so a design document that omits the language has underspecified the work | "name the language first" |
| Smuggled verdict | 8y69 | A term with its judgment inside the noun; using it asserts something while keeping a name's exemption from being defended | "a verdict noun" |
| The meaning test | 8y69 | Apply the term to your own code, then say the code is fine as it stands, and see whether the result means anything — this measures the verdict axis only | "run the meaning test" |
| Two axes, not one ladder | 8y69 | Does the term pick out something inspectable, and does it carry a verdict — independent questions giving four occupied cells | "the two axes" |
| Neither shape nor verdict | 8y69 | *Interesting approach* names nothing and asserts nothing, which is its function; a word from that cell means no design feedback was given | cite |
| Shape-plus-verdict is the damaging cell | 8y69 | The shape is checkable so the term reads as description, and the verdict rides along unexamined; this is the pattern-vocabulary case | cite |
| A no-shape term reports the reader | 8y69 | *This smells* is evidence about the reader's pattern-matching rather than a property of the file, and ch 02's classification test has nothing to grip | "no shape to check" |
| Marking a hunch makes it usable | 8y69 | Stated as the speaker's state and converted into a question about why this shape, a hunch becomes the Forces question; unmarked it is a verdict with no subject | cite |
| Two axes give two orderings | 8y69 | By *can you dissent* the shape-plus-verdict cell is worse; by *is there anything to check* the no-shape cell is worse, and neither is the ordering | cite |
| Anemic drops an antecedent | 8y69 | Fowler's argument is that you incurred a domain model's costs and got none of its benefits; without the mapping layer and object graph there is no wasted payment to complain about | cite |
| Behaviour is placed, not absent | 8y69 | What the rule must see — how much data you must be looking at before you can tell whether it holds — decides where a rule can live; mdbn owns why the widest case is not a preference | "placed by what the rule must see" |
| Verdict nouns are legitimate for Laws | 8y69 | SQL injection carries its verdict correctly because the condition attached is *always*; *premature optimization* does not, because whether it is premature is a latency-budget question | cite |
| A term's cell is not fixed | 8y69 | *Monolith* crossed the verdict axis and back while never leaving the top row — the tests measure a term in a community at a time | cite |
| Compressing well is why a verdict noun spreads | 8y69 | It passes 09's compression test easily, which is what carries it; b86v owns why the qualifier is the part that goes | cite |
| Scope and conditions are one boundary | b86v | Conditions say what must be true (a fact about Forces); scope says which situations the advice reaches. Stating either gives the other, and 15 says scope because it tracks what the wording carries | "the same boundary" |
| Scope is carried only where named | b86v | A compressed principle carries its scope only when it names the situation it applies to; where it does not, the reader reconstructs it from surrounding context or takes the widest reading | "the scope does not travel" |
| What survives is the actionable half | b86v | Across a verdict noun and an imperative proverb the missing piece differs — an antecedent, a situation — but the survivor is always the part saying what to do, which is why the error never runs the other way | "the actionable half" |
| A proverb is a pointer, not a container | b86v | Segoe's form is opaque by design — Pike reads two out and says don't worry whether you understand them; the phrase indexes the teaching rather than replacing it | cite |
| Board proverbs are predictive | b86v | They say what will happen and decline to say whether you want it; several of Pike's took imperative mood instead, and the change was unremarked | cite |
| What proverb one actually means | b86v | Pike glosses rather than coins it — *there is already one proverb you all know* — and the gloss is ownership transfer: hand off the pointer and lose access, not a preference for channels | "the forty seconds" |
| Designed to be spoken, not published | b86v | *I think you know them already… ideas you might use to explain to somebody* — the speaker carries the scope, the sentence is the handle, and Pike predicted the page that would carry the handle alone | cite |
| The reader resolves outward | b86v | *Sharing memory* has no fixed extent, so a reader resolved it to any memory two goroutines can reach; self-reported, and the code that prompted it is race-clean | cite |
| Scope gets rebuilt by hand | b86v | `MutexOrChannel`'s table reconstructs Pike's gloss; commenters reconstruct it again; a meta-proverb gets improvised — the repair Sensei's Library institutionalised as a category | cite |
| Scope lives inside or around | b86v | Either in the sentence, or in machinery around the collection; where it is in neither, the reader supplies it | "inside or around" |
| The property is in the wording, not the genre | b86v | The single responsibility principle and *don't repeat yourself* were never written to be memorable and name no situation anyway, so the reader answers a question the principle never asked; *money* and *cgo* name one | "past proverbs" |
| A named situation is a proxy | b86v | Naming a situation gives *a* scope, not necessarily the right one — syscall and cgo are two proverbs for one condition, so a third platform-specific case has none | "the proxy fits badly" |
| Ousterhout, threads, and Google's ban | b86v | Advice whose situation was pthreads in a particular domain arrived as *threads are bad* and held org-wide for years; Pike diagnoses it as generalizing beyond the domain | "the threads ban" |
| The source admits the omission | b86v | Pike's 2023 retrospective: the concurrency use cases were server software and they should have said so, and the concurrency/parallelism confusion drove people away | "the retrospective" |
| The reading does the damage, not the advice | b86v | Ousterhout was right about pthreads and the Go team right about concurrency; what harmed was a reading neither wrote — which is how the chapter says *harm* without asserting the advice caused it | "the reading, not the advice" |
| The test measures checkability, not fit | b86v | Passing it means the principle handed you something to compare your case against, not that it handed you the correct extent | cite |
| Some sentences cannot lose scope | b86v | A proverb whose grammatical subject is a named package has nowhere to drift to — structural, not a claim that those are never misapplied | "check the subject" |
| Having the source does not fix it | b86v | Sometimes there is nothing to recover; but all three of Part IV's principles have a source in print and the compressed version travelled anyway, because it arrives complete enough to act on and nothing prompts a check | "having the source is not enough" |
| Unconditional advice loses nothing | b86v | gofmt travelled intact because there is no situation in which one consistent format is wrong; 14's boundary in a different costume | cite |
| *Belongs with* names no scope | z47a | *Behaviour belongs with the data it operates on* does not say which entity owns a rule that reads two, so each rule goes to the entity it reads from and the references point both ways | "the sentence does not choose" |
| A value cycle is not a type cycle | z47a | Two classes referencing each other may cost nothing; a constructed graph with a back-pointer breaks serialization, equality, hashing and copying on the first call | "the value graph" |
| Generic walkers assume a tree | z47a | Serialization, structural equality, hashing and deep copy are written by somebody else and all assume every node is reached once — which is why the cost arrives from outside, late | "what walks this graph" |
| The instruction travels, the qualifier does not | z47a | Riel's 2.9 means one key abstraction split in two, which excludes a rule over two entities. The five words carry the instruction alone | "the qualifier stayed behind" |
| The author saw it coming and said so | z47a | Riel's introduction calls all sixty *warning bells*, says it is *perfectly valid to state that the heuristic does not apply*, and notes they conflict — written to avoid the fate of *goto considered harmful*, and compressed anyway | "warning bells, not rules" |
| Locally applicable, globally evaluable | z47a | The instruction can be followed one method at a time; the cohesion test measures every method at once and the cycle needs two rules resolved to opposite sides — so what compresses is exactly the part that survives being applied alone | cite |
| Mocks assert about mocks | u8eu | A mocked test passes when the real constraint has been deleted | cite |
| A test fails only for reasons it can reach | u8eu | Every double removes a region of the failure set deliberately; the instruction cannot say whether the rule under test lived in the removed region | "the reasons it can reach" |
| A dependency you must double is one you cannot run | u8eu | The narrow reading of *dependency* — costs money, needs hardware, belongs to someone else — against the wide one, anything the unit does not compute. Khorikov's sharper version: replace unmanaged dependencies, keep managed ones real, because only the former are observable outside your system | "cannot run, not have not run" |
| Mocking is a school, not a default | u8eu | Fowler names classical and mockist TDD in 2007 and takes the classical side; *mock your dependencies* is one position stated as if it were the only one, and this chapter argues the other, which has had a name for two decades | "the two schools" |
| The bundling is in the teaching, not the canon | u8eu | Beck's own statement of the loop mentions no mocking, no isolation and no speed requirement; the fast-tests-therefore-doubles chain is attached to TDD elsewhere | cite |
| A double encodes only known constraints | u8eu | A fake is written by the same author as the real rule and agrees with it by construction, so it cannot disagree with a schema that is wrong | cite |
| Mutation is the only mechanical check | u8eu | Coverage says a line executed, not that an assertion could fail; breaking the code deliberately is what answers the actual question | "break it and see" |
| Ask it at release scope too | u8eu | *If this broke in production tomorrow, could we say the cause is not ours because these tests would have caught it* — reaches the dependencies faked below production and the fixture data tidier than anything real | cite |
| Sequencing dropped out of the model | u8eu | Fucci et al. decomposed TDD into granularity, uniformity, sequencing and refactoring effort; the test-first fraction explained neither quality nor productivity, while short steady cycles did | "the ordering is not the part" |
| The paper states its own conditions | u8eu | Every process measured wrote tests — *provided that they keep writing tests*; test-first and test-last are substitutes *at the same level of granularity and uniformity*; gains may be small or uncertain short-term; long-term test-first benefits were not measured. 15's mechanism running on a peer-reviewed finding | cite |
| Granularity is pinned to a green bar | u8eu | The study's cycle is the interval between passing test runs, one to forty-nine minutes; read as advice about how often to settle a design, the word has been resolved outward to a scope nobody measured — 15's mechanism running on this chapter's own evidence | "the unit is a green bar" |
| The two principles arrive as one practice | u8eu | The loop runs at minutes, so the suite must answer in seconds, so the database leaves the test — the granularity carrying the measured benefit is the same granularity that produces the pressure to mock. Standard TDD teaching, not this book's observation | "the loop forces the mock" |
| The practice as performed is not the practice as described | u8eu | No session in the study ran purely test-first — 87.5% was the maximum, the upper quarter managed about half, and a quarter of subjects refactored in under a tenth of their cycles | "mostly not done as described" |
| Test-first couples tests to structure | u8eu | The test names an interface before it has settled, so it encodes shape as well as behaviour, and structural change costs test change in proportion | cite |
| Layered packages force exports | 7nkn | A directory wall requires publishing the helpers it was meant to hide — verified: `undefined: store.scanOrder`, then `go doc` listing the exported helper | cite |
| The same layout costs three amounts | 7nkn | A directory is a visibility boundary in Go, nothing in C# until assemblies split, and nothing enforced in Python — so *a folder per layer* has a price the instruction never names | "the layout's price varies" |
| `internal/` gives back what a split took | 7nkn | Lowercase already hides a type from clients; `internal/` solves the narrower problem of hiding a package from sibling packages, so reaching for it marks a wall drawn where the language charges | "what internal/ is for" |
| The mapping tax | 7nkn | Two packages cannot share an entity type without one owning the other's API, so each keeps its own and something converts — charged per field, per entity, per boundary, and where drift lives | "the mapping tax" |
| Plurality vs sequential replacement | 4jk6 | Two implementations live at once is what an interface is for; replacing one engine with another forever is not, and only the first is a Force | "plurality, not replacement" |
| The criterion was dropped, not the scope | 4jk6 | Martin's 1994 paper names stability as the test and an interface as one means; the five words that travel keep the technique and omit the test, because the technique is checkable in review and stability is a claim about the future | "the criterion, not the scope" |
| Stability comes from plurality | 4jk6 | The source's reason an abstraction is stable is that many implementations depend on it — so a one-implementation interface fails the principle's own test while carrying its name | "stability needs dependents" |
| The caveat was printed and still lost | 4jk6 | Martin's last paragraph says the standard may suit only certain applications and that he would regret unconditional conformance — 15's mechanism on advice whose scope was written down, not merely spoken | cite |
| Insurance that cannot pay out | 4jk6 | An abstraction bought against a future swap is shaped by the engine it was written against, sits in the code layer while the migration is a data problem, and costs the features you already run | "the premium is paid daily" |
| Legitimate uses of an interface | agjy | Narrowing what a consumer can reach — `querier` with `Begin` absent — breaking a cycle, and declaring a seam whose shape the consumer owns. 4jk6 says in its own text that agjy owns these, and that one implementation with no planned second can be right | cite |
| One implementation is not speculative | 4jk6 | The claim is about interfaces justified by a future substitution, not about interfaces. One implementation and no planned second can be correct, and the test is whether the reason survives without the word *later* | "without the word later" |
| Injection is not abstraction | 4jk6 | Passing a dependency in and hiding it behind an interface are two decisions; 05 argues for the first, and only the second is the speculative one | cite |
| The interface publishes a capability | 4jk6 | `GetForUpdate` is on the interface because Postgres has row locks; SQLite cannot implement it at all, so the abstraction promoted one engine's feature to a contract with its own callers | "the method names a capability" |
| The lowest common denominator is unknown | 4jk6 | It is the intersection of feature sets for engines nobody has chosen, so it gets approximated by superstition — `for update` is absent from SQLite, `on conflict` is not | cite |
| Premium continuous, payout singular | 4jk6 | The cost is paid daily in small amounts by people who do not know they are paying; the payout is one future event that mostly does not occur, so experience never disconfirms the practice | "the cost and the payout arrive apart" |
| *Later* is the tell | 4jk6 | An interface whose reason survives deleting the word *later* is one chapter agjy would defend | cite |
| Force-map method | r37x | Read forces, derive principles, check idioms — in that order | cite |
| FlowCore decision 12 as a worked map | r37x | Deep Get in a repeatable-read transaction: the transaction forced by concurrency and blast radius, four-queries-over-a-join chosen, completion-path locking deferred, and the trigger that would reopen it | cite |
| The order is auditable one way | r37x | Idioms depend on principles, principles on forces, forces on nothing; read that way every step has an input and something that would falsify it, read backwards the chain is consistent and unfalsifiable because it was assembled from the answer | "one direction only" |
| The output is a record, not a design | r37x | What it preserves is which decisions were forced and which were chosen — same code either way, but only a forced decision says what would have to change for it to be revisited | "forced or chosen" |
| What would have to be true for this to be unnecessary | r37x | The reverse of the derivation, used to detect an inherited principle whose forces are absent; concrete answer means go and check, *it is just good practice* means it arrived without its conditions | "the reverse question" |
| Five moves for conflicting forces | r37x | Check the assumed values, look for the third option, prefer the reversible direction, bound the loss rather than estimate odds, then escalate with quantities named. The method converts a conflict into a stated trade; it does not decide it | "the five moves" |
| The seven are not a closed list | r37x | They are the forces that recur often enough to name; a situation can hand you a fact that settles a question without appearing on it, and what makes it a force is that it is checkable and says what would change | "not a closed list" |
| Reading a force is not measuring one | r37x | Some are countable and some are judgements, and which facts count as forces depends on the decision in front of you. The claim is only that a force is the kind of thing that has an answer — which makes a disagreement winnable, not easy | "forces have answers" |
| What a force map adds to an ADR | r37x | Nygard's Context already asks for *the forces at play*; the map adds forced-against-chosen, which says what is safe to touch, and *revisit if*, which is a trigger written before rather than a Status marked after | "what the map adds"; us2k owns the ADR pattern |
| Forced, chosen, deferred | r37x | The three lines a map records that code cannot: what had no alternative, what did and could go back, and what is scheduled against a trigger | "forced or chosen" |
| The method needs the expertise it looks like it replaces | r37x | Deriving from a force requires already knowing what the force implies and what the options cost; a map filled in by someone who cannot price them is confident and wrong | cite |
| Inherited principles cluster | r37x | A codebase carries the whole set that travelled together, so finding one unforced principle is a reason to look at its neighbours | cite |
| An Idiom's condition is about your surroundings | 7nkn | A Principle's condition is a fact about your system, looked up by measuring it; an Idiom's is a fact about the language, the tooling, or who will read the code. Both are conditional — they differ in where you look the condition up, which is why an Idiom carried across arrives with nothing to check it against | "the condition is local" |
| Obedience rests on a condition too | 7nkn | *Other people will read this and expect the convention* is a fact about your surroundings of the same kind as the rest, so winning the argument about whether a convention is good does not touch it. Deviation is licensed by a failed condition, not by a better design | "the readers are still there" |
| The Idiom/Style line moves by language | 7nkn | Go makes an identifier's case an access modifier and Python makes indentation syntax, so the two things everyone files under Style are structural there. cjx4 owns the mechanical test; 7nkn owns the fact that it lands in a different place per language | "where the line falls" |
| One decision, three ecosystems | 7nkn | Go owns `main` so a container buys nothing; C#'s framework constructs the controllers so it must resolve them; Python has both conditions in different projects and adopts injection where a per-request lifetime is real. cjx4 owns the demonstration, 21 the explanation | cite |
| An Idiom can be a bad inference from a true condition | 7nkn | *Cleanup adjacent to acquisition* is true everywhere and does not imply discarding what `Close` returns. Naming the condition is half the test; the other half is checking the convention follows from it, which is what separates an Idiom encoding a mistake from one you merely dislike | "check the inference" |
| An Idiom bounds its own designers | 7nkn | Pike: interfaces coloured the team's thinking for more than a decade, so every proposed polymorphism had to be reconciled with them. Ian Taylor named the problem from early on and Pike ties the difficulty to interfaces being the bedrock — so naming the condition is necessary and not sufficient, which is the claim's boundary | "the Idiom bounded them" |
| A deviation, declared and dated | 7nkn | The early Go compiler in C: reason stated, offence taken, and the reason later expired and the deviation reversed | cite |
| Force profile | dnkz | The reading of every force bearing on a system, at least one of them at an intensity outside the ordinary range and staying there; this book's term, built on 03's intensity | "force profile" |
| Domain and force profile are independent axes | dnkz | Unrelated domains can share a profile — flight simulator, video encoder, trading loop; and one domain can hold opposite profiles — two sales systems whose concurrency readings are nothing alike. The domain name predicts almost nothing, though the reading itself comes from knowing the business | "domain and profile" |
| Profile inversions | dnkz | The forces a profile pins invert some standard advice | cite |
| Style has no resolving evidence | 9rng | A Law has a mechanical consequence, a Principle a Force with a value, an Idiom a machine that acts on the choice — Style has none, because two spellings of one program are the same program. So the argument has no terminating condition and ends by decision rather than conclusion | "nothing settles it" |
| A Style argument deposits nothing | 9rng | A Force argument that runs six days can end in a measurement everyone now has; a Style argument cannot end that way, so "produces nothing" is literal rather than a complaint about waste | cite |
| Formatting is automatable, naming is not | 9rng | `gofmt` ends the brace argument language-wide and has no opinion on whether a parameter is `amounts` or `a`, so naming arguments outlive formatting ones and the enforcement has to keep coming from a person | "no tool picks the name" |
| Where being right doesn't matter, being seen to have chosen does | 9rng | A short name with a recorded reason and one with nothing behind it are identical on screen; the second is indistinguishable from not having noticed. FlowCore's decision 18 and this book's 49 deviate from one convention for two different reasons, both written down | cite |
| Check both options produce the same program | 9rng | Before treating something as Style, confirm the two versions are the same program — if not, it was never Style and the discussion has a fact in it | "same program?" |
| Enforcing late costs more than early | 9rng | A formatter run over an established codebase rewrites files nobody edited, so `git blame` on those lines names whoever ran it — the same decision is cheap on day one and expensive on day one thousand | cite |
| A profile disagreement does not resolve | dnkz | f4m5 owns the mechanism; dnkz owns only the stability. An ordinary force disagreement ends when somebody measures, and two people reading different profiles are each reading a force that will not move in their own system | "stably different" |
| A force outside its ordinary range overturns a family | dnkz | Not one piece of advice but every piece that depended on the same thing — which is the signature that distinguishes a profile from a special case | cite |
| Fan-in alone is not the smell | dnkz | A type depended on by everything is a problem when it also depends on things; an AST has fan-in with no fan-out, which is the stable position | "fan-in with fan-out" |
| For a framework, inversion of control is the product | dnkz | Not a technique applied — a framework whose control you kept would be a library, and its lifecycle is a Force rather than a convention | "the lifecycle is a Force" |
| The seam goes where the profile changes | dnkz | Straddling systems are the common case; the boundary belongs where the data crosses, each side keeps its own rules, and the seam is where the bugs are | "where the profile changes" |
| Profile knowledge transfers, domain knowledge does not | dnkz | Readings and the moves that follow port to an unfamiliar business with the same profile; business knowledge is situational, which is why maritime and civil are different lawyers. Someone arriving carries conclusions — ask for the reading instead | "which transfers" |
| The team-size Force at its extreme | f4m5 | An AI coding agent answers *how many will still be here* with nobody: present for no conversation, keeping nothing between sessions, its output arriving at a volume review was not sized for. The comment → review habit → type system migration is forced harder and sooner, skipping the middle, because what a comment relies on is somebody remembering. Forces reach the agent only as far as a prompt carried them, since they are facts about your situation | "forced harder and sooner" |
| The interview does not improve the answer | r37x | It makes the answer disagreeable-with. The same two decisions exist in generated code as a column default and a v4 constructor, taken by whatever is most common and unmarked; at4r owns that case | "answers somebody can disagree with" |
| Fact and decision have different owners | at4r | Grilling's load-bearing line: facts get looked up, decisions get put to the human — steps one and two of the method, separated and given owners, which is what makes the output auditable | "fact or decision" |
| Grilling | at4r | An interview that surfaces each decision, with a recommendation, before anything is written; the human supplies the Force that settles it | "grilling" |
| Grilling's first limit | at4r | It surfaces decisions the agent recognizes as decisions, so it is weakest where the corpus is most uniform | cite |
| What persists is text | at4r | A forward pass discards its activations and every persistence mechanism these tools have stores tokens, so there is never a replay — which is why the chapter rests on that rather than on the contested question of whether stated reasoning reflects computation | "what persists is text" |
| Three cases, and the middle one does the damage | at4r | Same session with the reasoning written out is retrieval of what was said; same session with nothing written is a fresh computation on overlapping input, correlated and not a recollection; a new session has only the artifact. All three read alike from outside | "the middle case" |
| Behaviour is re-derivable, reasons are not | at4r | Asking what the code does is reading and works at any time; asking why this shape was chosen is not, because it was never in the artifact and no amount of freshness puts it there | cite |
| No author to ask, no talk to re-watch | at4r | 14's repair is to go back to the source and rebuild the scope, and that needs a source. A corpus default has none, which is what makes it the limiting case of a folk remedy rather than one more instance of it | cite |
| Folk remedy | at4r | Advice applied far outside the context it was made for, which stays misapplied because nobody rebuilds its scope — the author's term, not standard. *Depend on abstractions* is the worked case; a corpus default is the purest instance, since there nobody knows a scope existed | "a folk remedy"; 15 hands it over |
| Grilling's second limit: granularity | at4r | The interview only reaches decisions at the scale of the request, so asking for a whole application never separates out the trade-offs that live inside its fourth piece. FlowCore's slices, with scope written into standing instructions — *do not build ahead into these* — are the countermeasure | "the granularity limit" |
| An entry is reusable to the extent it records why | at4r | *Full-word identifiers everywhere* transfers nothing; *abbreviations must be decoded rather than read* can be checked against new readers and kept or dropped. A conclusion does not travel, a conclusion with its condition does — 15's mechanism running forwards | "why, not what" |
| Grilling leaves two artifacts | at4r | The log, and a person who now holds the trade-off. Accepting every recommendation is still not rubber-stamping if you understood what was being chosen between — and an agent keeps nothing between sessions, so the connection to next month's question has to live in a person or a document | "the second artifact" |
| The record is the only copy | at4r | For a human author memory covers the gap while it fades; remove the memory and there is no interval in which the reason is available and undocumented, so the record is not a backup of anything | cite |
| Unrecorded decisions compound | at4r | Each one constrains the next change without saying so, and removing anything requires knowing what it was for — which ends in requests that can only be negative, *fix this, do not break that* | "fix this, don't break that" |
| Self-enforcing beats recorded | at4r | Where a decision can be written into something that refuses to be violated, that is worth more than a record, because enforcement does not depend on anyone reading anything. Narrow: most design decisions are judgements, not invariants | "make it self-enforcing" |
| Silent defaults | at4r | Generated code states no decisions at all — a taken branch leaves no mark, so review cannot catch what it never suspected | "silent default" |
| Individual ownership | 3fjx | Every artifact has one name against it, and that name belongs to whoever holds the most context on the subject it is about. The two halves are one claim: ownership works *because* it tracks context, so a name without the context is a signature rather than an owner | "one name against it" |
| What makes it architecture | 3fjx | Not the diagram and not the choice of stack — both are consequences and either can be produced without anybody deciding anything. What makes it architecture is that the trade-offs were named, the Forces they answer were read, and one person is answerable for the choice | cite |
| The four artifacts before code | 3fjx | The rules, the force map, the solution, the code. Each described by its form, its ideal owner, and what that owner must be able to do — by capability, never by title | "the four artifacts" |
| The solution is missing from the method | 3fjx | r37x says in terms that its output *is not a design*, and no chapter supplies one. Between the constraints and the code sits the act of choosing what to build, and it is the artifact with the smallest pool of possible owners and the one most often given to a room | "constraints are not an answer" |
| An artifact with no name is made by nobody | 3fjx | A shared assignment supplies neither of the two things the work needs: a defensible answer to *why were you doing that instead of the ticket*, and whose judgement settles it | "assigned to the team" |
| Code is the artifact nobody assigns to a room | 3fjx | Not because it deserves an owner more, but because a shared assignment is *visibly* impossible there. Upstream the absence is invisible until much later, which is where the failure lives | cite |
| A meeting sorts by whether the decision has an owner | 3fjx | Called to decide something nobody owns, it is a decision assigned to a room and rooms do not decide; called to unblock somebody who already owns it, it does work and stops. Same slot, different object | "does the decision have an owner" |
| An artifact that needs two names | 3fjx | Where the artifact is a negotiation between two owners, rjf9's Conway mechanism, one owner is one side imposing — and what comes back is compliance and a workaround. Both names are still individuals | cite |
| Context and authority in different people | 3fjx | Give the artifact to the context and it is not honoured; give it to the authority and it is wrong. The chapter cannot resolve it; what the claim buys is that the split becomes sayable. Length of service is the proxy organisations reach for because it is the one written down | "the split" |
| Concentration is division of labour | 3fjx | If context accumulates where it is used, the same few people own the same few subjects, which is what an expert is. A team where everyone owns everything has no expert in anything | "not a defect" |
| A handoff does not transfer context | 3fjx | What four years produced is having been wrong and finding out why; what moves in a fortnight is the file layout and the table names. The honest responses are growing a second expert slowly or pricing the concentration | "the fortnight handoff" |

## Code examples

Each example is used **once**, in its owning chapter.
Reuse requires a different point *and* an explicit callback, never a re-run of the same lesson.

| Example | Owner | What it shows |
|---|---|---|
| Seat reservation race (read-then-update) | cjx4 | A Law violation: wrong in every language; also reused *within* 02 to show a Force making it inert |
| Manual wiring in Go vs C# | cjx4 | An Idiom difference: same shape, opposite reception |
| Page-view counter at four concurrency values | f4m5 | The dial: the fourth position is a different data model, not a hardened third |
| `add column tip not null default 0` | f4m5 | Durability: a default is a claim about history, and it erases "unknown" permanently |
| `split(8.03, 3)` | f4m5 | Blast radius: literally the same function, correct behind a dashboard and defective on an invoice |
| Payment method: switch, registry, six layers | f4m5 | Change frequency plus shape; the six-file version stubbed out so the count is checkable. 4jk6 owns what the boundaries cost |
| `Money` as a comment vs unexported fields | f4m5 | Team size: the same rule migrates from comment to type system. us2k owns the technique |
| 64-bit id in JSON, read by JavaScript | f4m5 | Control of callers: same defect, same fix, three different projects |
| Store helper taking `*Catalog` (the cycle) | agjy | One cycle, six detection outcomes across Go/C#/Python/CommonJS — the Law is granularity-blind, the tools are not |
| `querier` / `txQuerier` | agjy | Dependency direction enforced by the type system rather than by directories; `Begin` absent by design |
| Python partially-initialized module | agjy | The runtime face of a cycle: same code, outcome depends on which module was imported first |
| `billing` ↔ `accounts` | agjy | The chapter's running cycle: the change-cost scenario, two-phase construction, `PlanLookup`, and the four currencies |
| Compiler five parts, and three ways to force a line | agjy | An acyclic graph that is not a line; `ast` at the bottom with fan-in 4; and what options A/B/C each cost |
| `Money` vs `IUserService` | agjy | "Depend on abstractions" is about stability, not about the interface keyword |
| `Conn.Raw` vs a disclaimed accessor | agjy | Hiding's bill: the scoped callback keeps a promise the package can hold; the disclaimer does not |
| `LoggingOrderService` vs middleware | agjy | A cross-cutting concern made into a layer; per-method forwarding tax. esqm owns Decorator-as-composition |
| Mutually recursive `parseExpr`/`parseTerm` | agjy | A cycle that costs nothing, because the two were never separate units |
| `Particle` class vs ECS parallel arrays | agjy | Hiding inverted by cache layout — the Principle turns over while the Law holds. dnkz may cite for the domain, 637f owns the arithmetic |
| `net/http` `Handler` | agjy | Call up, dependency down — the legitimate version of an apparent violation |
| `completed_at is null` gate | agjy | The lower layer is more capable, so layering doctrine inverts. mdbn owns the race it closes |
| Sign-up handler, 50 accounts for one email | mdbn | Check-then-act with realistic work in the window; every step individually locked |
| 1000 increments producing 967 | mdbn | The lost-update race, and a different wrong answer each run |
| `os.path.exists` then `open` | mdbn | TOCTOU in its original filesystem sense — same shape, no database involved |
| 95% of consecutive `Now()` calls identical | mdbn | The wall clock cannot order two adjacent events on one machine, before any skew |
| `atomic.AddInt64` vs `count++` | mdbn | The one-instruction fix: 1000 exactly, every run |
| Symlink swap between stat and open | mdbn | TOCTOU in its original security sense: the bad version silently reads the wrong file; a descriptor binds to the object, a path does not |
| `on conflict do nothing` | mdbn | The insert becomes its own check |
| Version-column optimistic update | mdbn | Ordering from one authority instead of comparing clocks |
| Lamport counter exchange | mdbn | What does order events, and what it still cannot tell you |
| Unique index vs application check | mdbn | Only the enforcing layer closes the window |
| Timeout: slow peer vs dead peer | 49yh | Identical observations, and the slow peer committed |
| Retry without vs with an idempotency key | 49yh | Three deliveries, three charges; three deliveries, one charge |
| Order row then queue publish, vs outbox | 49yh | The crash between two commits, and the write that removes the gap |
| p^N availability table | 49yh | Ten dependencies at three nines is two nines |
| Outbox table | 49yh | Cross-system atomicity is impossible, so you sequence + retry |
| In-process channel vs lost ACK | q5c6 | Two Generals' two assumptions, and the two different escapes: in-process falsifies one, idempotency drops the requirement. 49yh owns the theorem |
| Halting problem vs its folk version | q5c6 | The theorem forbids a universal decider; termination checking for particular programs is routine |
| `rate` read once at startup | q5c6 | A definitional claim that either binds or has no cache to act on |
| Go map randomization vs Python dict order | q5c6 | One regularity, two opposite responses, and a magnitude that moved. agjy owns Hyrum's Law |
| Summing one field across 2M order records vs one column | 637f | 7.1x from where the bytes sit; 120-byte record, 64-byte cache line, no algorithm change. agjy owns the encapsulation argument and keeps `Particle` |
| Pointer-chase latency ladder | 637f | 1.94 ns to 196 ns across working-set sizes, same instruction |
| Nightly report, 20 of 100 minutes un-splittable | 637f | Amdahl worked concretely: a 5x ceiling, and 1024 cores beating 16 by 20% |
| Shared counter vs private counters, 1–64 workers | 637f | Negative scaling measured: throughput falls 4x between two workers and four |
| M/M/1 wait table and the marginal-cost table | 637f | The queue curve, with the 85% "cliff" shown not to exist |
| Linear scan vs map, ints and strings | 637f | The crossover moves with element type — the finding that the expected demo did not show |
| Word counts: Transaction Script, Singleton, Manager | 3xzc | Compression measured, and the two names with no referent to compress |
| Code each name forbids | 3xzc | Singleton and Transaction Script forbid something; Facade forbids nothing. r8dw owns Facade at scale |
| FastSell: `Receipt` to `LedgerEntry`, both sides owned | r8dw | The adapter is the second-best answer — renaming two fields deletes it |
| FastSell moves to Stripe | r8dw | The rename is unavailable, so adapting is the only move; six call sites speak Stripe, or one |
| Partial ownership | r8dw | An internal service two other teams call — changeable, but not unilaterally |
| Unit of Work / append-only log | us2k | Durability's two shapes, and what each constrains |
| Aggregate / identity map | us2k | The consistency boundary, and one row loaded once |
| Bulkhead / Result types | us2k | Containment in capacity and in the type system |
| Ports and adapters / strangler fig | us2k | Seams where two things move at different rates |
| Batching measured: 1145 ms to 11 ms | us2k | Latency's arithmetic; 637f owns the curve |
| Tolerant reader / consumer-driven contracts | us2k | Surviving a boundary you do not control |
| Delivery states as transition types | us2k | Illegal states in Go, and where the guarantee stops |
| Visitor: Java 1994 vs Java 26 | esqm | 28 lines to 11, same compile-time exhaustiveness |
| Strategy in four languages | esqm | Java class-per-algorithm vs named static methods, Go func field, Python callable — names kept on both sides |
| Fetcher, struct form vs function form | esqm | Decorator measured both ways; the function form is longer |
| loggingStore forwarding four methods | esqm | What decoration costs when the interface is not one function |
| WithLog/WithCache ordering | esqm | Composition order changes behaviour; both orders compile |
| Filesystem tree, Java and Go | esqm | Composite unchanged by the presence or absence of sum types |
| Old client against four API changes | rjf9 | Add is safe, retype fails loudly, rename fails silently with a zero amount |
| `io/ioutil`, deprecated 2021, running in 2026 | rjf9 | 175 deprecated declarations in Go's stdlib — the cost of a compatibility promise, kept |
| Brooks n(n−1)/2 and the weekly hours | rjf9 | A team of 20 spends a quarter of every week staying aligned |
| The 80h vs 988h remaining scenario | rjf9 | Same team, same hire, opposite answers; break-even sits at the ramp-up length |
| Invoice, named twice | 8y69 | One file, two accurate descriptions — one a shape, one a conviction |
| Invoice rules at three scopes | 8y69 | Value on the type, whole-object in the operation, cross-row in the schema, with sqlite refusing the duplicate |
| ParallelMap into a shared slice | b86v | The code a reader thought the proverb forbade; race-clean, because each goroutine writes one index |
| Pike's GopherConAU retrospective, 2023 | b86v | Two admissions of missing scope — Ousterhout's, and his own team's on concurrency |
| Pike's nineteen, split by grammatical subject | b86v | Named packages against ways of working — the control inside one talk |
| Bidirectional Order↔Customer, Java | z47a | Two rules, each placed correctly, leaving an edge each way; `HashSet.add` then throws `StackOverflowError` |
| The same pair flat, Go | z47a | `CustomerID uuid.UUID` instead of `*Customer`: `json.Marshal` refuses the first and encodes the second |
| FlowCore decision 3, pointer wiring rejected | z47a | The identifier trade priced both ways: `json.Marshal`, `reflect.DeepEqual` and offline construction bought; a query per route and cross-definition integrity moved to composite FKs, paid |
| `Money.plus` with a currency check | z47a | The boundary — a rule reading one entity, where the advice is right and moving it out would remove the enforcement |
| Deleted constraint, passing mock test | u8eu | `unique` dropped from the schema: the database-backed test fails, the mocked one still passes |
| A fixture that starts at the asserted state | u8eu | Account created `active`, so the verification test is satisfied before `verify` runs; gutting the method leaves it passing, and one word in the fixture restores the failure |
| FlowCore decision 37, as corroboration | u8eu | The same shape in a real system — one status for both terminal actions, caught by mutation, the fifth in one iteration, with a comment above it recording the weakness |
| Fucci et al.'s four dimensions | u8eu | Granularity, uniformity, sequencing and refactoring, each given with a plain gloss — three survived the analysis, and sequencing, the test-first share, predicted neither outcome |
| `get_definition` with and without its transaction | at4r | Both run; with a concurrent edit between the two reads the second returns revision 1 of a definition with three steps, which was never saved. 19 maps the same FlowCore decision as a log entry; this shows it in the code, where none of the reasoning is visible |
| `UNIQUE (definition_id, active)` | at4r | The boundary: the decision is in the schema, so violating it raises `IntegrityError` at the moment of the change and nobody needs to remember why |
| Store split into a package | 7nkn | One package with a private `scanOrder`, then split: `undefined: store.scanOrder`, exported to compile, and published by `go doc`. Paired with the same split in Python, which runs — `store._scan_order` reachable across the boundary, no bill |
| `defer file.Close()` | 7nkn | The convention discards an `error` return. Structural: `Close` reports a failed final write, and a network filesystem surfaces it there and nowhere earlier |
| One function, three formattings and two namings | 9rng | All print 1745; `gofmt` rewrites the hand-formatted one and reports nothing about `a` versus `amounts`. Binaries differ, because Go's line table records position — which is why 02's test is about behaviour |
| `(order_id,)` versus `(order_id)` | 9rng | The same trailing comma that is Style in a list is the tuple in a one-element tuple; sqlite3 answers `ProgrammingError: parameters are of unsupported type`. The boundary: one of the two apparent options never existed |
| Unindented Python function body | 7nkn | `IndentationError` — formatting as syntax, against Go and C# where the formatter settles it |
| `NewOrders(*sql.DB)` against `NewOrders(Repository)` | 4jk6 | Injection and abstraction as two separable decisions, with 05 arguing only for the first |
| `select … for update` refused by SQLite | 4jk6 | `OperationalError: near "for": syntax error`, beside `on conflict` succeeding — the second implementation cannot satisfy the interface, and the lowest common denominator is not the obvious list |
| The junior developer and the export ticket | 3fjx | Same developer, same two weeks, different software — ten minutes of Force reading handed over as one paragraph |
| "The team is responsible for designing feature X" | 3fjx | One engineer's reasoning after a shared assignment, and why none of it is unreasonable |
| The export-format meeting, twice | 3fjx | Six people and a document owned by the meeting; one owner, fifteen minutes booked, nine used |

## Deliberate repetition

Only these ideas may appear more than once, because the book's structure depends on them:

- **The kind of the current material** — stated where it does work, in the claim or in *Why the claim holds*, not as a standing opener. Chapters no longer carry an epigraph.
- **The mandatory boundary section** — every chapter has one. It is a section, not a repeated argument.
- **FlowCore as running example** — appears across Parts II, IV, and V, but each appearance must show a *different* facet.
