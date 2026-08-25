# Three Kinds of True

## The claim

**Not all Laws are the same kind of true, and the kind decides what you can do about one.**

Against a theorem you can work on its assumptions, or on what you actually need from it — never on the conclusion. Against a definitional claim you can only check whether its words describe you. Against an empirical law you can measure, because the number came from somebody else's system on some other day.

What no kind allows is arguing with the claim. The kind tells you where you are permitted to work instead.

## The three kinds

| Kind | What makes it true | What would falsify it | The only move available |
|---|---|---|---|
| **Theorem** | a proof, from stated assumptions | nothing, unless the proof is wrong | change its assumptions, or stop needing its conclusion |
| **Definition** | what the words mean | nothing; the words may simply not describe you | check whether they do |
| **Empirical law** | observed to hold, again and again | a measurement | measure it where you are |

They are named rather than lettered, and the reason is the book's own: a letter has to be decoded at every use and carries nothing, while *theorem* and *definition* say what they mean at the point they appear. An ordering would be worse still — it would suggest a theorem outranks a definitional claim, and it does not. Neither can be violated. They differ in why, not in how firmly.

---

## The demonstration

### Theorem: change the assumptions

The theorem here is the **Two Generals Problem**: over a channel that can lose messages, no protocol can leave both parties certain that the other received what was sent. Its practical consequence is that exactly-once delivery is impossible — you get at-least-once, and you make repeating safe ([chapter 06](06_distribution_49yh.md) owns the result and what gets built on top of it).

That theorem rests on two assumptions, and both are worth having in front of you:

1. **The channel can lose messages.**
2. **You need certainty** — the sender must know the receiver got it.

Neither is negotiable inside the proof. Both are negotiable in a program, and each gives a different escape. Here is the first, which works by making assumption one false:

```go
// A Go channel is a typed in-memory queue between concurrent parts
// of one program — roughly Java's BlockingQueue, or queue.Queue in
// Python. It lives in memory, so nothing in it can be lost.
jobs := make(chan string, 1) // a queue holding one item
jobs <- "job-1"              // put
job := <-jobs                // take

fmt.Println("in-process: received", job, "— exactly once, nothing retried")
```

**This code is correct and needs nothing added.** Exactly-once here is not an achievement, it is what memory does.

Now the same job crosses a network. A client asks a billing service to charge a customer; the service does it; the reply is lost on the way back. The network sits between `chargeRemote` and `billingService`, and is simulated here so the whole thing can be run:

```go
// --- the client, on this machine ---
// A timeout means the reply did not arrive. It does NOT mean the
// charge did not happen.
func chargeRemote(orderID string) error { return send(orderID) }

// --- the network ---
// The request always arrives; the reply is always lost.
func send(orderID string) error {
	billingService(orderID)
	return errors.New("timeout")
}

// --- the billing service, on another machine ---
func billingService(orderID string) { charges++ }
```

The client times out and retries, because that is what a client does:

```text
in-process: received job-1 — exactly once, nothing retried
attempt 1: timeout — retry? the client cannot tell
attempt 2: timeout — retry? the client cannot tell
attempt 3: timeout — retry? the client cannot tell
charges actually applied: 3 — one was intended
```

Two pieces of code, and only one has a problem — but the problem is not *in* the code.

The in-process version is correct as written. The networked version cannot be fixed by writing it more carefully: retrying is what produced three charges, and not retrying loses charges whenever a request genuinely fails to arrive. The client has no third option, because it cannot distinguish *the request never arrived* from *the request arrived and the reply was lost*, and those two demand opposite actions.

The fix is not in the client at all. It is to make the charge **idempotent** — attach an identifier to the request, have the service record which identifiers it has already applied, and ignore a repeat. Then at-least-once delivery is sufficient, because a duplicate does nothing.

Be exact about what that fix did, because it is not the same manoeuvre as the first one.

**The in-process version made assumption one false.** Memory does not lose messages, so the theorem's precondition is absent and it has nothing to say about that code. This escape is only available when you can choose not to be distributed, which is most of the time and not all of it.

**Idempotency changes neither assumption.** The channel still loses replies, the client still cannot tell what happened, and exactly-once *delivery* remains impossible. What changed is on your side of the problem: you stopped needing it. The requirement was never really exactly-once delivery — it was exactly-once *effect*, and the two were quietly assumed to be the same thing. Separate them and the theorem's conclusion stops being a problem you have.

So a theorem admits two escapes and no third:

- **Arrange for one of its assumptions not to hold**, and the theorem does not apply to you.
- **Stop needing the theorem's conclusion**, and the theorem applies but costs you nothing.

What you cannot do is get the forbidden thing. And the assumptions are always written down, because a proof cannot exist without them — which is why reading them is the first move, not the last.

### Definition: check whether the words apply

A definitional claim is not proved so much as unpacked. Its truth is already inside its terms, so reading it feels less like learning something than like noticing something.

> A cache needs an invalidation strategy.

Unpack it. A cache is a copy kept because reading the original costs too much. If the original changes and the copy does not, the copy is wrong. So "a cache with no invalidation strategy" means "a copy that is allowed to go wrong" — which is either a decision you made deliberately or a bug you have not met yet. There is no third possibility, and no proof was needed to see it.

```go
// Read once when the program starts, never refreshed.
var rate = mustFetchRate()
```

Whether that line is a defect depends on exactly one thing:

```text
rate is a compile-time constant     no original to drift from — the
                                    claim has nothing to act on
rate is edited in an admin screen   a bug: every process serves a stale
                                    value until someone restarts it
```

**The move is not to argue with the claim. It is to find that its words do not describe you.** In the first case there is no cache in the strict sense — there is a precomputed value, and nothing can make it wrong. The claim is true and inert, which is [chapter 01](01_the-five-kinds_cjx4.md)'s distinction seen from underneath.

This is why definitional claims feel unfalsifiable without being vacuous. "Dependencies must be acyclic" is one: a cycle makes two things a single unit of comprehension, test, and change, because that is what a cycle *is* ([chapter 04](04_structure_agjy.md) works it through). You cannot violate it. You can find that the two things were never separate units, in which case nothing was violated, because nothing was joined.

### Empirical law: measure, because the number moved

An empirical law describes the world rather than following from a proof, and the world is under no obligation to hold still.

First, a distinction that is easy to lose. **A measurement is not a law.** "The 99th percentile of our search endpoint is 180 milliseconds" is empirical, and it is about one endpoint on one day on one deployment. Nothing generalizes. An empirical law has two parts: a **regularity** that holds across many systems, and a **magnitude** that varies between them. The regularity is what earns the word *law*; the magnitude is the part you have to measure locally, and the part people quote instead.

Hyrum's Law is one. With enough users, every observable behaviour of your system ends up depended on, regardless of what you documented as public behavior. ([chapter 04](04_structure_agjy.md) owns the law and what to do about it). Nothing proves it. It is a regularity about what people do, observed across languages and decades, and what varies is how fast the dependency forms and how firmly it sets.

Two languages met that regularity and moved in opposite directions.

Go randomizes the order of map iteration deliberately, so that no order can be depended upon:

```text
$ go run .        b a c d e
$ go run .        d e b a c
$ go run .        a c d e b
```

Python did the reverse. Dictionary insertion order arrived as an implementation detail of a faster dictionary in 3.6, was relied upon widely enough that removing it became impractical, and was promoted to a language guarantee in 3.7:

```text
$ python3 -c "d={'b':1,'a':2,'c':3}; print(list(d))"
['b', 'a', 'c']
$ python3 -c "d={'b':1,'a':2,'c':3}; print(list(d))"
['b', 'a', 'c']
```

Neither is a mistake. Go judged the freedom worth more than the convenience and made the behaviour impossible to rely on. Python found the reliance had already formed at a scale that made removal costly, and turned it into a promise.

**What makes this an empirical law rather than a theorem is that both outcomes were available.** No proof forced either. And notice what happened to the claim in Python's case: the observable behaviour that "will be depended upon" became documented behaviour, so the law's own prediction, taken seriously, changed the thing it was predicting. A theorem cannot do that.

The practical form has two halves, and the second is the one that survives a successful measurement: **quoting somebody's number is not the same as knowing yours, and knowing yours does not mean you should be chasing their target.** A 40% cache miss rate is a fact about you; whether it should be 5% depends on what a miss costs you, which is a different measurement again.

---

## Why the claim holds

The three are not flavours of one thing. They differ in **where the claim's authority comes from**, and that is what makes the available moves differ.

**A theorem's authority is internal.** It follows from its assumptions and nothing else, which is why evidence cannot refute it and arguing with it is a category error. It is also why the assumptions are always stated — a proof that hid them would not be a proof. That is the crack, and it is deliberate: the theorem tells you exactly where to push.

**A definitional claim's authority is in its terms.** It is true because of what its words pick out, so the only question it admits is whether those words pick out anything in your program. This is why such claims are the easiest to state and the hardest to argue with, and also why they can evaporate without ever having been wrong.

**An empirical law's authority is accumulated observation.** It can therefore drift, and it does. The shape of the memory hierarchy has changed several times in forty years. Team communication overhead depends on tools that did not exist when it was first counted. Repeat an empirical number long enough and it starts to sound like a theorem, which is this kind's characteristic failure.

There is a fourth possibility the naming exists to catch: **the claim is not a Law at all.**

The test is [chapter 01](01_the-five-kinds_cjx4.md)'s, applied honestly. *Can circumstances make this bad advice?* A Law cannot become bad advice, because it is not advice — it describes what happens. "Prefer composition over inheritance" can certainly become bad advice, in a domain with a genuinely stable hierarchy and variation on a single axis. So it is a Principle, and calling it a law is how it gets applied where its Forces are absent.

Conway's Law — that a system's structure tends to mirror the communication structure of the organization that built it — survives the same test, and the difference is worth stating exactly. It tells you to do nothing. It describes a tendency, which can be weak, strong, or deliberately countered, but which cannot be *bad advice*, because it is not advice ([chapter 08](08_change_rjf9.md) owns what it means and what to do about it). **A Law describes; a Principle prescribes.** That one question separates them faster than any amount of arguing about how universal something feels.

---

## Where the claim doesn't apply

### Kind is not importance

Naming the kind tells you how to argue with a claim. It says nothing about whether the claim bears on your program, and the two are independent.

Amdahl's Law is a theorem: given the fraction of work that must run serially, it bounds the speedup available from any number of processors, and none of it is negotiable. Applied to a single-threaded tool that reads a file and prints a summary, it is also irrelevant — there is no parallel portion to bound. Meanwhile the gap between a cache hit and a main-memory read is empirical, drifting, and different on your machine than in whatever you read it in — and it decides the entire architecture of a physics engine.

Firmness and relevance are separate axes.

### One name over a theorem and a slogan

The halting problem is the clearest case, because the theorem and the thing people say about it differ in a way that costs real work.

**The theorem**, proved by Turing in 1936, is that no single algorithm can decide, for *every* program and input, whether that program halts. The quantifier is the whole content: it forbids a universal decider.

**The slogan** is "you can't tell whether a program halts." That is a claim about any particular program, and it is false. You can very often tell, and tools do it routinely:

```python
for i in range(10):     # halts. A compiler can prove it, and does.
    total += i
```

```python
while queue:            # halts if the body always shrinks the queue.
    item = queue.pop()  # here it does, and a checker can verify that.
    handle(item)
```

Termination checking is a working field. Proof assistants reject a recursive definition that cannot be shown to terminate; static analysers prove loop bounds; compilers unroll loops precisely because they know the count. None of that violates the theorem, because none of it is a universal decider — each proves termination for programs of a shape it understands, and gives up on the rest.

The cost of confusing the two is that the slogan gets used to end conversations. "We can't detect that statically, halting problem" is sometimes correct and often is not, and the difference is whether you need an answer for *all* programs or for the ones your codebase actually contains. The second is usually a solvable problem that nobody attempted.

So the useful advice is not "say which version you mean," which nobody would say out loud. It is that when a claim has a formal version and a folk version, the folk one has usually dropped a quantifier or a condition, and that is exactly where the engineering was.

### Some claims sit between kinds

"Adding people to a late project makes it later" can be read as near-definitional — new people consume the time of existing people, and communication paths grow faster than headcount — or as an empirical regularity with real exceptions, which is closer to how it behaves in practice. Both readings have support.

The honest response is to leave the question open rather than force an answer, because forcing it manufactures confidence in whichever direction you picked. A claim that resists classification is telling you something about the claim.

---

## What the claim costs

**A vocabulary that invites dismissal.** "That's only empirical" is available as a way to wave off a measured, load-bearing constraint on the grounds that nobody proved it. The defence is the same as for the five kinds: a classification must arrive with its reason. If you cannot say what would falsify the claim, you have not classified it.

**Theorems are genuinely hard to read.** The assumptions of a real one are stated in a paper, in notation, and following them is work. The realistic version is to read the assumptions and skip the proof — which is enough for engineering, since the assumptions are the negotiable part — and to be honest that you are trusting the proof rather than checking it.

**Measuring costs more than quoting.** That is why people quote. Sometimes quoting is right: an order of magnitude from a good source beats no number at all. The failure is quoting a number to three significant figures that you have never measured, in a setting that differs from the one it came from.

**Three kinds imply the world has three.** It has more — statistical laws with confidence intervals, results proved under assumptions nobody believes, claims true of every implementation ever built but never proved. This is a sorting aid, and most of its value is in separating *proved* from *observed*. The finer distinctions matter far less than that one.

---

## How to recognize the failure

**In a codebase:**

- **Machinery built to defeat a theorem** — a distributed transaction layer intended to deliver exactly-once over an unreliable network, rather than idempotent handlers that accept redelivery.
- **A performance constant hard-coded from a blog post**, with no measurement on the machine the code runs on and no comment saying where the number came from.
- **A cache with no invalidation and no note saying why none is needed.** Either the original cannot change — in which case say so, because the next reader cannot tell — or it can, and this is a bug waiting for its first report.
- **Elaborate defence against a Law whose preconditions are absent**, such as coordination machinery in a program with a single writer.
- **A comment citing a law by name to justify a design**, where the law's assumptions are never mentioned and do not hold.

**In a conversation:**

- **"We can't check that, halting problem"** — said about an analysis over the code in one repository, where the theorem forbids only a decider that works for every program ever written.
- **"Conway's Law says we should reorganize."** It says no such thing; it describes a tendency. The prescription belongs to whoever is making it, and should be defended on its own.
- **A number quoted with more precision than anyone present has measured.**
- **"It's a law"** offered as the end of a discussion rather than the start of one, when the useful next question is always *which kind, and what does it assume?*
- **An argument about any claim with a formal and a folk version**, where neither side has noticed they are holding different claims.

The question that does the work is short: **what would have to be true for this to be false?**

A theorem answers *nothing, given its assumptions* — and then you go and read them. A definitional claim answers *nothing, but the words may not describe me*. An empirical law answers *a measurement*, which you can go and take.

Anything that cannot answer at all was never a Law.

[Chapter 04](04_structure_agjy.md) takes the first family of Laws in detail — dependency direction and information hiding — and separates the part that is genuinely load-bearing from the two conventions travelling under the same name.

---

[← Ch. 02](02_forces_f4m5.md)  ·  [Contents](00_toc.md)  ·  [Ch. 04 →](04_structure_agjy.md)
