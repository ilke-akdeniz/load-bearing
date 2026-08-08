# Decision Log

Editorial decisions for *Load-Bearing*, recorded when made rather than reconstructed afterwards.

Each entry follows the same shape: **Context / Options / Decision / Why / Consequence**.
The reasoning is the point — a decision without its reasoning is just a fact about the current draft, and tells you nothing when you are deciding whether to reverse it.

Two purposes:

1. **Working memory.** In six months the question will be "why Levels and not Altitudes," and the answer should not have to be re-derived.
2. **Authorship record.** The book is written with AI assistance. What makes it an authored work rather than an assembled one is the selection, rejection, and correction recorded here — so those are recorded with attribution, contemporaneously.

Entries note who originated what.
"The author" is the human; "the draft" is generated text prior to review.

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
