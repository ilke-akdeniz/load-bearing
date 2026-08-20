# Load-Bearing

A book: **Load-Bearing — Which Software Principles Hold, and Where They Stop.**

Written in public, for readers.
Not a tutorial, not a beginner's introduction.

The prose is LLM-generated; the idea, the judgment, and the editorial control are the author's.
The README states this openly and `docs/DECISIONS.md` is the evidence, so **keep the decision log current** — it is part of the book's claim about itself, not bookkeeping.

## The thesis

Most software advice is true.
Almost none of it says what *kind* of claim it is.

"Dependencies must be acyclic" is nearly a mathematical fact.
"Every repository gets an interface" is a local convention of one ecosystem.
Both arrive in the same tone of voice from people of equal confidence, so the convention gets applied with the force of a law and the law gets treated as one option among several.

The book is a field guide for telling the difference.
Its central question is the one a builder asks before knocking out a wall: **is this load-bearing?**

The book is written to be **received**, not obeyed.
Its subject is how to read advice — a blog post, a review comment, a pattern name, a strong opinion in a meeting — and place it correctly before deciding what to do about it.

## The five kinds

The spine. Every chapter classifies **claims** against these — anything that can be true, false, or conditional.

Four of the five are advice and form a ladder of authority; Force is not advice, and sits outside the ladder.
So the count is **four levels and five kinds**, and the word *level* is reserved for position on the ladder rather than used as a synonym for *kind*.

Four are advice, forming a ladder of authority: **Law → Principle → Idiom → Style.**
The fifth, **Force**, is not advice — it is the input that decides where on the ladder you are standing.

| Kind | What it is | Authority |
|---|---|---|
| **Law** | true by the mechanics of computation | absolute |
| **Force** | a property of your situation | not advice — an input |
| **Principle** | good advice *given* certain Forces | conditional |
| **Idiom** | an ecosystem convention | local, non-transferable |
| **Style** | naming, formatting, layout | none, but be consistent |

Two rules about Forces that later chapters must not blur:

- **A Force never makes a Law false.** It decides whether the Law *binds* or sits inert.
- **A Force can make a Principle wrong.** Principles don't go quiet — they invert.

Short version: **a Law can be irrelevant but never wrong; a Principle can be wrong.**

Always name the kinds — Law, Force, Principle, Idiom, Style.
**Never number them.** The names carry meaning; a number is one more thing to decode.

## Authoritative documents

Read these before writing anything.

- `README.md` — premise, the model, the chapter rubric, conventions, license. The landing page.
- `00_toc.md` — the full 23-chapter TOC with per-chapter summaries and stated boundaries, plus the drafting status table.
- `docs/LEDGER.md` — **concept and example ownership.** Which chapter owns which idea. Non-optional; see the protocol below.
- `docs/DECISIONS.md` — editorial decisions, with reasoning and the options that lost. Consult before reversing anything.

If a change contradicts `docs/DECISIONS.md`, stop and say so rather than proceeding.

## Sources

Material outside this repo that the book draws on.
Most of it has already been worked through and corrected by the author, so **read it rather than re-deriving the argument** — re-derivation produces subtly different claims, and the book cannot afford to contradict itself between chapters.

- **`~/c/TechIter/01/coding-style-architecture.md`** — roughly 3,700 lines analysing FlowCore's structure, written and reviewed in dialogue with the author.
  Directly feeds several chapters: layering and the direction rule, DAG-versus-line shapes, when layering fails (→ 05, 18); placement-by-scope with worked rules (→ 19); Adapter at class scale versus system scale (→ 11); layered packages forcing exports (→ 18); dependency injection across Go, C#, Python, and Node (→ Part V); error taxonomies, params structs, and testing against a real database.
  It also contains the author's positions on pattern culture and methodology, which Part IV should stay consistent with.
- **`~/s/flowcore/docs/decisions.md`** — 38 design decisions in Context / Options / Decision / Why / Consequence form. The source of most FlowCore examples, and the model for this book's own decision log.
- **`~/s/flowcore/docs/code-map.md`** — how the library fits together; useful for picking an example that is genuinely representative.
- **`~/s/flowcore`** — the code itself. Prefer quoting real lines over inventing illustrative ones.

**`docs/pending/` holds the same kind of document inside this repo.**
Each file is a worked argument with its evidence and provenance already gathered, and a table saying which chapter is owed which piece.

Before drafting a chapter, or reopening one, check the folder for material owed to it.
Each file names its own chapters and tracks what has been routed, so the folder is the list and this file does not repeat it.
A document leaves `docs/pending/` for `docs/` once every piece in it has landed; it is not deleted, because the ledger cites these arguments as provenance.

Public repo: <https://github.com/ilke-akdeniz/flowcore>.

## The anti-repetition protocol

The single most important operational rule in this repo.

Earlier AI-assisted book attempts failed by restating the same ideas across three or four chapters.
The cause is structural: a chapter drafted in isolation cannot see what earlier chapters established, so it re-establishes it.
`docs/LEDGER.md` supplies the missing information.

**Before drafting any chapter:** read `docs/LEDGER.md`.
If a concept or code example is already owned by another chapter, the new chapter gets **one sentence and a cross-reference** — never a recap.

**After drafting any chapter:** add what it claimed to the ledger.

Only three things may legitimately recur, and they are listed in the ledger: each chapter naming its own kind, the mandatory boundary section, and FlowCore appearances that must each show a different facet.

A repetition found in review is a **ledger defect** — a missing or mis-assigned row — not a local wording problem.

## The rule the book holds itself to

**No chapter ships without a real counter-example.**

Every chapter has a mandatory *Where the claim doesn't apply* section containing a worked case, not a hedge.
"This always applies" is never an acceptable answer.
If a boundary cannot be found, that is evidence the claim is too vague to be useful — not evidence that it is universal.

This applies to Laws too.
They don't stop being true, but they stop being *relevant*, and knowing when they stop mattering is the same skill.

## Chapter rubric

Each chapter follows this shape:

1. **The claim** — one sentence, and the chapter opens on it. No epigraph, no framing paragraph before it: a reader who does not yet know the subject cannot use a note about the subject's standing.
2. **The demonstration** — code, in two or more languages when the point concerns translation.
3. **Why the claim holds** — the mechanism, never the authority. No argument from who said it.
4. **Where the claim doesn't apply** — mandatory, with a worked counter-example.
5. **What the claim costs** — every choice has a bill.
6. **How to recognize the failure** — what it looks like in a real codebase when someone got this wrong.

Then the back matter, after the argument ends: a `## Sources` section, and the `**Next:**` line handing off to the following chapter.

**Sources lists every work the chapter cites, and nothing else.**
Bare entries — author, title, venue, date, link — in order of first appearance in the chapter, with every link verified rather than recalled.
It is not a further-reading list: a work the chapter does not cite does not go in, and a work it does cite is not annotated with what the chapter took from it.
Provenance stays in the prose where the claim is made, so the section adds no footnote markers and changes no sentence.

### The claim sentence

The claim may assert **only what the chapter goes on to demonstrate**, and the standing bias is toward asserting more.
The bias has a specific shape: claiming *sufficiency* where only *necessity* was shown.

Two drafts of chapter 03's claim failed this, in the same direction:

- *"Evaluating the Forces is most of the work of choosing well"* — unquantifiable, and not what the chapter demonstrates.
- *"…is where the design is actually decided"* — contradicted by the book itself in three places: chapter 02's *classifying is not deciding*, chapter 03's own concession that conflicting Forces are decided rather than computed, and chapter 21's case for obeying an Idiom you can out-argue.

What survived was *"…is the groundwork"* — a prerequisite claim, necessary and explicitly not sufficient, provable from the seven cases the chapter works through.

**The test, run before the claim ships:** list the cases the book concedes elsewhere and check whether the claim survives them.
A chapter already written that contradicts the claim means the claim is wrong, not the other chapter.

**A claim too vague to be false is not the safe fallback.**
*"Evaluating the Forces is crucial"* cannot be disproved and cannot be used for anything.
Asserting importance is not making a claim — say what happens, or what breaks without it.

This applies to every bolded assertion in a chapter, but the claim sentence is where it costs most, because everything after it is read as support.

## Writing style

**Simple language, precise terminology.**
Plain words wherever they work, but name the real terms — Transaction Script, information hiding, TOCTOU, Hyrum's Law — because the reader needs the vocabulary to find the literature.
Explain a term once, at its owning chapter, then use it.

**Expand an abbreviation on first use**, unless an experienced engineer would produce the long form without hesitating.
`API`, `SQL`, `HTTP` need nothing. `FLP`, `2PC`, `PACELC`, `TOCTOU`, `ECS`, `CQRS` get the expansion once, at first appearance in the chapter, then the short form thereafter.
Where the name is initials of people — FLP is Fischer, Lynch, and Paterson — say so, because it tells the reader what to search for.

**A code demonstration for every major claim.**
Not an illustration bolted on afterwards; the code should be the argument.
Go, C#, and Python carry most examples; Rust, TypeScript, C, and SQL appear where a point needs them.

**Write for an engineer who is a tourist in this domain.**
The reader is experienced, and experienced in *their* specialty rather than in all the ones this book crosses.
A single chapter may traverse queueing theory, cache hierarchies, distributed consensus, and compiler structure.
Almost nobody is fluent in more than two of those, and the missing ones are invisible to whoever is writing — which is how a chapter ends up addressed to someone who already knew it.

Calibrate on what the sentence needs, not on whether the word looks familiar: **does this claim work on the gloss an experienced engineer already has, or does it need the specialist meaning?**

*Blockchain* is the case that shows why the question is put this way. "Blockchains are append-only" works on the common gloss — assume it and move on. "A reorg makes finality probabilistic below N confirmations" does not, and every load-bearing word there needs work.

**The same word falls on either side depending on the load it carries.**
*Transaction* is assumed everywhere in this book; *prepared transaction* is a two-phase-commit term and is not.
*Utilization* is ordinary English until it means the fraction of time a server is busy, at which point the queueing sense has to be given.

The lists below are **illustrative, not a lookup table** — a term missing from both is the normal case, and the question above decides it.

- **Usually assumed** — big-O notation, graphs and trees, hash tables, locks, transactions, HTTP, garbage collection, indexes, interfaces, recursion. Explaining these reads as condescension and spends attention the argument needs.
- **Usually explained at first use** — terms whose specialist meaning is the one being used. Cache line, prefetcher, working set, coherency traffic, linearizability, quorum, entity-component system, bitemporality.

The structural fix beats the inline definition: **lead with the situation, give the number, name the thing last.**
Chapter 08's Amdahl section works because a hundred-minute report with twenty un-splittable minutes makes the ceiling obvious before any formula appears — the name then labels something already understood rather than gating it.

Two failure symptoms, opposite directions.
Under-explaining reads as a textbook: the reader decodes vocabulary instead of following the argument, and the point is lost in the decoding.
Over-explaining is the likelier failure once this rule is in force, and it is just as bad — the reader is being told what they know.

**Write Go for a reader who does not know Go.**
The language-specific case of the rule above.
The audience is most likely fluent in Java, C#, or Python and not in Go.
Go carries a large share of the book's examples because FlowCore is written in it, so every Go sample has to be readable by someone who has never used the language.

- Gloss anything with no counterpart in those languages, at its first appearance, in one line — channels, goroutines, `defer`, the comma-ok idiom, struct embedding, capitalization as visibility.
- Reach for the nearest equivalent the reader already has: *a channel is a typed in-memory queue, roughly Java's `BlockingQueue` or Python's `queue.Queue`.*
- Comment what the line is doing when the syntax is the unfamiliar part, not what it means for the argument.
- Never send the reader away to look something up. They will not, and the example is then spent.

The same holds in reverse for a C# or Python sample carrying a point in a Go-flavoured chapter.

**Run the code before it goes in.**
Any example whose point depends on what it *does* — output, an error, an order of events, a value that surprises — gets executed first, in the scratchpad, and the chapter quotes the real result.
Confidence is not verification.
A chapter shipped with a Python circular-import example that claimed one import order worked; both failed, and the mistake survived a full self-review because it looked obviously right.

- **Verify, then write.** Not the reverse — a written example is one you have started defending.
- **When the example fails to show what you expected, that is the finding.** Say what actually happens, or replace the example. Do not adjust the prose to make a broken demonstration sound correct.
- **When a toolchain is unavailable**, say so in the chapter's review notes rather than asserting output. Go, Python, and Node are usually available; C#, Java, and Rust usually are not. Prefer a verifiable language when the point is language-independent, and describe the mechanism without invented numbers when it is not.
- **Structural code needs no run** — a type signature, an interface, a shape being contrasted with another shape. The rule is about claims of behaviour.

**Verification code is not example code.**
The program written to check a claim and the sample printed in the chapter are two different artifacts with two different jobs.
A harness may take a `dead bool` parameter, hard-code a delay, or drive both cases from one function, because its only reader is the person checking the claim.
A chapter sample is read by someone deciding whether their own code has this defect, so it must look like code they might have written.

This has gone wrong more than once. The tell is a sample whose shape only makes sense as a test:

- **Parameters that exist to select the scenario** — `call(150*time.Millisecond, false)` versus `call(0, true)`. A real caller never passes "and this time be dead."
- **The number in the prose missing from the code.** If the text says "a 100 ms timeout," the sample must contain `100 * time.Millisecond`, not hide it inside a helper.
- **One function standing in for two different systems**, when the point of the example is that they are two systems.
- **Names from the harness** — `call`, `run`, `doThing` — where the chapter is discussing a payment or an order.

So: verify with whatever is quickest, then **write the example again** in the shape a reader would recognize, and run *that*.
Real client libraries, real signatures, real names.
When the realistic version cannot be run — it needs a database, a network peer, a second machine — say so rather than reaching back for the harness.

**Mechanism over authority.**
Never "Fowler says." Always "here is what happens, and here is why."
Cite people for provenance, never as proof.

**Read the source before explaining why someone else's result holds.**
The rule above is about not using a citation as an argument.
It is not permission to skip the paper — and it was read that way twice in one chapter.

Naming a result is one thing; explaining its mechanism, or saying what its terms mean, is another.
The trigger is writing a sentence of the form *the mechanism is…*, *what X actually meant was…*, or *the reason this holds is…* about a named law, paper, or person's argument.
At that point, go and read it.

Chapter 09 explained Conway's Law twice without reading Conway.
The first attempt made it a temptation acting on individuals, which the author rejected as implausible.
The second replaced that with an ownership mechanism, which was defensible and still could not answer *is this what he said*.
One fetch settled it: Conway's own words are *negotiated and agreed upon*, which is the ownership reading in his vocabulary — and the paper contained a sharper example than anything invented for it, a five-person team producing a five-phase compiler and a three-person team producing a three-phase one.

Two things follow, and the second is the reason the rule is worth the trouble.

- **The paraphrase is usually less precise than the original.** *Communication structures* is vague; *negotiated and agreed upon an interface specification* is not, and the whole argument turns on it.
- **The source contains material you would not have thought of.** Examples, edge cases, and the author's own statement of what the result does *not* cover.

When the source genuinely cannot be reached — paywalled, offline, out of print — say so in the chapter's review notes and keep the claim to what is uncontroversially attributed, rather than explaining a mechanism from inference.

**Read the primary source in full, and never splice inference into it.**
Chapter 15 got the Pike material from a third-party transcript, read in excerpts, and then failed in a way excerpt-reading makes almost inevitable.

Pike's talk lists *Don't communicate by sharing memory* and, two items later, *Channels orchestrate; mutexes serialize*.
The draft asserted that the second is the **condition** for the first — "the condition was published beside the proverb, by the same person, on the same afternoon."
He never says that. They are two proverbs, each with its own explanation, and the relationship between them was the draft's inference presented as Pike's structure.
The author caught it by watching the talk.

Four rules follow, and the third is the one that would have caught this.

- **Read the whole thing, not the passages that answer your question.** This is the rule, and it is about partiality rather than about medium. Excerpts fetched to confirm a thesis return what was asked for; the context that would have disproved it sits in the parts nobody requested. A full verbatim transcript read end to end is a good source. The same transcript read in four keyword searches is how chapter 15 went wrong.
- **Rank what you have, and say which you used.** The author's own writing, then a full recording or transcript of them speaking, then someone else's account of it. Name the one you actually read when the chapter quotes it.
- **Never silently combine an author's words with your own inference and present the result as theirs.** Quoting two real sentences and asserting a relationship between them produces a claim the author never made, out of material that is entirely genuine. Where a connection is the book's, say so in the sentence.
- **Surface what the author must check.** End the response that ships a chapter with the primary sources under the heading **Must be read by the author before this chapter is marked draft**, with direct links and timestamps where they exist.

If the primary source cannot be reached at all: say so, propose alternatives, and **stop** rather than drafting the claim from inference and flagging it afterwards.

**A source's register is not the book's.**
Reading the primary source is the rule above; writing in its voice is a separate failure, and the better the source the likelier it is.

A paper, a specification, or a standards document states its finding in the vocabulary of its method — coefficients and models, the outcome names it defined on page four, the abbreviations it needs because it refers to them a hundred times.
That vocabulary exists so other specialists can check the work.
It is not what the finding says, and a chapter that carries it across has swapped its own reader for the source's.

Chapter 17 shipped a draft with three stacked block quotes, one of them containing *"this advice would require a negative (statistically significant) coefficient, which the models did not produce."*
What that sentence means is *they looked for a link in either direction and found none — had test-first been harmful, more of it would have gone with worse results.*
Same content, and only the second version is usable by this book's reader.
The same draft carried the paper's `GRA / UNI / SEQ / REF` abbreviations, used once each, and gave *external quality* as though it were plain English rather than *how much of a supplied acceptance suite the code passed*.

- **Say what was measured, not what it was called.** An operationalized term is a definition wearing a name. Give the definition and drop the name.
- **Leave the source's abbreviations in the source.** They earn their place in a document that uses them a hundred times, not in a chapter that uses them twice.
- **Paraphrase for meaning, quote for provenance.** State the finding in the book's voice, then quote the short fragment that proves the source said it. A long quotation usually does neither job well.
- **This does not loosen the quotation rules.** Quoted words stay exact, and a paraphrase reads as the book's own sentence. The rule above stops your inference being attributed to the source; this one stops the source's voice being imported into the book. Both are satisfied by keeping the two visibly separate on the page.

The symptom to watch for is a paragraph a reader has to decode rather than follow, in a chapter that was going fine until the citation arrived.

**Provenance, stated in prose.**
Before writing a claim whose standing could be mistaken, decide which it is: standard and citable, genuinely disputed, or this book's own.
Then **write that into the sentence** — there is no tagging notation.

- Standard: cite it in the normal way. *Parnas, 1972* is already its own provenance; do not label it as well.
- Disputed: say who disputes it and on what grounds. A bare "this is contested" is hedging, not honesty.
- The book's own: say it is not standard vocabulary, so the reader knows what to expect when they search for the term.

The five-kind model is the book's own, and every chapter that leans on it should read that way.

**Running example.**
FlowCore — a Go workflow library at `~/s/flowcore` with a 38-entry decision log — supplies examples in Parts II and V, because its reasoning was recorded at the time rather than reconstructed afterwards.
Each appearance must show a *different* facet. No chapter rests on FlowCore alone.

## Markdown conventions

Two sets.
Book chapters at the repo root are prose for a reader and a future print build; working documents in `docs/` are engineering artifacts reviewed as diffs.
They get different rules.

### Shared by both

- **Blank line between block elements**, and after every heading before its content.
- **Never two blank lines in a row.** File ends with a single newline.
- **Lists:** one item per line, no blank lines between items in a tight list.
- **Code fences and tables are literal** — never reflow their contents.
- **Bold lead-ins** (`**Term.**`) stay on the same line as the sentence they introduce.

### Book chapters — `NN_slug.md` at the repo root

Four rules, and they exist because the source is read as prose and will one day be built into a PDF.

- **One paragraph per line.** No breaking within a paragraph; the editor soft-wraps. Paragraph boundaries are the blank lines, and a paragraph is one line however long it runs.
- **Code is left exactly as the language's formatter produces it.** Never hand-break a signature to fit a page — code is read in the source far more often than in print, and the print build wraps long lines itself (see below). `gofmt` output goes in verbatim.
- **ASCII diagrams stay under 72 columns.** This is the one width rule, and it applies only to diagrams, because a wrapped diagram is destroyed rather than merely marked.
- **One H1 per file, the chapter title with no number** (`# Structure: Dependency and Hiding`). The number lives in the filename and the TOC. A print build numbers chapters itself, and a number in the title produces "Chapter 5 — 05. Structure."
- **Every code fence carries a language tag** — `go`, `csharp`, `python`, `sql`, `rust`, and `text` for terminal output, compiler errors, and ASCII diagrams. No bare fences.

Everything else stays as it reads best.
Long code lines, box-drawing characters in diagrams, `>` blockquotes, `---` section dividers, and plain `(Ch. 05)` cross-references are all fine — each is a build-time transformation, and none is worth making the source uglier for.

**For whoever writes the PDF build.**
Long code lines are handled by `fvextra`, which extends the `fancyvrb` environments pandoc already emits, so pandoc's syntax highlighting is kept:

```latex
\usepackage{fvextra}
\fvset{
  breaklines=true,          % wrap instead of overflowing the margin
  breakanywhere=false,      % break at whitespace, not mid-token
  breakindent=2em,
  breaksymbolleft={\small\ensuremath{\hookrightarrow}},
  fontsize=\small
}
```

At `\small` a normal measure fits roughly 72–80 monospace columns, so the handful of lines above that wrap once and carry a visible `↪`.
Diagrams must not be wrapped by this — either keep them inside the measure, which is the rule above, or emit `text` blocks with `breaklines=false`.

### Working documents — `docs/`

- **One sentence per line.** Break at `.` `?` `!`. A one-word change is then a one-line diff.
- **Don't split mid-sentence.** A clause after `;` `:` or `—` stays on its sentence's line.

These are read as diffs, not as prose, so sentence-level granularity is worth more than paragraph shape.

## Files

- Chapters at the repo root: `NN_slug.md`, matching the TOC in `00_toc.md`.
- Working documents in `docs/`, and in `docs/pending/` while they still owe material to a chapter.
- `tools/check-drift.py` — the mechanical consistency checks. Run it before committing.
- `00_toc.md` carries the status table — update it when a chapter's status changes. The README is the landing page and should stay short.

### Keeping the TOC honest

The TOC drifts in two ways, and they need different handling.

**Local drift** — an entry describing its own chapter wrongly, because the chapter changed during review.
Chapter 13's entry said *"Decorator is function composition"* after the chapter had measured that and found it false.
This needs judgment, so **update a chapter's entry when it moves to draft**, while what changed is still fresh.
Folding it into the status change costs a minute; finding it later means re-reading the chapter to reconstruct a conclusion nobody remembers reaching.

Entries for chapters that do not exist yet are a different thing again: they are the plan a drafting session reads, not a description.
A stale one produces a wrong chapter rather than a wrong paragraph, so update those when a decision changes them.

**Global drift** — two things that must differ don't, a retired term survives in one place, a count disagrees across files.
No per-chapter review catches these, because no single chapter is wrong.
Part I was called "The five kinds" while chapter 02 was called "The five kinds of claim" — neither wrong alone, and the collision was *created* by the sweep that fixed the terminology.
This is what `tools/check-drift.py` is for. Run it rather than looking for these by eye.

### Chapter status

Four states, and the transitions are not Claude's to invent.
Only the first is automatic; the other two happen when the author says so.

| Status | Meaning | Moves there when |
|---|---|---|
| **not started** | no file exists | — |
| **in progress** | the file exists and is being worked | Claude creates `NN_slug.md` |
| **draft** | the author is satisfied and the chapter is behind us | the author says the chapter is ok, or to proceed to the next one |
| **ready** | fit to publish | the author says it is ready for publication |

A chapter sits at **in progress** for the whole review cycle, however many passes it takes.
It moves to **draft** on the author's word and not on Claude's judgment that it looks finished.
**Ready** is a separate, later decision, and nothing reaches it by default.

## How we work

The author leads, reviews every chapter, and makes the editorial calls.
Claude drafts and makes local writing decisions.

**Ask before** changing the five-kind model, the chapter rubric, the TOC structure, or anything recorded in `docs/DECISIONS.md`.
Those are the author's, and they land in the decision log first.

Draft **one chapter at a time** and stop for review.
Do not batch chapters — the steering between them is where the book's judgments are made.

Record substantive editorial decisions in `docs/DECISIONS.md` using the existing shape: **Context / Options / Decision / Why / Consequence.**
The log doubles as the authorship record for an AI-assisted work, so it has to say where a decision came from.

### Attribution in decision entries

**The default is that unattributed content is the draft's.** That is stated once in `DECISIONS.md`'s header, so it does not need repeating per sentence.

Attribute explicitly where the origin changes how the entry reads later:

- The author originated the idea, chose between options, or rejected one.
- A correction came from review — say what it corrected, not merely that a correction occurred.
- The draft's recommendation did not survive, and why.
- The resolution was **joint**: an objection from the author, a concession, and an answer neither had at the start. Record it as joint rather than assigning it to whoever typed it.

Do not attribute routine drafting, formatting, or mechanical consequences.
*The draft wrote a section and nobody objected* is not a fact about the book.

Two failures, in opposite directions.
Tagging every sentence with its origin makes the log unreadable and is the inflation this rule exists to prevent.
Recording a jointly reached answer as the draft's, because the draft wrote it down, is the quieter one and the more damaging — it is the case where the log stops supporting the claim the README makes.

### The review cycle

A chapter is finished by alternating commits, and **both sides commit**, so that each party's contribution stays visible in the history.

1. **Claude writes and commits.** One commit per pass.
2. **The author reviews in the file itself.** Two kinds of change arrive together: direct edits to the prose, and notes to Claude written inline as `[claude …]` tags — questions, objections, requests, or a decision to apply.
3. **The author commits, and says so.**
4. **Claude reviews that commit, acts on all of it, and commits again.**
5. **Repeat** until the author says the chapter is done.

**Reviewing the author's commit means reviewing the whole commit, not only the tags.**
This is the step that has already gone wrong once: the tagged items were treated as the review and the direct edits as settled.
Edits written quickly in the margins of a review need proofreading like any other prose.
**Read the whole diff, line by line, before changing anything.**
Evaluate the direct edits first — they may have moved what the tags are asking about — then act on the tags.
Direct edits can alter the meaning of the text, including the claim sentence every tag is measured against.
Reversing this order could yield unwanted results, and tags sometimes explain a direct edit, so the reading is whole-diff even though the acting is ordered.

- **Review every direct edit on the merits, not only for grammar.** Ask whether it made the chapter better, and say so either way. Two failures a spellcheck cannot see: an edit that restates a concept another chapter *owns*, in different words, which is the drift `docs/LEDGER.md` exists to prevent; and an edit that weakens a claim while reading more smoothly. Check terms the ledger assigns elsewhere against their canonical wording.
- **Proofread every direct edit** — grammar, and the book's own rules. A review edit is as subject to the register and the no-decoration rules as anything Claude wrote. Note that automated checks skip fenced code, so comments inside samples need reading by eye.
- **Disagree when there is a reason to.** A tag is not always an instruction; some are questions and some are wrong. Say so, give the reason, propose the alternative. The author repeating it settles it.
- **Act on every `[claude …]` tag**, and delete it once addressed. A tag left in the file is unfinished work, and a chapter is not ready while any remain.
- **Report what changed and why**, including anything found that was not asked about.

**A wording problem found in one place is a survey, not a fix.**
Three times while finishing chapter 15, a single word caught in review was doing the same wrong job elsewhere, and the one-site fix would have left the rest.

- *Sentence* was vague in the claim. Correcting it exposed **thirteen** more uses in the body standing in as general vocabulary, including the chapter's second-strongest line and its closing test.
- *Extent* was a private synonym for *scope*, used **ten** times for the same thing inside one chapter.
- A table column confused a principle's scope with a term's extent. The same slip was in two further paragraphs.

So when a word is found doing the wrong job, **grep every use of it before calling it fixed** — and not only in the chapter. `docs/LEDGER.md` and `00_toc.md` carry the same vocabulary, go stale silently, and were wrong in each of these cases.

The cross-chapter version is the same rule at larger scale. *Scope* had acquired three incompatible meanings across chapters 13, 14, and 15, two of them bold definitions in adjacent chapters, before anyone counted. One survey found it; a lot of careful reading had not. `tools/check-drift.py` catches structural drift and cannot catch this, so the survey has to be run by hand when a term is in question.

### The final sweep

Rules and material accumulated while the book was written, so a chapter drafted early was held to fewer rules than one drafted late.
The correction is a single pass over the whole book, run once, after the last chapter reaches **draft**.

**It is the author's to start.**
When every chapter is at draft, ask for confirmation rather than beginning, and do not run it early because a chapter looks finished.

**Four slices, in this order, each followed by review.**
The order is load-bearing — every slice inspects what the one before it produced.
Work one chapter at a time inside a slice, commit per chapter, and stop for the author to review and amend before the next slice starts.

1. **Pending material.** Every document in `docs/pending/`, plus the owed table in `00_toc.md`, names the chapters it is owed to. Route every piece to its chapter, or record that it no longer fits and why.
2. **Rules.** Check each chapter against the rules in this file that postdate it. `git log CLAUDE.md` against the chapter's own history gives the candidates; a commit that changed this file *and* many chapters at once was already applied retroactively, and one that changed a single chapter was applied only there.
3. **Sources.** Every chapter that lacks a `## Sources` section gets one, with links verified rather than recalled. Slice 2 has just identified and checked the citations, which is most of the work.
4. **Reconciliation.** TOC entries against what each chapter now says, ledger rows against what each chapter now owns, then `tools/check-drift.py`.

**Content added during a slice has not been through the slices already finished.**
A passage routed in slice 1 still needs reading against the rules; an author amendment in slice 3 may carry a source nobody listed.

## Git

**Commit. Never push.**

Pushing is the author's, always. Nothing reaches the public repository without them.

After making changes:

1. Stage them — `git add -A`, or the specific paths when only part of the work is ready.
2. Commit, with a message that says what changed and why.

One commit per pass, so the history alternates cleanly between Claude's work and the author's review.
Never amend or rebase the author's commits — the point of the history is that both sides of the exchange stay readable.

Keep the message short: a subject line, and a body only when the change needs a reason rather than a description.
Where a change reverses something, or was made against a request, say so in the body.
The history is part of the book's authorship record, alongside `docs/DECISIONS.md`.

## Register

Direct, concrete, willing to say a popular idea is wrong and why.
Not breezy, not academic, no throat-clearing.
The reader is an experienced engineer who has been burned by advice that didn't fit.

Avoid: "best practice," "clean code," "simply," "just," and any sentence that would survive being deleted.

### No decorative language

An image earns its place only by doing work the plain sentence cannot.
Two tests, and a phrase must pass **both**:

1. **Is the image carrying the explanation?**
   Then there is no explanation — replace it with the mechanism.
   *"A well-encapsulated module is opaque at 3am"* explains nothing about why hiding costs you.
   *"Every decision you hide is one your users cannot reach when they turn out to need it"* does.
2. **Is the point already made without it?**
   Then delete it.
   This is the more common case and the harder to catch, because the paragraph reads well either way.

The recognizable forms, all of which have shipped in drafts of this book and been cut on review:

- **Personification** — "the cycle announces itself," "the Force does not negotiate." Structures do not act. Say what is observable, and where.
- **A metaphor promoted to a term** — "same meter," "the tell." If a figure of speech starts being used as vocabulary it needs defining, and if it needs defining it is not worth the definition.
- **Evaluative adjectives standing in for the argument** — "seductive," "elegant," "nasty." Name the consequence instead.
- **Grand summaries** — "that is the whole of API design." The preceding sentence already said it, and better.
- **Atmosphere** — 3am, war stories, the beleaguered engineer. The reader is one and does not need reminding.

### Vary the cadence

A distinct failure from decoration, and the one that makes generated prose recognizable: **every paragraph landing on a closing turn.**

The shape is setup, pivot, epigram — and it is fine once. Run it for forty paragraphs and the reader stops hearing the argument and starts hearing the rhythm.

The tells, all cut from drafts of this book:

- **A closing clause beginning "which is why."** Two in a row is a tic; four in a section is a style.
- **"It is not X. It is Y."** Reserve for a genuine correction. It is not a way to introduce Y.
- **Announcing a count, then delivering it** — *two things are worth noticing here.* Say the two things.
- **A final sentence engineered to be quotable** — *and no amount of profiling will find it.* Ask whether it adds a fact. Usually the preceding sentence already carried it.
- **Rule of three** — three parallel clauses, three-item lists, a triple where two would do.

The fix is not to delete every turn but to **let most paragraphs end flat**, on the fact, with no summary. A closing line earns its place roughly once a section, where the argument genuinely turns.

Read a finished section aloud. If the paragraphs share one rhythm, rewrite the flat content first and keep the turn only where it does work.

When one of these is found in review, **treat it as a signal that the surrounding claim may not be worked out.**
Decoration usually appears where an argument is thin — it is covering the gap rather than filling it.
Rewrite the claim, not the phrase.

## Identifier naming in code samples

Full, complete-word identifiers for domain concepts — variables, struct fields, parameters — in every language the book uses, regardless of scope (`catalog`, not `c`; `definition`, not `def`; `amount`, not `a`).

In Go this is a deliberate deviation from the usual short-local-name convention, and Go is the case that needs stating, because its style guidance actively ties name length to scope and distance from declaration.
C#, Python, and TypeScript conventions already favour full words.
The rule is written for all of them so that a Go sample and a C# sample in the same chapter read the same way.

**The reason is this book's reader, not a maintainer's convenience**, and the distinction decides the exceptions below.
Most readers do not write Go, and are already spending attention on `:=`, receivers, and the comma-ok idiom before they reach the argument the sample exists to make.
A truncated domain noun is one more thing to decode, in a sample they will read once and never return to.
This is **Write Go for a reader who does not know Go**, applied to names.

The test for every exception: **is this identifier's meaning recoverable from the line it appears on, by someone who does not know the codebase?**

- **Structural particles**, fixed in meaning across all code in that language rather than within one project: `err`, `ok`, `ctx`, loop indices (`i`, `j`), generic type parameters (`T`). They are exempt from being renamed, not from being explained — `ok` still gets its one-line gloss at first appearance, like any other Go-specific idiom.
- **Method receivers** keep Go's ordinary one- or two-letter convention (`func (c *Catalog) Get(...)`). The receiver's type is on the same line, and a spelled-out receiver stops looking like the Go the reader will meet everywhere else. This does **not** extend to ordinary parameters, which get full words however short the function is: `func (b *Billing) Charge(customerID uuid.UUID)`, never `Charge(m uuid.UUID)`.
- **Type shadowing.** An identifier is not expanded when the full word would be textually identical to its own type name — a `querier`-typed parameter stays `q`, not `querier querier`, since that shadows the type and makes it unreferenceable by name for the rest of the scope.
- **Quoted code is quoted.** Real lines from FlowCore, a standard library, or anyone else's published API keep the names they have. Renaming them turns a quotation into a paraphrase, and the book's claim to be showing real code rests on the difference. Where a real signature carries a name that will not read, gloss it in a comment rather than editing the source.

When in doubt, use the full word.
The exceptions are meant to be rare, not a broad loophole.

Adopted from FlowCore's decision 18 (`~/s/flowcore/docs/decisions.md`), on different grounds and with a narrower exception list; this book's version is `docs/DECISIONS.md`, decision 49.
