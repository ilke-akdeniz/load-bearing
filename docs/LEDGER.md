# Concept Ledger

Anti-repetition control.
Every concept, example, and code demonstration is **owned by exactly one chapter**.
Other chapters may reference it in a sentence and link — never re-explain it.

**Rule before drafting any chapter:** read this file.
If a concept is already owned, the new chapter gets one line and a cross-reference, not a recap.

**Rule after drafting any chapter:** add what it claimed here.

## Format

`concept` → owning chapter → the canonical one-line statement → how others may refer to it

---

## Concepts

| Concept | Owner | Canonical statement | Others may say |
|---|---|---|---|
| The five levels | 02 | Advice is one of five kinds — Law, Force, Principle, Idiom, Style — and the kind sets its authority | "a Law / an Idiom (Ch. 02)" |
| Classification test | 02 | Five questions that place a claim in one of the five kinds | "run the test (Ch. 02)" |
| Why the kinds get confused | 02 | Tone doesn't vary with authority; advocacy compresses; monoculture makes Idioms feel universal | one clause, cite 02 |
| Law inert vs Principle wrong | 02 | A Force decides whether a Law *binds*; it decides whether a Principle is *right* | one clause, cite 02 |
| Forces as inputs | 03 | Forces are properties of the situation, not advice | "the Force is X (Ch. 03)" |
| Law grading A/B/C | 04 | Theorem, near-tautology, or empirical constant — different standing | "Grade A (Ch. 04)" |
| Acyclic dependency | 05 | A cycle makes two components one unit of comprehension, test, and change | "the Direction Rule (Ch. 05)" |
| Layering as line-shaped DAG | 05 | Layering is the special case where the dependency DAG is a total order | one clause, cite 05 |
| Information hiding / Hyrum | 05 | What is observable will be depended upon | cite 05 |
| Check-then-act / TOCTOU | 06 | Between the check and the act, the world moved | "TOCTOU (Ch. 06)" |
| Only the lock-holder enforces | 06 | A rule over rows you haven't read can't be enforced by code that hasn't read them | cite 06 |
| Exactly-once impossible | 07 | Two Generals ⇒ at-least-once plus idempotency | cite 07 |
| Memory hierarchy ~6 orders | 08 | Register to network spans about a million-fold | cite 08 |
| Conway / Brooks / Lehman | 09 | Structure mirrors org; adding people to a late project; systems must change | cite 09 |
| Compression + constraint tests | 10 | A pattern earns its name by saving words and ruling something out | cite 10 |
| The scale test | 11 | The same name is trivial at class scale and load-bearing at system scale | "scale test (Ch. 11)" |
| Survives-translation test | 13 | If it disappears when you change language, it was a workaround | cite 13 |
| Smuggled verdict | 14 | Vocabulary arriving with its conclusion attached | cite 14 |
| Principle→movement mechanism | 15 | Observation gets a name, name gets a community, community forgets the conditions | cite 15 |
| Mocks assert about mocks | 17 | A mocked test passes when the real constraint has been deleted | cite 17 |
| Layered packages force exports | 18 | A directory wall requires publishing the helpers it was meant to hide | cite 18 |
| Force-map method | 19 | Read forces, derive principles, check idioms — in that order | cite 19 |
| Domain inversions | 20 | Each domain's dominant force inverts some standard advice | cite 20 |

## Code examples

Each example is used **once**, in its owning chapter.
Reuse requires a different point *and* an explicit callback, never a re-run of the same lesson.

| Example | Owner | What it shows |
|---|---|---|
| Seat reservation race (read-then-update) | 02 | A Law violation: wrong in every language; also reused *within* 02 to show a Force making it inert |
| Manual wiring in Go vs C# | 02 | An Idiom difference: same shape, opposite reception |
| Unique index vs application check | 06 | Only the enforcing layer closes the window |
| Outbox table | 07 | Cross-system atomicity is impossible, so you sequence + retry |
| AoS vs SoA benchmark | 08 | Memory hierarchy beats abstraction |
| Adapter at class vs system scale | 11 | The scale test |
| GoF collapse in 4 languages | 13 | Survives-translation test |
| Bidirectional Order↔Customer | 16 | OOP producing cycles |
| Deleted constraint, passing mock test | 17 | Mocks assert about mocks |
| Store split into a package | 18 | Layered packages force exports |

## Deliberate repetition

Only these ideas may appear more than once, because the book's structure depends on them:

- **The kind of the current material** — every chapter opens by stating it. One line.
- **The mandatory boundary section** — every chapter has one. It is a section, not a repeated argument.
- **FlowCore as running example** — appears across Parts II and V, but each appearance must show a *different* facet.
