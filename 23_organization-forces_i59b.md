# Organization Forces: What Decides the Process

## The claim

**Organization Forces decide which development processes can work. A process template adopted without reading them produces ceremony where no Force is acting, and surprises where one is acting unread.**

Every chapter so far has worked on the software. This one works on the arrangement around it — who decides what, how often the goal moves, how long an answer takes to arrive — because those are read the same way and settle the same kind of question.

## A word on two kinds of Force

[Chapter 02](02_forces_f4m5.md) named seven Forces and gave each a question. Look at what each of its answers changes and a pattern appears: *whether a mistake is correctable*, *how much prevention is worth buying*, *where the rule lives*, *what you can spend on abstraction*. Every one of the seven is read for its effect on **the design**.

So call those **design Forces**, and the name is applied here rather than there: [chapter 02](02_forces_f4m5.md)'s own claim already says *design arguments*, so nothing in it changes.

**Organization Forces are read the same way and change something else — how the work around the code is arranged.** Not what the code should look like, but who decides it, how much of the decision gets written down, how long the deciding takes, and which of that is worth doing at all.

The two sets are not a partition of the world into software facts and human facts. Team size and turnover is a fact about people and it is a design Force, because reading it moves a rule from a comment into the type system. What separates the sets is what the reading decides, not what the reading is about.

One of [chapter 02](02_forces_f4m5.md)'s seven already sits on the line. *Control of the callers* ends with **what changes with the Force: not the design, the *plan*** — which is this chapter's territory, reached from the other side. And [chapter 18](18_force-map-method_r37x.md) left the door open in terms: *the seven are not a closed list … what makes something a Force is the property below rather than membership of a list.*

That property is the one that decides membership here too, and it is worth restating because it disqualifies the most tempting candidate. **A Force has an instrument. A risk has none** ([Ch. 02](02_forces_f4m5.md)). *How senior is this team* can be answered by looking at the team. *Will the client change their mind*, *will this department be reorganized*, *will the budget survive the quarter* cannot be answered by looking at anything, and treating them as Forces to be estimated harder produces a number with no content. They are risks, and [chapter 02](02_forces_f4m5.md)'s reversibility question is the only thing that still works on them.

---

## Six Organization Forces

| Force | The question that reads it |
|---|---|
| **Skill spread** | How much can be left to judgement, and how much has to be specified? |
| **Requirement volatility** | How often does the goal move, and who moves it? |
| **Decision latency** | How long from a question being asked to an answer arriving? |
| **Budget and runway** | How much is there, and how much of it can go on records? |
| **Team Distribution** | Same room, same timezone, or neither? |
| **Regulatory obligation** | What has to be recorded whatever the other readings say? |

The first three are worked below. The others are read the same way and are listed rather than argued, for the reason [chapter 11](11_patterns-that-survive-translation_us2k.md) lists most of its entries: by now the method is the point, not the inventory.

### Skill spread

> **How much can be left to judgement, and how much has to be specified?**

[Chapter 18](18_force-map-method_r37x.md)'s method has three steps — read the Forces, derive the Principles, check the Idioms — and the third step is the one whose ownership moves with this reading.

At one end, everyone deriving the code can run that third step themselves. Tell them the rule about money is that amounts are minor units and never built from a float, and they will arrive at an unexported field and a constructor without being told which. The specification stops at the Principle.

At the other end, the third step has to be supplied, and supplied again. The same instruction produces a float somewhere, because knowing that a Principle implies a particular Idiom in this language is a separate piece of knowledge from holding the Principle.

**When the team is capable of deriving Idioms, specify the Principle and stop. When it does not, specify the Idiom too — and budget for specifying it again on the next feature, because a specification is not a transfer of the judgement that produced it.**

That last clause is where the reading is usually misread. Skill spread is read once and then treated as though writing enough documents would move it, and they do not: a document records a conclusion, and [chapter 22](22_never-written-down_at4r.md) is about the difference between a conclusion and the reasoning that produced it. What changes skill spread is people arriving, leaving, or learning, on a timescale no document reaches.

**What changes with the Force:** where the specification stops, and how often the same specification has to be issued again.

### Requirement volatility

> **How often does the goal move, and who moves it?**

Two halves, and the second decides more than the first. A goal that moves twice a year because you learned something is a different Force from a goal that moves twice a month because somebody didn't read the goals correctly.

The first is ordinary and cheap. The second produces the sequence every engineer recognises:

```text
week 1   we are building X for client A
week 3   the focus is now Y for client B
week 6   client B doesn't want Y, they need Z 
week 8   there is not enough budget left for Z
```

Nobody in that sequence made a mistake, which is what makes it corrosive. Each move was a reasonable response to something that had genuinely changed, and the accumulation is four weeks of work that produced nothing and a team that has stopped believing the current goal.

**When the goal moves on somebody else's schedule, write scope per slice and expect to throw slices away. When it moves on yours, write it once and hold people to it.**

The distinction is not planning horizon, it is *whose* horizon. A team that controls its own goal can plan a quarter. A team whose goal is set by a client mid-quarter cannot plan past the next commitment it can actually get, and the planning apparatus it is asked to run — roadmaps, quarterly commitments, story maps reaching six months out — produces documents that are wrong before they are read.

[-- And something worth condidering in "building X" example, did the client change his mind or did we get the requirement wrong the first time? My personal experience is that clients never change their mind on their business rules and invariants. Those are established facts about their business. I tried to fix this section by makind edits to reflect that incorrect read of requirements but there is still too much work left. The example is a mix of focus - priprity change, then bad requirement gathering, then budget contstraint arriving suddenly. My point with creating this examples was showcasing the price of bad decisions made by people outside the team, sabotaging all the teams efforts. Somebody decided that the team should switch from X to Y, no reasons, no input, just switch all work is gone to trash, then somebody got the requirements wrong, trash again, the somebody got the budget wrong, trash again. I don't know how all these fit into this "requirement volatility", maybe this is something like "context change": how many context (projects) you handle concurrently, are the contexts brought to a closure or you jump from one skeleton to another one?]

FlowCore is the small case, and it is a single-developer project, so it can show this Force and none of the ones about several people. Its instructions file writes the scope of each slice down and then forbids working past it: *"A capability earns its place this slice only if it's the correctness condition of something being built now, not because it's on the roadmap."* The goal moves there too. What the written slice buys is that the move is visible as a move, rather than as work quietly appearing. [-- we already gave too many flowcore examples in the book and this one has marginal value with high risk of disappointment. Would just delete this.]

**What changes with the Force:** how far ahead a plan can be written before writing it stops being planning.

### Decision latency

> **How long from a question being asked to an answer arriving?**

The reading is a duration, and it is measurable: pick the last five questions that blocked somebody and count the days.

An hour is a different system from two weeks. Where answers arrive in an hour, work proceeds question by question and nothing needs scheduling, because a question is asked when it appears and answered before it blocks anything. Where answers take two weeks, every question that could have been asked separately has to be asked together, because the alternative is two weeks per question in series.

That is the whole of it, and most meeting practice falls out of it rather than needing to be argued:

**When answers arrive in an hour, ask one question at a time and schedule nothing. When they take two weeks, batch the questions, and recognise that you are now designing around the wait rather than around the problem.**

A recurring meeting is what a team builds when decision latency is high and nobody has said so. It converts an unpredictable wait into a predictable one, which is a real gain — and it is paid for by everyone attending regardless of whether they had a question, which is the cost nobody prices. The honest version of the same trade is to say the latency out loud: *decisions here take a fortnight, so we batch them on Tuesdays.* That sentence is answerable. A standing invitation is not.

**What changes with the Force:** whether questions are asked singly or in batches, and therefore whether meetings are scheduled or summoned.

### The other three, briefly

**Budget and runway** is read as a number and decides how much of the work can go on records rather than on code. It is the Force most often read as a risk — *will the money last* has no instrument — when the readable version is *how much is committed, and what fraction of it is the recording costing*.

**Team Distribution** decides the shape of every synchronous thing. One room supports interruption as the default channel; three timezones make interruption impossible and written asynchronous decisions mandatory rather than virtuous. Most advice about remote work is this Force read at one value and stated without it.

**Regulatory obligation** is the one Force that can override every other reading. Where an auditor requires a signed record of who approved a change, that record is produced whether or not any other Force asks for it, and the only question left is whether it is produced once properly or twice badly.

---

## Why the claim holds

The claim says a process answers Forces or it answers nothing. The reason is that a process is not chosen [-- we need an adjective here, "a working process" maybe? People choose processes without deriving it all the time.], it is **derived** — and the derivation runs backwards from the thing you want to end up with.

### The chain, from the end

Start at the end and ask what each level needs in order to exist.

```text
level 1: software that is right for its context, and
survives design Forces moving
        ^
        |  depends on
        |
level 2: code matching the design Forces  +  records of the rules,
                             Forces and decisions
        ^
        |  depends on
        |
level 3: somebody who creates and maintains these
        ^
        |  depends on
        |
clear individual ownership 
```

Read downward it is unremarkable. Read upward it is the whole argument, because every level is load-bearing for the one above and the bottom level is the one nobody assigns.

**The top level is not "working software."** It is software that is still right after the Forces move, and [chapter 02](02_forces_f4m5.md) is explicit that they move without a commit: a team doubles, a service acquires a client outside the company, a table crosses a hundred million rows. Software that was right for a reading nobody wrote down cannot be checked against the new reading, because there is nothing to check against.

**The second level is why records are not documentation.** The code carries the decision; it does not carry the Forces the decision answered. [Chapter 18](18_force-map-method_r37x.md) owns what a record preserves — which decisions were forced and which were chosen — and [chapter 22](22_never-written-down_at4r.md) owns what happens when it does not exist. The chain adds only that both are prerequisites of the top level rather than good practice.

**The third level is where most process lives**, and where most of it is invented rather than derived. Standups, retrospectives, planning sessions, review policies: every one of them is an answer to *how do these get created and maintained*, and almost none of them was chosen by asking that question.

### Ownership is the leaf

The bottom of the chain is not a document or a meeting. It is one person, named.

**"Somebody" is the load-bearing word, and it is not a committee and not "the team."** A responsibility assigned to a team is discharged by nobody, and the mechanism is visible if you follow one engineer's reasoning after the assignment is made:

```text
"The team is responsible for designing feature X."

  How much time should I put into this? Not an afternoon —
  I have a high-priority ticket.
  I know feature X well and could design it properly.
  But others will object for reasons that are not good ones,
  and it will be rejected anyway. Why spend the afternoon?
```

Nothing in that is unreasonable, and none of it is fixed by asking harder. Ownership fixes it because it supplies two things a shared assignment cannot.

**It says the task is worth time.** An owner has a defensible answer to *why were you doing that instead of the ticket*, and without one the design work loses every collision with something scheduled.

**It says whose judgement settles it.** An owner is expected to hold the most context, so their answer stands unless somebody produces a better reason — which is a different position from having a view that must survive a room.

This is [chapter 08](08_change_rjf9.md)'s mechanism at a smaller scale. Conway's interfaces exist where two design groups had to negotiate one; where no group owns a piece, there is nobody to negotiate with, so the interface is not badly drawn — it is undrawn, and the seam appears later wherever the code happened to be cut.

**When a decision has an owner, the process around it can be thin. When it does not, no amount of process substitutes**, because every step you add is a step somebody has to decide to take.

---

## Where the claim doesn't apply

### The meeting that answers nothing, and is right anyway

The claim says a process step with no Force behind it is ceremony. Here is one that isn't.

A team meets for fifteen minutes on Friday with cameras on. Nobody is blocked, no decision is waiting, no clarification is needed — read every Force in the table and none of them asks for this meeting. By the claim it is ceremony, and the claim is wrong, because the meeting is answering something the claim does not model: people who work together do better when they have met each other.

The boundary is real and it is narrow, and the narrowness is the useful part. What makes this meeting defensible is that its reason is **stated and is not a work reason**: *we meet on Fridays for fifteen minutes to stay in contact with each other; we think it makes the rest easier.* That sentence can be disagreed with. The same meeting held daily, described as a standup, and defended as coordination is the failure — not because meeting is wrong, but because the stated reason is one the Forces do not support and the real reason has gone unsaid.

So the test is not whether a step answers a Force. It is whether the reason given for it is the reason it exists.

### The team that already reads them

The second boundary is sharper, because it turns this chapter's own prescription into the thing the claim warns about.

Take a small team of people who read Forces without being asked to — who have shipped several systems, who reach for the version column and the idempotency key without the derivation being spoken aloud, and whose record over some years is that the surprises did not arrive. Give them the apparatus in this chapter: a written force reading per feature, an owner named per decision, a record of what was forced and what was chosen.

Most of it is ceremony. The reading is already happening; writing it down answers no Force that was not already answered, and the claim's own definition convicts the chapter's own remedy.

Two conditions keep this from being the exception everybody claims.

**It holds only while the team is stable.** The reading lives in the people, and [chapter 22](22_never-written-down_at4r.md) is the chapter about what that costs when they leave: the reasoning is the perishable half, and there is no interval in which it is available and undocumented. A team of five who have worked together for six years is genuinely in this case. The same team the month after two of them leave is not, and nothing warns you at the transition.

**And the instrument is the record, not the self-assessment.** Many team believes it is "that" team. What distinguishes the ones that are is answerable: what did you ship, and what happened to it six months later. A team that cannot point at that is reading its own skill spread the way [chapter 02](02_forces_f4m5.md) warns Forces get read — from habit rather than from the situation.

---

## What the claim costs

**Reading these Forces demands the seniority it looks like it replaces.** [Chapter 18](18_force-map-method_r37x.md) states this for design Forces and it is worse here. *How much can be left to judgement* requires knowing what the judgement would have to produce; *how far ahead can we plan* requires having watched plans fail for reasons other than bad luck. A force reading produced by somebody who cannot tell a moved goal from a discovered one is a confident document with the wrong values in it.

**Naming a Force licenses machinery, and this set licenses the most.** [Chapter 02](02_forces_f4m5.md)'s warning applies unchanged and bites harder: *we have a wide skill spread* becomes a specification factory, *our requirements are volatile* becomes a change-control board, and both were built from the name without the intensity ever being read. The discipline is the same — no Force cited without a value beside it, or the words *we do not know* said out loud.

**The output is invisible when it works.** A design Force produces code you can point at. An organization Force produces a process, and a process that fits is one nobody notices, which makes it impossible to defend in the year somebody asks what the planning is for. The people who do this well are routinely described as having made things run smoothly, which is the description of an absence.

**It can be used to refuse work.** *What Force is that meeting answering* is a real question and an excellent way to avoid a meeting you did not want to attend. The same objection [chapter 09](09_what-a-pattern-is-for_3xzc.md) records about its two tests applies here: ask it where a process step is carrying the weight of a decision, not about every recurring event in the calendar. [-- I would just delete this. Reads like martial court sentences. Work refusal is not the best topic to talk about casually.]

**And the whole chapter is an ideal nobody occupies.** No team reads all of the forces, at intervals, with an owner named for each. The reason to describe the state anyway is that it's parts are still useful in isolation: naming one owner for one decision is available on Monday and does not require the rest, and a team that does only that is better off than one that adopted a template.

---

## How to recognize the failure

**In a codebase and its calendar:**

- **A standup where nobody is blocked.** Fifteen people report status to a room, and the two who needed each other could have said so in a message. Decision latency is low and the meeting is priced as though it were high.
- **A pointing session where nobody has read the tickets.** The estimate is produced anyway, which means it is a number about the room rather than about the work — and most of the people voting could not name the trade-offs in the ticket if asked.
- **An estimate that came in exactly on time.** One of two things happened, and both are worth knowing. Either it was generously padded and the surplus went somewhere invisible, or the Forces were not read and the work will come back as bug-fixing and gap-filling at some multiple of the original number.
- **A retrospective producing actions nobody owns.** The list is real, the observations are often good, and the leaf of the chain is missing, so none of it is discharged and the same items appear next month.
- **A recurring meeting whose reason nobody can state**, other than that it has always been there. The test is not whether it is useful — it is whether anyone can say which Force it answers, or admit honestly that it answers a different kind of need.
- **A design or architecture document that only describes the happy path.** Whoever wrote it did not use the system under load, under failure, or under an awkward customer, so the constraints that decide the design were never met. [-- which organization force is in play here. How does this relate to the chapters claim?]
- **Advice about a bug from somebody who has not reproduced it.** Confident, plausible, and untethered — and it costs the person who does have it reproduced an afternoon to disprove. [-- which organization force is in play here. How does this relate to the chapters claim?]

**In a conversation:**

- **"The team will decide X."** Nobody will. Ask which person, and watch whether the question is treated as pedantic.
- **"We're an agile team, we don't do big design up front."** Sometimes a correct reading of requirement volatility, and sometimes a reason not to write down the invariants of a system where getting them wrong is expensive to correct. The two sound identical.
- **"How long will this take?"** asked before anyone has read the Forces. There is no answer at that point that is not a guess wearing a number, and the honest reply is a comparison — this looks like the last thing of its shape, which took a month under conditions that will not repeat exactly.
- **"That's just process."** Usually true of the template, and used to dismiss the question underneath it, which is the one this chapter is about.

The question that does the work: **which Force is this step answering, and at what value?**

If there is no answer, one of two things is true, and they are worth separating. Either the step is ceremony, in which case it can go. Or it is answering something real that nobody has named — which is the more common case, and the more useful finding, because a step defended by *it just works better this way* is usually a Force somebody has read correctly and never written down.

---

## Sources

- FlowCore, `CLAUDE.md` — the per-slice scope rule — [github.com/ilke-akdeniz/flowcore](https://github.com/ilke-akdeniz/flowcore).

---

[← Ch. 22](22_never-written-down_at4r.md)  ·  [Contents](00_toc.md)
