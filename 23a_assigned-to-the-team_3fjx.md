# Assigned to the Team, Owned by Nobody

## The claim

**Programming with the five kinds depends on individual ownership: every artifact has one name against it, and that name belongs to whoever holds the most context on it.**

Every chapter so far has worked on a claim somebody made about software. This one works on the arrangement that produces the software, and it is the only chapter whose subject is people. It is here because the arrangement is derivable — not from a methodology, and not from what worked somewhere else, but from what has to exist before the software can be right.

---

## The demonstration

### The chain, from the end

Start from the end goal and ask what each level needs in order to exist.

```text
end goal     software that is right for its context, and
             survives its Forces moving
               ^
               |  depends on
               |
artifacts    code matching the Forces, and records of the
             rules, the Forces, and the decisions
               ^
               |  depends on
               |
ownership    individuals who create and maintain the artifacts
```

Read downward it is unremarkable. Read upward it is the argument, because each level is load-bearing for the one above it.

**The end goal is not "working software."** It is software that is still right after the Forces move, and [chapter 02](02_forces_f4m5.md) is explicit that they move without warning: a team doubles, a service acquires a client outside the company, a table crosses a hundred million rows.

**The artifacts are not meeting notes, slide decks, or chaos labelled documentation.** The code is one of them: it *applies* the decisions that answer the Forces and it *enforces* the business rules. Those two verbs are the limit of what it does. Code that reflects a decision perfectly still says nothing about which Forces were present, what the alternatives were, or why this one was chosen — so the records of the rules and the decisions are separate artifacts, separately created and separately maintained. [Chapter 22](22_never-written-down_at4r.md) owns what happens when they do not exist.

**Ownership is where people enter.** Standups, retrospectives, planning sessions, review policies — every one of them carries a tension looking for a resolution, and the tension is always the same question: *which artifacts do we need, and who makes each one?* Where that has been asked and answered, most of the meetings have nothing left to do. Where it has not, they are what the team does instead of answering it.

### The artifacts that come before code

Code is the obvious artifact and the easiest to own correctly. Nobody argues that code is unnecessary, and nobody says *the team will write this at next week's coding meeting*. Assigning a ticket to one person is second nature.

The trouble starts with everything upstream of it. There the same question produces *we don't need a list of the business rules, we're agile*, and *the team will decide on the design of feature X*.

Four artifacts sit between a request and the code. The claim here is not that these are the only ones or the most important ones — they are what following this book's advice lands you on, and two of the four are [chapter 18](18_force-map-method_r37x.md)'s method under a different description.

```text
1  the rules      what must always be true
2  the force map  what presses on it, and what follows
3  the solution   what we are actually going to build
4  the code       what applies and enforces the rest
```

Each is described below by what it looks like, who should own it, and what that owner has to be able to do. **Owners are given by capability and never by title.** A title says what somebody is called in one company; the capability says whether the artifact will exist, and it is the same question in a startup of four and a bank of forty thousand.

### 1. The rules and invariants

The root, because everything after it is conditioned on it. What must always be true of this system — an invoice reconciles, a booking cannot double-sell a seat, a payment is applied once.

**Form.** A statement of the invariants, at whatever length they take: a hundred pages, or one paragraph. **The length should reflect the rules that actually apply, not the prose style of whoever wrote it or the current mood of the team.** *We are an agile team* is not a reason to begin a medical scanner with a vague idea of what it does.

**Ideal owner.** Whoever holds the most context on the business itself — how it makes money, what it is obliged to do, what it has promised customers. That is rarely the person who holds the most context on the software, and this is the one artifact where the two usually come apart.

**What that owner must be able to do.** Get a decision out of the business and refuse a vague answer. Not translate a vague answer into a precise-sounding one — obtain a real one, which sometimes means going back three times.

**When the rules are not written, write them before anything else. When somebody says they cannot be written, that is the finding, and it is about the business rather than about the software.**

There is a myth that makes this artifact look optional, and it is the reason it gets skipped. It is called *changing requirements*, which says the business rules move. They rarely do. A company's invariants are facts about how it makes money, and facts of that kind hold for years. What moves is which of them you were asked to serve this quarter — and rules that were never gathered properly surface months later as *the requirements changed*, when nothing changed except who finally read them. Both arrive at the team as churn, and only one of them is anybody's mind being altered.

### 2. The force map

[Chapter 18](18_force-map-method_r37x.md) owns the method and [chapter 02](02_forces_f4m5.md) owns the Forces themselves. What is added here is that its output is an artifact somebody owns, and that its size varies more than anything else in the list.

**Form.** The Forces that bear on this, at values rather than as verdicts — *two writers, same row, twice a second*, not *concurrency is important* — and the Principles that follow, each with the Force that licenses it. Same rule as before: **the length should reflect the Forces that actually apply, not the prose style of whoever wrote it or the current mood of the team.**

Often that is a paragraph. Sometimes there is no separate document at all, because the feature is small and the whole thing fits in the ticket — and sometimes one person owns the rules and the map together, which is fine as long as both were considered and both were recorded where they mattered.

The size of the artifact is not the point. Whether the reading happened is the point, and the difference shows up immediately:

```text
A ticket goes to a junior developer: "let users export
their invoices."  Two weeks later it works, and it holds
the whole result set in memory, has no idempotency on the
retry, and writes a file the finance team cannot reconcile.

The same ticket, after ten minutes from somebody who can
read the Forces, carries one added paragraph: exports run
to fifty thousand rows so stream it; the caller retries on
timeout so make it idempotent; finance reconciles on
invoice id so that column is not optional.

Same developer, same two weeks, different software.
```

Nothing in that second version is a design. It is a set of constraints, and handing them over is a ten-minute act by somebody who already knew them.

**Ideal owner.** Whoever holds the most context on the system as it actually runs — what it costs, where it breaks, what the last incident was about.

**What that owner must be able to do.** Price the options. [Chapter 18](18_force-map-method_r37x.md) is blunt that this is where the expertise goes, and a reading produced by somebody who cannot say what a mechanism costs is a confident document with the wrong values in it.

**When the reading is instinctive, do it and move on. When two people read the same Force differently, stop — the disagreement is about a fact, and somebody can go and check it.**

### 3. The solution

This one is missing from the rest of the book, and [chapter 18](18_force-map-method_r37x.md) says so itself: **the output of a force map is not a design.** It is a record of what was forced and what was chosen. Constraints, not an answer.

So there is a gap between the second artifact and the fourth, and it is where most of the actual thinking happens. The rules say what must be true. The map says what presses on it. Neither of them says *what we are going to build* — a grid on this screen, a reminder sent by text the day before, a nightly job that reconciles and a queue for the failures.

**Form.** A description of the thing, short enough to read in one sitting, in whatever register the reader needs — a paragraph, a sketch, a screen, a sequence. It is the first artifact a non-engineer can check, and that is most of its value.

**Ideal owner.** Whoever holds the most context on both sides — enough of the business to know what would satisfy it, enough of the system to know what it will cost. This is the artifact with the smallest pool of possible owners, and it is the one most often assigned to a room.

**What that owner must be able to do.** Choose. The rules constrain, the Forces constrain, and something still has to be picked from what is left, which no amount of further reading does for you.

**When the rules and the map exist and there is still an argument, it is about the solution — and that is the argument worth having, because it is the only one of the three with genuine alternatives in it.**

### 4. The code

The artifact everybody already owns properly, and it is worth asking why.

Code has an owner because it cannot exist without one. Somebody's hands are on the keyboard; the ticket has a name on it; the commit is signed. Nothing about code is more deserving of an owner than the three artifacts above it — it is simply the one where a shared assignment is *visibly* impossible, so nobody tries.

The other three can be nominally assigned to a group, because the absence of the artifact is not visible until much later. That is the whole asymmetry, and it is why the failure this chapter is about happens upstream of the code and shows up in it.

---

## Why the claim holds

The chain says what has to exist. It does not say who makes it exist, and that is where it fails, because every artifact above is work somebody has to decide to do instead of something else.

### An artifact with no name against it is made by nobody

**"Individual owner" is the load-bearing phrase, and it is not a committee and not "the team."** Follow one engineer's reasoning after a shared assignment:

```text
"The team is responsible for designing feature X."

  How much time should I put into this? Not an afternoon —
  I have a high-priority ticket.
  I know feature X well and could design it properly.
  But others will object for reasons that are not good ones,
  and it will be rejected anyway. Why spend the afternoon?
```

Nothing in that is unreasonable, and none of it is fixed by asking harder or by asking again next sprint. What fails is not effort. It is that a shared assignment supplies neither of the two things the work needs.

**It does not say the task is worth time.** An owner has a defensible answer to *why were you doing that instead of the ticket*. Without one, the artifact loses every collision with something scheduled, and it collides with something scheduled every day.

**It does not say whose judgement settles it.** An owner is expected to hold the most context on the subject; an interchangeable team member is not. So the owner's answer stands unless somebody produces a better reason — a different position from having a view that has to survive a room.

That second mechanism is why the claim's two halves are one claim rather than two. Ownership works *because* it tracks context. Give the artifact to somebody without the context and you have the name without the authority, which is a signature rather than an owner.

This is [chapter 08](08_change_rjf9.md)'s mechanism at a smaller scale. Conway's interfaces exist where two design groups had to negotiate one — so where no group owns a piece, there is nobody to negotiate with, and the interface is not badly drawn. It is undrawn, and the seam turns up later wherever the code happened to be cut.

### What follows about meetings

**A meeting is a decision assigned to a room.** By the claim, that is an artifact with no name against it, which is why the meeting called to decide something rarely decides it and why the same subject returns three weeks later. What a meeting does well is the opposite operation: getting one specific thing unblocked for somebody who already owns it, and then ending.

A meeting with no decision in it at all is a different object and can be perfectly sound — a team meets for fifteen minutes on Friday to stay in contact with each other, and that answers something this chapter does not model. What makes it defensible is that the reason given is the reason it exists. The same meeting held daily, called a standup and defended as coordination, is the failure.

**Stages, transitions, and who is called at two in the morning** are the same mechanism applied to the flow of work rather than to a single artifact. None of the automation matters — not the pipeline, not the checks — if nobody can say when development ends and testing begins, or who is paged and what they are permitted to do when they arrive.

---

## Where the claim doesn't apply

### An artifact that needs two names

The claim's first half fails where the artifact is a negotiation.

[Chapter 08](08_change_rjf9.md) has Conway's mechanism in his own vocabulary: an interface exists where two design groups **negotiated and agreed upon** one. An interface binding two teams cannot have a single owner, because a single owner is one team imposing on the other, and what comes back is not agreement but compliance followed by a workaround.

So it has two names against it and the work is the negotiation between them. What does not change is that both names are individuals. *The platform team and the payments team will agree an interface* fails exactly as the dialogue above fails; two people, one from each side, each able to commit their own, does not.

### Where the context and the authority sit in different people

The claim's second half fails more often, and more quietly.

The person who holds the most context on a system is frequently not the person permitted to decide about it. A developer two years into a codebase knows what the last three incidents were really about; the decision is taken by somebody who has been in the company longer and has been in the code never. Give the artifact to the context and it will not be honoured; give it to the authority and it will be wrong.

There is no version of this chapter that resolves that, because it is not a fact about software. What the claim buys is only that the split becomes visible and nameable: *the person who should own this cannot, and the person who can should not.* That sentence is answerable by somebody with the power to fix it, where *the design keeps coming out wrong* is not.

**And seniority is not the instrument.** A senior engineer is not necessarily somebody who has been at the company ten years, and length of service is the proxy most organisations reach for precisely because it is the one that is written down. The reading that matters is who has the most context on *this*, which changes per artifact and sometimes points at the newest person in the room.

---

## What the claim costs

**Where the derivation already happens, the artifacts are ceremony.** Take a small team who have shipped several systems together, who reach for the version column and the idempotency key without the reasoning being spoken aloud, and whose record over some years is that the surprises did not arrive. Ask them for a written map per feature and most of it answers nothing — they are doing the work, they are simply not writing it down, and this claim is about ownership rather than about writing.

Two conditions keep that from being the exception everybody claims. **It holds only while the team is stable**, because the context lives in the people and [chapter 22](22_never-written-down_at4r.md) is the chapter about what that costs when they leave. And **the instrument is the record, not the self-assessment**: many teams believe they are that team, and what distinguishes the ones that are is answerable — what did you ship, and what happened to it six months later.

**Ownership by context concentrates.** If each artifact goes to whoever holds the most context, and context accumulates, the same two people end up owning everything and the team has built a bottleneck out of a principle. The correction is not to spread ownership thinner; it is to notice that context is transferable and that handing an artifact to somebody who will hold the most context *next year* costs something now and repays it.

**It demands the seniority it looks like it replaces.** Deciding who holds the most context is itself a judgement requiring context, and it is made by the person assigning the work — which is why an organisation that gets this wrong stays wrong, and why the correction almost never comes from inside the team.

**And nobody occupies the whole of it.** No group runs four artifacts with a named owner for each, every time, at every scale. The reason to set it out anyway is that the parts are separable and the first is free: putting one name against one artifact is available on Monday, needs nobody's permission, and does more than adopting a template.

---

## How to recognize the failure

**In a codebase and its calendar:**

- **A retrospective producing actions nobody owns.** The list is real, the observations are often good, and the same items appear next month. The claim in its plainest form.
- **A design that keeps coming out wrong**, where every individual decision in it was defensible. Usually the third artifact was assigned to a room, so what shipped is the intersection of what nobody objected to.
- **A standup where nobody is blocked.** Fifteen people report status, and the two who needed each other could have said so in a message.
- **A pointing session where nobody has read the tickets.** An estimate produced by a room rather than a person, which makes it a number about the room.
- **A recurring meeting whose reason nobody can state**, other than that it has always been there. The test is not whether it is useful — it is whether anybody can name what it is for, or admit that it answers something other than the work.
- **A design document describing only the happy path, or advice about a bug from somebody who has not reproduced it.** Both are ownership without the context that justifies it. Whoever wrote from the happy path never ran the system under load or under an awkward customer, and whoever advises on an unseen bug is spending authority they have not earned.
- **Business rules that live only in the code.** Nobody owned the first artifact, so the invariants exist as an emergent property of whatever the code currently does, and the only way to answer *is this correct* is to ask the code what it does and agree with it.

**In a conversation:**

- **"The team will decide X."** Nobody will. Ask which person, and watch whether the question is treated as pedantic.
- **"We're an agile team, we don't do big design up front."** Sometimes an accurate reading of how fast the goal moves. Sometimes a reason not to write down the invariants of a system where getting them wrong is expensive. The two sound identical, and the first artifact is where they separate.
- **"Let's take it offline."** Often the right instinct — the room is not where it gets decided — and worth completing: offline with whom, by when.
- **"Ask X, they know that system."** Said about somebody with no authority over it. That is the split named out loud by people who have noticed it and cannot fix it.

The question that does the work: **whose name is against this, and do they have the most context on it?**

Two answers fail, and they fail differently. If the name is a team, the artifact will not exist. If the name is a person chosen for their position rather than their context, it will exist and be wrong — which is worse, because it looks like the thing you asked for.

---

[← Ch. 22](22_never-written-down_at4r.md)  ·  [Contents](00_toc.md)
