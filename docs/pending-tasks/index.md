# Pending Material — Index

Work owed to chapters that are already at **draft**.
Listed here because a drafted chapter is not re-read on its own, and a decision entry is only consulted when reversing something.

Permanent project state lives in [STATUS.md](../STATUS.md), not here.

## Pending revisits

None.
Slice 1 of the final sweep discharged the last of them — two routed, five retired.
Decisions 110 and 111 record each disposition and the reason; 111 is the author's review, which cut two of the four the draft had routed.

## Known coverage gaps

Recorded when the contents page was reduced to a table of contents, because these were the only statements in it that existed nowhere else.
They are limits the book has chosen to live with, not work queued, and they stay here so that the choice is written down somewhere.

[Chapter 18](../../18_tdd-and-mocks_u8eu.md) does not cover the wider empirical literature on test-first development: the meta-analyses are paywalled and were not read, so the chapter rests on the primary studies it could reach.

Interface-per-class — the convention that every class is published behind an interface of its own, regardless of what the interface is for — is owned by no chapter.
[Chapter 19](../../19_abstraction-as-insurance_4jk6.md) takes the case where the interface exists to keep a dependency swappable, and stops there.

**Corrected 2026-08-26.** This gap previously also named the dependency-injection container, which is no longer true: [chapter 02](../../02_the-five-kinds_cjx4.md) classifies it as an Idiom and separates it from the Principle it travels with, and [chapter 22](../../22_idioms_7nkn.md) gives its conditions.
The same entry said [chapter 19](../../19_abstraction-as-insurance_4jk6.md) "reaches the testing half of the question and no further", which understated it — that chapter has six subsections on the swappability case and one on tests.
