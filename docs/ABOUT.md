# About this book

How *Load-Bearing* is put together. The book itself starts at [`README.md`](../README.md); the table of contents is in [`00_toc.md`](../00_toc.md).

## Chapter rubric

Each chapter follows a fixed shape:

1. **The claim** — one sentence.
2. **The demonstration** — code, in two or more languages when the point concerns translation.
3. **Why the claim holds** — the mechanism, never the authority. No argument from who said it.
4. **Where the claim doesn't apply** — mandatory, with a worked counter-example.
5. **What the claim costs** — every choice has a bill.
6. **How to recognize the failure** — what it looks like in a real codebase when someone got this wrong.

Then the back matter: a **Sources** section listing every work the chapter cites, with links, and a line handing off to the next chapter.

## Conventions

**Languages.**
Go, C#, and Python carry most examples.
Rust, TypeScript, C, and SQL appear where a point needs them — particularly in the chapters on translation and on domain inversions.

**Running example.**
[FlowCore](https://github.com/ilke-akdeniz/flowcore) supplies many examples in Parts II and V — its 38-entry decision log means the reasoning behind a choice can be quoted rather than guessed at.
Other domains supply the contrast, and no chapter rests on FlowCore alone.

## Files

One chapter per file at the book root, `NN_slug.md`.
This README is the entry point.

Working documents live in `docs/`:

- `docs/DECISIONS.md` — editorial decisions, with the reasoning and the options that lost.
- `docs/LEDGER.md` — concept and example ownership, one owner per chapter. Read before drafting, updated after.

## License

The prose is licensed **[CC BY 4.0](LICENSE)** — read it, quote it, translate it, teach from it, build on it.
The one condition is credit: name the author, link back, and say if you changed anything.

**Code samples are CC0** — public domain.
Lift any snippet into your own project without attribution.

## How to cite

> Akdeniz, M. *Load-Bearing: Which Software Principles Hold, and Where They Stop.*
> https://github.com/ilke-akdeniz/load-bearing — licensed CC BY 4.0.

If you make something with visible traces of this book — a course, a talk, a video, an article — the attribution above and a link are what the license asks for.
