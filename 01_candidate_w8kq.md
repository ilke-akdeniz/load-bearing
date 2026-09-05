# Is This Load-Bearing?

Someone tells you in review that the repository needs an interface.

You are not certain whether that is a rule or a habit. Neither, if you asked, are they — not because either of you is careless, but because nothing about the sentence carries that information. It arrives finished. It sounds the same as *don't repeat yourself*, which is sometimes wrong, and the same as *dependencies must not be circular*, which is never wrong, and the same as *put braces on the same line*, which is not the kind of thing that can be wrong at all. Four sentences, four completely different standings, one tone of voice.

That is an uncomfortable position to be in, and it is worth noticing that another trade is in it constantly and has stopped finding it difficult.

## Nobody guesses about a wall

A builder opening up a kitchen faces the same question with worse consequences. There is a wall in the way. Is it holding the building up?

Nothing about the wall answers that. Plastered and painted, a wall carrying the floor above looks exactly like one put there to divide two rooms. Same thickness, near enough. Same sound when you knock.

So the builder does not examine the wall. They look at what rests on it.

Which way do the floor joists run — parallel to the wall, or across it? Do they end on top of it, or pass over and land somewhere else? Is there a beam or a foundation wall directly below, in line? Is it an exterior wall, in which case the answer is almost always yes? Not one of those questions is about the wall. Every one is about the wall's surroundings.

Which is the part with no software equivalent. When a claim arrives in review, there is no inspection to perform. There is the sentence, and there is the confidence of the person who said it — and confidence is a fact about the speaker, not about the claim. The builder has a procedure that does not care who is holding the tape measure.

## The same bricks, doing a different job

Push on this and it gets stronger, because a wall's status is not a property of the wall at all.

Take the structural wall and turn the floor above it ninety degrees, so the joists now run parallel and land on the two walls at the ends instead. Nothing has been touched. Same bricks, same mortar, same thickness. It is now a partition, and you could take it out on a Saturday.

**A wall is not load-bearing by nature. It is load-bearing by circumstance.**

The software version of that sentence is the first thing this book demonstrates: the same wiring code is unremarkable in Go and gets sent back in review in C#, and neither version is more correct than the other ([chapter 02](01_the-five-kinds_cjx4.md) works it through). The code did not change. What it was resting on did.

Once you have seen that in a wall, the software case stops sounding like relativism and starts sounding like the obvious thing it is.

## What is actually pressing down, and where it goes

Ask a builder what a wall carries and you do not get a number, you get three answers, because the loads are different in kind.

**Dead load** is the permanent weight — the structure, the roof, the floors, the pipes that will still be there in fifty years. **Live load** is everything temporary and variable: people, furniture, snow, a room somebody filled with filing cabinets without asking. **Lateral load** arrives sideways rather than downward, from wind or from ground movement in an earthquake, and it is the one people picture last, because gravity is intuitive and horizontal force is not.

Those are three separate questions with three separate answers, and a wall can be adequate for two of them.

Software has one word for the whole category. *Requirements* covers the load that will still be there in ten years and the one that arrives from a direction nobody was designing for, and treats them as the same kind of thing.

Then there is where the weight goes. Roofing and flooring rest on joists; joists span between beams; beams carry into girders or columns; columns deliver to the foundation; the foundation spreads the lot into the soil. Every part holds up what is above it and hands the total down. The chain can be walked, one connection at a time, in either direction.

Now try to walk the chain backwards from *the repository needs an interface*. What is that resting on? Somebody's experience, from some codebase, at some size, in an ecosystem where the testing tools worked a particular way. None of which came with the sentence. The advice arrived as a finished conclusion with its supports removed, and there is nowhere to look them up — which is the actual reason these arguments do not end. ([Chapter 03](02_forces_f4m5.md) is about the supports, and about how rarely anyone names them.)

## A number for the doubt

Buildings are not designed to exactly the load anyone expects. They are designed to a **factor of safety** — in ordinary American practice, 1.5, meaning the structure is built to carry half again as much as the calculation says it will ever see. When an existing building is assessed against earthquake forces the minimum drops to 1.0, which is a way of saying: we would not build this today, and we are not going to demolish it either.

Argue with the number if you like; engineers do. The point is that there is one. The gap between what is expected and what is survivable has been written down, so it can be checked and revised.

Nothing you have ever been told about software came with a margin. *Always program to an interface* does not say how far past its range it stays sensible, or what it costs when it is wrong, or which situations it was calculated for. It is stated at full strength, everywhere, forever — and then quietly abandoned in the situations where it fails, without anybody recording that it was.

## Where a principle stops paying

The last thing worth taking from the building trade is what a limit looks like when you reach it.

The Monadnock Building in Chicago is the tallest load-bearing brick building ever constructed: sixteen rentable storeys, the north half finished in 1891, standing on walls **six feet thick at the base** and eighteen inches at the top. It is still standing. It works. Nothing about it was a mistake.

It is also where the method ran out. Going higher meant thicker walls still, and thicker walls consume the ground floor — the space the building exists to rent. Masonry did not fail structurally. It stopped being worth what it cost.

The proof is in the same building. The south half, finished two years later on a steel frame, delivered **fifteen percent more rentable space at fifteen percent less weight**. One address, two structural strategies, and a measurement of the difference between them.

That is the shape most software advice takes and almost none of it admits to. Not *this is wrong*, but *this was right and has stopped paying*, with nothing marking the moment it turned. The load-bearing wall is not the wrong answer. It is the answer to a shorter building.

## The part where the analogy runs out

A builder who cannot tell calls a structural engineer. There is a qualification, a professional body, a stamp on a drawing, and liability if the stamp is wrong. In most places you are not permitted to open a wall without one.

There is nobody to call about *the repository needs an interface*. There is no test that settles it, no register of who is qualified to say, and no consequence for whoever is wrong. Which is why the question has to be one you can run yourself, on the spot, in a review comment, with no tape measure.

The rest of this book is an attempt to build that. Not a set of rules to follow — the trade already has plenty of those, and their arriving all in one voice is the problem rather than the solution. What follows is a way of telling what kind of claim you are holding, what it is resting on, and where it stops. Each chapter takes a piece of common advice, works out which kind of thing it is, and shows the situations in which it stops applying, on the principle that a claim whose limits nobody can find is usually too vague to use.

Every chapter ends by handing you a question rather than an instruction. *Can I change the other side?* *Which fact about our situation would have to change for this to be the wrong choice?* *Whose name is against this, and do they have the most context?* Those are the instruments. This is the one they are all versions of, and it is three words long.

Before you knock the wall through: is this load-bearing?

The next chapter sets out the five kinds of claim this book sorts things into, and how much authority each of them carries.

---

## Sources

- *Monadnock Building* — Wikipedia. [en.wikipedia.org/wiki/Monadnock_Building](https://en.wikipedia.org/wiki/Monadnock_Building).
- *What Is a Load-Bearing Structure and How Does It Work?* — Science Insights. [scienceinsights.org](https://scienceinsights.org/what-is-a-load-bearing-structure-and-how-does-it-work/).

---

[← Introduction](README.md)  ·  [Contents](00_toc.md)  ·  [Ch. 02 →](01_the-five-kinds_cjx4.md)
