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
*Altitude* names the model but explains nothing until chapter 02 has been read; a title should not need a footnote.
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
The first draft of chapter 02 used both terms — "the five altitudes" in the title and model, "levels" throughout the prose.

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
The chapter file was renamed `02_the-five-altitudes.md` → `02_the-five-levels.md`.
Every occurrence of "altitude" was removed from `README.md`, `LEDGER.md`, and the chapter.
Chapter 23's title became "Reading advice at the right level"; Part I became "The five levels."

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

This is the same argument the book makes about pattern names in chapter 10 — a name earns its place by compressing, and an index compresses nothing — so using numbers here would have contradicted the book's own test.

**Consequence.**
Where relative position genuinely matters, the text names the ladder explicitly (Law → Principle → Idiom → Style) and says "one rung higher," rather than performing arithmetic on level numbers.
The `LEDGER.md` cross-reference convention was updated to `"a Law / an Idiom (Ch. 02)"`.

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
Chapter 02's *Where this doesn't apply* section closed with:

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
Recognizing something as an Idiom is not permission to ignore it, and chapter 21 argues that following local convention is usually correct even when one can out-argue it.
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
Discipline cannot compensate for missing information; a writer who does not know chapter 05 already covered acyclic dependency is not being careless when they cover it again.
The fix has to supply the missing information, which means it has to be external and written down.

The second option — drafting everything at once — trades one failure for a worse one: no opportunity for the author to steer between chapters, which is where this book's judgments are actually being made.

The third tolerates the defect being solved for.

**Consequence.**
The ledger was created **before** chapter 02 rather than retrofitted, so the first chapter was written against it.
The effect is visible in that chapter: it uses the seat-reservation race, manual DI wiring, and acyclic dependency, and explains none of them — each is demonstrated and handed to its owning chapter, e.g. *"the Law being broken is check-then-act, which chapter 06 owns."*

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
Chapter 05 had to say something about layering, which is the most widely endorsed structural advice in software and also the source of some of the worst structure in it.
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

It is also the book's own model applied to its most important structural material — three levels bundled under one name is precisely the failure chapter 02 describes.
If the model could not take layering apart, that would be evidence against the model.

**Provenance.**
The two-claim version — *dependencies flow one way* versus *and the layers are presentation/business/data* — comes from the FlowCore architecture dialogue at `~/c/TechIter/01/coding-style-architecture.md`, written in exchange with the author and corrected there.
That document also supplies the formulation the chapter quotes: *managed, acyclic dependency direction is a foundation of maintainable software; layering is its most common shape, not its definition.*
The draft's contribution is separating the taxonomy from its *expression as directories*, and attaching the five-level kinds to each claim.

**Consequence.**
Chapter 05 leads with the three-way table rather than with a definition of layering.
`LEDGER.md` records "layered is three claims" as owned by 05, so chapters 16, 18, 19, and 20 cite it rather than re-deriving it — 18 in particular, which owns what expressing claim 3 as packages actually costs.

---

## 9. Chapter 05 uses FlowCore for type-enforced direction, not for its package layout

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
Chapter 05 quotes decision 10's reasoning for keeping `querier` unexported ("a public commitment to a shape pgx defines") as its worked instance of export-surface-as-liability, and leaves the flat package unmentioned except as a cross-reference.
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
Its extra rules — `::: claim` fenced divs, `[Ch. 05](05_structure.md)` cross-reference links, ASCII-only diagrams, dropped `---` dividers — each traded source readability for build convenience, **and every one of them is a transformation a script can perform in a single pass years from now.**
Box-drawing glyphs need a font, not a rewrite; `(Ch. 05)` is a regex; `---` is one line of filter code.
Paying in readability today for work a machine can do later is the wrong direction.

The surviving rules are those a script *cannot* do:

- Joining prose into paragraphs is mechanical, but the resulting line lengths are what the author reads for the life of the project.
- Heading structure and fence tags are cheap now and ambiguous to infer later — nothing downstream can reliably tell a shell transcript from a diagram from Go.

**Correction: the 72-column code rule failed its own test.**
The first version of this decision required code fences to stay under 72 columns, on the reasoning that breaking a long signature well needs judgment and therefore could not be automated.
Chapters 02 and 05 were converted on that basis, with 16 lines rewrapped by hand.

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
Chapters 02 and 05 were converted: prose joined to one paragraph per line, chapter numbers removed from both H1s, 4 untagged code blocks given languages, and the DAG diagram in 05 narrowed from 86 to 52 columns.
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
Reviewing chapter 05, the author's reaction to `` `(established)` Parnas, 1972 `` was that the markers read as leftover draft notes rather than as content.

**Options.**
Keep the bracketed tags and explain them once in chapter 02; keep them but use them more sparingly; replace them with plain English in the prose; drop the distinction entirely.

**Decision.**
Write the standing into the sentence, in chapter 05.
`` `(ours)` `` on the three-claims table became "Splitting them this way is this book's, not standard vocabulary."
`` `(established)` Parnas, 1972 `` became "Parnas, 1972 — the founding paper, and still the clearest statement."
`` `(established)` `` on Hyrum's Law became "The name comes from Hyrum Wright at Google; the observation is standard and uncontroversial."

**Why.**
The author's reading is correct, and the reason is one the book already argues in chapter 02: a marker the reader must decode before the sentence means anything is a cost, and this one earns nothing back.
`(established)` in front of a dated citation is redundant — *Parnas, 1972* already is the provenance, stated in the form scholarship uses.

The tags also fail differently in the two directions they are meant to work.
Where a claim is genuinely contested or genuinely this book's, one clause of plain English says so *and* says how, which the tag cannot: "not standard vocabulary" tells the reader what to expect when they search for the term, where `(ours)` only tells them a category.
Where a claim is standard, the tag adds a decoding step to a sentence that was not in doubt.

This is the same argument as decision 3, which removed numbering from the five kinds on the grounds that a name is self-describing at the point of use and an index is not.
Applying it to provenance markers is consistent rather than novel.

**Open.** *(Resolved by decision 13, which removed the notation entirely.)*
`README.md` and `CLAUDE.md` still document the bracketed form, and chapter 02 still uses it in two places.
Reconciling them is the author's call: either the marker convention is replaced book-wide with the prose form, or chapter 05 is the exception and the rule stands.
Nothing was changed in those files, because the convention is a structural decision and this entry records only what was done to one chapter.

**Consequence.**
No bracketed markers remain in chapter 05.
If the prose form is adopted book-wide, `README.md`'s "Provenance markers" section and `CLAUDE.md`'s equivalent are the two places to edit, and chapter 02 has two occurrences.

---

## 12. Chapter 05 revised against the author's first content review

**Date.** 2026-08-05

**Context.**
Chapter 05 was drafted and committed, then reviewed by the author in one pass of seventeen comments.
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
That is the ledger working as decision 7 intended: the additions were entered at the point the chapter claimed them, so chapters 09, 13, 16, 17, and 18 now have explicit boundaries against material they would otherwise have re-derived.

**Worth recording about the process.**
Every one of the seventeen comments identified something real; none was rejected on the merits.
Two of the three groups are failure modes specific to generated prose — asserting a conclusion in the register of having argued it, and compressing a correct idea until it stops parsing — and both survived a full self-review pass before the author saw them.
The README's claim that the drafts are read and sent back is doing real work here, and this is the largest single instance of it so far.

---

## 13. Provenance markers removed entirely

**Date.** 2026-08-08

**Context.**
Decision 11 left the marker convention half-applied: chapter 05 stated provenance in prose, while `README.md` and `CLAUDE.md` still documented `(established)` / `(contested)` / `(ours)`, and chapter 02 and the TOC still used them.

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
`02_the-five-levels.md`'s epigraph now reads "the book's own framework, not standard terminology you will find elsewhere under these names."
`00_toc.md`'s chapter 17 summary now states the actual dispute — that the controlled studies disagree with each other and mostly measure test-first against no tests rather than against test-after — which is more informative than the tag it replaced and is the pattern the rest of the book should follow.

No markers remain anywhere in the book or its instructions.
The occurrences in this log are historical record and stay as written.

---

## 14. Chapter 05, second review: three reframings and a reversal

**Date.** 2026-08-08

**Context.**
The author's second pass over chapter 05 ran to fourteen comments, worked in four batches with a commit between each. Two batches were corrections of fact and structure; two were conceptual.

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
Chapter 05 is 857 lines, from 375 before the first review. `LEDGER.md` gained four concept rows, lost the reversed escape-hatch row, and had five rows corrected where the chapter had moved beneath them.

Worth recording about the process: of fourteen comments, one was a factual error in a shipped commit, two were sentences that did not parse, three were conceptual framings where the author's version was simply better than the draft's, and one reversed a decision this log had already recorded as settled. The failure modes are consistent with the first review — asserting rather than showing, and compressing until meaning is lost — with one new one: **verifying a claim by asserting it confidently.** The Python example was never run. It is now, along with the CommonJS and Go examples that replaced parts of it.

---

## 15. Chapter 03: a Force is a dial, not a switch

**Date.** 2026-08-09

**Context.**
The TOC lists seven Forces for chapter 03 and asks for "a code demo of the same problem solved differently under different values of it."
Chapter 02 had already established what a Force *is* — a property of the situation rather than advice, acting differently on Laws than on Principles — so 03 needed something beyond a catalogue, or it would be seven definitions and a table.

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

Chapter 03 runs 381 lines, the shortest of the three drafted so far, which suits a chapter whose job is to supply vocabulary the rest of the book spends.

---

## 16. Chapter 04: one grade, one move

**Date.** 2026-08-09

**Context.**
Chapter 04's difficulty is structural rather than editorial: it grades material that other chapters own. CAP belongs to 07, Conway to 09, the memory hierarchy to 08, acyclic dependency to 05, Hyrum's Law to 05. Written straight, the chapter becomes a tour of other chapters' examples with a letter attached to each.

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

Grade B uses a cache read once at startup. Chapter 02 lists "a cache needs an invalidation strategy" in its table of classified claims but nothing owns the argument, so 04 takes it. The point is the escape: if the original is a compile-time constant there is no cache in the strict sense, so the Law is true and inert.

Grade C uses Go's randomized map iteration against Python's guaranteed dictionary order — one observation, two opposite responses, verified by running both. It carries something the other grades cannot: Python's dict order began as an implementation detail, became widely depended upon, and was promoted to a guarantee in 3.7. The empirical claim's own prediction changed the thing it predicted, which is only possible for a Grade C.

**A distinction the chapter adds.**
The TOC asked what makes Conway's Law different from "prefer composition over inheritance." The answer turned out to be one line worth keeping: **a Law describes; a Principle prescribes.** Conway's Law cannot be bad advice because it is not advice. That separates the two faster than arguing about how universal either feels, and it gives chapter 02's classification test a sharper edge for this one boundary.

**The boundary section leads with the chapter's own misuse.**
*Grade is not importance.* Amdahl's Law is Grade A and irrelevant to a single-threaded tool; the cache-to-memory gap is Grade C, drifting, machine-dependent, and decides a game engine's whole architecture. Reading the grades as a priority ranking commits the error the book is about — treating a firm claim as an important one — using the book's own vocabulary to do it.

**Consequence.**
`LEDGER.md` gains five concept rows and three example rows.
Chapter 05's existing commitments are honoured: acyclic dependency stays Grade B, and Hyrum's Law stays an empirical regularity rather than a theorem.
Chapter 04 runs 206 lines, the shortest so far, which suits a chapter whose job is a distinction rather than a subject.

---

## 17. The A/B/C grading is dropped; the three kinds are named

**Date.** 2026-08-10

**Context.**
Chapter 04 was drafted with the TOC's A/B/C grading — Grade A a proven theorem, Grade B a near-tautology, Grade C an empirical constant.
Reviewing it, the author proposed two changes: refer to the kinds by name rather than by letter, and consider abandoning the grading concept entirely, on the grounds that grading implies a hierarchy nobody can justify — *I don't see why a theorem comes before tautology*.

**Options.**
Keep the letters with the names alongside; keep the letters and defend the ordering; drop the letters and name the kinds.

**Decision.**
Drop the grading. The kinds are **theorem**, **definition**, and **empirical law**, named at every use, in no order.
The chapter's title changes from *Grading a Law* to *Three Kinds of True*.

**Why.**
The author's objection is correct, and the decisive support for it is that **this book already decided this question, in decision 3, and chapter 04 contradicted it.**

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
`00_toc.md` gains the new chapter title and loses "Grade A theorems" from chapter 07's entry.
`05_structure.md`'s three-claims table now reads "true by definition (Ch. 04)" rather than "near-tautology, Grade B."
`LEDGER.md` has seven rows reworded and one added, for the regularity-versus-magnitude distinction.
`CLAUDE.md` gains a rule the author asked for directly: **write Go for a reader who does not know Go**, since the audience is fluent in Java, C#, or Python, and an unglossed `chan` spends the example.

---

## 18. A theorem admits two escapes, not one; CAP replaced by the halting problem

**Date.** 2026-08-10

**Context.**
The author's second pass on chapter 04 raised three things. One was a question about which assumptions the worked example was talking about. Answering it exposed an error in the chapter's central framing.

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
`00_toc.md`'s chapter 04 entry names the actual examples; CAP stays with chapter 07, which owns it.
`LEDGER.md` gains a row for the two escapes and one for the halting problem, and loses the CAP row.
Chapter 04 runs 259 lines.

---

## 19. Chapter 06: two halves, one claim

**Date.** 2026-08-10

**Context.**
The TOC gives chapter 06 seven topics across what look like two subjects — check-then-act, races, lock-holders, single-writer, clock skew, Lamport and vector clocks, coordination latency. Written as a list it is two chapters sharing a file.

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
`LEDGER.md` gains eleven concept rows and five example rows; chapter 06 was previously carrying two.
Six forward references from chapters 02, 03, and 05 are now discharged.
Chapter 06 runs 288 lines and moves to **in progress**.

---

## 20. Chapter 06 pairs every break with its repair

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
Chapter 06 runs 393 lines, up from 288.
`LEDGER.md` gains four concept rows and four example rows.
The atomic fix moved out of *Only the lock-holder can enforce*, which now generalizes the same move to the multi-process case rather than introducing it.

---

## 21. Two examples in chapter 06 were contrived; both replaced

**Date.** 2026-08-10

**Context.**
The author's second pass on chapter 06 rejected two demonstrations. Both objections were about the same failure: the code was arranged to produce a result rather than to be a thing anyone would write.

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
Chapter 06 runs 425 lines.
`LEDGER.md` has two example rows rewritten.
Both replacements were run before they went in, along with the attacker process for the symlink swap.

---

## 22. Chapter 07 leads with the root fact, not the theorem list

**Date.** 2026-08-10

**Context.**
The TOC gives chapter 07 six topics: CAP, PACELC, FLP, Two Generals, timeouts as guesses, p^N, plus the outbox and saga patterns. Written as a survey it is a reference card, and the reader leaves knowing three acronyms rather than one thing.

**Decision.**
Lead with the fact the theorems are consequences of:

> **You cannot tell a slow machine from a dead one.**

Two Generals, FLP, and CAP then arrive as three formalizations of one predicament — a lost message and a slow message look identical, a crashed process and a paused one look identical, a partitioned peer and a dead peer look identical. **The impossibility is always that you must act on information you cannot obtain.**

`p^N` is deliberately kept outside that unification and named as the other kind of fact, because it is arithmetic about independent events rather than a limit on knowledge. Folding it in would have been tidier and false.

**The theorems are presented by their assumptions rather than their proofs**, following chapter 04: the assumptions are the only negotiable part. FLP is stated with the consequence that matters — Raft and Paxos do not evade it, they add timeouts, giving up guaranteed termination to keep guaranteed safety. CAP is stated once and then set aside for PACELC, because the else-branch applies every day and CAP's branch only during an outage.

**Chapter 06's review shaped the structure.**
Two lessons carried forward without being asked for.

The boundary section moved to the **front**, as *When any of this applies to you*, because chapter 06 established that a qualification arriving after the alarm does not undo it. This chapter needed it more: distributed-systems machinery is imported into single-database systems constantly, and a reader who meets four impossibility results before being told none of them binds will import them again.

Every failure is **paired with its repair, adjacent** — four pairs, all run. The retry that charges three times against the idempotency key that charges once; the order that commits while the event is lost against the outbox that makes it one write.

**The check offered for the boundary** is deliberately not "is this a microservice." It is *can one part be alive while another part cannot reach it?* A deployment diagram does not answer that; a shared process and connection does.

**One thing the chapter says that is easy to get backwards.**
Distributed transactions are not impossible. Two-phase commit works and is used. What it costs is availability — a participant failing while holding a prepared transaction blocks the others — and for most systems that is a worse outcome than the inconsistency being avoided. Saying "you cannot have cross-system atomicity" would have been simpler and wrong, and it would have made the boundary section dishonest.

**Consequence.**
`LEDGER.md` gains ten concept rows and four example rows.
Debts from chapters 02, 03, 04, and 06 are discharged: exactly-once impossibility, why redelivery cannot be eliminated, and what idempotency is for.
Chapter 07 runs 262 lines and moves to **in progress**.

---

## 23. Verification code is not example code

**Date.** 2026-08-11

**Context.**
The author's review of chapter 07 identified a recurring failure and asked for it to be written into `CLAUDE.md`:

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
It is a distinct failure from the one decision 14 recorded. That rule says *run the code*; this one says *the thing you ran and the thing you print are two artifacts with different readers*. Following decision 14 exactly — as chapter 07 did — still produces this defect, because a verified harness is verified.

**A second rule, also requested.**
Expand an abbreviation on first use unless an experienced engineer would produce the long form without hesitating. `API` and `SQL` need nothing; `FLP`, `2PC`, `PACELC`, `TOCTOU`, `CQRS` get one expansion at first appearance. Where the name is initials of people, say so — FLP is Fischer, Lynch, and Paterson — because that is what the reader needs in order to search for it.

**Two substantive corrections in the same pass.**

The author flagged *reliability multiplies* as reading like a paradox, since multiplying reliability sounds like more of it. They were right that the sentence inverts its own meaning. It now reads **availabilities multiply, and every one of them is less than one**, with the section retitled *Availability is a product, not an average* and a paragraph on why the intuition fails — people average, and availability does not average because every dependency must be up at the same time.

They also asked where the transaction was in the outbox example, since only a comment claimed one, and whether `drain` had a transaction. Both were fair: the sample used Go slices with a comment asserting atomicity. It is now real `BeginTx`/`Commit` code with the two inserts inside it. And `drain` deliberately has **no** transaction spanning the publish and the delete, which the chapter now explains as the same impossibility one level down — publish-then-delete gives at-least-once, delete-then-publish gives at-most-once, and only the first is recoverable.

**Consequence.**
`CLAUDE.md` gains the verification-versus-example rule and the abbreviation rule.
`LEDGER.md` gains a row for publish-then-delete and one reworded for availability.
Chapter 07 runs 320 lines, up from 262.

---

## 24. AI material: distributed, not a chapter — and grilling goes to chapter 19

**Date.** 2026-08-12

**Context.**
The author proposed a new chapter on AI-assisted development, reasoning that generated code and generated design amplify the failure modes the book catalogues, that models sound authoritative regardless of a claim's standing, and that they cannot see what is in your head.

**Is there something real.**
Yes, and it is more specific than amplification. Four findings, each an instance of a mechanism the book already owns:

- **The training corpus is a monoculture.** Chapter 02 names monoculture as the single most common source of confusion and prescribes one cure — work in a second ecosystem until its conventions stop feeling wrong. That cure is structurally unavailable to a model, which has one distribution and no way to acquire another.
- **The generator cannot see your Forces**, so chapter 03's groundwork is skipped by construction rather than by carelessness.
- **Uniform confidence across all five kinds**, which is chapter 02's first mechanism with a single generator behind it.
- **The team-size Force at its limit** — a contributor present for no conversation, retaining nothing between sessions, producing at a rate no review process was sized for. Chapter 03's migration from comment to review habit to type system is forced harder and sooner.

**Decision — distribute, do not add a chapter.**
Every finding attaches to a concept another chapter owns, so a separate chapter would be six cross-references wearing a title.
The draft argued for a chapter on the grounds that it needs one organizing mechanism the way chapter 15 has one; testing that honestly, *the derivation never happened* explains the Forces finding and not the monoculture, confidence, or volume findings. There is no single mechanism, so there is no chapter.

The author raised distribution and the draft's own evidence undercut the draft's position, which is recorded here because the log is where a reversed recommendation belongs.

Distribution also ages better. A paragraph about a precondition failing survives model generations; a chapter titled for a technology is a dated object by construction.

**These are constraints, not a work queue.**
Five of the seven landing sites do not exist yet, so most of this material is blocked behind the ordinary drafting order and should not pull work forward.
The placements are recorded in `00_toc.md`'s contents lines and in `LEDGER.md`, because those are read when a chapter is drafted and this entry is not.
The two chapters already at draft — 02 and 03 — are listed under *Pending revisits* in the TOC.

**Decision — the synthesis goes in chapter 23, and grilling in chapter 19.**
Chapter 23's contents already list *receiving a blog post; a code review comment; a book; a colleague's strong opinion; your own past decisions.* Receiving generated code is the sixth item and the one the other five rehearse for.

Grilling is a method rather than a way of reading, so it belongs to chapter 19, the force-map method — it is that method run with a generator in the loop, and the interview is how the forces get read.

**A correction the author made, worth recording as such.**
The draft asked whether the book should take a position on whether to use these tools. The author's answer: usage is a fact, and the book does not take positions on facts.

That is the book's own model applied to the draft's question. Chapter 02 defines a Force as a property of the situation, *not negotiable by argument* — so the draft had misclassified a Force as a Principle while working on the chapter that defines the difference.

**A second correction, on what grilling is.**
The draft described grilling as a review technique — interrogating a draft after it exists, probing what the text does not say. That is the author's practice in *this* repo, the `[claude …]` tags, and the draft attached the wrong name to it.

Grilling happens **before** generation. It is an interview that walks the decision tree, puts each decision to the human with a recommended answer, and does not act until there is shared understanding.

The distinction matters more than a mislabelling, because it changes the failure mode being addressed. The draft had been writing that generated code presents an Idiom in the same voice as a Law. The author's framing is sharper:

> without "grilling", I would be building a system where I didn't know the trade-offs and important decisions and where a default "recommended" decision was silently made by the AI

**Generated code does not state its decisions at all.** It arrives with every branch already taken, and a taken branch leaves no mark — there is no confident sentence to be suspicious of, because there is no sentence. Review cannot reach that, since catching a silent default requires already suspecting the branch existed. Grilling makes the branch visible before anything is written.

It also resolves something chapter 03 leaves open. That chapter says a model cannot see your Forces, which leaves a reader unable to act: you cannot supply the Forces in a prompt without knowing which are about to matter. The interview inverts the flow — the model surfaces the decision, the human supplies the situational fact that settles it.

The load-bearing detail is the author's: *sometimes I choose an option that was not the recommended one.* The recommendation comes from the corpus, so overriding it is a local Force beating a majority convention — possible only because the convention was made visible as a choice rather than delivered as code. FlowCore's decision 18 is the artifact of exactly that: short Go names were a corpus default that lost to a local Force once it was on the table.

**The limit, which the chapter must state.**
Grilling surfaces the decisions the model recognizes *as* decisions, and that set comes from the same corpus. A question settled uniformly across the training data does not present itself as a branch point; it is simply how things are done.

So **grilling is weakest exactly where the monoculture is strongest** — it surfaces contested choices and hides settled ones, and settled-in-the-corpus is the class most likely to be wrong outside the ecosystem it came from. This follows from chapter 02's mechanism rather than from measurement and must be stated as reasoning, not as a finding.

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

## 25. Chapter 08 organizes by shape, and reports two measurements that contradicted the plan

**Date.** 2026-08-12

**Context.**
The TOC gives chapter 08 seven topics: Amdahl, the Universal Scalability Law, Little's Law, queueing and "why 85% utilization is a cliff," the memory hierarchy with an array-of-structs benchmark, the speed of light, and big-O against constants. Written as a list it is a formula sheet.

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

That makes the widely repeated *use a slice under about twenty items* a magnitude quoted without its conditions — chapter 04's exact failure, arriving unprompted in the material. The boundary section is stronger for the demonstration having failed than it would have been had it worked.

**Provenance for the measurements.**
Every number was measured on the machine the chapter was written on — an Apple M4, Go 1.26.5 — and a section before the demonstration says so, with the reason: the regularity holds everywhere and the magnitude is local, so the formulas are exact and the numbers are an instance. That is chapter 04's regularity-versus-magnitude distinction applied to the chapter's own evidence.

The AoS/SoA benchmark uses an 80-byte struct against a 64-byte cache line and shows 4.3× from field layout alone, discharging chapter 05's deferral of the arithmetic and chapter 03's latency-Force pointer.

**Consequence.**
`LEDGER.md` gains nine concept rows and four example rows.
Chapter 08 runs 280 lines and moves to **in progress**.

---

## 26. Chapter 08 rewritten: jargon, a repeated example, and a prose tic

**Date.** 2026-08-12

**Context.**
The author's review of chapter 08 ran to fourteen tags and included the judgement that a rewrite might be warranted. It was. The tags were not local wording problems — three systemic faults ran through the whole chapter.

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
The chapter reused chapter 05's `Particle` struct for the memory-layout benchmark. The ledger had split the two — 05 owns the encapsulation argument, 08 owns the arithmetic — but using the same struct made it read as the same example twice.

The author's rule, which is worth keeping: if two chapters share a *shape*, keep the shape and change the example, so it does not land as "oh, the particle thing again."

Replaced with summing one field across two million order records, which is the book's running domain (orders appear in chapters 03 and 07) and gives a **7.1×** difference against a 120-byte record. It also connects outward: this is why analytics databases store columns rather than rows.

**A prose tic, and a new rule.**
The author flagged two paragraphs as *"the pinnacle"* of an AI prose style and asked for a `CLAUDE.md` entry against it.

The pattern is every paragraph landing on a closing turn — setup, pivot, epigram. Fine once; run for forty paragraphs it becomes a rhythm the reader hears instead of the argument. `CLAUDE.md` gains *Vary the cadence* under the register section, naming five tells: a closing clause beginning "which is why," the *it is not X, it is Y* construction, announcing a count before delivering it, a final sentence engineered to be quotable, and the rule of three.

The instruction is not to delete every turn but to **let most paragraphs end flat**, keeping one where the argument genuinely turns. The rewritten chapter uses "which is why" once, down from four.

**Also corrected.**
The epigraph said *grades*, which decision 17 replaced with *kinds* — a regression against a recorded decision, caught by the author.

**Consequence.**
Chapter 08 runs 338 lines, up from 280, almost entirely in definitions and worked setup.
`LEDGER.md` has one example row replaced and three added.

---

## 27. Chapter 09 organizes by rate of change, and grades Lehman honestly

**Date.** 2026-08-12

**Context.**
Chapter 09 covers Lehman's laws, Conway's Law and the inverse manoeuvre, Brooks's Law, and compatibility. Four results from four different literatures, with no obvious connection beyond operating on long timescales.

**Decision.**
Organize by **rate of change**: code changes daily, schemas monthly, published interfaces rarely and never backwards, organizations yearly and expensively. The claim follows — everything changes, but not at the same rate, and the slow parts set the terms for the fast ones.

That gives the chapter a usable test (*which layer does this decision land in?*) and puts the four laws in an order that explains itself. It also keeps clear of chapter 03, which owns durability as a **Force** — 03 asks whether a mistake stays correctable, 09 asks what governs change across years and adds the organization, which 03 does not cover.

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

This follows chapter 04's empirical-law framing applied to the book's own sources: an empirical law carries a study population, and citing all eight equally would repeat the error the book exists to describe.

The same treatment is given to the inverse Conway manoeuvre. Conway's observation is established; the claim that architecture can be driven by reshaping teams is a strategy rather than a finding, and the chapter says so.

**Two things the chapter adds that were not in the TOC.**

*Lehman's ratchet has a mechanism.* Complexity rises because the costs are asymmetric: adding a case is cheap and local, removing one requires establishing that nothing depends on it. Additions happen continuously; removals need a project.

*One constraint here is unlike everything else in the book.* Every other law can be satisfied by changing code you control. Compatibility cannot, because **you cannot deploy other people's software** — the code that must change is on a machine you cannot reach, owned by someone with no reason to hurry.

**Consequence.**
`LEDGER.md` gains seven concept rows and three example rows.
Part II is complete: chapters 04 through 09 are drafted.
Chapter 09 runs 219 lines and moves to **in progress**.
