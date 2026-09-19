# Assigned to the Team, Owned by Nobody

## The claim

**Programming with the five kinds depends on individual ownership of four artifacts, each belonging to the person who holds the most context on its subject.**

---

## What the artifacts are for

**The end goal of programming with the five kinds is not "working software."** It is software that is still right after the Forces move, and [chapter 03](03_forces_f4m5.md) is explicit that they move without warning: a team doubles, a service acquires a client outside the company, a table crosses a hundred million rows.

**The artifacts are not meeting notes, slide decks, or chaos labelled documentation.** The code is one of them: it *applies* the decisions that answer the Forces and it *enforces* the business rules. Those two verbs are the limit of what it does. Code that reflects a decision perfectly still says nothing about which Forces were present, what the alternatives were, or why this one was chosen — so the records of the rules and the decisions are separate artifacts, separately created and separately maintained. [Chapter 21](21_never-written-down_at4r.md) owns what happens when they do not exist.

**Ownership is where people enter.** Standups, retrospectives, planning sessions, review policies — every one of them carries a tension looking for a resolution, and the tension is always the same question: *which artifacts do we need, and who makes each one?* For many teams, that question is never asked and answered clearly, and the meetings turn into a ceremony.

## The four artifacts

Four artifacts lie between a request and software that runs. The claim here is not that these are the only ones or the most important ones — they are what following this book's advice lands you on.

```text
1  the rules          what must always be true
2  the force reading  what presses on it, and what follows
3  the solution       what we are actually going to build
4  the code           what applies and enforces the rest
```

Each is described below by what it looks like, who should own it, and what that owner has to be able to do. **Owners are given by capability and never by title.** A title says what somebody is called in one company; the capability says whether the artifact will exist, and it is the same question in a startup of four and a bank of forty thousand.

**A fifth record runs alongside all four, and it is not on the list because it is not the same shape.** [Chapter 21](21_never-written-down_at4r.md) works it in full: a log of the decisions taken while the four are being produced, each entry saying what was forced, what was chosen, and what would reopen it. The four exist so that the software is right. The log exists so that any of them can be revisited when the Forces move, which is the end goal this chapter opened on.

**Ownership is where the difference shows.** Each of the four is owned whole — one person gathers the rules for a story, one reads the Forces, one decides what gets built. A log is closer to a table than to a document: nobody owns the whole of it, and every entry belongs to whoever wrote it. The claim holds there too, one level down, because the person with the most context on a decision is the person who took it.

## 1. The rules and invariants

The first artifact, because everything after it is conditioned on it. What must always be true of this system — an invoice reconciles, a booking cannot double-sell a seat, a payment is applied once.

**Form.** A statement of the invariants, at whatever length they take: a hundred pages, or one paragraph. **The length should reflect the rules that actually apply, not the prose style of whoever wrote it or the current mood of the team.** *We are an agile team* is not a reason to begin a medical scanner with a vague idea of what it does.

**Ideal owner.** Whoever holds the most context on the business itself — how it makes money, what it is obliged to do, what it has promised customers. That is rarely the person who holds the most context on the software, and this is the one artifact where the two usually come apart.

**What that owner must be able to do.** Get a decision out of the business and refuse a vague answer. Not translate a vague answer into a precise-sounding one — obtain a real one, which sometimes means going back three times.

## 2. The force reading

[Chapter 03](03_forces_f4m5.md) owns the Forces themselves and [chapter 21](21_never-written-down_at4r.md) owns what a written entry has to hold. What is added here is that it is an artifact somebody owns, and that its size varies more than anything else in the list.

**Form.** The Forces bearing on the work in front of you, given as values rather than as verdicts — *two writers, same row, twice a second*, not *concurrency is important* — and the Principles that follow, each with the Force that licenses it. Same rule as before: **the length should reflect the Forces that actually apply, not the prose style of whoever wrote it or the current mood of the team.**

Often that is a paragraph. Sometimes there is no separate document at all, because the feature is small and the whole thing fits in the ticket — and sometimes one person owns the rules and the reading together, which is fine as long as both were considered and both were recorded where they mattered.

The size of the artifact is not the point. Whether the reading happened is the point, and the difference shows up immediately:

```text
A ticket goes to a junior developer: "let users export
their invoices." Two weeks later it works, and then the
servers run out of memory and clients report that the
exports are crashing their integrations.

The same ticket, after ten minutes from somebody who can
read the Forces, carries one added paragraph: exports run
to fifty thousand rows, so stream it; the caller retries on
timeout, so make it idempotent; users feed these into their
own finance systems, so the invoice id is not optional.

Same developer, same two weeks, different software.
```

Nothing in that second version is a design. It is a set of constraints, and handing them over is a ten-minute act by somebody who already knew them.

**Ideal owner.** Whoever holds the most context on the system as it actually runs — what it costs, where it breaks, what the last incident was about.

**What that owner must be able to do.** Price the options. That is where the expertise goes, and a reading produced by somebody who cannot say what a mechanism costs is a confident document with the wrong values in it.

## 3. The solution

This one is missing from the rest of the book. A reading of the Forces is **not a design**: it is a record of what was forced and what was chosen ([Ch. 21](21_never-written-down_at4r.md)), which is constraints rather than an answer.

So there is a gap between the force reading and the code, and it is where most of the actual thinking happens. The rules say what must be true. The reading says what presses on it. Neither of them says *what we are going to build* — a grid on this screen, a reminder sent by text the day before, a nightly job that reconciles and a queue for the failures.

**Form.** A description of what gets built, short enough to read in one sitting, in whatever register the reader needs — a paragraph, a sketch, a screen. It is the first artifact a non-engineer can check, and that is most of its value.

This is where the word *architecture* is usually pointing, and it is worth being exact about what it covers. It is not the diagram and it is not the choice of stack; both are consequences, and either can be produced without anybody having decided anything. What people mean by architecture is the first three artifacts together — the rules it has to hold to, the Forces bearing on it, and the thing you are going to build. This is the third of them, and what makes it architecture rather than a sketch is that the other two exist and one person is answerable for what was chosen from them.

**Ideal owner.** Whoever holds the most context on both sides — enough of the business to know what would satisfy it, enough of the system to know what it will cost. This is the artifact with the smallest pool of possible owners, and it is the one most often assigned to a room.

**What that owner must be able to do.** Choose. The rules constrain, the Forces constrain, and something still has to be picked from what is left, which no amount of further reading does for you.

**When the rules and the reading exist and there is still an argument, it is about the solution — and that is the argument worth having, because it is the only one of the three with genuine alternatives in it.**

## 4. The code

This is the artifact owned individually almost everywhere: every ticket has a developer's name on it, and every commit is signed. Pair programming exists, mostly as a way for a less experienced developer to learn by watching, and nobody builds a serious system with two people at one monitor for a year.

Code is also the one artifact that cannot exist without an owner — somebody's hands are on the keyboard — so nobody has to argue for assigning it. The three above it can all be handed to a group instead, and the asymmetry rests on two facts about code:

- it is the last artifact in the sequence
- it gives the fastest feedback

**Being last means the others can be skipped.** A great deal of software is built without reading the Forces and without deciding on a solution, by going straight to the code, and it produces something. It runs, it can be shown to a client, it can be sold. The sequence binds anyone following this book's advice; it does not stop anyone starting at the end of it.

That is the first mechanism, and it explains the missing owners directly: an artifact nobody knows has to exist, or nobody believes is important, is not one anybody assigns.

**Fast feedback is what keeps the mistake from being corrected.** Leave something out of the code, or get it obviously wrong, and you find out tomorrow — a page breaks, the same item sells twice, a query that returned in milliseconds takes a minute. The artifact proves its own importance, quickly and in public. Get an invariant wrong, or read a Force incorrectly, and the failure arrives months or years later, by which point almost nobody traces it back to the reading.

A sales module shows how far that gap can run. The rules are settled in a meeting: every proposal belongs to a salesperson, and that person earns a commission on the revenue it generates. The implementation is immediate — a commission rate on the user, a user id on the proposal.

It ships in January and runs for a year without a serious complaint. The following January, sales directors update their people's rates, expecting the system to apply them from then on. The tickets arrive within the week: every historical commission is now wrong, because a rate was never stored against a period. Putting it right takes new tables, new code, and a manual repair of past amounts reconstructed from database backups.

The retrospective produces two actions — *be careful with sales calculations*, and *QA will add automated commission tests*. Nobody in that room was at the meeting a year earlier, and nobody can say who gathered the rules. Four words in the first artifact would have prevented all of it: **rates are set yearly**.

---

## Why the claim holds

The four artifacts say what has to exist. They do not say who makes any of it exist, and that is the gap, because every one of them is work somebody has to decide to do instead of something else.

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

**It does not say whose judgement settles it.** An owner is expected to hold the most context on the subject; an interchangeable team member is not. So the owner's answer stands unless somebody produces a better reason.

That second mechanism is the key to why ownership works: *because* it tracks context. Give the artifact to somebody without the context and you have the name without the authority, which is a signature rather than an owner.

---

## Where the claim doesn't apply

### An artifact that needs two names

[Chapter 10](10_organization_rjf9.md) has Conway's mechanism in his own vocabulary: an interface exists where two design groups **negotiated and agreed upon** one. An interface binding two teams cannot have a single owner, because a single owner is one team imposing on the other, and what comes back is not agreement but compliance followed by a workaround.

So it has two names against it and the work is the negotiation between them. What does not change is that both names are individuals. *The platform team and the payments team will agree an interface* fails exactly as the dialogue above fails; two developers, one from each side, each able to commit their own, does not.

### Where the context and the authority sit in different people

The person who holds the most context on a system is sometimes not the person permitted to decide about it. A developer two years into a codebase knows what the last three incidents were really about; the decision is taken by somebody who has been in the company longer and has been in the code never. Give the artifact to the context and it will not be honoured; give it to the authority and it will be wrong.

There is no version of this chapter that resolves that, because it is not a fact about software. What the claim buys is only that the split becomes visible and nameable: *the person who should own this cannot, and the person who can should not.* That sentence is answerable by somebody with the power to fix it, where *the design keeps coming out wrong* is not.

**And seniority is not the instrument.** A senior engineer is not necessarily somebody who has been at the company ten years, and length of service is the proxy most organisations reach for precisely because it is the one that is written down. The reading that matters is who has the most context on *this*, which changes per artifact and sometimes points at the newest person in the room.

---

## What the claim costs

**Where the derivation already happens, the artifacts are ceremony.** Take a small team who have shipped several systems together, who reach for the version column and the idempotency key without the reasoning being spoken aloud, and whose record over some years is that the surprises did not arrive. Ask them for a written map per feature and most of it answers nothing — they are doing the work, they are simply not writing it down, and this claim is about ownership rather than about writing.

Two conditions keep that from being the exception everybody claims. **It holds only while the team is stable**, because the context lives in the people and [chapter 21](21_never-written-down_at4r.md) is the chapter about what that costs when they leave. And **the instrument is the record, not the self-assessment**: many teams believe they are that team, and what distinguishes the ones that are is answerable — what did you ship, and what happened to it six months later.

**Ownership by context concentrates, and that is division of labour rather than a defect.** If each artifact goes to whoever holds the most context, and context accumulates where it is used, the same few people end up owning the same few subjects. That is what an expert is. A team where everybody owns everything equally has no expert in anything, and the instinct to arrange one — out of a fear of depending on individuals — buys evenness at the price of there being nobody who knows.

What the concentration does cost is real: one person leaves and a subject leaves with them. The standard remedy is a handoff. *Ana is leaving in a fortnight; hand the booking module over to Joe.* That remedy assumes context is a thing which can be passed across a table, and it is not. What Ana has is four years of having been wrong about that module and finding out why. What transfers in a fortnight is the file layout and the names of the tables.

So there are two honest responses and the handoff is neither. Grow a second person into the same subject, which is slow, is mostly done by giving them artifacts to own while the first person is still there, and has to start long before anybody resigns. Or accept the concentration and price it. The fortnight handoff is quick, produces a document nobody opens, and its main output is the belief that the problem has been dealt with.

**It demands the seniority it looks like it replaces.** Deciding who holds the most context is itself a judgement requiring context, and it is made by the person assigning the work — which is why an organisation that gets this wrong stays wrong, and why the correction almost never comes from inside the team.

---

## How to recognize the failure

**In a codebase and its calendar:**

- **A retrospective producing actions nobody owns.** The list is real, the observations are often good, and the same items appear next month. The claim in its plainest form.
- **A design that keeps coming out wrong**, where every individual decision in it was defensible. Usually the third artifact was assigned to a room, so what shipped is the intersection of what nobody objected to.
- **A design document describing only the happy path, or advice about a bug from somebody who has not reproduced it.** Both are ownership without the context that justifies it. Whoever wrote from the happy path never ran the system under load or under an awkward customer, and whoever advises on an unseen bug is spending authority they have not earned.
- **Business rules that live only in the code.** Nobody owned the first artifact, so the invariants exist as an emergent property of whatever the code currently does, and the only way to answer *is this correct* is to ask the code what it does and agree with it, until an important user says that behaviour is wrong.

**In a conversation:**

- **"The team will decide X."** Nobody will. Ask which person, and watch whether the question is treated as pedantic.
- **"We're an agile team, we don't do big design up front."** Sometimes an accurate reading of how fast the goal moves. Sometimes a reason not to write down the invariants of a system where getting them wrong is expensive. The two sound identical, and the first artifact is where they separate.
- **"Let's take it offline."** Often the right instinct — the room is not where it gets decided — and worth completing: offline with whom, by when.
- **"Ask Priya, she knows this system."** Said by whoever owns the current design, in answer to a question about it — an accurate description of the split between the owner and the context.

The question that does the work: **whose name is against this, and do they have the most context on it?**

Two answers fail, and they fail differently. If the name is a team, the artifact will not exist. If the name is a person chosen for their position rather than their context, it will exist and be wrong.

---

[← Ch. 21](21_never-written-down_at4r.md)  ·  [Contents](00_toc.md)
