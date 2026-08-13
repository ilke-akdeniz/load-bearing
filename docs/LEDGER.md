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
| The five levels | 02 | Advice is one of five kinds — Law, Force, Principle, Idiom, Style — and the kind sets its authority | "a Law / an Idiom (Ch. 02)" |
| Classification test | 02 | Five questions that place a claim in one of the five kinds | "run the test (Ch. 02)" |
| Why the kinds get confused | 02 | Tone doesn't vary with authority; advocacy compresses; monoculture makes Idioms feel universal | one clause, cite 02 |
| Law inert vs Principle wrong | 02 | A Force decides whether a Law *binds*; it decides whether a Principle is *right* | one clause, cite 02 |
| Forces as inputs | 03 | Forces are properties of the situation, not advice | "the Force is X (Ch. 03)" |
| A Force is a dial, not a switch | 03 | Forces have values; the design changes several times across the range, each answer discarding the last | "read the value (Ch. 03)" |
| The seven Forces | 03 | Concurrency, durability of the medium, blast radius, change frequency and shape, team size and turnover, latency budget, control of callers | name the Force, cite 03 |
| Concurrency | 03 | How many at once, and do they touch the same state — it binds where writers collide, not where they coexist | cite 03; 06 owns the races |
| Durability of the medium | 03 | How long what this writes outlives the code that wrote it | cite 03; 09 owns published compatibility |
| Blast radius | 03 | When it is wrong, what happens and who finds out — decides how much prevention is worth | cite 03 |
| Change frequency and shape | 03 | How often, and how many places must change with it | cite 03; 05 owns fan-in pricing |
| Team size and turnover | 03 | How many must agree, and how many will still be here — the rule migrates comment → review → type system | cite 03 |
| Latency budget | 03 | What the budget is, and what fraction one mechanism costs | cite 03; 08 owns the arithmetic |
| Control of the callers | 03 | Can I change every call site, and would I know if I broke one — three values, not two | cite 03; 05 owns what it implies for exposure |
| Reversibility decides deferral | 03 | Two questions — does waiting spoil it, is it cheap today — giving three cases: defer, take it now, or admit you are betting | "the reversibility rule (Ch. 03)" |
| Strict is the undoable direction | 03 | Under uncertainty prefer the decision you can walk back, which is usually the stricter one | cite 03 |
| Risk vs unmeasured Force | 03 | An unmeasured Force has an instrument and a trigger; a risk has neither, so the answer is bounding the cost rather than estimating harder | cite 03 |
| Shape of scale | 03 | "High scale" names no design — steady load, bursts, and data volume are different situations sharing a vocabulary | cite 03 |
| Forces move on their own clock | 03 | Team size, client count, and row count change without a commit, invalidating Principles nobody revisits | cite 03 |
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
| Layer ≠ directory | 05 | A layer is a rule about call direction; a folder is neither necessary nor sufficient for it | cite 05; 18 owns what folders *cost* |
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
| Conway's mechanism is ownership | 09 | Dividing the work is already a decomposition, and a boundary between owners needs agreement to move while one inside an owner does not | "the ownership asymmetry (Ch. 09)" |
| One team per service, read correctly | 09 | A constraint on who may own a service, not a recipe for how many to have | cite 09 |
| "Late" in Brooks's Law | 09 | Remaining work shorter than the time a new person takes to become useful — not the same as behind schedule | "what late means (Ch. 09)" |
| Long feedback loops | 09 | These decisions cannot be tested, because the evidence arrives after the cost is sunk | cite 09 |
| Compression + constraint tests | 10 | A pattern earns its name by saving words and ruling something out | cite 10 |
| The scale test | 11 | The same name is trivial at class scale and load-bearing at system scale | "scale test (Ch. 11)" |
| Survives-translation test | 13 | If it disappears when you change language, it was a workaround | cite 13 |
| Smuggled verdict | 14 | Vocabulary arriving with its conclusion attached | cite 14 |
| Principle→movement mechanism | 15 | Observation gets a name, name gets a community, community forgets the conditions | cite 15 |
| Mocks assert about mocks | 17 | A mocked test passes when the real constraint has been deleted | cite 17 |
| Layered packages force exports | 18 | A directory wall requires publishing the helpers it was meant to hide | cite 18 |
| Force-map method | 19 | Read forces, derive principles, check idioms — in that order | cite 19 |
| Domain inversions | 20 | Each domain's dominant force inverts some standard advice | cite 20 |
| Corpus monoculture | 02 | A model has one training distribution and cannot acquire a second, so 02's prescribed cure is unavailable to it | cite 02; argument in `docs/ai-material.md` |
| The generator cannot see your Forces | 03 | Forces are facts about your situation; a model has the prompt, so the groundwork is skipped by construction | cite 03; argument in `docs/ai-material.md` |
| The conditions were never derived | 15 | For generated design the answer to 15's test is not that conditions were forgotten but that none were formed | "no derivation (Ch. 15)"; argument in `docs/ai-material.md` |
| Grilling | 19 | An interview that surfaces each decision, with a recommendation, before anything is written; the human supplies the Force that settles it | "grilling (Ch. 19)"; text, provenance and limits in `docs/ai-material.md` |
| Grilling's limit | 19 | It surfaces decisions the model recognizes as decisions, so it is weakest where the corpus is most uniform | cite 19; argument in `docs/ai-material.md` |
| Silent defaults | 23 | Generated code states no decisions at all — a taken branch leaves no mark, so review cannot catch what it never suspected | "silent default (Ch. 23)"; argument in `docs/ai-material.md` |

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
| Adapter at class vs system scale | 11 | The scale test |
| GoF collapse in 4 languages | 13 | Survives-translation test |
| Old client against four API changes | 09 | Add is safe, retype fails loudly, rename fails silently with a zero amount |
| `io/ioutil`, deprecated 2021, running in 2026 | 09 | 175 deprecated declarations in Go's stdlib — the cost of a compatibility promise, kept |
| Brooks n(n−1)/2 and the weekly hours | 09 | A team of 20 spends a quarter of every week staying aligned |
| The 80h vs 988h remaining scenario | 09 | Same team, same hire, opposite answers; break-even sits at the ramp-up length |
| Bidirectional Order↔Customer | 16 | OOP producing cycles |
| Deleted constraint, passing mock test | 17 | Mocks assert about mocks |
| Store split into a package | 18 | Layered packages force exports |

## Deliberate repetition

Only these ideas may appear more than once, because the book's structure depends on them:

- **The kind of the current material** — every chapter opens by stating it. One line.
- **The mandatory boundary section** — every chapter has one. It is a section, not a repeated argument.
- **FlowCore as running example** — appears across Parts II and V, but each appearance must show a *different* facet.
