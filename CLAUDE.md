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

## The five levels

The spine. Every chapter classifies its material against these.

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

Every chapter has a mandatory *Where this doesn't apply* section containing a worked case, not a hedge.
"This always applies" is never an acceptable answer.
If a boundary cannot be found, that is evidence the claim is too vague to be useful — not evidence that it is universal.

This applies to Laws too.
They don't stop being true, but they stop being *relevant*, and knowing when they stop mattering is the same skill.

## Chapter rubric

Each chapter follows this shape:

1. **The claim** — one sentence.
2. **The demonstration** — code, in two or more languages when the point concerns translation.
3. **Why it holds** — the mechanism, never the authority. No argument from who said it.
4. **Where this doesn't apply** — mandatory, with a worked counter-example.
5. **What it costs** — every choice has a bill.
6. **How to recognize the failure** — what it looks like in a real codebase when someone got this wrong.

## Writing style

**Simple language, precise terminology.**
Plain words wherever they work, but name the real terms — Transaction Script, information hiding, TOCTOU, Hyrum's Law — because the reader needs the vocabulary to find the literature.
Explain a term once, at its owning chapter, then use it.

**A code demonstration for every major claim.**
Not an illustration bolted on afterwards; the code should be the argument.
Go, C#, and Python carry most examples; Rust, TypeScript, C, and SQL appear where a point needs them.

**Mechanism over authority.**
Never "Fowler says." Always "here is what happens, and here is why."
Cite people for provenance, never as proof.

**Provenance markers.** Tag claims whose standing could be mistaken:

- `(established)` — citable, standard, uncontroversial
- `(contested)` — genuinely disputed by competent people
- `(ours)` — this book's synthesis, not established terminology

The five-level model itself is `(ours)`.

**Running example.**
FlowCore — a Go workflow library at `~/s/flowcore` with a 38-entry decision log — supplies examples in Parts II and V, because its reasoning was recorded at the time rather than reconstructed afterwards.
Each appearance must show a *different* facet. No chapter rests on FlowCore alone.

## Markdown conventions

For clean diffs and portable rendering.

- **One sentence per line.** Break at `.` `?` `!`. A one-word change is then a one-line diff.
- **Don't split mid-sentence.** A clause after `;` `:` or `—` stays on its sentence's line.
- **Blank line between block elements**, and after every heading before its content.
- **Never two blank lines in a row.** File ends with a single newline.
- **Lists:** one item per line, no blank lines between items in a tight list.
- **Code fences and tables are literal** — never reflow or sentence-split their contents.
- **Bold lead-ins** (`**Term.**`) stay on the same line as the sentence they introduce.

## Files

- Chapters at the repo root: `NN_slug.md`, matching the TOC in `00_toc.md`.
- Working documents in `docs/`.
- `00_toc.md` carries the status table — update it when a chapter's status changes. The README is the landing page and should stay short.

## How we work

The author leads, reviews every chapter, and makes the editorial calls.
Claude drafts and makes local writing decisions.

**Ask before** changing the five-level model, the chapter rubric, the TOC structure, or anything recorded in `docs/DECISIONS.md`.
Those are the author's, and they land in the decision log first.

Draft **one chapter at a time** and stop for review.
Do not batch chapters — the steering between them is where the book's judgments are made.

Record substantive editorial decisions in `docs/DECISIONS.md` using the existing shape: **Context / Options / Decision / Why / Consequence.**
Note who originated what; the log doubles as the authorship record for an AI-assisted work.

## Git

**Never commit. Never push.**

After making changes:

1. Stage them — `git add -A`, or the specific paths when only part of the work is ready.
2. Print a recommended commit message to standard output.

The author reviews the staged diff and runs the commit.
Keep the recommendation short: a subject line, and a body only when the change needs a reason rather than a description.

## Register

Direct, concrete, willing to say a popular idea is wrong and why.
Not breezy, not academic, no throat-clearing.
The reader is an experienced engineer who has been burned by advice that didn't fit.

Avoid: "best practice," "clean code," "simply," "just," and any sentence that would survive being deleted.
