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
