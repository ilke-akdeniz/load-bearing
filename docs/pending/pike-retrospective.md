# Pike's 2023 Retrospective: Source Material

Working document, in the shape of `docs/pending/ai-material.md` and `docs/pending/speculative-abstraction.md`.
The passages are gathered here once so that the chapters owed them agree with each other.

**Source.** Rob Pike, *What We Got Right, What We Got Wrong* — closing talk at GopherConAU, Sydney, 10 November 2023, published as text with slides on his own site.
A local copy is at `~/c/TechIter/load-bearing/pike-right-wrong.html`.
This is primary: his words, his site, and he says up front that he speaks only for himself rather than for the Go team or Google.

**Read it rather than working from this file** when drafting a chapter that uses it.
Everything below is an excerpt chosen for one argument, which is exactly the partial reading `CLAUDE.md` warns against.

## Why the document is unusual, and what makes it worth a file

It is a designer publishing a list of his own project's mistakes, fourteen years in, with the reasoning attached.
That is rare enough to be worth using carefully rather than mining for quotes.

Two properties make it useful to this book in particular.
He repeatedly separates a decision from the conditions that made it right at the time.
And he is explicit that much of what people argue about is not the kind of thing that has a right answer — which is chapter 02's subject stated by someone with every reason to claim otherwise.

## Already used

**Chapter 15** takes the concurrency section: Ousterhout's *threads are bad*, whose situation was pthreads in a particular kind of program and which Google banned company-wide anyway; and Pike's own admission that the concurrency use cases were server software, that the team should have said so, and that the confusion between concurrency and parallelism probably drove some programmers away.
See decisions 72 and 73. Nothing else from the talk is in the book yet.

## Material owed to other chapters

### Chapter 02 — confidence does not track the kind of claim

Pike, setting up the talk, says that what is good and bad in a programming language is largely a matter of opinion rather than fact — **despite the certainty with which people argue about even the most trivial features**, of Go or of anything else.

Chapter 02's mechanism is that tone does not vary with authority, so a Style question and a Law arrive sounding alike.
This is that observation made by a language designer about arguments over his own language, which is a stronger witness than the book can otherwise get.
It is one paragraph in 02, not a section, and it belongs near the existing *why the kinds get confused* material.

### Chapter 09 — a compatibility promise, priced by the person who made it

He lists locking the language down with a compatibility guarantee at 1.0 among the things the project got right, says he finds it puzzling that most other projects have resisted doing the same, and states the trade in one line: there is a cost to maintaining strong compatibility, and it **blocks feature-itis**.

Chapter 09 owns *once published, it is forever* and the add-only rule.
What this supplies is the other half — somebody who paid the cost deliberately, saying what it bought.
The chapter currently argues the constraint; this is a case of the constraint being adopted on purpose as a feature, which is a different and more useful thing than a warning.

### Chapter 21 — an Idiom that limited the people who invented it

The strongest piece in the talk for this book, and it is not about Go's users.

On why generics took Go more than a decade: he says that although he would not change a thing about how interfaces worked, **they colored the team's thinking in ways it took more than a decade to correct**.
Interfaces were the bedrock, so every proposed form of polymorphism had to be reconciled with them, and finding a way through took several aborted implementations and outside help from type theorists.

Chapter 21 takes Idioms seriously rather than dismissing them.
This is an Idiom's designers reporting that the Idiom bounded what they could imagine — which is a cost the chapter should be able to name without reaching for a community that got it wrong.
It also inverts the usual telling: the failure is not that people obeyed the convention thoughtlessly, but that the convention shaped the thinking of the people best placed to see past it.

### Chapter 21 — a deviation from Idiom, defended by Forces

The early Go compiler was written in C rather than self-hosted or built on LLVM, against what the language community expected.
His account of why is Forces reasoning without the vocabulary: bootstrapping needs an existing language; writing a compiler in the language you are designing tends to produce a language that is good for writing compilers; and the C compiler they already had made segmented stacks cheap to add where a toolkit would have made it infeasible.
Then the line that matters: unorthodox as it was, it helped them move fast, some people were offended, and **it was the right one for us at the time**.

Chapter 21's contents already promise *when to deviate, and how to pay for it — declare it, document the reason, keep it narrow*.
This is a worked instance with all three, including the later translation of the compiler to Go once the reason had expired.
Pair it with FlowCore's decision 18, which is the same shape at a much smaller scale.

### Chapter 13 — lower confidence, and worth checking before use

The aside on async/await: it is easier for implementers to build or retrofit, and it pushes some complexity back onto the programmer, producing what Bob Nystrom named *colored functions*.

This is adjacent to chapter 13 rather than in it.
Chapter 13 is about patterns that dissolve when the language has the feature; this is about a feature that creates work the programmer must then carry, which is closer to an inverse.
Do not force it. If it fits anywhere it may be chapter 20's distributed-services section, or nowhere.

**2026-08-23: nowhere, on the evidence of chapter 20 being drafted.** Coloured functions is an observation about what a language feature costs its users, not about a domain's force profile, and 20's distributed section is almost entirely chapter 07's material cited. Forcing it in would have been a fifth thing in a section that adds one. Leaving it recorded here in case chapter 21 or 23 wants it.

### Chapter 05 — background rather than evidence

The origin story: the problems the project set out to address were controlling dependencies, working with large teams and changing personnel, maintainability, testing, and multicore.
The famous 45-minute build was not a slow compiler but a dependency structure.

Chapter 05 owns dependency structure and does not need this to make its argument.
Useful as context if the chapter ever wants a case where dependency cost drove the creation of a language, and not otherwise.

## Where each piece lands

| Piece | Chapter | Size | Status |
|---|---|---|---|
| Ousterhout's ban; the concurrency admission | 15 | a section | **done** |
| Confidence does not track the kind of claim | 02 | a paragraph | owed, chapter at draft |
| Compatibility priced by the person who paid it | 09 | a passage | owed, chapter at draft |
| Interfaces coloured their own designers' thinking | 21 | a section | owed, chapter not started |
| The compiler in C, as a declared deviation | 21 | a passage | owed, chapter not started |
| async/await and coloured functions | 13 or 20 | uncertain | check the fit first |
| The 45-minute build | 05 | background | probably not needed |

## The decision on chapters already at draft

**Record now, apply when the chapter is next open.**
Chapters 02, 05, 09, and 13 are at **draft**, and the additions above wait.

Three reasons.

Applying material to four finished chapters at once means four review cycles running in parallel, which is the batching the project avoids everywhere else.
Material of this kind is strongest when the chapter is live, because the argument can be shaped around it — chapter 15's use of this source worked for that reason, and a quotation bolted onto a finished chapter is the decoration the register rules exclude.
And the precedent already exists and worked: `docs/pending/ai-material.md` holds material owed to 02 and 03 in exactly this way.

**The test that would override this: a revisit can wait, a contradiction cannot.**
The talk was checked against what is already shipped and contradicts none of it.
Had it made a drafted chapter wrong rather than incomplete, the fix would not be a pending item.
