# The Force-Map Method

## The claim

**Design advice is checked in one sequence: forces, then principles, then idioms. A principle followed where its forces are absent, and an idiom followed where its principles are not needed, are the two ways a design goes wrong while every decision in it still looks correct.**

Everything before this chapter was diagnosis. This is the procedure, and it is short enough to state in three lines before the rest of the chapter argues about it.

---

## The demonstration

### The three steps of force-mapping

**One: read the forces.** Not the requirements — the forces. Chapter 03 names seven and gives each a question: how many run at once and do they touch the same state; how long what this writes outlives the code that wrote it; what happens when it is wrong and who finds out; how often it changes and how many places change with it; how many people must agree and how many will still be here; what the latency budget is and what fraction one mechanism costs; whether you can change every call site and would know if you broke one.

Answers are values, not verdicts. *Concurrency: two writers, same row, twice a second.* Not *concurrency is important.*

**Two: derive the principles those forces support.** A Principle is good advice given certain forces (Ch. 02), so with the forces in hand the derivation is mechanical in one direction: information hiding follows from not controlling your callers; idempotency follows from at-least-once delivery; a version column follows from concurrent writers and a rule spanning the read and the write.

**Three: check the idioms last.** An idiom is a local convention. Once you know which principles you need, the question about any convention becomes answerable: does this serve the principle, is it neutral, or does it work against it? Before you know that, the same convention is just what people do here.

The sequence is the whole of the method. The same three steps in a different order do not fail loudly — they produce an answer that looks the same and cannot be checked, which is what the rest of this chapter is about.

### Reading a force is not measuring one

Chapter 03 calls forces facts about your situation, and the word invites a picture that is wrong: an instrument, a reading, a number. Some are like that. Row counts, request rates, latency budgets, the number of people with commit access, how many clients you cannot contact — these are countable, and where they are countable a disagreement is settled by going and counting.

Most are not. *What happens when this is wrong and who finds out* requires knowing what the system is for and who is downstream of it. *How often does this change and how many places change with it* requires a history somebody has to remember or reconstruct. Both are judgements, and two competent people can read them differently.

And a third thing decides more than either: **which facts count as forces depends on the decision in front of you.** The same system has different force readings for different questions. Concurrency is the dominant force for one decision in a codebase and entirely inert for the next one, twenty lines away.

So step one is not instrument work, and this is where the expertise the last section of this chapter charges for actually goes. What the method claims is narrower than measurement and is still worth something: **a force is the kind of thing that has an answer.** Two people disagreeing about whether callers can be changed are disagreeing about a fact, and can go and find out. Two people disagreeing about whether a repository is good architecture are not, and cannot. Moving an argument from the second kind to the first does not win it. It makes it winnable.

### Four systems, read cold

Here are four systems, given only as force readings. Nothing about their architecture, their stack or their teams appears in the table, and nothing needs to.

```text
 force              script    ledger    library   simulator
 -----------------  --------  --------  --------  --------
 concurrency        none      real      unknown   extreme
 durability         hours     decades   years     frames
 blast radius       re-run    money     users     a glitch
 change shape       none      add-only  add-only  constant
 team, turnover     one       many      strangers small
 latency budget     none      ms        none      µs
 control of callers total     total     none      total
```

The script is a one-off data migration, run once and deleted. The ledger records money movements. The library is published to people you will never meet. The sim is a real-time loop with a frame budget.

Nothing in that table is a design decision. Every cell is a fact somebody could check.

### The same advice, four verdicts

Now run advice the book has already graded across all four, and watch it change value.

**Make illegal states unrepresentable** (Ch. 12). For the ledger this is worth a type and a constructor per rule: durability is decades, so a bad row outlives every engineer who could explain it, and being wrong costs money. For the script it is waste — an invalid state cannot outlive the afternoon, and the re-run is the recovery. The force that moved is durability.

**Hide the representation** (Ch. 05). For the library this is the central obligation: control of callers is *none*, so anything observable becomes a commitment you cannot withdraw. For the simulator it inverts — the memory layout *is* the design, and hiding it costs the frame budget, which is the entity-component case chapter 05 works through. The force that moved is the latency budget, and it moved far enough to flip a Principle rather than weaken it.

**Compatibility is add-only** (Ch. 09). For the library this binds absolutely: you cannot deploy other people's software, so a removed field is a permanent break in code you will never see. For the ledger and the script it does not bind at all, because you control every caller and can change them in the same commit. The force that moved is control of the callers, and note that it did not weaken the rule anywhere — it removed it, and a rule that does not apply is not a rule you get partial credit for following.

**One writer, no coordination** (Ch. 06). For the simulator this is the design: each system owns its arrays, nothing else writes them, and the coordination cost falls to zero — which is the only way the frame budget survives extreme concurrency. For the ledger it is unavailable. Many clients write the same rows and none of them can be made to stop, so the concurrency has to be paid for rather than removed. Same force at a similar value, opposite answers, because what differs is whether you control who writes.

Every difference above traces to a cell in the table, which means each one can be checked instead of argued.

### A map, for one real decision

The table above is a comparison, not a map. Here is a map: one decision, from a real system, written the way the method produces it.

A FlowCore workflow definition is a four-level tree — definition, statuses, steps, actions — and the decision is what happens when a client fetches one.

```text
 decision    Get returns the whole definition tree, assembled from four
             queries run inside a repeatable-read transaction

 forces      concurrency    definitions are edited while being read
             blast radius   a torn read is a definition that never
                            existed: steps from before an edit,
                            actions from after
             latency        four round trips, against one join whose
                            fan-out is 15 rows to dedupe
             durability     schema; outlives the code that reads it
             callers        a library, so they are strangers

 licensed    atomicity: a reader sees the whole tree or none of it
             -> deep Get, because a shallow one hands back the
                partial view the invariant exists to ban
             -> snapshot isolation, because four separate queries on
                the pool can straddle a concurrent edit

 idioms      "just use a join"      rejected: 5 steps x 3 actions
 checked                            fans out to 15 rows to dedupe,
                                    and left joins for empty sets
                                    get fiddly
             "defer concurrency     rejected: this is not concurrency
              work until later"     work, it is this read's own
                                    correctness condition

 forced      the transaction, by concurrency and blast radius together
 chosen      four queries over one join; a join satisfies the same
             principle, so this one is legibility and can go back
 deferred    completion-path locking, until that path is written

 revisit if  definitions stop being editable while readable, or the
             tree stops fitting in four queries
```

Every line above is in FlowCore's decision log already, in prose. The map is the same information in the order the method produces it, and the three lines near the bottom are the ones nothing else in a codebase records.

**Forced, chosen, deferred is the distinction that does the work.** The code shows a transaction. It does not show that the transaction was forced — that concurrency and blast radius together left no other option — and someone reading it later cannot tell whether removing it would be a cleanup or a data-loss bug. The log says which, in its own words: the wrapper is taken now *"because it's this read's own correctness condition."*

The *chosen* line is the one people skip, and it is the most useful. Four queries against one join is a legibility call; a join would satisfy atomicity equally well. Writing that down means the next person can revisit the query shape without re-opening the question of whether the read has to be atomic. Without it, both look like the same kind of decision, so touching either feels equally risky and nobody touches anything.

The *deferred* line is a decision, not a gap. Completion-path locking is not missing; it is scheduled against a trigger, and the entry says so — the justification "is kept local to Get; it's not precedent for building other concurrency machinery this slice." A deferred decision with a stated trigger is chapter 03's reversibility rule leaving a mark.

And *revisit if* is what makes the map outlive the decision. Forces move on their own clock, and a codebase does not announce it when they do. This line converts that into something a person can search for.

**None of which is a new artifact.** Chapter 12 lists the architecture decision record among the patterns that answer team size and turnover — the reasoning written down while it was fresh, for the people who were not in the room. A force map is what an ADR's first section already asks for, and the original template says so in the book's own vocabulary. Michael Nygard's, from 2011: the Context section *"describes the forces at play, including technological, political, social, and project local."*

His reason for the practice is this chapter's argument in different words. Without the rationale, whoever arrives later is left either accepting decisions that may no longer apply, or reversing them without knowing what they cost.

So what the map adds is two lines. **Forced against chosen** — an ADR's Context can carry it and usually does not, because describing the forces and saying which of them left no alternative are separate sentences, and only the second one tells you what is safe to touch. And **revisit if**, which is not Nygard's Status. Status is set after a decision has been superseded; *revisit if* is written before, and names the thing to watch for. One records what happened. The other is a trigger.

### What the map records
Generalising from that: the output is not a design. It is a record of which decisions were forced and which were chosen, and that distinction is the one thing you cannot reconstruct from the code afterwards.

A forced decision has a force behind it — *this is a version column because two writers touch one row.* A chosen decision does not — *this is a version column because that is what we do.* Both produce identical code. Only the first says what would have to change for it to stop being right.

Which answers something chapter 03 raises and leaves open. Forces move on their own clock, and nobody revisits a design when they do, because nothing signals it. A map is what makes the revisit possible: it says *this assumed two writers*, so when the second writer goes away there is a sentence to search for.

### How to notice a principle whose forces are absent

Most principles in a codebase were not derived there. They arrived with a framework, a previous employer, or a book, and the question is whether the situation they answer is your situation.

The test is one question, and it is the reverse of the derivation: **what would have to be true for this to be unnecessary?**

If the answer comes back concrete — *if only one process ever wrote to this table* — you have found the force, and you can go and look at whether it holds. If the answer is *nothing, it is just good practice*, the principle arrived without its conditions and nobody in the room can say what it is for. That is chapter 15's mechanism, detected from inside your own codebase rather than in a talk.

The failure has a shape worth naming. Inherited principles cluster: a codebase does not carry a single one, it carries the whole set that travelled together from similar sources. Finding one unforced principle is a reason to look at its neighbours.

### When the forces conflict

Chapter 03 states the problem and hands it here: low latency pulls against durability, a small team pulls against a large blast radius, and naming both does not tell you which wins. It does not, and no method computes it. Trade-offs are decided.

What the map does is make the decision smaller. Five moves, roughly in the order worth trying them.

**Check that both forces are at the values you assumed.** Conflicts dissolve under measurement more often than they get resolved. *Low latency* is a budget with a number; *durability* is a retention period someone can name. Two people arguing usually have different numbers in mind and have never said them out loud.

**Look for the third option.** Most conflicts are between two implementations rather than two requirements. Durability against latency is irreconcilable if the choice is *write to disk synchronously* versus *do not*; it often dissolves at *write to a log and acknowledge*, which is chapter 07's outbox reasoning applied one level down.

**Ask which direction is reversible.** Chapter 03's rule decides this: if one branch is cheap to walk back and the other is not, take the reversible one and buy information. That is not a compromise; it is choosing to decide later with more facts, which is a different thing.

**Bound the loss instead of estimating the odds.** When you cannot say which force wins, you can usually say what it costs to be wrong in each direction. Pick the branch whose wrong case is survivable. Chapter 03 draws the line this sits on — a risk with no instrument is bounded rather than estimated harder.

**Then escalate, and say what you are escalating.** A genuine conflict between latency and durability is a business decision wearing technical clothes. Handing it up is correct, and the map is what makes the hand-off usable: *we can acknowledge a write in under ten milliseconds, or we can guarantee it survives a machine dying, and we cannot do both on the same write — here is what each one costs.* That sentence is answerable by someone who does not write code. *Which is more important, speed or reliability* is not.

The method's honest limit is here. It does not resolve conflicts. It converts them from arguments about taste into a stated trade with named quantities, and then somebody decides.

### Grilling: the method under AI-assisted development

The procedure above assumes you can name the forces before the design exists. Usually you cannot — not because you are careless, but because you do not yet know which decisions are about to be made, so you do not know which facts about your situation are about to matter.

One technique inverts the flow, and it is worth stating in full because it is the method's shape with the roles swapped. Instead of supplying forces up front, you have the decisions surfaced one at a time and supply the fact that settles each one as it arrives. The prompt, quoted as the author of this book uses it:

> Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.
>
> Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.
>
> If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.
>
> Do not act on it until I confirm we have reached a shared understanding.

The technique is not this book's. It comes from Matt Pocock's skills repository, as `skills/productivity/grilling/SKILL.md`, and this book's author encountered this use of it through a video by Jason Ku. The version quoted above is an earlier one, frozen here because the upstream text has since changed.

**The split between fact and decision is the load-bearing line.** Facts get looked up; decisions get put to the human. That is the force-map method's step one and step two, separated and given owners — and the separation is what makes the output auditable, because every decision arrives with a recommendation you either took or overrode.

The recommendation attached to each question is where the value is, and it takes an example to see why. Two questions from the start of a real library, with the answers that were actually given:

```text
> Should ids be generated by the application or by the database?
  Recommended: the database, via a column default. One less thing
  for a client to get wrong.

< The application. A client assembles a whole definition offline
  and hands it over in one call, so the ids have to exist before
  any of it reaches Postgres.

> Then UUIDv4 or UUIDv7?
  Recommended: v4. It is the common default.

< v7. These are primary keys on a table that only grows, and v4
  scatters inserts across the index.
```

Both recommendations were sensible, both were overridden, and the same kind of thing did the overriding each time: a fact about this library that is not in any corpus.

The first is about how the library is used — a client builds a whole definition in memory before any part of it exists, so ids cannot come from a column default without splitting the call. The second is a latency-budget reading at volume: these are primary keys on a table that only grows, and v4 scatters inserts across the index.

Only the second is one of chapter 03's seven. **The seven are the forces that recur often enough to be worth naming, not a closed list**, and a situation will sometimes hand you a fact that settles a question without appearing on it. What makes both of them forces is the property from earlier in this chapter rather than membership of a list: each is checkable, and each says what would have to change for the answer to change.

And note who supplied them. In both cases the human, because both are facts about this situation — which is the one thing a recommendation drawn from what is common cannot contain. The recommendation is the majority ecosystem's convention arriving in the voice of an answer, which is an Idiom (Ch. 02) with its locality stripped off.

The alternative is not that these two decisions go unmade. Generated code would have carried both — a column default and a call to a v4 constructor — taken by whatever is most common, with nothing in the file showing that anything was chosen. Chapter 23 takes that case in full.

The narrower point here is the one worth keeping: **grilling does not produce better answers. It produces answers somebody can disagree with.**

And disagreeing with them later requires that they were written down. The interview produces a sequence of decisions with the reasoning attached, and the reasoning is the perishable half: an hour afterwards the code is still there and the override is not. So the last step of the loop is that each settled decision goes into the log — which is the artifact from earlier in this chapter, and the reason FlowCore's decision 12 was available to be mapped months after anyone made it.

That closes the circuit, and it is worth seeing as one thing rather than three. The interview surfaces the decision, the log records what settled it, and a standing instructions file promotes the answers that keep recurring into constraints so the same question stops being asked. Chapter 23 works through what that loop is for; here it is enough that grilling without the second step is a conversation, not a record.

The upstream text has since changed in a way worth one line: it asks a round of questions at once where the frozen version asks one at a time. That is throughput against how much the reader has to hold in working memory, which is a force with a value, so neither version is a regression.

**The limit, and it is severe.** Grilling surfaces the decisions the model recognizes *as* decisions, and that set comes from the same corpus. A question settled uniformly across the training data does not present itself as a branch point at all — it is simply how things are done.

So the technique is weakest exactly where a monoculture is strongest. It surfaces contested choices and conceals settled ones, and settled-in-the-corpus is precisely the class most likely to be wrong outside the ecosystem it came from. This follows from chapter 02's mechanism rather than from any measurement, and it should be read as reasoning.

---

## Why the claim holds

The three kinds stand in a fixed relation, and the relation is what makes the order work.

Forces are facts about your situation. They are not advice, they cannot be argued with, and they are the only inputs the other kinds take. Principles are conditional on them — *good advice given certain forces* — so a Principle without its forces is a conclusion with its premises removed. Idioms are conventions local to an ecosystem, which means the question *is this idiom right* is not answerable at all until you know which Principle it is supposed to serve.

So the dependency runs one way: idioms depend on principles, principles depend on forces, forces depend on nothing. Read in that direction, every step has an input from the step before, and every claim has something that would falsify it — *this Principle applies because concurrency is at this value* fails the moment concurrency is measured and it isn't.

**Read in the other direction, nothing falsifies.** Start from *we use repositories here* and there is no subsequent step at which the repository could turn out to be wrong. You can derive a principle that justifies it and then find forces that support the principle, and the whole chain will be internally consistent and unfalsifiable, because it was assembled from the answer backwards. That is not a failure of rigour. It is what working backwards from a conclusion produces every time, in any field.

Which is also why the method's output is a record rather than a design. Two teams can run it on the same system and end up with different designs. There are two reasons, and both are honest.

Step two does not determine one answer. A set of forces licenses a set of principles, and more than one design can satisfy the same set — four queries or one join, as above. And where forces conflict, the method converts the conflict into a stated trade and hands it to somebody, who decides. Neither of those is a defect being excused; they are what the method claims, which is less than a procedure that outputs a design.

What the two teams cannot do is disagree about the forces without one of them being wrong about a fact. That is a smaller argument than the one they would otherwise be having, and unlike the other one, it ends.

---

## Where the claim doesn't apply

### The conventional answer is good enough

Most decisions do not deserve this. A form with three fields, a script that prints a report, a config file — the conventional answer is fine, the cost of being wrong is a rewrite that takes an afternoon, and the analysis costs more than the decision.

The test is chapter 03's blast radius applied to the decision itself rather than to the code: **what does being wrong here cost, and who finds out?** Where the answer is *me, in ten minutes*, take the convention and move on. The method is for decisions that are expensive to reverse, and using it everywhere is a way of never shipping.

### The forces are not knowable yet

Some forces cannot be read at the time the decision is made. You do not know the load, the team is not hired, the customers do not exist. Reading them is then guessing with a table attached, which is worse than guessing, because the table makes it look like analysis.

The correct move is chapter 03's: identify what would tell you, and defer if deferral is cheap. A force you cannot measure is not a force you get to assume.

### A decision with one live option

Sometimes the platform, the contract, or the existing schema leaves one thing you can actually do. Mapping the forces there is theatre. Write down that the option was forced by something external, which takes a line, and skip the rest.

---

## What the claim costs

**It requires the expertise it appears to replace.** This is the condition to state most harshly, because the method reads like a substitute for experience and is the opposite. Most of that expertise goes into step one, for the reason given earlier: reading a force is a judgement about which facts matter to the decision in front of you, not a measurement. Deriving *idempotency follows from at-least-once delivery* requires already knowing what at-least-once delivery implies. Reading a latency budget as a force requires knowing what a mechanism costs. The method organizes knowledge you have; it does not supply knowledge you lack, and a force map produced by someone who cannot price the options is a confident-looking document with the wrong cells filled in.

The same holds for the countermeasure in the previous section. Overriding a generator's recommendation is only possible for someone who can tell that the recommendation is a convention rather than a consequence — which scales with depth in that specific domain, and is the opposite of what people usually want from these tools.

**It costs real time per decision, and pays only under specific forces.** FlowCore carries thirty-eight recorded decisions for roughly five thousand lines. That ratio is justified by durability: those are schema decisions that outlive the code. On a script with a known death date the same ratio is waste, and saying so is not a hedge — it is the method applied to itself.

**The map goes stale silently.** Forces move on their own clock (Ch. 03) and nothing in a codebase announces that the team grew, the client count doubled, or the row count crossed the point where the query plan changed. A force map records what was true when it was written, which is what makes the revisit possible and also what makes it necessary.

**It is socially expensive in a room that has already decided.** Asking *what forces support that* reads as obstruction when everyone else is on the implementation. The move that works is narrower: ask what would have to be true for the choice to be wrong. It is the same question, it takes one sentence, and it does not require anyone to defend a position they have not yet realized they are holding.

---

## How to recognize the failure

**In a codebase:**

- **A principle nobody can price.** Ask what it would cost to stop following it and the answers are about correctness in general rather than about this system.
- **The same convention at every scale.** An interface at every boundary, a folder per layer, a test per class — applied uniformly is a sign nothing was derived, because forces vary across a codebase and derived answers vary with them.
- **Configuration for a force that has one value.** A pluggable strategy where one strategy has ever been used, a timeout that is settable and has never been set. Somebody anticipated variation the situation does not have.
- **Decisions recorded as descriptions.** *We use event sourcing* is not a record. *We use event sourcing because the audit requirement is a legal retention period and reconstruction has to be exact* is one, and only the second can be revisited.

**In a conversation:**

- **"That's the standard approach."** True and irrelevant until someone says which force it answers. The useful reply names one: *standard where the callers are strangers — are ours?*
- **"We might need to scale."** *Scale* is not a force; chapter 03 splits it into steady load, bursts and data volume, which have different designs. The question is which one, at what number.
- **"Let's keep it flexible."** Flexible against what? Flexibility is bought against a specific change, and a change nobody can name is not one you can prepare for (Ch. 18).
- **Two people arguing about a design for more than ten minutes.** Write the forces down instead. It ends more of these arguments than continuing them does, for the reason chapter 03 gives.

The question that does the work: **which fact about our situation would have to change for this to be the wrong choice?**

Ask it of your own decisions and it produces the force map as a by-product. Ask it of advice arriving from outside and it is the same question chapter 15 ends on, pointed at the present rather than at a source. If there is no answer — if no fact about the situation could make the choice wrong — then what you are holding is not a design decision, and finding out which of the five kinds it actually is takes one pass through chapter 02.

---

## Sources

- Matt Pocock, *skills* — [github.com/mattpocock/skills](https://github.com/mattpocock/skills), `skills/productivity/grilling/SKILL.md`. The text quoted here is an earlier version, frozen; upstream has since changed.
- Jason Ku, on using the technique during development — [youtube.com/watch?v=ikGhv9kKFdU](https://www.youtube.com/watch?v=ikGhv9kKFdU&t=356s).
- Michael Nygard, *Documenting Architecture Decisions*, 15 November 2011 — [cognitect.com/blog/2011/11/15/documenting-architecture-decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
- FlowCore, `docs/decisions.md`, decision 12 — [github.com/ilke-akdeniz/flowcore](https://github.com/ilke-akdeniz/flowcore).

---

**Next:** chapter 20 runs the method across six force profiles and finds that the forces each one pins invert a piece of standard advice — not weaken it, invert it, so that the thing to do is the opposite of what the advice says.
