# AI-Assisted Development: Source Material

Worked-out argument for the AI material, held here because it is owed to five chapters that do not exist yet.

**Read this rather than re-deriving it.**
The reasoning below was argued through with the author and corrected twice; re-derivation produces subtly different claims, and the distributed mentions must agree with each other.

Decision 24 records what was decided and why.
This file records the argument itself, at the fidelity the chapters will need.
Delete a section once the chapter that owns it has been drafted against it.

---

## The claim, and what it is not

The material is **not** that AI produces bad code.
FlowCore's decision 18 is the counter-example, and it is the strongest evidence here: the generated code was *idiomatic*, and that was the problem.

The claim is that generated artifacts **state no decisions at all**.
Every branch is already taken by the time you read the code, and a taken branch leaves no mark.
There is no confident sentence to be suspicious of, because there is no sentence — the decision is the shape of the code.

The author's framing, which is the sharpest available:

> Without "grilling", I would be building a system where I didn't know the trade-offs and important decisions and where a default "recommended" decision was silently made by the AI.

Chapter 02 says the kinds get confused because tone does not vary with authority.
Generated code is worse than that: it has no tone, because it makes no claim.

---

## The four findings

Each is an instance of a mechanism the book already owns, which is why this is distributed rather than a chapter.

### 1. The training corpus is a monoculture — chapter 02

Chapter 02 names monoculture as "the single most common source of confusion here" and prescribes exactly one cure: work in a second ecosystem long enough that its conventions stop feeling wrong and start feeling like conventions.

A model has one training distribution.
It cannot go and work somewhere else.
**The prescribed cure is structurally unavailable to it**, so the majority ecosystem's Idioms arrive as defaults, wearing the authority of the obvious.

This is the finding that makes the material non-obvious: it is not a claim about capability, it is a claim about what "idiomatic" can mean to something with one corpus.

### 2. An AI coding agent cannot see your Forces — chapter 03

Chapter 03's claim is that evaluating the Forces is the groundwork.
A model has the prompt.
Forces are facts about your situation, so the derivation happens without its inputs — not carelessly, but by construction.

Chapter 03 leaves a reader stuck here, and grilling is the resolution: you cannot supply the Forces in a prompt because you do not yet know which ones are about to matter.
The interview inverts the flow — the model surfaces the decision, the human supplies the fact that settles it.

### 3. Uniform confidence across all five kinds — chapter 02

One agent produces Laws, Principles, Idioms, and Style in one voice.
Chapter 02's first mechanism, with a single source behind it.

Weaker than the other three, and should stay a clause rather than a section.

### 4. The team-size Force at its limit — chapter 03

Chapter 03's team-size Force asks how many people must agree, and how many of today's people will still be here.
Its mechanism is that a rule migrates **comment → review habit → type system** as the number who must know it rises and the chance any of them was present for the original argument falls.

Generated code sits at the extreme of both axes at once: a contributor present for no conversation, retaining nothing between sessions, producing at a rate no review process was sized for.

The prediction is specific and checkable: **the migration is forced harder and sooner.**
Rules that survived in a comment or a review habit must move into types, constraints, and tests, because every mechanism depending on someone remembering has lost its constituency.

---

## Grilling — chapter 19

A skill the author runs by default in FlowCore sessions.
It is an **interview conducted before generation**, not a review technique.

### What it does

It walks the decision tree, puts each decision to the human with the model's recommended answer, and does not act until there is shared understanding.

The load-bearing detail is the author's:

> sometimes I choose an option that was not the recommended one

The recommendation is drawn from the corpus, so it is the majority ecosystem's convention arriving as a default.
Overriding it is a local Force beating a corpus convention — possible only because the convention was made visible as a *choice* rather than delivered as code.

### The frozen text, quoted in full

The author uses an earlier version and the book quotes that one.
It is recorded here because it no longer exists upstream.

> Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.
>
> Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.
>
> If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.
>
> Do not act on it until I confirm we have reached a shared understanding.

### Provenance

Cite all of it; the author's instruction was that there is no virtue in hiding it.

- The skill is from Matt Pocock's skills repository, `skills/productivity/grilling/SKILL.md` — <https://github.com/mattpocock/skills>.
- The author encountered this use of it during development through Jason Ku's video — <https://www.youtube.com/watch?v=ikGhv9kKFdU&t=356s>.

The current upstream version was fetched on 2026-08-12 and differs materially.
It organizes questions into **rounds** over a **frontier** of decisions whose prerequisites are settled, asks the whole frontier at once with numbered questions in a fixed format, and dispatches sub-agents to establish facts.

The two versions **disagree on a design point**, and the chapter should say so rather than smooth it over: the frozen version says *asking multiple questions at once is bewildering*; the current one asks a round at a time.
The trade is throughput against how much the human must hold in working memory, which is a Force, and which wins is situational.
Do not imply the later version is a regression.

Worth noting that upstream converged on the same language independently — it ends *"every branch of the design tree visited, nothing left silently assumed."*

### The limit, which the chapter must state

Grilling surfaces the decisions the model recognizes **as** decisions, and that set comes from the same corpus.
A question settled uniformly across the training data does not present itself as a branch point at all; it is simply how things are done.

So **grilling is weakest exactly where the monoculture is strongest.**
It surfaces contested choices and hides settled ones — and settled-in-the-corpus is precisely the class most likely to be wrong outside the ecosystem it came from.

This follows from chapter 02's mechanism rather than from measurement.
State it as reasoning, not as a finding.

### The ordinary costs

- **Slow by design.** One question at a time, waiting for each answer. Absurd overhead on a small change.
- **Requires the human to hold opinions.** A user who accepts every recommendation has bought the silent defaults back with ceremony attached.

---

## The FlowCore evidence

Lead with this rather than with the book's own decision log.
FlowCore's log is about schemas, concurrency, and naming, with consequences; this book's log is about prose, and readers will discount a book that proves its method works by citing itself.

### Decision 18 — an Idiom whose precondition failed (chapter 21)

Its context line:

> Reviewing generated code (test files especially) surfaced a real comprehension cost: abbreviated domain-concept names (`def`, `act`, `mgr`, `c` for a Catalog) required constantly re-deriving what they stood for.

The model wrote **idiomatic** Go.
Short local names are the convention, the corpus is dense with them, and every standard measure passes it.

What broke was the Idiom's precondition, which decision 18 states exactly: the convention's justification "assumes the reader is holding the whole function in working memory in one sitting."
That holds when you write the code.
It does not hold when you review generated code in volume, having authored none of it.

So the Force that changed is **the reader is no longer the author**, and the result is a documented, deliberately narrow deviation — which is chapter 21's prescription (declare it, document the reason, keep it narrow) carried out in full, for an AI-shaped reason.

### Decision 37 — generated tests that never reach their condition (chapter 17)

> This is the fifth toothless or invalid test in the iteration […] The recurring shape is a test that never reaches the condition it names.

The mitigation recorded there is mutation: break the code deliberately and confirm the test notices.
That is the only check that catches a test which passes without testing anything, and volume is what makes it necessary.

### The loop, wired explicitly

FlowCore's `CLAUDE.md` line 77:

```text
Reasoning and worked examples: `docs/decisions.md`, decision 18.
```

and lines 95–97: *"`docs/decisions.md` is authoritative for design reasoning. When the two appear to disagree, `decisions.md` wins."*

So a condition discovered by reviewing generated code became an instruction, and the instruction points back at the entry holding its reasoning.
That is the full circuit:

| Stage | Artifact | What it answers |
|---|---|---|
| Before generation | grilling | decisions made explicitly, by the human, with Forces supplied |
| At the decision | `decisions.md` | the reasoning recorded for whoever comes next |
| Standing | `CLAUDE.md` | recurring answers promoted to constraints |
| After generation | review | drift from all three |

Each artifact alone is ordinary.
The loop is the thing.

---

## The traps

Three, and the first is the serious one.

**This is where the book is most likely to commit its own diagnosed error.**
Twenty-two chapters arguing that advice arrives stripped of its conditions, closing with "keep a decision log and interview the model," is chapter 15's mechanism running on the book itself, in its final pages, with the author as the movement.

Avoiding it requires the conditions stated as harshly as Part IV states them for TDD.
Two are non-negotiable:

- **The countermeasure requires the expertise it was supposed to substitute for.** The author caught this book's CAP overreach because they knew CAP well enough to be suspicious. A reviewer without that knowledge reads the same confident paragraph and approves it. This scales with the reviewer's depth in the specific domain, which is the opposite of what people want from these tools — and saying so is the most valuable thing the material can contribute, because most writing on the subject will not.
- **The log costs real time per decision and pays only under specific Forces.** FlowCore has 38 entries for roughly 5,000 lines. That ratio is justified by durability — those are schema decisions that outlive the code (chapter 03) — and it would be waste on a script with a known death date.

**Dating.**
Refuse every capability claim.
Any sentence naming a model or a version should be cut.
The mechanisms — one corpus, no access to your situation, no continuity — are structural and survive; capability claims do not.

**The book must not take a position on whether to use these tools.**
Usage is a fact, which makes it a Force, and the book does not take positions on facts.
This was an author correction to the draft, recorded in decision 24: the draft had misclassified a Force as a Principle while working on the chapter that defines the difference.

---

## Where each piece lands

| Piece | Chapter | Shape |
|---|---|---|
| Corpus monoculture | 02 | a paragraph, as a new instance of an owned mechanism |
| Cannot see your Forces; team-size Force at its limit | 03 | a passage in the relevant Force sections |
| The conditions were never derived | 15 | a paragraph applying 15's own test — **the argument is not worked above**; ledger row *The scope was never set* cites this file for it and there is nothing here yet |
| Generated tests that never reach their condition | 17 | a passage, with FlowCore decision 37 |
| Grilling, in full | 23 | **done** — drafted into 19, moved to 23 by decision 96; the frozen text, the provenance, the two versions' disagreement and the limit |
| An Idiom whose precondition failed | 22 | **done** — landed in 22 rather than 21, because 02's mechanical test sorts short names as Style (decision 87) |
| Silent defaults; receiving generated code | 23 | **done** — the chapter was created for it (decision 96), and it is no longer a *receiving case*, since 23 stopped being the receiving chapter |

Chapters 02, 03, 15 and 17 are all at **draft**; see *Pending revisits* in `00_toc.md`.
This file is deleted once the four outstanding pieces land, per decision 92.
