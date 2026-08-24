# Six Profiles, Six Inversions

## The claim

**What decides which advice holds is not the domain but the force profile.**

To make the claim precise two terms need to be settled:  

- *Domain* means what the software is about. Payroll, ledgers, air traffic, imaging. 

- **Force profile** is the reading of every force bearing on a system — and what makes a reading a *profile* is that at least one of those forces sits at an intensity outside the ordinary range (Ch. 03), and stays there. Unlike domain, force profile is this book's term and is not standard vocabulary.

Chapter 19 gave the force-map method for one decision. This chapter runs it at the scale of whole systems, six times, and the finding is that the answers cluster.

---

## The demonstration

### Domain and force profile are two different axes

A flight simulator, a video encoder and a high-frequency trading loop share almost nothing anyone would call a domain. They share a force profile: a fixed latency budget measured in milliseconds, inside which the memory hierarchy decides what is possible. And they share its inversions — all three end up with memory layouts nobody may hide and allocation moved out of the loop.

That is one direction. **The other direction matters more, because it is the one that catches people.**

Consider two systems in the same business. One company sells high-end pizza ovens to restaurants: a salesperson writes a proposal, one person to a proposal, and nobody else touches it. Another company sells and installs security systems for marine ports: several salespeople, technicians and advisors work the same proposal, and often the same line items, at overlapping stages.

Both are sales software. Ask a domain expert to describe either one and the vocabulary comes back identical — proposal, line item, discount, approval. And the concurrency reading is not close: one has a single writer and no contention worth naming, the other has a rule spanning rows that several people are editing at once, which is chapter 06's territory in full. The business does tell you which. It just does not answer the question people usually put to it. *What are the things called* gets the same reply from both companies; *who touches a proposal, and when* gets opposite ones.

So domain and force profile vary independently. Unrelated domains can share a profile; one domain can contain opposite profiles. The six sections below are organised by profile, with the domain kept as the place you are most likely to meet it: the profile is what predicts the inversion, and the domain name on its own predicts almost nothing.

Six profiles follow. Each has at least one force outside its ordinary range, and each inverts something the mainstream states without qualification.

```text
 where you meet it   the force profile
 ------------------  --------------------------------------------
 line-of-business    durability: the data outlives every rewrite
 games and sims      latency: a fixed frame, and the cache decides
 embedded            latency again, but a missed deadline is the
                     bug, and there is no allocator
 compilers           change shape: one type touched by everything
 UI frameworks       control of callers: you are not the caller
 distributed         concurrency across machines, so no shared
                     transaction exists at all
```

The left column is where each profile is commonly met, not what the profile is. The two sales systems above share a domain and would not share a row.

**Most of what follows is worked elsewhere in this book**, because the individual findings belong to the chapters that established them. What this chapter adds is the observation that they are not scattered. They cluster, one cluster per force that leaves its ordinary range.

### Line-of-business: the schema outlives the code

The force is durability. A payroll system's tables will be read by software nobody has written yet, in a language nobody has chosen, after every original author has left.

**What inverts: keep business rules out of the database.** In most software this is sound — logic in the schema is hard to test, hard to version, invisible to the debugger. Here it turns over, because a rule enforced only in application code is a rule that holds until the next application. Chapter 14 works the placement, and chapter 17 shows what a constraint catches that a test double cannot.

**And a second one: the database is an implementation detail you can abstract away.** Chapter 18 takes this apart in full. The profile-level version is shorter: the abstraction sits in the layer that changes fastest, and the thing it claims to insure sits in the layer that changes slowest, so the insurance is filed against the wrong asset.

The ORM question follows from the same force and is worth stating plainly, because it is usually argued as taste. An ORM is a productivity trade whose bill comes due at exactly the point where this profile's force bites: the generated query, the migration, the constraint the mapping cannot express. It is not that ORMs are wrong here.

It is that an ORM chosen because it means you will not have to write SQL is chosen on a promise this profile breaks. You will read the SQL it generates — on the day a query is slow, a migration is wrong, or a constraint cannot be expressed through the mapping. That is an argument against one particular reason for picking one, not against the tool.

### Games and simulations: the memory layout is the interface

The forces are the frame budget and the memory hierarchy, and chapter 05 works this profile's central inversion. *Hide the representation* turns over: in an entity-component system the order and grouping of fields in memory is what a dozen systems index directly, so it is the contract rather than a private detail, and changing it means changing all of them. Chapter 08 owns the arithmetic underneath it.

Two further inversions belong here rather than there.

**What inverts: allocate when you need it, and optimize later if profiling says so.** Here it becomes: allocate everything before the loop starts, and never again inside it.

Outside this profile, allocating in a loop is a performance question you resolve when a profiler points at it. Inside a frame it is a latency event with a distribution rather than a cost — the allocator is cheap until the collector runs, and the collector runs when it likes, which is a spike you cannot schedule around. So the pools are built up front. That reads as premature optimization and is nothing of the kind: the budget was fixed before anyone wrote a line, so there is no *later* in which to optimize.

**What inverts: use the most accurate and fastest method available.** Here it becomes: use the reproducible one, and pay for it in accuracy and speed.

The mainstream treats reproducibility as a testing convenience. In a simulation it is part of the specification, because a replay that drifts is not a replay and a bug report you cannot reproduce is not a bug report. What costs reproducibility is precisely the better routes: a parallel reduction sums in a different order than a sequential one, fused multiply-add is more accurate and changes the result, an adaptive timestep is better physics than a fixed one, and iterating a hash map is fine until the order leaks into the simulation. So the deterministic version is often slightly less accurate per step and slower, on purpose. The divergence you are avoiding is tiny — and tiny is fatal, because it compounds over a few thousand frames into two machines watching different games. Chapter 06's ordering material is the mechanism; what is unusual here is which side of the trade is non-negotiable.

### Embedded and real-time: no allocator, no second chance

The force is a deadline that is part of the specification rather than a target, on hardware with a fixed memory budget and often no heap at all.

**What inverts: prefer exceptions to error codes.** Here it becomes: return a status from every call, and check it at every call site.

In most software, error codes are the weaker option — easy to ignore, noisy everywhere, and chapter 12 catalogues the alternatives. In hard real-time, unwinding has an execution time nobody can bound in advance, and a path whose worst case cannot be computed cannot be certified. So the code looks like this, and the noise is the point:

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

**What inverts: allocate what you need at run time.** Here it becomes: size every buffer at compile time, because there is frequently no allocator to call at all. This is the games inversion taken further — there the heap exists and you avoid it, here it may not exist.

**And what inverts quietly: inject your dependencies.** Here it becomes: construct them, once, in place. There is one sensor, one radio, one clock, and the composition root chapter 05 argues for has exactly one composition to root. Injection buys the ability to substitute something that does not exist, and the seam costs a pointer indirection on a deadline you are already fighting.

### Compilers and language tooling: one type touched by everything

The force is the shape of change. A compiler's abstract syntax tree — the tree of nodes representing the parsed program — is read by the type checker, the optimizer, the code generator, the formatter and the language server. Every one of them depends on it.

**What inverts: nothing should be depended on by everything.** In most systems, a type with that many dependents is the god object chapter 10 warns about, and the advice to break it up is correct. Here it is exactly right that everything depends on the AST, and breaking it up produces a translation layer per consumer for no gain.

The reason is chapter 05's, applied to a shape it already names: the dependency graph is a pipeline, not a stack of layers, and the AST is at the bottom of it — depended on by many, depending on nothing. That is the *stable* position, which is what "depend on abstractions" was pointing at all along (Ch. 18). An AST is concrete, has no interface, and is one of the most stable types in the system. Chapter 05 makes the same point about a parser's mutually recursive node types being nobody's idea of a violation.

What this profile adds is that the property generalises: **a type depended on by everything is a problem exactly when it also depends on things.** Fan-in alone is not the smell. Fan-in with fan-out is.

### UI frameworks: you are not the caller

The force is control of the callers, at the third of the three intensities chapter 03 gives it: you can neither see your callers nor change them. And it applies from both ends. As a framework author you cannot see your callers. As a framework *user* you are the callee, and the flow of control belongs to somebody else.

**What inverts: your code should own the flow.** Structured programming, layering, most architectural advice, and every diagram with an arrow pointing downward assume your `main` is at the top. Under a framework it is not. The framework's loop calls your component, decides when to call it again, decides what happens between calls, and may discard and rebuild your state without asking.

Chapter 05 owns the mechanism — the call goes up while the dependency goes down, and that is inversion of control done properly. What belongs here is that under this profile it is not a technique you apply. **It is the product.** A framework whose control you kept would be a library, and the distinction between the two words is exactly this.

Which has a practical consequence worth more than the definition: the framework's lifecycle is a Force, not a convention. Fighting it — holding state outside it, calling into it from your own loop, treating its callbacks as an inconvenient API over the thing you really wanted — is the single most common way applications under this profile become unmaintainable, and it is always defended in the language of good architecture.

### Distributed services: atomicity is gone, so everything downstream changes

The force is concurrency across machines, and chapter 07 owns this profile end to end: you cannot tell a slow peer from a dead one, exactly-once delivery is impossible, so at-least-once plus idempotency is the shape everything takes, and two systems cannot share a transaction.

The profile-level observation is what happens to the toolkit as a whole. Nothing here weakens by a little. A transaction becomes a saga with visible compensations. A foreign key becomes an eventual reconciliation. A unique constraint becomes an idempotency key generated by the client before the first attempt. A rollback becomes a compensating business operation a customer can see.

**Which is the signature of a profile, and the reason this chapter groups by force rather than by domain.** A force outside its ordinary range does not overturn one piece of advice. It overturns the whole family that depended on it, because they all depended on the same thing — and here the thing is that a set of writes either all happen or none do.

### What the six have in common

In every case the pattern is identical, and it is chapter 02's distinction seen at scale.

**A Law holds throughout.** Acyclic dependency does not stop being true in an entity-component system; chapter 05 is explicit that the ECS graph is still acyclic. Check-then-act is still a race in a game loop. The impossibility results still bind on a trading system.

**A Principle turns over.** Hide the representation, keep rules out of the database, own your flow, avoid god objects — each is good advice with a condition, and each condition fails in exactly one of these profiles.

**And the failure is predictable.** Not one of the six inversions is a surprise once the force reading is in front of you. That is the whole claim: you do not need to have worked under a profile to know which advice it overturns, if you know which force it pins.

---

## Why the claim holds

A Principle is advice that is good given certain forces (Ch. 02). Its condition is a force at a range of values, usually unstated because in most software that force sits in an ordinary range and the condition is quietly satisfied.

A profile is where at least one force leaves that ordinary range and stays there. So the condition fails not occasionally but structurally, for every system with that reading, all the time — which is why the failures cluster rather than scatter, and why the same six or seven pieces of advice come up every time practitioners from two profiles argue.

**And it is why the arguments are so unproductive.** Two people disagreeing about whether to put logic in the database are not disagreeing about databases. One of them works where the schema outlives four rewrites of the application, and the other works where the application outlives the storage it happens to be using this year. Both are right, both are giving advice that has worked every time they have applied it, and neither has said the force out loud. Chapter 03 identifies this as the general shape of unresolvable design arguments. What a profile adds is that the two readings are not merely different but stably different — they will be just as far apart on the next question, and on the one after that, so the two will never converge by talking about code. [-- this "two people arguing both are right" theme was used maybe 5 times in the book with near identical idea. Search the book for "two people" and see what I mean. You need to do something about this problem. It's ok to edit older chapters in addition to this chapter for fixing this.]

The practical consequence is an asymmetry between the two axes, and it is worth stating because it decides what to ask a new colleague.

**Profile knowledge transfers. Domain knowledge does not.** Someone who has worked where the frame budget dominates can find their way in an unfamiliar business with the same profile, because what they carry is a set of readings and the moves that follow from them. Someone who knows a business deeply carries something far less portable — which is why there are lawyers who do maritime and lawyers who do civil, and surgeons who do hands and surgeons who do brains, and why nobody finds that odd.

So when a person arrives from a domain you do not share, they are carrying conclusions that were correct where they came from. What is worth extracting is not the conclusion but the reading it came from — a question they can nearly always answer, and are nearly never asked.

**And the two are more tangled than either side tends to admit.** Profile knowledge is what transfers, but it is not what supplies a reading in the first place. Nobody reads *several people edit the same line items at overlapping stages* off an architecture diagram; it comes from someone who knows how ports buy security systems.

---

## Where the claim doesn't apply

### Most interesting systems straddle two profiles

This is the common case rather than the exception, and it is where the chapter's neat six-way split stops being useful.

A game with a persistent inventory is two profiles in one repository. The frame loop is games — arrays, no allocation, determinism. The inventory is line-of-business — it outlives the client build, it is worth money to the player, and a torn write is a support ticket. A trading system is real-time on one path and durable-audit on another. A browser is a UI framework hosting a compiler.

The mistake is choosing one profile and applying it throughout. A game that treats its save file with frame-loop discipline loses inventories; an inventory service that treats the frame loop with LOB discipline misses frames.

**What to do is a boundary question, and the boundary is a real one: it goes where the force profile changes.** That is the same seam chapter 05 draws for dependency direction and chapter 09 draws for rate of change, arriving from a third direction. Concretely:

- **Name the two profiles.** Write down which force is outside its ordinary range on each side. If you cannot, there is one profile and the question is moot.
- **Put the seam where the data crosses**, not where the code is organized. In the game, the seam is the point where component arrays become rows — and that point should be a small, explicit, boring piece of code that both sides understand, rather than a leak of either discipline into the other.
- **Let each side keep its own rules.** The frame loop does not get to use the inventory's transactional habits, and the inventory does not get to be lock-free because it lives in a game.
- **Expect the seam to be where the bugs are**, because it is the only place where two sets of assumptions meet, and each side is written by someone for whom the other side's rules look wrong.

### The ordinary case, where every force sits in its ordinary range

Most software is here, and it is the largest boundary on the claim. Nothing is pinned, every condition the mainstream advice depends on is quietly satisfied, and that advice is simply correct. None of the six inversions applies.

That is a finding about your system rather than a disappointment, and four things follow from it.

**It licenses the conventional answer.** Following the mainstream because you checked and every force sits in its ordinary range is a different act from following it because it is what people do — the first can be defended and revisited, the second cannot. Converting the second into the first is most of what this book is for.

**Most systems have one path that leaves the ordinary case**, and it is rarely the whole system. The nightly report that outgrew memory, the table nobody can migrate any more, the one integration you do not control. Recognising the shape of a force leaving its ordinary range is what lets you notice the crossing, and the crossing is where the interesting bugs are.

**Most advice you meet was written from inside a profile.** Knowing the six lets you discount it correctly — *that is the distributed profile talking and I have no network*, *that is the frame budget talking and I have no budget*. Advice arrives without its profile stated for the same reason it arrives without its scope stated (Ch. 15).

**And it explains the senior person whose advice is obviously wrong here.** Usually they are right somewhere else and nobody has asked which reading they are carrying.

### A profile you are visiting rather than living in

Reading this chapter and concluding you now understand embedded development is the failure it is easiest to commit. The readings above are real and they are also the first page. What they let you do is ask better questions and stop offering advice from your own profile as though it were general. What they do not do is substitute for the thing chapter 19 charges for, which is knowing what the options cost.

### Domains that are not on this list

Six is not a complete enumeration and nothing in the argument requires it to be. Scientific computing, data engineering, security-critical systems and machine-learning infrastructure each have force profiles that would produce their own inversions, and the method for finding them is chapter 19's rather than this chapter's list.

---

## What the claim costs

**Moving between profiles costs you judgement you do not know you are losing.** If the inversions cluster by profile, then arriving under a new one means part of your accumulated judgement is wrong in a way that feels exactly like being right. Nothing in the experience of having been correct for ten years tells you which of your conclusions travelled and which were local.

**"It's a different profile" becomes an excuse.** The claim is falsifiable and the excuse is not. The check is to name the force and its value: *the schema outlives the code, so the rule goes in the schema* can be argued with, and *we do things differently in fintech* cannot. Any use of the domain frame that does not name a force is chapter 15's mechanism, running on this chapter.

**Six labels invite a lookup table.** The point is the derivation, not the list — and a reader who takes the six as categories to sort systems into has taken the conclusion and left the method, which is precisely what this book spends Part IV describing.

---

## How to recognize the failure

**In a codebase:**

- **Advice applied uniformly across a seam.** One allocation discipline, one error-handling convention, one testing strategy across both sides of a boundary where the force profile changes. Somebody chose a house style over a force reading.
- **A translation layer whose only job is to make one side look like the other.** Frequently the seam done wrong: rather than a small explicit crossing, one profile's shapes are dressed up as the other's throughout.
- **Fighting the framework.** State held outside the lifecycle, effects run in the wrong phase, the framework's calls treated as an API to work around. Almost always defended as separation of concerns. [-- what does framework mean here? That's a very loaded term. Did you mean tech stack?]
- **A god object that only has fan-in.** Before breaking it up, check whether it depends on anything. If it does not, it may be an AST. [-- explain this more concretely, what's the failure here. Also these last two failures need to be tied to a failure about the force profiles.]

**In a conversation:**

- **"That's not how it's done."** The reply that moves things forward is not *why not* but *where have you seen it done, and what was true there?*
- **"We need to be pragmatic about the database."** Ask what outlives what. The answer decides it, and it is a fact rather than a preference.
- **"Premature optimization."** True almost everywhere and false where the budget is fixed in advance. The question is whether there is a *later* in which to optimize.
- **Someone senior giving advice that is obviously wrong here.** The most likely explanation is not that they are wrong. It is that they are right somewhere else and have not been asked which force they are reading.
[-- these points need to be tied to force profiles]

The question that does the work: **which force here is outside its ordinary range, and what does it hold still?**

Every inversion in this chapter is that question answered. If every force sits in its ordinary range, you are in the ordinary case, the mainstream advice applies, and the interesting thing about your system is somewhere other than its architecture.

---

**Next:** chapter 21 turns from profiles to ecosystems — why two languages solving the same problem settle on conventions that contradict each other, and what an idiom is actually worth once you can see where it came from.
