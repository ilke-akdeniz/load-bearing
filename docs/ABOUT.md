# About this book

How *Load-Bearing* is put together. The book itself starts at [`README.md`](../README.md); the table of contents is in [`00_toc.md`](../00_toc.md).

## Chapter rubric

Each chapter follows this shape:

1. **The claim** — one sentence, and the chapter opens on it.
2. **The demonstration** — code, in two or more languages when the point concerns translation.
3. **Why the claim holds** — the mechanism, never the authority. No argument from who said it.
4. **Where the claim doesn't apply** — mandatory, with a worked counter-example.
5. **What the claim costs** — every choice has a bill.
6. **How to recognize the failure** — what it looks like in a real codebase when someone got this wrong.

**Part IV is the exception.**
[Chapters 17](../17_behaviour-placement_z47a.md), [18](../18_tdd-and-mocks_u8eu.md) and [19](../19_abstraction-as-insurance_4jk6.md) are case studies in [chapter 16](../16_principle-loses-scope_b86v.md)'s claim rather than claims of their own.
So each opens on the advice as it actually travels and on what its source said, and its mandatory counter-example asks when following the compressed version is right — the same rule, framed for a chapter that makes no claim to bound.

The argument's last paragraph hands off to the next chapter, written as prose with no label.
Then the back matter, after a divider: a **Sources** section listing every work the chapter cites, with links, and last a navigation row.

## Conventions

**Languages.**
Go carries most of the examples, since the running example is written in it, and Python is the second.
Java and C# appear where a point needs a class-based contrast — Java mostly in the chapters on missing language features and on behaviour placement, C# in the early structural chapters.
SQL runs through seven chapters, and C, Rust, and JavaScript appear once or twice each, where nothing else would show the point.

**Running example.**
[FlowCore](https://github.com/ilke-akdeniz/flowcore) supplies examples in Parts II, IV, and V — its 38-entry decision log means the reasoning behind a choice can be quoted rather than guessed at.
Each appearance shows a different facet, other domains supply the contrast, and no chapter rests on FlowCore alone.

## Files

One chapter per file at the book root, `NN_slug_ID.md`.
The four characters at the end are permanent: a chapter's number and its slug can both change, and cross-references point at the identifier so that renumbering the book cannot silently repoint them.

Working documents live in `docs/`:

- `docs/DECISIONS.md` — editorial decisions, with the reasoning and the options that lost.
- `docs/LEDGER.md` — concept and example ownership, one owner per concept. Read before drafting, updated after.
- `docs/STATUS.md` — which chapter is at which status.
- `docs/pending-tasks/` — work owed to chapters that are already drafted, and the gaps the book knows it has.

## License

The prose is licensed **[CC BY 4.0](../LICENSE)** — read it, quote it, translate it, teach from it, build on it.
The one condition is credit: name the author, link back, and say if you changed anything.

**Code samples are CC0** — public domain.
Lift any snippet into your own project without attribution.

## How to cite

> Akdeniz, M. *Load-Bearing: Which Software Principles Hold, and Where They Stop.*
> https://github.com/ilke-akdeniz/load-bearing — licensed CC BY 4.0.

If you make something with visible traces of this book — a course, a talk, a video, an article — the attribution above and a link are what the license asks for.
