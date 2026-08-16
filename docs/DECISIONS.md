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

---

## 28. Conway's mechanism corrected, and Brooks given its actual condition

**Date.** 2026-08-12

**Context.**
The author's review of chapter 09 raised eight points. Two were challenges to the substance, and both found real defects.

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

The ramp-up figures are marked illustrative rather than measured, with the note that substituting your own moves the break-even — which is the reason to compute it rather than quote it (Ch. 04).

**An expansion the author asked for, and the ledger allowed.**
They asked whether one-team-per-service deserved treatment here. Nothing else in `LEDGER.md` owns organizational structure, so it landed in 09.

The section states the heuristic's real content and the two ways it is misapplied: many services owned by one team is fine, one service owned by many teams is the failure it prevents, and services sized to the team chart is the failure it causes. The honest form is that it constrains **who may own a service**, not **how many services there should be**.

**Smaller corrections.**
A sentence reading as an instruction to the writer — *cite the two, treat the rest as observations of their era* — was removed. Go struct tags are now explained, with the Java and C# equivalents, which is the audience rule applied in a chapter drafted after that rule was added. And the demonstration now says the server sends the new shape in every case and the output is what the client makes of it, since the draft said "reaches" while the output said "parsed."

**Consequence.**
Chapter 09 runs 278 lines, up from 219.
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
Chapter 09 runs 289 lines.

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
Chapter 09 runs 301 lines.
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
Chapter 09 runs 311 lines.

---

## 32. Read the source before explaining why someone else's result holds

**Date.** 2026-08-12

**Context.**
Chapter 09 explained Conway's Law twice without reading Conway, and the author asked for a rule that would prevent it.

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
Chapter 10 opens Part III and has to say what the two tests are testing. The book's model classifies claims into five kinds, and the obvious move was to ask which kind a pattern is.

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

Two things from that document are deliberately left alone: *anemic domain model* as a term that smuggles a verdict belongs to chapter 14, and *does the idea come with the conditions under which it's wrong* belongs to chapter 15.

**Consequence.**
`LEDGER.md` gains six concept rows and two example rows.
Chapter 10 runs 181 lines and moves to **in progress**.

---

## 34. The teaching boundary does not survive, and is replaced

**Date.** 2026-08-12

**Context.**
The TOC promised chapter 10 a boundary at teaching: *a name with low information content is still a useful handle for a beginner.* The draft wrote it that way. The author rejected the argument:

> what can you realistically teach with a name that doesn't compress and doesn't forbid? This is a facade. Ok so what? […] in fact most of the times it clouds the learning because the reasons — principles behind that shape is not identified. […] Then you never encounter that particular requirement in real life and you forget the pattern even exists.

**Decision.**
The objection holds and the boundary is removed.

Attempts to steelman it all collapse into a boundary the chapter already had. The strongest version — that a name gives a learner something to recognize the shape by later — fails on the author's point that recognition without the reason is not usable knowledge: you can identify a Facade and still not know when a simplified interface is the right move, what it costs, or how to design a good one.

What survives is narrower and is folded into the *search* boundary: a name a learner can look up is a door into the discussion of when the shape fails, and a name without that discussion attached is a sound they can make in a meeting. The chapter now says the widely assumed opposite is wrong, and connects the failure to chapter 15's mechanism — a compressed judgement, repeated without its conditions, becomes a slogan.

**The replacement boundary is the author's, from a separate note.**
Commenting on *naming precisely costs more than naming vaguely*, they added that a vague name is sometimes the right move because the design is not mature enough to decide, and that waiting for a little more functionality often turns four awkward things into three natural ones.

That is a genuine counter-example to the chapter's claim, and a better one than teaching: **the two tests assume you can say what the code does.** Before that is true, a precise name is a claim you have not earned. The chapter states the failure precisely — not the vague name, but losing track that it is provisional — and borrows chapter 03's device for any deferred decision: write down what would have to become true for the name to be settled.

**Two smaller corrections.**
The constraint demonstrations now show what each name *permits* before what it forbids, at the author's suggestion, which makes the forbidden case legible rather than requiring the reader to infer the permitted one.

And the failure list's `strategies/` entry now carries its reason, which the author could see was a failure but not articulate: **a directory should group things that change together, while a pattern name groups things that are shaped alike.** So every feature change reaches into a folder holding other features' code.

**Consequence.**
`00_toc.md`'s boundary line for chapter 10 is rewritten, since the promised boundary is gone. The TOC now names the three that survive.
`LEDGER.md` gains two concept rows and one reworded.
Chapter 10 runs 202 lines.

---

## 35. The scale test's axis is ownership, not size

**Date.** 2026-08-12

**Context.**
The TOC frames chapter 11 around scale: the same name is trivial at class scale and load-bearing at system scale, with Adapter becoming an Anti-Corruption Layer. Written literally, "scale" means size, which is wrong in a way that would have made the chapter unusable — a fifty-line integration with a vendor is system scale, and a thousand-line internal refactor is not.

**Decision.**
State the axis as **ownership**: can you change the other side?

Class scale means both sides are yours — same repository, same deploy — so if two things do not fit you may change either. System scale means one side is not yours to edit: a vendor's API, another team's service, a published format.

That reframing does three things the size framing cannot. It explains why a small integration is a serious commitment and a large refactor is not. It connects the chapter to material the book already owns — chapter 03's control-of-the-callers Force and chapter 09's *you cannot deploy other people's software*. And it produces the diagnostic the chapter ends on, which is a question with an answer rather than a judgement call.

**The insight that carries the demonstration.**
What makes Adapter cheap at class scale is not the line count. It is that **a third option exists**: change the other side so no adapter is needed. Rename the method, change the signature, move the parameter.

At system scale that option is gone, and the pattern stops being one fix among several and becomes the only move. That is the whole difference, and it is why the same word denotes a convenience in one place and a maintained translation layer in the other.

**What the scale table is actually tracking.**
Drafting the table showed that the second column is not "the same thing but bigger." Every entry acquires a **failure mode** that the class-scale version does not have — the vendor changes without asking, the surface becomes a commitment, delivery can fail or repeat, the call can be slow or partial.

Those are Part II's Laws arriving one at a time. So the table's last column names them, and the chapter can say what it is really about: a pattern name transfers the shape and drops the Forces, and the Forces were the expensive half. That is chapter 02's mechanism — advice stripped of its conditions — in a new place.

**Both demonstrations were run.**
Go's structural typing satisfying `querier` with two vendor types and zero wrapper code, against the C# shape that needs a class and two forwarding methods per type. And the Stripe status leaking into three call sites versus stopping at one translation function, with the counts taken from the file rather than asserted.

**A question chapter 10 left open is answered here.**
Chapter 10 used Facade to show that compression and constraint are independent — it compresses well and forbids nothing — and handed the scale question forward. The answer: at class scale a facade is a word for a wrapper; at system scale it is what other teams call, so chapter 09's compatibility rule applies and it may be added to but never narrowed. The name did not change; the commitment did.

**The boundary section found a genuine asymmetry.**
The TOC asked for patterns trivial at every scale. The test that works is whether you can state the system-scale version at all — Strategy and Template Method have none, because nothing about passing a function becomes unreliable when the program grows.

Singleton turns out to do the opposite, and is worth the contrast: at system scale "exactly one" means one across a cluster, which is leader election, which needs consensus. It does not stay trivial; it becomes one of the hardest items on the list under an unchanged name.

**Consequence.**
`LEDGER.md` gains six concept rows and two example rows.
Chapter 11 runs 222 lines and moves to **in progress**.

---

## 36. Chapter 11 fought its own vocabulary; the word "scale" is now the thing being corrected

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

The title stays. *The Scale Test* now names the received framing the chapter examines, which is the same move chapter 05 makes with "layered architecture" — worth flagging to the author as reversible if they would rather the title matched the conclusion.

**One running example, replacing two borrowed ones.**
The author objected that the `querier` demonstration had already been used repeatedly — it appears nine times in chapter 05 — and suggested one coherent example carrying the whole chapter, sketching it as *we own FastSell and have our own payment processor, then we switch to Stripe*.

Adopted as sketched. FastSell's own `Receipt` and `LedgerEntry` for the owned case, then the same problem after moving to Stripe. That is better than two static examples because it shows **the transition** — the moment an option disappears — rather than two unrelated states, and the pattern's shape is identical on both sides of it, which is the chapter's whole point.

**The third option is now shown rather than asserted**, at the author's request. The owned case gives the adapter, then gives the better answer as code: rename two fields in `payments.Receipt` and delete the adapter. Seeing the alternative is what makes its later absence land.

**Counts taken mechanically.** Six sites test Stripe's vocabulary without a boundary, one with. Both versions were run and produce identical output, which is worth having — the boundary costs nothing functionally, so its whole value is what happens on the day the vendor changes.

**Consequence.**
`LEDGER.md` has five rows reworded and three examples replaced.
Chapter 11 stays at 222 lines; almost all of it is different.

---

## 37. Chapter 11's axis is chapter 03's Force, and the pattern table is graded

**Date.** 2026-08-14

**Context.**
Sixteen review notes. Three of them were challenges to whether the chapter was sound rather than to how it read, and answering those changed the chapter's relationship to the rest of the book.

**The axis was already in the book, and the chapter had not noticed.**
The author asked whether *can I change the other side* is one of the seven Forces, and if so which.

It is. Chapter 03's **control of the callers** asks whether you can change everyone who calls you; chapter 11 asks whether you can change what you call. Same Force, same three settings, pointed the other way — which the chapter now says explicitly rather than presenting the axis as new.

The same oversight produced the repetition the author flagged separately. The *partial ownership* boundary had re-derived chapter 03's middle setting — *you can see them but not change them* — in fresh words, which is precisely what `LEDGER.md` exists to prevent. It now cites 03 for the three settings and spends its space on what the middle one does to the pattern question: a temporary forwarding method with a removal date, which is neither an adapter nor a permanent translation layer.

**The pattern table is now graded rather than asserted.**
The author asked whether the table was solid or this book's theory, and separately whether a message bus is really Observer with a network in it or only a surface resemblance.

Checked row by row, and they are not equally supported:

- **Proxy** is canonical. The Gang of Four list a *remote proxy* — "a local representative for an object in a different address space" — among the pattern's named variants. Crossing the line was in the original definition.
- **Adapter** is supported by the anti-corruption layer literature; Evans describes such a layer as containing translators.
- **Facade** is this book's extension, and is marked as such. No catalogue says a facade becomes a public API.
- **Observer is the weakest, and the author's suspicion was right.** A broker is genuinely new structure, and the publisher stops holding references to its subscribers — a change in mechanism, not only in what can fail. The chapter now calls it a family resemblance rather than the same pattern relocated.

Grading the rows turned out to strengthen the chapter rather than weaken it, because the distribution is informative: **the rows that survive best are the ones where nothing structural is added.** That is a condition on when this reading applies at all, and it was not visible while every row was asserted equally.

**Singleton expanded, at the author's request.**
Their question was what invariant ties one object in one process to consensus across machines, given that a cluster obviously *has* many machines. The answer needed stating: the singleton is in the **role**, not the hardware — exactly one machine running the billing job while the others stand ready. The shared invariant is *at most one holder at a time, and everyone agrees which one*, and both halves are free in one process and expensive across machines, for reasons chapter 07 owns.

**A claim that was simply wrong.**
The draft said a ten-thousand-line refactor is not a serious commitment. The author rejected that, correctly. The point being reached for was about *kinds* of expense: a large refactor is a large piece of work that ends, while a small integration is a standing obligation that does not. Rewritten to say that.

**Title.**
Changed by the author to *Patterns That Cross The Line*, on the grounds that chapter 08 is already called *Scale* and using the word here is confusing when the chapter argues it is the wrong word. Kept, with the TOC entry, the ledger row, and chapter 10's two forward references updated to match.

**Consequence.**
Chapter 11 runs 302 lines, up from 222, almost all of it in the graded table, the Singleton expansion, and worked code for the facade and partial-ownership cases the author asked to see rather than be told about.

---

## 38. Reviewing the author's edits found a real imprecision in the facade example

**Date.** 2026-08-14

**Context.**
The author's third pass on chapter 11 was direct edits only, with no tags, plus a file rename. They asked for the edits to be reviewed rather than absorbed.

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
The file was renamed `11_the-scale-test.md` → `11_patterns-that-cross.md`. Two references in `00_toc.md` still pointed at the old name and are updated.

**Worth recording about process.**
The instruction was a reminder: *always check my direct edits as well.* This pass is why the rule exists — one of five edits contained a correction the draft would have absorbed silently, and following it through produced a better example than either version had.

---

## 39. Chapter 12 is not a catalogue

**Date.** 2026-08-14

**Context.**
The TOC planned chapter 12 as a graded catalogue: roughly sixty patterns, each with a definition, the constraint it imposes, a code demo, and its Force. Drafting it as specified would have produced four problems at once.

It **re-covers owned material** — the Outbox, Saga, and Idempotency Key are chapter 07's; the Anti-Corruption Layer is 11's; Transaction Script is 10's compression example; the test-double taxonomy is 17's; data-oriented layout is 05's and 08's. A catalogue explains them again, which is what `LEDGER.md` exists to prevent.

It **has no claim.** The rubric requires one sentence the chapter demonstrates, and sixty entries have sixty. The TOC's own boundary line conceded it: *each entry carries its own boundary* is not a boundary section.

It **undercuts chapter 10**, which argues that a name earns its place by compressing and ruling something out. Listing sixty names without applying those tests contradicts the chapter two before it.

And it **overlaps chapter 13**, which owns *if it disappears when you change language, it was a workaround*. The catalogue as planned is the positive cases of that same test.

**Decision.**
Keep the material and replace the organizing idea. The claim is that **the patterns which last are answers to Forces, and grouping them by Force finds the name from the situation** — the direction that is actually useful, and the one a catalogue organized by shape cannot serve, since it can only be searched by a name you already have.

**The coverage question, put to the author.**
The first proposal had two or three exemplars per Force, about fifteen patterns. They asked whether that meant all the patterns or a select few, which surfaced the real objection: a reader can reply *you picked the ones that fit your grouping*.

Resolved by splitting the entries in two. **Worked** entries — two per Force, with code, constraint, and cost — carry the argument. **Listed** entries — the rest of each family, one line each — are placed rather than explained, and their job is evidence: if fifty patterns sort into six Forces, the grouping covers the field rather than the chosen cases. Patterns another chapter owns appear with a pointer instead of a definition.

**The sort was done before the chapter was written, and produced the boundary section.**
Forty-three patterns fall into six Forces. Seven refuse, and they fail in two distinct ways, which is more useful than a tidy result would have been.

Some answer a **goal** rather than a situation — golden tests, property-based testing, the test-double taxonomy, functional core / imperative shell. All answer *how will I know this works*, which is something you want, not a fact about where you are standing. Chapter 03 is explicit that a Force is not negotiable by argument; testability is.

Some answer the **shape of the problem** rather than the situation. A state machine is right when the domain has states and transitions, which is a fact about the business. Transaction Script is what you write when no Force pushes you anywhere else.

So the chapter's claim is stated in its narrower true form, and the boundary section names the three-way distinction — Force, goal, problem shape — as one way people end up applying machinery to a question they were not asking.

**Verification.**
Most entries are structural, which needs no run. The one behavioural claim was measured: at a millisecond per round trip, a thousand rows takes 1,145 ms one call at a time and 11 ms in batches of a hundred.

**Consequence.**
`00_toc.md`'s entry for chapter 12 is rewritten, since the planned chapter no longer describes this one.
`LEDGER.md` gains four concept rows and six example rows.
Chapter 12 runs 385 lines, the longest so far, against 600–900 for the catalogue it replaces.

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

Checked before deleting: eight of the eleven were already covered in their bodies. Chapter 06 states the definitional point at line 353, chapter 09 gives the study-population caveat inside the Lehman section, chapter 08 has an entire *About the numbers* section.

**Three needed relocating first**, and were.

Chapter 02's epigraph carried the only statement that the five-level model is this book's own rather than standard vocabulary — provenance that decision 13 requires be in the prose. It now sits in the claim section, with the addition that the reader should expect nothing when they search for the names, and should instead find the distinctions already familiar and only unnamed.

Chapter 07's carried the two escapes from a theorem as a bulleted list. Those are load-bearing: the chapter refers back to them, and the boundary section depends on them. Moved into the body before *When any of this applies to you*.

Chapter 10's carried a substantive argument — a pattern is not one of the five kinds, because the kinds classify claims and a name is not a claim. That is the question a reader arriving from Part II will actually ask, so it became a short named section immediately after the claim rather than a note before it.

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

More decisive than distance is what immediately precedes the heading, since a pronoun binds to its nearest antecedent. In chapter 05 the reader has just finished *Hyrum's Law*, so "Why it holds" reads as *why Hyrum's Law holds*. In chapter 12 they have just finished *Force six*. **That is the default reading rather than a risk**, which makes the author's experience the predictable one.

Chapter 05 supplies a sharper case: its claim is two claims joined by *and* — the dependency graph must be acyclic, and what a module makes observable is what it has committed to. "Why it holds" has no referent there even in principle.

**Decision.**
Change the headings, not only the rubric. Thirty-two headings across eleven chapters, plus the rubric in `CLAUDE.md` and `README.md`, the mandatory-boundary sentence in both, one `LEDGER.md` reference, and twenty-three boundary labels in `00_toc.md`.

*Cost of the claim* was reverted to **What the claim costs**, since items three and four are clauses and a noun phrase broke the parallel.

**On repetitiveness, which the author asked about directly.**
Not a problem, and for a reason specific to headings. Three `##` headings containing the same phrase are separated by 50 to 200 lines and encountered one at a time; the only place they appear adjacent is a table of contents, and there the repetition carries navigational information — it signals that the three sections interrogate one object, which is the fact the old headings concealed.

**What was deliberately not changed.**
`docs/DECISIONS.md` keeps the old names throughout. Entries are contemporaneous records of what was decided when, and rewriting them to match later terminology would falsify the log the README points at as evidence.

**A gap the sweep exposed.**
Chapter 02 has no *Why the claim holds* section at all — it has *Why the kinds get confused*, which serves a different purpose. Ten chapters have three rubric sections and 02 has two. Left alone for now, since the instruction was to make the headings uniform rather than to add a missing section, but it is a real omission in the chapter that introduces the model.

**Still open.**
Two `[claude …]` tags remain in `CLAUDE.md`, on the *five levels* heading: what the five are five *of*, and whether the book has drifted from *level* to *kind*. Both are unresolved pending the author's decision, and the tags are left in place rather than removed, because the questions are live.

---

## 42. Four levels, five kinds

**Date.** 2026-08-14

**Context.**
The author queried the `CLAUDE.md` heading *The five levels* on two grounds: five levels **of what**, given that Force is not advice; and whether the book had drifted from *level* to *kind* without the structural labels following.

Both were right, and the first exposed a live contradiction in the book's foundational sentence. Chapter 02 opened with

> Every piece of software advice is one of five kinds

and said ten lines later

> The fifth, Force, is **not advice at all.**

**The count, measured.**

```text
 "five kinds"    15        "the kinds"    12
 "five levels"    9        "the levels"    0
```

Zero occurrences of *the levels* in prose is decisive: the drift had already happened everywhere except in structural labels — Part I's name, chapter 02's title and one heading, the README's spine heading, `CLAUDE.md`'s heading, and one `LEDGER.md` row.

**Decision.**
**Four levels, five kinds**, and the two words now mean different things rather than being synonyms.

The four levels are rungs on the ladder of authority: Law → Principle → Idiom → Style. Force is the fifth *kind* precisely because it is not on the ladder. So *level* is reserved for position, and *kind* for membership.

That also fixes the contradiction without weakening anything. The five classify **claims** — anything that can be true, false, or conditional — which is the answer chapter 10 had already reached independently while arguing that a pattern is not one of the five. Chapter 02's opening becomes *every claim you meet about software is one of five kinds*, which is true of Force as well as of the other four.

**This partly reverses decision 2**, which chose *Levels* over *Altitudes*. That decision's reasoning was plainness and consistency, and both now favour the change: *kind* is what the prose had already settled on, and *level* was being used for two things at once.

**Consequence.**
`02_the-five-levels.md` renamed to `02_the-five-kinds.md`, titled *The Five Kinds*, with a paragraph stating the four-and-five distinction where the ladder is introduced.
Part I renamed. The README's spine section renamed, with a sentence on why the counts differ. `CLAUDE.md`'s section renamed, now saying the five classify claims and reserving *level* for the ladder. `LEDGER.md`'s row rewritten. The five-level model becomes the five-kind model in both places `CLAUDE.md` names it.

Chapter 23's title, *Reading advice at the right level*, is deliberately left alone — that chapter is about placing advice on the ladder, which is what *level* now means.

---

## 43. Chapter 02 states a premise, not a claim

**Date.** 2026-08-14

**Context.**
The author raised three connected points about chapter 02. The heading *The five kinds* did not say five kinds of what. The rubric headings created a recursion — *where the claim doesn't apply* inside a chapter whose subject is kinds of claim. And a hypothesis: perhaps the chapter's opening is not a claim in this book's sense at all, which would explain the missing *Why the claim holds* section noted in decision 41.

They asked for the hypothesis to be tested rather than accepted: *to rule out that this is not a claim you should try to find satisfactory proofs for this chapter's claim and be unsuccessful.*

**The attempt, and its failure.**

*Derive the five from an exhaustive partition.* Split claims into descriptive and prescriptive; descriptive ones are about your situation (Force) or about computation (Law); prescriptive ones are conditional on situation (Principle), on ecosystem (Idiom), or on nothing (Style). It fails three ways. Evaluative claims — *this design is ugly* — are neither descriptive nor prescriptive, and Style absorbs them by fiat. The branches overlap: *don't write race conditions* is prescriptive in form and a Law in content. And claims about one program, or about the industry, fit nowhere.

*Exhaustive survey.* The chapter classifies twenty claims. That is evidence a taxonomy is useful; it is not proof that it is exhaustive, and the counter-examples above show it is not.

*Prove the second half.* "The kind determines how much authority it has" needs no proof: the kinds are **defined** by their authority. It is analytic, and there is nothing to demonstrate.

So the sentence has two halves and neither can be shown, for opposite reasons — one is true by construction and the other is an exhaustiveness claim that admits counter-examples. The author's hypothesis is correct.

**It also explains the gap.**
Decision 41 noted that chapter 02 has no *Why the claim holds* section and called it an omission. It is not. There is nothing to hold.

**Decision.**
Chapter 02's rubric headings change: *The claim* becomes **The premise**, *Where the claim doesn't apply* becomes **Where the model breaks down**, *What the claim costs* becomes **What the model costs**. A paragraph after the premise names both reasons it cannot be demonstrated and says why the chapter's headings differ from every other one's, so the deviation reads as deliberate rather than as an oversight.

This makes chapter 02 a deliberate exception to the uniformity decision 41 established, on the grounds that 02 defines the model while every other chapter applies it.

**Why not "axiom", which the author proposed.**
It is closer than *model* and still over-claims, for two reasons.

An axiom is posited without justification, and this chapter justifies itself — three worked demonstrations and twenty classified claims. Something offering evidence is not an axiom.

More seriously, it borrows mathematical authority the thing has not got. Chapter 04 grades claims as theorem, definition, or empirical law, and warns that folk versions drop quantifiers and conditions. *Axiom* sits adjacent to *theorem*, so using it would claim standing the model cannot support — in the chapter that defines the test for exactly that error. **Premise** keeps the derivation role and drops the over-claim.

It also echoes `README.md`'s own *The premise* section, where the book states the same idea informally; chapter 02 is that premise made precise, and the TOC entry now says so.

**Title.**
*The Five Kinds of Claim*, from the author, which answers "five kinds of what" permanently.

**Consequence.**
Prose uses of *the model* inside chapter 02 are left alone — by that point the chapter has defined the referent, and the overloading risk is in a heading a reader arrives at cold.

---

## 44. Chapter 12 uses chapter 03's Force names and order, which changed the sort

**Date.** 2026-08-14

**Context.**
The author's second review of chapter 12 made one point:

> we already named and listed forces on chapter 2. Follow the exact namings here in the chapter, then you don't have to say "this is … durability of medium" later. Also follow the exact order of forces used on that chapter unless there is a very good reason not to.

The draft had invented six group names — *something must survive*, *two things at once*, and so on — in an order of its own, and then annotated each with which chapter 03 Force it corresponded to. That is a fresh vocabulary for concepts the book had already named, which is the drift `LEDGER.md` exists to prevent, and it cost a line per section explaining the mapping.

**Decision.**
Use chapter 03's seven names, in chapter 03's order: concurrency, durability of the medium, blast radius, change frequency and its shape, team size and turnover, latency budget, control of the callers. The per-section translation lines are gone, since there is nothing left to translate.

**What that exposed.**
The invented list had six entries against chapter 03's seven, and the missing one was **team size and turnover**. That was not a considered omission — it was invisible while the labels were the draft's own, and it became obvious the moment the two lists were laid side by side.

Writing the missing section produced a finding worth keeping. This Force does not change *what* a rule is, it changes **where the rule lives** — chapter 03's migration from comment, to review habit, to type system. So it generates fewer patterns of its own than the others and mostly relocates rules the remaining Forces produced, which is why the section is short and says so.

**The sort changed, and the change is evidence the sort is real.**
Golden tests had been in the *refuses to sort* list, filed under patterns that answer a goal rather than a situation. With team size restored they have an obvious home: a golden test exists so behaviour cannot change silently under people who did not write it.

The chapter now records that, because it demonstrates the method doing work rather than confirming a guess: **a pattern that will not sort is sometimes evidence about the categories rather than about the pattern.**

Counts move from forty-three sorted and seven refusing, to forty-nine sorted and five refusing.

**Consequence.**
`00_toc.md`'s entry for chapter 12 gives the new counts and says the Forces are chapter 03's, so the grouping can be checked against the definition rather than against a fresh set of labels.
`LEDGER.md` loses the six-family row and gains two: the sort against chapter 03's seven, and the observation about team size relocating rules.
Chapter 12 runs 432 lines, up from 385.

---

## 45. A cross-reference must carry a fact, not a location

**Date.** 2026-08-15

**Context.**
The author's third review of chapter 12 raised a pattern that had built up unnoticed:

> I started to thing that lines like this after each worked pattern are like the chapter epigraphs we got rid off. Not much value and they create noise. Evaluate if removing these while preserving valuable parts without saying chapter this chapter that is better

Eleven of the fourteen worked patterns ended on a line naming another chapter — *chapter 04's definitional claim applies*, *which is chapter 07's territory*, *Chapter 06's registration example puts the hashing outside the lock for exactly this reason*.

**Options.**
Delete them all, which loses real pointers; keep them, which is the status quo the author objected to; or separate the two things they were doing.

**Decision.**
Separate them. A cross-reference stays when the fact it carries is one the reader needs at that moment, and it is then written as the fact with a compact `(Ch. NN)` pointer. It goes when the sentence exists only to say another chapter owns the idea.

By that test six lines lost their scaffolding and kept their content — *a copy with no invalidation strategy is a copy that is allowed to be wrong (Ch. 04)* says the thing rather than reporting that chapter 04 says it. One sentence was deleted outright: chapter 06's registration example was a pure location, and the claim before it already stood.

**Why.**
The failure is the one the epigraph decision found. A line that names another chapter reads as though it is adding authority, and authority is not what the book runs on — the mechanism is. It also degrades over time: a pointer to *where* a claim lives breaks silently when chapters move, while a pointer that states the claim survives being wrong about the number.

**Consequence.**
The pattern generalizes past chapter 12 and is worth applying whenever cross-references accumulate: **write what the other chapter established, not that it established it.**
The same review applied the author's other standing note — that showing the failing code before the pattern is worth doing where it does not make the example worse — to the tolerant reader, which now opens with a strict decoder that breaks on the one change chapter 09 calls always safe.
Both tags were the author's; the test that separates a fact-carrying reference from a locating one is the draft's.

---

## 46. Go has no way to withhold a zero value, and the chapter says so

**Date.** 2026-08-15

**Context.**
The author's fourth review of chapter 12 asked for caller code under *Make illegal states unrepresentable*:

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
Decision 44 recorded that golden tests moved out of the *refuses to sort* list once chapter 03's real Force names were restored, and the chapter carried a paragraph saying so. The author's fourth review cut it:

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
Chapter 12's *five that refuse to sort* ended on a bolded summary: **A Force is a fact about your circumstances. The shape of the problem is a fact about the business. A goal is something you chose and could choose differently.** The author's fifth review cut it, on the grounds that the two paragraphs above already made the distinction, and that *your circumstances* was adding a phrase rather than a fact.

**Decision.**
Removed. The section now has two bolded lead-ins — *Some answer a goal rather than a situation* and *Some answer what the problem is rather than what the situation is* — and the paragraph that follows them names all three in passing: *confusing the Forces, goals, and problem shapes in play.* Nothing states the taxonomy as a taxonomy.

**Why.**
It was a grand summary of the two preceding paragraphs, and a rule of three, which are both on the cadence list. The stronger reason is that it read as though it were introducing a distinction the section had spent two paragraphs making — so a reader who had followed the argument was told it again in the voice of a first telling.

**One change to the author's suggestion.**
The suggestion was to replace the *Some answer a goal* paragraph wholesale with the goal definition written in the fourth review. That paragraph names the three patterns at issue — property-based testing, the test-double taxonomy, functional core / imperative shell — and this is the section that says which five refuse to sort, so the names cannot go. Merged instead: the lead-in keeps the names, the definition and its test follow.

**Consequence.**
`LEDGER.md`'s row for this concept is reworded, since the canonical phrasing it pointed at no longer exists. The concept is still chapter 12's; it is now carried by the section rather than by a quotable line.

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
A survey of every Go sample in chapters 02 through 12 found about seventy-five short-name sites, and this exception licensed nearly all the ones that read badly: `FromMinorUnits(a int64, c string)` reduces amount and currency to letters in a chapter arguing about money handling, and `(b *Billing) Charge(m uuid.UUID)` uses a letter that is not the initial of anything on the line, so there is nothing to recover it from.
The exception is written as a structural rule, which is how it stops applying FlowCore's own test.
Receivers keep the convention, because the receiver's type is on the same line and a spelled-out receiver stops looking like Go.

*A fourth exception was added: quoted code is quoted.*
`CLAUDE.md` tells the draft to prefer real lines over invented ones, and a quotation with the names changed is a paraphrase.
Where a real signature carries a name that will not read, the fix is a comment, not an edit.

*The structural-particle exception gained a clause.* It exempts `err`, `ok`, and `ctx` from being renamed, not from being explained — the gloss rule still applies at first appearance.

*The type-shadow exception is unchanged*, and it earns its place: `05_structure.md` carries a real `q querier` quoted from FlowCore.

**Consequence.**
About thirty-five identifiers across chapters 02 through 12 do not comply.
Those chapters are at **draft**, so the cleanup is a separate pass on the author's word rather than a silent edit.
`CLAUDE.md`'s pointer now resolves: it named `docs/decisions.md, decision 18`, which in this repo is the entry on theorems and the halting problem, and now cites FlowCore's file by path alongside this entry.
Three copy artifacts from the verbatim import were fixed: an exception list introduced as "two" and containing three, a missing article, and a lost trailing newline.

---

## 50. The identifier sweep across chapters 02 through 12

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
Also `Receipt(o Order)`, `Register(name string, m Method)`, `chargeBad(l *Ledger, …)`, `PlaceOrder(…, q Queue, o Order)`, `receipt(c StripeCharge)` and its four neighbours, `adapt(r Receipt)`, `signUp(e Email)`, and the sign-up store's `u`, `e`, and `h` in chapter 06.

*Truncations* — `qty` to `quantity`, `pct` to `percent`, `dec` to `decoder`, `st` to `stat`, `dt` to `deltaTime`, `msgs`/`m` to `messages`/`message`, `Cur` to `Currency`, `src` to `source`, `key` to `idempotencyKey` where the chapter's own pattern name is *Idempotency key*.

*Paired letters standing for two things* — `a`/`b` became `accounts`/`billing` in the cycle example, `first`/`second` in Singleton, `timestampA`/`timestampB` in the clock-resolution measurement, where the prose already spoke of events A and B.

*One rename beyond the letter of the rule*, flagged because the rule names variables, fields, and parameters but not functions: chapter 06's Lamport-clock method `recv` became `receive`.
The defect is the same and the fix was free; it is recorded here so it can be reverted if the author disagrees.

**What was deliberately left, all fourteen sites.**

- **Type shadowing** — `q querier`, `q txQuerier`, `p *parser`. The exception, working as intended.
- **The `http.Handler` signature** — `handleSignup(w http.ResponseWriter, r *http.Request)`. The types are on the line and self-describing, and a spelled-out version stops looking like the Go the reader will meet everywhere else.
- **Complete words and standard terms** — `mux`, `job`, `row`, `sku`, `on`, `id`, `tx`, `db`, `req`, `fd`. None is a project-specific truncation, and each is recoverable from its line.
- **`(c *Conn) Raw(f func(driverConn any) error)`** is labelled in the chapter as a real standard-library method, so the quoted-code exception applies and it keeps `f`. The caller written beneath it is the book's own, and its `dc` and `pg` became `driverConn` and `pgxConn`.

**What the verification caught.**
Nothing behavioural, but two formatting defects the renames introduced: `Currency` lengthened chapter 11's struct and broke `gofmt`'s field alignment, and chapter 12's identity map needed its call sites updated to match.
Chapter 04's retranscribed output, chapter 06's race, chapter 12's identity map, and chapter 12's compiler error were all re-run and match what the chapters print — including the error text quoted in a comment, *cannot refer to unexported field at in struct literal of type delivery.Delivered*.

**Consequence.**
Chapters 02, 08, and 09 needed no changes.
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
*You cannot tell a slow machine from a dead one* is chapter 07's claim verbatim.
The 95% is chapter 06's measured figure.
So the promotional voice and the book's voice are the same sentences, which is the only version of this the book can defend.

Two hooks were pulled back on a check against the chapters, and the corrections are the substance of this entry.
*"You cannot, and it is a theorem"* was wrong: chapter 07 calls the indistinguishability a property of asking questions over a network, and the theorems are its consequences. Now *"most of what is impossible in distributed systems follows from it."*
*"'This should be a Repository' forbids nothing"* asserted something the chapter does not demonstrate — it works the test on Facade and lists Repository as a case for the reader to apply it to. Now phrased as chapter 10's own question, *what would that rule out?*, which is both accurate and a better invitation.

**Consequence.**
The rule this establishes for any promotional copy: **a hook must be cashable by the chapter it links to.**
A reader who arrives on an overclaim and then meets chapter 04's careful separation of theorem, definition, and empirical law will feel the mismatch, and not overclaiming is the book's differentiator.

---

## 52. Chapter 13 argues from Java's own history rather than across four languages

**Date.** 2026-08-15

**Context.**
`00_toc.md` planned chapter 13 as Norvig's observation "demonstrated in four languages side by side."
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
The folk version — *patterns are just missing language features* — drops both, which is chapter 04's dropped-quantifier failure applied to a smaller result.
He also defines three levels, invisible / informal / formal, where the retelling has two.
And he lists five purposes for patterns, of which "to avoid limitations of implementation language" is one; the claim that patterns are *only* workarounds is something readers added.

The chapter therefore states the narrower version, and is better for it: the strong version is easy to disprove and the real one is not.

**The counter-example came out of the source too.**
Norvig's sixteen omit seven — Adapter, Bridge, Composite, Decorator, Memento, Prototype, Singleton — and that omission is the boundary section.
The sharpest form is that **sum types dissolve Visitor and leave Composite standing in the same file**: the dispatch mechanism changes completely and the containment does not, because directories containing files is a fact about filesystems rather than about a compiler.
That is chapter 12's category of patterns answering the shape of the problem, reached from a different direction.

Two further boundaries: Observer dissolves in one process and returns across a machine with all of chapter 07's failure modes, so the test is scoped and returns a confident wrong answer when run at the wrong scope; and the test names the language you moved *to*, so "Visitor is a workaround" is true and useless if your compiler lacks sum types.

**Consequence.**
Every sample was compiled and run as printed — nine fences across Java, Go, and Python, plus both quoted `javac` errors.
`LEDGER.md` gains nine concept rows and four example rows.
The relationship to chapter 12 is stated in the second sentence rather than left implicit: 12 asks what a pattern answers, 13 asks what it is made of, and the two are independent.

---

## 53. The Strategy comparison was rigged, and Decorator fails the chapter's own test

**Date.** 2026-08-16

**Context.**
The author's first review of chapter 13 objected to the Strategy demonstration:

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
The quantifier discussion was rewritten in plain words with chapter 04's halting-problem parallel given enough context to work without turning back, per the author's note that nobody re-reads an earlier chapter.
*Sum type* is now defined at first use.
Two cross-references to chapters 10 and 11 were cut as detours; the author's standing objection to "abrupt flashbacks" is that they need to earn their place, and these restated a convergence the local argument did not need.

**Consequence.**
Twelve code fences, all compiled and run as printed.
The chapter grew from 379 to about 470 lines, almost entirely in the boundary section, which is the right place for it to grow.

---

## 54. The book has no authorial "we", and chapter 13 nearly acquired one

**Date.** 2026-08-16

**Context.**
The author's second review of chapter 13 was direct edits only, no tags.
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

## 55. Chapter 14 grades loaded terms into three tiers rather than condemning them

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

**Why this is not a repeat of chapters 04 and 13.**
Both of those are about a claim losing a qualifier — the halting problem's quantifier, Norvig's *for at least some uses*.
Chapter 14's mechanism is lexical rather than propositional: a claim can be qualified and a noun cannot, so the condition is not merely dropped but made unsayable while the word is in play.
The chapter states that difference rather than leaving the three to look alike.

**The boundary comes from the book's own spine.**
*Use-after-free*, *SQL injection*, and *data race* carry verdicts and are fine, because there is no configuration of Forces under which they are the right answer.
That gives the rule: **a verdict noun is legitimate when it names a Law violation and dangerous when it names a Principle violation**, since a Law has no condition that can fail and a Principle is conditional by definition.
Two further boundaries: refusing all judgment-laden vocabulary is itself a slogan with its conditions removed, and you need the term anyway because it will be used on you.

**Source material.**
The argument is largely the author's, worked through while building FlowCore and recorded in `~/c/TechIter/01/coding-style-architecture.md` — the *anemic domain model* critique, the vocabulary-versus-prescription distinction, and *placed by scope* with its worked rules.
Per `CLAUDE.md`, that was read rather than re-derived.
Chapter 19 owns the placement method; chapter 14 takes only what the vocabulary argument needs and cites 06 for why the widest scope is not a preference.

**Verification.**
The Go sample compiles and runs as printed.
The sqlite demonstration was run and the chapter quotes the real output — a first draft of that block invented `sqlite>` prompts and trimmed the error text, which is the failure the run-the-code rule exists to prevent, caught on re-reading before commit.

**Open question for the author.**
The chapter is titled *Patterns That Smuggle a Verdict*, matching the TOC, but its subject is vocabulary rather than patterns — *code smell* is not a pattern, and neither is *anti-pattern*.
*Smuggled Verdicts* would be more accurate. The title is the author's call, and the drift check enforces H1 against the TOC either way.
