# Assigned to the Team, Owned by Nobody

## The claim

**Software that is right for its context, and resilient to Force changes is the result of artifacts owned by the individuals with deep knowledge of the context**

Every chapter so far has worked on a claim somebody made about software. This one works on the arrangement that produces the software, and it is the only chapter whose subject is people. It is here because the arrangement is derivable — not from a methodology, and not from what worked somewhere else, but from what has to exist before the software can be right.

---

## The demonstration

### The chain, from the end

Start from the end goal and ask what each level needs in order to exist.

```text
end goal              software that is right for its context, and
                      survives its Forces moving
                        ^
                        |  depends on
                        |
artifacts             code matching the Forces, and records of the
                      rules, the Forces, and the decisions
                        ^
                        |  depends on
                        |
ownership             individuals who creates and maintains the artifacts
```

Read downward it is unremarkable. Read upward it is the argument, because each level is load-bearing for the one above it.

**The end goal is not "working software."** It is software that is still right after the Forces move. [chapter 02](02_forces_f4m5.md) is explicit that they move without a warning: a team doubles, a service acquires a client outside the company, a table crosses a hundred million rows. 

**The artifacts are not random meeting notes, powerpoint slides or chaos labeled as "documentation".** The code itself is an artifact. It applies the decisions that answer the Forces and enforces business rules. [Chapter 18](18_force-map-method_r37x.md) Pay attention to the words "apply, enforce". An ideal code reflects the decisions but it's not a record that tells what forces were present, what alternative options were available and why this specific option was chosen. [-- we talked about this on another chapter, I'm not usre if a chapter reference would be appropriata or too much here, between two existing references] Those records of decisions and business rules are separate artifacts to create and maintain. [chapter 22](22_never-written-down_at4r.md) owns what happens when these does not exist.

**The ownership is where people and processes around them enter into picture**. Standups, retrospectives, planning sessions, review policies: every one carries a tension that seeks a resolution. That tension comes from the question: *Which artifacts we need to create and who will create what?* But for many teams, that question is never asked and answered clearly and the meetings turn into a ceremony.

### Pre-code artifacts
Code is the most obvious artifact and the easiest to get the ownership right. Nobody will argue that code is not needed, nobody would say: "team will code this in next week's coding meeting." Letting indviduals work on development tickets assigned to their name is second nature. 

Problems start as you move to the artifacts that predate the code. Then you step on the land of chaos and ambiguity. You will hear statements like: "we don't need a list of the business rules we are agile." or "team will decide on the design of the feature X."  

We will focus on 4 artifact material that come before the code is written. Our claim is not that these are the most important ones or are the only ones. These are simply what following the advice of this book could land you on because 2-4 were already described as the force-map method on chapter 18.

### The rules and invariants

The root, because everything after it is conditioned on it. What must always be true of this system — an invoice reconciles, a booking cannot double-sell a seat, a payment is applied once.

Sometimes that is a hundred pages, sometimes one paragraph. **The length should reflect the rules that actually apply, not the prose style of whoever wrote it or the current mood of the team.** *We are an agile team* is not a reason to begin a medical scanner with a vague idea of what it does.

**Format** a statement of the invariants, in whatever length they take.

**What its owner must be able to do:** get a decision out of the business and refuse a vague answer. Not translate one — obtain one.

**When the rules are not written, write them before anything else. When somebody says they cannot be, that is the finding, and it is about the business rather than about the software.**

There is a myth that makes this step look optional, and it is worth naming because it is the reason it gets skipped. It is called *changing requirements*, which says the business rules move. They rarely do. A company's invariants are facts about how it makes money, and facts of that kind hold for years. What moves is which of them you were asked to serve this quarter — and rules that were never gathered properly surface months later as *the requirements changed*, when nothing changed except who finally read them. Both arrive at the team as churn, and only one of them is anybody's mind being altered. [-- I don't understand previous sentence, maybe just delete it]

### Step two: read the Forces

[Chapter 18](18_force-map-method_r37x.md)'s first step, and [chapter 02](02_forces_f4m5.md) owns the Forces themselves. Nothing is added here except position: it comes after the rules, because a Force is read against something, and *how bad is it when this is wrong* has no answer until somebody has said what wrong means.

Sometimes it takes two days. Sometimes it is an instinctive check that takes a minute and is still a reading — a bug fix in a path with one writer does not need a document to establish that concurrency is inert there.

**Artifact:** A written record of the force map, .

**What its owner must be able to do:** price the options. [Chapter 18](18_force-map-method_r37x.md) is blunt that this is where the expertise goes, and a reading produced by somebody who cannot say what a mechanism costs is a confident document with the wrong values in it.

**When the reading is instinctive, do it and move on. When two people read the same Force differently, stop — the disagreement is about a fact and somebody can go and check it.**

### Step four: derive the Principles

[Chapter 18](18_force-map-method_r37x.md)'s second step. With the Forces in hand the derivation runs one way and is close to mechanical: information hiding follows from not controlling your callers, idempotency follows from at-least-once delivery, a version column follows from concurrent writers and a rule spanning the read and the write.

**What it produces:** the advice that actually applies here, with the Force it answers written beside it.

**What its owner must be able to do:** recognise a Principle whose Forces are absent — which is [chapter 18](18_force-map-method_r37x.md)'s own test, and the reason this step is not a literature search.

**When a Principle arrives without the Force that supports it, ask which reading licences it. When nobody can name one, it was inherited rather than derived.**

### Step five: check the Idioms, and decide how much to say

[Chapter 18](18_force-map-method_r37x.md)'s third step, and the one whose ownership moves most.

An Idiom is a local convention, and [chapter 20](20_idioms_7nkn.md) owns why it is worth following even where you can out-argue it. What changes here is only how much of it has to be said out loud, and that depends on who is writing the code. Tell somebody the rule about money — amounts are minor units, never built from a float — and one team arrives at an unexported field and a constructor without being told which. Another produces a float somewhere, because knowing that a Principle implies a particular Idiom in this language is a separate piece of knowledge from holding the Principle.

**What it produces:** either nothing, or the conventions that have to be stated because they will not otherwise be derived.

**What its owner must be able to do:** tell the difference between the two cases, which is a judgement about people rather than about code.

**When the Idiom will be derived, state the Principle and stop. When it will not, state the Idiom too — and expect to state it again next time, because a specification records a conclusion rather than the judgement that produced it.**

### Step six: settle the Styles and stop

[Chapter 21](21_style_9rng.md) owns this and its finding is the whole of the step: there is no fact that settles a Style argument, so it ends when somebody who can enforce a style acts, and everything before that produces nothing.

So the step is not *decide the styles*, it is *end the discussion*. Pick a formatter, run it, and spend no further attention.

**What it produces:** a configuration file and no more meetings.
**What its owner must be able to do:** decide without a consensus and take the complaints.

**When a Style question is open, close it with a tool if one exists. When no tool exists — naming is the case — choose, write down why, and stop.**

---

## Why the claim holds

The chain says what has to exist. It does not say who makes it exist, and that is where the process fails, because every step above is work that somebody has to decide to do instead of something else.

### A step with no name is discharged by nobody

**"Somebody" is the load-bearing word, and it is not a committee and not "the team."** Follow one engineer's reasoning after a shared assignment:

```text
"The team is responsible for designing feature X."

  How much time should I put into this? Not an afternoon —
  I have a high-priority ticket.
  I know feature X well and could design it properly.
  But others will object for reasons that are not good ones,
  and it will be rejected anyway. Why spend the afternoon?
```

Nothing in that is unreasonable, and none of it is fixed by asking harder or by asking again next sprint. What fails is not effort. It is that a shared assignment supplies neither of the two things the work needs.

**It does not say the task is worth time.** An owner has a defensible answer to *why were you doing that instead of the ticket*. Without one, the design work loses every collision with something scheduled, and it collides with something scheduled every day.

**It does not say whose judgement settles it.** An owner is expected to hold the most context on the subject; an interchangeable team member is not. So the owner's answer stands unless somebody produces a better reason, which is a different position from having a view that has to survive a room.

This is [chapter 08](08_change_rjf9.md)'s mechanism at a smaller scale. Conway's interfaces exist where two design groups had to negotiate one — so where no group owns a piece, there is nobody to negotiate with, and the interface is not badly drawn. It is undrawn, and the seam turns up later wherever the code happened to be cut.

### Two things follow, and both are usually argued on other grounds

**A meeting is a decision assigned to a room.** By the claim, that is a step with no name against it, which is why the meeting that decides something rarely decides it and why the same subject returns three weeks later. What a meeting is good for is the opposite operation: getting a specific thing unblocked for somebody who already owns it, quickly, and ending. A standing invitation for a decision nobody owns is the shape the claim predicts, and it is normally defended as collaboration.

**Stages, transitions, and deliverables are ownership applied to the flow of work rather than to a decision.** None of the automation matters — not the pipeline, not the checks — if nobody can say when development ends and testing begins, or who is called when production breaks at two in the morning and what that person is permitted to do. Those are the same question as the dialogue above, asked about a boundary instead of a design.

---

## Where the claim doesn't apply

### Something not derived from the artifact, and right anyway

A team meets for fifteen minutes on Friday with cameras on. Nobody is blocked, no decision is waiting, no step of the chain requires it. Derive the process from the artifact and this meeting does not appear anywhere in the derivation — and it can still be the right thing to do, because it answers something the chain does not model: people who work together do better when they have met each other.

The boundary is real and narrow, and the narrowness is the useful part. What makes the meeting defensible is that its reason is **stated and is not a work reason**: *we meet on Fridays for fifteen minutes to stay in contact with each other; we think it makes the rest easier.* That sentence can be disagreed with. The same meeting held daily, called a standup and defended as coordination, is the failure — not because meeting is wrong, but because the reason given is not the reason it exists.

So the test the chapter leaves you with is not whether a step falls out of the chain. It is whether the reason given for it is the reason it exists.

### A step that needs two names

The claim's second half fails where the step is a negotiation.

[Chapter 08](08_change_rjf9.md) has Conway's mechanism in his own vocabulary: an interface exists where two design groups **negotiated and agreed upon** one. A decision that binds two teams cannot have a single owner, because a single owner would be one team imposing on the other, and what comes back is not agreement but compliance followed by a workaround.

So the step has two names against it, and the work is the negotiation. What does not change is that both names are individuals. *The platform team and the payments team will agree an interface* fails in exactly the way the dialogue above fails; two people, one from each side, with the authority to agree, does not.

---

## What the claim costs

**Where the derivation already happens, the artifacts are ceremony.** Take a small team who have shipped several systems together, who reach for the version column and the idempotency key without the derivation being spoken aloud, and whose record over some years is that the surprises did not arrive. Give them a written reading per feature and an owner named per decision and most of it answers nothing — they are running the chain, they are simply not writing it down, and the claim does not require writing.

Two conditions keep that from being the exception everybody claims. **It holds only while the team is stable**, because the derivation lives in the people and [chapter 22](22_never-written-down_at4r.md) is the chapter about what that costs when they leave. And **the instrument is the record, not the self-assessment**: many teams believe they are that team, and what distinguishes the ones that are is answerable — what did you ship, and what happened to it six months later.

**It demands the seniority it looks like it replaces.** [Chapter 18](18_force-map-method_r37x.md) states this for the middle three steps and it is true of all six. Deciding how much of an Idiom to state requires knowing what the team would otherwise derive; refusing a date requires knowing what the comparison is worth. The sequence organises judgement; it does not supply it.

**It is invisible when it works.** A design decision produces code you can point at. This produces an absence — the surprises that did not arrive, the meeting nobody scheduled, the rewrite nobody needed. The people who do it well are described as having made things run smoothly, which is not a description of anything you can put in a review.

**And nobody occupies the whole of it.** No team runs six steps with an owner named for each, at every scale, every time. The reason to set it out anyway is that the parts are separable and the first one is free: naming one person for one decision is available on Monday, requires nobody's permission, and does more than adopting a template.

---

## How to recognize the failure

**In a codebase and its calendar:**

- **A retrospective producing actions nobody owns.** The list is real, the observations are often good, and the same items appear next month. This is the claim in its plainest form.
- **A standup where nobody is blocked.** Fifteen people report status, and the two who needed each other could have said so in a message. A meeting doing the one thing a meeting is bad at — proceeding regardless of whether anybody had a question.
- **A pointing session where nobody has read the tickets.** An estimate produced before steps one and two, by a room rather than by a person, which makes it a number about the room.
- **An estimate that came in exactly on time.** One of two things happened. Either it was generously padded and the surplus went somewhere invisible, or the work was not read and it will come back as bug-fixing and gap-filling at some multiple of the original.
- **A recurring meeting whose reason nobody can state**, other than that it has always been there. The test is not whether it is useful — it is whether anybody can name what it is for, or admit that it answers something other than the work.
- **A design document describing only the happy path, or advice about a bug from somebody who has not reproduced it.** Both are the ownership mechanism running without the thing that justifies it. An owner is expected to hold the most context on the subject; whoever wrote from the happy path never ran the system under load or under an awkward customer, and whoever advises on an unseen bug is spending authority they have not earned.
- **A rule that has been explained more than twice.** Step five's judgement was made wrongly — the Idiom is not being derived, and stating it again will not change that. Move it somewhere that cannot be ignored, or accept the cost and keep stating it.

**In a conversation:**

- **"The team will decide X."** Nobody will. Ask which person, and watch whether the question is treated as pedantic.
- **"We're an agile team, we don't do big design up front."** Sometimes an accurate reading of how fast the goal moves. Sometimes a reason not to write down the invariants of a system where getting them wrong is expensive. The two sound identical and step one is where they separate.
- **"How long will this take?"** asked before anything has been read. There is no answer at that point that is not a guess wearing a number.
- **"Let's take it offline."** Often the right instinct — the room is not where it gets decided — and worth completing: offline with whom, by when.

The question that does the work: **whose name is against this step?**

If the answer is a team, a committee, or a role that three people could claim, the step is not going to happen, and no amount of process around it will change that. If the answer is a person, most of the process can go.

---

[← Ch. 22](22_never-written-down_at4r.md)  ·  [Contents](00_toc.md)
