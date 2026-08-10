# Grading a Law

*This chapter is about **Law** alone — the top of the ladder — and about the fact that the top rung has three steps. Chapter 02 established that a Law is true by the mechanics of computation and that a Force can render it inert. This chapter says what kind of true, and what that changes.*

## The claim

**Not all Laws are the same kind of true, and the kind decides what you can do about one.**

Against a proven theorem you can only change which assumptions hold. Against a near-tautology you can only check whether the words apply to you. Against an empirical constant you can measure, because the number may have moved since somebody wrote it down.

Three kinds of true, three different moves, and no others available.

## Three grades

| Grade | What makes it true | What would falsify it | The only move available |
|---|---|---|---|
| **A** — theorem | a proof, from stated assumptions | nothing, unless the proof is wrong | change which assumptions hold |
| **B** — near-tautology | what the words mean | nothing; the terms may simply not apply | check whether the words describe you |
| **C** — empirical | observation of the world | a measurement | measure it yourself |

The grades are not a ranking of importance, and treating them as one is the first mistake. They rank *how firmly the thing is true*, which is a different question from how much it bears on your program. A Grade A theorem about distributed consensus is irrelevant to a single-process command-line tool, while the Grade C span between cache and main memory can dominate every design decision in a game engine.

---

## The demonstration

### Grade A: the move is to change the model

A theorem is proved from assumptions, and the assumptions are where all the engineering lives. You do not beat a theorem. You arrange to be somewhere its assumptions do not hold.

Take message delivery. Inside one process, delivering a job exactly once is not an achievement — it is the default, because the channel cannot lose anything:

```go
ch := make(chan string, 1)
ch <- "job-1"
fmt.Println("in-process: received", <-ch, "— delivered exactly once")
```

Now cross a network, and one assumption changes: a message can be lost. Not the request — the *acknowledgement*, after the work is done:

```go
// The work happens. The reply does not arrive.
func callWithLostAck(id string) error {
	charge(id)
	return errors.New("timeout")
}
```

The caller sees a timeout and has to decide something it does not have the information to decide:

```text
attempt 1: timeout — retry? the caller cannot tell
attempt 2: timeout — retry? the caller cannot tell
attempt 3: timeout — retry? the caller cannot tell
charges actually applied: 3
```

Three charges, one intended. The caller was never careless; it could not distinguish *the request never arrived* from *the request arrived and the reply was lost*, and those two require opposite actions.

**What matters for grading is the shape of the escape.** The in-process version is not a cleverer implementation of the networked one. It is the same problem with an assumption removed, and that is the only thing that ever works against a Grade A result. Chapter 07 owns this particular theorem and what you build once you accept it.

The practical form of the rule: **when you meet a Grade A Law, stop looking for a way round the conclusion and go read the assumptions.** They are always listed, because a proof cannot exist without them, and they are the only negotiable part.

### Grade B: the move is to check whether the words apply

A near-tautology is not proved so much as unpacked. Its truth is already in the terms, and reading it feels less like learning something than like noticing something.

> A cache needs an invalidation strategy.

Unpack it. A cache is a copy kept because reading the original costs too much. If the original changes and the copy does not, the copy is wrong. So "a cache with no invalidation strategy" means "a copy that is allowed to go wrong" — which is either a decision you made deliberately or a bug you have not met yet. There is no third possibility, and no proof was required to see it.

```go
// Read once at startup, never refreshed.
var rate = mustFetchRate()
```

Whether this is a defect depends entirely on one thing:

```text
rate is a compile-time constant     no original to drift from — inert
rate is edited in an admin screen   every process serves a stale value
                                    until someone restarts it
```

**The escape is not to argue with the Law. It is to find that the words do not describe you.** In the first case there is no cache, in the strict sense — there is a precomputed value, and nothing can make it wrong. The Law is true and has nothing to act on, which is chapter 02's distinction seen from underneath.

This is why Grade B claims feel unfalsifiable and are not vacuous. "Dependencies must be acyclic" is Grade B: a cycle makes two things one unit of comprehension, test, and change, because that is what a cycle is (Ch. 05 works it through). You cannot violate it. You can find that the two things were never separate units, in which case nothing was violated because nothing was joined.

### Grade C: the move is to measure, because the number moved

An empirical Law describes the world rather than deriving from a proof, and the world is under no obligation to hold still. Every Grade C claim carries a magnitude, and the magnitude is the part people quote and stop checking.

Hyrum's Law is Grade C. It says that with enough users, every observable behaviour of your system ends up depended on regardless of what you documented (Ch. 05 owns the Law and what to do about it). Nothing proves that. It is an observation about what people do, and its strength depends on how many people, how observable, and how long.

Two languages met that observation and moved in opposite directions.

Go randomizes map iteration, so that order cannot be depended on:

```text
$ go run .        b a c d e
$ go run .        d e b a c
$ go run .        a c d e b
```

Python did the reverse. Dictionary insertion order started as an implementation detail of a faster dict in 3.6, became so widely relied upon that it was made a guarantee in 3.7, and is now part of the language:

```text
$ python3 -c "d={'b':1,'a':2,'c':3}; print(list(d))"
['b', 'a', 'c']
$ python3 -c "d={'b':1,'a':2,'c':3}; print(list(d))"
['b', 'a', 'c']
```

Neither is a mistake. Go decided the freedom was worth more than the convenience and made the behaviour impossible to depend on; Python found that the dependency had already formed at a scale that made removal impractical, and promoted it to a promise.

**What makes this Grade C is that both outcomes were available.** No proof forced either. And notice what happened to the claim in Python's case: the observable behaviour that "will be depended upon" became the documented behaviour, which means the Law's own prediction, taken seriously, changed the thing it was predicting.

The practical form: **a Grade C constant is a measurement someone took, somewhere, at some time.** Cache latencies, failure rates, how long a team takes to onboard, how many users notice a two-second delay. Quoting the number is not the same as having it. Chapter 08 works through the ones that come with arithmetic.

---

## Why it holds

The grades are not three flavours of the same thing. They differ in **where the claim's authority comes from**, and that is what makes the available moves different.

**A theorem's authority is internal.** It follows from its assumptions and nothing else, which is why it cannot be refuted by evidence and why arguing with it is a category error. It is also why the assumptions are always stated — a proof that hid them would not be a proof. That is the crack, and it is deliberate: the theorem tells you exactly where to push.

**A near-tautology's authority is definitional.** It is true because of what the words pick out, so the only question it admits is whether those words pick out anything in your program. This is why Grade B claims are the easiest to state and the hardest to argue with, and also why they can evaporate without ever being wrong.

**An empirical claim's authority is a measurement**, taken by someone, under conditions. It can therefore drift, and it does. The memory hierarchy's shape has changed several times in forty years. Team communication overhead depends on tools that did not exist when it was first counted. When a Grade C number is repeated for long enough it starts to sound like a theorem, and that is the specific way this grade goes wrong.

There is a fourth possibility that the grading exists to catch: **the claim is not a Law at all.**

The test is chapter 02's, applied honestly. *Can circumstances make this bad advice?* A Law cannot become bad advice, because it is not advice — it describes what happens. "Prefer composition over inheritance" can absolutely become bad advice, in a domain with a genuinely stable hierarchy and behaviour that varies on one axis. So it is a Principle, and calling it a law is how it gets applied where its Forces are absent.

Conway's Law survives the same test, and the difference is worth being exact about. It does not tell you to do anything. It says systems tend to mirror the communication structure of the organizations that build them — a description, which can be weak, strong, or countered deliberately, but which is not the kind of thing that can be *bad advice*, because it is not advice (Ch. 09 owns what it means and what to do about it). **A Law describes; a Principle prescribes.** That single question separates them faster than any amount of arguing about how universal something feels.

---

## Where this doesn't apply

### Grade is not importance

The most common misuse of this chapter's own material.

Amdahl's Law is a Grade A result: given a fraction of work that must run serially, it bounds the speedup available from any number of processors. Nothing about it is negotiable. Applied to a single-threaded command-line tool that reads a file and prints a summary, it is also completely irrelevant — there is no parallel portion to bound, so the theorem is true and has nothing to constrain.

Meanwhile the gap between a cache hit and a main-memory read — a Grade C number, measured, drifting, different on the machine under your desk than in the paper you read it in — decides the entire architecture of a physics engine.

So the grade tells you **how to argue with a claim**, not **whether to care about it**. Those are independent, and reading grade as a priority ranking produces exactly the error the book is about: treating a firm claim as an important one.

### One name over a theorem and a slogan

CAP is the standard case. The proved result is narrow and precise: in an asynchronous network model with no clocks, a register cannot be simultaneously available and consistent when partitioned. That is Grade A, and the proof names its model.

The version that travels is "pick two of consistency, availability, and partition tolerance," which is not the theorem, is not proved, and is misleading — partition tolerance is not a property you choose, it is a fact about whether your network can drop packets. People then argue past each other, one holding a theorem and the other a slogan, both correctly reporting what they were taught.

When a claim has both forms, grading requires saying which one you mean before the conversation can go anywhere. Chapter 07 works through the theorem and what follows from it.

### The grade is sometimes genuinely open

Some claims sit between B and C and the argument about which is not settled.

"Adding people to a late project makes it later" can be read as near-tautological — new people consume the time of existing people, and communication paths grow faster than headcount — or as an empirical regularity with exceptions, which is how it behaves in practice. Both readings have support. The honest response is to hold the question open rather than to force a grade, because the forcing is what produces false confidence in either direction.

The book's rule applies to itself here: a claim that cannot be graded cleanly is telling you something about the claim, not about your grading.

---

## What it costs

**A vocabulary that invites showing off.** "That's only Grade C" is available as a way to dismiss a measured, load-bearing constraint on the grounds that it lacks a proof. The defence is the same as for the five kinds: a grade must arrive with its reason. If you cannot say what would falsify the claim, you have not graded it.

**Grade A material is genuinely hard to read.** The assumptions of a real theorem are stated in a paper, in notation, and following them is work. The realistic version is to read the assumptions and not the proof — which is enough for engineering, because the assumptions are the negotiable part — and to be honest that you are trusting the proof rather than checking it.

**Measuring a Grade C constant costs more than quoting one.** That is why people quote. Sometimes quoting is correct: an order of magnitude from a reputable source beats no number at all. The failure is quoting a number to three significant figures that you have not measured, in a context that differs from where it was taken.

**Three grades imply the world has three grades.** It has more. Statistical laws with confidence intervals, results proved only under assumptions nobody believes, claims true of every implementation anyone has built but not proved. The grading is a sorting aid whose value is mostly in separating "provable" from "measured," and the finer distinctions matter far less than that one.

---

## How to recognize the failure

**In a codebase:**

- **Machinery built to defeat a theorem** — a distributed-transaction layer intended to give exactly-once delivery over an unreliable network, rather than idempotent handlers that accept redelivery.
- **A performance constant hard-coded from a blog post**, with no measurement of the machine the code actually runs on, and no comment saying where the number came from.
- **A cache with no invalidation and no note saying why none is needed.** Either the original cannot change — in which case say so, because the next person cannot tell — or it can, and this is a bug waiting for its first report.
- **Elaborate structure defending against a Law whose preconditions are absent**, such as coordination machinery in a program with one writer.
- **A comment citing a law by name to justify a design**, where the law's assumptions are never mentioned and do not hold.

**In a conversation:**

- **"That violates CAP"** — asked about a system with one database and no partitions, where the theorem has nothing to act on.
- **"Conway's Law says we should reorganize."** It says no such thing; it describes a tendency. The prescription is somebody's, and it should be defended on its own.
- **A number quoted with more precision than anybody present has measured.**
- **"It's a law"** offered as the end of a discussion rather than the start of one — since the useful next question is always *which kind, and what are its assumptions?*
- **Two people arguing about CAP, or about any claim with a formal and an informal version**, without either establishing which one they are holding.

The question that does the work is short: **what would have to be true for this to be false?** A theorem answers *nothing, given its assumptions* — and then you go read them. A near-tautology answers *nothing, but it may not describe you*. An empirical claim answers *a measurement*, which you can go and take.

Anything that cannot answer at all was never a Law.

---

**Next:** chapter 05 takes the first family of Laws in detail — dependency direction and information hiding — and separates the part that is genuinely load-bearing from the two conventions that travel under the same name.
