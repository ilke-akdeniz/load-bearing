# The Force-Map Method

## The claim

**Design advice can be checked with the sequence of forces, principles, idioms. Following a principle when the forces it depends on are missing and following and idiom when the principles it serves are not needed are design failures.**

Everything before this chapter was diagnosis. This is the procedure, and it is short enough to state in three lines before the rest of the chapter argues about it.

---

## The demonstration

### The three steps of force-mapping

**One: read the forces.** Not the requirements — the forces. Chapter 03 names seven and gives each a question: how many at once apply in your situation and do they touch the same state; how long what this writes outlives the code; what happens when it is wrong and who finds out; how often it changes and how many places change with it; how many person must agree and how many will still be here; what the latency budget is and what fraction one mechanism costs; whether you can change every call site and would know if you broke one.

Answers are values, not verdicts. *Concurrency: two writers, same row, twice a second.* Not *concurrency is important.*

**Two: derive the principles those forces support.** A Principle is good advice given certain forces (Ch. 02), so with the forces in hand the derivation is mechanical in one direction: information hiding follows from not controlling your callers; idempotency follows from at-least-once delivery; a version column follows from concurrent writers and a rule spanning the read and the write.

**Three: check the idioms last.** An idiom is a local convention. Once you know which principles you need, the question about any convention becomes answerable: does this serve the principle, is it neutral, or does it work against it? Before you know that, the same convention is just what people do here.

This specific sequence of steps is the whole of the method. Following the same steps in any other is not permitted.

### Four systems, read cold

Here are four systems described by the forces that apply to each. We know nothing about their architecture or stack. [-- we know nothing is not true, we expand later: the script is a one-off data migration...]

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

**Make illegal states unrepresentable** (Ch. 12). For the ledger this is worth a type and a constructor per rule: durability is decades, so a bad row outlives every engineer who could explain it, and blast radius is money. For the script it is waste — the invalid state cannot outlive an afternoon, and the re-run is the recovery. Same technique, opposite verdicts, and the force that moved was durability.

**Hide the representation** (Ch. 05). For the library this is the central obligation: control of callers is *none*, so anything observable becomes a commitment you cannot withdraw. For the simulator it inverts — the memory layout is the design, and hiding it costs the frame budget, which is the case chapter 05 works through as an entity-component system.  Force that apply is the latency budget, and it moved far enough to flip a Principle rather than to weaken it.

**Write the decision down** — a log entry with the options that lost. For the ledger, yes: change is add-only and the people who made the decision will be gone before the schema is. For the script, no. The decision does not outlive the week, and the log is a cost with no reader.

**A version column on writes** (Ch. 06). For the ledger it follows from the forces alone: two writers, one row, a rule that spans the read and the write. For the script, concurrency is *none*, so the Law is inert (Ch. 02) — not overruled, not risked, simply not engaged.
[3 out of 4 of these verdicts is a battle between ledger and script, that is not ok, more variety is needed to make a point.]

Four systems, four different sets of correct advice, and no disagreement anywhere. Every difference traces to a cell in the table. [-- what's the idea of this sentence? "No disagreement anywhere", what does that even mean? Maybe just delete this sentence.]

### What the map records
The output is not a design. It is a record of which decisions were forced and which were chosen — and that distinction is the thing you cannot reconstruct later.

A forced decision has a force behind it: *this is a version column because two writers touch one row.* A chosen decision does not: *this is a version column because that is what we do.* Both produce the same code. Only the first can be revisited when the force changes, because only the first says what would have to change.

Which answers a question chapter 03 raises and leaves open — forces move on their own clock, and nobody revisits the design when they do. A force map is what makes that revisit possible: it says *this decision assumed two writers*, so when the second writer disappears, there is something to search for.

[The name of the chapter is "Force-map method", this section is "what the map records", there are some sentences about what the map does and why it's useful, ok but where is the map!? Show me an actual, detailed, force-map so that I can believe you... Not something like the summary table above but a force-map, used for one example system for one or mupltiplr design problems, using the ideas of this chapter, showcasing how to do it, and what the map offers. And it better be as close to real-world situations as possible, otherwise this becomes the same as the caricature situations attached to design problems: makes sense when you read it but you never encounter that shape in real world. If you have a goode force-map example, you can expand on that on the remainder of the chapter to illustrate the existing ideas.] 

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

**Then escalate, and say what you are escalating.** A genuine conflict between latency and durability is a business decision wearing technical clothes. Handing it up is correct, and the map is what makes the hand-off usable: *we can have four nines or sub-ten-millisecond writes, not both, and here is what each costs.* [-- small clarification needed, maybe different wording, I don't get this: "we can have four nines or sub-ten-millisecond writes"] That sentence is answerable by someone who does not write code. *Which is more important, speed or reliability* is not.

The method's honest limit is here. It does not resolve conflicts. It converts them from arguments about taste into a stated trade with named quantities, and then somebody decides.

### Grilling: the method with a generator in the loop

[slight problem with this section: This is about using a skills file while doing ai assisted development or while letting AI generate the code to be more clear. But that is never communicated and for the reader it's hard to understand what's going on here: "grilling, generator, loop... What!?"]

The procedure above assumes you can name the forces before the design exists. Usually you cannot — not because you are careless, but because you do not yet know which decisions are about to be made, so you do not know which facts about your situation are about to matter.

One technique inverts the flow, and it is worth stating in full because it is the method's shape with the roles swapped. Instead of supplying forces up front, you have the decisions surfaced one at a time and supply the fact that settles each one as it arrives. The instruction, quoted as the author of this book uses it:

> Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.
>
> Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.
>
> If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.
>
> Do not act on it until I confirm we have reached a shared understanding.

The technique is not this book's. It comes from Matt Pocock's skills repository, as `skills/productivity/grilling/SKILL.md`, and this book's author encountered this use of it through a video by Jason Ku. The version quoted above is an earlier one, frozen here because the upstream text has since changed.

**The split between fact and decision is the load-bearing line.** Facts get looked up; decisions get put to the human. That is the force-map method's step one and step two, separated and given owners — and the separation is what makes the output auditable, because every decision arrives with a recommendation you either took or overrode.

Which is where the value is, and it is not obvious. [-- empty filler sentence, maybe remove it] The recommendation comes from the corpus, so it is the majority ecosystem's convention arriving as a default. Overriding it is a local force beating a corpus convention — and that is only possible because the convention was made visible as a *choice* rather than delivered as code. A generated file contains the same decision, unmarked. [-- which recommendation, what corpus? Maybe a small example can shed light on all these: A prompt, first grilling question, human choose default, then another one, human overrides, decisions logged..]

**The two versions if the grilling skill file disagree on a real point, and it is a force question rather than an improvement.** The frozen text says *asking multiple questions at once is bewildering* and asks one at a time. The current upstream version organizes questions into rounds over a frontier of decisions whose prerequisites are settled, and asks a whole round at once. The trade is throughput against how much the human has to hold in working memory. Which wins depends on how many decisions are in flight and how much context each carries, which is a force with a value, and neither version is a regression. [-- Does this paragraph really add much value to this chapter? I'm not sure, it looks like this can be remove to me.]

**The limit, and it is severe.** Grilling surfaces the decisions the model recognizes *as* decisions, and that set comes from the same corpus. A question settled uniformly across the training data does not present itself as a branch point at all — it is simply how things are done.

So the technique is weakest exactly where a monoculture is strongest. It surfaces contested choices and conceals settled ones, and settled-in-the-corpus is precisely the class most likely to be wrong outside the ecosystem it came from. This follows from chapter 02's mechanism rather than from any measurement, and it should be read as reasoning.

---

## Why the claim holds

The three kinds stand in a fixed relation, and the relation is what makes the order work.

Forces are facts about your situation. They are not advice, they cannot be argued with, and they are the only inputs the other kinds take. Principles are conditional on them — *good advice given certain forces* — so a Principle without its forces is a conclusion with its premises removed. Idioms are conventions local to an ecosystem, which means the question *is this idiom right* is not answerable at all until you know which Principle it is supposed to serve.

So the dependency runs one way: idioms depend on principles, principles depend on forces, forces depend on nothing. Read in that direction, every step has an input from the step before, and every claim has something that would falsify it — *this Principle applies because concurrency is at this value* fails the moment concurrency is measured and it isn't.

**Read in the other direction, nothing falsifies.** Start from *we use repositories here* and there is no subsequent step at which the repository could turn out to be wrong. You can derive a principle that justifies it and then find forces that support the principle, and the whole chain will be internally consistent and unfalsifiable, because it was assembled from the answer backwards. That is not a failure of rigour. It is what working backwards from a conclusion produces every time, in any field.

Which is also why the method's output is a record rather than a design. Two teams can run it on the same system and reach different designs, because step two under-determines the result and conflicts get decided rather than computed [-- maybe this part: "because step two...and conflict get decided rather than computed" is key to my previous tag bit it's too compressed and I don't understand it wholly]. What they cannot do is disagree about the forces without one of them being wrong about a fact — and that is a smaller and much more tractable argument than the one they would otherwise be having.

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

**It requires the expertise it appears to replace.** This is the condition to state most harshly, because the method reads like a substitute for experience and is the opposite. Deriving *idempotency follows from at-least-once delivery* requires already knowing what at-least-once delivery implies. Reading a latency budget as a force requires knowing what a mechanism costs. The method organizes knowledge you have; it does not supply knowledge you lack, and a force map produced by someone who cannot price the options is a confident-looking document with the wrong cells filled in.

The same holds for the countermeasure in the previous section. Overriding a generator's recommendation is only possible for someone who can tell that the recommendation is a convention rather than a consequence — which scales with depth in that specific domain, and is the opposite of what people usually want from these tools.

[-- I wrote this tag first on an earlier place, before reading the two paragraphs above. I think these paragraphs answered my questions that follow. I'm still gonna paste it here because maybe some of my interpretation is valuable:  deep question, not trying to criticise but I'm genuinely curious: If forces are facts why the first step is "read the forces" and we said this: "Facts get looked up; decisions get put to the human. That is the force-map method's step one and step two, separated and given owners". My point is that "force" and "facts" sound like physics, you take an instrument and measure them and they are either there or not. Obviously they are not like that in the sense we used on our book, something requires human judgment, perception, even group decisions. Can we uncover and explain that clearly?]

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
- **Two people arguing about a design for more than ten minutes.** Chapter 03's finding is that they are almost never disagreeing about the answer; they are holding different values for the same force and have not said so. Stopping to write the forces on a whiteboard ends more of these arguments than continuing them does.

The question that does the work: **which fact about our situation would have to change for this to be the wrong choice?**

Ask it of your own decisions and it produces the force map as a by-product. Ask it of advice arriving from outside and it is the same question chapter 15 ends on, pointed at the present rather than at a source. If there is no answer — if no fact about the situation could make the choice wrong — then what you are holding is not a design decision, and finding out which of the five kinds it actually is takes one pass through chapter 02.

---

## Sources

- Matt Pocock, *skills* — [github.com/mattpocock/skills](https://github.com/mattpocock/skills), `skills/productivity/grilling/SKILL.md`. The text quoted here is an earlier version, frozen; upstream has since changed.
- Jason Ku, on using the technique during development — [youtube.com/watch?v=ikGhv9kKFdU](https://www.youtube.com/watch?v=ikGhv9kKFdU&t=356s).
- FlowCore, `docs/decisions.md` — [github.com/ilke-akdeniz/flowcore](https://github.com/ilke-akdeniz/flowcore).

---

**Next:** chapter 20 runs the method across six domains and finds that each one's dominant force inverts a piece of standard advice — not weakens it, inverts it, so that the thing to do is the opposite of what the advice says.
