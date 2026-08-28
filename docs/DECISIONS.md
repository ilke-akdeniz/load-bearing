# Decision Log

Editorial decisions for *Load-Bearing*, recorded when made rather than reconstructed afterwards.

Each entry follows the same shape: **Context / Options / Decision / Why / Consequence**.
The reasoning is the point — a decision without its reasoning is just a fact about the current draft, and tells you nothing when you are deciding whether to reverse it.

Two purposes:

1. **Working memory.** In six months the question will be "why Levels and not Altitudes," and the answer should not have to be re-derived.
2. **Authorship record.** The book is written with AI assistance. What makes it an authored work rather than an assembled one is the selection, rejection, and correction recorded here — so those are recorded with attribution, contemporaneously.

Entries note who originated what.
"The author" is the human; "the draft" is generated text prior to review.

**Unattributed content in an entry is the draft's.**
Attribution is stated where the origin changes how the entry reads later — the author originating an idea, choosing between options, or rejecting one; a correction arriving in review; a draft recommendation that did not survive; or a resolution reached jointly, which is recorded as joint rather than credited to whoever wrote it down.

---

## 1. Title: *Load-Bearing*

**Date.** 2026-08-03

**Context.**
The book needed a name that carried its thesis: that software advice comes in kinds of differing authority, and the damage comes from confusing them.

**Options.**
Five candidates were put forward — *Load-Bearing*, *Altitude*, *Where It Stops*, *It Depends*, *Laws, Idioms, and Slogans* — each framing the book differently.

**Decision.**
*Load-Bearing — Which Software Principles Hold, and Where They Stop.*
Chosen by the author from the five.

**Why.**
The metaphor does the work without explanation: in a building some walls carry the structure and some are partitions painted to look structural, and the whole book is the question a builder asks before knocking one out.
It also supplies the working question in three words — *is this load-bearing?* — which is what a reader should be left holding.

The rejected candidates each failed differently.
*Altitude* names the model but explains nothing until [chapter 01](../01_the-five-kinds_cjx4.md) has been read; a title should not need a footnote.
*Where It Stops* is honest but sounds like a book about limits rather than judgment.
*It Depends* is memorable and undersells the material — a good deal of the book is emphatically not "it depends."
*Laws, Idioms, and Slogans* reads like a paper title; it survives as a section name.

**Consequence.**
The load-bearing metaphor is now the book's spine and should recur as the reader's question, not as decoration.
The subtitle commits publicly to the mandatory *Where this doesn't apply* section, so the promise is on the cover.

---

## 2. "Levels," not "Altitudes"

**Date.** 2026-08-03

**Context.**
The first draft of [chapter 01](../01_the-five-kinds_cjx4.md) used both terms — "the five altitudes" in the title and model, "levels" throughout the prose.

**Options.**
Standardize on *altitudes*; standardize on *levels*; keep both with one as a formal term and one as shorthand.

**Decision.**
*Levels*, everywhere.
Raised and decided by the author on reading the draft.

**Why.**
Two reasons, and the first is sufficient on its own: mixing the terms is worse than either choice, because the reader must work out whether they name the same thing.

Second, the book's stated register is simple language wherever possible.
*Level* needs no explanation; *altitude* is a metaphor that must be unpacked before it earns anything.
The counter-argument — that *level* is overloaded in software (log levels, isolation levels, levels of abstraction) — was judged weaker than plainness and consistency.

**Consequence.**
The chapter file was renamed `01_the-five-altitudes.md` → `01_the-five-levels.md`.
Every occurrence of "altitude" was removed from `README.md`, `LEDGER.md`, and the chapter.
[Chapter 22](../22_never-written-down_at4r.md)'s title became "Reading advice at the right level"; Part I became "The five levels."

---

## 3. Name the kinds, do not number them

**Date.** 2026-08-03

**Context.**
The draft referred to "a Level 0 violation," "altitude 3," and similar throughout, with numbers assigned in the model table.

**Options.**
Keep the numbers as the primary handle; keep both name and number; use names only, with numbers reserved for where ordering carries meaning.

**Decision.**
Names only — Law, Force, Principle, Idiom, Style.
Numbering removed from the model table, chapter prose, and cross-references.
Raised and decided by the author, with the reasoning: *numbering is decoration that should be used only when it adds something.*

**Why.**
"A Level 0 violation" forces the reader to decode an arbitrary index before the sentence means anything, and the decoding must be repeated on every occurrence.
"A Law violation" is self-describing at the point of use.

This is the same argument the book makes about pattern names in [chapter 09](../09_what-a-pattern-is-for_3xzc.md) — a name earns its place by compressing, and an index compresses nothing — so using numbers here would have contradicted the book's own test.

**Consequence.**
Where relative position genuinely matters, the text names the ladder explicitly (Law → Principle → Idiom → Style) and says "one rung higher," rather than performing arithmetic on level numbers.
The `LEDGER.md` cross-reference convention was updated to `"a Law / an Idiom ([Ch. 01](../01_the-five-kinds_cjx4.md))"`.

---

## 4. Forces relate differently to Laws than to Principles

**Date.** 2026-08-03

**Context.**
The draft contained two claims that could not both be true.
One section said Forces "decide which Principles apply"; another was headed "A force deciding whether the law applies."
The classification test compounded it: its Law question made no mention of Forces at all, implying only Principles were Force-sensitive.

The author identified the contradiction and asked directly whether Forces govern Laws as well as Principles.

**Options.**
Restrict Forces to Principles only, and rewrite the seat-reservation demonstration; extend Forces to both without distinction; distinguish *how* Forces act on each.

**Decision.**
Distinguish the two relationships explicitly, as a named section of the chapter:

> A Force never makes a Law false — it decides whether the Law **binds** or sits inert.
> A Force can make a Principle **wrong** — Principles do not merely go quiet, they can invert.

Summarized as: **a Law can be irrelevant but never wrong; a Principle can be wrong.**

**Why.**
The loose version was not merely imprecise, it licensed a misreading in which Laws bend to circumstance — which would have undermined the entire distinction between a Law and a Principle, and with it the book's thesis.

Amdahl's Law is true of a single-threaded script; it simply has nothing to constrain there.
That is a different relationship from "don't repeat yourself," which can be actively bad advice in the right circumstances.

**Why it was worth the rework.**
The correction improved the model rather than patching it.
It clarified that Law / Principle / Idiom / Style form an authority ladder while Force sits outside as the input deciding where on the ladder one is standing — a cleaner structure than five undifferentiated kinds.

**Consequence.**
Three knock-on edits followed.
The seat-reservation demonstration previously said "now it is correct," implying the Law had bent; it now states that the Law is **true and inert** because its precondition — a second concurrent writer — is absent.
Test question 2 gained the clause "when its preconditions hold," without which every inert Law is misclassified.
A new failure symptom was added: defensive code guarding a condition the architecture makes impossible, i.e. an inert Law treated as live.
`LEDGER.md` gained a row so later chapters cite the distinction rather than re-derive it.

---

## 5. Delete the "two competent teams" heuristic

**Date.** 2026-08-03

**Context.**
The draft offered a shortcut for the classification test:

> If two competent teams can disagree and both ship working software, it is not a law.

**Options.**
Keep it; qualify it; replace it with a different shortcut; delete it without replacement.

**Decision.**
Delete, no replacement.
Rejected by the author, on the grounds that shipped software is a poor standard of evidence — the observation being that a great deal of what ships and is counted as working in practice is nothing of the sort.

**Why.**
The objection is correct, and the heuristic is worse than unreliable — it is backwards.
Laws are violated in shipped software constantly; that is the normal case, not the exception.
Race conditions ship.
Applied honestly, the heuristic would classify check-then-act as "not a Law" on the grounds that many competent teams ship with the bug — the exact opposite of the truth.

The deeper fault: it used *outcome* as evidence of *correctness*, when the book's whole method is to reason from mechanism instead.

**Consequence.**
No replacement shortcut was substituted.
A snappy heuristic that is wrong is worse than none, and the five-question test already does the work.

---

## 6. Reject the "homogeneous shop" boundary

**Date.** 2026-08-03

**Context.**
[Chapter 01](../01_the-five-kinds_cjx4.md)'s *Where this doesn't apply* section closed with:

> In a homogeneous shop — one language, one stack, one domain, stable team — the kinds rarely come into conflict.
> Local convention is a perfectly good proxy for correctness there […]
> If your context is uniform, follow the convention and read a different book.

**Options.**
Keep as written; soften it; delete it and accept three boundaries instead of four; replace it with a boundary that survives scrutiny.

**Decision.**
Rejected outright by the author, from experience: monoculture environments are where malpractice breeds, and local convention is the birthplace of precisely the failures the book catalogues.
The passage was replaced with its inversion:

> **In a monoculture you need this most and can execute it least.**

**Why.**
The author's objection is correct on the merits, and the passage was also **internally contradictory**.
The same chapter identifies monoculture as a cause of confusion — "monoculture makes Idioms look like physics" — and prescribes cross-ecosystem experience as the cure.
Two sections later it declared monoculture unproblematic.
The draft argued against itself and neither half had noticed.

The replacement gives the mechanism rather than an assurance.
Test question 4 — *would competent engineers elsewhere do the opposite?* — is unanswerable without having seen elsewhere.
So a single-stack shop is exactly where conventions get misclassified as Laws, and exactly where nothing surfaces the error, because nobody arrives carrying a contradicting habit.

The section still ends by advising the reader to follow local convention, but for a defensible reason rather than an optimistic one: not that convention is a good proxy for correctness, but that without comparative experience one lacks the standing to overrule it, and idiosyncratic is worse than conventionally wrong.
The stated remedy is acquiring contrast — reading the *source* of well-regarded projects in another ecosystem, not their blog posts — since one cannot reason one's way to a counter-example one has never seen.

**Consequence.**
The boundary count rose from four to five: a further boundary, **classifying is not deciding**, was added in the same pass.
Recognizing something as an Idiom is not permission to ignore it, and [chapter 20](../20_idioms_7nkn.md) argues that following local convention is usually correct even when one can out-argue it.
This closes the "licence to dismiss" loophole structurally rather than only in the costs section.

Related: the cryptic "validate input at the boundary" note was deleted from the same chapter in this pass, as in-chapter repetition of a point the boundary section already makes properly.

---

## 7. A concept ledger, to prevent cross-chapter repetition

**Date.** 2026-08-03

**Context.**
Before any chapter was drafted, the author raised a failure observed in previous AI-assisted book attempts: the same ideas restated across three or four chapters, to the point of being an obstacle to reading.

This is a foreseeable failure rather than an accident of those particular tools.
A chapter drafted in isolation cannot see what earlier chapters already established, and a writer who cannot see it will re-establish it — reasonably, since each chapter must make sense.
The result is a book that explains its foundations five times and its conclusions once.

**Options.**
Rely on per-chapter discipline and reviewer vigilance; draft the whole book in a single pass so everything stays in view; cross-reference heavily but tolerate re-explanation; maintain an explicit external registry of what each chapter owns.

**Decision.**
A concept ledger, kept at `docs/LEDGER.md`.
Every concept and every code example is assigned to exactly one owning chapter, with a canonical one-line statement and a note on how other chapters may refer to it.
Two rules bracket every drafting session: **read it before writing a chapter, update it after.**
A chapter needing an idea it does not own gets one sentence and a cross-reference, never a recap.

The ledger also names the small set of ideas permitted to recur — each chapter stating its own kind, the mandatory boundary section, and FlowCore appearances that must each show a different facet — so legitimate structure is not mistaken for drift.

**Why.**
The first option fails because the problem is structural, not attitudinal.
Discipline cannot compensate for missing information; a writer who does not know [chapter 04](../04_structure_agjy.md) already covered acyclic dependency is not being careless when they cover it again.
The fix has to supply the missing information, which means it has to be external and written down.

The second option — drafting everything at once — trades one failure for a worse one: no opportunity for the author to steer between chapters, which is where this book's judgments are actually being made.

The third tolerates the defect being solved for.

**Consequence.**
The ledger was created **before** [chapter 01](../01_the-five-kinds_cjx4.md) rather than retrofitted, so the first chapter was written against it.
The effect is visible in that chapter: it uses the seat-reservation race, manual DI wiring, and acyclic dependency, and explains none of them — each is demonstrated and handed to its owning chapter, e.g. *"the Law being broken is check-then-act, which [chapter 05](../05_time_mdbn.md) owns."*

Costs: one more file to maintain, and a mandatory read-and-update step per chapter.
The bookkeeping is real, and it will be wrong occasionally.

**Where this doesn't hold.**
The ledger only prevents repetition of *registered* concepts.
It cannot catch an argument that arises independently in two chapters and was never entered, nor near-duplicate phrasing of the same idea under two names.
Author review remains the backstop, and a repetition found in the drafts should be treated as a ledger defect — a missing or mis-assigned row — rather than as a wording problem to edit locally.

---

## 8. "Layered architecture" is split into three claims, not treated as one

**Date.** 2026-08-03

**Context.**
[Chapter 04](../04_structure_agjy.md) had to say something about layering, which is the most widely endorsed structural advice in software and also the source of some of the worst structure in it.
Treating it as a single claim makes that contradiction unexplainable: either the advice is good and the pass-through classes are somebody's execution failure, or the advice is bad and a great deal of well-functioning software is an accident.

**Options.**
Treat "layered architecture" as one Principle and note that it is often over-applied; treat it as a Law with common misapplications; split it into its component claims and classify each separately.

**Decision.**
Split into three, and give each its own kind:

| Claim | Kind |
|---|---|
| Dependencies flow one way — no cycles | **Law** |
| The acyclic graph is a straight line | **Principle** |
| The line is `presentation → business → data`, expressed as directories | **Idiom** |

**Why.**
The split explains the contradiction instead of restating it.
Almost all real damage is a violation of claim 1; almost all damage done by layering *advocacy* is claim 3 applied where the graph is not a line.
That is a diagnosis, and it tells a reviewer which of the three they are looking at.

It is also the book's own model applied to its most important structural material — three levels bundled under one name is precisely the failure [chapter 01](../01_the-five-kinds_cjx4.md) describes.
If the model could not take layering apart, that would be evidence against the model.

**Provenance.**
The two-claim version — *dependencies flow one way* versus *and the layers are presentation/business/data* — comes from the FlowCore architecture dialogue at `~/c/TechIter/01/coding-style-architecture.md`, written in exchange with the author and corrected there.
That document also supplies the formulation the chapter quotes: *managed, acyclic dependency direction is a foundation of maintainable software; layering is its most common shape, not its definition.*
The draft's contribution is separating the taxonomy from its *expression as directories*, and attaching the five-level kinds to each claim.

**Consequence.**
[Chapter 04](../04_structure_agjy.md) leads with the three-way table rather than with a definition of layering.
`LEDGER.md` records "layered is three claims" as owned by 05, so [chapters 15](../15_behaviour-placement_z47a.md), 18, 19, and 20 cite it rather than re-deriving it — 18 in particular, which owns what expressing claim 3 as packages actually costs.

---

## 9. [Chapter 04](../04_structure_agjy.md) uses FlowCore for type-enforced direction, not for its package layout

**Date.** 2026-08-03

**Context.**
FlowCore is the running example, and each appearance must show a different facet.
Two chapters want its structure: 05 (dependency and hiding) and 18 (Clean Architecture as directories).
The obvious material — one flat package, 133 exported identifiers, no `internal/` — is the same material for both.

**Options.**
Let 05 introduce the flat-package argument and have 18 refer back; give 18 the flat package and find 05 a different facet; split the flat-package argument across both.

**Decision.**
18 keeps the package layout and what walls cost.
05 uses `querier` and `txQuerier` — the dependency direction enforced by *what a function can reach*, with `Begin` deliberately absent from both interfaces so no store helper can start a transaction.

**Why.**
It is a genuinely different facet rather than a division of one, and it is the stronger example for 05's actual claim: it shows a real, compiler-checked layering with no directory involvement at all, which is exactly the *layer ≠ directory* point.
The compiler error is quotable from FlowCore's decision 37, so the enforcement can be shown rather than asserted.

The third option was rejected on the ledger's own logic — an argument split across two chapters is re-established in both.

**Consequence.**
[Chapter 04](../04_structure_agjy.md) quotes decision 10's reasoning for keeping `querier` unexported ("a public commitment to a shape pgx defines") as its worked instance of export-surface-as-liability, and leaves the flat package unmentioned except as a cross-reference.
The chapter's other examples are deliberately non-FlowCore — a compiler's DAG, ECS parallel arrays, `net/http` — so no section rests on it alone.

---

## 10. Book chapters and working documents get different markdown conventions

**Date.** 2026-08-03

**Context.**
`CLAUDE.md` carried one set of markdown rules, written for a code repository, applied to everything.
The central rule was **one sentence per line**, chosen so a one-word change produces a one-line diff.

The author raised that this does not suit book content, and asked for conventions that keep the source readable while staying easy for a future script to build into a PDF.

**Options.**
Keep one rule set for the whole repo; adopt a full print-oriented convention set for chapters (semantic markup, fenced divs, explicit cross-reference links, ASCII-only diagrams, per-file YAML frontmatter); adopt a minimal set covering only what a script cannot fix later.

**Decision.**
Two rule sets, split by location.
`docs/` keeps one sentence per line.
Chapters at the repo root get four rules and nothing more:

1. One paragraph per line.
2. Code left exactly as the language's formatter produces it, never hand-broken to fit a page; ASCII diagrams under 72 columns.
3. One H1 per file, the title with no chapter number.
4. Every code fence carries a language tag.

The middle option was drafted first and rejected in the same pass.

**Why.**
The diagnosis of the sentence-per-line problem is specific: it is not that the sentences are short, it is that **paragraphs stop looking like paragraphs**.
Every line begins at column zero with a capital letter, so the blank line is the only surviving signal of where a thought ends, and it is a weak one against fifteen identical-looking lines.
Prose reads as a list of assertions.

What sentence-per-line buys — one-word-change-is-one-line-diff — is recoverable at any time with `git diff --word-diff`, at finer granularity than it offered.
Source readability is paid on every read; diff granularity is a flag away.

The larger convention set was rejected on a test the book itself supplies.
Its extra rules — `::: claim` fenced divs, `[Ch. 04](04_structure_agjy.md)` cross-reference links, ASCII-only diagrams, dropped `---` dividers — each traded source readability for build convenience, **and every one of them is a transformation a script can perform in a single pass years from now.**
Box-drawing glyphs need a font, not a rewrite; `([Ch. 04](../04_structure_agjy.md))` is a regex; `---` is one line of filter code.
Paying in readability today for work a machine can do later is the wrong direction.

The surviving rules are those a script *cannot* do:

- Joining prose into paragraphs is mechanical, but the resulting line lengths are what the author reads for the life of the project.
- Heading structure and fence tags are cheap now and ambiguous to infer later — nothing downstream can reliably tell a shell transcript from a diagram from Go.

**Correction: the 72-column code rule failed its own test.**
The first version of this decision required code fences to stay under 72 columns, on the reasoning that breaking a long signature well needs judgment and therefore could not be automated.
[Chapters 01](../01_the-five-kinds_cjx4.md) and 05 were converted on that basis, with 16 lines rewrapped by hand.

The author rejected the result on sight: the breaks made the code harder to read and harder to follow.
That objection is correct, and the rule was wrong for the reason the rest of this entry gives — **it was paying in source readability for something the build can do.**
LaTeX's `fvextra` wraps long lines inside the environments pandoc already emits, at whitespace, with a continuation marker, and keeps pandoc's syntax highlighting; the settings are recorded in `CLAUDE.md`.
Nothing needed to be broken by hand at all.

Two things had gone wrong.
The premise was unchecked — "a script cannot break a line well" was assumed rather than verified against what the toolchain actually offers.
And the rule was worse than a neutral mistake: hand-broken signatures are not the code, so the book would have been quoting FlowCore inaccurately in a chapter whose argument rests on the exact shape of a function signature.

All code was restored verbatim.
The one width rule that survives applies to **ASCII diagrams only**, because a wrapped diagram is destroyed rather than marked — and that is a genuine asymmetry between code and art, not a page-fitting preference.

**Format.**
Markdown was reconsidered and kept.
AsciiDoc is genuinely better at books — native cross-references, indexes, code callouts, a real PDF toolchain — and Typst and LaTeX produce better print output.
All three optimize for the printed artifact, and for this book the printed artifact is not the point: the repository is.
The book is published in public while in progress and read in a browser, it is CC BY so readers must be able to fork and translate it without installing a toolchain, and it is LLM-drafted, where markdown is generated reliably and AsciiDoc accumulates low-grade syntax errors.
Markdown is the only candidate satisfying all three.
The decision is also reversible: pandoc converts markdown to AsciiDoc or LaTeX mechanically, and consistent source is most of that work.

**Consequence.**
`CLAUDE.md`'s markdown section was split into shared rules, book rules, and `docs/` rules.
[Chapters 01](../01_the-five-kinds_cjx4.md) and 05 were converted: prose joined to one paragraph per line, chapter numbers removed from both H1s, 4 untagged code blocks given languages, and the DAG diagram in 05 narrowed from 86 to 52 columns.
All code is byte-identical to what it was before the conversion, verified by diff.
The prose was verified unchanged word-for-word; the only differences are the two chapter numbers and one redundant `>` prefix on a joined blockquote.

`CLAUDE.md` carries the `fvextra` settings, so the constraint is recorded where the build will need it rather than imposed on every chapter written between now and then.

The visible cost is that a chapter's prose is now unreadable in a terminal without soft wrap, and that `git diff` on a revised paragraph reports the whole paragraph.
`git diff --word-diff=color` is the intended review command and should be used on chapter files.

---

## 11. Provenance markers are written as prose, not as bracketed tags

**Date.** 2026-08-05

**Context.**
`README.md` and `CLAUDE.md` specify three inline markers for tagging a claim's standing: `(established)`, `(contested)`, `(ours)`.
Reviewing [chapter 04](../04_structure_agjy.md), the author's reaction to `` `(established)` Parnas, 1972 `` was that the markers read as leftover draft notes rather than as content.

**Options.**
Keep the bracketed tags and explain them once in [chapter 01](../01_the-five-kinds_cjx4.md); keep them but use them more sparingly; replace them with plain English in the prose; drop the distinction entirely.

**Decision.**
Write the standing into the sentence, in [chapter 04](../04_structure_agjy.md).
`` `(ours)` `` on the three-claims table became "Splitting them this way is this book's, not standard vocabulary."
`` `(established)` Parnas, 1972 `` became "Parnas, 1972 — the founding paper, and still the clearest statement."
`` `(established)` `` on Hyrum's Law became "The name comes from Hyrum Wright at Google; the observation is standard and uncontroversial."

**Why.**
The author's reading is correct, and the reason is one the book already argues in [chapter 01](../01_the-five-kinds_cjx4.md): a marker the reader must decode before the sentence means anything is a cost, and this one earns nothing back.
`(established)` in front of a dated citation is redundant — *Parnas, 1972* already is the provenance, stated in the form scholarship uses.

The tags also fail differently in the two directions they are meant to work.
Where a claim is genuinely contested or genuinely this book's, one clause of plain English says so *and* says how, which the tag cannot: "not standard vocabulary" tells the reader what to expect when they search for the term, where `(ours)` only tells them a category.
Where a claim is standard, the tag adds a decoding step to a sentence that was not in doubt.

This is the same argument as decision 3, which removed numbering from the five kinds on the grounds that a name is self-describing at the point of use and an index is not.
Applying it to provenance markers is consistent rather than novel.

**Open.** *(Resolved by decision 13, which removed the notation entirely.)*
`README.md` and `CLAUDE.md` still document the bracketed form, and [chapter 01](../01_the-five-kinds_cjx4.md) still uses it in two places.
Reconciling them is the author's call: either the marker convention is replaced book-wide with the prose form, or [chapter 04](../04_structure_agjy.md) is the exception and the rule stands.
Nothing was changed in those files, because the convention is a structural decision and this entry records only what was done to one chapter.

**Consequence.**
No bracketed markers remain in [chapter 04](../04_structure_agjy.md).
If the prose form is adopted book-wide, `README.md`'s "Provenance markers" section and `CLAUDE.md`'s equivalent are the two places to edit, and [chapter 01](../01_the-five-kinds_cjx4.md) has two occurrences.

---

## 12. [Chapter 04](../04_structure_agjy.md) revised against the author's first content review

**Date.** 2026-08-05

**Context.**
[Chapter 04](../04_structure_agjy.md) was drafted and committed, then reviewed by the author in one pass of seventeen comments.
The comments fell into three groups rather than being a list of wording fixes, and the grouping is the useful record.

**Group one — claims asserted rather than shown.**
Five passages stated a conclusion the reader had no way to reach.
"The damage is the same at every granularity" never said what the damage *was*.
The parser/`ast` example was named but not explained, so the point landed only for readers who already knew how a compiler is put together.
"Depend on abstractions" was stated in a way that reads as *add interfaces*, which is advice the book attacks elsewhere.
Three passages in *What it costs* asserted a bill with no worked case.

**Group two — two sentences that did not parse.**
"The cost of a cycle *is* the forced merging of units — and there is no merging to force," and the ECS paragraph ending "that agreement is the design."
Both were compressed to the point of being unreadable; the author's note on each was "What?"
Neither was a subtle point badly phrased — they were correct ideas written as if the reader already held them.

**Group three — an objection the chapter never answered.**
*"A cycle spreads. Once A and B are mutually dependent, any C that touches either one inherits both" — I don't get this, can't we just inject a and b to c?*

**Decision.**
All three groups were treated as defects rather than as taste, and the chapter grew from 375 to 704 lines.

The structural change: **the cycle mechanism moved from *Why it holds* into the demonstration**, immediately after the four-granularities block, on the author's observation that this is where the reader asks what the damage is.
The section that answers it is new and splits the damage in two — the small part that crashes (a worked Python partially-initialized-module failure whose outcome depends on import order) and the large part that never crashes at all (a worked change-request scenario across `billing` and `accounts`, showing the cost arriving as a bad estimate rather than a bug report).

**Why the injection objection mattered most.**
It is the obvious response, the chapter had no answer, and the answer turned out to be one of the chapter's better paragraphs: injection moves *construction*, not *dependency*, and the two-phase construction it forces (`a := &A{}; b := &B{a}; a.b = b`) is the cycle admitting itself at the wiring site.
What does remove the edge is an interface **owned by the module that needs it** — which is the same manoeuvre as `net/http`'s `Handler`, already in the chapter's boundary section and never connected to it.
The objection exposed a missing link between two sections that were both already there.

A related question — *doesn't dependency injection contradict information hiding?* — got its own short section for the same reason: it is the reading a careful reader arrives at, and leaving it unanswered makes the chapter look self-contradictory.

**Other substantive corrections.**

- **"The count is what matters, not the count of *your* dependents"** was garbled. The author proposed *depth of dependency tree*. Neither was adopted verbatim: fan-in is what drives change cost, depth drives build times and comprehension chains, and the sentence was trying to say something third — that internal dependents are countable with `grep` and external ones are not. It is now a heading that says exactly that, and it is the bridge into the hiding half.
- **"exported — a promise"** became **"a contract"**, on the author's note that *promise* collides with the async primitive.
- **"Forty dependents is a decision; two is an afternoon"** was compressed past sense; it now spells out both cases.
- **The bridge from cycles to hiding** — absent, and the author reported having no idea how the two halves related. A short section now states it: cycles are about which way edges point, hiding is about how many edges exist at all. Same graph, same cost model.
- **The failure checklists** gained a clause each explaining how the symptom relates to dependency or hiding, which the author noted was not obvious for several.

**Consequence.**
`LEDGER.md` gained 10 concept rows and 6 example rows, most of them for material that did not exist before the review.
That is the ledger working as decision 7 intended: the additions were entered at the point the chapter claimed them, so [chapters 08](../08_change_rjf9.md), 13, 16, 17, and 18 now have explicit boundaries against material they would otherwise have re-derived.

**Worth recording about the process.**
Every one of the seventeen comments identified something real; none was rejected on the merits.
Two of the three groups are failure modes specific to generated prose — asserting a conclusion in the register of having argued it, and compressing a correct idea until it stops parsing — and both survived a full self-review pass before the author saw them.
The README's claim that the drafts are read and sent back is doing real work here, and this is the largest single instance of it so far.

---

## 13. Provenance markers removed entirely

**Date.** 2026-08-08

**Context.**
Decision 11 left the marker convention half-applied: [chapter 04](../04_structure_agjy.md) stated provenance in prose, while `README.md` and `CLAUDE.md` still documented `(established)` / `(contested)` / `(ours)`, and [chapter 01](../01_the-five-kinds_cjx4.md) and the TOC still used them.

Settling it meant choosing a form.
The author's objection to the bare parenthesis was precise: it does not signal *this is a shorthand and the full description is elsewhere*.
That is a fair complaint about a pointer that does not point.

The design escalated across three attempts.
A markdown footnote was proposed, then improved into a per-claim footnote carrying the substance of the dispute rather than a glossary lookup.
The author preferred an inline link on the marker itself, which surfaced a further problem: the canonical definition lived in `README.md`, and there is no README in a printed book.
Fixing *that* required giving the convention a home in the book body — a new front-matter file and a TOC entry.

At which point the author asked whether the marker was worth anything at all.

**Options.**
Keep `(contested)` as a linked parenthesis, with a new `00_conventions.md` to link to; keep it as per-claim footnotes carrying the substance of each dispute; drop the notation entirely and state standing in prose.

**Decision.**
Drop all three markers and the notation with them.
Nothing replaces it: where a claim's standing could be mistaken, the sentence says so.
`CLAUDE.md` keeps the underlying discipline as a writing instruction rather than as syntax.

**Why.**
The escalation was itself the argument, and it went unnoticed while it was happening.
By the third iteration the convention required its own file, a TOC entry, an anchor scheme, and a README edit — to save eleven characters.
That is the book's own compression test failing (decision 3): a notation earns its place by saving more than it costs, and this one had inverted.

Three further points, all available earlier than they were made.

**Usage was one occurrence.**
Two chapters drafted, zero markers in prose, one in a TOC chapter summary.
A convention with a single instance across twenty-three planned chapters is not a convention.

**The book already commits to this twice, more strongly.**
The stated register is mechanism over authority — so a disputed claim should say *what the dispute is*, which is content a tag cannot carry.
And every chapter carries a mandatory *Where this doesn't apply* section with a worked case.
`(contested)` was a weaker restatement of a commitment the structure already makes.

**It reads as hedging**, which the register explicitly rules out.

**Attribution, and a correction.**
The draft recommended keeping `(contested)` on the grounds that it compresses a claim Part IV must make repeatedly, and that it forces the drafter to classify.
The author rejected it.
The recommendation did not survive its own follow-through: the same analysis that justified keeping one marker also produced a three-step escalation in what it would cost, and the draft did not notice that the second half refuted the first.

The one genuine point in favour — that the marker forced the drafter to decide whether a claim is standard, disputed, or the book's own — was preserved, but moved to where it belongs.
`CLAUDE.md` now instructs that the decision be made and written into the sentence, with the failure modes named: do not label a dated citation, and do not write a bare "this is contested," which is hedging rather than honesty.

**Consequence.**
`README.md`'s "Provenance markers" section was deleted outright.
The draft first replaced it with a paragraph explaining that there is no notation to learn; the author removed that too, on the grounds that it added nothing to the landing page.
That is right, and it generalizes: a section whose content is the *absence* of a convention only makes sense to a reader who came looking for the convention, and nobody arrives at a README looking for one.
Documenting a removal is a decision-log job, not a landing-page job.

`CLAUDE.md`'s section became a writing instruction with three worked cases, and is now the only place the discipline is recorded.
`01_the-five-levels.md`'s epigraph now reads "the book's own framework, not standard terminology you will find elsewhere under these names."
`00_toc.md`'s [chapter 16](../16_tdd-and-mocks_u8eu.md) summary now states the actual dispute — that the controlled studies disagree with each other and mostly measure test-first against no tests rather than against test-after — which is more informative than the tag it replaced and is the pattern the rest of the book should follow.

No markers remain anywhere in the book or its instructions.
The occurrences in this log are historical record and stay as written.

---

## 14. [Chapter 04](../04_structure_agjy.md), second review: three reframings and a reversal

**Date.** 2026-08-08

**Context.**
The author's second pass over [chapter 04](../04_structure_agjy.md) ran to fourteen comments, worked in four batches with a commit between each. Two batches were corrections of fact and structure; two were conceptual.

**The reversal, recorded first because decision 12 got it wrong.**

Decision 12 called *"can't we just inject a and b to c?"* the best question of the first review and built a section around answering it. The author's second pass corrected the reading: the question was never about injecting into a third module, it was **why dependencies are bound to accumulate at all** — with the observation that accumulation looks like habit rather than necessity.

They were right, and so was the underlying objection. The draft's claim that "the tangle grows monotonically" does not survive examination. What is mechanical is that every new dependent of a tangled module inherits the whole tangle transitively — it cannot be built, tested, or extracted without both ends. What is *not* mechanical is cycles begetting cycles: that is a tendency created by the placement ambiguity the first cycle introduces, and discipline resists it.

The invented section was deleted. The material worth keeping — two-phase construction as the visible symptom, and the interface fix — survives under a heading that describes what it does rather than answering a question nobody asked.

**Two examples were wrong, and one was wrong in the book.**

The Python circular-import demonstration claimed one import order works and the other fails. Both fail. The example demonstrated nothing and had been in a commit for four days. Replaced with a verified one whose asymmetry comes from a definition sitting above the import rather than below it — a better example, since the reason is visible in the code.

While rebuilding the four-currencies section, two further examples turned out to be wrong in the same way: an event type declared by `billing` would still force `accounts` to import `billing` to receive it, and a shared module accepting `accounts.Plan` would point an arrow straight back and rebuild the cycle it was introduced to break. Both are fixed, and both fixes are now *stated* in the text, because the mistake is instructive: it is possible to apply a cycle-breaking technique and leave the cycle in place.

**The three reframings, all the author's.**

The draft explained dependency injection in terms of *who knows more*, which produced the unreadable line "billing hides nothing from itself." The author's framing is better and was adopted wholesale: **injection is a module declining to hold decisions that were never its to make.** Where plans are stored, how they are fetched, what is configured — `billing` had helped itself to four decisions belonging elsewhere. The same voice now carries the `net/http` explanation, where the framework says what it cannot decide on a client's behalf.

The author also asked for the difference between dependency *injection* and dependency *inversion*, which the chapter had been using interchangeably. The distinction is now stated: **injection decides who constructs; inversion decides who declares the interface, and only inversion turns an arrow around.**

**The escape hatch was self-contradictory and is now reversed.**

The draft proposed an unsupported accessor with a comment disclaiming compatibility. The author rejected it as having no technical merit — a ceremonial answer that says "yes we have that" while planning to deal with the consequences later.

Correct, and worse than that: the chapter explains Hyrum's Law three sections earlier and then proposes a solution Hyrum's Law defeats. Ship the method, people call it, and removing it breaks them; the disclaimer changes only whose fault that is. The section now gives the two honest answers — a narrow API you commit to, with `database/sql`'s scoped `Conn.Raw` as the model, or a straight no — and says plainly why the disclaimer is neither.

**A precision fix that propagated.**

Making the three claims explicit, as the author asked, exposed a weakness in Part three. Stating claim two precisely — every part gets a rank, and may depend only on the rank immediately beneath — makes it clear that the compiler graph *can* be topologically sorted, so "you must order `parser` and `printer`" was too strong. What actually fails is the strict rank rule: `codegen` and `typecheck` both reach two ranks down to `ast`, and the ranks that fall out of the sort carry no meaning. Part three now says that, which is a stronger argument than the one it replaces.

The author also noted that claim three's physical boundary was more often *libraries and assemblies* than directories in their C# experience. Generalized.

**Consequence.**
[Chapter 04](../04_structure_agjy.md) is 857 lines, from 375 before the first review. `LEDGER.md` gained four concept rows, lost the reversed escape-hatch row, and had five rows corrected where the chapter had moved beneath them.

Worth recording about the process: of fourteen comments, one was a factual error in a shipped commit, two were sentences that did not parse, three were conceptual framings where the author's version was simply better than the draft's, and one reversed a decision this log had already recorded as settled. The failure modes are consistent with the first review — asserting rather than showing, and compressing until meaning is lost — with one new one: **verifying a claim by asserting it confidently.** The Python example was never run. It is now, along with the CommonJS and Go examples that replaced parts of it.

---

## 15. [Chapter 02](../02_forces_f4m5.md): a Force is a dial, not a switch

**Date.** 2026-08-09

**Context.**
The TOC lists seven Forces for [chapter 02](../02_forces_f4m5.md) and asks for "a code demo of the same problem solved differently under different values of it."
[Chapter 01](../01_the-five-kinds_cjx4.md) had already established what a Force *is* — a property of the situation rather than advice, acting differently on Laws than on Principles — so 03 needed something beyond a catalogue, or it would be seven definitions and a table.

**Options.**
Present the seven as a reference list with a demonstration each; organize around one running problem shown seven ways; find the claim the catalogue is evidence for and lead with that.

**Decision.**
Lead with the claim: **a Force has a value, not just a presence, and the design changes several times across that range — each answer discarding the previous one rather than refining it.**
The seven Forces are then the demonstration of it rather than the point.

The chapter opens with one counter at four concurrency values, ending at a position where the answer is no longer a different way to increment but a different data model — an append-only log with an idempotency key, because a retried message is indistinguishable from a second event.

**Why.**
The catalogue alone is not worth a chapter. Everyone already knows concurrency and latency matter; what they do with that knowledge is treat the Force as a flag, pick the design that handles "concurrency," and stop.

The dial framing is what makes the seven useful, and it is falsifiable in a way a list is not: if the design only ever changed once across a Force's range, the framing would be wrong. The counter example is chosen because its fourth position is unreachable from its third by any amount of hardening, which is the strongest available form of the claim.

**A second decision inside the boundary section.** *(Superseded during review — see below.)*
The TOC promised "Forces you can't measure yet, and why guessing is worse than deferring." Written straight, that produces the standard advice to defer decisions, which is wrong often enough to be worth correcting.

The draft's rule was:

> Defer what you can reverse. Decide what you cannot. And when you must decide under uncertainty, choose the strict version, because strictness is the direction that can be undone later.

Both halves are quoted from FlowCore's decision log — `internal/` deferred with its trigger recorded, and the unique index shipped on day one because "dropping a unique index later is trivial; adding one after clients hold duplicate rows is not."

**The author rejected it, and the replacement was reached jointly.**

Their objection was a reductio: judged purely on cost asymmetry, the rule licenses adding every possible index on every combination of columns, since each is cheap now and awkward later. It does.

The draft's first response was that asymmetry, stated precisely, already excludes that — a unique constraint *expires* while you wait, because duplicate rows accumulate and then block it, whereas a performance index does not expire at all, since the data was never an obstacle. True, and insufficient: it does not cover sharding, where waiting genuinely does spoil the decision and acting early is ruinous. Asymmetry alone says shard immediately, which is wrong.

What resolved it was adding a second question, giving three cases rather than two:

> **Does waiting spoil this decision?** If delay lets state pile up that the decision would have prevented, the decision expires.
> **Is this decision cheap to take today?** If it expires and it is cheap, take it now. If it expires and it is expensive, you are making a bet, and should say so.

Neither party held that at the start. The author supplied the counter-example that broke the two-part rule; the draft supplied the expiry-versus-cost distinction; the third case came out of the exchange.

**A reversal inside the reversal.** The author's original wording had included a likelihood clause — *and the need is likely to arise* — which the draft cut as reintroducing the guessing the rule was meant to remove. The third case restores it, scoped to that case only: where a decision both expires and is expensive, it is a forecast whether or not anyone admits it, and pretending otherwise does not make it less of one. The draft was wrong to cut it outright and right that it does not belong in the other two cases.

The surviving general form still inverts what "stay flexible" suggests: under uncertainty the reversible choice is usually the *stricter* one.

**Verification, following decision 14.**
Every runnable example was run before it went in. The JavaScript number-precision demonstration was checked at the point that matters: a 64-bit identifier arriving as a JSON number reads back as `9007199254740992` in Node, and the same value sent as a string round-trips intact. The float-versus-minor-units sums were run rather than asserted.

One example was discarded during verification. A first version of the precision demonstration used a JavaScript integer literal, which is already truncated before `JSON.stringify` sees it — so the round-trip appeared lossless and the example proved the opposite of its caption. The loss only shows when the value arrives as text and is parsed, which is also the real scenario.

**Consequence.**
`LEDGER.md` gained twelve concept rows and six example rows.
The seven Forces are now individually owned by 03, so later chapters name a Force and cite rather than re-deriving it — and the two that were being coined in passing by earlier chapters, control-of-callers and the memory hierarchy, have a home.

[Chapter 02](../02_forces_f4m5.md) runs 381 lines, the shortest of the three drafted so far, which suits a chapter whose job is to supply vocabulary the rest of the book spends.

---

## 16. [Chapter 03](../03_grading-a-law_q5c6.md): one grade, one move

**Date.** 2026-08-09

**Context.**
[Chapter 03](../03_grading-a-law_q5c6.md)'s difficulty is structural rather than editorial: it grades material that other chapters own. CAP belongs to 07, Conway to 09, the memory hierarchy to 08, acyclic dependency to 05, Hyrum's Law to 05. Written straight, the chapter becomes a tour of other chapters' examples with a letter attached to each.

**Options.**
Present the three grades as a taxonomy with examples; organize around how to check a claimed Law; find what the grade is *for* and make that the claim.

**Decision.**
Lead with what the grade buys: **each grade admits exactly one move, and no others.**

- **Grade A**, a theorem — change which assumptions hold. Arguing with the conclusion is a category error, and the assumptions are always stated because a proof cannot exist without them.
- **Grade B**, a near-tautology — check whether the words describe you. It cannot be violated; it can be found not to apply.
- **Grade C**, an empirical constant — measure it, because the number was taken somewhere else at some other time.

That framing solves the ownership problem rather than working around it. The chapter never explains CAP or Conway; it uses them to show what grading buys, and each cross-reference is a sentence.

**Why the demonstrations are the ones they are.**
Each grade needed a demonstration that was 04's own rather than a borrowed one.

Grade A shows an assumption being removed instead of a theorem being stated: the same delivery problem in one process, where a channel cannot lose anything, and across a network, where the acknowledgement can be lost after the work is done. Running it prints three charges for one intended charge, and the caller was never careless — it could not distinguish *never arrived* from *arrived, reply lost*.

Grade B uses a cache read once at startup. [Chapter 01](../01_the-five-kinds_cjx4.md) lists "a cache needs an invalidation strategy" in its table of classified claims but nothing owns the argument, so 04 takes it. The point is the escape: if the original is a compile-time constant there is no cache in the strict sense, so the Law is true and inert.

Grade C uses Go's randomized map iteration against Python's guaranteed dictionary order — one observation, two opposite responses, verified by running both. It carries something the other grades cannot: Python's dict order began as an implementation detail, became widely depended upon, and was promoted to a guarantee in 3.7. The empirical claim's own prediction changed the thing it predicted, which is only possible for a Grade C.

**A distinction the chapter adds.**
The TOC asked what makes Conway's Law different from "prefer composition over inheritance." The answer turned out to be one line worth keeping: **a Law describes; a Principle prescribes.** Conway's Law cannot be bad advice because it is not advice. That separates the two faster than arguing about how universal either feels, and it gives [chapter 01](../01_the-five-kinds_cjx4.md)'s classification test a sharper edge for this one boundary.

**The boundary section leads with the chapter's own misuse.**
*Grade is not importance.* Amdahl's Law is Grade A and irrelevant to a single-threaded tool; the cache-to-memory gap is Grade C, drifting, machine-dependent, and decides a game engine's whole architecture. Reading the grades as a priority ranking commits the error the book is about — treating a firm claim as an important one — using the book's own vocabulary to do it.

**Consequence.**
`LEDGER.md` gains five concept rows and three example rows.
[Chapter 04](../04_structure_agjy.md)'s existing commitments are honoured: acyclic dependency stays Grade B, and Hyrum's Law stays an empirical regularity rather than a theorem.
[Chapter 03](../03_grading-a-law_q5c6.md) runs 206 lines, the shortest so far, which suits a chapter whose job is a distinction rather than a subject.

---

## 17. The A/B/C grading is dropped; the three kinds are named

**Date.** 2026-08-10

**Context.**
[Chapter 03](../03_grading-a-law_q5c6.md) was drafted with the TOC's A/B/C grading — Grade A a proven theorem, Grade B a near-tautology, Grade C an empirical constant.
Reviewing it, the author proposed two changes: refer to the kinds by name rather than by letter, and consider abandoning the grading concept entirely, on the grounds that grading implies a hierarchy nobody can justify — *I don't see why a theorem comes before tautology*.

**Options.**
Keep the letters with the names alongside; keep the letters and defend the ordering; drop the letters and name the kinds.

**Decision.**
Drop the grading. The kinds are **theorem**, **definition**, and **empirical law**, named at every use, in no order.
The chapter's title changes from *Grading a Law* to *Three Kinds of True*.

**Why.**
The author's objection is correct, and the decisive support for it is that **this book already decided this question, in decision 3, and [chapter 03](../03_grading-a-law_q5c6.md) contradicted it.**

Decision 3 removed numbering from the five kinds, with the reasoning that "a Level 0 violation" forces the reader to decode an arbitrary index before the sentence means anything, while "a Law violation" is self-describing at the point of use. Grade A, B, and C is the identical failure, introduced a week later in a chapter drafted against a file that records the earlier decision. The draft did not notice.

The ordering objection is separately right. The letters imply a rank, and there is none: a theorem and a definitional claim are both unfalsifiable, and neither is more binding than the other. They differ in *why* they are true, which is what the names now carry. The draft's own boundary section conceded the point without following it — *grade is not importance* — which the author identified as a reason to question the grading rather than a caveat on it.

**One substitution against the author's wording.**
The author changed *near-tautology* to *tautology*, adding a parenthetical that this is imprecise and adopted for simplicity. That caveat is evidence the word does not fit. A tautology is true by logical form; these claims are true by what their terms pick out, which is a different thing. **Definition** is accurate, needs no apology in the text, and names the reason the claim is true. The parenthetical is gone with it.

**Five corrections the review forced, beyond the terminology.**

- **The theorem was never named.** The Grade A section demonstrated an escape without saying what it was escaping from. It now opens with the Two Generals Problem and says what follows from it.
- **The lesson was not stated.** The author could not tell which of the two code samples was acceptable. The section now says: the in-process version is correct as written, the networked version cannot be fixed by writing it more carefully, and the actual fix removes an assumption rather than improving the client.
- **"Change the model" was ambiguous**, twice. Replaced with "change the assumptions," and CAP's *asynchronous network* is now defined where it appears — no shared clock, unbounded message delay, messages can be lost.
- **An empirical law was reduced to a measurement.** The author's objection: *my measurement of one endpoint's latency is not Hyrum's Law, or we would have millions of laws.* Correct. An empirical law is now a **regularity** across systems carrying a **magnitude** that varies between them; the regularity earns the word *law*, and the magnitude is the part people quote from somebody else's instance.
- **CAP was asserted rather than shown**, and the author flagged both claims as ones that will attract probing. Both are now argued: the theorem is narrow because it concerns linearizable registers and requires every non-failed node to answer, and partition tolerance is not a choice because a partition is an event rather than a design option, so the only real choice is what to do while one is happening. Brewer's own 2012 retrospective is cited for the second.

**Consequence.**
`00_toc.md` gains the new chapter title and loses "Grade A theorems" from [chapter 06](../06_distribution_49yh.md)'s entry.
`04_structure_agjy.md`'s three-claims table now reads "true by definition ([Ch. 03](../03_grading-a-law_q5c6.md))" rather than "near-tautology, Grade B."
`LEDGER.md` has seven rows reworded and one added, for the regularity-versus-magnitude distinction.
`CLAUDE.md` gains a rule the author asked for directly: **write Go for a reader who does not know Go**, since the audience is fluent in Java, C#, or Python, and an unglossed `chan` spends the example.

---

## 18. A theorem admits two escapes, not one; CAP replaced by the halting problem

**Date.** 2026-08-10

**Context.**
The author's second pass on [chapter 03](../03_grading-a-law_q5c6.md) raised three things. One was a question about which assumptions the worked example was talking about. Answering it exposed an error in the chapter's central framing.

**The error.**
The chapter claimed that the only move against a theorem is to change which of its assumptions hold, then demonstrated it with Two Generals and offered idempotency as the fix — describing idempotency as "removing an assumption."

That is wrong. Idempotency removes nothing. The channel still loses replies, the client still cannot distinguish *never arrived* from *arrived, reply lost*, and exactly-once delivery remains impossible. The theorem is untouched.

The example actually contains **two different escapes**, conflated:

- **Running in one process falsifies an assumption.** Memory does not lose messages, so the theorem's precondition is absent and it has nothing to say.
- **Idempotency drops a requirement.** The theorem applies in full and stops mattering, because the thing wanted was never exactly-once *delivery* — it was exactly-once *effect*, and the two had been silently assumed identical.

**Decision.**
State both, and correct the claim. A theorem admits two escapes and no third: make an assumption false so it does not apply, or stop needing the conclusion so it costs nothing. What is never available is arguing with the conclusion.

The chapter's framing widens to match: *what no kind allows is arguing with the claim; the kind tells you where you are permitted to work instead.*

**Why this matters beyond the one paragraph.**
Dropping a requirement is the **more common** escape in practice, and the draft had no name for it. Almost nothing in engineering is solved by arranging not to be distributed; a great deal is solved by noticing that the requirement was stronger than the need. Presenting only the assumption-falsifying move would have taught the rarer half.

**CAP, replaced.**
The author asked for a simpler example in the theorem-versus-slogan section, reporting possible gaps in the draft's account and preferring not to defend it.

Replaced with the **halting problem**, which carries the same point at a fraction of the defensive burden. Turing's result forbids a *universal* decider — no single algorithm deciding halting for every program and input. The folk version, "you can't tell whether a program halts," is a claim about particular programs and is false: termination checking is a working field, proof assistants reject non-terminating definitions, and compilers prove loop bounds routinely.

It is also the better teaching case. The gap between the two versions is a **dropped quantifier**, which generalizes: a folk version has usually lost a quantifier or a condition, and that is exactly where the engineering was. CAP's gap needed a paragraph on linearizability and another on why partition tolerance is not a choice before it could be stated at all.

The failure-list entry changes with it: *"we can't check that, halting problem"* said about an analysis over one repository, where the theorem forbids only a decider that works for every program ever written.

**One addition the author proposed and left to Claude.**
The empirical section's practical form gains a second half: quoting somebody's number is not the same as knowing yours, **and knowing yours does not mean you should be chasing their target.** Worth having — it closes the failure that follows a successful measurement, where a team measures honestly and then adopts someone else's goal for the number.

**Consequence.**
`00_toc.md`'s [chapter 03](../03_grading-a-law_q5c6.md) entry names the actual examples; CAP stays with [chapter 06](../06_distribution_49yh.md), which owns it.
`LEDGER.md` gains a row for the two escapes and one for the halting problem, and loses the CAP row.
[Chapter 03](../03_grading-a-law_q5c6.md) runs 259 lines.

---

## 19. [Chapter 05](../05_time_mdbn.md): two halves, one claim

**Date.** 2026-08-10

**Context.**
The TOC gives [chapter 05](../05_time_mdbn.md) seven topics across what look like two subjects — check-then-act, races, lock-holders, single-writer, clock skew, Lamport and vector clocks, coordination latency. Written as a list it is two chapters sharing a file.

**Decision.**
One claim, stated so both halves fall out of it:

> A check tells you what was true, not what is true. And no clock tells you what happened first.

Both are **there is no shared now** — locally the observation is stale by the time you act on it, globally there is no agreed ordering and timestamps cannot supply one.

**The demonstration that carries the chapter.**
A registration handler that refuses duplicate emails, with a uniqueness check before every insert, and two milliseconds of password hashing between the check and the write. Fifty concurrent requests produce **fifty rows for one email**.

Three things fall out of that one number, and none of them would from a smaller one.

- Every step is individually mutex-protected. The map is never corrupted. What broke spans two operations, and no lock inside either can span them — which is the chapter's real content, since composing safe things into safe things is the intuition most engineers arrive with.
- Remove the hashing and the same code returns one row on an idle machine. The bug is unchanged; only the window narrowed. That is why these defects reach production — testing happens on idle machines, which is testing with the narrowest windows the code will ever have.
- Nothing in the code looks wrong. There is no missing lock to find in review, because the defect is in the shape rather than in a line.

**The clock demonstration, and why it is stronger than skew.**
The obvious argument against timestamps is skew between machines. The chapter starts somewhere harder to dismiss: one machine, one process, no network.

Two hundred thousand pairs of consecutive `time.Now()` calls, with **95% returning an identical value** and a smallest observed gap of 1000 ns. Python agrees within a percent. The wall clock on this machine advances in microsecond steps, so two events a hundred nanoseconds apart do not get an order — they get the same number. Skew, jumps, and the absence of any link to causality then make it worse, but the instrument has already failed before any of that arrives.

**Every claim of behaviour was run.** Four demonstrations and both fixes, in Go and Python: the fifty rows, the lost-update race producing 967 then 929, the filesystem TOCTOU, the clock resolution, the atomic rewrite returning 1, and the Lamport exchange. The lost-update race was confirmed with Go's race detector.

One demonstration was rebuilt during verification. The first check-then-act version had no work between the check and the insert and produced one row — the race existed and did not show. Adding what a real handler does there is not a contrivance to make the bug appear; it is what makes the example honest, and the difference between one row and fifty is the chapter's point about window width.

**A corollary the chapter states separately**, because it is the part people resist: an application-level check is not wrong, but it is not the enforcement. Keep it for the error message, which is what it is good at. Do not keep it as the guarantee.

**Consequence.**
`LEDGER.md` gains eleven concept rows and five example rows; [chapter 05](../05_time_mdbn.md) was previously carrying two.
Six forward references from [chapters 01](../01_the-five-kinds_cjx4.md), 03, and 05 are now discharged.
[Chapter 05](../05_time_mdbn.md) runs 288 lines and moves to **in progress**.

---

## 20. [Chapter 05](../05_time_mdbn.md) pairs every break with its repair

**Date.** 2026-08-10

**Context.**
The author's review made one structural criticism and three local ones. The structural one:

> This chapter reads like anytime you read a state and act on it there is a potential for a very serious problem. There is only 1 "good version" code example.

Both halves are correct, and they are the same defect. The chapter demonstrated five failures and one fix, so a reader met four breakages before any repair, and the accumulated impression was that reading state at all is dangerous.

**Decision.**
Two changes.

**Every break now carries its repair, adjacent.** Five bad/good pairs where there was one: the registration handler with its atomic rewrite, `count++` against `atomic.AddInt64`, the filesystem check against attempting the open, the SQL select-then-insert against a unique index with `on conflict`, and clock comparison against an optimistic version column. All were run.

**A section was added before the demonstration**, stating when this material binds at all. Reading state and acting on it is a problem only when three conditions hold together: something else can write that state, the decision depends on what was read, and the rule spans data that was not held still. Miss one and there is nothing to fix — which covers configuration read at startup, a row already locked, a value only one writer touches, anything immutable.

That section also names the three ordinary fixes before the reader meets any failure, so the failures arrive as instances of a solved problem rather than as an accumulating list.

**Why the ordering mattered more than the content.**
Nothing in the original chapter was wrong. The boundary section already said the Law is inert with one writer, and the fix for the registration handler was present. But the boundary was at the end and the fix was two sections after its failure, so the reader had already formed the impression the chapter then tried to correct. **A qualification that arrives after the alarm does not undo it.**

**Three local corrections.**
The author could not find the mutex in the sample, because `exists` and `insert` were described as taking one without being shown; both are now shown. They rewrote a Go comment for readers who do not know the language, which was a rule added at their request two chapters ago and not applied here. And they caught that the broken and fixed versions of the registration handler used different operations — one called `insert`, the other incremented the map directly — so the comparison was not quite like for like.

**Consequence.**
[Chapter 05](../05_time_mdbn.md) runs 393 lines, up from 288.
`LEDGER.md` gains four concept rows and four example rows.
The atomic fix moved out of *Only the lock-holder can enforce*, which now generalizes the same move to the multi-process case rather than introducing it.

---

## 21. Two examples in [chapter 05](../05_time_mdbn.md) were contrived; both replaced

**Date.** 2026-08-10

**Context.**
The author's second pass on [chapter 05](../05_time_mdbn.md) rejected two demonstrations. Both objections were about the same failure: the code was arranged to produce a result rather than to be a thing anyone would write.

**The sign-up example.**

> I fail to grasp how email registration works. Is there a rows map where each email has a count? And the count can only be 1 at most? Why? Is this just random code?

Fair. The store was `map[string]int`, and registration incremented the counter — so a duplicate registration showed up as `rows["a@example.com"] == 50`, which is a number no real system would ever hold. The shape existed because it made the failure easy to count, which is exactly backwards.

Replaced with a slice of `User` records, appended on sign-up. The output is now *50 accounts for ada@example.com*, which is a sentence someone could read in an incident report.

**The filesystem example, which was worse.**

> I don't see any difference between bad and good version, I only see Python's syntactic sugar that gives you the FileNotFoundError in one statement.

Correct, and the criticism goes deeper than the phrasing. The broken version checked `os.path.exists` and then opened the file; the fix wrapped the open in `try`. Both ended at the same `FileNotFoundError`, so the demonstration showed two spellings of one outcome and claimed a window had closed.

The replacement is the case the term TOCTOU was coined for. An upload handler checks that a path is not a symlink and is under a size limit, does a few milliseconds of work, then reads it. Another process swaps the file for a symlink to a secrets file in between:

```text
BAD : SECRET-DB-PASSWORD=swordfish
GOOD: harmless user upload
```

No exception in either case. The broken version validates one file and reads another, silently, because `os.stat(path)` and `open(path)` resolve the *name* twice and the name was repointed between them. The fix opens once and interrogates the descriptor with `fstat`, because a file descriptor refers to the object while a path refers to a name.

That is a genuinely different outcome rather than different syntax, and it makes a point the chapter needed anyway: **checking twice would not help, because it only adds a third moment for the file to change.** The window closed because the check and the use now refer to the same object by construction.

**A knock-on correction.**
The chapter had named three ordinary fixes up front, and the old filesystem example was the only instance of the third — *do not check at all*. The new one demonstrates the first instead. Rather than leave a move without an example, the SQL fix now carries it explicitly: the `select` disappears, and the insert with a unique constraint is what "stop asking, let the attempt answer" looks like in practice.

**Consequence.**
[Chapter 05](../05_time_mdbn.md) runs 425 lines.
`LEDGER.md` has two example rows rewritten.
Both replacements were run before they went in, along with the attacker process for the symlink swap.

---

## 22. [Chapter 06](../06_distribution_49yh.md) leads with the root fact, not the theorem list

**Date.** 2026-08-10

**Context.**
The TOC gives [chapter 06](../06_distribution_49yh.md) six topics: CAP, PACELC, FLP, Two Generals, timeouts as guesses, p^N, plus the outbox and saga patterns. Written as a survey it is a reference card, and the reader leaves knowing three acronyms rather than one thing.

**Decision.**
Lead with the fact the theorems are consequences of:

> **You cannot tell a slow machine from a dead one.**

Two Generals, FLP, and CAP then arrive as three formalizations of one predicament — a lost message and a slow message look identical, a crashed process and a paused one look identical, a partitioned peer and a dead peer look identical. **The impossibility is always that you must act on information you cannot obtain.**

`p^N` is deliberately kept outside that unification and named as the other kind of fact, because it is arithmetic about independent events rather than a limit on knowledge. Folding it in would have been tidier and false.

**The theorems are presented by their assumptions rather than their proofs**, following [chapter 03](../03_grading-a-law_q5c6.md): the assumptions are the only negotiable part. FLP is stated with the consequence that matters — Raft and Paxos do not evade it, they add timeouts, giving up guaranteed termination to keep guaranteed safety. CAP is stated once and then set aside for PACELC, because the else-branch applies every day and CAP's branch only during an outage.

**[Chapter 05](../05_time_mdbn.md)'s review shaped the structure.**
Two lessons carried forward without being asked for.

The boundary section moved to the **front**, as *When any of this applies to you*, because [chapter 05](../05_time_mdbn.md) established that a qualification arriving after the alarm does not undo it. This chapter needed it more: distributed-systems machinery is imported into single-database systems constantly, and a reader who meets four impossibility results before being told none of them binds will import them again.

Every failure is **paired with its repair, adjacent** — four pairs, all run. The retry that charges three times against the idempotency key that charges once; the order that commits while the event is lost against the outbox that makes it one write.

**The check offered for the boundary** is deliberately not "is this a microservice." It is *can one part be alive while another part cannot reach it?* A deployment diagram does not answer that; a shared process and connection does.

**One thing the chapter says that is easy to get backwards.**
Distributed transactions are not impossible. Two-phase commit works and is used. What it costs is availability — a participant failing while holding a prepared transaction blocks the others — and for most systems that is a worse outcome than the inconsistency being avoided. Saying "you cannot have cross-system atomicity" would have been simpler and wrong, and it would have made the boundary section dishonest.

**Consequence.**
`LEDGER.md` gains ten concept rows and four example rows.
Debts from [chapters 01](../01_the-five-kinds_cjx4.md), 03, 04, and 06 are discharged: exactly-once impossibility, why redelivery cannot be eliminated, and what idempotency is for.
[Chapter 06](../06_distribution_49yh.md) runs 262 lines and moves to **in progress**.

---

## 23. Verification code is not example code

**Date.** 2026-08-11

**Context.**
The author's review of [chapter 06](../06_distribution_49yh.md) identified a recurring failure and asked for it to be written into `CLAUDE.md`:

> I'm guessing you just put the "test code" you used to see if a claim is true directly into the book. You should never do that. […] You say "a client calls a service with a 100 ms timeout," calling code has different params on each call, 100ms is nowhere. What's worse is that the client is setting the timeout to 0 deliberately and nobody would see this as "slow peer."

The observation is correct and the diagnosis is exact. The sample was:

```go
_, errA := call(150*time.Millisecond, false)
_, errB := call(0, true)
```

A real client never passes *and this time be dead*. The `100 ms` the prose promised was inside a helper the reader never sees, and one function was standing in for two different services in two different states — in a chapter whose entire subject is that they are two systems.

**Decision.**
Two things.

The example was rewritten as code a reader might have written: a `charge` function taking a `context.Context`, setting its own deadline with `context.WithTimeout`, and issuing a real HTTP request. It is then called twice against two `httptest` servers, one sleeping 150 ms and one never responding. The output is unchanged in substance and now demonstrates it honestly, including that the slow service applies the charge after the client has given up.

And a rule was added to `CLAUDE.md`, under the existing verification section, naming four tells: parameters that exist to select the scenario, a number promised in prose but absent from the code, one function standing in for two systems, and harness names like `call` or `run` where the chapter is discussing a payment. The procedure is now explicit: verify with whatever is quickest, **then write the example again** in the shape a reader would recognize, and run that one.

**Why this is worth a decision entry.**
It is a distinct failure from the one decision 14 recorded. That rule says *run the code*; this one says *the thing you ran and the thing you print are two artifacts with different readers*. Following decision 14 exactly — as [chapter 06](../06_distribution_49yh.md) did — still produces this defect, because a verified harness is verified.

**A second rule, also requested.**
Expand an abbreviation on first use unless an experienced engineer would produce the long form without hesitating. `API` and `SQL` need nothing; `FLP`, `2PC`, `PACELC`, `TOCTOU`, `CQRS` get one expansion at first appearance. Where the name is initials of people, say so — FLP is Fischer, Lynch, and Paterson — because that is what the reader needs in order to search for it.

**Two substantive corrections in the same pass.**

The author flagged *reliability multiplies* as reading like a paradox, since multiplying reliability sounds like more of it. They were right that the sentence inverts its own meaning. It now reads **availabilities multiply, and every one of them is less than one**, with the section retitled *Availability is a product, not an average* and a paragraph on why the intuition fails — people average, and availability does not average because every dependency must be up at the same time.

They also asked where the transaction was in the outbox example, since only a comment claimed one, and whether `drain` had a transaction. Both were fair: the sample used Go slices with a comment asserting atomicity. It is now real `BeginTx`/`Commit` code with the two inserts inside it. And `drain` deliberately has **no** transaction spanning the publish and the delete, which the chapter now explains as the same impossibility one level down — publish-then-delete gives at-least-once, delete-then-publish gives at-most-once, and only the first is recoverable.

**Consequence.**
`CLAUDE.md` gains the verification-versus-example rule and the abbreviation rule.
`LEDGER.md` gains a row for publish-then-delete and one reworded for availability.
[Chapter 06](../06_distribution_49yh.md) runs 320 lines, up from 262.

---

## 24. AI material: distributed, not a chapter — and grilling goes to [chapter 18](../18_force-map-method_r37x.md)

**Date.** 2026-08-12

**Context.**
The author proposed a new chapter on AI-assisted development, reasoning that generated code and generated design amplify the failure modes the book catalogues, that models sound authoritative regardless of a claim's standing, and that they cannot see what is in your head.

**Is there something real.**
Yes, and it is more specific than amplification. Four findings, each an instance of a mechanism the book already owns:

- **The training corpus is a monoculture.** [Chapter 01](../01_the-five-kinds_cjx4.md) names monoculture as the single most common source of confusion and prescribes one cure — work in a second ecosystem until its conventions stop feeling wrong. That cure is structurally unavailable to a model, which has one distribution and no way to acquire another.
- **The generator cannot see your Forces**, so [chapter 02](../02_forces_f4m5.md)'s groundwork is skipped by construction rather than by carelessness.
- **Uniform confidence across all five kinds**, which is [chapter 01](../01_the-five-kinds_cjx4.md)'s first mechanism with a single generator behind it.
- **The team-size Force at its limit** — a contributor present for no conversation, retaining nothing between sessions, producing at a rate no review process was sized for. [Chapter 02](../02_forces_f4m5.md)'s migration from comment to review habit to type system is forced harder and sooner.

**Decision — distribute, do not add a chapter.**
Every finding attaches to a concept another chapter owns, so a separate chapter would be six cross-references wearing a title.
The draft argued for a chapter on the grounds that it needs one organizing mechanism the way [chapter 14](../14_principle-loses-scope_b86v.md) has one; testing that honestly, *the derivation never happened* explains the Forces finding and not the monoculture, confidence, or volume findings. There is no single mechanism, so there is no chapter.

The author raised distribution and the draft's own evidence undercut the draft's position, which is recorded here because the log is where a reversed recommendation belongs.

Distribution also ages better. A paragraph about a precondition failing survives model generations; a chapter titled for a technology is a dated object by construction.

**These are constraints, not a work queue.**
Five of the seven landing sites do not exist yet, so most of this material is blocked behind the ordinary drafting order and should not pull work forward.
The placements are recorded in `00_toc.md`'s contents lines and in `LEDGER.md`, because those are read when a chapter is drafted and this entry is not.
The two chapters already at draft — 02 and 03 — are listed under *Pending revisits* in the TOC.

**Decision — the synthesis goes in [chapter 22](../22_never-written-down_at4r.md), and grilling in [chapter 18](../18_force-map-method_r37x.md).**
[Chapter 22](../22_never-written-down_at4r.md)'s contents already list *receiving a blog post; a code review comment; a book; a colleague's strong opinion; your own past decisions.* Receiving generated code is the sixth item and the one the other five rehearse for.

Grilling is a method rather than a way of reading, so it belongs to [chapter 18](../18_force-map-method_r37x.md), the force-map method — it is that method run with a generator in the loop, and the interview is how the forces get read.

**A correction the author made, worth recording as such.**
The draft asked whether the book should take a position on whether to use these tools. The author's answer: usage is a fact, and the book does not take positions on facts.

That is the book's own model applied to the draft's question. [Chapter 01](../01_the-five-kinds_cjx4.md) defines a Force as a property of the situation, *not negotiable by argument* — so the draft had misclassified a Force as a Principle while working on the chapter that defines the difference.

**A second correction, on what grilling is.**
The draft described grilling as a review technique — interrogating a draft after it exists, probing what the text does not say. That is the author's practice in *this* repo, the `[claude …]` tags, and the draft attached the wrong name to it.

Grilling happens **before** generation. It is an interview that walks the decision tree, puts each decision to the human with a recommended answer, and does not act until there is shared understanding.

The distinction matters more than a mislabelling, because it changes the failure mode being addressed. The draft had been writing that generated code presents an Idiom in the same voice as a Law. The author's framing is sharper:

> without "grilling", I would be building a system where I didn't know the trade-offs and important decisions and where a default "recommended" decision was silently made by the AI

**Generated code does not state its decisions at all.** It arrives with every branch already taken, and a taken branch leaves no mark — there is no confident sentence to be suspicious of, because there is no sentence. Review cannot reach that, since catching a silent default requires already suspecting the branch existed. Grilling makes the branch visible before anything is written.

It also resolves something [chapter 02](../02_forces_f4m5.md) leaves open. That chapter says a model cannot see your Forces, which leaves a reader unable to act: you cannot supply the Forces in a prompt without knowing which are about to matter. The interview inverts the flow — the model surfaces the decision, the human supplies the situational fact that settles it.

The load-bearing detail is the author's: *sometimes I choose an option that was not the recommended one.* The recommendation comes from the corpus, so overriding it is a local Force beating a majority convention — possible only because the convention was made visible as a choice rather than delivered as code. FlowCore's decision 18 is the artifact of exactly that: short Go names were a corpus default that lost to a local Force once it was on the table.

**The limit, which the chapter must state.**
Grilling surfaces the decisions the model recognizes *as* decisions, and that set comes from the same corpus. A question settled uniformly across the training data does not present itself as a branch point; it is simply how things are done.

So **grilling is weakest exactly where the monoculture is strongest** — it surfaces contested choices and hides settled ones, and settled-in-the-corpus is the class most likely to be wrong outside the ecosystem it came from. This follows from [chapter 01](../01_the-five-kinds_cjx4.md)'s mechanism rather than from measurement and must be stated as reasoning, not as a finding.

Two ordinary costs alongside it: the protocol is slow by design, so it is absurd overhead on a small change; and it requires the human to hold opinions, since a user who accepts every recommendation has bought the silent defaults back with ceremony attached.

**Provenance.**
Directed by the author: cite everything, because there is no virtue in hiding it.

The skill comes from Matt Pocock's skills repository, `skills/productivity/grilling/SKILL.md`, at <https://github.com/mattpocock/skills>. The author encountered this use of it during development through Jason Ku's video, <https://www.youtube.com/watch?v=ikGhv9kKFdU&t=356s>.

The author uses a **frozen earlier version**, and the book quotes that one. It is recorded here in full, because it no longer exists upstream:

> Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.
>
> Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.
>
> If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.
>
> Do not act on it until I confirm we have reached a shared understanding.

The current upstream version was fetched on 2026-08-12 and differs materially. It organizes questions into **rounds** over a **frontier** of decisions whose prerequisites are settled, and asks the whole frontier at once with numbered questions and a fixed format. It also dispatches sub-agents to establish facts.

The two versions **disagree on one design point**, which is worth noting rather than smoothing over: the frozen version says *asking multiple questions at once is bewildering*; the current one asks a whole round at a time. The trade is throughput against how much the human must hold in working memory at once — which is a Force, and which one wins is situational. The book should say the author uses the earlier version and not imply the later one is a regression.

Worth recording that the upstream version converged on the same language independently: it ends *"every branch of the design tree visited, nothing left silently assumed."*

---

## 25. [Chapter 07](../07_scale_637f.md) organizes by shape, and reports two measurements that contradicted the plan

**Date.** 2026-08-12

**Context.**
The TOC gives [chapter 07](../07_scale_637f.md) seven topics: Amdahl, the Universal Scalability Law, Little's Law, queueing and "why 85% utilization is a cliff," the memory hierarchy with an array-of-structs benchmark, the speed of light, and big-O against constants. Written as a list it is a formula sheet.

**Decision.**
Organize by **shape**, since the shape is what decides the fix:

| Shape | Law | What to do |
|---|---|---|
| Ceiling | Amdahl | stop buying hardware, shrink the serial fraction |
| Knee where the sign flips | USL | stop adding workers, remove shared state |
| Superlinear curve | queueing | buy headroom, not speed |
| Discontinuity | cache line | look at layout, not algorithm |
| Floor | speed of light | change geography or stop waiting |

The claim follows: adding more of a resource has a shape, and intuition assumes a straight line when nothing here is one. Naming the shape converts five unrelated formulas into one diagnostic question — *which shape am I on, and where is the knee?*

**Two measurements contradicted the plan, and both are reported as found.**

**The 85% cliff does not exist.** The TOC says "why 85% utilization is a cliff rather than headroom." Computing the marginal cost of one extra point of utilization shows a smooth curve with no threshold anywhere:

```text
  50% -> 51%: wait  2.00x ->  2.04x  (+2.0%)
  85% -> 86%: wait  6.67x ->  7.14x  (+7.1%)
  95% -> 96%: wait 20.00x -> 25.00x  (+25.0%)
```

What rises is the marginal cost, continuously, from the start. 85% is a convention marking roughly where that cost becomes obvious to humans, not a threshold in the mathematics. The chapter says so and corrects the received framing rather than repeating it.

**The small-n demonstration failed.** A linear scan was expected to beat a hash map below some *n*. With string keys it never did — the map won at *n* = 4 and every size above.

Following decision 14's rule that a failed demonstration is the finding, the chapter reports it and runs the integer version, where the scan wins to about eleven elements. So **the crossover is not a property of the two algorithms**: it is set by the cost of one comparison against the cost of one hash, and string comparison is expensive enough to move the crossing off the bottom of the chart.

That makes the widely repeated *use a slice under about twenty items* a magnitude quoted without its conditions — [chapter 03](../03_grading-a-law_q5c6.md)'s exact failure, arriving unprompted in the material. The boundary section is stronger for the demonstration having failed than it would have been had it worked.

**Provenance for the measurements.**
Every number was measured on the machine the chapter was written on — an Apple M4, Go 1.26.5 — and a section before the demonstration says so, with the reason: the regularity holds everywhere and the magnitude is local, so the formulas are exact and the numbers are an instance. That is [chapter 03](../03_grading-a-law_q5c6.md)'s regularity-versus-magnitude distinction applied to the chapter's own evidence.

The AoS/SoA benchmark uses an 80-byte struct against a 64-byte cache line and shows 4.3× from field layout alone, discharging [chapter 04](../04_structure_agjy.md)'s deferral of the arithmetic and [chapter 02](../02_forces_f4m5.md)'s latency-Force pointer.

**Consequence.**
`LEDGER.md` gains nine concept rows and four example rows.
[Chapter 07](../07_scale_637f.md) runs 280 lines and moves to **in progress**.

---

## 26. [Chapter 07](../07_scale_637f.md) rewritten: jargon, a repeated example, and a prose tic

**Date.** 2026-08-12

**Context.**
The author's review of [chapter 07](../07_scale_637f.md) ran to fourteen tags and included the judgement that a rewrite might be warranted. It was. The tags were not local wording problems — three systemic faults ran through the whole chapter.

**Fault one: written for someone who already knew the material.**
The author's summary:

> An average software engineer doesn't have good depth on all of these and the points are lost trying to understand the jargon.

Terms used without definition, in a chapter whose subject is four separate specialist domains: *must run serially*, *speedup*, *bounded*, *ceiling*, *utilization*, *rho*, *queue length*, *wait scales as*, *pointer-chasing a shuffled ring*, *prefetcher*, *working set*, *dependent load*. The queueing section drew the verdict *"reads like a statistics textbook."*

The rewrite inverts the order of every section: a concrete situation first, then the number, then the formula named afterwards. Amdahl now opens with a nightly report that takes 100 minutes, 20 of them reading a file that cannot be split, and works the arithmetic out in minutes before the notation appears. Utilization is defined as the fraction of time a server is busy. The cache line is introduced as a hardware fact — the machine always fetches 64 bytes — before anything depends on it.

**Fault two: the Universal Scalability Law was asserted, not demonstrated.**
The author noted that plotting the formula gives no insight without showing when workers interfere and what that concretely means.

Correct, and the fix is a measurement that is stronger than the plot. Two million small computations spread over a growing worker pool, in two versions differing only in whether workers update one shared counter or their own:

```text
workers   shared counter    private counters
     2      72.54 M/s        179.54 M/s
     4      16.44 M/s        304.05 M/s
    64      13.33 M/s        600.24 M/s
```

Between two workers and four, throughput **falls more than fourfold** and never recovers. That is the reversal measured on the machine rather than drawn from fitted coefficients, and it shows the fix in the same table: the right-hand column is the same arithmetic without the sharing.

**Fault three: a repeated example, which is a ledger violation.**
The chapter reused [chapter 04](../04_structure_agjy.md)'s `Particle` struct for the memory-layout benchmark. The ledger had split the two — 05 owns the encapsulation argument, 08 owns the arithmetic — but using the same struct made it read as the same example twice.

The author's rule, which is worth keeping: if two chapters share a *shape*, keep the shape and change the example, so it does not land as "oh, the particle thing again."

Replaced with summing one field across two million order records, which is the book's running domain (orders appear in [chapters 02](../02_forces_f4m5.md) and 07) and gives a **7.1×** difference against a 120-byte record. It also connects outward: this is why analytics databases store columns rather than rows.

**A prose tic, and a new rule.**
The author flagged two paragraphs as *"the pinnacle"* of an AI prose style and asked for a `CLAUDE.md` entry against it.

The pattern is every paragraph landing on a closing turn — setup, pivot, epigram. Fine once; run for forty paragraphs it becomes a rhythm the reader hears instead of the argument. `CLAUDE.md` gains *Vary the cadence* under the register section, naming five tells: a closing clause beginning "which is why," the *it is not X, it is Y* construction, announcing a count before delivering it, a final sentence engineered to be quotable, and the rule of three.

The instruction is not to delete every turn but to **let most paragraphs end flat**, keeping one where the argument genuinely turns. The rewritten chapter uses "which is why" once, down from four.

**Also corrected.**
The epigraph said *grades*, which decision 17 replaced with *kinds* — a regression against a recorded decision, caught by the author.

**Consequence.**
[Chapter 07](../07_scale_637f.md) runs 338 lines, up from 280, almost entirely in definitions and worked setup.
`LEDGER.md` has one example row replaced and three added.

---

## 27. [Chapter 08](../08_change_rjf9.md) organizes by rate of change, and grades Lehman honestly

**Date.** 2026-08-12

**Context.**
[Chapter 08](../08_change_rjf9.md) covers Lehman's laws, Conway's Law and the inverse manoeuvre, Brooks's Law, and compatibility. Four results from four different literatures, with no obvious connection beyond operating on long timescales.

**Decision.**
Organize by **rate of change**: code changes daily, schemas monthly, published interfaces rarely and never backwards, organizations yearly and expensively. The claim follows — everything changes, but not at the same rate, and the slow parts set the terms for the fast ones.

That gives the chapter a usable test (*which layer does this decision land in?*) and puts the four laws in an order that explains itself. It also keeps clear of [chapter 02](../02_forces_f4m5.md), which owns durability as a **Force** — 03 asks whether a mistake stays correctable, 09 asks what governs change across years and adds the organization, which 03 does not cover.

**The compatibility demonstration, and what it turned up.**
An old client against four server changes, run rather than described:

```text
ADD an optional field:   parsed fine
RENAME a field:          amount=0, err=<nil>
CHANGE a type:           err=cannot unmarshal string
ADD a new enum value:    parses, client has no branch for it
```

The rename is the finding. It produces **no error and a zero amount** — a payment of nothing, reported as a successful parse. The type change, by contrast, fails loudly and gets fixed within the hour. So the ordering of danger is the opposite of the ordering of noise, which is not obvious before seeing it.

**Go's standard library as dated evidence.**
`io/ioutil` was deprecated in Go 1.16, February 2021. It was compiled and run under Go 1.26.5 for this chapter and works. Counting the standard library gives **175 declarations marked deprecated** across 85 files — each one something the maintainers would remove and cannot.

That is better than an assertion about compatibility promises: it is checkable, dated, and it quantifies the cost of keeping one.

**Lehman is graded rather than recited.**
There are eight of Lehman's laws and they are not equally solid. The chapter uses two — continuing change, and increasing complexity — and says plainly that the study population was mainframe systems decades ago with release cycles measured in years, and that several of the others ("conservation of familiarity," "conservation of organizational stability") are vague enough to resist checking.

This follows [chapter 03](../03_grading-a-law_q5c6.md)'s empirical-law framing applied to the book's own sources: an empirical law carries a study population, and citing all eight equally would repeat the error the book exists to describe.

The same treatment is given to the inverse Conway manoeuvre. Conway's observation is established; the claim that architecture can be driven by reshaping teams is a strategy rather than a finding, and the chapter says so.

**Two things the chapter adds that were not in the TOC.**

*Lehman's ratchet has a mechanism.* Complexity rises because the costs are asymmetric: adding a case is cheap and local, removing one requires establishing that nothing depends on it. Additions happen continuously; removals need a project.

*One constraint here is unlike everything else in the book.* Every other law can be satisfied by changing code you control. Compatibility cannot, because **you cannot deploy other people's software** — the code that must change is on a machine you cannot reach, owned by someone with no reason to hurry.

**Consequence.**
`LEDGER.md` gains seven concept rows and three example rows.
Part II is complete: [chapters 03](../03_grading-a-law_q5c6.md) through 09 are drafted.
[Chapter 08](../08_change_rjf9.md) runs 219 lines and moves to **in progress**.

---

## 28. Conway's mechanism corrected, and Brooks given its actual condition

**Date.** 2026-08-12

**Context.**
The author's review of [chapter 08](../08_change_rjf9.md) raised eight points. Two were challenges to the substance, and both found real defects.

**Conway's mechanism was written so that it implied something absurd.**
The draft's illustration set two engineers at neighbouring desks, who build tightly coupled code, against two teams in different time zones, who build a versioned interface. The author's objection:

> Does this mean that the only way to develop maintainable software with a team is to let each team member talk to each other in carefully crafted messages, in given times, in preset conversational topics? To me this logical extension sounds absurd.

It is absurd, and the draft had earned it. The two examples were written with the low-friction case as the bad outcome and the high-friction case as the good one, which smuggles a value judgement into a law that has none. Conway's Law describes; it does not recommend friction.

Rewritten so the point is that **neither outcome is better in itself.** Tight coupling between things that genuinely are one thing is correct. A firm interface between things that genuinely are separate is correct. What the law predicts is a **mismatch** — your software gets its seams where your organization has its seams, whether or not the problem has seams there — and both directions of mismatch are now given: one team owning what should be two things, and two teams owning what should be one.

The illustration is also now marked as this book's rather than Conway's, since his 1968 paper argues the general claim and the desks-and-time-zones mechanism is one ordinary way it comes about.

**Brooks's Law was stated without the condition that makes it true.**
The author posed a thought experiment: a project estimated at 100 hours, two people, 120 hours spent and not finished. One manager says 80 hours remain; another says the estimate was wrong and 988 remain. Is it late in Brooks's sense in both cases? Does adding people hurt in both?

Working it rather than answering from intuition produced the sharper statement the chapter was missing:

```text
A:  80h remaining    2 people:  8 days    +1 person:  9 days   -> later
B: 988h remaining    2 people: 99 days    +1 person: 71 days   -> sooner
```

Same team, same hire, opposite answers — and sweeping the remaining work puts the break-even at roughly the length of the ramp-up itself. So:

> **"Late" means the remaining work is shorter than the time it takes a new person to become useful.**

That is not the same question as *are we behind schedule*, and the two come apart precisely in case B: a project badly behind a wrong estimate is not late in Brooks's sense, it is under-staffed, and the fix is people added now rather than later, since the ramp-up cost is fixed and the runway only shrinks.

The ramp-up figures are marked illustrative rather than measured, with the note that substituting your own moves the break-even — which is the reason to compute it rather than quote it ([Ch. 03](../03_grading-a-law_q5c6.md)).

**An expansion the author asked for, and the ledger allowed.**
They asked whether one-team-per-service deserved treatment here. Nothing else in `LEDGER.md` owns organizational structure, so it landed in 09.

The section states the heuristic's real content and the two ways it is misapplied: many services owned by one team is fine, one service owned by many teams is the failure it prevents, and services sized to the team chart is the failure it causes. The honest form is that it constrains **who may own a service**, not **how many services there should be**.

**Smaller corrections.**
A sentence reading as an instruction to the writer — *cite the two, treat the rest as observations of their era* — was removed. Go struct tags are now explained, with the Java and C# equivalents, which is the audience rule applied in a chapter drafted after that rule was added. And the demonstration now says the server sends the new shape in every case and the output is what the client makes of it, since the draft said "reaches" while the output said "parsed."

**Consequence.**
[Chapter 08](../08_change_rjf9.md) runs 278 lines, up from 219.
`LEDGER.md` gains three concept rows and one example row.

---

## 29. Conway's mechanism is ownership, not communication distance

**Date.** 2026-08-12

**Context.**
The chapter's account of *why* Conway's Law holds was rewritten once already (decision 28) and was still wrong. The author rejected the second version too:

> Everybody works with messaging apps like Slack, many devs and teams work remotely. A neighbouring desk is rarely seen as quick communication nowadays. Also you make this sound like inevitable but I doubt it. Two good engineers at neighbouring desks will talk about many different things but will build the right structure the situation demands. I don't see an invisible force between the desks, tempting them to not use an interface when it's obviously the right solution.

Two separate objections, both correct. The illustration was dated, and — more seriously — the mechanism it described was implausible: it framed the law as a *temptation acting on individual engineers*, which invites the obvious reply that competent engineers are not tempted.

**Decision.**
Replace communication distance with **ownership** as the mechanism.

Work must be divided before it can start, and dividing it is already a decomposition of the system — you cannot hand out the work without partitioning the design. That partition is usually settled before anyone has read the problem closely, by whoever was arranging the work rather than by anyone who would call it architecture.

What makes it stick is an asymmetry in who may change what. A boundary **inside** one owner's area can be moved on a Tuesday afternoon by the person who noticed it. A boundary **between** owners requires persuading another team to reopen something settled, reschedule committed work, and accept a change with no benefit to them this quarter. So internal boundaries stay fluid and shared ones calcify.

**Why this answers the objection rather than dodging it.**
It explains why good engineers do not escape the law. Two excellent engineers owning the two halves of a badly split problem will each build their half well; neither is positioned to see that the split was wrong, and the one who does see it cannot fix it, because it is not an engineering decision they are permitted to make.

It also survives the tooling objection completely. Slack changes the cost of talking. It does not change who owns what, and the constraint was never the cost of talking — it is that agreement is required at all.

**A related correction.**
The author queried "the result is correct" in the one-owner-two-parts case, objecting that building separable things as one is not correct. Right — the word was doing two jobs. The passage now says nothing is broken and every test passes, which is why nobody notices, until the two need to ship on different schedules or one has to be replaced.

**Attribution.**
The ownership mechanism is the draft's; the two objections that forced it are the author's, and the second version would have shipped without them. Conway's 1968 paper argues the general claim, and the chapter now marks the mechanism as this book's account of why it holds rather than implying it is Conway's.

**Consequence.**
`LEDGER.md` gains a row for the ownership asymmetry.
[Chapter 08](../08_change_rjf9.md) runs 289 lines.

---

## 30. Conway checked against the source, and quoted

**Date.** 2026-08-12

**Context.**
Having accepted the ownership mechanism, the author raised the obvious problem with it:

> law says "...copy their own communication structures." We say "Ease of communication does not help", "The mechanism is not about communication being easy or hard" and then we show the "ownership" problem. I didn't read Conway's work but I suspect this is a respectable stretch. If it isn't, maybe we should just drop Conway's law from the book and frame this "law" for what it is.

A fair challenge: the chapter was contradicting the words of the law it was citing, which is the misattribution the book's provenance rule exists to prevent.

**Decision.**
Fetch the paper rather than reason about it. Conway's own account of the mechanism settles it:

> If there is a branch, then the two […] design groups X and Y which designed the two nodes must have **negotiated and agreed upon an interface specification** […] If, on the other hand, there is no branch between x and y, then the subsystems do not communicate with each other, there was nothing for the two corresponding design groups to negotiate.

*Negotiated and agreed upon.* Conway's "communication structure" is not about how easily people can reach each other — it is about which design groups had to settle something between them. The ownership reading is his mechanism in modern vocabulary, not a stretch.

So the chapter now quotes him directly, with a short passage explaining that "communication structure" is easy to misread and what he meant by it. It also quotes the consequence, which is stronger than anything the draft had written:

> Given any design team organization, there is a class of design alternatives which cannot be effectively pursued by such an organization because the necessary communication paths do not exist.

**Attribution corrected in the other direction.**
Decision 29 recorded the ownership mechanism as the draft's. That over-claimed. The negotiation mechanism is Conway's; what this book adds is the asymmetry that makes a partition stick — free to move inside one owner, expensive across — and the translation of "design groups" into teams. The chapter's note now says exactly that.

**Worth recording as method.**
Two rounds were spent rewriting an explanation of Conway's Law without reading Conway. The second rewrite was defensible and still could not answer *is this what he said*, which is the question the author asked. Fetching the source took one call and produced a better section than either rewrite, because his own words are more precise than the paraphrase — *negotiated and agreed upon* is the phrase the whole argument turns on.

The book's rule is mechanism over authority, which is about not using citation as proof. It is not a licence to skip reading the thing being cited.

**Consequence.**
[Chapter 08](../08_change_rjf9.md) runs 301 lines.
`LEDGER.md`'s row is reworded: the mechanism is negotiation, and it is Conway's.

---

## 31. The author read the source; the paper had a better example than the draft invented

**Date.** 2026-08-12

**Context.**
After decision 30, the author read Conway's paper themselves and returned with excerpts, an interpretation to check, and the instruction to decide what was worth using.

Their reading — that "linear graph of a system" means the architecture and its components, and "linear graph of its design organization" means teams and ownership boundaries — is correct against the source. Conway maps *system* to *committee*, *subsystem* to *subcommittee*, and *interface* to *coordinator*, and says of the system graph that "each node is a subsystem which communicates with other subsystems along the branches."

**What was added, and what was left out.**

Two of the excerpts earn their place.

The **homomorphism** is more precise than "copies": every subsystem corresponds to a design group and every interface to a negotiation. It is a structure-preserving map, and it runs in one direction.

The **COBOL/ALGOL example** is the strongest thing in the paper and better than anything the draft had written. Five people on a COBOL compiler and three on an ALGOL compiler produced a five-phase compiler and a three-phase compiler. Nobody chose the phase count; it was chosen when the people were assigned.

Left out: "stamps out an image of itself in every design it produces," which is rhetoric adding nothing over the homomorphism, and the two military services producing a copy of their organization chart, which is funny but less precise than the compiler example. One demonstration is enough; the second would be padding.

**An unplanned payoff.**
The homomorphism runs *from* the system *to* the organization, and following that direction settles a heuristic the chapter had already stated informally. A map in that direction gives every subsystem exactly one design group — so several subsystems may share a group, and none may have two. That is precisely *many services per team is fine, one service across many teams is not*, which the chapter had argued from experience two sections later.

Marked as this book's reading. Conway states the homomorphism and does not draw the consequence out.

**Consequence.**
`LEDGER.md` gains a row for the homomorphism and its direction.
[Chapter 08](../08_change_rjf9.md) runs 311 lines.

---

## 32. Read the source before explaining why someone else's result holds

**Date.** 2026-08-12

**Context.**
[Chapter 08](../08_change_rjf9.md) explained Conway's Law twice without reading Conway, and the author asked for a rule that would prevent it.

**What actually happened.**
The first attempt described the law as a temptation acting on individual engineers; the author rejected it as implausible, since competent engineers are not tempted into bad structure. The second replaced that with an ownership mechanism. It was defensible, survived scrutiny, and still could not answer the question the author then asked — *is this what he said*. Only fetching the paper settled it.

**Decision.**
A rule in `CLAUDE.md`, placed directly after *Mechanism over authority*, because the two are easily confused and the second was being read as licence for the first failure.

Naming a result is one thing. Explaining its mechanism, or saying what its terms mean, is another. The trigger is writing a sentence of the form *the mechanism is…*, *what X actually meant was…*, or *the reason this holds is…* about a named law or argument. At that point, read it.

**Why the rule is worth its cost.**
Two reasons, and the second is the one that decides it.

The paraphrase is less precise than the original. *Communication structures* is vague; Conway's *negotiated and agreed upon an interface specification* is not, and the entire argument turns on that phrase.

And **the source contains material nobody would have invented.** The five-phase and three-phase compilers are better than the draft's illustration, and were sitting in the paper through two rewrites of a section about that paper.

**Boundary.**
Where a source genuinely cannot be reached — paywalled, offline, out of print — say so in the chapter's review notes and keep the claim to what is uncontroversially attributed, rather than explaining a mechanism from inference.

**Attribution.**
The failure and the rule are both the draft's; the author identified the pattern and asked for the rule. The correction that started it — reading the paper and returning with excerpts — was theirs.

---

## 33. A pattern is not one of the five kinds

**Date.** 2026-08-12

**Context.**
[Chapter 09](../09_what-a-pattern-is-for_3xzc.md) opens Part III and has to say what the two tests are testing. The book's model classifies claims into five kinds, and the obvious move was to ask which kind a pattern is.

**Decision.**
None of them, and the chapter says so in its first line.

Law, Force, Principle, Idiom, and Style classify **claims** — things capable of being true, false, or conditional. A pattern is a **name for a shape**, and names are not true or false. The trouble starts when a name is used as though it were a claim, which is the subject of the rest of Part III.

That is worth stating rather than glossing, because a reader arriving from Part II will reasonably try to run the classification test on *Repository* and find that it does not fit. The answer is that the question is malformed.

**The two tests, and one thing the TOC did not anticipate.**
The TOC gives compression and constraint. Drafting them showed they are **independent**, which the plan had left implicit and which turns out to be the useful part.

*Facade* is the case that proves it: it compresses well — one word for "an object providing a simplified interface to a larger body of code" — and forbids nothing. Any object that calls several things and exposes fewer methods qualifies. So the tests give four outcomes rather than a single axis, and the top-right cell (compresses, constrains nothing) is where most pattern arguments happen, because those names feel informative while excluding nothing.

**Both tests are made mechanical**, since a test nobody can run is a slogan.

Compression is counted in words: *Transaction Script* is two words standing for twenty-six, a ratio of 13:1, while *Manager* has no agreed description to stand for — the failure is not that the word is short but that there is nothing specific behind it.

Constraint is tested by trying to write the code the name forbids. Singleton forbids a second instance; Transaction Script forbids a loaded entity graph carrying the rule; Facade forbids nothing anyone could write down.

**A condition on compression that is easy to miss.**
The saving exists only for a reader who already knows the term. Introducing a name costs its definition plus the name, so a term coined inside one codebase compresses nothing for anyone outside it. Compression is therefore a claim about shared vocabulary rather than about a word, and the boundary section keeps local vocabulary as legitimate rather than treating it as a lesser thing.

**Provenance.**
The vocabulary-versus-prescription distinction and the Transaction Script compression example come from the FlowCore architecture dialogue at `~/c/TechIter/01/coding-style-architecture.md`, where the author worked them through — including the observation that a catalogue is ethnography, and that a name's other value is as an index into the literature on its failure modes.

Two things from that document are deliberately left alone: *anemic domain model* as a term that smuggles a verdict belongs to [chapter 13](../13_smuggled-verdicts_8y69.md), and *does the idea come with the conditions under which it's wrong* belongs to [chapter 14](../14_principle-loses-scope_b86v.md).

**Consequence.**
`LEDGER.md` gains six concept rows and two example rows.
[Chapter 09](../09_what-a-pattern-is-for_3xzc.md) runs 181 lines and moves to **in progress**.

---

## 34. The teaching boundary does not survive, and is replaced

**Date.** 2026-08-12

**Context.**
The TOC promised [chapter 09](../09_what-a-pattern-is-for_3xzc.md) a boundary at teaching: *a name with low information content is still a useful handle for a beginner.* The draft wrote it that way. The author rejected the argument:

> what can you realistically teach with a name that doesn't compress and doesn't forbid? This is a facade. Ok so what? […] in fact most of the times it clouds the learning because the reasons — principles behind that shape is not identified. […] Then you never encounter that particular requirement in real life and you forget the pattern even exists.

**Decision.**
The objection holds and the boundary is removed.

Attempts to steelman it all collapse into a boundary the chapter already had. The strongest version — that a name gives a learner something to recognize the shape by later — fails on the author's point that recognition without the reason is not usable knowledge: you can identify a Facade and still not know when a simplified interface is the right move, what it costs, or how to design a good one.

What survives is narrower and is folded into the *search* boundary: a name a learner can look up is a door into the discussion of when the shape fails, and a name without that discussion attached is a sound they can make in a meeting. The chapter now says the widely assumed opposite is wrong, and connects the failure to [chapter 14](../14_principle-loses-scope_b86v.md)'s mechanism — a compressed judgement, repeated without its conditions, becomes a slogan.

**The replacement boundary is the author's, from a separate note.**
Commenting on *naming precisely costs more than naming vaguely*, they added that a vague name is sometimes the right move because the design is not mature enough to decide, and that waiting for a little more functionality often turns four awkward things into three natural ones.

That is a genuine counter-example to the chapter's claim, and a better one than teaching: **the two tests assume you can say what the code does.** Before that is true, a precise name is a claim you have not earned. The chapter states the failure precisely — not the vague name, but losing track that it is provisional — and borrows [chapter 02](../02_forces_f4m5.md)'s device for any deferred decision: write down what would have to become true for the name to be settled.

**Two smaller corrections.**
The constraint demonstrations now show what each name *permits* before what it forbids, at the author's suggestion, which makes the forbidden case legible rather than requiring the reader to infer the permitted one.

And the failure list's `strategies/` entry now carries its reason, which the author could see was a failure but not articulate: **a directory should group things that change together, while a pattern name groups things that are shaped alike.** So every feature change reaches into a folder holding other features' code.

**Consequence.**
`00_toc.md`'s boundary line for [chapter 09](../09_what-a-pattern-is-for_3xzc.md) is rewritten, since the promised boundary is gone. The TOC now names the three that survive.
`LEDGER.md` gains two concept rows and one reworded.
[Chapter 09](../09_what-a-pattern-is-for_3xzc.md) runs 202 lines.

---

## 35. The scale test's axis is ownership, not size

**Date.** 2026-08-12

**Context.**
The TOC frames [chapter 10](../10_patterns-that-cross_r8dw.md) around scale: the same name is trivial at class scale and load-bearing at system scale, with Adapter becoming an Anti-Corruption Layer. Written literally, "scale" means size, which is wrong in a way that would have made the chapter unusable — a fifty-line integration with a vendor is system scale, and a thousand-line internal refactor is not.

**Decision.**
State the axis as **ownership**: can you change the other side?

Class scale means both sides are yours — same repository, same deploy — so if two things do not fit you may change either. System scale means one side is not yours to edit: a vendor's API, another team's service, a published format.

That reframing does three things the size framing cannot. It explains why a small integration is a serious commitment and a large refactor is not. It connects the chapter to material the book already owns — [chapter 02](../02_forces_f4m5.md)'s control-of-the-callers Force and [chapter 08](../08_change_rjf9.md)'s *you cannot deploy other people's software*. And it produces the diagnostic the chapter ends on, which is a question with an answer rather than a judgement call.

**The insight that carries the demonstration.**
What makes Adapter cheap at class scale is not the line count. It is that **a third option exists**: change the other side so no adapter is needed. Rename the method, change the signature, move the parameter.

At system scale that option is gone, and the pattern stops being one fix among several and becomes the only move. That is the whole difference, and it is why the same word denotes a convenience in one place and a maintained translation layer in the other.

**What the scale table is actually tracking.**
Drafting the table showed that the second column is not "the same thing but bigger." Every entry acquires a **failure mode** that the class-scale version does not have — the vendor changes without asking, the surface becomes a commitment, delivery can fail or repeat, the call can be slow or partial.

Those are Part II's Laws arriving one at a time. So the table's last column names them, and the chapter can say what it is really about: a pattern name transfers the shape and drops the Forces, and the Forces were the expensive half. That is [chapter 01](../01_the-five-kinds_cjx4.md)'s mechanism — advice stripped of its conditions — in a new place.

**Both demonstrations were run.**
Go's structural typing satisfying `querier` with two vendor types and zero wrapper code, against the C# shape that needs a class and two forwarding methods per type. And the Stripe status leaking into three call sites versus stopping at one translation function, with the counts taken from the file rather than asserted.

**A question [chapter 09](../09_what-a-pattern-is-for_3xzc.md) left open is answered here.**
[Chapter 09](../09_what-a-pattern-is-for_3xzc.md) used Facade to show that compression and constraint are independent — it compresses well and forbids nothing — and handed the scale question forward. The answer: at class scale a facade is a word for a wrapper; at system scale it is what other teams call, so [chapter 08](../08_change_rjf9.md)'s compatibility rule applies and it may be added to but never narrowed. The name did not change; the commitment did.

**The boundary section found a genuine asymmetry.**
The TOC asked for patterns trivial at every scale. The test that works is whether you can state the system-scale version at all — Strategy and Template Method have none, because nothing about passing a function becomes unreliable when the program grows.

Singleton turns out to do the opposite, and is worth the contrast: at system scale "exactly one" means one across a cluster, which is leader election, which needs consensus. It does not stay trivial; it becomes one of the hardest items on the list under an unchanged name.

**Consequence.**
`LEDGER.md` gains six concept rows and two example rows.
[Chapter 10](../10_patterns-that-cross_r8dw.md) runs 222 lines and moves to **in progress**.

---

## 36. [Chapter 10](../10_patterns-that-cross_r8dw.md) fought its own vocabulary; the word "scale" is now the thing being corrected

**Date.** 2026-08-14

**Context.**
The author traced their confusion through the chapter's opening sentence by sentence:

> "size matters, five line convenience" → *size of involved code is important I guess*
> "the scale decides" → *oh it's not size of code but scale. What scale?*
> "not how much code is involved. It is whether you can change the other side" → *ok not size, not scale but whether you are on an integration point*
> "two scales: class — system" → *ok not integration point but the size of the component matters*
> "the size is not what changes the answer" → *does the author even know what his point is?*

**The diagnosis.**
The draft argued that the deciding axis is ownership while continuing to call it *scale*, and while naming its two ends **class scale** and **system scale** — terms that denote size. Twenty-one occurrences across the chapter. So the prose spent four paragraphs contradicting its own vocabulary, and a reader following the words rather than the argument arrives exactly where the author did.

This is decision 17's failure in a new place: vocabulary that has to be decoded and that contradicts what it labels.

**Decision.**
Delete the terms. The two ends are now described rather than named — *both sides yours*, *the other side is theirs* — because coining a replacement term invites the same decoding problem.

And confront the word in the opening rather than working around it. The chapter now says people call this a question of scale, that this is close enough to be misleading, and why: size correlates with the thing that matters because systems acquire other owners as they grow, but reasoning from size gives wrong answers in both directions.

The title stays. *The Scale Test* now names the received framing the chapter examines, which is the same move [chapter 04](../04_structure_agjy.md) makes with "layered architecture" — worth flagging to the author as reversible if they would rather the title matched the conclusion.

**One running example, replacing two borrowed ones.**
The author objected that the `querier` demonstration had already been used repeatedly — it appears nine times in [chapter 04](../04_structure_agjy.md) — and suggested one coherent example carrying the whole chapter, sketching it as *we own FastSell and have our own payment processor, then we switch to Stripe*.

Adopted as sketched. FastSell's own `Receipt` and `LedgerEntry` for the owned case, then the same problem after moving to Stripe. That is better than two static examples because it shows **the transition** — the moment an option disappears — rather than two unrelated states, and the pattern's shape is identical on both sides of it, which is the chapter's whole point.

**The third option is now shown rather than asserted**, at the author's request. The owned case gives the adapter, then gives the better answer as code: rename two fields in `payments.Receipt` and delete the adapter. Seeing the alternative is what makes its later absence land.

**Counts taken mechanically.** Six sites test Stripe's vocabulary without a boundary, one with. Both versions were run and produce identical output, which is worth having — the boundary costs nothing functionally, so its whole value is what happens on the day the vendor changes.

**Consequence.**
`LEDGER.md` has five rows reworded and three examples replaced.
[Chapter 10](../10_patterns-that-cross_r8dw.md) stays at 222 lines; almost all of it is different.

---

## 37. [Chapter 10](../10_patterns-that-cross_r8dw.md)'s axis is [chapter 02](../02_forces_f4m5.md)'s Force, and the pattern table is graded

**Date.** 2026-08-14

**Context.**
Sixteen review notes. Three of them were challenges to whether the chapter was sound rather than to how it read, and answering those changed the chapter's relationship to the rest of the book.

**The axis was already in the book, and the chapter had not noticed.**
The author asked whether *can I change the other side* is one of the seven Forces, and if so which.

It is. [Chapter 02](../02_forces_f4m5.md)'s **control of the callers** asks whether you can change everyone who calls you; [chapter 10](../10_patterns-that-cross_r8dw.md) asks whether you can change what you call. Same Force, same three settings, pointed the other way — which the chapter now says explicitly rather than presenting the axis as new.

The same oversight produced the repetition the author flagged separately. The *partial ownership* boundary had re-derived [chapter 02](../02_forces_f4m5.md)'s middle setting — *you can see them but not change them* — in fresh words, which is precisely what `LEDGER.md` exists to prevent. It now cites 03 for the three settings and spends its space on what the middle one does to the pattern question: a temporary forwarding method with a removal date, which is neither an adapter nor a permanent translation layer.

**The pattern table is now graded rather than asserted.**
The author asked whether the table was solid or this book's theory, and separately whether a message bus is really Observer with a network in it or only a surface resemblance.

Checked row by row, and they are not equally supported:

- **Proxy** is canonical. The Gang of Four list a *remote proxy* — "a local representative for an object in a different address space" — among the pattern's named variants. Crossing the line was in the original definition.
- **Adapter** is supported by the anti-corruption layer literature; Evans describes such a layer as containing translators.
- **Facade** is this book's extension, and is marked as such. No catalogue says a facade becomes a public API.
- **Observer is the weakest, and the author's suspicion was right.** A broker is genuinely new structure, and the publisher stops holding references to its subscribers — a change in mechanism, not only in what can fail. The chapter now calls it a family resemblance rather than the same pattern relocated.

Grading the rows turned out to strengthen the chapter rather than weaken it, because the distribution is informative: **the rows that survive best are the ones where nothing structural is added.** That is a condition on when this reading applies at all, and it was not visible while every row was asserted equally.

**Singleton expanded, at the author's request.**
Their question was what invariant ties one object in one process to consensus across machines, given that a cluster obviously *has* many machines. The answer needed stating: the singleton is in the **role**, not the hardware — exactly one machine running the billing job while the others stand ready. The shared invariant is *at most one holder at a time, and everyone agrees which one*, and both halves are free in one process and expensive across machines, for reasons [chapter 06](../06_distribution_49yh.md) owns.

**A claim that was simply wrong.**
The draft said a ten-thousand-line refactor is not a serious commitment. The author rejected that, correctly. The point being reached for was about *kinds* of expense: a large refactor is a large piece of work that ends, while a small integration is a standing obligation that does not. Rewritten to say that.

**Title.**
Changed by the author to *Patterns That Cross The Line*, on the grounds that [chapter 07](../07_scale_637f.md) is already called *Scale* and using the word here is confusing when the chapter argues it is the wrong word. Kept, with the TOC entry, the ledger row, and [chapter 09](../09_what-a-pattern-is-for_3xzc.md)'s two forward references updated to match.

**Consequence.**
[Chapter 10](../10_patterns-that-cross_r8dw.md) runs 302 lines, up from 222, almost all of it in the graded table, the Singleton expansion, and worked code for the facade and partial-ownership cases the author asked to see rather than be told about.

---

## 38. Reviewing the author's edits found a real imprecision in the facade example

**Date.** 2026-08-14

**Context.**
The author's third pass on [chapter 10](../10_patterns-that-cross_r8dw.md) was direct edits only, with no tags, plus a file rename. They asked for the edits to be reviewed rather than absorbed.

**Their catch, which was substantive.**
The draft said that once the orders object is exposed over HTTP, *you may not rename `Place`*. That is false, and the author's edit — changing it to "the endpoints `Place`" — was reaching for the right correction even though the wording conflated two things.

`Place` is a Go method name and stays entirely yours: rename it, adjust the routing line, and nobody outside notices. What is now in somebody else's source is `POST /v1/orders` and the shape of the JSON body.

So the example was making the chapter's own error in miniature — treating "the facade" as one undivided thing when the published surface is only part of it. Rewritten to draw the line explicitly:

```text
still yours     the method name, its parameters, everything behind it
now theirs      the route, the field names on the wire, which are optional
```

That is a better demonstration than the original, because it shows the boundary falling *inside* what the pattern name covers — which is exactly the information the name omits.

**Three edits kept, with mechanical fixes.**

*"You can rename … with reasonable effort. You just have to fix the call sites"* is better than the draft's phrasing, which implied renaming is free. Kept; the typo *Imaging* corrected to *Now imagine*, and a trailing space removed.

*"The name of the pattern did not change"* fixes a duplicated sentence the draft had left in — the same clause appeared twice, once with a full stop and once with a semicolon. Their version is right and the duplication was the draft's error.

*"Singleton is a notable exception"* is shorter and clearer than the draft's "the exception to this exception," which was cute and hard to parse. Kept, with the comma splice repaired and the referent named, since the point of the original tag was that a reader inside *Where this doesn't apply* needs to know what Singleton is an exception **to**.

**Housekeeping.**
The file was renamed `10_the-scale-test.md` → `10_patterns-that-cross_r8dw.md`. Two references in `00_toc.md` still pointed at the old name and are updated.

**Worth recording about process.**
The instruction was a reminder: *always check my direct edits as well.* This pass is why the rule exists — one of five edits contained a correction the draft would have absorbed silently, and following it through produced a better example than either version had.

---

## 39. [Chapter 11](../11_patterns-that-survive-translation_us2k.md) is not a catalogue

**Date.** 2026-08-14

**Context.**
The TOC planned [chapter 11](../11_patterns-that-survive-translation_us2k.md) as a graded catalogue: roughly sixty patterns, each with a definition, the constraint it imposes, a code demo, and its Force. Drafting it as specified would have produced four problems at once.

It **re-covers owned material** — the Outbox, Saga, and Idempotency Key are [chapter 06](../06_distribution_49yh.md)'s; the Anti-Corruption Layer is 11's; Transaction Script is 10's compression example; the test-double taxonomy is 17's; data-oriented layout is 05's and 08's. A catalogue explains them again, which is what `LEDGER.md` exists to prevent.

It **has no claim.** The rubric requires one sentence the chapter demonstrates, and sixty entries have sixty. The TOC's own boundary line conceded it: *each entry carries its own boundary* is not a boundary section.

It **undercuts [chapter 09](../09_what-a-pattern-is-for_3xzc.md)**, which argues that a name earns its place by compressing and ruling something out. Listing sixty names without applying those tests contradicts the chapter two before it.

And it **overlaps [chapter 12](../12_missing-language-features_esqm.md)**, which owns *if it disappears when you change language, it was a workaround*. The catalogue as planned is the positive cases of that same test.

**Decision.**
Keep the material and replace the organizing idea. The claim is that **the patterns which last are answers to Forces, and grouping them by Force finds the name from the situation** — the direction that is actually useful, and the one a catalogue organized by shape cannot serve, since it can only be searched by a name you already have.

**The coverage question, put to the author.**
The first proposal had two or three exemplars per Force, about fifteen patterns. They asked whether that meant all the patterns or a select few, which surfaced the real objection: a reader can reply *you picked the ones that fit your grouping*.

Resolved by splitting the entries in two. **Worked** entries — two per Force, with code, constraint, and cost — carry the argument. **Listed** entries — the rest of each family, one line each — are placed rather than explained, and their job is evidence: if fifty patterns sort into six Forces, the grouping covers the field rather than the chosen cases. Patterns another chapter owns appear with a pointer instead of a definition.

**The sort was done before the chapter was written, and produced the boundary section.**
Forty-three patterns fall into six Forces. Seven refuse, and they fail in two distinct ways, which is more useful than a tidy result would have been.

Some answer a **goal** rather than a situation — golden tests, property-based testing, the test-double taxonomy, functional core / imperative shell. All answer *how will I know this works*, which is something you want, not a fact about where you are standing. [Chapter 02](../02_forces_f4m5.md) is explicit that a Force is not negotiable by argument; testability is.

Some answer the **shape of the problem** rather than the situation. A state machine is right when the domain has states and transitions, which is a fact about the business. Transaction Script is what you write when no Force pushes you anywhere else.

So the chapter's claim is stated in its narrower true form, and the boundary section names the three-way distinction — Force, goal, problem shape — as one way people end up applying machinery to a question they were not asking.

**Verification.**
Most entries are structural, which needs no run. The one behavioural claim was measured: at a millisecond per round trip, a thousand rows takes 1,145 ms one call at a time and 11 ms in batches of a hundred.

**Consequence.**
`00_toc.md`'s entry for [chapter 11](../11_patterns-that-survive-translation_us2k.md) is rewritten, since the planned chapter no longer describes this one.
`LEDGER.md` gains four concept rows and six example rows.
[Chapter 11](../11_patterns-that-survive-translation_us2k.md) runs 385 lines, the longest so far, against 600–900 for the catalogue it replaces.

---

## 40. The chapter epigraphs are removed

**Date.** 2026-08-14

**Context.**
Every chapter from 02 to 12 opened with an italic paragraph before the claim, stating what kind the chapter's material was — *this chapter is **Law**, and mostly of the definitional kind*. The author's objection was about reading, not content:

> I find the introductory sentences in italics in each chapter unbearable. They are like the famous paperclip character on old Word, popping suddenly and giving marginally useful data when you are trying to focus on an important task.

**Decision.**
Remove all eleven. Every chapter now opens directly on its claim.

**Why the objection holds even though the content was defensible.**
The convention had a real justification: this book argues that you should know what kind of claim you are holding, so a chapter announcing its own kind is the book practising what it preaches. `LEDGER.md` even recorded it as sanctioned repetition.

But the placement was wrong, and that is what the author identified. *This chapter is Law of the strictest kind* means nothing to a reader who does not yet know what the chapter is about. The classification is useful **after** the claim, not before — which is where several chapters already stated it anyway, making the epigraph a duplicate as well as an interruption.

Checked before deleting: eight of the eleven were already covered in their bodies. [Chapter 05](../05_time_mdbn.md) states the definitional point at line 353, [chapter 08](../08_change_rjf9.md) gives the study-population caveat inside the Lehman section, [chapter 07](../07_scale_637f.md) has an entire *About the numbers* section.

**Three needed relocating first**, and were.

[Chapter 01](../01_the-five-kinds_cjx4.md)'s epigraph carried the only statement that the five-level model is this book's own rather than standard vocabulary — provenance that decision 13 requires be in the prose. It now sits in the claim section, with the addition that the reader should expect nothing when they search for the names, and should instead find the distinctions already familiar and only unnamed.

[Chapter 06](../06_distribution_49yh.md)'s carried the two escapes from a theorem as a bulleted list. Those are load-bearing: the chapter refers back to them, and the boundary section depends on them. Moved into the body before *When any of this applies to you*.

[Chapter 09](../09_what-a-pattern-is-for_3xzc.md)'s carried a substantive argument — a pattern is not one of the five kinds, because the kinds classify claims and a name is not a claim. That is the question a reader arriving from Part II will actually ask, so it became a short named section immediately after the claim rather than a note before it.

**Consequence.**
`CLAUDE.md`'s rubric now says the chapter opens on the claim, with the reason: a reader who does not yet know the subject cannot use a note about the subject's standing.
`LEDGER.md`'s sanctioned-repetition entry is rewritten — the kind is stated where it does work, not as a standing opener.

---

## 41. The rubric headings name the claim

**Date.** 2026-08-14

**Context.**
The author changed three rubric item names in `CLAUDE.md` — *Why it holds* to *Why the claim holds*, and similarly for the other two — and asked whether the change should reach the actual chapter headings, or whether naming the claim three times would make the prose repetitive.

Their reason was a reading experience: the questions read as though they were about a point just made, rather than about the claim at the top of the chapter.

**The measurement, which is stronger than the impression.**
The distance from `## The claim` to `## Why it holds` runs from 125 to 489 lines, median about 224.

More decisive than distance is what immediately precedes the heading, since a pronoun binds to its nearest antecedent. In [chapter 04](../04_structure_agjy.md) the reader has just finished *Hyrum's Law*, so "Why it holds" reads as *why Hyrum's Law holds*. In [chapter 11](../11_patterns-that-survive-translation_us2k.md) they have just finished *Force six*. **That is the default reading rather than a risk**, which makes the author's experience the predictable one.

[Chapter 04](../04_structure_agjy.md) supplies a sharper case: its claim is two claims joined by *and* — the dependency graph must be acyclic, and what a module makes observable is what it has committed to. "Why it holds" has no referent there even in principle.

**Decision.**
Change the headings, not only the rubric. Thirty-two headings across eleven chapters, plus the rubric in `CLAUDE.md` and `README.md`, the mandatory-boundary sentence in both, one `LEDGER.md` reference, and twenty-three boundary labels in `00_toc.md`.

*Cost of the claim* was reverted to **What the claim costs**, since items three and four are clauses and a noun phrase broke the parallel.

**On repetitiveness, which the author asked about directly.**
Not a problem, and for a reason specific to headings. Three `##` headings containing the same phrase are separated by 50 to 200 lines and encountered one at a time; the only place they appear adjacent is a table of contents, and there the repetition carries navigational information — it signals that the three sections interrogate one object, which is the fact the old headings concealed.

**What was deliberately not changed.**
`docs/DECISIONS.md` keeps the old names throughout. Entries are contemporaneous records of what was decided when, and rewriting them to match later terminology would falsify the log the README points at as evidence.

**A gap the sweep exposed.**
[Chapter 01](../01_the-five-kinds_cjx4.md) has no *Why the claim holds* section at all — it has *Why the kinds get confused*, which serves a different purpose. Ten chapters have three rubric sections and 02 has two. Left alone for now, since the instruction was to make the headings uniform rather than to add a missing section, but it is a real omission in the chapter that introduces the model.

**Still open.**
Two `[claude …]` tags remain in `CLAUDE.md`, on the *five levels* heading: what the five are five *of*, and whether the book has drifted from *level* to *kind*. Both are unresolved pending the author's decision, and the tags are left in place rather than removed, because the questions are live.

---

## 42. Four levels, five kinds

**Date.** 2026-08-14

**Context.**
The author queried the `CLAUDE.md` heading *The five levels* on two grounds: five levels **of what**, given that Force is not advice; and whether the book had drifted from *level* to *kind* without the structural labels following.

Both were right, and the first exposed a live contradiction in the book's foundational sentence. [Chapter 01](../01_the-five-kinds_cjx4.md) opened with

> Every piece of software advice is one of five kinds

and said ten lines later

> The fifth, Force, is **not advice at all.**

**The count, measured.**

```text
 "five kinds"    15        "the kinds"    12
 "five levels"    9        "the levels"    0
```

Zero occurrences of *the levels* in prose is decisive: the drift had already happened everywhere except in structural labels — Part I's name, [chapter 01](../01_the-five-kinds_cjx4.md)'s title and one heading, the README's spine heading, `CLAUDE.md`'s heading, and one `LEDGER.md` row.

**Decision.**
**Four levels, five kinds**, and the two words now mean different things rather than being synonyms.

The four levels are rungs on the ladder of authority: Law → Principle → Idiom → Style. Force is the fifth *kind* precisely because it is not on the ladder. So *level* is reserved for position, and *kind* for membership.

That also fixes the contradiction without weakening anything. The five classify **claims** — anything that can be true, false, or conditional — which is the answer [chapter 09](../09_what-a-pattern-is-for_3xzc.md) had already reached independently while arguing that a pattern is not one of the five. [Chapter 01](../01_the-five-kinds_cjx4.md)'s opening becomes *every claim you meet about software is one of five kinds*, which is true of Force as well as of the other four.

**This partly reverses decision 2**, which chose *Levels* over *Altitudes*. That decision's reasoning was plainness and consistency, and both now favour the change: *kind* is what the prose had already settled on, and *level* was being used for two things at once.

**Consequence.**
`01_the-five-levels.md` renamed to `01_the-five-kinds_cjx4.md`, titled *The Five Kinds*, with a paragraph stating the four-and-five distinction where the ladder is introduced.
Part I renamed. The README's spine section renamed, with a sentence on why the counts differ. `CLAUDE.md`'s section renamed, now saying the five classify claims and reserving *level* for the ladder. `LEDGER.md`'s row rewritten. The five-level model becomes the five-kind model in both places `CLAUDE.md` names it.

[Chapter 22](../22_never-written-down_at4r.md)'s title, *Reading advice at the right level*, is deliberately left alone — that chapter is about placing advice on the ladder, which is what *level* now means.

---

## 43. [Chapter 01](../01_the-five-kinds_cjx4.md) states a premise, not a claim

**Date.** 2026-08-14

**Context.**
The author raised three connected points about [chapter 01](../01_the-five-kinds_cjx4.md). The heading *The five kinds* did not say five kinds of what. The rubric headings created a recursion — *where the claim doesn't apply* inside a chapter whose subject is kinds of claim. And a hypothesis: perhaps the chapter's opening is not a claim in this book's sense at all, which would explain the missing *Why the claim holds* section noted in decision 41.

They asked for the hypothesis to be tested rather than accepted: *to rule out that this is not a claim you should try to find satisfactory proofs for this chapter's claim and be unsuccessful.*

**The attempt, and its failure.**

*Derive the five from an exhaustive partition.* Split claims into descriptive and prescriptive; descriptive ones are about your situation (Force) or about computation (Law); prescriptive ones are conditional on situation (Principle), on ecosystem (Idiom), or on nothing (Style). It fails three ways. Evaluative claims — *this design is ugly* — are neither descriptive nor prescriptive, and Style absorbs them by fiat. The branches overlap: *don't write race conditions* is prescriptive in form and a Law in content. And claims about one program, or about the industry, fit nowhere.

*Exhaustive survey.* The chapter classifies twenty claims. That is evidence a taxonomy is useful; it is not proof that it is exhaustive, and the counter-examples above show it is not.

*Prove the second half.* "The kind determines how much authority it has" needs no proof: the kinds are **defined** by their authority. It is analytic, and there is nothing to demonstrate.

So the sentence has two halves and neither can be shown, for opposite reasons — one is true by construction and the other is an exhaustiveness claim that admits counter-examples. The author's hypothesis is correct.

**It also explains the gap.**
Decision 41 noted that [chapter 01](../01_the-five-kinds_cjx4.md) has no *Why the claim holds* section and called it an omission. It is not. There is nothing to hold.

**Decision.**
[Chapter 01](../01_the-five-kinds_cjx4.md)'s rubric headings change: *The claim* becomes **The premise**, *Where the claim doesn't apply* becomes **Where the model breaks down**, *What the claim costs* becomes **What the model costs**. A paragraph after the premise names both reasons it cannot be demonstrated and says why the chapter's headings differ from every other one's, so the deviation reads as deliberate rather than as an oversight.

This makes [chapter 01](../01_the-five-kinds_cjx4.md) a deliberate exception to the uniformity decision 41 established, on the grounds that 02 defines the model while every other chapter applies it.

**Why not "axiom", which the author proposed.**
It is closer than *model* and still over-claims, for two reasons.

An axiom is posited without justification, and this chapter justifies itself — three worked demonstrations and twenty classified claims. Something offering evidence is not an axiom.

More seriously, it borrows mathematical authority the thing has not got. [Chapter 03](../03_grading-a-law_q5c6.md) grades claims as theorem, definition, or empirical law, and warns that folk versions drop quantifiers and conditions. *Axiom* sits adjacent to *theorem*, so using it would claim standing the model cannot support — in the chapter that defines the test for exactly that error. **Premise** keeps the derivation role and drops the over-claim.

It also echoes `README.md`'s own *The premise* section, where the book states the same idea informally; [chapter 01](../01_the-five-kinds_cjx4.md) is that premise made precise, and the TOC entry now says so.

**Title.**
*The Five Kinds of Claim*, from the author, which answers "five kinds of what" permanently.

**Consequence.**
Prose uses of *the model* inside [chapter 01](../01_the-five-kinds_cjx4.md) are left alone — by that point the chapter has defined the referent, and the overloading risk is in a heading a reader arrives at cold.

---

## 44. [Chapter 11](../11_patterns-that-survive-translation_us2k.md) uses [chapter 02](../02_forces_f4m5.md)'s Force names and order, which changed the sort

**Date.** 2026-08-14

**Context.**
The author's second review of [chapter 11](../11_patterns-that-survive-translation_us2k.md) made one point:

> we already named and listed forces on chapter 2 [Forces — now chapter 02]. Follow the exact namings here in the chapter, then you don't have to say "this is … durability of medium" later. Also follow the exact order of forces used on that chapter unless there is a very good reason not to.

The draft had invented six group names — *something must survive*, *two things at once*, and so on — in an order of its own, and then annotated each with which [chapter 02](../02_forces_f4m5.md) Force it corresponded to. That is a fresh vocabulary for concepts the book had already named, which is the drift `LEDGER.md` exists to prevent, and it cost a line per section explaining the mapping.

**Decision.**
Use [chapter 02](../02_forces_f4m5.md)'s seven names, in [chapter 02](../02_forces_f4m5.md)'s order: concurrency, durability of the medium, blast radius, change frequency and its shape, team size and turnover, latency budget, control of the callers. The per-section translation lines are gone, since there is nothing left to translate.

**What that exposed.**
The invented list had six entries against [chapter 02](../02_forces_f4m5.md)'s seven, and the missing one was **team size and turnover**. That was not a considered omission — it was invisible while the labels were the draft's own, and it became obvious the moment the two lists were laid side by side.

Writing the missing section produced a finding worth keeping. This Force does not change *what* a rule is, it changes **where the rule lives** — [chapter 02](../02_forces_f4m5.md)'s migration from comment, to review habit, to type system. So it generates fewer patterns of its own than the others and mostly relocates rules the remaining Forces produced, which is why the section is short and says so.

**The sort changed, and the change is evidence the sort is real.**
Golden tests had been in the *refuses to sort* list, filed under patterns that answer a goal rather than a situation. With team size restored they have an obvious home: a golden test exists so behaviour cannot change silently under people who did not write it.

The chapter now records that, because it demonstrates the method doing work rather than confirming a guess: **a pattern that will not sort is sometimes evidence about the categories rather than about the pattern.**

Counts move from forty-three sorted and seven refusing, to forty-nine sorted and five refusing.

**Consequence.**
`00_toc.md`'s entry for [chapter 11](../11_patterns-that-survive-translation_us2k.md) gives the new counts and says the Forces are [chapter 02](../02_forces_f4m5.md)'s, so the grouping can be checked against the definition rather than against a fresh set of labels.
`LEDGER.md` loses the six-family row and gains two: the sort against [chapter 02](../02_forces_f4m5.md)'s seven, and the observation about team size relocating rules.
[Chapter 11](../11_patterns-that-survive-translation_us2k.md) runs 432 lines, up from 385.

---

## 45. A cross-reference must carry a fact, not a location

**Date.** 2026-08-15

**Context.**
The author's third review of [chapter 11](../11_patterns-that-survive-translation_us2k.md) raised a pattern that had built up unnoticed:

> I started to thing that lines like this after each worked pattern are like the chapter epigraphs we got rid off. Not much value and they create noise. Evaluate if removing these while preserving valuable parts without saying chapter this chapter that is better

Eleven of the fourteen worked patterns ended on a line naming another chapter — *[chapter 03](../03_grading-a-law_q5c6.md)'s definitional claim applies*, *which is [chapter 06](../06_distribution_49yh.md)'s territory*, *[Chapter 05](../05_time_mdbn.md)'s registration example puts the hashing outside the lock for exactly this reason*.

**Options.**
Delete them all, which loses real pointers; keep them, which is the status quo the author objected to; or separate the two things they were doing.

**Decision.**
Separate them. A cross-reference stays when the fact it carries is one the reader needs at that moment, and it is then written as the fact with a compact `(Ch. NN)` pointer. It goes when the sentence exists only to say another chapter owns the idea.

By that test six lines lost their scaffolding and kept their content — *a copy with no invalidation strategy is a copy that is allowed to be wrong ([Ch. 03](../03_grading-a-law_q5c6.md))* says the thing rather than reporting that [chapter 03](../03_grading-a-law_q5c6.md) says it. One sentence was deleted outright: [chapter 05](../05_time_mdbn.md)'s registration example was a pure location, and the claim before it already stood.

**Why.**
The failure is the one the epigraph decision found. A line that names another chapter reads as though it is adding authority, and authority is not what the book runs on — the mechanism is. It also degrades over time: a pointer to *where* a claim lives breaks silently when chapters move, while a pointer that states the claim survives being wrong about the number.

**Consequence.**
The pattern generalizes past [chapter 11](../11_patterns-that-survive-translation_us2k.md) and is worth applying whenever cross-references accumulate: **write what the other chapter established, not that it established it.**
The same review applied the author's other standing note — that showing the failing code before the pattern is worth doing where it does not make the example worse — to the tolerant reader, which now opens with a strict decoder that breaks on the one change [chapter 08](../08_change_rjf9.md) calls always safe.
Both tags were the author's; the test that separates a fact-carrying reference from a locating one is the draft's.

---

## 46. Go has no way to withhold a zero value, and the chapter says so

**Date.** 2026-08-15

**Context.**
The author's fourth review of [chapter 11](../11_patterns-that-survive-translation_us2k.md) asked for caller code under *Make illegal states unrepresentable*:

> just show this with caller's code at the end with a simple comment at the top of the code

Writing that caller and compiling it disproved the sentence the section rested on. The chapter said that outside the package "the only way to obtain a `Delivered` is to call `Deliver` on a `Shipped`." That is false. `delivery.Delivered{}` — the empty composite literal, naming no fields — compiles from any package. Go gives every struct type a zero value and provides no mechanism to withhold it. Only naming an unexported field is rejected: *cannot refer to unexported field at in struct literal of type delivery.Delivered*.

**Options.**
Switch the example to an exported interface with an unexported method, which is airtight in Go; keep the struct and narrow the claim; or move the example to a language with sum types.

**Decision.**
Keep the struct and narrow the claim. What the transition types actually buy is that no *populated* illegal state can be constructed — nobody outside the package can hold a `Delivered` carrying a signature and a delivery time without having held a `Shipped`. The zero value is a hole, and the chapter now names it.

**Why not the interface.**
It works, and it costs an exported interface, an unexported implementation, and a marker method for a section that has two paragraphs to make its point. The machinery would become the thing the reader remembers.

**Why the narrowed version is better than the original anyway.**
It gives the section a second observation it did not have. `Delivery{Delivered: true}` is a lie that reads as data; a zero `Delivered` has no times and no signature and fails at the first field anyone reads. And the gap is the chapter's own subject in miniature — the shape crosses into Go, the guarantee does not, and the difference is invisible to anyone who carried only the name. Rust's `enum` and F#'s discriminated union have no zero value to fall back to; neither could be compiled here, so the chapter states the mechanism and claims no output.

**Consequence.**
This is the rule about running code catching an error that a reading pass would not have. The claim was not careless — it is what the pattern's name asserts, and it is what the pattern does in the languages it came from. The author's request for caller code is what turned a plausible sentence into a compiled one.
`LEDGER.md` gains a row for the zero-value hole, so a later chapter reaching for this example knows the limit is already stated.

---

## 47. Removed the golden-test paragraph: the book's process is not the book's subject

**Date.** 2026-08-15

**Context.**
Decision 44 recorded that golden tests moved out of the *refuses to sort* list once [chapter 02](../02_forces_f4m5.md)'s real Force names were restored, and the chapter carried a paragraph saying so. The author's fourth review cut it:

> above paragraph is a specific situation that happened durung our book writing process, delete the paragraph, not valuable for the audience of the book.

**Decision.**
Deleted. Decision 44's record of the reordering stands; the chapter's account of it does not.

**Why.**
The paragraph's claim — *a pattern that will not sort is sometimes evidence about the categories rather than about the pattern* — is true and is about method rather than about patterns, which is 19's subject. What made it into the chapter was the anecdote, and the anecdote is about drafting this book. A reader deciding whether their aggregate is drawn correctly gains nothing from knowing that an earlier pass used different labels.

**Consequence.**
Decision 44's line "The chapter now records that" is no longer true, and is left as written — the log records what was decided when, and correcting it retroactively would remove the evidence that this entry reverses it.
A general test worth keeping: **the drafting history belongs in the decision log, not in the chapter.** The log exists so the chapter does not have to carry it.

---

## 48. The three-way distinction is made by the section's structure, not by a sentence naming it

**Date.** 2026-08-15

**Context.**
[Chapter 11](../11_patterns-that-survive-translation_us2k.md)'s *five that refuse to sort* ended on a bolded summary: **A Force is a fact about your circumstances. The shape of the problem is a fact about the business. A goal is something you chose and could choose differently.** The author's fifth review cut it, on the grounds that the two paragraphs above already made the distinction, and that *your circumstances* was adding a phrase rather than a fact.

**Decision.**
Removed. The section now has two bolded lead-ins — *Some answer a goal rather than a situation* and *Some answer what the problem is rather than what the situation is* — and the paragraph that follows them names all three in passing: *confusing the Forces, goals, and problem shapes in play.* Nothing states the taxonomy as a taxonomy.

**Why.**
It was a grand summary of the two preceding paragraphs, and a rule of three, which are both on the cadence list. The stronger reason is that it read as though it were introducing a distinction the section had spent two paragraphs making — so a reader who had followed the argument was told it again in the voice of a first telling.

**One change to the author's suggestion.**
The suggestion was to replace the *Some answer a goal* paragraph wholesale with the goal definition written in the fourth review. That paragraph names the three patterns at issue — property-based testing, the test-double taxonomy, functional core / imperative shell — and this is the section that says which five refuse to sort, so the names cannot go. Merged instead: the lead-in keeps the names, the definition and its test follow.

**Consequence.**
`LEDGER.md`'s row for this concept is reworded, since the canonical phrasing it pointed at no longer exists. The concept is still [chapter 11](../11_patterns-that-survive-translation_us2k.md)'s; it is now carried by the section rather than by a quotable line.

---

## 49. Full-word identifiers in code samples, adopted from FlowCore on different grounds

**Date.** 2026-08-15

**Context.**
The author imported FlowCore's decision 18 — full-word identifiers over Go's short-name convention — into this repo verbatim, as an instruction in `CLAUDE.md` and as a decision entry, having noticed the same comprehension problem in this book's samples that prompted it in that codebase.

FlowCore's reasoning is about maintenance.
Its stated cost is a solo maintainer returning to code after a context switch, re-deriving what `def`, `act`, and `mgr` stand for, and the observation that the cost does not amortize away with familiarity.

**The problem with importing the reasoning.**
Neither half of that applies here.
Nobody maintains the book's samples, and the reader's exposure is a single pass, so there is no second reading for familiarity to build across.

The book has a stronger reason FlowCore does not, and `CLAUDE.md` had already committed to it: **write Go for a reader who does not know Go.**
FlowCore's reader is fluent in Go and paying a re-derivation cost.
This book's reader is most likely fluent in Java, C#, or Python, is already spending attention on `:=`, receivers, and the comma-ok idiom, and has an argument to follow underneath the sample.
A truncated domain noun spends attention that is already committed elsewhere.

So the conclusion is over-determined and the imported premise is false in this repo.
That matters beyond tidiness: a rule whose stated grounds do not hold is a rule someone later overturns for the right reason applied to the wrong argument.

**Decision.**
Keep the rule, replace the reasoning, and narrow the exceptions.
The rule applies to every language the book uses, not only Go — the author's call, on the grounds that a Go sample and a C# sample in the same chapter should read the same way.
Go is still the case the instruction argues, because Go style is the only one of the book's languages that pushes the other way.

**What changed from FlowCore's version.**

*The single-dominant-parameter exception is gone.*
FlowCore allows a receiver-style short name for the one value a short function operates on — `fillIDs(d *WorkflowDefinition)`.
A survey of every Go sample in [chapters 01](../01_the-five-kinds_cjx4.md) through 12 found about seventy-five short-name sites, and this exception licensed nearly all the ones that read badly: `FromMinorUnits(a int64, c string)` reduces amount and currency to letters in a chapter arguing about money handling, and `(b *Billing) Charge(m uuid.UUID)` uses a letter that is not the initial of anything on the line, so there is nothing to recover it from.
The exception is written as a structural rule, which is how it stops applying FlowCore's own test.
Receivers keep the convention, because the receiver's type is on the same line and a spelled-out receiver stops looking like Go.

*A fourth exception was added: quoted code is quoted.*
`CLAUDE.md` tells the draft to prefer real lines over invented ones, and a quotation with the names changed is a paraphrase.
Where a real signature carries a name that will not read, the fix is a comment, not an edit.

*The structural-particle exception gained a clause.* It exempts `err`, `ok`, and `ctx` from being renamed, not from being explained — the gloss rule still applies at first appearance.

*The type-shadow exception is unchanged*, and it earns its place: `04_structure_agjy.md` carries a real `q querier` quoted from FlowCore.

**Consequence.**
About thirty-five identifiers across [chapters 01](../01_the-five-kinds_cjx4.md) through 12 do not comply.
Those chapters are at **draft**, so the cleanup is a separate pass on the author's word rather than a silent edit.
`CLAUDE.md`'s pointer now resolves: it named `docs/decisions.md, decision 18`, which in this repo is the entry on theorems and the halting problem, and now cites FlowCore's file by path alongside this entry.
Three copy artifacts from the verbatim import were fixed: an exception list introduced as "two" and containing three, a missing article, and a lost trailing newline.

---

## 50. The identifier sweep across [chapters 01](../01_the-five-kinds_cjx4.md) through 12

**Date.** 2026-08-15

**Context.**
Decision 49 set the naming rule; the eleven drafted chapters predated it.
A survey found about seventy-five short-name sites, of which roughly half were genuine violations.

**Decision.**
Swept all of them in one pass, verifying rather than assuming: every Go sample whose behaviour the chapter claims was recompiled and re-run, and the chapters' quoted output was checked against the new run.

**What was renamed, and the reasoning where it was not obvious.**

*Domain nouns reduced to letters* — the bulk of it.
`FromMinorUnits(a int64, c string)` became `(amount int64, currency string)` in a chapter arguing that money must not be a float.
`(b *Billing) Charge(m uuid.UUID)` became `Charge(merchantID uuid.UUID)`; `m` was the initial of nothing on the line, which is the case the rule exists for.
Also `Receipt(o Order)`, `Register(name string, m Method)`, `chargeBad(l *Ledger, …)`, `PlaceOrder(…, q Queue, o Order)`, `receipt(c StripeCharge)` and its four neighbours, `adapt(r Receipt)`, `signUp(e Email)`, and the sign-up store's `u`, `e`, and `h` in [chapter 05](../05_time_mdbn.md).

*Truncations* — `qty` to `quantity`, `pct` to `percent`, `dec` to `decoder`, `st` to `stat`, `dt` to `deltaTime`, `msgs`/`m` to `messages`/`message`, `Cur` to `Currency`, `src` to `source`, `key` to `idempotencyKey` where the chapter's own pattern name is *Idempotency key*.

*Paired letters standing for two things* — `a`/`b` became `accounts`/`billing` in the cycle example, `first`/`second` in Singleton, `timestampA`/`timestampB` in the clock-resolution measurement, where the prose already spoke of events A and B.

*One rename beyond the letter of the rule*, flagged because the rule names variables, fields, and parameters but not functions: [chapter 05](../05_time_mdbn.md)'s Lamport-clock method `recv` became `receive`.
The defect is the same and the fix was free; it is recorded here so it can be reverted if the author disagrees.

**What was deliberately left, all fourteen sites.**

- **Type shadowing** — `q querier`, `q txQuerier`, `p *parser`. The exception, working as intended.
- **The `http.Handler` signature** — `handleSignup(w http.ResponseWriter, r *http.Request)`. The types are on the line and self-describing, and a spelled-out version stops looking like the Go the reader will meet everywhere else.
- **Complete words and standard terms** — `mux`, `job`, `row`, `sku`, `on`, `id`, `tx`, `db`, `req`, `fd`. None is a project-specific truncation, and each is recoverable from its line.
- **`(c *Conn) Raw(f func(driverConn any) error)`** is labelled in the chapter as a real standard-library method, so the quoted-code exception applies and it keeps `f`. The caller written beneath it is the book's own, and its `dc` and `pg` became `driverConn` and `pgxConn`.

**What the verification caught.**
Nothing behavioural, but two formatting defects the renames introduced: `Currency` lengthened [chapter 10](../10_patterns-that-cross_r8dw.md)'s struct and broke `gofmt`'s field alignment, and [chapter 11](../11_patterns-that-survive-translation_us2k.md)'s identity map needed its call sites updated to match.
[Chapter 03](../03_grading-a-law_q5c6.md)'s retranscribed output, [chapter 05](../05_time_mdbn.md)'s race, [chapter 11](../11_patterns-that-survive-translation_us2k.md)'s identity map, and [chapter 11](../11_patterns-that-survive-translation_us2k.md)'s compiler error were all re-run and match what the chapters print — including the error text quoted in a comment, *cannot refer to unexported field at in struct literal of type delivery.Delivered*.

**Consequence.**
[Chapters 01](../01_the-five-kinds_cjx4.md), 08, and 09 needed no changes.
The eleven drafted chapters now comply, so the rule applies to new drafting rather than accumulating a backlog behind it.

---

## 51. The README gets a "Start here" block, written as back-cover copy

**Date.** 2026-08-15

**Context.**
The author is preparing to promote the book publicly before it is finished — it is free, on GitHub, and functions as a portfolio piece alongside FlowCore, so waiting for twenty-three chapters costs more than launching partial.

The draft's observation was that the highest-leverage change was not another chapter but the README, which had no reading path: a visitor arriving from a link had to read the premise, the five-kind table, and the rubric before reaching a pointer to a twenty-three-chapter table of contents, eight of whose entries do not exist.

**The draft's first attempt failed, and the author said why.**
It described what each chapter covered — *"why acyclic dependency is a Law and layering is one shape among several"* — which is a table of contents in prose.

> I think the book has many surprising claims parts that can condensed in simple terms to attract attention. […] Another way to thinkg about this is like the cover or back-cover of a technical book. No matter how boring and technical the book is, they always try to put simple and attention grabing statements there and I think that's the right move. We believe that the book is good and worth reading but other people don't believe that, and we are trying to convince them in a very short amount of time.

**Decision.**
Four hooks, in the author's chosen order — 06, 07, 10, 03 — each a claim rather than a description, each followed by two lines and a link.
Placed directly under the status callout, so the first thing after a reader learns the book is a draft is a reason to read it anyway.

**Why this does not conflict with the book's register.**
The hooks are the chapters' own claim sentences at full strength, not copy written over them.
*You cannot tell a slow machine from a dead one* is [chapter 06](../06_distribution_49yh.md)'s claim verbatim.
The 95% is [chapter 05](../05_time_mdbn.md)'s measured figure.
So the promotional voice and the book's voice are the same sentences, which is the only version of this the book can defend.

Two hooks were pulled back on a check against the chapters, and the corrections are the substance of this entry.
*"You cannot, and it is a theorem"* was wrong: [chapter 06](../06_distribution_49yh.md) calls the indistinguishability a property of asking questions over a network, and the theorems are its consequences. Now *"most of what is impossible in distributed systems follows from it."*
*"'This should be a Repository' forbids nothing"* asserted something the chapter does not demonstrate — it works the test on Facade and lists Repository as a case for the reader to apply it to. Now phrased as [chapter 09](../09_what-a-pattern-is-for_3xzc.md)'s own question, *what would that rule out?*, which is both accurate and a better invitation.

**Consequence.**
The rule this establishes for any promotional copy: **a hook must be cashable by the chapter it links to.**
A reader who arrives on an overclaim and then meets [chapter 03](../03_grading-a-law_q5c6.md)'s careful separation of theorem, definition, and empirical law will feel the mismatch, and not overclaiming is the book's differentiator.

---

## 52. [Chapter 12](../12_missing-language-features_esqm.md) argues from Java's own history rather than across four languages

**Date.** 2026-08-15

**Context.**
`00_toc.md` planned [chapter 12](../12_missing-language-features_esqm.md) as Norvig's observation "demonstrated in four languages side by side."
The author installed a JDK on request, which made a better argument available and changed the chapter's centrepiece.

**Decision.**
The four-language comparison stays, carrying Strategy.
But the chapter opens on Visitor written twice **in Java** — the 1994 double-dispatch shape, and the same design in Java 26 using `sealed`, `record`, and pattern matching in `switch`.

**Why.**
A cross-language comparison invites the reply *that is just a different language*, and the reader who has to ship Java can dismiss it.
Watching the pattern die inside the language that entrenched it removes that exit.
Visitor did not fail to survive translation somewhere more expressive; it expired in place.

The demonstration also had to be about the guarantee rather than the line count, because line count is the weak version of this argument.
Visitor's actual payment is that adding a node type breaks every un-updated operation at compile time.
Both versions were compiled with a `Neg` case added and the consumer left alone; both refuse, one with *does not override abstract method visitNeg*, one with *the switch expression does not cover all possible input values*.
Same guarantee, 28 lines against 11.

**Reading the source changed the chapter's claim.**
The talk was fetched and its slides extracted rather than paraphrased from memory, and two things in it do not survive into the version people quote.

Norvig's count is "16 of 23 patterns are either **invisible or simpler**", and the preceding slide adds "**for at least some uses of each pattern**".
The folk version — *patterns are just missing language features* — drops both, which is [chapter 03](../03_grading-a-law_q5c6.md)'s dropped-quantifier failure applied to a smaller result.
He also defines three levels, invisible / informal / formal, where the retelling has two.
And he lists five purposes for patterns, of which "to avoid limitations of implementation language" is one; the claim that patterns are *only* workarounds is something readers added.

The chapter therefore states the narrower version, and is better for it: the strong version is easy to disprove and the real one is not.

**The counter-example came out of the source too.**
Norvig's sixteen omit seven — Adapter, Bridge, Composite, Decorator, Memento, Prototype, Singleton — and that omission is the boundary section.
The sharpest form is that **sum types dissolve Visitor and leave Composite standing in the same file**: the dispatch mechanism changes completely and the containment does not, because directories containing files is a fact about filesystems rather than about a compiler.
That is [chapter 11](../11_patterns-that-survive-translation_us2k.md)'s category of patterns answering the shape of the problem, reached from a different direction.

Two further boundaries: Observer dissolves in one process and returns across a machine with all of [chapter 06](../06_distribution_49yh.md)'s failure modes, so the test is scoped and returns a confident wrong answer when run at the wrong scope; and the test names the language you moved *to*, so "Visitor is a workaround" is true and useless if your compiler lacks sum types.

**Consequence.**
Every sample was compiled and run as printed — nine fences across Java, Go, and Python, plus both quoted `javac` errors.
`LEDGER.md` gains nine concept rows and four example rows.
The relationship to [chapter 11](../11_patterns-that-survive-translation_us2k.md) is stated in the second sentence rather than left implicit: 12 asks what a pattern answers, 13 asks what it is made of, and the two are independent.

---

## 53. The Strategy comparison was rigged, and Decorator fails the chapter's own test

**Date.** 2026-08-16

**Context.**
The author's first review of [chapter 12](../12_missing-language-features_esqm.md) objected to the Strategy demonstration:

> most reader will object that two versions don't offer the same guarantee or maintainability. In the first example the shipping formulas are defined in one place, they are named and can be reused easily. […] But if there is a trade-off then does our claim that the pattern became simpler still hold here?

**The objection was correct and the diagnosis is worth stating.**
The draft compared an interface plus two implementing classes against two lambdas written inline at the call site.
That changes two independent things at once — whether the scaffolding exists, and whether the policies keep their names and their home — and only the first is what the chapter claims.

**Decision.**
Keep the names on both sides.
The new version is a class of named static methods, referenced as `ShippingPolicies::flatRate`, which is nine lines of interface and classes reduced to four lines of methods with reuse, discoverability, and a single home all intact.
The chapter now separates the two changes explicitly before showing the second version, because conflating them is how this comparison is usually rigged.

**A second claim was also overstated and is now measured.**
The draft's cost section said a closure has no name in a stack trace.
Throwing from both forms shows the anonymity belongs to inlining, not to function values: a method reference reports `Trace.byWeight(Trace.java:4)` and an inline lambda reports `Trace.lambda$main$0`.
So the cost is real but avoidable, and the honest version is that the feature removed a requirement rather than a capability — which is also the chapter's general shape.

**Decorator moved from the demonstration to the boundary section, because writing it both ways disproved it.**
The author asked to see the pattern first in the form that lacks the feature.
Written as an interface and two wrapper structs, and again as a function type and two closures, the **function version is longer** — thirty-seven non-blank lines against thirty-one.
Go asks nothing for a one-method interface, so a feature that removes ceremony has no ceremony to collect.

That is not a small correction. It means Decorator does not demonstrate the chapter's claim, and it explains an omission the draft had noticed without understanding: **Decorator is not among Norvig's sixteen.**
What function values actually buy is composability at the call site, which is a real gain and a different one.
The section now says so, and carries the second limit as well — a five-method interface costs four forwarding methods that no language feature removes, because they are not simulating anything.

**Two prescriptions were replaced with the author's.**

The draft said a dissolved pattern loses its name and with it the literature on its failure modes.
The author's correction: when the scaffold goes, the scaffold's own problems go with it, and what you inherit is the failure modes of the language feature — *decorator gotchas becomes function composition gotchas*.
That is right, and the chapter now demonstrates the largest of them, composition order, with two orderings that both compile and log differently.

The chapter closed on *whatever survives is the design, whatever vanishes was the cost of expressing it*, which the author flagged as having no real-world move attached.
The move is now stated: **name the language first, then the design.** A document saying "use Strategy" means an interface and three classes in one language and passing a function in another, so omitting the language underspecifies the work — and the same reading applies to advice you receive.

**Also on review.**
The quantifier discussion was rewritten in plain words with [chapter 03](../03_grading-a-law_q5c6.md)'s halting-problem parallel given enough context to work without turning back, per the author's note that nobody re-reads an earlier chapter.
*Sum type* is now defined at first use.
Two cross-references to [chapters 09](../09_what-a-pattern-is-for_3xzc.md) and 11 were cut as detours; the author's standing objection to "abrupt flashbacks" is that they need to earn their place, and these restated a convergence the local argument did not need.

**Consequence.**
Twelve code fences, all compiled and run as printed.
The chapter grew from 379 to about 470 lines, almost entirely in the boundary section, which is the right place for it to grow.

---

## 54. The book has no authorial "we", and [chapter 12](../12_missing-language-features_esqm.md) nearly acquired one

**Date.** 2026-08-16

**Context.**
The author's second review of [chapter 12](../12_missing-language-features_esqm.md) was direct edits only, no tags.
Two of them introduced first-person plural: "Before **we** see the Java 26 version" and "So **we** keep the names."

**The check, and what it found.**
Every occurrence of *we*, *our*, and *us* across the eleven drafted chapters was surveyed outside code fences.
Forty-five hits, and all of them are **quoted speech** — a developer saying "We'll just make it exactly-once", "We can't change that, things depend on it", "We should put an adapter there" — or a claim quoted inside a table.
There is no authorial *we* anywhere in the book.

**Decision.**
Reverted both to the impersonal form the rest of the book uses.
A third instance in a paragraph the author added — "As we have seen with Java and the visitor pattern" — went the same way.

**Why it matters more than a pronoun.**
The book is written to be *received*, and it addresses the reader as *you* while never speaking as a *we* that includes them.
An authorial *we* invites the reader into a collaboration that is not on offer and quietly changes who is responsible for the claim, which is a live question for a book whose README says the sentences are generated and the judgment is the author's.
This is worth recording because the drift is invisible one sentence at a time and only shows up under a survey.

**Also on this review.**

The author deleted the chapter-04 halting-problem parallel, which had been added in response to their own first-review tag asking for it to be explained or cut.
The cut is accepted: the paragraph before it already states the principle concretely — with the five words the claim survives a counter-example, without them a single case knocks it over — so the parallel was restating in the abstract what the local case had just shown.
This makes decision 53's line about that parallel no longer true of the shipped chapter; it is left as written, being the record of what was decided when.

Three edits were corrected rather than kept.
"Norvigs" for the possessive.
"A blog post recommending a pattern **that** was written in some language, and if it does not say which…" — the inserted *that* left the sentence with no main verb.
"There are key distinctions" was a repair for a count made stale by the deletion above, and is now "Three distinctions", since three is what follows and *key* is an evaluative filler the register rules exclude.

One addition was kept and rewritten rather than reverted.
The author's closing point — that *language* need not mean a different language, because two releases of Java were enough — is a good one and ties the ending back to the chapter's centrepiece.
It arrived with "It is worth reiterating that", which is throat-clearing, and "drastically", which asserts rather than shows.
The kept version is: *Visitor changed status between two releases of Java, so the version you compile with is part of the answer.*

---

## 55. [Chapter 13](../13_smuggled-verdicts_8y69.md) grades loaded terms into three tiers rather than condemning them

**Date.** 2026-08-16

**Context.**
The chapter's subject is vocabulary that arrives with its conclusion attached, and the obvious failure mode was writing loaded language about loaded language.

Both sources were read rather than paraphrased, and both turned out to be carefully qualified in ways their reputations are not.
Fowler's *AnemicDomainModel* (2003): *"they incur all of the costs of a domain model, without yielding any of the benefits"*, plus *"Domain Models aren't always the best tool."*
Fowler on *CodeSmell*, crediting Kent Beck with the coinage: *"a surface indication that usually corresponds to a deeper problem"*, and that smells *"don't always indicate a problem."*

**The finding that shaped the chapter: the two terms fail differently.**
*Code smell* can be used with its hedge intact — *"that is a smell and it is fine here"* is a sentence the definition licenses, and the author is on your side when you say it.
*Anemic domain model* cannot — *"this is anemic and that is correct here"* contradicts itself, because *anemic* means sick.

So the chapter grades terms in three tiers rather than treating loadedness as binary: **shape name, hint word, verdict noun**, separated by a one-sentence test — say the term about your own code, then disagree with it, and see whether the result parses.
This grading is the book's own and the chapter says so.

**Why this is not a repeat of [chapters 03](../03_grading-a-law_q5c6.md) and 13.**
Both of those are about a claim losing a qualifier — the halting problem's quantifier, Norvig's *for at least some uses*.
[Chapter 13](../13_smuggled-verdicts_8y69.md)'s mechanism is lexical rather than propositional: a claim can be qualified and a noun cannot, so the condition is not merely dropped but made unsayable while the word is in play.
The chapter states that difference rather than leaving the three to look alike.

**The boundary comes from the book's own spine.**
*Use-after-free*, *SQL injection*, and *data race* carry verdicts and are fine, because there is no configuration of Forces under which they are the right answer.
That gives the rule: **a verdict noun is legitimate when it names a Law violation and dangerous when it names a Principle violation**, since a Law has no condition that can fail and a Principle is conditional by definition.
Two further boundaries: refusing all judgment-laden vocabulary is itself a slogan with its conditions removed, and you need the term anyway because it will be used on you.

**Source material.**
The argument is largely the author's, worked through while building FlowCore and recorded in `~/c/TechIter/01/coding-style-architecture.md` — the *anemic domain model* critique, the vocabulary-versus-prescription distinction, and *placed by scope* with its worked rules.
Per `CLAUDE.md`, that was read rather than re-derived.
[Chapter 18](../18_force-map-method_r37x.md) owns the placement method; [chapter 13](../13_smuggled-verdicts_8y69.md) takes only what the vocabulary argument needs and cites 06 for why the widest scope is not a preference.

**Verification.**
The Go sample compiles and runs as printed.
The sqlite demonstration was run and the chapter quotes the real output — a first draft of that block invented `sqlite>` prompts and trimmed the error text, which is the failure the run-the-code rule exists to prevent, caught on re-reading before commit.

**Open question for the author.**
The chapter is titled *Patterns That Smuggle a Verdict*, matching the TOC, but its subject is vocabulary rather than patterns — *code smell* is not a pattern, and neither is *anti-pattern*.
*Smuggled Verdicts* would be more accurate. The title is the author's call, and the drift check enforces H1 against the TOC either way.

---

## 56. [Chapter 13](../13_smuggled-verdicts_8y69.md): "meaningful" beats "parses", and the title loses "Patterns"

**Date.** 2026-08-16

**The author's correction to the test was substantive, not stylistic.**
The draft's test read *"say the term about your own code, then disagree with it, and see whether the result parses."*
That is wrong. *"This is an anemic domain model, and that is correct here"* parses perfectly — it is grammatical English. What it fails to be is *meaningful*, because the noun contradicts the predicate.
The author's rewrite substituted meaning for grammar, and the chapter is now: **apply the term to your own code, then say the code is fine as it stands, and see whether the result means anything.**
`LEDGER.md`'s row is renamed accordingly.

**The title.**
The author's edit changed the H1 to *Smuggled a Verdict*, which the drift check caught against the TOC, and which is not a title.
The intent is clear and matches decision 55's open question and the filename, so both H1 and the TOC entry are now **Smuggled Verdicts**.

**One direct edit reverted, with a reason.**
The claim was narrowed to *"some pattern vocabulary carries its verdict inside the noun."*
The chapter's own examples defeat that: *code smell*, *anti-pattern*, *clean*, *premature optimization*, and *SQL injection* are none of them patterns.
The edit also runs against the title change made in the same commit, which removed *Patterns* from the chapter's name. Reverted to *some vocabulary*.

**Naming the tiers instead of numbering them.**
The author replaced *"the second tier"* and *"tier three"* with *hint word* and *verdict noun* throughout.
This is the book's own rule about the five kinds — **never number them, the names carry meaning** — applied to a taxonomy the book invented two hours earlier, and it was applied by the author rather than by the draft that wrote the rule down.

**Three tags.**

*The Fowler service-layer paragraph* was cut as a detour. Correct: it defends Fowler against a misreading, which is not this chapter's argument.

*The Law/Principle boundary needed worked examples* — the author reported not following it. It now works two: **SQL injection**, where the condition attached to the verdict is *always*, so compressing it costs nothing; and **premature optimization**, where the judgment sits in the first word and whether it is premature is a latency-budget question that [chapter 02](../02_forces_f4m5.md) measures across four orders of magnitude. *Use-after-free* was dropped rather than explained, since three Law examples were already enough.

*The "you still need the term" section was deleted*, on the author's objection that its tone belonged in a different book. That was right, and the register rules name the failure: atmosphere, the beleaguered engineer. It is replaced by a boundary that does more work — **a term's tier is not fixed**, evidenced by *monolith* moving from shape name to verdict noun and partly back within fifteen years, which means the test measures a term in a community at a time and has to be re-run rather than memorized.

**Also.**
A latency table written for the Principle example was cut before commit: it ran to 75 columns, and it re-presented [chapter 02](../02_forces_f4m5.md)'s own order-matcher example rather than citing it. It is now one sentence with a cross-reference.

---

## 57. Part III is about names, and [chapter 13](../13_smuggled-verdicts_8y69.md) now says so

**Date.** 2026-08-16

**Context.**
The author asked why [chapter 13](../13_smuggled-verdicts_8y69.md) sits in *Part III — Patterns, graded* if its subject is vocabulary rather than patterns, having added *pattern* to the claim sentence for that reason and had it reverted:

> If chapter 14 [now 13] is about vocabulary and not patterns I'm not sure how to justify this placement. […] So I'm still confused how vocabulary, namings and patterns relate and is it still ok for chapter 14 to belong to part III?

**What settled it was [chapter 09](../09_what-a-pattern-is-for_3xzc.md)'s actual scope.**
Its formal claim is about names, not patterns: *"A pattern is a name for a shape, and names are neither"* true nor false.
Both of its tests are run on `Manager`, `Helper`, `Util`, `OrderManager`, `PaymentHelper`, and `DataUtil` — none of which are patterns — alongside Singleton and Transaction Script.

So the part's opening chapter already generalises past the catalogue. **Part III is about names, with the pattern catalogue as the densest supply of them.**
[Chapter 09](../09_what-a-pattern-is-for_3xzc.md) asks what a name buys; 11, 12, and 13 grade the catalogue's names against ownership, Forces, and language; 14 is what a name can do when it stops being neutral.

**Decision.**
[Chapter 13](../13_smuggled-verdicts_8y69.md) stays in Part III, and the claim stays general.
The defect was that the chapter never justified its own placement — it leaned on [chapter 09](../09_what-a-pattern-is-for_3xzc.md) in a single clause and left the relationship implicit.
Two paragraphs now state it, including why the demonstration is pattern vocabulary and the boundary cases are not.

**Why the claim is not narrowed to "pattern vocabulary".**
The chapter's own material defeats it — *code smell*, *anti-pattern*, *premature optimization*, and *SQL injection* are none of them patterns, and the *monolith* boundary is architecture vocabulary.
Narrowing the claim to fit the part title would have made the chapter assert less than it demonstrates, which is the failure the claim-sentence rule exists to prevent, pointed the other way.

**Part III's title is left as "Patterns, graded".**
It names the part's centre of gravity, which is the catalogue, and [chapters 09](../09_what-a-pattern-is-for_3xzc.md) and 14 are the frame around it — what a name is worth going in, and what a name can do coming out.
The alternatives considered were vaguer, and the author's question was about placement rather than about the title.

---

## 58. [Chapter 13](../13_smuggled-verdicts_8y69.md) restructured onto two axes, because a ladder made *Decorator* and *code smell* the same species

**Date.** 2026-08-16

**Context.**
The author, after the first review, kept returning to a discomfort with the chapter's placement in Part III:

> With this chapter organizations and terminology, aren't we implying in the book that "code smell" and "decorator" are of the same species? That feels wrong to me.

They were right, and the fault was structural rather than presentational.

**The diagnosis.**
The chapter graded terms on a single ladder — shape name, hint word, verdict noun — which collapsed two independent questions into one ordering.

- **Does the term pick out something in the code?** *Decorator*: yes. *Anemic domain model*: yes. *Code smell*: no.
- **Does the term carry a verdict?** *Decorator*: no. *Anemic*: yes. *Code smell*: yes.

On those axes *Decorator* and *code smell* are diagonally opposite, and the ladder had put them adjacent with *anemic* in between.

**[Chapter 09](../09_what-a-pattern-is-for_3xzc.md) had already got this right and the draft ignored it.**
It grades names on compression and constraint, has a section headed *The two tests are independent*, and prints a 2×2 with four named outcomes.
[Chapter 13](../13_smuggled-verdicts_8y69.md) took a related question about the same objects and flattened it, which is also why the chapter read as though it did not belong in the part.
Restructuring makes it fit better, not worse: it is [chapter 09](../09_what-a-pattern-is-for_3xzc.md)'s method applied to a different pair of questions.

**The ladder also had the ordering backwards on one axis.**
By *can you dissent*, the shape-plus-verdict cell is worse — *anemic* forbids the sentence that disagrees with it and *smell* does not.
By *is there anything here to check*, the no-shape cell is worse — with *anemic* you can open the file, establish that behaviour is off the entities, and argue about whether that is a defect; with *smell* there is nothing to establish.
Two axes give two orderings, and the chapter had been presenting one of them as the ordering.

**What the author added, and it is the practical core of the new section.**
That a no-shape term is admissible when it is marked as what it is, contrasted in two sentences of theirs:

> "This code has smells, should be rewritten from sctach"

> "This part has code smells, but I can't make up what could go wrong. Can you walk me over why you choose this shape"

The first goes hunch to conclusion with nothing checkable between, so only deference and refusal are available and seniority decides.
The second declares its own status and converts into a request for the reasoning — which is [chapter 02](../02_forces_f4m5.md)'s Forces question.
The rule the chapter now states: **a no-shape term is admissible when it is stated as the speaker's state and turned into a question.**

**Two things the draft added on top.**
That a no-shape term is **a fact about the reader rather than about the code** — Fowler's own *"surface indication"* says exactly this and the word will not carry it.
And that **[chapter 01](../01_the-five-kinds_cjx4.md)'s classification test has nothing to grip** on *this smells*: it is not a Law, Force, Principle, Idiom, or Style, because it is not a claim about software. If the test cannot take it, it was not a design claim.

**Consequences.**
The claim sentence now covers both axes.
*Tier* vocabulary is gone from the chapter entirely.
The *monolith* boundary is sharper against a grid than against a ladder — it crossed the verdict axis and partly back while never leaving the top row, because the shape it named never changed.
The closing questions are now two, one per axis.
`LEDGER.md` loses the three-tier row and gains five.

---

## 59. The fourth cell is occupied, and what fills it is worth one paragraph

**Date.** 2026-08-16

**Context.**
The chapter's grid claimed the bottom-left cell — names no shape, carries no verdict — was empty, and gave a reason: *"a word that neither picks anything out nor asserts anything gives nobody a reason to say it."*

The author's second review disproved it:

> it might surprise you but bottom-left words are very commonly used maybe even more than the others on some orgs. […] You use it when you are forced to say something about a situation you have no control and you don't want involvement. […] Example: "What do you think about this design? It looks exciting, I'm sure lots of effort went into it."
> I'm not sure if this is worth putting in the book tough, you decide.

**The correction was not optional.**
Whether to expand on it was a judgment call; whether to fix it was not.
The draft had asserted a mechanism for a non-fact, which is the failure this book spends chapters diagnosing in other people, sitting inside a grid whose purpose is to sort claims by how checkable they are.

**Decision: include it, in one paragraph, framed by what it tells the reader.**

Against including it: the book's subject is technical advice, and filler is the absence of advice; the register rules exclude office atmosphere; the author had already objected to an earlier section of this chapter for a tone that belonged in a different book.

For including it, which won: the cell is real, and there is a use for knowing it. **A word from it means no design feedback was given.** Rewriting something because a senior reviewer called it *interesting* is acting on a statement that was never about the code — and correctly placing what you have been handed is the book's actual subject, so this is in scope where a complaint about corporate language would not be.

The framing deliberately avoids the author's *office politics* and *non-technical people* wording. Neither is needed to make the point, both invite a reading in which the book is sneering at colleagues, and the useful content survives without them: these words get said when a response is required and a position is not.

**Consequence.**
"Four combinations, and only three of them occur" becomes "all four are occupied".
The grid's bottom-left cell is filled in.
The paragraph closes on the chapter's own test — *if you accept the word, what have you agreed is true?* — where the answer is nothing, which is the finding rather than a gap.

---

## 60. [Chapter 14](../14_principle-loses-scope_b86v.md) gets its mechanism from Pike's own transcript, not from the paraphrase

**Date.** 2026-08-16

**Context.**
`00_toc.md` planned the chapter around "Go proverbs quoted as law, Rob Pike's own complaint about it", and the author's source document states it the same way: *"Rob Pike has publicly complained about Go proverbs being quoted as rules — he wrote them as observations, and watched them become slogans."*

**Reading the source changed what the chapter argues.**
The complaint as described could not be found — no such statement appears on `go-proverbs.github.io`, and searches turned up nothing.
What exists is better: a transcript of the Gopherfest 2015 talk itself, in which Pike says the thing the paraphrase reports him complaining about later.

> they might be contradictory. Proverbs aren't always — real proverbs in the real world you can find lots that are exactly the opposite. And that's okay too, because sometimes one engineering decision is right, sometimes the exact opposite is right.

So the chapter does not need a later complaint. **The disclaimer was in the original talk**, and it did not travel, which is a sharper instance of the chapter's own claim than a subsequent grumble would have been.

**The finding that became the chapter's mechanism.**
Pike also states his selection criteria for a proverb: "really short", "kind of poetic", "memorable", "a little saying".
Those are criteria on *form*, and a condition cannot survive them — it is longer, it does not scan, and it is useless to anyone not in the situation it names.

That converts the chapter from a description of a sequence into an explanation of why the sequence is the normal outcome: **compression is what makes advice transmissible and is the same operation that strips it.** The claim sentence is now that, rather than the four-step narration the TOC planned.

**The demonstration is the proverb and its condition, three lines apart.**
*Don't communicate by sharing memory* is the first item on the list; *Channels orchestrate; mutexes serialize* is the third.
One is quoted in code reviews a decade later and the other is not, and the difference is length and rhythm rather than correctness.
A counter written both ways: 14 lines and 145 ns/op with a mutex, 34 lines and 355 ns/op with a goroutine and three channels — one machine, ratio 2.4–2.5 across repeats, and the chapter says so rather than quoting a single run as if it were a constant.
[Chapter 05](../05_time_mdbn.md) owns why the channel version is a correct way to protect state, so this cites it rather than re-deriving it.

**The AI material owed to this chapter is a section rather than a paragraph.**
`docs/ai-material.md` assigns 15 "a paragraph applying 15's own test", and the finding is that generated design fails it in a way the four steps cannot describe: not that the conditions were forgotten but that none were ever formed.
The chapter also draws the consequence the source material implies — this is a *harder* case than a movement, because a slogan leaves a thread to pull and a taken branch leaves no mark.

**The third boundary is the trap the material warned about.**
`ai-material.md` says the book is most likely to commit its own diagnosed error by closing with a method and a name.
[Chapter 14](../14_principle-loses-scope_b86v.md) is where that has to be answered, since it is the chapter that names the mechanism, so its boundary section states the two non-negotiable conditions: [chapter 01](../01_the-five-kinds_cjx4.md)'s model is a lens that cannot be proved, and the review practice requires the expertise it appears to replace.

**Verification.**
Both Go samples compiled, `gofmt` clean, `go vet` clean. Benchmarks run four times.
One error caught on re-reading before commit: the line counts were quoted inverted — *"the second is fourteen lines against thirty-four"* — which reversed the point the sentence was making.

---

## 61. [Chapter 14](../14_principle-loses-scope_b86v.md) rewritten after the draft fabricated its own centrepiece

**Date.** 2026-08-17

**Context.**
The first draft of [chapter 14](../14_principle-loses-scope_b86v.md) rested on a claim the author disproved by watching the source.
The draft said Pike's *channels orchestrate, mutexes serialize* is the **condition** for *don't communicate by sharing memory* — "the condition was published beside the proverb, by the same person, on the same afternoon."
He never says that. They are two entries on a list, each with its own explanation, and the relationship was the draft's inference presented as his structure.

Every quotation in that draft was genuine. The claim built from them was not, which is why it survived a self-review.

**The failure repeated once more during the review**, which is the part worth recording.
Correcting the first error, the draft then asserted that the folk reading of proverb one is *use channels, not mutexes* — another unevidenced bridge between the same two proverbs, in the message reporting the first one.
Twice, the same span, opposite directions.

The cause was not careless source-reading; the full transcript was in hand for the second attempt.
It was that **the chapter shape required a harm demonstration, no evidence supported one, and the draft supplied the missing piece rather than reporting its absence.**
The `CLAUDE.md` rule added in response covers reading sources; it does not cover this, and the honest record is that the corrective here was the author watching the talk.

**What reading the whole transcript produced instead.**

Pike's own gloss on proverb one is narrow and specific: pass the address of a data structure over a channel, and *"if you don't keep the pointer then you don't have access to it anymore."* Ownership transfer.
He describes the borrowed form as opaque by design — reading two of Segoe's aloud and saying *"don't worry whether you understand that or not."*
He says the proverbs are for people who already know them, to be used *"to explain to somebody."*
And two minutes before the end he predicts the artifact detaching from the speaker: *"maybe this will turn into something that the community maintains on the wiki."*

**The harm the draft kept trying to invent turned out to be documented.**
The Go project's own wiki page opens by quoting the proverb, then says over-using channels is a common newcomer mistake, and supplies a table whose channel column reads *passing ownership of data* — Pike's gloss, reconstructed by his own project.
A forum thread the author saved has a reader stating the over-application in their own words, twice, about code that is race-clean.
The chapter states explicitly that the wiki attributes the over-use to enthusiasm rather than to the proverb, and does not claim causation.

**The claim changed as a result, and narrowed.**
Not *conditions are lost in transmission* but: **a compressed principle does not fix the scope of its own key words, and a reader without the context resolves them outward.**
The underdetermined thing in this case is the phrase *sharing memory* — whether writing to your own index in a shared slice counts. Eleven words do not settle it.

**The strongest evidence arrived last, from the author.**
Supplied with the *Wei Qi Shi Jue*, the draft noticed that most of its ten four-character rules spend part of that budget on their trigger — *when in danger, sacrifice*; *against strong positions, play safely*.
Which generalises: **scope lives inside the sentence or in machinery around the collection, and where it is in neither the reader supplies it.**

And that exposed a control inside Pike's own list. Four of his nineteen take a named package as their grammatical subject — syscall, cgo, unsafe, reflect — and **have nowhere to drift to**, because the word fixes the domain. The rest take a way of working as their subject. Same author, same talk, same form, one variable.
The chapter's test is now checkable rather than hopeful: look at the grammatical subject.

**Title.**
*How a Principle Becomes a Movement* asserted something the chapter never showed — no movement was named, dated, or traced.
The author proposed *How a Principle Becomes a Folk Remedy*.
The draft argued against it and the author accepted: the chapter's evidence ends in **repair** rather than entrenchment, so a title naming a bad endpoint overshoots what is demonstrated.
*How a Principle Loses Its Scope* claims exactly what is shown.
*Folk remedy* is a good term for the case where repair never arrives, and moves to [chapter 22](../22_never-written-down_at4r.md), recorded in its TOC entry so it is not lost.

**Consequence.**
`LEDGER.md`'s eleven rows for [chapter 14](../14_principle-loses-scope_b86v.md) are replaced; the old ones describe a chapter that no longer exists.
Sensei's Library material is used under short quotation for commentary — its content is under the OpenContent License, whose share-alike clause defers to fair use, so the chapter states facts about the page and quotes two sentences rather than reproducing lists.
The author's review file keeps its words; only trailing whitespace was normalised so the drift check stops failing on it.

---

## 62. [Chapter 14](../14_principle-loses-scope_b86v.md), second review: Pike glosses the proverb rather than coining it

**Date.** 2026-08-17

**The author's warning was correct and changed three headings.**
The draft called Pike the proverb's author. The transcript has him introducing it as *"there is already one proverb you all know"* — he is glossing something in circulation, not coining it.
The chapter now says so, and the point survives: he is the language's designer saying what the sentence is taken to mean, which makes the gloss more authoritative rather than less.

**The claim contradicted the chapter's own later finding.**
It said a compressed principle *does not contain* the scope of its key words, while the chapter goes on to show scope living inside the sentence in the *Wei Qi Shi Jue* and in four of Pike's own nineteen.
Now conditional: **it carries the scope only where the sentence names it**, and where it does not, the reader supplies it.

**Two sections cut on the author's judgement.**

*This book is doing it too* — their objection was that it read as "part splitting hairs, part self-flattery, and part trying to counter every possible argument against the book pre-emptively like a paranoid."
That is right about its placement. The material came from `docs/ai-material.md`'s warning that the book is most likely to commit its own diagnosed error, but answering the charge in the chapter that names the mechanism is pre-emption. The two non-negotiable conditions move to [chapter 22](../22_never-written-down_at4r.md)'s TOC entry, where the method is actually delivered.

The opening paragraph listing [chapters 03](../03_grading-a-law_q5c6.md), 13, and 14 as prior instances also went. It was orientation rather than argument.

**One recognition bullet was wrong about its own evidence.**
The draft described the Reddit thread as an argument about what a word covers. The author quoted the post to show it is not: the poster found working code, could not fault it, still suspected it violated the proverb, and asked.
That is a better tell than a dispute, and quieter — **a competent reader who cannot reconcile a rule with code they have no complaint about is missing the rule's extent, not their own judgement.** The bullet now says that.

**Consequence.**
[Chapter 14](../14_principle-loses-scope_b86v.md)'s TOC entry is rewritten; the old one described the movement chapter that no longer exists.
`LEDGER.md` loses the row for the deleted section and has two rows corrected — the claim's wording, and the note that Pike glosses rather than coins.
The chapter runs 193 lines.

---

## 63. How [chapter 14](../14_principle-loses-scope_b86v.md)'s claim sentence was arrived at

**Date.** 2026-08-17

Recorded at the author's request, because the claim took six exchanges and each one removed a specific defect. The final sentence is unremarkable to read, which is the point — the record is of what it had to survive.

**Where it started.**
The first draft claimed the mechanism was conditions being lost to compression: *"what travels is selected for being short, and a condition makes a saying longer."*
That died with the draft it belonged to (decision 61).

**Version two, after the rewrite.**
*"A compressed principle does not fix the scope of its own key words. A reader without the author's context has to supply that scope, and the widest reading is the only one available without it."*

**The author's first correction: it contradicted the chapter.**
They tagged it against a line two sections later — *scope lives either inside the sentence or in machinery around the collection*.
A claim asserting a principle **does not** contain its scope cannot stand in a chapter demonstrating that four-character rules do, and that four of Pike's nineteen do.
The fix had to be conditional rather than absolute.

**The author's second proposal, and the one thing in it the draft argued against.**
They offered a three-sentence version turning on *"if the compression didn't wipe it"*, with *reconstruct* in place of *supply*.

Two of those three moves were improvements and were kept: three short sentences read better than two packed clauses, and **reconstruct** is the right verb because it names the task the reader is handed and connects the claim to the chapter's third act, where the Go wiki and two commenters do exactly that.

The draft argued against the third, and the author accepted: *the compression wiped it* makes compression the agent, which the chapter disproves twice. The *Wei Qi Shi Jue* rules are four Chinese characters — compression at maximum — and most carry their trigger. *Syscall must always be guarded with build tags* is short and cannot drift, because its subject fixes the domain. Compression is orthogonal; what decides it is whether the principle names its own situation.

**The author's third correction: the word *sentence* had no referent.**
This is the one the draft kept missing. Their objection, verbatim: *"We have principle, slogan claim and then 'sentence'. What sentence, which sentence?"* — plus the substantive point that a compressed principle need not be one sentence. *Design the architecture, name the components, document the details* is three imperatives.

The draft had twice patched around this rather than fixing it, keeping *sentence* while adjusting everything else. Correcting it exposed **nine more places in the body** where *sentence* was standing in as general vocabulary for the chapter's subject, including its second-strongest line and its actionable test. In a chapter about imprecise vocabulary, that was a poor thing to have shipped.

**The author's fourth correction: *what it applies to* invites a useless answer.**
*"It obviously applies to Go or it obviously applies to software, what does it have to name?"*
Correct — a domain is not a narrowing.

**What resolved it was already in the book.**
The thing the good ones name is a **situation**. Go is not a situation; software is not a situation. And *situation* is [chapter 02](../02_forces_f4m5.md)'s word for what a Force is a property of, and [chapter 01](../01_the-five-kinds_cjx4.md)'s first classification question asks whether a claim is a statement about your situation.
So the claim borrows vocabulary the reader has had since Part I rather than introducing a third term — which was the author's original objection to *sentence*, satisfied rather than worked around.

**The result.**

> **A compressed principle carries its scope only when it names the situation it applies to. Where it doesn't, the reader has to reconstruct that scope from the surrounding context. Without that context, only the widest reading is available.**

Sentence one covers scope living inside the principle. *Surrounding context* in sentence two covers scope living in apparatus around the collection — Segoe's diagrams, the wiki's categories. Sentence three is the failure case, and the chapter's Reddit reader is an instance of it.

**Attribution.**
The three-sentence shape, *reconstruct*, the removal of *sentence*, and the objection to *applies to* are the author's.
The argument against compression-as-agent, the conditional form, and the identification of *situation* as vocabulary the book already owns are the draft's.
That the claim contradicted its own chapter was caught by the author reading the two against each other, which is the check no single pass performs.

---

## 64. The chapter stops confessing its own first draft

**Date.** 2026-08-17

**Context.**
The author's third review deleted a clause from [chapter 14](../14_principle-loses-scope_b86v.md)'s cost section. It had read that reconstructing rather than reading is how a plausible mechanism gets attached to somebody else's words — *"this chapter's first draft did exactly that, asserting a relationship between two of Pike's proverbs that he never claimed."*

**Decision.**
Accepted. The clause is gone.

**Why it is the right cut, and why it took a second pass to see.**
The reader has no first draft to compare against, so the confession is unverifiable from inside the chapter and reads as a credibility move rather than as evidence.
The failure is already recorded where the authorship record belongs — decisions 61, 62, and 63 — and the README points there rather than at the prose.

It is also the second time the author has cut the book talking about itself in this chapter. The first was *This book is doing it too*, removed in the second review as pre-emptive. **The pattern is worth naming: a chapter about how advice goes wrong is unusually tempting to decorate with the book's own fallibility, and every such passage costs the reader something and buys the book nothing.**

**Consequence.**
Decision 61's line saying the chapter names its own first draft in the costs section is no longer true of the shipped chapter, and is left as written — the log records what was decided when.

**One correction to the review, in the other direction.**
The third review changed the description of Segoe's book to *published fifty years earlier*. Pike's words are that it *"was translated about 50 years ago from Japanese into English"*, and the Japanese original is older than that. Restored to *translated into English about fifty years earlier*, which keeps the author's disambiguation — that this is go the board game rather than the language — and their split of an overstuffed sentence.

The rest of both reviews stands: *scope* for *content* where the chapter's own key term applies; *proverb* for *sentence* in a place the vocabulary sweep missed; *the Reddit thread* for *the forum thread*; and *shows the book's cover* for the ambiguous *shows it*.

---

## 65. Bridging [chapter 14](../14_principle-loses-scope_b86v.md) from proverbs to principles, and making 16–18 read as instances

**Date.** 2026-08-17

**Context.**
The author raised a structural worry before drafting 16:

> I'm slightly worried that we need to find a way to generalize Pike's "go proverbs losing the scope" to "principles losing the scope." That looks very plausible but do we have a plan for it.

Stated sharply: **[chapter 14](../14_principle-loses-scope_b86v.md)'s title and claim say *principle*, and every piece of its evidence is a *proverb*** — a genre built on purpose to be short and memorable, which a reader can fairly call a special case.

Checking turned up a second gap the author had not asked about. [Chapters 15](../15_behaviour-placement_z47a.md), 17, and 18 *are* the generalization, but nothing in their TOC entries said so; read cold they were three independent critiques. So [chapter 14](../14_principle-loses-scope_b86v.md)'s opening line — *this chapter is the mechanism they share* — was a promise the rest of Part IV did not keep.

**Decision, gap one.**
A short section in 15 runs the chapter's structural test on advice nobody wrote to be memorable.

This is safe where a harm example would not have been, and the distinction is the one the last three reviews were about. Asking whether a principle names the situation it applies to is a question about **wording**. It needs no history, no author to interview, and no claim about what anyone did with it — the same kind of claim as the `syscall` versus *clear is better than clever* split already in the chapter.

*A class should have one reason to change* and *don't repeat yourself* were not compressed for memorability and fail the test anyway, because *responsibility* and *repeat* have no fixed extent. *Don't store money in a float* and *guard cgo with build tags* pass, because *money* and *cgo* name situations.

So **the property belongs to the wording rather than to the genre.** Being built for memorability makes omission more likely, since the situation is the longest part and the first to go. It is not what causes it.

**Decision, gap two.**
Each of 16, 17, and 18 gains a block naming the principle, the term with no fixed extent, and the wide reading:

- **16** — *behaviour belongs with the data it operates on*; **belongs with**; every entity gets methods reaching other entities, producing object webs and cycles. The narrow reading is [chapter 13](../13_smuggled-verdicts_8y69.md)'s *placed by scope*.
- **17** — *write the test first* and *mock your dependencies*; what **first** buys, and what counts as a **dependency**; the ordering ritual causes good design, and anything you did not write gets mocked.
- **18** — *depend on abstractions* and *the database is a detail*; **abstraction** and **detail**; an interface at every boundary and a directory per layer. The narrow reading is [chapter 04](../04_structure_agjy.md)'s, and `docs/speculative-abstraction.md` holds the argument.

**Why this was worth doing before drafting 16 rather than after.**
Without it, 16 gets written as a standalone critique of object orientation and has to be retrofitted into Part IV's structure later. With it, each drafting session starts with a spine rather than a topic — and the three chapters stop being three complaints.

**Consequence.**
`LEDGER.md` gains a row for the wording-not-genre finding.
[Chapter 14](../14_principle-loses-scope_b86v.md) runs 214 lines.

---

## 66. "Scope" gets one meaning; [chapter 13](../13_smuggled-verdicts_8y69.md)'s is renamed and [chapter 14](../14_principle-loses-scope_b86v.md) drops its synonym

**Date.** 2026-08-18

**Context.**
The author noticed [chapter 14](../14_principle-loses-scope_b86v.md) had started saying *scope* where earlier chapters say *conditions*, and asked whether the book should sweep one word for the other.

The survey said no to the sweep and found a different problem. Of 92 uses of *condition*, only about a third are [chapter 14](../14_principle-loses-scope_b86v.md)'s sense; the rest are logical antecedents, code branches, and ordinary English including the README's licence terms. And *conditions* already carries one clean meaning across seven chapters, tied to Forces by `CLAUDE.md`'s own definition of a Principle as *good advice given certain Forces — conditional*. Replacing it would cut the word loose from the thing it names.

**The real defect was that *scope* meant three things.**

- [Chapter 12](../12_missing-language-features_esqm.md), casually: whether a test runs in one process or across machines.
- [Chapter 13](../13_smuggled-verdicts_8y69.md), defined in bold: how much data you must see before you can tell whether a rule holds.
- [Chapter 14](../14_principle-loses-scope_b86v.md), defined and in the title: how far a piece of advice reaches.

[Chapters 13](../13_smuggled-verdicts_8y69.md) and 15 are adjacent, and each defines the word.

**Decisions, all the author's.**
[Chapter 14](../14_principle-loses-scope_b86v.md) keeps *scope*. [Chapter 12](../12_missing-language-features_esqm.md) stays as it is, its single use being casual rather than definitional. [Chapter 13](../13_smuggled-verdicts_8y69.md)'s term is renamed.

**Why not *data access*, which the author proposed.**
It collides with *data access layer*, a term of art in exactly the architecture space this book argues about, and *access* names permission rather than quantity, which is the wrong axis.

**Why no replacement noun at all.**
The chapter already had the plain version one line below the bold term: its table is headed *how much you must see*. The noun was carrying nothing the table did not. So the term becomes the phrase — **what the rule must see** — which is self-defining and has nothing to look up. `CLAUDE.md`'s rule points the same way: a figure of speech promoted to vocabulary needs defining, and if it needs defining it is not worth the definition.

**[Chapter 14](../14_principle-loses-scope_b86v.md)'s private synonym also went.**
It used *extent* ten times for exactly what it called *scope* — two words, one meaning, inside one chapter. All ten are now *scope*.

**Consequence.**
`CLAUDE.md`'s Sources line still says the author's FlowCore document feeds *placement-by-scope*, and is left alone: it describes what is in that file, and that file says *scope*. [Chapter 18](../18_force-map-method_r37x.md) should note the book renamed it, or a later session will search the source for a phrase that is not there.
Two `DECISIONS.md` entries mention *placed by scope* and stay as written.
[Chapter 13](../13_smuggled-verdicts_8y69.md)'s *value-scoped rules* also went, being the retired sense leaking into a passage.
The sweep turned up that [chapter 14](../14_principle-loses-scope_b86v.md)'s TOC entry still carried the pre-review claim, including the word *sentence* that three reviews removed from the chapter; it now matches.

---

## 67. [Chapter 14](../14_principle-loses-scope_b86v.md) defines *scope* against *conditions* at first use

**Date.** 2026-08-18

**Context.**
Decision 66 settled that the book keeps both words — *conditions* in the earlier chapters, *scope* in [chapter 14](../14_principle-loses-scope_b86v.md) — on the grounds that they are not synonyms. The author then made the obvious follow-on point:

> This confusion between principle's conditions, and principle's scope is a real risk for the reader and we are not stating the exact meaning of scope in chapter 15 [now 14] as it is introduced.

Correct, and the risk was created by the previous decision. Keeping two words for one boundary is only defensible if the chapter says which is which.

**Decision.**
Two short paragraphs after the claim, before anything else.

**Conditions** are what must be true for a Principle to hold, which is always some fact about your Forces — [chapter 04](../04_structure_agjy.md)'s information-hiding Principle has a sharp one, *you do not control your callers*.
**Scope is the same boundary seen from the other side: the situations the advice reaches.**

**Why the book needs both, stated in the chapter rather than left implicit.**
Stating the conditions gives you the scope, and naming the situation gives you the scope too — they are two routes to one boundary.
[Chapter 14](../14_principle-loses-scope_b86v.md) says *scope* because it tracks **what the wording carries** rather than what the advice requires, and a principle can carry that boundary either way. *Don't store money in a float* names a situation and states no condition, and passes the chapter's test regardless. A chapter using *conditions* would have to call that a principle whose conditions are absent, which is false.

**Consequence.**
`LEDGER.md` gains a row for the relationship, so a later chapter reaching for either word knows it is picking a view rather than a synonym.
This closes the terminology work opened by decision 66.

---

## 68. A named situation is a proxy, and [chapter 14](../14_principle-loses-scope_b86v.md)'s test is weaker than it read

**Date.** 2026-08-18

**Context.**
After the *scope* versus *conditions* definition landed, the author pushed on it:

> What if the wording names a situation but that doesn't imply the conditions the advice requires. Is that possible, basically a scope without a condition. Or is it a scope with the wrong conditions.

It is possible, and the chapter's own evidence proves it — which the draft had not noticed while building the test on that evidence.

**The finding, from Pike's list.**
Two of the nineteen are the same instruction with a different noun: *syscall must always be guarded with build tags*, and *cgo must always be guarded with build tags*. Introducing the second he says it is for exactly the same reason as the first.

One condition — the code is platform-specific — and **two proverbs, because he was naming situations and the condition covered more than one of them.**

So a named situation is a **proxy** for the conditions, chosen for cheapness and recognizability rather than for fit, and it can miss in either direction. Narrower than the conditions, and the advice under-applies: a third platform-specific thing that is neither syscall nor cgo has no proverb, and somebody following both faithfully ships it unguarded having misread nothing. Wider, and it over-applies mildly: *don't store money in a float* covers a dashboard total that is never summed or reconciled, where the condition does not hold.

**What this does to the claim, which is less than it first appears.**
The claim says a principle carries its scope when it names a situation. That survives — it carries **a** scope. What it never guaranteed, and what the draft had let readers assume, is that the scope matches where the advice is true.

So the test measures **checkability, not correctness**. With *guard cgo with build tags* you can ask what your case has in common with cgo and get an answer. With *clear is better than clever* there is nothing to compare against, because no situation was named. That difference is real and is what the chapter is about; the chapter now says so instead of implying more.

**Why it belongs in the boundary section rather than being fixed.**
This is a limit on the chapter's sharpest tool, discovered from the same source that produced the tool. Stating it is the book's own rule — no chapter ships without a real counter-example — applied to a test rather than to a claim.

**Consequence.**
`LEDGER.md` gains two rows, one for the proxy and one for what the test actually measures.
[Chapter 14](../14_principle-loses-scope_b86v.md)'s TOC boundary line now leads with the proxy limit.
The chapter runs 240 lines.

---

## 69. [Chapter 13](../13_smuggled-verdicts_8y69.md)'s Fowler section was [chapter 14](../14_principle-loses-scope_b86v.md)'s mechanism, and the overlap was a ledger defect

**Date.** 2026-08-18

**Context.**
The author, rereading [chapter 13](../13_smuggled-verdicts_8y69.md) after 15 was finished:

> This section of chapter 14 [now 13] has many parallels with chapter 15 [now 14], it reads like a mini chapter 15 to me now. I'm not saying that is bad, that's interesting and I'm wondering if we should do anything about it, like at least acknowledging that and trying to find some insight from it

They were right, and `CLAUDE.md` names the diagnosis: **a repetition found in review is a ledger defect, not a local wording problem.** Two rows were wrong.

Row: *Compression is what strips the condition* was assigned to **14**. That is [chapter 14](../14_principle-loses-scope_b86v.md)'s mechanism, and 15 was rewritten after 14 shipped, so nothing caught it. It is now split — 14 keeps *compressing well is why a verdict noun spreads*, 15 keeps why the qualifier is the part that goes.

Row: *Scope is carried only where named* still carried [chapter 14](../14_principle-loses-scope_b86v.md)'s pre-review wording, including *extent* and *sentence*, both retired from the chapter by later reviews.

**Two other things the reread surfaced.**
[Chapter 13](../13_smuggled-verdicts_8y69.md)'s closing line still described the [chapter 14](../14_principle-loses-scope_b86v.md) that no longer exists — *a true observation acquires a name, the name acquires a community.* That is the movement chapter, deleted in decision 61.
And [chapter 13](../13_smuggled-verdicts_8y69.md)'s Fowler section had generalised past its own subject: *that is not a fact about Fowler; it is a fact about the shape of the term… the one word that survives being repeated.* That sentence states 15's mechanism. It is trimmed to hand the transmission question to 15 and keep 14's own narrower point — the word that survived **convicts**, so a reply must reject the vocabulary before it can reach the design.

**The insight the author asked for, now in [chapter 14](../14_principle-loses-scope_b86v.md).**

The two cases are different kinds of vocabulary losing different kinds of qualifier. *Anemic domain model* is a verdict noun and lost an **antecedent**. *Don't communicate by sharing memory* is an imperative proverb and lost a **situation**.

Same selection, though: **what survives is the part that tells you what to do, and what goes is the part that tells you whether to do it.**

That earns its place because it explains something neither chapter had accounted for — why the error only ever runs one way. Nobody under-applies a principle received without its scope, because the fragment that would have narrowed them is exactly the fragment that was dropped.

**Consequence.**
`LEDGER.md` gains a row for the actionable-half finding, so a later chapter meeting the same shape has somewhere to point.
The overlap is now a relationship the book states rather than a duplication a reader notices.

---

## 70. The bridge table was mixing two levels, and one column was incoherent

**Date.** 2026-08-18

**Context.**
The author could not follow [chapter 14](../14_principle-loses-scope_b86v.md)'s table generalising the test past proverbs, and gave two reasons.

The first was a plain error. Column one read *one reason to change* and column three read *responsibility* — a word not present in the row it was labelling. The statement of the principle was in one cell and the name of the principle was being drawn on for the other.

The second was the real problem:

> your "term with no fixed scope" column doesn't make sense to me. A principle has a scope or not, any term in it having a scope is meaningless here.

**Correct, and the confusion was the draft's throughout.**
There are two levels — a principle's scope, meaning which situations it applies to, and a term's extent, meaning which things a word covers. The chapter's claim is about the first. The table's third column was about the second, and the prose slid between them without noticing.

**Decision.**
The author's replacement shape, which fixes it by changing what the column is for: **principle / situation named / what you must ask.** The third column is now a question about the principle rather than a property of a word inside it, which keeps everything at one level and is actionable — *one responsibility of what, a method, a class, a service?*

The paragraph after the table was rewritten to match: the top four fail not because a word inside them is fuzzy but because none of them says which situation it is about, so applying one means answering a question it never asked. Two engineers who both accept the single responsibility principle can disagree about every class in the codebase, having answered *of what?* differently.

**Two more instances of the same slip, found by sweeping for it.**
*The phrase sharing memory has no fixed scope in the proverb containing it* is now *the proverb never says what counts as sharing memory* — same fact, stated about the principle.
*Compression fixes words. It does not fix their scope* is now *compression fixes the wording. It does not fix the scope.*

**Consequence.**
`LEDGER.md`'s row for the bridge section is reworded, since it described the finding in the term-level vocabulary that has now been retired from the chapter.

---

## 71. `CLAUDE.md` is canonical and does not know about other agents

**Date.** 2026-08-18

**Context.**
The author experimented with a second coding agent on this repository, which added `AGENTS.md` — an adapter that defers to `CLAUDE.md` as the project guide rather than restating it.

The draft suggested listing `AGENTS.md` in `CLAUDE.md`'s Files section, on the grounds that a rules file nobody mentions is the stale-pointer problem this repo has already hit twice.

**Decision.**
No. The author's ruling:

> Think claude is primary and doesn't care and shouldn't know about codex, codex is secondary and is responsible for it's setup when/if it's needed.

`CLAUDE.md` is canonical and stays unaware of any other agent. An adapter file is responsible for its own adaptation. A third agent writes its own adapter and does not edit the canonical file either.

**Why, in the book's own terms.**
The dependency runs adapter → canonical, and it has to stay one-way. `AGENTS.md` names `CLAUDE.md` in its second line. If `CLAUDE.md` named `AGENTS.md` back, the two would each require the other as context, which is [chapter 04](../04_structure_agjy.md)'s cycle — and the cost is the one that chapter states: neither file can then be read or changed without the other, for as long as both exist.

Keeping the arrow single means `CLAUDE.md` can be edited without checking anything else, which is the property that matters for the file every session loads.

**Also worth recording, because it is the more embarrassing half.**
`AGENTS.md` already contains a line instructing agents not to add it to `CLAUDE.md` unless the author explicitly asks to invert the relationship. The draft had read that file and proposed the thing it forbids.

**Consequence.**
`CLAUDE.md` is unchanged and lists no adapter files.
The stale-pointer concern that motivated the suggestion is real but lands on the adapter rather than on the canonical file: if `CLAUDE.md` moves or is renamed, fixing `AGENTS.md` is the adapter's problem.

---

## 72. Pike's 2023 retrospective gives [chapter 14](../14_principle-loses-scope_b86v.md) the harm it had conceded it lacked

**Date.** 2026-08-18

**Context.**
The author supplied Pike's closing talk from GopherConAU 2023, *What We Got Right, What We Got Wrong*, published on his own site. Two passages in it are [chapter 14](../14_principle-loses-scope_b86v.md)'s mechanism with Pike naming it.

**What it supplies.**

*An instance in someone else's advice.* Google banned threads around 2002, engineers citing John Ousterhout's position that threads were bad. Pike's diagnosis is that Ousterhout was **generalizing beyond the domain he was interested in**, and was complaining about low-level packages like pthreads rather than about the idea. The situation was pthreads in a particular kind of program; what arrived was *threads are bad*, applied organisation-wide, for years, with a name attached.

*An admission about his own project.* On concurrency, the team's use cases were server software and he says they should have explained that up front, that programmers who tried it elsewhere struggled to see how it helped, and that the lack of guidance was theirs. On concurrency versus parallelism, that the team did a terrible job explaining it and it probably drove some programmers away.

**Why this changes the chapter rather than decorating it.**
[Chapter 14](../14_principle-loses-scope_b86v.md) had conceded it has **no documented harm**, and that concession shaped its boundary section — the chain ends in repair, harm deferred to 16 through 18. That is now only half true. This is the source of a piece of advice stating that the situation was never named and what it cost, which is stronger than a reader's complaint or an inference from a codebase.

It also supplies a third repair. Pike gave a whole talk in 2012 to restore the concurrency/parallelism distinction, and says it should have happened earlier.

**What the chapter is careful not to claim.**
*Don't communicate by sharing memory* and *concurrency support in the language* are different artifacts. Nothing here says the proverb caused what Pike describes, and the chapter says so in as many words. It is the same mechanism twice from the same person, not more evidence for one artifact.

This distinction is the one the whole chapter-15 review was about, and it is stated rather than left for a reader to notice.

**Process note.**
When the author first offered this source, the draft was asked for a one-word answer and gave one — without having read the file. The answer happened to be right. It should have been *let me read it first*, and the entry records that because the same shortcut is how the chapter's original fabricated centrepiece got written.

**Consequence.**
`LEDGER.md` gains two concept rows and one example row.
The TOC entry for 15 carries both instances.
The boundary line saying the scope was rebuilt twice now says three times, the third being the source himself.
The chapter runs 282 lines.

---

## 73. The damage follows from the reading, not from the advice

**Date.** 2026-08-18

**Context.**
The author rewrote the closing paragraph of [chapter 14](../14_principle-loses-scope_b86v.md)'s retrospective section to end on the mechanism — *the underlying mechanism is the same: a principle loses its scope and causes long-term harm.*

The draft replaced it with a version that restated the two preceding subsections and added dates. The author's verdict was that this "runs around the crucial matter and produces word salad", being a summary of what the reader had just read, and that the crucial information was to pinpoint the mechanism.

**Correct on both counts, and the draft was wrong for a specific reason worth recording.**
It had blocked *causes harm* as an unsupported causal claim. But the caution it was applying had been earned in a different section — the one where the Go project's wiki attributes channel over-use to enthusiasm rather than to the proverb. In *this* section Pike asserts the link himself: the engineers doing the banning cited Ousterhout, and the concurrency confusion probably drove some programmers away. The causation is in the source, and the draft was guarding against a problem that is not there.

**Decision.**
The author's sentence, with the step it skipped restored, and one addition.

> But the mechanism is the same, and that is the whole of it: a principle arrives without its scope, the reader takes the widest reading available, and the damage follows from the reading rather than from the advice.

The middle clause is the chapter's actual claim and connects this section back to the reader in the forum thread.

The final clause is the one that earns the word *harm*. **If the damage follows from the reading rather than from the advice, the chapter can say harm without asserting the advice caused it** — which is the distinction the rest of the chapter is careful about, and which the evidence supports directly: Pike says Ousterhout's complaint about pthreads was legitimate and the error was generalizing, and that the concurrency feature was right and the explanation wrong.

**A register check that produced a smaller change.**
The author proposed opening the turn with *However*. The turn is needed — after two sentences of *this is not evidence of*, a reader can begin parsing the next one as a third limitation. But a survey found **zero** uses of *However* as a sentence opener across fourteen drafted chapters, against nine of *But*. The connector is now *But*, which does the same work in the register the book already keeps.

*Long-term* was dropped. The years are already in the section above, and an adjective is weaker than dates the reader has.

**Consequence.**
`LEDGER.md` gains a row for the reading-versus-advice distinction, since it is what licenses the word *harm* anywhere in Part IV.

---

## 74. Pike's retrospective gets a source document, and drafted chapters wait

**Date.** 2026-08-18

**Context.**
[Chapter 14](../14_principle-loses-scope_b86v.md) took two passages from Pike's 2023 GopherConAU talk. Reading it turned up material owed to several other chapters, four of which are already at **draft**, and the author asked for a record plus a decision on whether to apply it now.

**Decision, part one: a source document.**
`docs/pike-retrospective.md`, in the shape of `docs/ai-material.md` — the passages sorted by which chapter is owed them, with the fit argued once so the mentions agree.
It says at the top to read the talk rather than the file, because everything in it is an excerpt chosen for one argument, which is the partial reading `CLAUDE.md` warns about.

**What it assigns.**

*[Chapter 20](../20_idioms_7nkn.md)* gets the most, and the strongest. Pike says interfaces **coloured the team's thinking** in ways it took more than a decade to correct — an Idiom bounding what its own designers could imagine, which is a cost the chapter can state without needing a community that got something wrong. Second, the early compiler written in C against the language community's expectations: reason stated, offence taken, right at the time, and reversed later once the reason expired. That is 21's promised *declare it, document the reason, keep it narrow* with all three present.

*[Chapter 01](../01_the-five-kinds_cjx4.md)* gets a paragraph: Pike observing that what is good and bad in a language is largely opinion, argued with certainty. That is 02's *tone does not vary with authority*, witnessed by a language designer about arguments over his own language.

*[Chapter 08](../08_change_rjf9.md)* gets the compatibility promise priced by the person who made it — it costs, and it blocks feature-itis. The chapter argues the constraint; this is somebody adopting it deliberately as a feature.

*[Chapter 12](../12_missing-language-features_esqm.md)* gets a flagged maybe — the async/await aside and *coloured functions* — with an explicit instruction not to force it, since 13 is about patterns dissolving into features and this is closer to the inverse.

**Decision, part two: chapters at draft wait.**

Record now, apply when the chapter is next open.

Applying to four finished chapters at once means four review cycles in parallel, which is the batching this project avoids everywhere.
Material of this kind is strongest when the chapter is live, because the argument can be shaped around it — [chapter 14](../14_principle-loses-scope_b86v.md)'s use worked for that reason, and a quotation bolted onto a finished chapter is the decoration the register rules exclude.
And the precedent exists: `ai-material.md` holds material for 02 and 03 the same way, and the TOC's *Pending revisits* table is the mechanism for not losing it.

**The test that would have overridden this**, stated because it is the part that matters: **a revisit can wait, a contradiction cannot.**
The talk was checked against what is already shipped and contradicts none of it. Had it made a drafted chapter wrong rather than merely incomplete, it would not be a pending item.

**Consequence.**
`CLAUDE.md` names the document as the third of its kind and says when to read it.
`00_toc.md` gains three rows in *Pending revisits* and a block in [chapter 20](../20_idioms_7nkn.md)'s entry.
`LEDGER.md` gains two rows for 21, since those concepts are definite enough to be owned before the chapter exists.

---

## 75. Every chapter carries its own Sources section

**Date.** 2026-08-18

**Context.**
The drafted chapters cite roughly twenty works by name and year — Parnas, Conway, Fowler, Norvig, Pike, Ousterhout, the Gang of Four — and quote several of them directly, across about fifty-five blockquote lines.
They contained no external links at all: the only three URLs anywhere in the book pointed at FlowCore and at the book's own repository.
The author raised the gap and asked whether a references section was needed.

**Options.**
A back-of-book references appendix, derived at publication from an internal record; a list at the end of each chapter file; an internal record only, with nothing reader-facing.

**Decision.**
A `## Sources` section at the end of every chapter, in the back matter above the `**Next:**` line.

**The draft's recommendation did not survive, and the author's argument was the medium.**
The draft proposed `docs/SOURCES.md` — an internal record of what was cited and which form of each source was actually consulted — with a reader-facing appendix generated later, at publication.
The author's objection: this is a free online book whose chapters are separate files, and the README links readers straight into 03, 06, 07, and 10.
A reader arriving at [chapter 06](../06_distribution_49yh.md) from one of those links has no reason to know a references file exists elsewhere in the repository.
The sources belong where the reading happens.

That also absorbed the one job the internal record was for.
`CLAUDE.md` requires ranking the available sources and naming the one actually read — a rule that exists because [chapter 14](../14_principle-loses-scope_b86v.md)'s Pike material came from a third-party transcript read in excerpts.
Recording that in the chapter rather than in a private file matches how the book already handles its claims about itself.

**Why it is not an academic apparatus.**
`CLAUDE.md` states that provenance is written into the sentence and that there is no tagging notation.
The section is a lookup table, not a footnote system: no superscripts, no numbered markers, and no existing sentence altered.
*Parnas, 1972* stays where it is and also appears in the list.

**Consequence.**
[Chapter 14](../14_principle-loses-scope_b86v.md) was done first as the prototype, every link verified against the author's local source archive or fetched live.
`Sources` is now in the chapter rubric in `CLAUDE.md` and `README.md`, placed as back matter rather than as a seventh section, because it is not a step in the argument — so [chapters 01](../01_the-five-kinds_cjx4.md) and 16–23 are drafted with it.
[Chapters 01](../01_the-five-kinds_cjx4.md)–14 are retrofitted in the final sweep, decision 77.

---

## 76. Sources entries are bare, and links do not open in new tabs

**Date.** 2026-08-18

**Context.**
[Chapter 14](../14_principle-loses-scope_b86v.md)'s first Sources section annotated each entry with what the chapter had taken from it — which quotations came from the recording, which part of a large wiki page was used.
The author then asked whether the links could be made to open in a new tab.

**Decision.**
Bare entries: author, title, venue, date, link, and nothing else.
No new-tab behaviour.

**Why bare.**
The annotations restated what the chapter's prose already says.
The register rules exclude any sentence that would survive being deleted, and every note failed that test once the chapter above it had been read.
Two survived because they are citation data rather than commentary, and each prevents a reader thinking they have found an error: Ousterhout's slide deck is dated September 1995 while the talk is USENIX January 1996, and the *Wei Qi Shi Jue* is published in English under a different title.

**Why no new tabs.**
It is not possible where the book is actually read.
GitHub's sanitiser allows exactly one attribute on an anchor, `href`; `target` is stripped, and the request to support it in GitHub Flavored Markdown is still open.
Raw HTML anchors would replace clean Markdown in the source for no effect at all.

It would also be the wrong choice in a future HTML build, where a template could apply it.
WCAG places unannounced new windows under 3.2.5 *Change on Request*; the back button stops working, and screen reader and keyboard users are moved without being told.
Readers already have the choice through modifier-click, so setting `target` removes a decision rather than adding a capability.
The argument for new tabs is weakest exactly where these links sit — at the end of a chapter the reader has finished.

**Consequence.**
The format is recorded in the chapter rubric, so the annotations are not reintroduced by a later drafting session.
If an HTML edition is built, the useful template work is a stable anchor on the `Sources` heading, not link targets.
The bare-entry format is the author's call; the sanitiser and accessibility reasoning is the draft's, in answer to the author's question.

---

## 77. The final sweep is recorded as four slices, not as a list of rules

**Date.** 2026-08-18

**Context.**
`CLAUDE.md` changed 33 times between 3 and 17 August, while the fourteen drafted chapters were being written, so a chapter drafted early was held to fewer rules than one drafted late.
Three documents hold material owed to chapters, and `00_toc.md` carries an owed table.
The author planned a final pass over every chapter once all of them reach **draft**, and asked whether the references retrofit should run now as a separate sweep.

**Decision.**
No standalone references sweep.
The final sweep is recorded in `CLAUDE.md` as a four-slice task — pending material, rules, Sources, reconciliation — triggered when the last chapter reaches draft, begun only on the author's confirmation, with review between slices.

**Why references fold in.**
Building a Sources list means identifying every source a chapter cites and confirming what each one is, which is step one of the primary-source rule the sweep has to apply anyway.
Run separately, the expensive half is done twice.
Decision 74 had already settled the general form of this: record now, apply when the chapter is next open.

**A rule map was proposed and rejected.**
The draft offered `docs/late-rules.md`, mapping each rule to the chapters that predate it.
The author's objection settled it: the map would go stale the next time a rule was added, so it could not be useful.
It would also have been a third copy of what `CLAUDE.md` and git already hold, which is the duplication the survey rule exists to catch.

**What replaced it is derivation.**
Slice 2 says to check each chapter against the rules that postdate it, so a rule added later is covered without anyone editing the sweep.
One derived fact was kept, because it is about how to read git rather than a list that can rot: a `CLAUDE.md` commit that also touched many chapters was applied retroactively, and one that touched a single chapter was applied only there.
Running that query showed the two 14 August commits touching eleven and twelve chapters were real sweeps, and that the residue is roughly five prose-affecting rules concentrated in the earliest chapters — not 33 rules across fourteen chapters.

**Consequence.**
The slice order is stated as load-bearing, because each slice inspects what the one before it produced, with a note that content added during a slice has not been through the slices already finished.
The shape of the record is the author's; the slice contents and their ordering are the draft's.

---

## 78. Material documents move to `docs/pending/`, and `CLAUDE.md` points at the folder

**Date.** 2026-08-18

**Context.**
Slice 1 of the final sweep named `ai-material.md`, `speculative-abstraction.md`, and `pike-retrospective.md` individually, and `CLAUDE.md` described each with the list of chapters it was owed to.

**Decision.**
The three documents move to `docs/pending/`.
`CLAUDE.md` refers to the folder in both places that used to name them — the drafting instruction and slice 1 — and names no files.

**Why.**
The author's reason: a document can then be added or renamed without editing `CLAUDE.md`, and the sweep still functions.
It is the same derivation principle as slice 2, applied to material rather than to rules.

The per-file chapter lists went for the same reason, and one of them was already wrong.
`CLAUDE.md` said to read `ai-material.md` before drafting 02, 03, 15, 17, 19, 21, or 23; [chapters 01](../01_the-five-kinds_cjx4.md), 03, and 15 had all reached draft, and nobody had updated the line.
Each document tracks its own chapters in the table it already carries.

**Two calls made in the draft.**
The folder is `docs/pending/` rather than a root-level `pending/`, because `CLAUDE.md`'s own file convention puts chapters at the repo root and working documents in `docs/`.
A document leaves the folder for `docs/` when every piece in it has landed, rather than being deleted, because six `LEDGER.md` rows cite these arguments as provenance.

**Consequence.**
Seventeen paths updated across `CLAUDE.md`, `00_toc.md`, `LEDGER.md`, and cross-references inside the moved documents.
`DECISIONS.md` keeps the old paths: it is the historical record, and an entry written on 12 August should say where the file was on 12 August.
Slice 4 reconciles ledger rows, so it is where a path gets fixed when a document leaves the folder.

---

## 79. A source's register is not the book's

**Date.** 2026-08-19

**Context.**
[Chapter 16](../16_tdd-and-mocks_u8eu.md) takes its ordering argument from Fucci et al., read in full.
The draft that came back from that reading carried three stacked block quotes in the paper's own prose, including *"this advice would require a negative (statistically significant) coefficient, which the models did not produce."*
It also carried the paper's `GRA / UNI / SEQ / REF` abbreviations, each used once, and used *external quality* and *productivity* as if they were plain English rather than the paper's operationalized measures.

**The author's objection.**
The sentence could not be read in plain terms, and the style was not the book's.
Raised as two separate worries — that the quotation itself was impenetrable, and that importing that register anywhere in the chapter was inconsistent with the book's tone.

**Decision.**
Paraphrase the findings into the book's voice, keeping short exact fragments where the chapter needs to show the source said it.
Record the general rule in `CLAUDE.md`, after the primary-source rules, since it is what to do once the source has been read.

**Why this is a distinct failure from the one already recorded.**
Decision 71's rule — read the primary source in full, never splice inference into it — is about **attribution**: your reasoning presented as theirs.
This is about **register**: their prose presented as the chapter.
The two pull in opposite directions if either is taken alone, which is why the new rule states explicitly that it does not loosen the quotation requirements: quoted words stay exact, and a paraphrase must read as the book's own sentence.
Both are satisfied by keeping the two visibly separate on the page.

**What the rule says.**
Say what was measured, not what it was called — an operationalized term is a definition wearing a name.
Leave the source's abbreviations in the source; they earn their place in a document that repeats them a hundred times, not in a chapter that uses them twice.
Paraphrase for meaning, quote for provenance, and prefer a short fragment over a long block.
The symptom named for future review is a paragraph the reader must decode rather than follow, in a chapter that was going fine until the citation arrived.

**The sweep was scoped before it was proposed.**
The author asked whether earlier chapters need the same pass.
A survey found the problem contained: one block quote over 200 characters in the whole book — Conway's, in [chapter 08](../08_change_rjf9.md), which the chapter's argument turns on and which is his own plain wording — and three hits for statistics vocabulary, all of them ordinary usage (*control group* describing a study's limits, *correlate* in its everyday sense).
So no standalone sweep. [Chapter 07](../07_scale_637f.md) had already been through a jargon pass in August, and anything not visible to this survey is covered by the final sweep's slice 2 (decision 77), which checks each chapter against the rules that postdate it — a set this rule now joins.

**Consequence.**
The [chapter 16](../16_tdd-and-mocks_u8eu.md) section reads as three plain statements with short quoted fragments attached, and states the study's outcomes as what they measured rather than as their names.
`CLAUDE.md` gains the rule; no chapter is reopened for it now.

---

## 80. Speculative abstraction gets [chapter 18](../18_force-map-method_r37x.md); 19–23 renumber to 20–24

**Date.** 2026-08-20

**Context.**
`docs/pending/speculative-abstraction.md` had carried an open question since it was written: [chapter 17](../17_abstraction-as-insurance_4jk6.md)'s subject is a structural idea expressed as directories, this argument is about abstraction bought as insurance, and the two are adjacent without being the same.
It marked the resolution as the author's call.
Drafting 18, the draft answered the question itself and folded both into one chapter, joined by an *and* in the claim sentence.

**The author rejected it on review**, on the grounds that the two ideas are not tied by anything and that binding two claims with *and* and hoping is a failure the book has seen before.

**What settled it.**
Language-dependence. Everything in 18 — the export bill, `internal/`, the mapping tax, the three-language table — changes with the language. The insurance argument is identical in every language, being about time and data.
A chapter titled *versus the language* cannot rest half its length on an argument in which the language never appears.

Two further confirmations the draft had missed. 18's own contents line in `00_toc.md` already scoped it correctly — exports, mapping tax, the `internal/` manoeuvre, three layouts — a complete chapter with no abstraction material in it. And FlowCore's decision 1 supplied the two items the first draft skipped, so the material was available and unused.

**Decision.**
A new [chapter 18](../18_force-map-method_r37x.md), *Abstraction as insurance*, running *depend on abstractions, not concretions*.
Part IV becomes five chapters; 19–23 renumber to 20–24; the book is twenty-four chapters.

**On which slogan moved.**
The author's recommendation was to take *the database is a detail* out of 18.
The draft argued the reverse and the author accepted: *the database is a detail* is what puts persistence in its own ring, so it is the layout slogan and stays in 18; *depend on abstractions* is what produces the interface, so it goes to 19.

**The umbrella alternative, considered and declined.**
The author offered a pattern worth keeping for later: a chapter can carry two claims under one umbrella idea, both supporting it.
It was the wrong tool here because the two claims share a villain rather than a mechanism, so the umbrella would have to be something like *the doctrine's artifacts transfer and its benefits do not* — too general to be checkable, which the claim-sentence rule already forbids.
Worth noting that the draft had written a version of that sentence into 18's *Why the claim holds*, where it read as a good line rather than as a claim doing work.

**The renumbering.**
Twenty-nine references across twelve files, swept descending so the ranges never collide, and restricted to chapter-context forms — `chapter NN`, `Ch. NN`, `cite NN`, TOC headings, bare table cells, filenames, `belongs to NN`, `(→ NN)`.
A numeric sweep would have corrupted *16 of 23 patterns* in [chapter 12](../12_missing-language-features_esqm.md), *a team of 20* in [chapter 08](../08_change_rjf9.md), and `Trace.java:19` in 13. Every changed line was reviewed.

`docs/DECISIONS.md` is deliberately **not** renumbered, on the same reasoning as decision 78's file paths: an entry written when 19 was the force-map method should say 19. This entry is the key for reading the earlier ones.

**Consequence.**
`README.md`'s count and status line, and the count words in `tools/check-drift.py`, move to twenty-four.
`docs/pending/speculative-abstraction.md` records the question as settled and now owes only one line, to [chapter 20](../20_idioms_7nkn.md).

**The pattern worth recording, because it is the second instance.**
A working document said *this is the author's call*, the draft formed a view and shipped the view instead of the question.
[Chapter 16](../16_tdd-and-mocks_u8eu.md) had the same shape when the draft decided a paper's conditions were its to summarize.
Flagging rather than resolving is the cheaper error in both directions, and the draft has twice taken the expensive one.

---

## 81. The scope was written down in all four Part IV cases

**Date.** 2026-08-20

**Context.**
Reviewing [chapter 18](../18_force-map-method_r37x.md), the author objected that *depend on abstractions, not concretions* was being treated as a scopeless slogan when it is the Dependency Inversion Principle and has a reachable statement.
That was right, and reading the source falsified the chapter's claim.
The author then ran the same check over 16, 17 and 18 and collected the objections in `docs/pending/claim-research.md`, in the shape that had worked: the objection, the reasoning, and a lead rather than an answer.

**What the four sources say.**

*[Chapter 15](../15_behaviour-placement_z47a.md).* Riel's heuristic 2.9 is *keep related data and behavior in one place*, and his own gloss defines *related* — "the two areas are actually of the same key abstraction." By his 2.8 an order and a customer are two abstractions, so the chapter's case is outside the heuristic's stated reach. His introduction calls all sixty *warning bells* rather than rules, says it is "perfectly valid to state that the heuristic does not apply," and was written expressly to avoid what happened to *goto considered harmful*.

*[Chapter 16](../16_tdd-and-mocks_u8eu.md).* Fowler named two schools in 2007 — classical and mockist — and came down classical. *Mock your dependencies* is one side of a recorded disagreement stated as if it were the only side. Beck's own statement of the TDD loop mentions no mocking, no isolation requirement and no speed requirement.

*[Chapter 17](../17_abstraction-as-insurance_4jk6.md).* Martin separates the data model, "highly significant to the architecture of your system," from the database system, "a low-level detail — a mechanism," and his 2012 post is about deferring the choice rather than hiding it.

*[Chapter 18](../18_force-map-method_r37x.md).* Martin's 1994 paper names stability as the test and derives stability from plurality: "the more varieties of Reader and Writer exist, the more dependents these classes have."

**Decision.**
All four chapters rebuilt on their sources; all four dropped from **draft** to **in progress**, since a falsified claim is a contradiction rather than a revisit.

**The finding, and where it landed.**
The compression survives and the qualification does not, four times out of four, across four independent sources.
That is a sharper thesis than *this advice is vague*, and it changes what [chapter 14](../14_principle-loses-scope_b86v.md) could say: its cost section asserted that "usually nobody wrote it down," directly above four counter-instances.

[Chapter 14](../14_principle-loses-scope_b86v.md) now splits the case by who said it, and states the consequence: **prominence is what makes advice travel and also what makes its scope recoverable, and only the first gets used** — so the failure is retrieval rather than preservation, and retrieval fails because the compressed form is complete enough to act on.

**What was declined.**
A Part IV framing line saying the pattern held four times. The author's call, and skipped.

**Two corrections to the draft's own work, recorded because both were overclaims in the book's own diagnosed shape.**
[Chapter 15](../15_behaviour-placement_z47a.md) had asserted the advice "has no author," on the strength of one failed fetch, and made the absence load-bearing.
It had also used Riel's 4.6 as a cohesion test that a two-entity rule fails; 4.6 detects a class holding two abstractions, which is the opposite failure.
[Chapter 16](../16_tdd-and-mocks_u8eu.md) had said mocking is taught with test-first "and always has been," which Beck's canon contradicts.

**Consequence.**
`docs/pending/claim-research.md` is marked consumed and records where each source was found.
**2026-08-22:** deleted, once all four outcomes were verified in the chapters and every source had a line in a chapter's own Sources section. Decision 83 records the fourth brief's outcome, which was that its chapter went.
Riel's book was read from the author's local copy; its PDF stores text as subset-font glyph ids, decoded with a uniform `gid + 29` offset verified against known words.
Two sources remain unreached and nothing is claimed from them: Rafique and Mišić's meta-analysis, and Martin's 1996 *C++ Report* paper, which exists only on `web.archive.org`.

---

## 82. Part IV cases are not claim chapters

**Date.** 2026-08-22

**Context.**
[Chapter 14](../14_principle-loses-scope_b86v.md) states a mechanism and [chapters 15](../15_behaviour-placement_z47a.md) through 19 were planned as case studies of it — "the mechanism, stated once, so the case studies can be short."
They were drafted in the general rubric anyway, opening on a bolded claim sentence like every other chapter.

**The author's diagnosis, after a full re-read of 15–19.**
The four claim sentences are not claims. They are loose summaries, and forcing the rubric is what produced them.

Checking it against the four confirmed a sharper version. Each of those chapters carries two different kinds of content:

- **A particular** — this piece of advice had a stated scope, here it is, here is what travelled instead. That is *evidence for [chapter 14](../14_principle-loses-scope_b86v.md)'s claim*, not a claim.
- **A general** — a value graph with a cycle breaks generic walkers; a test can only fail for reasons it can reach; a directory costs whatever the language ties to it; an abstraction's stability comes from having dependents.

The single `## The claim` slot forced the two together, and every one of the four came out as two assertions joined by a connective: 16's *"drops two qualifications … **and** placing each such rule leaves a reference pointing each way"*; 17's *"**Neither** X **nor** Y …"*.
That is the same welding the author rejected in [chapter 17](../17_abstraction-as-insurance_4jk6.md) at decision 80, which was treated then as one chapter's mistake. It was systemic and the draft did not see it.

**Decision.**
A stated Part IV shape, recorded in `CLAUDE.md`, replacing the claim rubric for [chapters 15](../15_behaviour-placement_z47a.md)–19 only: the advice, what the source said, what the wide reading produces, why it is the reading that gets taken, where the wide reading is right, what the alternative costs, how to recognize it.

The mandatory counter-example survives unchanged; only its framing moves, from *where this claim doesn't apply* to *when following the compressed version is correct*. Chapters before Part IV keep the general rubric, because they do make claims of their own.

**Consolidation, considered and declined.**
The author left the call to the draft. The test applied was what would be lost: the verified `StackOverflowError` and `json.Marshal` cycle error, Fucci read in full with its five conditions, the `undefined: store.scanOrder` compile error and the three-language table, SQLite refusing `for update`, and FlowCore's decisions 1, 3 and 37.
That evidence is spread roughly evenly across the four, and a merged chapter keeps the narrative while dropping the demonstrations — which inverts the book's rule that the code should be the argument.
Length was never the problem. The manufactured claim was.

**Consequence.**
[Chapter 15](../15_behaviour-placement_z47a.md) is reworked first as the prototype, for review before 17, 18 and 19 follow.
[Chapter 14](../14_principle-loses-scope_b86v.md)'s line *"Part IV is four case studies, and this chapter is the mechanism they share, stated once"* stops being descriptive and becomes the thing that licenses the different shape.

---

## 83. *The database is a detail* is cut, and with it [chapter 17](../17_abstraction-as-insurance_4jk6.md)

**Date.** 2026-08-22

**Context.**
[Chapter 17](../17_abstraction-as-insurance_4jk6.md) ran [chapter 14](../14_principle-loses-scope_b86v.md)'s mechanism on *the database is a detail*, and demonstrated the cost with a Go package split that publishes the helpers it was drawn to hide.
Reworking it into the Part IV case-study shape did not fix it, and the author called the result a failure: two unrelated things bundled under a common theme.

**The decisive argument, which is the draft's and is stronger than "uninteresting".**
Every other Part IV case shows damage that follows from the *reading*. This one does not.
The export bill is a property of Go's package semantics, paid identically whatever the motive for the split — and the chapter's own boundary section conceded it: *"Splitting a package to break a dependency cycle is [chapter 04](../04_structure_agjy.md)'s third option, and it works — the cycle is gone whatever the export cost."*
So the demonstration was never a demonstration of the advice. It was a Go fact welded to a Martin sentence, which is the third time in Part IV the draft bound a real finding to advice it does not follow from.

**The author's argument for cutting the database material entirely**, which the draft had wanted to salvage into [chapter 16](../16_tdd-and-mocks_u8eu.md).
*Clean Architecture*'s chapter 30 is titled *The Database Is a Detail* and opens: *"From an architectural point of view, the database is a non-entity — it is a detail that does not rise to the level of an architectural element. Its relationship to the architecture of a software system is rather like the relationship of a doorknob to the architecture of your home."*
The distinction the draft found — data model significant, database system a mechanism — comes later in the same chapter.
That is not a scope stated plainly and lost in transmission. It is a chapter that opens on a maximal claim and qualifies it in its own pages, and untangling that is the original author's responsibility rather than this book's.

It would also have contaminated the pattern. Riel's *related*, Fowler's two schools and Martin's stability criterion are clean transmission losses; authorial overreach-then-hedge is a different phenomenon, and mixing it in makes Part IV mushier rather than broader.

**Decision.**
[Chapter 17](../17_abstraction-as-insurance_4jk6.md) is deleted. Part IV is 15 plus three cases: OOP and the direction rule, TDD and mocks, abstraction as insurance.
[Chapters 18](../18_force-map-method_r37x.md)–24 renumber to 18–23; the book returns to twenty-three chapters.

**What was salvaged, and what was not.**
`docs/pending/layout-and-language.md` holds the Go compile error, the `go doc` output, the `internal/` reasoning, the mapping tax and the three-language table, owed to [chapter 20](../20_idioms_7nkn.md) as one section. A directory means a package in Go, nothing in C# until assemblies split, and nothing enforced in Python — which is an idiom finding, and *why ecosystems diverge* is the chapter for it.
The database material is not salvaged anywhere.

**Consequence.**
[Chapter 04](../04_structure_agjy.md) loses three cross-references to a chapter that no longer exists; two of its sentences already stated the finding in full, so only the pointers went.
Five ledger rows move to 21 and three are deleted.
`CLAUDE.md`'s Part IV shape, [chapter 14](../14_principle-loses-scope_b86v.md)'s case counts in four places, [chapter 15](../15_behaviour-placement_z47a.md)'s opening, the README count and the drift checker's count words all follow.

---

## 84. Chapters and reviews are worked by interview

**Date.** 2026-08-23

**Context.**
[Chapter 18](../18_force-map-method_r37x.md) documents grilling — an interview conducted before generation, in which each decision is put to the human with a recommended answer, one at a time. Until now it was material the book described rather than a way the book was made.
The author ran [chapter 19](../19_six-profiles_dnkz.md)'s first review that way instead of tagging and waiting, and then asked for it to become standing practice for both drafting and review.

**Decision.**
`CLAUDE.md` gains a *Grilling* section under *How we work*, with the procedure stated as Claude's behaviour rather than as a prompt, and pointers to it from the drafting rule and from step one of the review cycle.

**What the [chapter 19](../19_six-profiles_dnkz.md) session added to the technique as documented.**
Three things, all learned by doing it and none of them in the original prompt.

**Order the questions by dependency.** Terminology had to be question one, because the title, every section heading, the TOC entry, three ledger rows and two cross-references inherited from it. Asked later, it would have been asked twice.

**Look up the blast radius before asking.** Counting *domain* across the book — 71 uses, only three outside [chapter 19](../19_six-profiles_dnkz.md) in that chapter's sense — turned a matter of taste into an easy decision, and it was Claude's job to find that rather than the author's to weigh it.

**Surface what the author did not tag.** Two items came out of that session unprompted: the file needed renaming because its slug carried the removed word, and the Sources section listed a work the chapter never cited.

**The limit, stated because the book states it.**
Grilling is slow by design, and [chapter 18](../18_force-map-method_r37x.md) records that as one of its costs.
A review that is three typos is applied rather than interviewed, and the test written into `CLAUDE.md` is whether any item would change what the other items should be. Where nothing depends on anything there is no tree to walk.

**Consequence.**
The review cycle's shape is unchanged — the author still reviews in the file, still commits, and Claude still commits one pass at a time. What changes is that between their commit and Claude's there is now a conversation, and the work is applied in one go at the end of it rather than tag by tag.

## 85. [Chapter 19](../19_six-profiles_dnkz.md): *extreme* was a private synonym for a term [chapter 02](../02_forces_f4m5.md) owns

**Context.**
[Chapter 19](../19_six-profiles_dnkz.md)'s second review raised four things, and the first one governed the rest.
The chapter defined a force profile as a reading "with at least one force pinned at an extreme," and used *extreme* ten times as its threshold word.

**The author rejected it on meaning:** *extreme* evokes rareness, and the threshold is not at 99% — a force tipped to 70% is enough.
They proposed *significant intensity* instead, and said they believed *intensity* had been used in an earlier chapter.

It had, and more heavily than the suggestion assumed.
[Chapter 02](../02_forces_f4m5.md) defines it at line 11 — *"Intensity means **how hard the Force presses on the design**, which is not always the same as how large the number is… Read the pressure, not the number"* — uses it thirteen times, and [chapter 11](../11_patterns-that-survive-translation_us2k.md) leans on it to choose between patterns answering the same Force.
So the author's objection was already the book's stated position, and *extreme* was not merely evocative: it was [chapter 19](../19_six-profiles_dnkz.md) inventing a private synonym for a term another chapter owns, which is the drift `docs/LEDGER.md` exists to prevent.

**Options for the threshold word.**
*Significant intensity*, the author's proposal.
*High intensity*.
No adjective at all.

**Decision, reached jointly.**
The draft argued against *significant* — an evaluative adjective is a judgment about the reading rather than a position on [chapter 02](../02_forces_f4m5.md)'s dial, which the register rules exclude — and proposed instead a sentence [chapter 19](../19_six-profiles_dnkz.md) already contained.
Line 142 read *"A profile is where one force leaves the ordinary range and stays there."*
That answers the rareness objection directly, needs no new vocabulary, and pairs with the chapter's own boundary section on the ordinary case, so the two now share wording.
The definition is: **the reading of every force bearing on a system, with at least one at an intensity outside the ordinary range, and staying there.**

Neither party arrived with this.
The author had the objection and a word; the draft had the survey showing the word was owned elsewhere; the answer was a sentence already in the file that nobody had noticed was the definition.

**The plural, and where it went.**
The author had edited the claim to *"which advices holds"*, reasoning that a profile is not a single force and that many pieces of advice follow from one.
*Advices* is not English and the verb did not agree, so the claim reverted to *advice*, which as a mass noun already refers to many.
The reasoning survives in the definition, which is a better home for it: it is a fact about profiles rather than about grammar.

**Three further corrections in the same review.**

**The business does tell you.**
The chapter's central demonstration — two sales systems with opposite concurrency readings — ended *"Nothing about knowing the business tells you that."*
The author rejected it: the business said so literally, in the sentence describing several people working the same proposal at overlapping stages.
They were right, and the chapter already contradicted itself about it — its *Why the claim holds* section says the reading *"comes from someone who knows how ports buy security systems."*
The missing distinction is between the domain as a label and the domain as detail: both systems are "sales software" and share a vocabulary, and what separates them is a fact about how the work is done, which is business knowledge.
The paragraph now concedes it and takes the sharper point, that the reading is available from the business but not in answer to the question usually put to it — *what are the things called* gets the same reply from both companies, *who touches a proposal, and when* gets opposite ones.
This converts *"you have to read the forces"*, an instruction with no method, into a question that can be asked.

**The table said `profile` over a column of domain names.**
The author noticed that the six labels — line-of-business, games, embedded, compilers, UI frameworks, distributed — are domains, in a chapter whose claim is that domain and profile are different axes.
The draft recommended fixing both column headers rather than one, so the left column is demoted rather than left ambiguous, and against the thorough version of the fix.
Renaming the six profiles by their forces — *durable-schema*, *frame-budget*, *hard-deadline* — is more honest and was rejected: it makes the chapter navigable only by a reader who can already read force profiles, which is the skill the chapter exists to teach.
Someone who works on embedded systems finds their section by the word *embedded*.
A sentence under the table now says the left column is where a profile is commonly met rather than what it is, and that the two sales systems share a domain and would not share a row.

**A misattribution the review did not tag.**
[Chapter 19](../19_six-profiles_dnkz.md) said the UI-framework force sits *"at the value [chapter 02](../02_forces_f4m5.md) names as the extreme."*
[Chapter 02](../02_forces_f4m5.md) names no such value; it gives control of the callers three intensities, the third being *"you can neither see nor change them."*
Fixed to name the actual position.

**Consequence.**
Ten uses of *extreme* in [chapter 19](../19_six-profiles_dnkz.md), one heading, two TOC lines, and four ledger rows changed, including [chapter 02](../02_forces_f4m5.md)'s own row, whose canonical citation was *"read the value"* and is now *"read the intensity"* to match the chapter's bolded term.
[Chapter 18](../18_force-map-method_r37x.md) is at draft and was touched once, in its handoff line, where *"each one's dominant force"* was singular against a definition that permits several — games pins the frame budget and the memory hierarchy, embedded pins the deadline and the absence of a heap.
Its force-map cell reading `extreme` was left alone: there the word is ordinary English about one reading, in a row that also carries `none`, `real` and `unknown`, and [chapter 19](../19_six-profiles_dnkz.md) giving up the word as vocabulary does not oblige the book to give up the adjective.

## 86. One idea, seven places: the repetition the ledger had no row for

**Context.**
[Chapter 19](../19_six-profiles_dnkz.md)'s third review objected to a paragraph explaining that two people arguing about whether logic belongs in the database are really disagreeing about forces.
The author's note: *"this 'two people arguing both are right' theme was used maybe 5 times in the book with near identical idea… You need to do something about this problem. It's ok to edit older chapters."*

**The survey, and a false start.**
The first pass was run case-sensitively and missed every instance that begins a sentence, which produced a count of five and a plan built on it.
Re-run properly, the idea appears seven times: [chapter 01](../01_the-five-kinds_cjx4.md) twice, [chapter 02](../02_forces_f4m5.md) twice, [chapter 18](../18_force-map-method_r37x.md) twice, [chapter 19](../19_six-profiles_dnkz.md) once.
The correction was reported before the second decision was taken rather than after, and the three sites already agreed were the right three.

**The cause is a ledger defect, as `CLAUDE.md` predicts.**
No row in `docs/LEDGER.md` owned the concept.
With no owner, four chapters each re-established it, and — this is what made it invisible — each one politely cited the others while doing so.
[Chapter 02](../02_forces_f4m5.md) cited 02, [chapter 18](../18_force-map-method_r37x.md) cited 03, [chapter 19](../19_six-profiles_dnkz.md) cited 03.
A citation reads like deference to an owner, so nothing looked wrong at any single site.

**Decision.**
[Chapter 02](../02_forces_f4m5.md) owns the mechanism, since it is the Forces chapter and states it at line 393.
[Chapter 01](../01_the-five-kinds_cjx4.md) keeps one sentence and its handoff, which is exactly what the anti-repetition protocol allows.
Four sites were cut:

**03:504** said it a third time, thirty pages after 393, before delivering its remedy.
The restatement goes; the remedy stays.

**19:288** recapped [chapter 02](../02_forces_f4m5.md)'s finding in two sentences with a citation attached, and carried a remedy nearly identical to 03's.
Reduced to the trigger plus [chapter 18](../18_force-map-method_r37x.md)'s own remedy, which is the force map rather than 03's advice.

**20:143** spent four sentences rebuilding 03's case to reach one clause of new material.
That clause is genuinely [chapter 19](../19_six-profiles_dnkz.md)'s and was kept: **an ordinary force disagreement ends when somebody measures, and a profile disagreement does not**, because each side is reading a force that will not move in their own system.
So 20 now owns the stability and nothing else.

**20:221** duplicated 20:185 — the senior person who is right somewhere else — thirty-six lines apart, inside one chapter.
Replaced.

**Two ledger rows added**, which is the actual fix: one assigning the mechanism to 03, one recording that 20 owns only the non-resolution.

**Four passages that look like the theme and are not**, left alone: [chapter 04](../04_structure_agjy.md)'s folder-structure pair are confusing an Idiom for a Law, [chapter 10](../10_patterns-that-cross_r8dw.md)'s two engineers are picturing different scopes of one word, [chapter 18](../18_force-map-method_r37x.md):33's pair is about which arguments are winnable at all, and [chapter 01](../01_the-five-kinds_cjx4.md):263 is about litigating the classification.

**Three further items in the same review.**

**A loaded word.**
The author asked what *framework* meant in a recognition bullet and whether *tech stack* was intended.
It was not: [chapter 19](../19_six-profiles_dnkz.md) defines the term in its own UI-framework section — a framework calls you, a library is what you call — but the bullet did not recall that, so the loaded reading was available.
Retitled *Fighting the lifecycle*, with the distinction restated in the clause.

**A bullet that named no failure.**
*"A god object that only has fan-in… if it does not, it may be an AST"* asked the reader to supply the failure themselves.
Now concrete: five named consumers each get a narrowed view of the syntax tree and adapter code to convert back, so a change touches the tree and five translations of it.

**The conversation list was [chapter 02](../02_forces_f4m5.md)'s list.**
The author asked for the bullets to be tied to force profiles.
Doing it revealed why they needed it: *"That's not how it's done"* was already [chapter 02](../02_forces_f4m5.md)'s opening bullet in the same kind of section, and the senior-person bullet was [chapter 19](../19_six-profiles_dnkz.md)'s own line repeated.
Naming a profile in each is what makes the list [chapter 19](../19_six-profiles_dnkz.md)'s — the database bullet is line-of-business, premature optimization is frame-budget and hard-deadline, *"we're not Google"* is the distributed profile — and two bullets that could not be tied were replaced.

**One direct edit reverted.**
The review restructured the claim section's two definitions into a list under *"To make the claim precise two terms need to be settled:"*.
The list is an improvement and was kept; the lead-in is announce-then-deliver, which `CLAUDE.md`'s cadence rule names explicitly and which commit `052d09d` cut from [chapter 14](../14_principle-loses-scope_b86v.md)'s opener.
The edit had also dropped that *domain* keeps its meaning book-wide rather than only in this chapter, which is what stops a reader treating it as local jargon; restored.

## 87. The Idiom/Style line is mechanical, and [chapter 20](../20_idioms_7nkn.md)'s claim is about conditions

**Context.**
[Chapter 20](../20_idioms_7nkn.md) was drafted through a grilling session — four questions, each answered before the next was asked, nothing written until the author closed the interview.
This entry records the exchange rather than only the outcome, at the author's request: *"grilling is like interactive reviewing so remember to log all my input and important decisions."*

**Question 1 — the claim.**
The draft offered three candidates: divergence, obedience, and a third it recommended, that an Idiom grows from **a language feature you can name**.

The author asked how FlowCore's decision 18 was related to it.

It was not, and the question exposed two faults.
The draft had described the decision from memory and got it wrong — it gave this book's decision 49's reasoning, a reader who sees a sample once, where FlowCore 18's is a maintainer returning after a context switch, for whom decoding an abbreviation never amortizes.
`CLAUDE.md` already says the two were adopted on different grounds, and the draft collapsed them.

The larger fault was in the claim.
Go's short-name convention traces to no language feature — there is nothing in Go that makes `def` cheaper than `definition` — and Pike's compiler-in-C deviates from a community expectation rather than from a feature.
Two of the three pieces of evidence did not fit the claim they were offered for.

**Decision, reached jointly.**
Widen the thing that must be nameable from a language feature to **a condition about your surroundings** — the language, the tooling, or who will read the code.
That keeps the Idiom distinct from the Principle by where the condition is looked up: a Principle's is a fact about your system, an Idiom's is a fact about your situation in an ecosystem.
Neither party arrived with this; the author had the objection, the draft had the survey showing the evidence did not fit.

**Question 2 — where the short-name material belongs.**
The draft proposed keeping it in 21 on the test *if deviating from it required a written reason, it was never Style.*

The author rejected it with two counters, both correct.
The scope-length argument behind Go's short names is not Go-specific, so it cannot explain why only Go adopted the convention.
And most Style has a stated reason from some authority if you dig — PEP 8 and gofmt both give reasons for pure formatting — so *has a stated reason* does not discriminate.

**The author's replacement, which is now the book's rule.**

> It's style if your choice doesn't change the execution of code. It's an idiom when the execution changes even when the behavior is the same, ex: DI.

The draft checked it against [chapter 01](../01_the-five-kinds_cjx4.md)'s twenty-claim table and it sorts all six Idiom/Style rows correctly with no judgement call, which the draft's test could not do.

**One refinement from the draft, accepted.**
*Execution* alone mis-sorts the layout material: splitting a Go package changes what compiles rather than what runs, and under a strict reading that would make it Style and cost [chapter 20](../20_idioms_7nkn.md) its strongest demonstration.
So the test is whether **the compiler or the runtime** acts on the choice, while the program behaves the same either way.

**Consequences.**
Short names are Style and move to [chapter 21](../21_style_9rng.md), and 02's table gains the row, because it is the case where intuition fails — Go-specific and still Style.
[Chapter 01](../01_the-five-kinds_cjx4.md)'s question 4 was catching short names before question 5 could sort them, so ecosystem-specificity is now stated as a consequence of the answer rather than as the test.

And the rule turned up better material than it cost.
**The line falls in a different place in each language**, and the two places it moves are exactly the two things everyone files under Style: Go makes an identifier's case an access modifier, and Python makes indentation syntax.
[Chapter 20](../20_idioms_7nkn.md) owns that; 02 owns the test.

**Question 3 — the chapter's evidence was all Go.**
The layout material, the capitalization finding and both Pike passages are Go, in a chapter arguing that you cannot see an ecosystem from inside it.
The draft proposed running the *same* package split in Python rather than tabling it, and the author took the shape as drawn.
Both halves were executed: Go refuses to compile, Python reaches the underscore-prefixed helper across the boundary and runs.
C# is given as mechanism without output, since the toolchain is not available here.

**Question 4 — the claim sentence.**
Adopted: *an Idiom rests on a condition about your surroundings rather than about your problem, and naming that condition is what separates deviating from an Idiom from merely ignoring one.*

The draft offered a stronger alternative — *defensible **exactly when** you can name the condition* — and argued against its own suggestion, because *exactly when* claims sufficiency and the chapter's counter-example disproves it.
That is the standing bias `CLAUDE.md` records — claiming sufficiency where only necessity was shown, which cost [chapter 02](../02_forces_f4m5.md) two drafts of its claim — caught this time before shipping rather than in review.

**What reading the primary source in full supplied.**
The Pike talk was read end to end rather than from the excerpts in `docs/pending/pike-retrospective.md`, and it contained something that file had missed.
Ian Taylor pushed the team to face the generics problem "from early on", and Pike ties the difficulty directly to the convention's standing — it was hard "given the presence of interfaces as the bedrock of Go programming".
That is what makes the interfaces case a boundary rather than an anecdote: the alternative was named early, from inside, by someone who was right, and the convention held for a decade regardless.

**One claim cut for want of evidence.**
The draft asserted that `defer file.Close()` returns success on a truncated report, and could only produce that by closing the handle mid-function — harness-shaped code that no caller writes.
The demonstration was dropped rather than dressed up.
The chapter now shows `Close`'s signature, which is structural and needs no run, and states the mechanism: on a network filesystem the failed write surfaces at close and nowhere earlier.

**Also fixed.**
Four ledger rows owned by 21 still cited "[Ch. 17](../17_abstraction-as-insurance_4jk6.md)" after the renumbering that cut the old [chapter 17](../17_abstraction-as-insurance_4jk6.md), and `docs/pending/layout-and-language.md` carried the same fossil in its own body.

## 88. Grilling sessions are logged, not just their outcomes

**Context.**
`CLAUDE.md` gained a *Grilling* section in decision 84 describing how the interview is run, and said nothing about recording it.
Decision 87 was written because the author asked for it in the moment — *"grilling is like interactive reviewing so remember to log all my input and important decisions"* — not because any rule required it.

**Decision.**
Two bullets added to the procedure: log the exchange rather than only its conclusion, and keep a running note while the interview is in progress.

**Why.**
Grilling is the format that generates the most attributable material and loses it the fastest.
In the [chapter 20](../20_idioms_7nkn.md) session the author rejected the draft's proposed test and supplied a replacement, the draft's own recommendation lost twice, and one question was settled by a fact discovered while answering it.
An entry recording only the result — *the Idiom/Style line is mechanical* — would read as though the draft had worked it out, which is the failure the attribution rules already name as the more damaging of the two.

The running note is the operational half.
By the fourth question the first exchange is easy to reconstruct wrongly and easy to reconstruct confidently, and the author's own words are consistently sharper than the paraphrase: *most of the things you will categorize as style will also have reasons stated by an authority if you dig deep enough* is the sentence that killed the draft's test, and a summary written later would have softened it.

**Consequence.**
Decision 87 is the worked shape for the format — questions in dependency order, the author's objections quoted, and the two places the draft's recommendation did not survive marked as such.

## 89. What "behaves the same" means, and one duplication the ledger did not catch

**Context.**
The first review of [chapters 20](../20_idioms_7nkn.md) and 02, worked as a grilling after a false start.
The draft applied the whole review directly and committed it; the author asked whether grilling had been used, and it had not.
The commit was discarded before it was pushed and the review restarted as an interview.

**Why it was skipped, recorded because it is the fourth instance of one pattern.**
The draft published its survey result before enumerating what the result permitted, and once a finding is stated the action reads as its consequence rather than as a choice with branches.
The draft had even named the fork in its own reasoning — *whether to keep 21's `internal/` and mapping-tax passages at all* — and then answered it, which is the behaviour decisions 80 and 81 already record.

The draft proposed adding a rule to `CLAUDE.md` about it.
**The author declined, and was right.** Grilling's fourth bullet already says the decisions are the author's and the facts are Claude's; the failure was of an existing rule rather than a missing one, and two prior entries recording the same pattern had not prevented it, so a third restatement is weak evidence. `CLAUDE.md` is loaded every session and the marginal rule costs attention whether or not it fires.

**The author's correction to the Idiom/Style test.**
Decision 87 settled the test as: the compiler or the runtime acts on an Idiom, *while the program behaves the same either way*.
Reviewing [chapter 01](../01_the-five-kinds_cjx4.md) the author rewrote the passage and caught that the last clause was doing unexamined work.
A container plainly does change behaviour — a missing registration fails at run time where a missing constructor argument fails at compile time — so as written the test's own worked example contradicted it.

Their fix names which behaviour is held constant and what that excludes:

> By "visible behaviour" we specifically mean what the software produces on success mode. Notice that this narrow definition excludes many areas: failure modes, developer experience, maintainability…

Kept in full, in the book's register.
The narrowness is what makes the test usable, and the excluded list is exactly what people reach for when arguing that a convention is more than a convention.
Checked against [chapter 01](../01_the-five-kinds_cjx4.md)'s table: the narrowing still sorts all four Idiom rows and all three Style rows with no judgement call.

Substance is the author's and unaltered. The draft corrected register and grammar — a bold lead-in standing alone as its own paragraph against the markdown conventions, *"Let's take a look at"* which appears nowhere else in the book, first-person plural used to define a term, and four slips — and merged the two parallel paragraphs into one, because they described the options rather than contrasting them.

**Question 1: the package-boundary material.**
The author asked for [chapter 20](../20_idioms_7nkn.md)'s passage to be *gauged* for repetition rather than assumed repetitive.

The survey says the three sites do different jobs, which is the division `docs/pending/layout-and-language.md` planned.
It also found a real duplication the ledger had not caught: [chapter 02](../02_forces_f4m5.md) already glosses what `internal/` is, and 21 explained it again from scratch, because **no row recorded 03's use.** Decision 86's shape exactly.

Three options were put: cite and keep, cut both elaborations, or move the mapping tax to [chapter 04](../04_structure_agjy.md).
**The author chose cite-and-keep.**

The draft's earlier private reasoning had been that the mapping tax weakens that option, since the same bill is charged in Go, C# and Java and so demonstrates no divergence.
Laying the options out disproved it: **the tax is only ever charged where the language forces a wall.** Python's split produces no second type and C# pays nothing until assemblies split. The tax is downstream of the language's decision, which is the chapter's subject.
That argument only appeared because the options had to be written down for someone else, which is the case for the interview and not for the draft's judgement.

**Question 2: an overlap created by the review itself.**
The author's new [chapter 01](../01_the-five-kinds_cjx4.md) passage and [chapter 20](../20_idioms_7nkn.md) both observed that a container moves a wiring mistake past the compiler.
[Chapter 20](../20_idioms_7nkn.md) was written before the edit existed, so neither cited the other.
**The author chose to keep it in 02 and drop it from 21**, on the draft's recommendation: in 02 the fact is the evidence that a compiler acts on the choice, which is the test itself; in 21 it was a bonus clause riding along beside the actual argument, which is about who constructs your objects.

**Consequence.**
A ledger row assigns the `internal/` gloss to 03. [Chapter 20](../20_idioms_7nkn.md) cites 03 for the mechanism and 05 for the general bill, and keeps its two contributions — what the directory is for, and the itemised mapping tax.
The row for the mechanical test now carries the narrowed definition.

## 90. The rewrite lost the point of the edit it was tidying

**Context.**
Decision 89 kept the author's narrowing of the Idiom/Style test and rewrote it into the book's register.
The author read the result and rejected it: *"my version of the previous paragraph reads much better then current one. I think if you compare the two again you will agree with me."*

**On comparison, correct, and for two reasons — one of which is not a matter of taste.**

**The definition was demoted into an aside.** The author's version gives it a sentence of its own: state the invariant, define the term, name the exclusions. The rewrite folded the definition into an em-dash clause. Pinning down what *behaves the same* means was the entire point of the edit being tidied, and the tidying buried it — the sentence that flags a term is being fixed deserves to be a sentence.

**And one of the rewrite's exclusions was wrong.** It listed "how much of the wiring a compiler can check" among the things free to differ. That is not an excluded consideration; it is the classification criterion. A compiler acting on the choice is exactly what makes something an Idiom, so the list named the test as one of the things the test ignores.

**Decision.**
The author's structure and list are restored — three sentences, one job each, and *failure modes, developer experience, maintainability*.
Only the defects are corrected: a missing full stop on the bolded sentence, *on success mode*, first-person plural used to define a term, *Notice that* as filler, a trailing ellipsis, and a subject that changed number mid-clause.

One deviation, flagged rather than silent: *acts on the Idiom but they ignore the Style* becomes *acts on an Idiom, and ignores a Style*, which fixes the number agreement and makes the two verbs parallel.

**The pattern worth recording.**
The register rules are for prose that has no other problem.
Applied to a passage whose structure was doing argumentative work, the tidying pass optimised the sentences and lost the shape — and produced an error in the list while it was at it.
Standalone bolded sentences were checked before restoring the author's: there are twenty-six in the book, so that form was never the defect.

## 91. A standalone bolded sentence is a signal, so it cannot be used for an ordinary topic sentence

**Context.**
The author's [chapter 01](../01_the-five-kinds_cjx4.md) edit put a blank line after its bolded sentence, leaving it standing alone, and then proposed removing it: *"it's a formatting that doesn't exist elsewhere on the book so it can trip the reader as well."*

**The premise is wrong and the conclusion is right, which is why the survey was worth running.**
The form exists seventy-three times. Counted by what follows the bolded line: forty-eight introduce a list, five introduce a code block, and twenty introduce prose.

The twenty prose cases are what matter, and they are not a general licence:

- **Thirteen are chapter claim sentences** — line 5 of every chapter that has one, which the rubric mandates.
- **Five are [chapter 04](../04_structure_agjy.md)'s enumerated markers** — *First, the small part*, *Option B*, *Four — replace a reference with an identifier*.
- **One is [chapter 02](../02_forces_f4m5.md) line 121**, and it is an outlier inside its own device: *What changes with the Force* appears six times in that chapter and the other five are inline.
- **One was [chapter 01](../01_the-five-kinds_cjx4.md) line 53.**

Against that, the inline form — a bolded lead-in continuing on its own line — is used **349 times**.

**Decision.**
Merged, as the author asked.

**Why the real reason is stronger than the stated one.**
The standalone form is not merely rare; in this book it *signals*. A reader who has met thirteen chapter claims and five enumerated options has learned that a bolded sentence alone on a line announces either the chapter's claim or a labelled branch of an argument. [Chapter 01](../01_the-five-kinds_cjx4.md)'s line was neither — it was the topic sentence of the paragraph directly beneath it, which is exactly the job the inline lead-in does 349 times.
So the objection is not that the reader has never seen the form. It is that they have, and it means something else.

**The same inconsistency in [chapter 02](../02_forces_f4m5.md), surfaced and then fixed on the author's instruction.**
*What changes with the Force* appears six times in [chapter 02](../02_forces_f4m5.md). Line 121 differed from the other five twice over: it stood alone, and it bolded the answer as well as the label, where the others bold only *What changes with the Force:* and leave the answer in plain text.
Both are now matched to the majority form. [Chapter 02](../02_forces_f4m5.md) is at draft, and the change is formatting with no word altered.

## 92. A discharged pending document is deleted, and why the draft moved one instead

**Context.**
[Chapter 20](../20_idioms_7nkn.md) reached draft, discharging `docs/pending/layout-and-language.md` entirely.
The draft moved it to `docs/`. The author's correction: **`docs/pending/` is a task list, and a finished task leaves nothing behind.**

**Why the draft moved it, which is the part worth recording.**
`CLAUDE.md` said so, in terms:

> A document leaves `docs/pending/` for `docs/` once every piece in it has landed; it is not deleted, **because the ledger cites these arguments as provenance.**

That reason is a condition, and the draft had already tested it.
Before moving the file it grepped for every citation of it, found exactly one — in `00_toc.md`, in an entry it was about to rewrite — and removed it.
It then recorded the result in its own reasoning as *nothing cites it, but `CLAUDE.md` says these docs are kept as provenance regardless*, and moved the file.

So the failure is not that the rule was misread.
**The rule's condition was checked, found false, and the rule followed anyway** — on the strength of the instruction while the reason for the instruction had already been disproved for this document.
It is the distinction [chapter 20](../20_idioms_7nkn.md) had just been written about, running backwards: the chapter's claim is that naming the condition is what separates deviating from ignoring, and here the condition was named, shown not to hold, and obeyed.

**The reason was not spurious in general.**
Seven ledger rows do cite pending documents — `ai-material.md` and `speculative-abstraction.md` — so the provenance concern is real for those.
It simply was not true of this one, which is what a condition is for.

**Decision.**
The document is deleted.
`CLAUDE.md`'s rule now says delete rather than move, with the reason stated positively: the argument lives in the chapter and the reasoning lives in this log, so a discharged working document is duplication.
It also says the ledger pointer goes with the document, which closes the gap the old reason was gesturing at — a row citing `docs/pending/x.md` is a pointer for a drafting session that has now happened, and it is spent once the chapter carries the argument.

## 93. `docs/pending/` becomes `docs/pending-tasks/`

**Context.**
Decision 92 established that the folder is a task list and a discharged document is deleted.
The name did not say that: *pending* describes the documents, and what the author wanted named is the work.

**Decision.**
The folder is `docs/pending-tasks/`.
`docs/pending/speculative-abstraction.md` was deleted in the same pass — every row of its own table read **done**, and the last piece owed, the line-of-business inversion for [chapter 19](../19_six-profiles_dnkz.md), is present at `19_six-profiles_dnkz.md:54`. Its header still claimed one line outstanding, contradicting its table. The single ledger pointer to it and the TOC line sending readers to it went with it.

Two documents remain: `ai-material.md`, owed to [chapter 22](../22_never-written-down_at4r.md), and `pike-retrospective.md`, owed to 02, 09 and possibly 13.

**What was updated, and what deliberately was not.**
Fifteen live references were changed — four in `CLAUDE.md`, six ledger rows, three in `00_toc.md`, two inside `pike-retrospective.md`.

**`docs/DECISIONS.md` was left alone**, and its fifteen occurrences of the old path stand.
This log records what was decided at the time, so rewriting the path inside decision 78 — titled *Material documents move to `docs/pending/`* — would make the entry describe a decision nobody took. Decision 92 quotes the superseded `CLAUDE.md` rule verbatim for the same reason.
A log that is silently updated to match the present cannot be used as evidence about the past, which is the job the README gives this file.

**One near-miss worth recording.**
`09_what-a-pattern-is-for_3xzc.md` contains `` `pending/` `` twice, in the passage about provisional names — a holding-pen folder in a hypothetical codebase, nothing to do with this repository's layout. A path-wide sweep would have renamed it and broken the example. It was checked before the sweep ran, not after.

## 94. [Chapter 21](../21_style_9rng.md)'s claim, and two examples the author rejected

**Context.**
[Chapter 21](../21_style_9rng.md) drafted through a grilling. Recorded per the rule added in decision 88.

**The claim, reached over three rounds.**
The draft proposed *the only reliable end is to take the choice away from the people having it*.
The author rejected the register — too dramatic — and proposed *only a resort to authority can end it*.

The draft objected on a specific ground rather than a general one: **authority is a defined term in this book.** [Chapter 01](../01_the-five-kinds_cjx4.md)'s own claim is that the kind of a claim *"determines how much authority it has"*, the four advice kinds *"form a ladder of authority"*, Style *"has no authority at all"*, [chapter 03](../03_grading-a-law_q5c6.md) has a section on where a claim's authority comes from, and 02 lists citing an authority rather than a mechanism as a failure symptom. So the sentence would have read as: Style has no authority, and what ends a Style argument is authority.

The draft's replacement, *the choice is made once for everyone*, the author rejected in turn — *"wishy-washy… evokes the images of endless style convention meetings"* — which was correct, since it reads as consensus where the point is decisiveness.

The author's next version supplied what the draft had been circling: **a person who can enforce a style decides to act.**
The draft objected to a fourth thing, its own habit: *somebody who can make it stick* was periphrasis where a plain noun would do. The author's phrasing is plainer and was kept.

**Settled:** *A Style discussion has no fact that would settle it, so it ends only when a person who can enforce a style decides to act — and everything before that produces nothing.*

*Wastes resources* became *produces nothing*, which is the chapter's finding rather than a complaint about cost: if there is no fact to find, the discussion cannot have found one.

**Two examples the author rejected, and why the second rejection was the sharper one.**

**Hungarian notation.** The author supplied Joel Spolsky's *Making Wrong Code Look Wrong* after the draft found the URL unreachable, and the draft read it in full. It contains the boundary in the source's own words — `us` and `s` for unsafe and HTML-encoded strings, *"both of type string… the compiler won't help you"* — and the Apps-versus-Systems split, where the useful version encodes what the compiler cannot know and the version that spread encodes what it already does.

The author read the draft's summary and cut it: *"very messy, hard to understand, hard to think about the meaning related to chapter."*
That is the right call and the reaction is the evidence for it. Landing one boundary would have cost Simonyi's paper, a misread word, two variants and Microsoft's documentation history, in a chapter the plan says should be short, for a reader who has only met the ridiculed version. One passage survives — Spolsky's six days arguing about brace style — which needs no exposition and is worth more than a complaint would be, since he spends the rest of the essay arguing that some naming conventions matter enormously.

**The trailing comma across two languages.** The draft then proposed: in Python the trailing comma looks like Style but has a fact behind it, the diff being three lines instead of one; in Go, omitting it is a syntax error.

The author: *"I think you cheated on this."* The two halves were in two different languages, which makes it [chapter 20](../20_idioms_7nkn.md)'s finding — the line moves by language — wearing a boundary's clothes.
They specified the shape instead: **one language, two options that both appear available, you pick the second, and the second was never a real option.**

That produced the boundary the chapter uses. The same trailing comma, inside Python: in a list it is Style and both forms build the identical object; in a one-element tuple it *is* the tuple, so `(order_id)` is an integer with brackets round it. Verified against `sqlite3`, which answers `ProgrammingError: parameters are of unsupported type`. The demonstration and the boundary now turn on the same token, so the chapter bounds itself without introducing a second subject.

**A test that failed, and what it changed.**
The draft expected two differently-formatted Go files to compile to identical binaries, and intended to use that as proof that no fact exists in the program.
They differ, and stripping debug information does not fix it: Go embeds a table mapping instruction addresses to source lines, which survives `-w -s`.

**That vindicates the author's narrowing in decision 89.** They had insisted the Idiom/Style test hold constant *what the program produces when it succeeds* rather than something looser. Had it said *the machine cannot tell the difference*, this chapter's own demonstration would have disproved it in four commands.
The chapter now states the caveat rather than hiding it.

**Two categories cut from the plan.**
The TOC promised naming, formatting, file layout and comment density. File layout's interesting half is [chapter 20](../20_idioms_7nkn.md)'s — a directory costs what the language ties to it — leaving *which folder*, and there is no material for comment density.
Cut, with the author's agreement, on the grounds that the entry says *short, deliberately* and filling a plan line by inventing material is how that stops being true.

**Verification.**
`gofmt` is available and its output is quoted from a run. Black and Prettier are not installed, so they are given as mechanism with no output claimed.
The naming demonstration turns on a verified silence: `gofmt` reports nothing about `a` versus `amounts`, which is why naming arguments outlive formatting ones.

## 95. [Chapter 21](../21_style_9rng.md) review 01: a caveat written to defend the test against a fact that was never about it

**Context.**
First review of [chapter 21](../21_style_9rng.md), worked as a grilling. Six items, presented at once by the draft and corrected by the author — *"we are settling one question at a time"* — then taken in order.

**The largest item: a misreading of [chapter 01](../01_the-five-kinds_cjx4.md), and where it actually came from.**
The draft had written a paragraph noting that two differently-formatted Go files do not compile to identical binaries, because Go's line table records source positions, and offering that as the reason 02's test is about behaviour rather than about what the machine can see.

The author's verdict: *"your identical binaries in go point is useless hair splitting, not worthy of mention and rebuttal."*
Correct. The paragraph defends the test against a fact that was never about the test — the compiler recording a line number is not the compiler acting on a formatting choice — and the draft had gone and measured artifacts because it read *ignores* as *produces an identical artifact*.

The author asked whether the confusion warranted clarifying [chapter 01](../01_the-five-kinds_cjx4.md) as well.
Checking that produced a better answer than either party had. **[Chapter 01](../01_the-five-kinds_cjx4.md)'s test already carries the distinction:** question 4 reads *"while the program behaves the same either way"*, which excludes an ordinary code change such as `i++` against `i--`. No paragraph was needed.

**But the check found the actual defect, one question further down.**
Question 5 read *"Can neither of them tell which way you chose?"*
A compiler **can** tell — it parses the file and records positions — and that technically-true answer is the loose thread the draft pulled. It now reads *"Does neither of them act on the choice?"*, matching question 4's phrasing one line above.
One word, and it closes the gap rather than papering over it. The definition paragraph keeps the author's *ignores a Style*, where the contrast with *acts on an Idiom* makes the meaning plain.

**The claim was being hedged against an objection it should have accepted.**
The draft's opening said *"The claim is not that Style does not matter. Consistency is worth having."*
The author: *"I think the claim is more or less exactly that, you are confusing the consistency of style with the choice of style."*
Right, and the hedge was defending against *so style doesn't matter?* by pointing at consistency, which is a different question. The chapter now opens on the claim and one sentence of orientation.

**The joker-developer case, which is the author's and is the chapter's second boundary.**
The author supplied a rewrite of the demonstration function using `G`, `p`, `z` and `y`, noted that it compiles, and asked how that does not invalidate the claim — *"in a consistent way."*

Verified: it compiles, `go vet` is silent, `gofmt` approves it, and it prints `1745`. Every machine test in the chapter says it is the same program.

The resolution: `Total` and `Sum` are two names for one function and nothing separates them, which is the Style question and has no answer. `G` is not a third name — it names nothing, so it is not an alternative to the others but the choice not to name the thing. And the question has evidence behind it: show a colleague `func Total(amounts []int) int` and ask what it returns and they answer; show them `func G(p []int) int` and they cannot.

**That exposed a defect in the boundary section's rule.**
It read *"check that both options produce the same program"* — and `G` **does** produce the same program, so the rule did not cover the case being added under it.
Generalised to: **check that both options do the job you are choosing between two ways of doing.** For the tuple that job is passing a sequence of parameters and the driver says which option fails; for the name it is saying what the thing is and a reader says.

The author also corrected the draft's framing of the case. The draft wrote that `G` *is* Style by the definition *and* indefensible, which sets up a contradiction the section then has to argue its way out of. The author's version — *looks like a Style choice by the definition, but it is not* — dissolves it and matches the tuple, where one of two apparent options also turned out not to exist.

**The closing line, settled over three rounds.**
Draft: *where being right does not matter, being seen to have chosen still does.*
Author: *not possible* rather than *does not matter*, since correctness is unavailable rather than unimportant. Correct, and the draft's version said the weaker thing.
The draft objected that *the reasons for the choice matter* could be read as *some reasons are better than others*, reopening the correctness the first half closes.
The author's answer supplied the fix rather than dodging it — **recording** the reasons is what matters, not the reasons — and made the case for keeping the harder sentence: *"the leading 'this chapter's oddity' signals the mind bending statement that comes… I would rather keep the mind-bending and more correct one then softening it for fear of misunderstanding."*

Settled: *where being right about the choice is unavailable, but recording the reasons for it still matters.*
Which, as the author noted, is also why a decision log for Style choices is worth keeping.

**One direct edit accepted without change.**
The author deleted the draft's note that Black and Prettier were not installed. The chapter claims no output from either, so the caveat was defensive noise.

## 96. Decision 24 reversed: there is an AI chapter, and grilling moves into it

**Context.**
Decision 24, on 2026-08-12, rejected a chapter on AI-assisted development and distributed the material instead.
The author proposed the chapter then; the draft argued against it and won on this test:

> The draft argued for a chapter on the grounds that it needs one organizing mechanism the way chapter 15 [now 14] has one; testing that honestly, *the derivation never happened* explains the Forces finding and not the monoculture, confidence, or volume findings. **There is no single mechanism, so there is no chapter.**

**Why it is reversed.**
The author proposed it again while [chapter 22](../22_never-written-down_at4r.md) was being planned, and supplied a mechanism decision 24 never tested.
Decision 24 examined *the derivation never happened*. The author's is **the decisions were never stated, and what would have to survive for them to be recovered does not exist.**

The second half is new to the book. Nothing in decision 24, in the pending document, or in [chapter 18](../18_force-map-method_r37x.md) says anything about irreversibility. The nearest thing is 19's line that *"the reasoning is the perishable half"*, which is about one interview's output rather than a system passing a point of no return.

The author's own framing, recorded because it is sharper than the draft's summary of it:

> AI is like a giant force that skewed most of the topics we talked in this book… the ideas explained in this book were not eliminated, they [are] more important than before… you don't know the trade-offs that were made, you don't know the forces that were considered… the entropy takes over quickly and you have nothing to tame it.

And the line that decided the chapter's shape:

> it's a black box for the AI as well

**Decision 24's dating objection stands and is answered rather than dismissed.**
It held that *"a chapter titled for a technology is a dated object by construction."* The chapter is titled for its mechanism — *What Was Never Written Down* — and its claim is true of any unstated decision, with these tools as the force that makes it bite.

**Grilling moves from [chapter 18](../18_force-map-method_r37x.md) into it.**
Decision 24 placed grilling in 19 because *"grilling is a method rather than a way of reading."* That was a choice between 19 and [chapter 22](../22_never-written-down_at4r.md) as then planned, which was six ways of reading. It was never a choice against a chapter about method under these tools, because none was proposed.

The draft's own argument for moving it is decision 24's, applied one level down: a sixty-one-line section about these tools inside the method chapter dates the method chapter. Moving it quarantines the dating where it belongs and leaves 19 as a method that survives model generations.

**A verification task the author called for, and it changed the claim.**

The claim under discussion was *a decision nobody stated can be recovered while the context that produced it is alive*. The author stopped the drafting to ask whether that is true when the author of the decision is a tool — whether such tools make decisions with reasons in any sense that permits recovery, or whether asking produces invention.

That is a claim about mechanism, so it was checked rather than reasoned out.

**What the sources support.** Turpin et al., *Language Models Don't Always Say What They Think* (NeurIPS 2023): chain-of-thought explanations *"can systematically misrepresent the true reason for a model's prediction"* — shown by biasing inputs, with models rationalising the biased answer and failing to mention what moved them.

**What is contested, and the draft would not have known without looking.** A later paper argues the standard metric *"confuses unfaithfulness with incompleteness, the lossy compression needed to turn distributed transformer computation into a linear natural language narrative"*, that non-verbalised influences still act causally through the reasoning, and that larger inference budgets improve verbalisation.

**What is not established.** Nothing studies our actual case — a coding tool asked afterwards why it made a design choice in code it wrote. The chapter will not extrapolate from benchmark reasoning traces to that.

**The correction this produced.**
The author read the finding and drew the strong conclusion: *there is simply nothing to recover, the decisions never existed.*
The draft agreed with the practical consequence and objected to the metaphysics, because the counter-paper's result is that non-verbalised influences **do** act causally — something determined this line rather than another one. What never existed is not the determination but the articulation.

Settled formulation, the author's, accepted:

> There was a computation that produced this line rather than another one, and there was never a sentence saying why. Asking afterwards does not retrieve one. It produces one.

**And the architectural fact the chapter turns on**, which is not research and not contested: a forward pass discards its activations; the key-value cache is derived from tokens and is a recomputation shortcut rather than a record; every persistence mechanism these tools have stores **text**. So there is never a replay. What persists is always tokens.

Which gives three cases rather than the two the author posed, and the middle one is the chapter's contribution: same session with the reasoning written out is genuine retrieval of what was *said*; same session with nothing written is a fresh computation on overlapping input, producing a correlated answer that is not a recollection; a new session has only the artifact. **From the outside all three are fluent and indistinguishable**, which is why *ask it while the context is fresh* feels reliable.

**A consequence for grilling, which improves it.**
If there are no reasons to extract, grilling is not an interview that gets reasons out of a tool. It is a procedure that forces the decision to happen in the open, where a person makes it, and the record is trustworthy for that reason rather than because anything introspected. [Chapter 18](../18_force-map-method_r37x.md) already contains the evidence — *"note who supplied them. In both cases the human"* — without drawing the conclusion.

This also answers the author's question of whether grilling with every recommendation accepted differs from not grilling at all. It does, and not marginally: the decision was made by a person and written down either way.

**The claim, settled.**

> **A decision nobody stated can be recovered only while someone still remembers it — and when the author was a tool that remembers nothing between sessions, that window was never open.**

**The title.**
The draft proposed *Decisions That Leave No Mark* and the author rejected it — it *"frames the guilt on the decisions"*, which is the personification the register rules exclude, and the draft should have caught that before offering it.
The author preferred *Decisions Nobody Stated*; the draft raised that it is [chapter 02](../02_forces_f4m5.md)'s construction — *Forces: the inputs nobody names* — and the same shape of claim.
Settled on **What Was Never Written Down**, which names the absence of a record rather than the absence of a decision, and is the distinction the verification established.

**The folk remedy lands here after all**, in a paragraph rather than a section. [Chapter 14](../14_principle-loses-scope_b86v.md) forward-references *"what [chapter 22](../22_never-written-down_at4r.md) calls a folk remedy"*, and the term's purest instance is a corpus default: advice applied far outside the context it was made for, where nobody rebuilds the scope because nobody knows a scope existed. The author noted the monoculture point already appears in grilling's limit passage, so the term is defined once early and the limit passage then *uses* it — which shortens the transplanted section and stops the observation appearing twice.

## 97. How [chapter 22](../22_never-written-down_at4r.md) lost its planned identity, and a chapter outlined against a chapter nobody had read

**Context.**
Decision 96 records the second half of the [chapter 22](../22_never-written-down_at4r.md) grilling — the reversal of decision 24, the source verification, the claim and the title. It was written mid-session and stopped there. This entry records the first half, and one process failure that is the point of writing it down at all.

**Sequencing: 23 before 01.**
With only [chapters 01](../01_the-five-kinds_cjx4.md) and 23 unwritten, the draft recommended 01 — it is the last item in the launch set, and an opener written now describes twenty-one finished chapters rather than a plan.

The author overruled it:

> stop, chapter 01 [the opener, never written — see decision 103] generation. Let's do the final chapter now, then formulating 01 will be easier.

Which is right for a reason the draft had not weighed: [chapter 01](../01_the-five-kinds_cjx4.md) promises what the book delivers, and the delivery was not finished. An opener written before the closing chapter exists would describe a method whose last chapter had not been settled.

**[Chapter 18](../18_force-map-method_r37x.md) had absorbed [chapter 22](../22_never-written-down_at4r.md)'s planned job, and nobody had noticed.**

The TOC gave 23 six receiving cases, four questions, the folk remedy, the book's own conditions, and *"the final answer to 'is this load-bearing' as a repeatable procedure rather than a judgement call."*

A survey found:

- **[Chapter 18](../18_force-map-method_r37x.md) already claims to be the procedure.** Its second line: *"Everything before this chapter was diagnosis. This is the procedure."*
- **23's planned boundary was already spent.** The TOC assigned it *"when you don't have time to analyse and must simply pick the conventional answer"*; 19's boundary section opens with `### The conventional answer is good enough` and works it through blast radius.
- **Four of the six receiving cases are worked elsewhere** — a review comment in 14, a colleague's strong opinion in 20, a book in 16, 17 and 18, a blog post in 15. Only *your own past decisions* and *generated code* were left.

None of this was a defect in any chapter. [Chapter 18](../18_force-map-method_r37x.md) grew into the space while 23's entry sat unchanged from before 19 existed.

**And then the failure that matters.**

On that survey the draft proposed a claim for 23 built on reconstruction — *advice reaches you as a conclusion with its situation removed, so using it means rebuilding that situation* — and drew a full outline against it.

The author:

> I'm genuinely struggling to figure out the difference between the claims of chapter 19 [now 18] and this outline's main claims. I'm guessing that you didn't read the chapter 19, read the chapter 19 from start to finish and then reassess the situation.

They were right. The draft had worked from 19's claim sentence and two greps. Reading it end to end showed that **every item in the outline was already in 19**: the reconstruction move at its *How to notice a principle whose forces are absent*; the four questions collapsed into its *what would have to be true for this to be unnecessary*, pointed at incoming advice in its closing line; the decision log in full; and both of the book's own conditions the outline was going to introduce, including the thirty-eight entries for five thousand lines.

The proposed claim was [chapter 18](../18_force-map-method_r37x.md)'s claim, pointed slightly differently, and the author detected it from the outline alone.

**This is the same failure as the FlowCore decision 18 error earlier in the same session** — asserting the contents of a document from memory and a keyword search rather than reading it — committed within a few hours of recording that one. `CLAUDE.md` states the rule for primary sources; the finding here is that **it applies to this book's own chapters too**, which is not obvious, because the draft believes it knows what they contain.

**The options that followed**, once the space was actually mapped: a narrow chapter of what 19 leaves; cutting 23 entirely and letting 22 close the book; or reconceiving it around emitting advice rather than receiving it, which the book has never covered. The draft leaned toward the third. The author proposed the AI chapter instead, which decision 96 takes up.

**The demonstration, and why the FlowCore decision reappears.**
[Chapter 18](../18_force-map-method_r37x.md) already uses FlowCore's decision 12 for its worked force map, so the draft flagged reusing it as a second appearance and offered two alternatives — a sorted map iteration and a schema constraint.

The author took decision 12 and supplied the differentiation:

> I read chapter 19's [now 18] section again, there the situation is very briefly described and then the decision log is dissected. Here the example would probably look very different: code samples, explanations of the decisions and the reasons, problematic change...

Which is the ledger's requirement for FlowCore appearances met exactly: 19 shows the decision being **mapped**, 23 shows it being **lost**, and the second is in code where none of the first is visible.

**The rewrite material, kept out of the claim and kept in the chapter.**
The author had simplified the claim by dropping *the only route back is a rewrite*, then returned to it:

> I dropped the "only route back" to simplify the claim but I think that mini-story or detail of unrecoverable decisions forcing a whole rewrite of a system can still be used inside the chapter.

It became the section that scales one lost decision to a system, with the author's own comparison as its safeguard — this happens without these tools too, so what changed is the rate rather than the failure. That framing is what keeps the passage a force reading rather than a verdict, which decision 24 requires and this chapter is the likeliest place in the book to breach.

The draft flagged one register risk in advance: *point of no return*, *entropy takes over*, *futile* are the atmosphere the register rules exclude, and the mechanism — each guess adding a constraint nobody recorded either — has to carry it instead.

**One duplication the author caught before it was written.**
The draft planned to define the folk remedy by way of corpus defaults. The author pointed out that the monoculture observation already appears in grilling's limit passage, which was arriving in the same chapter.

The fix improved the transplanted text rather than merely avoiding a repeat: the term is defined once, early, and the limit passage now **uses** it — *"grilling is weakest against folk remedies, because a folk remedy does not present itself as a branch point"* — where it previously rebuilt the observation longhand because the term did not exist where that passage was written.

## 98. Say "AI coding agent", not "generator" or "the tool"

**Context.**
[Chapter 22](../22_never-written-down_at4r.md) and the AI material in [chapters 18](../18_force-map-method_r37x.md), 03 and the ledger avoided naming the technology, using *generator*, *the tool*, *a tool in the loop* and *something with one training distribution* instead.

**The author's correction.**

> Inventing terms that are generic to denote a known technology doesn't make the chapters technology independent, it only obscures the meaning and discoverability. Those sections talk about AI tools, the dependency is there and accepted, there is no need to hide that.

**Where the draft's reasoning went wrong.**
It was applying decision 24's argument — *"a chapter titled for a technology is a dated object by construction"* — which was about **titling a chapter**, to vocabulary inside chapters, where it does not hold. Avoiding the word does not remove the dependency; it removes the reader's ability to look the subject up.

`CLAUDE.md` already rules against it directly: *"Plain words wherever they work, but name the real terms… because the reader needs the vocabulary to find the literature."* *Generator* fails that outright — nobody searches for it.

**Decision, the author's terms.**
Three, used deliberately rather than interchangeably:

- **AI coding agent** — the actor. The default noun.
- **agentic coding tool** — the variant, where repetition would be worse.
- **model** — kept only where the subject really is the underlying model: the faithfulness research, and the training corpus.

That third distinction is a gain rather than a compromise. [Chapter 22](../22_never-written-down_at4r.md) cites Turpin et al. and Zaman and Srivastava, whose subject is models and not agents, and the sentence *"whether a model's stated reasoning reflects its computation"* is correct as written. Blanket-replacing would have made it wrong.

**The survey, which mattered more than the replacements.**
Twenty-three occurrences of *generat\** across the chapters, and **almost all of them were unrelated** — invoice generation, a compiler's code generator in [chapter 19](../19_six-profiles_dnkz.md), JSON generated rather than written, an idempotency key generated by the client, `regenerate`. One was a verbatim quotation from the grilling transcript, *"Should ids be generated by the application or by the database?"*, which must not change because it is quoted.

A path-wide replacement would have corrupted all of them. This is the second time in one session a sweep needed checking first — the other was `pending/` appearing in [chapter 09](../09_what-a-pattern-is-for_3xzc.md) as a hypothetical source folder.

**What changed:** seven sites in [chapter 22](../22_never-written-down_at4r.md), one in [chapter 18](../18_force-map-method_r37x.md), two ledger rows, one line in `00_toc.md`'s owed table, and two headings in `docs/pending-tasks/ai-material.md` so the material lands in [chapters 01](../01_the-five-kinds_cjx4.md) and 03 with the right vocabulary.

**`docs/DECISIONS.md` is left alone**, on the same reasoning as decision 93: it records what was decided in the language used at the time, and decision 24 is titled for the material it describes.

## 99. [Chapter 22](../22_never-written-down_at4r.md) review 01: a cost bullet that was arguing against the chapter

**Context.**
First review of [chapter 22](../22_never-written-down_at4r.md), worked as a grilling. Two commits from the author, nine items.

This entry exists because the author asked for it, for the second time in one session, after decision 88 added the rule requiring it. Recorded here rather than treated as a note: **the rule has now failed twice on the session that introduced it**, which is evidence about where it needs to fire — at the end of a review pass, not only at the end of a drafting session.

**The folk remedy had been over-built, against what was already agreed.**
The author's tag: *"this section should simply be deleted, adds not much to the chapter, mostly distracts from the natural flow."*

Decision 96 records the agreement as *"in a paragraph rather than a section"*, and the draft wrote a five-paragraph `###` section. The reaction was to the thing the draft built past the agreement.

The draft put the constraint in front of the author before acting: deleting it outright dangles [chapter 14](../14_principle-loses-scope_b86v.md), which ends on *"you get what [chapter 22](../22_never-written-down_at4r.md) calls a folk remedy"*, plus a ledger row and a TOC line. Compressed instead to one paragraph inside grilling's limit passage, where the term is used, with the term bolded so 15's promise is discharged and the reference stays findable. **The heading going is most of what fixed the flow** — a `###` between the recovery argument and grilling reads as a new subject arriving.

The author asked for a short example. They proposed *depend on interfaces* or DRY applied to a one-off script; the draft recommended [chapter 17](../17_abstraction-as-insurance_4jk6.md)'s own phrasing, *depend on abstractions, not concretions*, because 18 is the worked case and can carry it in a clause, and because it is exactly what an AI coding agent emits unasked — which is what makes it belong in the limit passage rather than beside it.

**A cost bullet that was arguing against the chapter.**
The author flagged *"It requires you to hold opinions"* as reversing an earlier point. It was: the chapter said both *"grilling does not produce better answers, it produces answers somebody can disagree with"* and, forty lines later, that a record of accepted recommendations is *"worse than none, because it looks like evidence."*

The draft offered two ways out — delete, or fix the direction so the record is genuine but thin. **The author supplied a third that is better than either**, and it is recorded in their words because the draft would not have reached it:

> the real issue is making choices without fully grasping the options and what they mean, without understanding the trade-offs. Even if you went with all of the recommended options — by the way this happens 90% of the time in my experience — if you read every decision and option carefully and put an effort to make a conscious decision, something intangible but very real was gained. The expanded versions of those decisions and reasons are now in you as a person.

**This is not a cost. It is the claim's own first half, which the chapter had not noticed it was resting on.** The claim says a decision can be recovered *while someone still remembers it*. Grilling produces two artifacts — the log, and a person who now holds the trade-off — and the chapter was counting only the first.

**One adjustment to the author's point, flagged rather than made silently.** They wrote that the agent *"will never be able to make"* those connections. That is a capability claim, and `docs/pending-tasks/ai-material.md` is explicit that capability claims do not survive while structural ones do. Written structurally instead: it keeps nothing between sessions, so the connection has to live in a person or a document.

**The force-reading paragraph, deleted.**
The author found it cynical — showing at length how badly this goes and then adding that the book takes no position reads as washing hands.

The draft checked whether deleting it breached decision 24, which records the author's own correction that *"usage is a fact, and the book does not take positions on facts."* It does not. Decision 24 requires the book not to take a position; it does not require a paragraph saying so, and the paragraph before it already does the work by observing that this is the ordinary history of software written entirely by people and that only the rate changed. The disclaimer added a defensive tone and nothing else.

**Two places the draft disagreed.**

*Comments that say what the code does.* The author objected that sometimes a comment restating bad code is exactly what is needed and there is no time to refactor. Correct, and the bullet was too absolute. Narrowed rather than dropped: a comment restating dense code earns its place, and **the signal is when every comment in a file is of that kind**, because the reason is then nowhere.

*The closing question.* The author preferred *who can tell us why it was done?* over *what would tell us*. The draft kept *what*, because the three answers immediately below it are a person, a document, and inference — *who* covers only the first. The dead clause the author actually objected to, *if this turns out to be wrong*, was cut, and the paragraph now says why it is *what*.

**The ending, which is the author's.**
Their expansion material became the chapter's last three paragraphs, close to as supplied: reading is rarely enough on its own, you ask the people who might know and they half-remember different things, and what you hold at the end is not an answer but a position — fixing Y changes Z, some customers depend on Z, leaving Y another month costs a different customer. Nobody is being unreasonable and no fact available settles it.

The draft added one connective clause, because the expansion assumes colleagues exist to ask and the chapter's own case is worse: where the code came from an agent there is nobody in that position at all.

**Direct edits accepted without change:** *recovery window* for *window* in the claim, naming the agentic coding tool as what the negative requests are addressed to, and *None of this is new* for *None of which is new*. The author also deleted a sentence the draft had itself flagged as possible self-aware decoration — *"which is a sentence worth resisting the urge to soften"* — and was right to.

## 100. The faithfulness passage was undermining the remedy that follows it

**Context.**
The author proposed applying decision 26's diagnosis to [chapter 22](../22_never-written-down_at4r.md)'s paragraph on chain-of-thought faithfulness, and reported an itch they could not place:

> This reads like we value extracting those sentences from the coding agent "live", while it branches but then we say we have no idea if those sentences are of value, that's still debated. I know that's not the point of the passage but no matter how I try to read it it sounds like that.

**Two faults, and the second is the one they were feeling.**

**Register, exactly as decision 26 and the *source's register* rule describe it.** The paragraph carried `chain-of-thought` unglossed and used once; `unfaithfulness` and `incompleteness` used once each, which the rule calls *"a definition wearing a name"*; a fifteen-word quotation — *"the lossy compression needed to turn distributed transformer computation into a linear natural language narrative"* — which is [chapter 16](../16_tdd-and-mocks_u8eu.md)'s failure verbatim; and two named researchers with two quotes, for an argument the chapter then says it does not need. The rule's own symptom line fits: *"a paragraph a reader has to decode rather than follow, in a chapter that was going fine until the citation arrived."*

**Placement, which the author felt and the draft had not seen.** The passage sits immediately before the grilling section. A reader meets *whether a model's self-explanations mean anything is contested*, then meets a remedy built on interviewing a model, with nothing between them saying those are different questions. So the caveat reads as discounting the thing the chapter is about to recommend.

They **are** different questions, and decision 96 records the distinction — the record grilling leaves is trustworthy *"for that reason rather than because anything introspected"*. It appeared only inside the grilling section, eighty lines later, which is after the wrong impression has formed.

**Decision.**
The passage is rewritten in the book's voice, with the paper titles in `## Sources` carrying the searchable terms so the body does not have to. A paragraph is added drawing the distinction where the reader needs it: a model accounting for its own output afterwards is what the research contests; a decision put to a person before any code is written, and settled by facts that person supplied, is not.

**Authorship.**
The rewrite is the draft's; the diagnosis of *what* was wrong is the author's, and the final wording is theirs — they took the draft's version and revised it again, adding *without deliberate effort* to the behaviour-survives paragraph, which sharpens the contrast, since decisions need effort to preserve and behaviour does not.

**Three corrections to that revision, made rather than asked about.**
Their first pass changed *this line* to *this line of reasoning*, which moves the referent from the line of code to the model's reasoning and is not the chapter's subject; the ambiguity they spotted was real, so it became *this line of code*.
A bold span covered a subject clause but stopped before its predicate, so scanning it gave a noun phrase rather than a claim; the emphasis moved to the assertion it was pointing at.
And the closing paragraph opened *"Finally, worth separating out another thing does survive"*, which does not parse.

## 101. [Chapter 22](../22_never-written-down_at4r.md) reopened: granularity as grilling's second limit, and what a record buys beyond recovery

**Context.**
The author brought a stream of new material after 23 reached draft, and asked directly whether it was worth using or should be abandoned. Three ideas survived the assessment, one was reframed because it contradicted the book, and two were dropped.

**Taken: granularity is grilling's second limit.**
The chapter had one limit stated — the interview surfaces only what the corpus treats as a decision. The author's is different and easier to walk into: **it surfaces only decisions at the granularity you asked at.**

> You can ask AI to generate the app in one go… it will give you something that looks good and works. But even if you used grilling, you compacted the process and as a result you skipped many granular decisions and trade-offs that could only be surfaced with the phases.

And the reason it is missable, which is the part worth having: *"This is obvious with traditional dev, but easy to miss with AI because of the illusion of speed."* Nobody skips phases on a project measured in months; an afternoon does not feel like it needs a plan.

**This is evidenced rather than proposed.** FlowCore was built in slices — the decision log says *"this slice"* twenty-seven times, with real scoping such as *"full definition-side CRUD this slice"* — and the boundary is written into its standing instructions rather than left to intention:

```text
In scope: configure workflow, start workflow, get current step, complete step.
Out of scope: AI review steps, synchronization, failure handling, scale work.
Do not build ahead into these.
```

Checked firsthand in `~/s/flowcore/CLAUDE.md` rather than taken from `ai-material.md`'s quotation of it.

**Reframed, because as stated it contradicted the book.**
The author proposed reusing decisions as instructions for other projects. A decision's reason is a fact about your situation, so carrying the conclusion across is precisely how a folk remedy is made — a term this chapter defines.

The version that survives is better and is the book's own thesis pointed at its own artifact: **an entry is reusable exactly to the extent that it records why rather than what.** *Full-word identifiers everywhere* transfers nothing to a codebase with different readers; *abbreviations must be decoded rather than read, and the decoding does not get cheaper with familiarity* can be checked against those readers and kept or dropped on the evidence. A conclusion does not travel; a conclusion with its condition attached does.

**Replay: evidenced, but not with the evidence the author offered.**
Asked whether they had actually replayed a decision, the author pointed at this session — decision 26, recorded about [chapter 07](../07_scale_637f.md), invoked against a paragraph in [chapter 22](../22_never-written-down_at4r.md).

That is a genuine instance, and a better one than a clean replay because it was **partial**: one of decision 26's three faults transferred, and the new context produced a finding decision 26 never contained. Which isolates the mechanism — decision 26 travelled because it recorded *written for someone who already knew the material* rather than *[chapter 07](../07_scale_637f.md) rewritten*.

**The anecdote cannot be used, on two existing constraints.** Decision 47 takes a general rule from the author's own instruction: *"the drafting history belongs in the decision log, not in the chapter."* And `ai-material.md`: *"readers will discount a book that proves its method works by citing itself."*

So the mechanism is stated and FlowCore supplies the evidence — its identifier rule ends in a pointer, *"Reasoning and worked examples: `docs/decisions.md`, decision 18"*, and the same file makes the log authoritative where the two disagree, so an unclear case is decided by returning to the reasoning rather than guessing at the rule's edge.

**Dropped.**
*Meta-source code* as a term, on the rule against a metaphor promoted to vocabulary. And this session as the worked example, per decision 47.

**A placement error the author caught.**
The draft proposed putting replay in [chapter 18](../18_force-map-method_r37x.md), reasoning that 19 owns the decision log. That is ownership by association rather than an argument: 19's claim is about the order of checking, and its interest in the log is that it records forced against chosen. Reuse serves no part of it.

The argument that settles it: [chapter 18](../18_force-map-method_r37x.md) lost sixty-one lines of AI material in decision 96, on the grounds that a section about these tools dates the method chapter. Handing a log back to an agent is an AI-shaped practice and would date the same way, so putting replay there would re-import the problem decision 96 removed.

**Consequence.**
[Chapter 22](../22_never-written-down_at4r.md) runs 288 lines, up from 264. Two ledger rows added and one renamed, since grilling now has a first and a second limit rather than *the* limit.

## 102. Naming the two artifacts, and a term the book had never settled

**Context.**
The author's review of the reopened [chapter 22](../22_never-written-down_at4r.md) raised four tags, three of which were one fault: the passage described its artifacts abstractly — *that promotion*, *the same file*, *the log*, *a pointer*, *standing instructions* — where a reader needs to know which document holds what.

> is the rule an entry on CLAUDE.md? File => Claude.md ? log => decision.md? pointer is confusing => reference to a decision log

That is decision 26's fault one again, in a passage written for somebody who already knew the layout.

**A term the book had never settled, delegated to the draft.**
A survey found the asymmetry. **Decision log** is settled and consistent — [chapters 02](../02_forces_f4m5.md), 05, 16, 17, 19 and 22 all use it, with `docs/decisions.md` named where it helps. **The instructions file has no term at all**: `CLAUDE.md` is named in no chapter, and *standing instructions* appears only in the two sentences the author tagged.

The author left the choice to the draft. Settled the same way decision 98 settled *AI coding agent* against *model*: **the generic thing carries the argument, the concrete file is named once for discoverability.** `CLAUDE.md` alone dates and is product-specific; a generic phrase alone is what the author had just flagged as unclear. The chapter now says the instructions file is the set of rules an agent is given at the start of every session, that FlowCore's is `CLAUDE.md`, and that tools differ on the filename rather than on the idea.

**One vocabulary collision fixed while there.**
The section used *slices* and *phases* for the same thing — FlowCore's word and the author's. Unified on *phases*, with one clause noting FlowCore calls them slices, so the quoted log lines still parse.

**The author's rewrite of the closing paragraph, corrected.**
Their version — *"**Slices are elusive with AI assisted development** The whole implementation can arrive in an afternoon… The discipline to clarify the phases before any implementation is needed to prevent the loosy compression of decisions"* — carried a bold lead-in with no terminal punctuation, an unhyphenated *AI assisted*, *loosy* for *lossy*, and a passive construction that buries its own subject.

It also reached for **compression**, which the chapter had already spent eighty lines earlier on a different subject — an explanation compressing a computation. Rewritten to say what actually happens instead: settling the phases first is what keeps the decisions far enough apart to be asked about one at a time.

**A cut of the draft's that the author was right to make.**
They removed two sentences ending *"never surfaced is the same as never written down"*, noting they repeated the earlier section. They did — the claim had already been made twice by that point, and the paragraph was restating it a third time to land a rhythm rather than a fact.

## 103. There is no [chapter 01](../01_the-five-kinds_cjx4.md): the README is the introduction, and 02–23 become 01–22

**Date.** 2026-08-25

**Context.**
With twenty-two chapters at draft, only [chapter 01](../01_the-five-kinds_cjx4.md) — *Why good advice goes wrong* — remained unwritten. Three attempts to give it a claim each landed on ground another chapter already owned.

- The TOC's plan, *"advice arrives without its conditions attached"*, is [chapter 14](../14_principle-loses-scope_b86v.md)'s mechanism. That chapter opens by reconciling the two words: *"Scope is the same boundary seen from the other side."*
- Its planned demonstration, *"two teams receive the same advice and get opposite outcomes"*, is [chapter 18](../18_force-map-method_r37x.md)'s section `The same advice, four verdicts`.
- The draft's own proposal — *advice that is true can still be wrong for you, and nothing in the advice tells you which* — turned out to be the README's premise, which is `CLAUDE.md`'s thesis almost word for word.

**The test this book already applies.**
When a chapter cannot be given a claim that is not already somebody else's, it has no job. Decision 24 cut the AI chapter on that basis — *"there is no single mechanism, so there is no chapter"* — and decision 83 cut the database chapter outright. This is the third application, not a new rule.

**The author's proposal, which is what the evidence pointed at anyway.**

> README.md is actually what we called "first chapter" in this session… That's both the elevator pitch and converter. If the book does ever get published README.md could be foreword or introduction. What do we write on the first chapter then? Nothing, first chapter already exists, it's the current chapter 02 [now chapter 01].

**Decision.**
No [chapter 01](../01_the-five-kinds_cjx4.md) is written. The README becomes the book's introduction, and [chapters 01](../01_the-five-kinds_cjx4.md) through 23 renumber to 01 through 22. The book is twenty-two chapters.

**Why [chapter 01](../01_the-five-kinds_cjx4.md) works as the opener with no repair.**
It opens cold — nothing in it refers to a predecessor. Its first heading is `## The book's model` rather than `## The claim`, because decision 43 established that it states a premise rather than a claim, and it says so itself: *"Both are assumed by the rest of the book rather than proved by this one."* That is an oddity in a second chapter and exactly right in a first.

**What was checked before the sweep.**
Prior renumberings in this repo corrupted unrelated numbers, so the hazards were enumerated first: *"16 of 23 patterns"* in [chapter 12](../12_missing-language-features_esqm.md), the TOC and the ledger is the Gang of Four count; *"a team of 20"* is a team size; and *Clean Architecture*'s chapter 30 is somebody else's book. None matches a `chapter NN` pattern, and none was touched.

**The decision log is renumbered, reversing the draft's first position.**
The draft proposed leaving `docs/DECISIONS.md` alone, carrying over the reasoning from decision 93, where `docs/pending/` was left in place because decision 78 is *titled* for that path — there, the path was part of what was decided.

The author asked why, and the analogy does not hold. **A chapter number in the log is an address, not part of what was decided.** Leaving it would be worse than stale: decision 26 is titled *"[Chapter 07](../07_scale_637f.md) rewritten"*, and after the shift a reader looking up [chapter 07](../07_scale_637f.md) would land on a different chapter that the entry is not about — a wrong pointer rather than a dead one. The README says the log exists *"so that claim can be checked rather than taken on trust"*, and four hundred silently-off-by-one pointers is a tax on precisely that.

So the log's own prose and entry titles are renumbered. **The eight quoted lines containing a chapter number are left exactly as spoken**, with a bracketed `[now NN]` gloss — the conventional signal for an editorial insertion — so nobody's words are altered and no reader is misdirected. Six of the eight are the author's.

**Entries above this one were written before the shift.** Their prose has been renumbered to match the current book; their quotations have not.

## 104. The README gets a default entry point, and the disclosure stays put

**Context.**
First review of the restructured README. Three tags.

**[Chapter 01](../01_the-five-kinds_cjx4.md) gets its own hook, and the jump-ins get demoted.**
The author's point: with the README now the introduction, its *Start here* block sent readers to [chapters 05](../05_time_mdbn.md), 06, 09 and 02 and skipped the model entirely.

> 01 is the default start, those are jumping, skipping suggestions if 01 doesn't sound "sexy".

So *Start here* now carries one hook, for [chapter 01](../01_the-five-kinds_cjx4.md), and the four existing ones move under **Or start anywhere** — a title the author invited a suggestion for.

**The hook, written to decision 51's rule.** It comes from the chapter's own claim at full strength — *the kind determines how much authority it has, not the confidence of the person saying it* — and is cashable, because the chapter carries both code samples and the line *"The C# version works… It will still be sent back."*

> **The same wiring code is unremarkable in Go and gets sent back in review in C#.**
> It compiles, it runs, it serves requests correctly, it is thread-safe — and neither version is more correct than the other.
> Some of the rules you follow are like that and some are not, and they arrive in the same voice.

It deliberately does not reuse the acyclic-versus-repository pair, which is the premise section's example two screens further down.

**A question answered rather than a change made.**
The author asked whether *How this book was written* had been slated to leave the README. It had not. The decision was to **reorder** it — the draft asked whether it should sit after the premise and the spine rather than between the hooks and the premise, so a reader meets the idea before judging the method, and the author answered *"move it"*.

It stays in the README on a stronger ground than habit: `CLAUDE.md` treats the disclosure as part of the book's claim about itself — *"The README states this openly and `docs/DECISIONS.md` is the evidence"* — so relocating it to `docs/ABOUT.md` would bury the thing the book is most exposed on, in the document a visitor is least likely to open.

## 105. The README's opening block, and naming the links as chapters

**Context.**
Second review of the README. The author moved the status line to the foot of the page, removed the `Start here` / `Or start anywhere` headings, cut the three-line tagline and the subtitle, and replaced the draft's [chapter 01](../01_the-five-kinds_cjx4.md) hook with the chapter's claim verbatim.

**Taken as given.**
The status line at the foot — the author's call on what a visitor needs first, and it is the least urgent thing on the page.

The headings removed. Their argument is *addition by subtraction*: the first entry is the suggested start and the rest are alternatives, and ordering says so without a label.

**The verbatim claim, which is more rule-compliant than the draft's version.** Decision 51 requires the hook be written *"from the chapter's own claim sentence at full strength"*; the chapter's own sentence is full strength by definition. The draft had paraphrased into the Go-versus-C# observation, which is weaker and one step removed.

> this is the verbatim claim of chapter 01 and I think the repetition is justified. This is in my opinion most beautiful and striking claim in the book.

**Two things restored, on the draft's objection.**

**The subtitle.** *Which Software Principles Hold, and Where They Stop* had survived only in `CLAUDE.md`, `docs/ABOUT.md` and this log — nowhere a reader sees. A visitor arriving from a link would get `# Load-Bearing` and a claim about five kinds, without learning what the book is called or that its subject is software. The author's reason for the cut holds for the three-line tagline, which really is the claim in weaker words, and does not hold for the book's name. Tagline stays cut; subtitle back.

**A fact line under the first hook.** The other four are claim, fact, sharpener, link — *95% of the time*, *most of what is impossible follows from it*. [Chapter 01](../01_the-five-kinds_cjx4.md)'s was claim and link, making the default entry the thinnest item on the page, and the fact is what makes a hook credible rather than merely assertive. The Go-versus-C# observation the draft had over-promoted to a claim works at its proper size as that beat.

**Naming the links as chapters, which does more than clarify.**
The author noticed that with the headings gone, nothing marks the arrow links as belonging to this book. Links are now `[Chapter 01](../01_the-five-kinds_cjx4.md) — The Five Kinds of Claim` and so on.

The side effect is the useful part: the numbers read `01, 05, 06, 09, 02`, so a reader infers *start here, or jump in* from the sequence. **That recovers exactly what removing the headings gave up**, without a label.

**Also fixed:** a stray `**` after *"how widely it is repeated"*, left over from the edit, which would have rendered as literal asterisks.

## 106. The renumbering sweep broke things nothing could see, so the checker learns to see them

**Context.**
The author asked for chapter navigation and, on the way, noticed `00_toc.md` referred to *"[chapters 01](../01_the-five-kinds_cjx4.md), 03, 15, 17, 20, 22 and 24"* — a chapter 24 that has never existed in this numbering. That opened an audit of the renumbering in decision 103, which turned out to be broken in three ways.

**What the sweep missed.**
The ledger's `cite` column entirely — 147 entries, still holding a `cite 23`. The *Pending revisits* table's chapter column and its *"next time NN is open"* cells. Around thirty bare references of the shape `cite 02; 06 owns the races`. Nine chapter lists, where only the first number moved: `[Chapters 02](../02_forces_f4m5.md), 03, 15 and 17` became `[Chapters 01](../01_the-five-kinds_cjx4.md), 03, 15 and 17`. And five possessives such as *"15's own test"*.

**What it corrupted.**
The ledger example `split(8.03, 3)` became `split(8.02, 3)` while its owner column stayed at `03`. The sweep replaced the first occurrence of the target string within each match, and in that row the first `03` is inside the float. It renamed a real example from [chapter 02](../02_forces_f4m5.md) and left untouched the thing it was meant to change.

**And the repair introduced a fault of its own.**
The fix for bare references ran over `00_toc.md`, which already held correctly-shifted `chapter NN owns` phrases, so four of them moved twice — the entity-component inversion ended up credited to *Three Kinds of True*. Caught by a semantic spot-check that printed each citation beside the title of the chapter it named, not by any pattern.

**Two faults that predate the renumbering, fixed while there.**
Three ledger rows still cited the force-map chapter for grilling after decision 96 moved grilling out of it — their owner was changed and their citation was not. And the `and 24` line was stale from an earlier renumbering.

**The author's diagnosis, and a check of the draft's instinct against it.**

> Every chapter gets a unique id in their filename… Then you do all your matchings with ids never by chapter number.

The draft's first reaction was that the slug already is a stable identifier and no new token is needed. **The history says otherwise**: five slugs have changed — `the-five-levels`, `the-scale-test`, `principle-to-movement`, `oop-vs-direction`, `six-domains` — which is more churn than the numbers have had. An opaque identifier is better founded than the draft's alternative.

**Decision: validation first, identifiers after.**
Converting roughly 840 references without a checker is how this happened. `tools/check-drift.py` gains four checks:

- **Every chapter reference in every live document resolves.** Check 5 was case-sensitive on `Ch`/`Chapter` and never looked at the ledger, which is why `cite 23` survived. The new one covers lowercase prose, `cite NN`, comma-and-`and` lists, bare `NN owns`, and `next time NN is open`, across the chapters, the TOC, the README, `CLAUDE.md`, `AGENTS.md`, the ledger, `docs/ABOUT.md` and the pending-tasks documents.
- **The ledger's columns agree**: a row owned by `NN` cites `NN`, in both its `cite NN` and its `(Ch. NN)` phrase.
- **Markdown links resolve**, and where the link text names a chapter number it must match the file it points at.
- **TOC tables agree with themselves**: the status row's number against its filename, and a revisits row's number against its own *"next time NN is open"*.

**Verified against the broken state rather than the fixed one.** Run over the pre-sweep commit, the checker reports 52 problems, including the four dead README links that were originally found by accident.

**The limit, stated because it decides whether the identifiers are still worth doing.**
Resolution cannot catch an off-by-one where the wrong target also exists. A reference that should say 04 and says 05 passes every check above. So the checker catches dangling references, dead links and internal disagreement; it does not catch a consistent, wrong shift. **That gap is exactly what matching by identifier closes**, which is the argument for doing the identifiers next rather than considering the problem solved.

## 107. Every chapter gets a permanent identifier, and the checker enforces it

**Context.**
Decision 106 built the validation and ended by arguing for this migration: resolution checks catch a dangling reference but not a consistent, wrong shift, and only matching on something stable closes that.
This entry records the migration itself.

**The identifier.**
Four characters drawn from `abcdefghjkmnpqrstuvwxyz23456789`, appended to the filename after the slug: `04_structure_agjy.md`.
The alphabet omits `0`/`o` and `1`/`l`/`i` so an identifier read aloud or retyped from a diff is unambiguous.
They are random rather than mnemonic **on purpose**: a mnemonic identifier invites being read as a description, and then it goes stale for exactly the reason the slugs did.

**The author's ruling on where identifiers may be seen.**
The draft proposed writing references as `Ch. 04 (agjy)`, with the identifier visible beside the number.

> Letting id-label frankensteins sit in the book is another thing.
> They are not even ok inside the book and the compromise is exactly this: every book reference gets the id in the link, what's visible to the reader is still pure chapter name and number, the id is on the markdown source.

So the identifier lives in the link target and nowhere else.
The reader sees *Ch. 04* and follows a link that cannot drift; the durable token is in the source, where the tooling reads it and the reader does not.
The author then allowed one exception — bare identifiers in `docs/LEDGER.md`, whose owner column is machinery rather than prose, and which is now keyed by identifier for all 22 chapters.

**What moved.**
Twenty-two files renamed, in their own commit, because a rename bundled with edits drops below git's similarity threshold and the diff becomes unreadable — which has happened three times in this repo.
Then 926 cross-references converted to links across the chapters, the TOC, the README, `CLAUDE.md`, the pending-tasks documents and the decision log, 509 of them in this file.

**The checker is now keyed to identifiers, and one new check does the actual work.**
Five checks changed shape: ledger ownership, ledger owner resolution, link resolution, link-text agreement, and the TOC status table, which now cross-checks each row's number against the identifier in the filename it names.
The one that matters is new: **a chapter reference written as plain text is an error.**
That is what makes the scheme hold rather than merely exist — without it, the next person to write `Ch. 04` reintroduces exactly the class of defect decision 106 catalogued, and nothing complains.
Quoted or backticked text is exempt, being illustration rather than reference.

**Each new check was verified by breaking something.**
Every one was confirmed to fire on a deliberate fault — a link pointed at another chapter's file, a ledger owner that names no chapter, a status row carrying the wrong identifier, a chapter file stripped of its identifier — and the file restored afterwards.
Two of the first mutations reported nothing, and in both cases the fault was in the mutation rather than in the check; finding that out took longer than assuming it would have, and assuming it would have shipped two checks that never fire.
Removing one chapter's identifier fails the run in four places at once, including every ledger row and every link that named it.

**What this does not fix.**
The identifiers make a reference survive renumbering.
They do nothing about a reference that was wrong when it was written, and no check can, since a citation to the wrong existing chapter is well-formed in every mechanical sense.
That remains a reading job.

## 108. The contents page is reduced to what can be derived, and chapters get navigation

**Context.**
Deferred twice while the identifiers landed.
The author's complaint was concrete: there is no way to move between chapters, and `00_toc.md` had become something other than a table of contents.

**The author's reframing, which replaced the draft's first question.**
The draft opened by asking whether `00_toc.md` should keep its annotated entries with a compact list added at the head.

> Prepare a proper toc for the reader, compact as a toc, has only the information a proper toc can have.
> Not this toc and that and also this…

That is a rejection of the draft's option rather than a choice between the ones offered — fusing two audiences in one file is what produced the problem, and the proposal fused three.
The author then set the test that decided everything after it:

> Does the reader need the material? Do we need the material?
> If the answers are no, we should simply discard those; there is no point maintaining a material that can be derived easily when needed and which is barely used.

**What the facts said when the test was applied.**
Where a TOC entry carried a claim it was a **verbatim copy** of the chapter's own claim sentence, and the rest summarised the chapter's mandatory boundary section.
The entries' working purpose is stated in `CLAUDE.md` — for chapters that do not exist yet they are *"the plan a drafting session reads"* — and **all twenty-two chapters are at draft**, so that purpose is spent.
Of 211 lines of entry prose, exactly one sentence was not derivable: [chapter 16](../16_tdd-and-mocks_u8eu.md)'s note that the meta-analyses are paywalled and unread, and that interface-per-class and the dependency-injection container are owned by no chapter.
It was rescued to `docs/pending-tasks/index.md`; the rest was discarded.

Two further sections failed the same test and were not part of the original question.
*Build order* and *Forward references currently outstanding* both describe a book with unwritten chapters — naming [chapter 05](../05_time_mdbn.md) as "the most owed and the most immediate" and [chapter 01](../01_the-five-kinds_cjx4.md) as easier to write "once the rest exists."
The author confirmed both go.

**Decision.**
`00_toc.md` holds a part heading and one line per chapter — number, title, link — and nothing else.
Permanent project state moves to `docs/STATUS.md`; genuinely pending work moves to `docs/pending-tasks/index.md`, which is deleted when spent like every other file in that folder.
The draft raised the lifetime clash — a status table never "lands" — and the author took the split rather than widening the folder's contract.

**Why a bare contents page is the strong option, and it is not brevity.**
Every field on it is derivable from the chapters: the number from the filename, the title from the H1, the order from both.
So `tools/check-drift.py` verifies the whole of it, and a wrong entry became a failing check instead of something a reader has to notice.
The annotated version could not be checked by anything, which is why [chapter 12](../12_missing-language-features_esqm.md)'s entry sat asserting *"Decorator is function composition"* after the chapter had measured that and found it false.
**The class of error was deleted rather than policed**, and `CLAUDE.md`'s *Keeping the TOC honest* section was rewritten to say so, its local-drift half no longer describing anything that can happen.

**Navigation, and the draft's recommendation that did not survive.**
The `**Next:**` label goes; the handoff paragraph it introduced moves up to close the argument, before `## Sources`, on the grounds that the handoff is authorial prose and Sources is apparatus.
A navigation row goes last, after the sources.

The draft recommended putting chapter titles in that row, arguing they tell a reader where they are going.
**The author chose numbers only** — `[← Ch. 19] · [Contents] · [Ch. 21 →]` — and the choice is the better one for a reason the draft had not connected: keeping the handoff paragraph means the chapter already says what comes next and why, so a title in the row restates it.
The two decisions were taken separately and only fit together in retrospect.

**Found on the way through, none of it asked about.**
[Chapter 08](../08_change_rjf9.md)'s handoff pointed at Part III with **no link at all** — the book's one dead end — and now links [chapter 09](../09_what-a-pattern-is-for_3xzc.md).
Nineteen handoffs opened with a lower-case *"[chapter NN]"*, correct after a bold label and wrong once they became the paragraph's first word.
`CLAUDE.md` described *"the full 23-chapter TOC"*; the count check ran over `00_toc.md` and `README.md` only, so it never saw it, and now covers `CLAUDE.md` and `docs/ABOUT.md` too.
The README promised a contents page "with a summary and a stated boundary for every chapter", which stopped being true in the same commit.

**Consequence.**
`tools/check-drift.py` reaches sixteen checks.
The contents page is verified line by line against the chapters, and every chapter's navigation row is regenerated from the file order, so an inserted or renumbered chapter cannot leave a row pointing anywhere wrong.
Both were confirmed by deliberately breaking them.

## 109. Four of the twenty-one handoff sentences had drifted

**Context.**
Decision 108 kept the handoff paragraphs, against the option of deleting them, on the grounds that they paraphrase a neighbour rather than copy it and so do not rot the way the contents-page entries did.
The author then asked for them to be checked, having spotted one.
There were four.

**What had drifted.**
[Chapter 01](../01_the-five-kinds_cjx4.md) promised that [chapter 02](../02_forces_f4m5.md) shows "why naming them is most of the work."
That is a claim this log records as **rejected** — *"Evaluating the Forces is most of the work of choosing well"* was ruled unquantifiable and not what the chapter demonstrates, and *the groundwork* replaced it.
Worse, it credits *naming*, which [chapter 02](../02_forces_f4m5.md) gives as the failure mode: *"Naming a Force, without evaluating it, licenses machinery."*
The handoff was selling the chapter on the argument the chapter exists to refuse.

[Chapter 10](../10_patterns-that-cross_r8dw.md) said [chapter 11](../11_patterns-that-survive-translation_us2k.md) groups patterns "by what they are about."
That is the organization [chapter 11](../11_patterns-that-survive-translation_us2k.md) rejects: *"Catalogues are organized by shape, so they let you look up what you already know the name of. Grouping by Force lets you find the name from the problem."*

[Chapter 12](../12_missing-language-features_esqm.md) ended on "the argument was over before anyone noticed it had started," dropping the qualifier that is half of [chapter 13](../13_smuggled-verdicts_8y69.md)'s claim — how much you concede depends on whether the word also names something you can check.

[Chapter 21](../21_style_9rng.md) described [chapter 22](../22_never-written-down_at4r.md) as putting the five kinds to work on "a blog post, a review comment, a colleague's strong opinion."
[Chapter 22](../22_never-written-down_at4r.md) says those are what *every chapter before it* worked on, and that it takes the case where **there is no assertion at all**.
This one is a survivor of the cut synthesis chapter, describing a chapter that no longer exists.

**Why they drifted, which decision 108 got wrong.**
The argument for keeping them was that a paraphrase does not rot like a copy.
That is false in the direction that matters: a copy drifts *visibly*, because the two strings stop matching and a check can say so, while a paraphrase drifts **silently** and stays fluent.
Three of these four read perfectly well and were wrong about the chapter next door.

**Consequence.**
No mechanical check is possible here — the failure is semantic and the handoffs are prose by design.
What is possible is a rule about when to read them: **a handoff describes its neighbour, so changing a chapter's claim means checking the handoff that points at it.**
Two of these four are traceable to exactly that — [chapter 02](../02_forces_f4m5.md)'s claim was rewritten and [chapter 22](../22_never-written-down_at4r.md) replaced a different chapter, and in both cases the sentence pointing at them was left alone.

---

## 110. Slice 1 of the final sweep: four pieces routed, three retired

**Date.** 2026-08-26

**Context.**
Every chapter reached **draft**, and the author started the final sweep.
Slice 1 is the pending material: `docs/pending-tasks/` names the chapters it is owed to, and every piece is either routed to its chapter or recorded as no longer fitting.
Ten outstanding pieces across `ai-material.md`, `pike-retrospective.md` and `index.md`, owed to chapters 01, 02, 04, 08, 12, 14 and 16.

**The root question, and the draft's recommendation did not survive.**
Six of the seven chapters are at draft, so slice 1 is by construction the bolting-on that `pike-retrospective.md` warned against in its own deferral argument — *"a quotation bolted onto a finished chapter is the decoration the register rules exclude."*
The draft recommended a **minimal footprint**: discharge each piece in the smallest form that still says the thing, attach to existing paragraphs, no new headings.

The author chose the third option instead — **route only what strengthens the chapter, and formally retire the rest with reasons.**
That is a higher bar than the draft proposed, and it changed four of the ten dispositions.
Recorded because the difference matters: under the draft's answer every piece would have landed somewhere, which is the ledger-defect shape the anti-repetition protocol exists to prevent.

**Three facts found during the interview that changed the questions being asked.**

[Chapter 16](../16_tdd-and-mocks_u8eu.md) already carried FlowCore decision 37 in full — the count, the mutation, the comment above the weak fixture, the entry's verdict.
So the mechanism and the evidence were never what it was owed, and the question narrowed to what the provenance adds.

[Chapter 22](../22_never-written-down_at4r.md) already made the argument [chapter 14](../14_principle-loses-scope_b86v.md) was owed, at the line about a corpus default being the purest folk remedy.
Meanwhile ledger row *The scope was never set* assigned that concept to `b86v`, and [chapter 14](../14_principle-loses-scope_b86v.md) contained no trace of it — so the ledger was asserting an ownership that did not exist.

One of the two *known coverage gaps* was half stale.
It said the dependency-injection container is owned by no chapter; [chapter 01](../01_the-five-kinds_cjx4.md) classifies it as an Idiom and separates it from the Principle it travels with, and [chapter 20](../20_idioms_7nkn.md) gives its conditions.
It also said [chapter 17](../17_abstraction-as-insurance_4jk6.md) "reaches the testing half of the question and no further", which understates a chapter with six subsections on the swappability case.

**Decision — the ten dispositions.**

| Piece | Chapter | Disposition |
|---|---|---|
| Corpus monoculture | 01 | routed, with the uniform-confidence clause folded in |
| Pike on certainty over trivial features | 01 | routed |
| Cannot see your Forces | 02 | folded to one sentence inside the piece below |
| Team-size Force at its extreme | 02 | routed |
| Compatibility priced by the person who paid it | 08 | routed |
| The scope was never set | 14 | **retired**; ledger row moved to `at4r` |
| Generated tests that never reach their condition | 16 | **retired** from the FlowCore paragraph; the volume point routed to the costs section instead |
| async/await and coloured functions | 12 | **retired** |
| The 45-minute build | 04 | **retired** |
| Known coverage gaps | — | kept in `index.md`, with the stale half corrected |

**Why each retirement.**

[Chapter 14](../14_principle-loses-scope_b86v.md) tracks scope lost **in transmission** — a compressed sentence that travelled without its conditions.
Generated design has no sentence and no transmission, so 14's test (*does this advice say how wide it is?*) has no input rather than a wrong answer.
`ai-material.md` had never worked the argument, and [chapter 22](../22_never-written-down_at4r.md) had already made it.
The ledger row is reworded and moved to `at4r`, keeping the part that was distinctive — that 14's repair needs a source to go back to, and a corpus default has none.

[Chapter 16](../16_tdd-and-mocks_u8eu.md)'s two paragraphs before the FlowCore case work specifically to close off the reader's escape — *"this could look like a rookie mistake, or an example built for the book"* — and then build a human account of how a test file arrives in that state.
A provenance clause there hands the same dismissal back in AI form.
What was genuinely new went to the costs section, where the chapter says the where-to-mutate decision has no rule to hand: spot-checking rests on the author's own list of assertions they were unsure about, and tests generated in bulk arrive without one.

The last two were already dispositioned in `pike-retrospective.md` and are only being made final: coloured functions was ruled *nowhere* on 2026-08-23, and the 45-minute build is background [chapter 04](../04_structure_agjy.md) does not need.

**An author correction, on what gets deleted.**
The draft proposed deleting `docs/pending-tasks/` entirely and relocating the *known coverage gaps* to `docs/ABOUT.md`, and put the destination to the author as a question.

> who told you to delete the folder pending-tasks? If there are still things to do in index.md keep index.md and the folder, you don't have to move those to other places.

The draft had inferred the deletion from `CLAUDE.md`'s *delete a document once every piece in it has landed*, which decision 92 wrote for the worked-argument documents, and applied it to the index as well.
The index is not that kind of document: it is the folder's own list, and the coverage gaps are recorded limits rather than landed arguments.
`index.md` and the folder stay, the gaps stay where they are, and only `ai-material.md` and `pike-retrospective.md` are deleted, both fully discharged.

**A splice found in a pending document, and corrected before it shipped.**
`pike-retrospective.md` said Pike "lists *using upper case for export* alongside *where the newlines go* as perennial arguments", offered as the witness for [chapter 01](../01_the-five-kinds_cjx4.md).
Reading the talk shows two separate sentences: one about the certainty with which people argue over trivial features, and — two sentences later, on a different subject — a list of topics the talk will skip because they have already been discussed at length.
Pike never says those are the trivial features argued with certainty; the connection was the pending document's, presented as his.
The first draft of the chapter 01 paragraph inherited it, including a point about the two examples landing in different kinds by the book's own test.
Both were cut, and only what he said is quoted.

This is the failure `CLAUDE.md` describes at [chapter 14](../14_principle-loses-scope_b86v.md)'s Pike material, in the same source, caught this time by the rule that came out of it: read the primary source rather than the excerpt document, even when the excerpt document is in this repo.

**Consequence.**
Chapters 01, 02, 08 and 16 are amended, one commit each.
Ledger changes: two rows rewritten to the narrower claims that shipped, two added, one moved from `b86v` to `at4r`, one extended.
Six ledger rows pointed at `docs/pending-tasks/ai-material.md` as the argument's home; all six pointers are spent and go with the file, three of them on chapter 22 rows whose material landed long ago.
`docs/pending-tasks/` survives on `index.md` alone, which now holds nothing but the two coverage gaps.

Chapter 08 gained a citation and has no `## Sources` section to put it in.
That is slice 3's work and is deliberately left for it, which is what `CLAUDE.md` means by content added during a slice not having been through the slices already finished.

---

## 111. Decision 110 in part reversed: the chapter 01 and 16 additions are cut

**Date.** 2026-08-26

**Context.**
The author's review of slice 1, commit `d285001`.
Four tags and one direct edit across the four amended chapters.
Two of the four pieces the draft had routed are removed, one is rewritten under a direct edit, and one is kept but sent back for clarification.

**Decision — the chapter 01 and chapter 16 additions are cut, permanently.**
The author's reason, given identically on both:

> let's remove previous two paragraphs, the late addition didn't mesh well

And the standing instruction that came with the review:

> those deleted materials were considered and the decision was to not use them anywhere in the book. We don't need to think about finding other places for those.

So this is a retirement rather than a re-routing.
The corpus-monoculture argument, the uniform-confidence clause, the Pike certainty witness, and the mutation-volume point are decided against for the book as a whole, and no chapter is owed them.
[Chapter 01](../01_the-five-kinds_cjx4.md) and [chapter 16](../16_tdd-and-mocks_u8eu.md) are byte-identical to their pre-slice-1 state.

**What the surviving two have in common, which is worth carrying into slice 2.**
Decision 110's bar was *route only what strengthens the chapter*, applied by the draft to ten pieces; the author then cut two of the four that passed it.
The two that survived attach to a question their section had already opened.
[Chapter 02](../02_forces_f4m5.md)'s section is about a Force as a dial, and the addition is a value at the end of that dial.
[Chapter 08](../08_change_rjf9.md)'s section argues a constraint and had only the victim's posture, so the designer's is the missing half.
The two that were cut added a new subject to a section that had finished its argument — three extra paragraphs hung under two entries of [chapter 01](../01_the-five-kinds_cjx4.md)'s four-mechanism list, and a fifth consideration appended to [chapter 16](../16_tdd-and-mocks_u8eu.md)'s costs.
**A late addition survives if the section was still asking something. It does not survive being another thing the section could also have said.**

**The direct edit in [chapter 02](../02_forces_f4m5.md), which is an improvement, and two slips it introduced.**
The author replaced the draft's *"One kind of contributor sits at the extreme of both halves"* with *"AI coding agents sit at the extreme of both halves"*, and *"generated code answers the second with none"* with *"for coding agents the answer to the second is nobody"*.
That is better: the draft's phrasing was coy about its subject, and naming it costs nothing the dating rule protects, which is about capability claims and version numbers rather than about saying what is being discussed.

The edit also moved the subject from generated code to the model, and two predicates were left behind.
*"The model … arrives at a volume the review step was not sized for"* — the output arrives at volume, not the model.
*"The agent can only reach it to the extent that some prompt happened to carry them"* — *it* has no antecedent; the thing being reached is the Forces, which *them* refers to in the same sentence.
Both repaired, keeping every word of the author's that was doing work.

**The [chapter 08](../08_change_rjf9.md) tag was a question, not a removal.**

> this seems like an intersting point and good addition but I read it two times and couldn't get the exact meaning … what you mean by "feature-itis" and what is the trade-off here and why that is justified and doesn't contradict our chapter?

Three things were missing and are now stated.
*Feature-itis* is defined rather than quoted through — a language steadily accumulating features, each defensible on its own.
The mechanism connecting it to compatibility is given: under the promise anything added is added permanently, so a proposal has to be worth keeping for the life of the language, which most are not.
And the non-contradiction is stated outright, because the draft had left the reader to infer it: *once published, it is forever* is unchanged, Pike is not disputing it, and the difference is timing — a team that discovers the rule after it has users has no choice left, and Go's team took it at 1.0 while declining was still available.

That the question had to be asked is the finding.
The draft's version ended *"the deprecated declarations are one side of that trade, and the features it stopped are the other"*, which reads as though both were costs, when one is the cost and the other is what the cost bought.

**A tag acted on by its reason rather than its count.**
[Chapter 16](../16_tdd-and-mocks_u8eu.md)'s tag said *"remove previous two paragraphs"*, in the same wording as [chapter 01](../01_the-five-kinds_cjx4.md)'s, where two paragraphs were indeed the draft's.
In [chapter 16](../16_tdd-and-mocks_u8eu.md) only one was: **Mutation testing is expensive** predates slice 1 and is present at `12faccb`.
The stated reason — *the late addition didn't mesh well* — applies only to the added paragraph, so one paragraph was removed and the pre-existing cost item was left alone.
Raised here rather than settled silently; if the author did want the costs item gone, it is one line to remove.

**Consequence.**
Slice 1's tally is two routed and five retired, not four and three.
`docs/pending-tasks/index.md` is corrected to say so.

Ledger: row *Why the kinds get confused* is reverted to its pre-slice-1 wording, and the rows *Corpus monoculture* (`cjx4`) and *Volume removes the cheap alternative to mutation* (`u8eu`) are deleted, both concepts now being owned by no chapter and owed to none.
Row *The team-size Force at its extreme* is rewritten into the vocabulary the chapter now uses.
Row *Compatibility adopted rather than suffered* carries the mechanism the chapter now spells out.

[Chapter 01](../01_the-five-kinds_cjx4.md)'s `## Sources` entry for the Pike retrospective is removed with the paragraph that cited it; nothing in that chapter cites him now.
[Chapter 08](../08_change_rjf9.md) still has no `## Sources` section and still needs one for the same talk, which remains slice 3's work.

---

## 112. `docs/ABOUT.md` reviewed before slice 2, and it was wrong about the book in six ways

**Date.** 2026-08-26

**Context.**
`CLAUDE.md` requires `docs/ABOUT.md` to be reviewed before slice 2, on the grounds that slice 2 applies the chapter rubric to every chapter and measuring the book against an unchecked statement of that rubric is circular.
The review found the document had drifted from the book on every count it makes.
`README.md` names it as the home for the rubric, the language conventions, the running example, and the license, so its scope was never in question and this is a correction pass rather than a question about what the file is for.

**The two findings that matter, because they are in the rubric itself.**

**Part IV named the wrong chapters, and `CLAUDE.md` carried the same error.**
Both documents said [chapters 14](../14_principle-loses-scope_b86v.md), 16 and 17 are the case studies.
`CLAUDE.md`'s very next clause contradicts it — *"[chapter 14](../14_principle-loses-scope_b86v.md) makes the claim; they are three instances of it"* — and the files settle it.
[Chapter 14](../14_principle-loses-scope_b86v.md) uses the general rubric, opening on `## The claim` and running through `## The demonstration`.
[Chapters 15](../15_behaviour-placement_z47a.md), 16 and 17 all use the case-study shape, opening on `## The advice` and `## What the wide reading produces`.
So the list should read 15, 16 and 17, and [chapter 15](../15_behaviour-placement_z47a.md) had been sitting under a rubric that does not describe it.
Corrected in both files, and `CLAUDE.md` now also says explicitly that [chapter 14](../14_principle-loses-scope_b86v.md) keeps the general rubric, which is the fact that made the original sentence ambiguous.

Caught only because this review is scheduled before slice 2 rather than after.
Slice 2 is the pass that would have enforced the wrong rubric on [chapter 15](../15_behaviour-placement_z47a.md).

**The back matter was described in the wrong order and missing a component.**
`ABOUT.md` had it as *"a Sources section … and a line handing off to the next chapter."*
The handoff is not back matter: it is the argument's last paragraph, before the divider, written as prose with no label.
After the divider come Sources and then the navigation row, which the document never mentioned at all.

**Four further corrections, each a claim about the book that had stopped being true.**

*Languages.*
`ABOUT.md` said Go, C# and Python carry most examples, with Rust, TypeScript, C and SQL where needed.
Counting fenced blocks across the twenty-two chapters: Go 119, Python 25, SQL 14, **Java 10**, C# 6, C 2, Rust 1, JavaScript 1, **TypeScript 0**.
Java is the third-heaviest language in the book and was named in neither document; TypeScript is named in both and appears nowhere.
C# is lighter than Java and was billed as one of the three that carry the book.
Rewritten to what the book contains, with Java placed where it actually sits — the chapters on missing language features and on behaviour placement, both of which need a class-based contrast.

*The running example's range.*
Both documents said FlowCore supplies examples in Parts II and V.
It also carries [chapters 15](../15_behaviour-placement_z47a.md) and 16, at six and seven mentions, which is as heavy as anything in Part V.
Corrected to Parts II, IV, and V in both.
Parts I and III have one passing mention each and are not claimed.

*The filename convention.*
`ABOUT.md` still said `NN_slug.md`, from before decision 107 gave every chapter a permanent identifier.
Now `NN_slug_ID.md`, with one line on why the identifier exists, since a reader looking at the repository will otherwise read the four characters as noise.

*Two broken references.*
The license linked to `LICENSE`, which from `docs/` resolves to a file that does not exist; now `../LICENSE`.
And the Files section ended *"This README is the entry point"*, which `ABOUT.md` is not.

**Also.**
The working-documents list named only `DECISIONS.md` and `LEDGER.md`; `STATUS.md` and `docs/pending-tasks/` are added.
`LEDGER.md` was described as *"one owner per chapter"*, which inverts it — the ledger assigns one owner per concept.

**The Part IV exception is stated in one sentence, not reproduced.**
Put to the author as the review's only real choice, since `ABOUT.md` could have carried the full seven-step alternate shape.
The author took the compact form.
The reason it is the right one is that two documents stating the same rubric in full is the drift class `tools/check-drift.py` exists to kill, and nothing checks `ABOUT.md` against `CLAUDE.md`.
`CLAUDE.md` stays the operative checklist for slice 2; `ABOUT.md` tells a reader the shape is not uniform and why.

**Consequence.**
`docs/ABOUT.md` is rewritten.
`CLAUDE.md` takes three corrections: the Part IV chapter list, FlowCore's range, and the language palette.

The language palette is the one to look at again, because it is a rule rather than a description and changing it was the draft's call.
It now reads *"Go and Python carry most examples, with Java and C# where a point needs a class-based contrast; SQL, C, Rust, and JavaScript appear where a point needs them."*
The old wording was not wrong as guidance — it was a palette to reach for — but it named a language the finished book never used and omitted one it uses ten times, and slice 2 checks chapters against these rules.

---

## 113. Slice 2 of the final sweep: rules applied to the chapters that predate them

**Date.** 2026-08-26

**Context.**
Slice 2 checks each chapter against the rules in `CLAUDE.md` that postdate it, excluding rules that were already applied retroactively.
The method `CLAUDE.md` prescribes is `git log CLAUDE.md` against each chapter's own history, and a commit touching this file *and* many chapters at once counts as already applied.

**The timeline, built once and worth keeping.**
Every chapter's most recent commits are the mechanical sweeps of 2026-08-25 — renumbering, identifiers, navigation — so the date that decides which rules a chapter was written under is its **creation** date, not its last touch.

Two rules were never applied retroactively and reach the most chapters:

| Rule | Added | Chapters predating it |
|---|---|---|
| Identifier naming in code samples | 2026-08-15 | 01–11 |
| A source's register is not the book's | 2026-08-19 | 01–15 |

Chapters 17–22 postdate every rule in the file, so slice 2's remit for them is empty.

**What was found, by chapter.**

[Chapter 01](../01_the-five-kinds_cjx4.md) — three, and the first is the one worth recording. The chapter establishes that *"the levels are rungs on the ladder, and Force is the fifth kind precisely because it is not on it"*, then closed by saying a disagreement about a Force sits *"one rung down from where it is being conducted."*
That is the four-levels-five-kinds rule broken by the chapter that defines it, eleven days after the rule was written.
Also `goroutine` unglossed in a code comment, which survived because automated checks skip fenced code; and a three-sentence annotation in `## Sources` whose real content — Alexander quoted via Appleton, *The Timeless Way of Building* unread — moved into the prose making the claim.

[Chapter 02](../02_forces_f4m5.md) — `uid` across three samples in Python, Go and C, and `n` for a line-item count in two more. Both `split` samples were re-run after the rename rather than assumed; output unchanged. The comma-ok idiom had no gloss anywhere, though `CLAUDE.md` names it twice.

[Chapter 04](../04_structure_agjy.md) — `defer` and comma-ok unglossed, and `ECS` used bare with its expansion arriving 47 lines later.
Parnas was verified against the paper rather than trusted, because the chapter says *"Parnas proposed something narrower"*, which is the sentence shape that triggers reading the source. Both claims hold verbatim: *"it is almost always incorrect to begin the decomposition of a system into modules on the basis of a flowchart"*, and *"Every module … is characterized by its knowledge of a design decision which it hides from all others."*
No change was needed, and the chapter has no `## Sources` section to record that in yet.

[Chapter 06](../06_distribution_49yh.md) — CAP was stated as *"a linearizable register cannot also be available during a partition"*, with linearizability then listed among the assumptions, unexplained.
This is exactly what the source-register rule is about: the sentence is CAP's formal statement in CAP's vocabulary, and the reader decodes rather than follows. Rewritten to lead with the situation and name the thing last, and to say that *Consistency* here is much narrower than the everyday word.

[Chapter 09](../09_what-a-pattern-is-for_3xzc.md) — a repository called `repo`, in the chapter that examines the Repository name.

[Chapter 11](../11_patterns-that-survive-translation_us2k.md) — `CQRS` bare, though it is on the must-expand list.

**A ledger row that kept vocabulary its chapter had dropped.**
The source-register rule was written *about* [chapter 16](../16_tdd-and-mocks_u8eu.md) carrying the `GRA / UNI / SEQ / REF` abbreviations from Fucci et al.
The chapter was fixed. `docs/LEDGER.md`'s row for the same exhibit was not, and still read *"GRA, UNI, SEQ, REF and which survived model selection"* — the retired vocabulary preserved in the index that is read before drafting.
This is the failure `CLAUDE.md` describes under *a wording problem found in one place is a survey*: the ledger carries the same vocabulary and goes stale silently.
Rewritten in the chapter's own words, and a count corrected on the way — three of the four dimensions survived the analysis, not two.

**Four chapters were checked and needed nothing, which is worth recording as a result rather than a silence.**

[Chapter 07](../07_scale_637f.md) is the model `CLAUDE.md` cites for leading with the situation, and it earns it — *utilization* is given in the queueing sense at first use, a cache line is *"64 bytes on most machines"*, Coherency gets a full paragraph before the bare term reappears 130 lines later, and the Universal Scalability Law arrives with the caveat that its coefficients are fitted rather than derived.

[Chapter 08](../08_change_rjf9.md) satisfies the no-splicing rule in the text itself: *"The negotiation mechanism is his. What this book adds is the asymmetry…"* and *"Conway states the homomorphism; drawing this consequence out of its direction is this book's."*

[Chapter 15](../15_behaviour-placement_z47a.md) quotes Riel by heuristic number, gives his own gloss on *related*, and carries his standing instruction that the sixty are *"warning bells"* rather than rules.

[Chapter 14](../14_principle-loses-scope_b86v.md)'s Pike comparison — the passage that produced the read-the-whole-source rule — now labels itself *"a structural claim rather than an empirical one"*, so the relationship between the two proverbs reads as the book's observation rather than as Pike's.

**Two things fixed that no postdating rule required.**
[Chapter 04](../04_structure_agjy.md) used *Part one* through *Part four* as its own section headings, colliding with the book's Parts I–V, so *"Part three works through one that doesn't"* read as a reference to Part III. Put to the author, who chose to rename; the headings were already descriptive after the colon, so the number was carrying nothing.
[Chapter 19](../19_six-profiles_dnkz.md) spelled out *line-of-business* three times and abbreviated it to `LOB` once, between two spelled-out uses. One word.

**Consequence.**
Nine chapters amended, one commit each or grouped where a group needed one change between them.
`docs/LEDGER.md` takes one row rewrite.
Chapter statuses are unchanged; slice 2 is a rules pass, not a status transition.

Slice 3 inherits a larger job than its description implies: **thirteen chapters have no `## Sources` section** — 02 through 13, and 19 — and two of slice 2's findings deferred to it, chapter 04's Parnas verification and chapter 08's Pike citation from slice 1.

---

## 114. *Force* is not a borrowed word, and the provenance paragraph is cut

**Date.** 2026-08-26

**Context.**
Reviewing slice 2, the author cut [chapter 01](../01_the-five-kinds_cjx4.md)'s paragraph on where the word *Force* comes from — the pattern-writing literature, Alexander's formulation, and the note that the Gang of Four book does not use the term.
Slice 2 had just strengthened that paragraph rather than questioning it, by moving the *Timeless Way of Building was not consulted* disclosure into it from `## Sources`.

**The author's objection, in their own words.**

> I don't think we borrowed this word, we didn't start by reading "Timeless Way of Building" and then thinking about forces and It doesn't seem that the way we use Forces and Appleton uses there are identical. I really don't think we need to be apolegitic about using such a common word and try to go such lengths to explain the provenance.

**Decision.**
The paragraph is deleted. The paragraph after it keeps only what it said about the book's own meaning, rewritten to stand alone: a Force is read before any pattern or technique is in view, and it is one of the five kinds in its own right, which is what lets it decide whether a Law binds and whether a Principle inverts.

**Why the objection is right, stated in the book's own terms.**
*Forces* in the pattern-writing literature is a **field in a template** — part of how a pattern is written up, describing the tensions that one pattern resolves.
A Force in this book is a **kind of claim**. Those are not the same thing under one name, so the relationship was never a borrowing; it was a collision between a common word's two uses.
Describing it as borrowed also contradicts what `CLAUDE.md` says about this model: *the five-kind model is the book's own, and every chapter that leans on it should read that way.* Two paragraphs of provenance for one of the five names read against that.

**Three dependencies the cut had, found by survey rather than by the tag.**
This is the *a wording problem found in one place is a survey* rule, and all three would have been left behind by a local deletion.

- [Chapter 01](../01_the-five-kinds_cjx4.md)'s **opening paragraph forward-referenced it**: *"You will not find these five names used together this way elsewhere — with one exception, noted where that kind is defined below, because Force turns out to have a literature of its own."* The clause is now gone, and the sentence is stronger for it: the model is the book's own with no exception attached.
- **Appleton was the chapter's only `## Sources` entry.** Nothing in the chapter cites him now, so the entry and the section went with the paragraph. Amdahl and Knuth are named in passing but no work is cited for either, and their chapters own them.
- **`docs/LEDGER.md` had a row** — *Force is a borrowed word* — assigning the concept to `cjx4`. Deleted; no chapter carries it.

**What is lost, recorded so the decision can be reversed knowingly.**
A reader who searches for *forces* alongside *patterns* will find Alexander and Appleton, and will find the word used for something else.
The deleted paragraph pre-empted that. Nothing does now.
The judgement is that the risk is small — this section and the whole of [chapter 02](../02_forces_f4m5.md) define the book's sense at length, so a reader has no shortage of context — and that it does not justify two paragraphs of apology in the chapter that introduces the model.

**Consequence for slice 3.**
[Chapter 01](../01_the-five-kinds_cjx4.md) now has **no `## Sources` section, deliberately**, because it cites no work.
Slice 3's instruction is that every chapter lacking one gets one, and this chapter is the exception unless slice 3 finds a citation the chapter actually makes.

---

## 115. The claim of originality is cut, and decision 40 was wrong about why it was needed

**Date.** 2026-08-26

**Context.**
Continuing the slice 2 review, the author cut [chapter 01](../01_the-five-kinds_cjx4.md)'s remaining opening paragraph — *"This premise, and the model attached to it, are this book's own. You will not find these five names used together this way elsewhere…"*

> just delete this paragraph as well. This is like a door to door salesman pitch. Books don't say this thing is book's own, they point what is borrowed and put references for those which we already do.

**The draft raised a conflict, and was wrong to treat it as one.**
Decision 13 dropped provenance markers with the rule that *where a claim's standing could be mistaken, the sentence says so*.
Decision 40 then removed the chapter epigraphs, and said of this one:

> [Chapter 01](../01_the-five-kinds_cjx4.md)'s epigraph carried **the only statement** that the five-level model is this book's own rather than standard vocabulary — provenance that decision 13 requires be in the prose. It now sits in the claim section.

So the paragraph existed because decision 40 put it there, and `CLAUDE.md` says to stop and say so when a change contradicts the log. The draft stopped and asked.

The author's reply was to ask what they were missing.

**Nothing, and the log is what was wrong.**
Checking the chapter as it stood at decision 40's own commit shows *Vocabulary nobody shares* already present, in *What the model costs*:

> "That's an Idiom, not a Law" means little to colleagues who haven't read this. The model is for your own thinking; in conversation, say the content.

Decision 40's *the only statement* was false when written.
The costs section already carried the same information and carries it better: it does not assert originality, it tells the reader what the vocabulary will and will not do for them, in the section about what the model costs — which is where a reader can act on it.

**Decision.**
The paragraph is deleted. Nothing replaces it.
Decision 13's requirement is satisfied, at the site that was always satisfying it.

**The general point, which is the author's and worth keeping.**
Defining a term and stating the chapter's claim is the work. Announcing that the work is original is a separate move, and it is the book selling itself rather than saying something.
The five other places where the book marks its own vocabulary — [chapters 03](../03_grading-a-law_q5c6.md), [04](../04_structure_agjy.md), [13](../13_smuggled-verdicts_8y69.md), [17](../17_abstraction-as-insurance_4jk6.md), [19](../19_six-profiles_dnkz.md) — are all the shape the author describes: a clause at the point the term is used, saying it is not standard vocabulary so the reader knows what a search will return. None of them claims credit, and none is a paragraph.

**A note on the draft's error, since the log is where method gets recorded.**
Raising the conflict was right; deferring to the log without checking its factual claim was not.
A decision entry is evidence about what was decided, not about what was true, and *the only statement* is the kind of assertion that can be checked in one command against the commit the entry describes.
Checking it first would have turned a question for the author into a finding.

**Consequence.**
[Chapter 01](../01_the-five-kinds_cjx4.md)'s opening is the claim, then the paragraph beginning *Both are assumed by the rest of the book*, whose *Both* now points directly at the two assertions in the claim sentence and is explained in the same paragraph.
Decision 40 stands as the record of the epigraph removal; this entry corrects its statement about [chapter 01](../01_the-five-kinds_cjx4.md).

---

## 116. Slice 3 of the final sweep: Sources

**Date.** 2026-08-26

**Context.**
Slice 3 gives a `## Sources` section to every chapter lacking one, with links verified rather than recalled.
Fourteen chapters lacked one at the start: 01 through 13, and 19.

**Decision — ten chapters get one, four do not, and the four are the finding.**
`CLAUDE.md` says Sources lists *every work the chapter cites, and nothing else*, and that it is **not a further-reading list**.
Applying that literally, a chapter that names a standard result as a label — *Amdahl's Law is true of a single-threaded script* — is not citing a work. A chapter that states a result **with its assumptions**, presents someone's algorithm, or quotes them, is.

On that test:

- **[Chapter 01](../01_the-five-kinds_cjx4.md)** names Amdahl and Knuth as labels only, and after decision 114 removed the Appleton material it cites nothing. No section.
- **[Chapter 03](../03_grading-a-law_q5c6.md)** discusses Two Generals, Hyrum's Law, Conway's Law and Amdahl's Law entirely as named results whose chapters own them, and quotes no work. No section.
- **[Chapters 11](../11_patterns-that-survive-translation_us2k.md) and [19](../19_six-profiles_dnkz.md)** name no external work at all — they are synthesis chapters drawing on the rest of the book. No section.

Adding sections to those four would have made them further-reading lists, which is the one thing the rule forbids.

**[Chapter 07](../07_scale_637f.md) settled a question it had already answered.**
Its *About the numbers* section states that *"every measurement here was taken on the machine this was written on — an Apple M4 laptop, Go 1.26.5"*, so none of its tables needs a source. What it cites is the three results it states and uses: Amdahl, Gunther's Universal Scalability Law, and Little's Law.

**Verification found two things a recalled citation would have got wrong.**

The first is why the rule says *verified*.
`web.mit.edu/~sgraves/www/papers/Little's Law-Published.pdf` returns 200 and **redirects to a faculty homepage** — it is not the paper. It was dropped rather than listed.

The second is more interesting, and it went the other way.
[Chapter 12](../12_missing-language-features_esqm.md) cites Norvig's talk as *Design Patterns in Dynamic Programming*. The landing page at `norvig.com/design-patterns/` is headed *Design Patterns in Dynamic Languages*, which looked like a chapter error.
The slide deck itself settles it — its title slide reads *Design Patterns in Dynamic Programming*, Peter Norvig, Chief Designer, Adaptive Systems, Harlequin Inc., **Object World, May 5, 1996**.
The chapter was right and the landing page would have produced a wrong "correction". The entry now carries the verified venue and date and notes the page's later title, so a reader following the link does not think it is a different talk.

**Books and unreachable papers get an entry without a link**, following [chapter 15](../15_behaviour-placement_z47a.md)'s Riel entry, which has none.
That covers Brooks, the Gang of Four, Evans, Lehman, and Little, and it removes the pressure to attach a link that has not been checked.

**A format split, settled.**
The eight chapters that already had the section disagreed: [14](../14_principle-loses-scope_b86v.md), [15](../15_behaviour-placement_z47a.md), [16](../16_tdd-and-mocks_u8eu.md), [17](../17_abstraction-as-insurance_4jk6.md) and [18](../18_force-map-method_r37x.md) used a bulleted list with markdown links; [20](../20_idioms_7nkn.md), [21](../21_style_9rng.md) and [22](../22_never-written-down_at4r.md) used blank-line-separated paragraphs with bare `<url>`.
A Sources section is a list, `CLAUDE.md`'s markdown conventions have a rule for lists, and the bulleted form is both the majority and the earlier convention. The three outliers were normalized.

**Links.**
All 50 unique URLs across every Sources section were checked, including the pre-existing ones.
47 return 200. Three are bot-blocked rather than dead — IEEE, Reddit, and a university server — and two of those are pre-existing entries whose companion link works.
[Chapter 17](../17_abstraction-as-insurance_4jk6.md)'s Robert C. Martin paper was moved off a mirror that blocks automation onto `objectmentor.com`, his own company's copy, which serves the PDF directly.

**Consequence.**
Ten new sections; three normalized; one link replaced.
Slice 4 — reconciliation — is the last, and takes ledger rows against what each chapter now owns, then `tools/check-drift.py`.

---

## 117. Slice 4 of the final sweep: reconciliation

**Date.** 2026-08-26

**Context.**
The last slice: ledger rows against what each chapter now owns, then `tools/check-drift.py`.
345 rows across 22 chapters, after three slices that changed nine chapters, deleted two working documents, and cut four paragraphs on the author's review.

**Structural checks, all clean.**
Every ledger owner id resolves to a real chapter, every chapter has rows, and no row points at `docs/pending-tasks/` now that the two discharged documents are gone.
No row references material the sweep cut — the *Force is a borrowed word* row went with decision 114, and the two rows for the [chapter 01](../01_the-five-kinds_cjx4.md) and [16](../16_tdd-and-mocks_u8eu.md) additions went with decision 111.
Every relative link in every chapter, the contents page and the README resolves to a file that exists.

**One real drift, and it is the third instance of a claim fixed twice already.**
`docs/LEDGER.md`'s *Deliberate repetition* section said FlowCore *"appears across Parts II and V"*.
Decision 112 corrected that claim in `docs/ABOUT.md` and `CLAUDE.md` after counting — it also carries [chapters 15](../15_behaviour-placement_z47a.md) and [16](../16_tdd-and-mocks_u8eu.md), at six and seven mentions, so the range is Parts II, IV, and V.
The ledger was not in that grep, which is exactly the failure `CLAUDE.md` describes: *the ledger carries the same vocabulary, goes stale silently.* Twice now in one sweep, counting the `GRA / UNI / SEQ / REF` row in slice 2.

**Two rows that had fallen behind their chapters.**

*Why the kinds get confused* listed three mechanisms; [chapter 01](../01_the-five-kinds_cjx4.md) states four and names the fourth, *teaching leaves the training wheels on*. Added.

*CAP, FLP, Two Generals by assumption* predated slice 2's rewrite of the CAP statement, so the canonical line said nothing about what *Consistency* means there. It now carries the definition the chapter gives, since that is the part a reader is most likely to get wrong.

**The anti-repetition scan found three candidates and all three were false alarms**, which is worth recording because a clean result here is the ledger doing its job.

*Transaction Script* appears five times in [chapter 09](../09_what-a-pattern-is-for_3xzc.md) and five in [13](../13_smuggled-verdicts_8y69.md). The ledger assigns it to **09**, not to [15](../15_behaviour-placement_z47a.md) as the scan assumed, and [chapter 13](../13_smuggled-verdicts_8y69.md) links to 09 in its second paragraph. It uses the name as a neutral term against *anemic domain model*, which is its own subject, and never redefines it.

*Idempotency key* appears twice in [chapter 09](../09_what-a-pattern-is-for_3xzc.md) with no link to [06](../06_distribution_49yh.md). Both are inside a table that counts words in names. The 22-word description is never written out, so nothing of [chapter 06](../06_distribution_49yh.md)'s material is repeated — the name is a specimen for 09's compression test, which is the legitimate use.

**A note on the scan itself, since method belongs here.**
The first mechanical check run in this slice was wrong and was discarded: it tested whether each row's *Others may say* column appears verbatim in the owning chapter, and reported 75 failures.
That column is *how other chapters may refer to* a concept — a permitted shorthand, not a quotation from the owner. The check was measuring something the ledger never claimed.
A mechanical check over a document's own format needs the format read first; 75 findings that all turn out to be the same misreading is the shape of that error.

**Consequence.**
`tools/check-drift.py`: 16 checks over 22 chapters, no drift. The twelve remaining notes are `text` fences wider than 72 columns, all terminal output rather than diagrams, which is what the note exists to distinguish.

The four slices are complete. Every chapter remains at **draft**; nothing in this sweep moves a status, and **ready** is a separate decision that is the author's alone.

---

## 118. [Chapter 01](../01_the-five-kinds_cjx4.md)'s opening is reorganized

**Date.** 2026-08-26

**Context.**
Asked whether the book was ready to promote, the draft named [chapter 01](../01_the-five-kinds_cjx4.md)'s opening as the one thing to fix first.
Decision 114 and decision 115 had removed two paragraphs from it, and what remained opened on a caveat: the first paragraph after the claim began *"Both are assumed by the rest of the book"*, a pronoun pointing at a paragraph that no longer existed, and its content was that this chapter cannot demonstrate its claim.

**The draft's fix, and the author's, which is larger and better.**
The draft reordered: it moved the paragraph naming the five kinds up beneath the claim, so a reader who has just been told there are five kinds learns what they are before meeting an epistemology note, and resolved the pronoun to *"The claim above has two halves."*

The author then restructured the chapter, and the draft kept all of it:

- `## The book's model` and `## The five kinds` are both gone. The chapter opens directly under its title on the claim.
- The five names fold into the claim sentence itself, so the ladder paragraphs follow immediately.
- `### Law`, `### Force`, `### Principle`, `### Idiom` and `### Style` are promoted to `##`, which is consistent once the section that contained them is removed.
- **The caveat moves to the end of the chapter**, as a closing section before the handoff, with its tense changed to the past.

That last move is the one that matters. The draft's version still opened the book's first chapter on what it could not prove; the author's opens it on the model and closes on the honest accounting. The draft's reorder was superseded rather than adopted.

**What the draft repaired.**
The new section carried an empty `## ` heading with no title and no blank line after it; it is now *What this chapter assumed*, which matches the register of the chapter's other closing headings.
*"the five claim classification and the authority mapping are true"* was ungrammatical and became *"both halves of that claim"* — which the author rejected in turn, on the grounds that the claim is now three hundred lines away and *"what claim, what halves?"* is a fair question from a reader who has just read the whole chapter. Their replacement sentence is the one that shipped.

**Two deviations from the rubric, raised and left standing as the author's choice.**
The claim is now two sentences where the rubric asks for one.
And [chapter 01](../01_the-five-kinds_cjx4.md) is the only chapter with no heading before its claim — every other opens `## The claim` or `## The advice`. Defensible here, since this claim is the book's premise rather than a chapter's and the title already names it.

---

## 119. The claim becomes *Many claims*, not *every*

**Date.** 2026-08-26

**Context.**
Decision 118's closing section conceded that the model is not exhaustive.
Reviewing it, the author refused the combination:

> If it does not survive inspection we should be honest with ourselves. Then it becomes "Many claims you meet about software is one of five kinds"

Either the claim is wrong or the concession is, and asserting *every* while conceding *not every* is neither.

**The draft argued against it and proposed a third way.**
`CLAUDE.md` says *a claim too vague to be false is not the safe fallback*, and *many* cannot be disproved or used.
So the draft proposed narrowing what the claim ranges over instead, keeping a true universal over a smaller domain: *every claim that bears on a software decision*.
The reasoning was that a claim which bears on a decision and is not advice is a property of your situation, which is a Force, so nothing qualifying would fall outside the five.

**The author falsified it with one example**, and it is worth recording in full because the draft had no answer:

> The government is planning to make it illegal to trade cryptocurrencies, we will have to change all our modules

That bears on a software decision. It is not advice. And it is not a Force, by [chapter 02](../02_forces_f4m5.md)'s own test — *an unmeasured Force has an instrument … a risk has none, and no amount of thinking produces one.* A forecast about someone else's future decision has no instrument, and it is negotiable by argument, which is precisely what a Force is defined not to be.
It is a **risk**, which [chapter 02](../02_forces_f4m5.md) separates from Forces in its own boundary section.

So the narrowing fails: any domain wide enough to hold Forces also holds risks, forecasts and estimates, because those bear on decisions too. And the example is ordinary rather than contrived — it is the kind of sentence said in real meetings.

**Decision — the author's original wording, reaffirmed after the argument.**

> I'm fine with those five kinds and I see no reason to dig to other kinds in this book.

The claim now reads *Many claims you meet about software are one of five kinds*. Whether the five are useful, and whether what falls outside them is a real gap, is left to the reader rather than answered by a chapter that would have to catalogue other kinds to answer it.
`is` was corrected to `are`.

**The sentence travels, so the change did too.**
Three other sites carried it: `README.md`'s first hook, which had the claim verbatim and would otherwise have kept asserting what [chapter 01](../01_the-five-kinds_cjx4.md) had stopped asserting; `docs/LEDGER.md` row 22; and the closing section itself.

**The concession is deleted rather than softened.**
With coverage no longer claimed, there is nothing to concede, so *What this chapter assumed* keeps only that the five kinds and their authority are assumed and not proven here, and why — the authority half is true by construction.
The line *"So this chapter was a way of sorting rather than a proof"* went with it, on the author's flag: the section now ends on *there is nothing left to show*, which is flatter and says the same thing.

---

## 120. The five kind names are capitalized when they name the kind

**Date.** 2026-08-26

**Context.**
The end-to-end read found [chapters 18](../18_force-map-method_r37x.md), [19](../19_six-profiles_dnkz.md) and [22](../22_never-written-down_at4r.md) using *force*, *principle* and *idiom* in lower case where the rest of the book capitalizes them.
In the identical position — *a Force* / *the Force* — the other nineteen chapters ran 68 capital to 0 lower case. [Chapter 02](../02_forces_f4m5.md) alone writes *the Force* 26 times for exactly what [chapter 18](../18_force-map-method_r37x.md) lower-cased, so there was no kind-versus-instance distinction hiding in it.

**A wrong explanation, corrected by the author.**
The draft argued that *Force* and *Idiom* needed fixing while *Law* and *Style* did not, because *"outside this book's model, a Force means nothing."*
That is false — *force* and *idiom* are ordinary English words, and the author said so:

> I see no difference between any of kind words regarding your statement.

They were right. The counts differ because **this book rarely has occasion for the ordinary senses of *force* and *idiom***, not because a different rule governs them. It is not a physics book and it does not discuss figures of speech, while it discusses *an empirical law*, *Lehman's laws* and *a style guide* constantly. One rule, five words, and a cleaner sample for two of them.

**The rule.**

> Capitalize when the word names one of the five kinds. Lower case for the ordinary word, for a proper name, and where the word modifies a noun.

The third clause is what handles the tail, and it was the part the draft underestimated. *Force map*, *force profile*, *force reading*, *force-mapping* stay lower case for the same reason *style guide* does: the word is modifying a noun rather than being one. So do *single responsibility principle* and *single-writer principle*, which are names, and *in principle*, which is an idiom of English.

**[Chapter 14](../14_principle-loses-scope_b86v.md) settled itself.**
The draft had held *principle* back as a genuine question, since [chapter 14](../14_principle-loses-scope_b86v.md) lower-cases it ten times and is arguably discussing advice-as-such rather than the kind.
Its first seven lines answer it. The title is *How a **Principle** Loses Its Scope*; the claim is *"A compressed **principle**…"*; the very next paragraph is *"Earlier chapters say a **Principle** has conditions … [chapter 04](../04_structure_agjy.md)'s information-hiding **Principle**."*
Capital, lower case, capital, capital, one referent, three paragraphs. A chapter that cannot hold the generic reading for two paragraphs running was not using one.

**Execution, and what review caught.**
The change was applied by script and reviewed as a word-level diff, which was necessary rather than cautious — the first pass was wrong in three ways.

- The determiner list was case-sensitive, so sentence-initial *A principle* was skipped while *its principles* in the same sentence was not.
- Bare plurals after a colon were missed, leaving [chapter 18](../18_force-map-method_r37x.md)'s claim reading *"forces, then Principles, then Idioms"* — worse than before the change.
- The rule protecting the verb *forces you to* also matched the noun in *"A force you cannot measure is not a force you get to assume."*

Five further mis-fires were found by listing every surviving lower-case instance and reading it, rather than by trusting the pass.

**Consequence.**
Roughly a hundred instances across [chapters 08](../08_change_rjf9.md), [14](../14_principle-loses-scope_b86v.md), [16](../16_tdd-and-mocks_u8eu.md), [17](../17_abstraction-as-insurance_4jk6.md), [18](../18_force-map-method_r37x.md), [19](../19_six-profiles_dnkz.md) and [22](../22_never-written-down_at4r.md).
The book now runs 124 capital to 14 lower case on *Force*, 59 to 4 on *Principle*, and 42 to 0 on *Idiom* — and every survivor is an attributive compound on the keep-list above.

[Chapter 18](../18_force-map-method_r37x.md)'s claim was the sentence that mattered most, and it now names the model's three rungs as the model names them: *Forces, then Principles, then Idioms.*

---

## 121. The book has no closing section, by decision

**Date.** 2026-08-27

**Context.**
The end-to-end read reported that the book has no ending: [chapter 22](../22_never-written-down_at4r.md) closes its own argument and stops, so the last words of the book are a *How to recognize the failure* paragraph and nothing returns to the question `README.md` opens with.
The author asked for an attempt at one.

**What was tried.**
A final section in [chapter 22](../22_never-written-down_at4r.md), after the rubric and before the back matter, in which the book ran its own test on itself — the five-kind model classified as a sorting scheme that sits outside the things it sorts, the three conditions the book's Principles carry stated in one place, and the observation that this book arrived as confident prose in one voice like the advice it examines, which is what the decision log exists to answer.

Two shapes were ruled out before that one and are recorded so they are not tried again. A recap of the argument is excluded by the register rules, which put grand summaries out of bounds, and would also be [chapter 14](../14_principle-loses-scope_b86v.md)'s mechanism running on the book in its own final pages. A closing exhortation is worse on both counts.

**Decision — reverted, and the book ends where it ended.**
The author's judgement:

> I read it and simply didn't like it, it's a dead end that can't be salvaged.

Reverted in full; [chapter 22](../22_never-written-down_at4r.md) is byte-identical to its state before the attempt.

**The point of recording it.**
The absence is now a decision rather than an oversight, which matters because a later pass over a finished book will notice the missing ending exactly as this read did.
The finding was correct and the remedy was not, and *the book stops on its last chapter's own last sentence* is the answer, not a gap waiting to be filled.

No reason beyond the author's judgement is recorded here, because none was given and inventing one would misrepresent what happened.

---

## 122. Chapter 23, and the grilling that produced it

**Date.** 2026-08-27

**Context.**
The author drafted an idea for a final, practical chapter in `docs/pending-tasks/last-chapter-idea.md` and asked for an evaluation before any drafting.
That evaluation is kept verbatim beside it as `last-chapter-idea-claude-review.md`, at the author's instruction, so it does not follow the one-sentence-per-line convention for `docs/`.
It offered two shapes: a derivation chapter, or the practical manifesto the notes reached for. The author chose the manifesto, with the derivation as its spine, and asked for the chapter to be worked through by grilling.

**The interview, in the order the questions were asked.**

**Q1 — how the new Forces relate to [chapter 02](../02_forces_f4m5.md)'s seven.**
The author's opening proposal was to relabel the seven as *software forces*, move team size out, and call the new set *human forces*.
Looking it up first changed the question. Every one of the seven ends with a *what changes with the Force* line, and every one names a **design** consequence — *whether a mistake is correctable*, *where the rule lives*, *what you can spend on abstraction*. So the seven are not software facts: team size is a fact about people and belongs there because reading it moves a rule into the type system, and two of the seven, blast radius and control of the callers, are organizational facts. The proposed label would have been false about the book, and the move would have cost *seven* becoming *six* in seven live places plus rehoming [chapter 11](../11_patterns-that-survive-translation_us2k.md)'s team-size family of six patterns.

The author's answer took the recommended split — by **what the reading decides** — and improved on it with the naming: **design Forces** and **organization Forces**.
Three checks made the retrofit free. [Chapter 02](../02_forces_f4m5.md)'s claim already says *design arguments*, so the label names something it has always said. [Chapter 18](../18_force-map-method_r37x.md) already says *the seven are not a closed list*. And [chapter 14](../14_principle-loses-scope_b86v.md)'s opening is the established move for introducing refined vocabulary late, in one paragraph. No earlier chapter changes.

**Q2 — the claim, where the author's revision beat the draft's.**
The draft proposed *"…and most standard process was chosen without reading any of them"*, which is an industry-wide assertion neither party can measure.
The author's replacement removed that: *"Organization forces carve pathways for the development processes. Following a process template without reading the forces leads to inefficiencies."* It claims what happens rather than what people do, which is checkable against the reader's own situation.

Two of its words did not survive the book's rules. *Carve pathways* is an image doing a mechanism's job, and it implies determinism where [chapter 18](../18_force-map-method_r37x.md) says a set of Forces **licenses** a set rather than determining one. *Inefficiencies* is the vague fallback the claim-sentence rule forbids. What shipped names the two failures the machinery actually predicts:

> **Organization Forces decide which development processes can work. A process template adopted without reading them produces ceremony where no Force is acting, and surprises where one is acting unread.**

That sentence also solved a problem the draft had raised separately: it **earns** the word *ceremony* by definition rather than asserting it, so the author's process criticism needed no retrospective hedging.

**Q3 — what the organization Forces are.**
Of the four in the notes, team size had moved to design Forces and *risks* is disqualified by [chapter 02](../02_forces_f4m5.md)'s instrument test, leaving two. Six were proposed with the test run on each, and the author took the set: skill spread, requirement volatility, decision latency, budget and runway, distribution, regulatory obligation. Three worked, three listed.

**Ownership was deliberately kept off the list.** It is the strongest idea in the notes, and a Force is *read* rather than established — the notes' own wording, *"owner should be clear before every step"*, is a prescription. It belongs at the root of the artifact chain, which is a stronger position than being one of six.

**Q4 — the shape.** [Chapter 11](../11_patterns-that-survive-translation_us2k.md)'s skeleton, with organization Forces where it has design Forces. Two placements do real work: the artifact chain is *why the claim holds*, because it is the mechanism; and the process criticism sits in *how to recognize the failure*, which conditions it structurally — that section is by definition about what it looks like when somebody got this wrong, so a standup with no blocker reads as a symptom rather than a verdict on standups.

**Q5 — what it demonstrates with, and a correction from the author.**
Decision 47 already settles half: *the book's process is not the book's subject*, so this book's own making is inadmissible.
The draft then proposed presenting the examples as anonymized real cases, since the author has decades of them and naming real people would be gossip. The author refused the framing:

> I don't think we should say something like those are real stories or these ideas came from someone that lived through all these. Those would be pointless. We make our points and tell our examples and if they sound reasonable and make sense they do, if they don't they don't.

That is the book's own rule — *cite people for provenance, never as proof* — applied to the draft's suggestion. A claim of lived experience asks the reader to extend trust on the speaker's standing, which is what the book spends every chapter arguing against. So the examples work exactly as [chapter 02](../02_forces_f4m5.md)'s do: constructed, mechanism visible, no provenance note, and the draft's proposed *unverifiable by the reader* line in the costs section went with it. The draft had this wrong twice in a row.

FlowCore appears once, for the per-slice scope rule, with its limit stated in the text: it is a single-developer project and can carry none of the Forces about several people.

**Q6 — placement.** Part V, chapter 23. The chapter cannot be called *Contextual Programming*, which is Part V's own name, so it is *Organization Forces: What Decides the Process*. Adding it also dissolves the problem decision 121 recorded: the practical chapter is now the book's ending, which is a better close than a coda classifying the book.

**Q7 — the counter-example, after a mistake.**
The draft had put regulatory obligation on the Force list in Q3 and then offered it as the boundary in Q4. It cannot be both: if regulation is a Force, a process it mandates is the claim working. So the chapter had no boundary, which the counter-example rule treats as evidence the claim is too vague.

The author's notes contained the first one — *"socially good to meet every week maybe but every day is theatre"* — a step answering no work Force that is right anyway, which yields the chapter's sharper test: **the reason given for a step has to be the reason it exists.**

The author supplied the second, and it is the better of the two because it is self-applying:

> With a team of highly talented engineers - managers who follow the forces instinctively and who have a track record of efficiency, our CP utopia would just be another set of ceremonies.

The chapter's own remedy convicted by the chapter's own claim. Two conditions were added in the interview and both strengthen it: it holds only while the team is stable, since [chapter 22](../22_never-written-down_at4r.md) owns what the reasoning costs when people leave; and the instrument is the shipping record rather than the self-assessment, because every team believes it is this team.

**Q8 — scope.** Five thousand words authorized. The draft came in at about 3,900 including back matter, and was not padded to the budget.

**Consequence.**
`23_organization-forces_i59b.md` at **in progress**. Chapter 22 gains a handoff and a next-chapter link.
The count moves from twenty-two to twenty-three in `00_toc.md`, `README.md` three times, `CLAUDE.md`, and `tools/check-drift.py`'s number-word map.
Nine concept rows and three example rows added to `docs/LEDGER.md`.
No earlier chapter's text changes, which was the point of Q1's answer.
