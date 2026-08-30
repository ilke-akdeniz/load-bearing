# Pending Material — Index

Work owed to chapters that are already at **draft**.
Listed here because a drafted chapter is not re-read on its own, and a decision entry is only consulted when reversing something.

Permanent project state lives in [STATUS.md](../STATUS.md), not here.

## Pending revisits

None.
Slice 1 of the final sweep discharged the last of them — two routed, five retired.
Decisions 110 and 111 record each disposition and the reason; 111 is the author's review, which cut two of the four the draft had routed.

## The last-chapter idea — discharged

[last-chapter-idea.md](last-chapter-idea.md) produced [chapter 23](../../23_assigned-to-the-team_3fjx.md), and the four slices were run over that chapter on 2026-08-29.
What landed: the artifact chain, ownership and its two mechanisms, the business rules as the root, the force map, people not being cogs, a senior engineer not being somebody with ten years' service, the brutality of a handoff, meetings, and the pointing-session and *we're agile* tells.
Routed during the slice: *architecture is not diagrams or tech stack choices* — the notes' sharpest statement of the chapter's own thesis, which had not made it in.

Retired, with the reason:

- **The estimate**, and *time estimates are harmful games*. Cut by the author in the restructure from six steps to four artifacts. It is not an artifact the ownership claim governs; it was a consequence of sequence, and the sequence framing went with the six-step draft.
- **1:1s and performance reviews as ceremony.** Not development artifacts, so outside the claim.
- **Agile is overrated**, as a claim. It survives only as conditioned symptoms in *how to recognize the failure*, which is where a verdict has to live.
- **Stages, transitions, deliverables, playbooks**, and **the utopia framing with its closing counsel.** Both cut by the author on review.

Still open, and not a chapter matter: the note about changing the book's title.

## Known coverage gaps

Recorded when the contents page was reduced to a table of contents, because these were the only statements in it that existed nowhere else.
They are limits the book has chosen to live with, not work queued, and they stay here so that the choice is written down somewhere.

[Chapter 16](../../16_tdd-and-mocks_u8eu.md) does not cover the wider empirical literature on test-first development: the meta-analyses are paywalled and were not read, so the chapter rests on the primary studies it could reach.

Interface-per-class — the convention that every class is published behind an interface of its own, regardless of what the interface is for — is owned by no chapter.
[Chapter 17](../../17_abstraction-as-insurance_4jk6.md) takes the case where the interface exists to keep a dependency swappable, and stops there.

**Corrected 2026-08-26.** This gap previously also named the dependency-injection container, which is no longer true: [chapter 01](../../01_the-five-kinds_cjx4.md) classifies it as an Idiom and separates it from the Principle it travels with, and [chapter 20](../../20_idioms_7nkn.md) gives its conditions.
The same entry said [chapter 17](../../17_abstraction-as-insurance_4jk6.md) "reaches the testing half of the question and no further", which understated it — that chapter has six subsections on the swappability case and one on tests.
