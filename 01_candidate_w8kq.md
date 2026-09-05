# Is This Load-Bearing?

> **AccountRepository needs an interface — depend on abstractions.**

Says the code review for your latest commit.

On one hand, the advice sounds reasonable. Everybody knows the maxim "Depend on abstractions", and adding an interface would not hurt anything, right? Still, something in your gut says the interface would be pure drudgery here, with no benefit at all. But that is hard to establish in a convincing way, so you comply with the request and move on.

Notice that the review carries nothing you can object to. It arrives finished with a confident tone, similar to *don't repeat yourself*, *dependencies must not be circular*, or *put braces on the same line*.

This is an uncomfortable position to be in. It feels like as developers, we are sometimes drill-sergeants, sometimes privates, giving and following clear orders with minimal room for interpretation. But maybe, military is not the right field in search for clues about software claims.

## Builders do not guess whether a wall can come out

A builder opening up a kitchen faces the same dilemma with worse consequences. The developer was trying to gauge whether the advice could safely be ignored; the builder is trying to gauge whether the wall can. Is it safe to demolish or is it actually holding the building up?

Nothing about the wall answers that. Plastered and painted, a wall carrying the floor above looks exactly like one put there to divide two rooms. Same thickness, near enough. Same sound when you knock.

So the builder does not examine the wall. They look at what rests on it.

Which way do the floor joists run — parallel to the wall, or across it? Do they end on top of it, or pass over and land somewhere else? Is there a beam or a foundation wall directly below, in line? And so on. Not one of those questions is about the wall. Every one is about the wall's surroundings.

Which is the part with no software equivalent. When a claim arrives in review, there is no inspection to perform. There is the sentence, and there is the confidence of the person who said it — and confidence is a fact about the speaker, not about the claim. The builder has a procedure that does not care about the confidence of the mason who built the wall.

**A wall is not load-bearing by nature. It is load-bearing by circumstance.**

Take the structural wall and turn the floor above it ninety degrees, so the joists now run parallel and land on the two walls at the ends instead. Nothing has been touched. Same bricks, same mortar, same thickness. It is now a partition, and you could take it out on a Saturday.

The software version of that sentence is the first thing this book demonstrates: the same structural advice is wrong in Go but the default shape in C#, and neither version is more correct than the other ([chapter 02](01_the-five-kinds_cjx4.md) works it through). The code did not change. What it was resting on did.

## What is actually pressing down, and where it goes

Ask a builder what a wall carries and you do not get a number, you get three answers, because the loads are different in kind.

- **Dead load** is the permanent weight — the structure, the roof, the floors, the pipes that will still be there in fifty years.
- **Live load** is everything temporary and variable: people, furniture, snow, a room somebody filled with filing cabinets without asking.
- **Lateral load** arrives sideways rather than downward, from wind or from ground movement in an earthquake, and it is the one people picture last, because gravity is intuitive and horizontal force is not.

Those are three separate questions with three separate answers, and a wall can be adequate for two of them.

Software has one word for the whole category. *Requirements* covers the load that will still be there in ten years and the one that arrives from a direction nobody was designing for, and treats them as the same kind of thing.

Then there is where the weight goes. Roofing and flooring rest on joists; joists span between beams; beams carry into girders and so on all the way to the foundation. Every part holds up what is above it and hands the total down. The chain can be walked, one connection at a time, in either direction.

Now try to walk the chain backwards from *the repository needs an interface*. What is that resting on? Somebody's experience, from some codebase, at some size, in an ecosystem where the testing tools worked a particular way. None of which came with the sentence. The advice arrived as a finished conclusion with its supports removed, and there is nowhere to look them up — which is the actual reason these arguments either do not start or do not end. ([Chapter 03](02_forces_f4m5.md) is about the supports, and about how rarely anyone names them.)

## Where a principle stops paying

The last thing worth taking from the building trade is what a limit looks like when you reach it.

The Monadnock Building in Chicago is the tallest load-bearing brick building ever constructed: sixteen rentable storeys, the north half finished in 1891, standing on walls **six feet thick at the base** and eighteen inches at the top. It is still standing. It works. Nothing about it was a mistake.

It is also where the method ran out. Going higher meant thicker walls still, and thicker walls consume the ground floor — the space the building exists to rent. Masonry did not fail structurally. It stopped being worth what it cost.

The proof is in the same building. The south half, finished two years later on a steel frame, delivered **fifteen percent more rentable space at fifteen percent less weight**. One address, two structural strategies, and a measurement of the difference between them.

That is the shape most software advice takes and almost none of it admits to. Not *this is wrong*, but *this was right and has stopped paying*, with nothing marking the moment it turned.

## The part where the analogy runs out

A builder who cannot tell calls a structural engineer. There is a qualification, a professional body, a stamp on a drawing, and liability if the stamp is wrong. In most places you are not permitted to open a wall without one.

There is nobody to call about *the repository needs an interface*. There is no test that settles it, no register of who is qualified to say, and no consequence for whoever is wrong. Which is why the question has to be one you can run yourself, on the spot, in a review comment, with no tape measure.

The rest of this book is an attempt to build that. Not a set of rules to follow — the trade already has plenty of those, and their arriving all in one voice is the problem rather than the solution. What follows is a way of telling what kind of claim you are holding, what it is resting on, and where it stops. The goal is to be able to ask, and to answer:

**Is this claim load-bearing?**

---

## Sources

- *Monadnock Building* — Wikipedia. [en.wikipedia.org/wiki/Monadnock_Building](https://en.wikipedia.org/wiki/Monadnock_Building).
- *What Is a Load-Bearing Structure and How Does It Work?* — Science Insights. [scienceinsights.org](https://scienceinsights.org/what-is-a-load-bearing-structure-and-how-does-it-work/).

---

[← Introduction](README.md)  ·  [Contents](00_toc.md)  ·  [Ch. 02 →](01_the-five-kinds_cjx4.md)
