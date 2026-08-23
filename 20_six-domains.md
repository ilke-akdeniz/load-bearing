# Six Domains, Six Inversions

## The claim

**A domain is not a subject area. It is a recurring profile of forces, with at least one of them pinned at an extreme — and that is why advice which is sound in one domain inverts in another, and why the inversion is predictable from the profile rather than something you discover by being burned.**

Chapter 19 gave the method for one decision. This chapter runs it at the scale of whole systems, six times, and the finding is that the answers cluster.

---

## The demonstration

### What makes a domain

*Games* is not a domain because games are a kind of software. It is a domain because a game has a fixed frame budget measured in milliseconds, and inside that budget the memory hierarchy decides what is possible. A flight simulator, a video encoder and a high-frequency trading loop share that profile and share its inversions, while sharing nothing anyone would call a subject.

So the test for whether something is a domain in this sense is not what the software is about. It is whether two systems from unrelated industries, put side by side, turn out to face the same overturned advice. Where they do, what they have in common is a force reading rather than a topic.

Six profiles follow. Each has one force at an extreme, and each inverts something the mainstream states without qualification.

```text
 domain            the force at an extreme
 ----------------  ---------------------------------------------
 line-of-business  durability: the data outlives every rewrite
 games and sims    latency: a fixed frame, and the cache decides
 embedded          latency again, but a missed deadline is the
                   bug, and there is no allocator
 compilers         change shape: one type touched by everything
 UI frameworks     control of callers: you are not the caller
 distributed       concurrency across machines, so no shared
                   transaction exists at all
```

**Most of what follows is worked elsewhere in this book**, because the individual findings belong to the chapters that established them. What this chapter adds is the observation that they are not scattered. They cluster, one cluster per force at its limit.

### Line-of-business: the schema outlives the code

The force is durability. A payroll system's tables will be read by software nobody has written yet, in a language nobody has chosen, after every original author has left.

**What inverts: keep business rules out of the database.** In most software this is sound — logic in the schema is hard to test, hard to version, invisible to the debugger. Here it turns over, because a rule enforced only in application code is a rule that holds until the next application. Chapter 14 works the placement, and chapter 17 shows what a constraint catches that a test double cannot.

**And a second one: the database is an implementation detail you can abstract away.** Chapter 18 takes this apart in full. The domain-level version is shorter: the abstraction sits in the layer that changes fastest, and the thing it claims to insure sits in the layer that changes slowest, so the insurance is filed against the wrong asset.

The ORM question follows from the same force and is worth stating plainly, because it is usually argued as taste. An ORM is a productivity trade whose bill comes due at exactly the point where this domain's force bites: the generated query, the migration, the constraint the mapping cannot express. It is not that ORMs are wrong here. It is that this is the domain where you will be reading the SQL they generate, so choosing one on the basis that you will not have to is choosing on a claim the domain disproves.

### Games and simulations: the layout is the interface

The forces are the frame budget and the memory hierarchy, and chapter 05 works this domain's central inversion — hide the representation turns over, because in an entity-component system the array layout *is* the contract that a dozen systems agree on. Chapter 08 owns the arithmetic underneath it.

Two further inversions belong here rather than there.

**Allocate when you need it** inverts. Outside this domain, allocating in a loop is a performance question you resolve if profiling says so. Inside a frame, an allocation is a latency event with a distribution rather than a cost — the allocator is fine until the collector runs, and the collector runs when it likes. So the pattern is to allocate everything before the loop starts and never again, which reads as premature optimization and is nothing of the kind. The budget is fixed in advance; there is no *later* in which to optimize.

**Prefer correctness to determinism** inverts too, and this one surprises people from outside. A simulation that produces a slightly different result on two machines is not slightly wrong; it is unusable for replay, for lockstep multiplayer, and for reproducing a bug report. Floating-point associativity, iteration order over a hash map, and anything threaded become correctness concerns rather than performance ones. Chapter 06's ordering material is the mechanism; what is unusual here is which side of the trade is non-negotiable.

### Embedded and real-time: no allocator, no second chance

The force is a deadline that is part of the specification rather than a target, on hardware with a fixed memory budget and often no heap at all.

**Exceptions inverts.** In most software, error codes are the weaker option — easy to ignore, noisy at every call site, and chapter 12 catalogues the alternatives. In hard real-time, unwinding has an execution time nobody can bound in advance, and a path whose worst case cannot be computed cannot be certified. So the code looks like this, and the ugliness is the point:

```c
/* No allocation, no unwinding, and every failure path visible
   at the call site because it has to be countable. */
status_t read_sample(sensor_t *sensor, uint16_t *out) {
    if (sensor == NULL || out == NULL) return STATUS_INVALID;
    if (!sensor->ready) return STATUS_NOT_READY;
    *out = sensor->latest;
    return STATUS_OK;
}
```

**Allocate dynamically** inverts, harder than in games: there is frequently no allocator to call, and static buffers sized at compile time are the whole strategy. **And dependency injection stops meaning anything**, because there is one sensor, one radio, one clock, and the composition root chapter 05 argues for has exactly one composition to root. Injecting it buys the ability to substitute something that does not exist.

### Compilers and language tooling: one type touched by everything

The force is the shape of change. A compiler's abstract syntax tree — the tree of nodes representing the parsed program — is read by the type checker, the optimizer, the code generator, the formatter and the language server. Every one of them depends on it.

**What inverts: nothing should be depended on by everything.** In most systems, a type with that many dependents is the god object chapter 10 warns about, and the advice to break it up is correct. Here it is exactly right that everything depends on the AST, and breaking it up produces a translation layer per consumer for no gain.

The reason is chapter 05's, applied to a shape it already names: the dependency graph is a pipeline, not a stack of layers, and the AST is at the bottom of it — depended on by many, depending on nothing. That is the *stable* position, which is what "depend on abstractions" was pointing at all along (Ch. 18). An AST is concrete, has no interface, and is one of the most stable types in the system. Chapter 05 makes the same point about a parser's mutually recursive node types being nobody's idea of a violation.

What this domain adds is that the property generalises: **a type depended on by everything is a problem exactly when it also depends on things.** Fan-in alone is not the smell. Fan-in with fan-out is.

### UI frameworks: you are not the caller

The force is control of the callers, at the value chapter 03 names as the extreme — and pointed the other way. As a framework author you cannot see your callers. As a framework *user* you are the callee, and the flow of control belongs to somebody else.

**What inverts: your code should own the flow.** Structured programming, layering, most architectural advice, and every diagram with an arrow pointing downward assume your `main` is at the top. Under a framework it is not. The framework's loop calls your component, decides when to call it again, decides what happens between calls, and may discard and rebuild your state without asking.

Chapter 05 owns the mechanism — the call goes up while the dependency goes down, and that is inversion of control done properly. What belongs here is that in this domain it is not a technique you apply. **It is the product.** A framework whose control you kept would be a library, and the distinction between the two words is exactly this.

Which has a practical consequence worth more than the definition: the framework's lifecycle is a Force, not a convention. Fighting it — holding state outside it, calling into it from your own loop, treating its callbacks as an inconvenient API over the thing you really wanted — is the single most common way applications in this domain become unmaintainable, and it is always defended in the language of good architecture.

### Distributed services: atomicity is gone, so everything downstream changes

The force is concurrency across machines, and chapter 07 owns this domain end to end: you cannot tell a slow peer from a dead one, exactly-once delivery is impossible, so at-least-once plus idempotency is the shape everything takes, and two systems cannot share a transaction.

The domain-level observation is what happens to the toolkit as a whole. Nothing here weakens by a little. A transaction becomes a saga with visible compensations. A foreign key becomes an eventual reconciliation. A unique constraint becomes an idempotency key generated by the client before the first attempt. A rollback becomes a compensating business operation a customer can see.

**Which is the signature of a domain, and the reason this chapter groups by force rather than by topic.** One force at an extreme does not overturn one piece of advice. It overturns the whole family that depended on it, because they all depended on the same thing — and here the thing is that a set of writes either all happen or none do.

### What the six have in common

In every case the pattern is identical, and it is chapter 02's distinction seen at scale.

**A Law holds throughout.** Acyclic dependency does not stop being true in an entity-component system; chapter 05 is explicit that the ECS graph is still acyclic. Check-then-act is still a race in a game loop. The impossibility results still bind on a trading system.

**A Principle turns over.** Hide the representation, keep rules out of the database, own your flow, avoid god objects — each is good advice with a condition, and each condition fails in exactly one of these profiles.

**And the failure is predictable.** Not one of the six inversions is a surprise once the force reading is in front of you. That is the whole claim: you do not need to have worked in a domain to know which advice it overturns, if you know which force it pins.

---

## Why the claim holds

A Principle is advice that is good given certain forces (Ch. 02). Its condition is a force at a range of values, usually unstated because in most software that force sits in an ordinary range and the condition is quietly satisfied.

A domain is where one force leaves the ordinary range and stays there. So the condition fails not occasionally but structurally, for every system in the domain, all the time — which is why the failures cluster rather than scatter, and why the same six or seven pieces of advice come up every time practitioners from two domains argue.

**And it is why the arguments are so unproductive.** Two people disagreeing about whether to put logic in the database are not disagreeing about databases. One of them works where the schema outlives four rewrites of the application, and the other works where the application outlives the storage it happens to be using this year. Both are right, both are giving advice that has worked every time they have applied it, and neither has said the force out loud. Chapter 03 identifies this as the general shape of unresolvable design arguments; a domain is the case where the two people's force readings differ so far apart that they will never converge by talking about the code.

The practical consequence is that **domain experience transfers as a force reading, not as a set of rules.** Someone arriving from a domain you do not share is carrying conclusions that were correct where they came from. What is worth extracting from them is not the conclusion but the reading it was derived from, which is a question they can usually answer and are almost never asked.

---

## Where the claim doesn't apply

### Most interesting systems straddle two domains

This is the common case rather than the exception, and it is where the chapter's neat six-way split stops being useful.

A game with a persistent inventory is two domains in one repository. The frame loop is games — arrays, no allocation, determinism. The inventory is line-of-business — it outlives the client build, it is worth money to the player, and a torn write is a support ticket. A trading system is real-time on one path and durable-audit on another. A browser is a UI framework hosting a compiler.

The mistake is choosing one profile and applying it throughout. A game that treats its save file with frame-loop discipline loses inventories; an inventory service that treats the frame loop with LOB discipline misses frames.

**What to do is a boundary question, and the boundary is a real one: it goes where the force profile changes.** That is the same seam chapter 05 draws for dependency direction and chapter 09 draws for rate of change, arriving from a third direction. Concretely:

- **Name the two profiles.** Write down which force is extreme on each side. If you cannot, there is one domain and the question is moot.
- **Put the seam where the data crosses**, not where the code is organized. In the game, the seam is the point where component arrays become rows — and that point should be a small, explicit, boring piece of code that both sides understand, rather than a leak of either discipline into the other.
- **Let each side keep its own rules.** The frame loop does not get to use the inventory's transactional habits, and the inventory does not get to be lock-free because it lives in a game.
- **Expect the seam to be where the bugs are**, because it is the only place where two sets of assumptions meet, and each side is written by someone for whom the other side's rules look wrong.

### A domain you are visiting rather than living in

Reading this chapter and concluding you now understand embedded development is the failure it is easiest to commit. The force readings above are real and they are also the first page. What they let you do is ask better questions and stop offering advice from your own domain as though it were general. What they do not do is substitute for the thing chapter 19 charges for, which is knowing what the options cost.

### Domains that are not on this list

Six is not a complete enumeration and nothing in the argument requires it to be. Scientific computing, data engineering, security-critical systems and machine-learning infrastructure each have force profiles that would produce their own inversions, and the method for finding them is chapter 19's rather than this chapter's list.

---

## What the claim costs

**Domain knowledge does not transfer, and this is worse news than it sounds.** If the inversions cluster by force profile, then moving domains means your accumulated judgement is partly wrong in a way that feels exactly like being right. Nothing in the experience of having been correct for ten years tells you which of your conclusions travelled.

**"It's a different domain" becomes an excuse.** The claim is falsifiable and the excuse is not. The check is to name the force and its value: *the schema outlives the code, so the rule goes in the schema* can be argued with, and *we do things differently in fintech* cannot. Any use of the domain frame that does not name a force is chapter 15's mechanism, running on this chapter.

**Six labels invite a lookup table.** The point is the derivation, not the list — and a reader who takes the six as categories to sort systems into has taken the conclusion and left the method, which is precisely what this book spends Part IV describing.

**And most software is in none of these profiles.** The ordinary case is a system where no force is at an extreme, every condition is quietly satisfied, and the mainstream advice is simply correct. This chapter is about the edges; a reader who concludes that their CRUD application is secretly six domains in a trenchcoat has misread it.

---

## How to recognize the failure

**In a codebase:**

- **Advice applied uniformly across a seam.** One allocation discipline, one error-handling convention, one testing strategy across both sides of a boundary where the force profile changes. Somebody chose a house style over a force reading.
- **A translation layer whose only job is to make one side look like the other.** Frequently the seam done wrong: rather than a small explicit crossing, one domain's shapes are dressed up as the other's throughout.
- **Fighting the framework.** State held outside the lifecycle, effects run in the wrong phase, the framework's calls treated as an API to work around. Almost always defended as separation of concerns.
- **A god object that only has fan-in.** Before breaking it up, check whether it depends on anything. If it does not, it may be an AST.

**In a conversation:**

- **"That's not how it's done."** The reply that moves things forward is not *why not* but *where have you seen it done, and what was true there?*
- **"We need to be pragmatic about the database."** Ask what outlives what. The answer decides it, and it is a fact rather than a preference.
- **"Premature optimization."** True almost everywhere and false where the budget is fixed in advance. The question is whether there is a *later* in which to optimize.
- **Someone senior giving advice that is obviously wrong here.** The most likely explanation is not that they are wrong. It is that they are right somewhere else and have not been asked which force they are reading.

The question that does the work: **which force is at an extreme here, and what does it hold still?**

Every inversion in this chapter is that question answered. If nothing is at an extreme, you are in the ordinary case, the mainstream advice applies, and the interesting thing about your system is somewhere other than its architecture.

---

## Sources

- FlowCore, `docs/decisions.md` — [github.com/ilke-akdeniz/flowcore](https://github.com/ilke-akdeniz/flowcore).

---

**Next:** chapter 21 turns from domains to ecosystems — why two languages solving the same problem settle on conventions that contradict each other, and what an idiom is actually worth once you can see where it came from.
