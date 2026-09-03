# Change: Evolution, Organization, Compatibility

## The claim

**Everything you build changes, but not at the same rate — and the slow parts set the terms for the fast ones.**

Code changes daily. The database schema changes monthly, and each change is a migration. A published interface changes rarely and never backwards, because other people's software depends on it. The shape of your organization changes yearly, expensively, and reproduces itself in the software regardless.

The practical skill is knowing **which of those layers a decision lands in**, because that decides how long you will live with it.

## When this binds

Unlike most of this book, this chapter has almost no boundary at the fast end — every system changes. What varies is whether the *slow* layers exist for you at all.

You are fully in this chapter's territory when three things are true: the system stores data that outlives a deploy, other people's code calls yours, and more than a handful of people work on it. Miss all three — a script you wrote this morning, run once, by you — and none of this applies.

Most systems have one or two of the three. A team with a database but no external callers has the evolution problems and none of the compatibility ones. A solo developer publishing a library has the compatibility problem and no organizational one.

---

## The demonstration

### Software that is used must change

The first of **Lehman's laws of software evolution**, from Meir Lehman and László Belady's study of large systems in the 1970s: a system that is used must be continually adapted, or it becomes progressively less satisfactory.

The mechanism is not that code rots. Code that nobody touches does exactly what it did last year. What changes is everything around it — tax rules, currencies, browser versions, the API you call, what users expect, what your competitors ship. **A system is judged against a moving world, so standing still is a slow decline** measured against that movement rather than against the code.

The second law is the one with teeth: as a system evolves, its complexity increases, unless deliberate work is done to reduce it.

That is a ratchet, and it works because of an asymmetry in what changes cost. Adding a case to a system is cheap and local — one `if`, one column, one flag. Removing one is expensive and diffuse: you have to establish that nobody depends on it, which means finding every caller, every saved row, every customer whose workflow quietly relies on it. So additions happen continuously and removals need a project, and the ratio between those two costs is what makes the direction one-way.

**On how much weight these carry.** Lehman's laws are empirical, and the study population was mainframe systems, decades ago, with release cycles measured in years. There are eight of them, and they are not equally solid — the two above are widely recognizable, and several of the others ("conservation of familiarity," "conservation of organizational stability") are vague enough that they resist being checked at all.

### Once published, it is forever

This is the sharpest constraint in the chapter, and the one that is most often discovered late.

Here is a client written against version 1 of an API. It is installed on machines you do not control and will not be recompiled:

```go
type OldClient struct {
	ID     string `json:"id"`
	Amount int64  `json:"amount_minor"`
	Status string `json:"status"`
}
```

The strings in backticks are **struct tags** — Go's way of saying which JSON key fills which field, the same job as `@JsonProperty` in Java or `[JsonPropertyName]` in C#. This client will look for a key called `amount_minor` and put it in `Amount`. It will ignore any key it has no field for.

Now change the server four ways. The server sends the new shape in every case; what follows is **what the old client makes of it**:

```text
v1, what the old client was built for:
  parsed: id="ord-1" amount=4200 status="paid"  err=<nil>

ADD an optional field:
  parsed: id="ord-1" amount=4200 status="paid"  err=<nil>

RENAME a field (amount_minor -> total_minor):
  parsed: id="ord-1" amount=0 status="paid"  err=<nil>

CHANGE a type (int -> string, for big numbers):
  parsed: id="ord-1" amount=0 status="paid"  err=json: cannot unmarshal string ...

ADD a new enum value the old client never heard of:
  parsed: id="ord-1" amount=4200 status="partially_refunded"  err=<nil>
```

Adding a field is safe: the old client ignores what it does not recognize.

The type change is a **loud** failure. An error comes back, someone gets paged, and it is fixed within the hour.

The rename is the dangerous one. **No error, and the amount is now zero.** A payment of nothing, reported as a successful parse, on a machine you cannot reach. The field did not disappear from the client's point of view — it was never there, so its absence looks exactly like a legitimately absent value.

The enum case is subtler still. The parse succeeds and the client holds a status it has no code path for, so what happens next depends on whether its author wrote a default branch three years ago.

**The general rule this produces:** you may add optional things and you may relax constraints. You may not remove, rename, retype, or tighten. Nothing about that is specific to JSON — it is the same in protocol buffers, in database views other teams query, in library function signatures, in the shape of a message on a queue.

Go's standard library is a large, dated demonstration of living with it. `io/ioutil` was deprecated in Go 1.16, released February 2021. It is still present in Go 1.26.5:

```go
// Deprecated: As of Go 1.16, the same functionality is now provided
// by package [io] or package [os] ...
package ioutil
```

```text
go 1.26.5: ioutil compiled and ran, returned "still here"
```

Five years after being declared obsolete, it compiles and works, because Go promised that code written for Go 1 keeps building. Across the standard library there are **175 declarations marked deprecated** — each one something its maintainers would remove and cannot.

That is what the commitment costs when it is kept.

Those 175 were bought rather than incurred. Rob Pike lists locking the language down at 1.0 among the things the Go project got right, and names two returns for the cost. The first is uptake: he calls the effect on Go's adoption dramatic and documented, and says he finds it puzzling that most other projects have resisted doing the same. The second is that it "blocks feature-itis".

**Feature-itis** is a language steadily accumulating features, each one defensible on its own and the total more than anyone wants to learn. The promise blocks it using the same irreversibility this section has been describing as a burden. Under a compatibility guarantee, anything added is added permanently: a feature that turns out to be a mistake cannot be withdrawn, and instead joins the list of things that must keep working. So a proposal has to be worth not merely having but keeping, for as long as the language exists, and most proposals are not.

This does not contradict the argument above, because it is the same rule. *Once published, it is forever* holds exactly as stated, and Pike is not arguing with it — he is reporting what happens when you accept it early. The difference is timing. A team that discovers the rule after it has users has no choice left to make. Go's team took it at 1.0, while declining was still available, wanting the effect that permanence has on what gets added in the first place. The 175 deprecations are what the promise cost them; a language that stayed small is what they were buying.

[Chapter 04](04_dependency-and-hiding_agjy.md) covers the other half of this problem: users depend on behaviour you never documented, so the surface you are committed to is larger than the one you published.

### The organization ends up in the software

**Conway's Law**, from Melvin Conway in 1968. In his words:

> Organizations which design systems […] are constrained to produce designs which are copies of the communication structures of these organizations.

It is a description, not advice — [chapter 03](03_grading-a-law_q5c6.md) uses exactly this distinction, since a law describes what happens while a Principle tells you to do something. Conway's Law tells nobody to do anything.

**"Communication structure" is easy to misread**, so it is worth taking from the same paper what Conway meant by it. He is not talking about how easily people can reach each other. He is talking about which groups have to agree with which:

> If there is a branch, then the two […] design groups X and Y which designed the two nodes must have **negotiated and agreed upon an interface specification** […] If, on the other hand, there is no branch between x and y, then the subsystems do not communicate with each other, there was nothing for the two corresponding design groups to negotiate.

*Negotiated and agreed upon.* An interface exists between two parts of the system exactly where two groups had to settle something between them. So the structure that gets copied is **who owns what and therefore who must agree with whom** — which is why messaging tools do not change the outcome. They lower the cost of talking; the constraint was never talking, it was agreement.

He states the relationship more precisely than "copy" suggests. Both the system and the organization are graphs — for the system, "each node is a subsystem which communicates with other subsystems along the branches"; for the organization, the nodes are design groups and the branches are the pairs who had to negotiate something. His claim is that there is

> a homomorphism from the linear graph of a system to the linear graph of its design organization.

A homomorphism is a map that preserves structure: every subsystem corresponds to a group, every interface to a negotiation. It also runs in one direction only, which turns out to matter.

His own example is the one worth carrying. A research organization put five people on a COBOL compiler and three on an ALGOL compiler, and got **a five-phase COBOL compiler and a three-phase ALGOL compiler.** Nobody chose the number of phases. It was chosen when the people were assigned.

And the consequence that matters most here:

> Given any design team organization, there is a class of design alternatives which cannot be effectively pursued by such an organization because the necessary communication paths do not exist.

Some designs are not available to you, given who owns what.

Work has to be divided before it can start. Someone decides that this team takes billing and that team takes fulfilment, or that these three engineers own the importer. **That division is already a decomposition of the system** — you cannot hand out the work without partitioning the design — and it is usually settled before anyone has read the problem closely, by whoever was arranging the work.

What makes the partition stick is an asymmetry in who can change what.

- A boundary **inside** your own area is yours to move. Notice it is wrong on Tuesday, change it on Wednesday, and nobody else is involved.
- A boundary **between** areas is a negotiation. Moving it means persuading another team to reopen something they consider settled, reschedule work they have committed to, and accept a change with no benefit to them this quarter.

So internal boundaries stay fluid and shared ones calcify — not because anyone is tempted into bad design, but because one kind of correction is free and the other needs a meeting, a quarter, and somebody's agreement.

This is why good engineers do not escape it. Two excellent engineers who own the two halves of a badly split problem will each build their half well. Neither is in a position to notice that the split itself was wrong, and if one does notice, fixing it is not an engineering decision they are allowed to make.

**Neither shape is better in itself**, and this is where the law is most often misread. Tight coupling between two things that genuinely are one thing is right — splitting them adds ceremony to something indivisible. A firm interface between things that genuinely are separate is also right. The law does not say that distance improves design.

What it says is that **your software gets its seams where the work was divided**, whether or not the problem has seams there. The failure it predicts is a *mismatch*: when the shape of the problem and the shape of the ownership disagree, ownership wins.

Both directions of mismatch are common.

- **One owner, two natural parts.** A team that owns what should be two separable things builds them as one. Nothing is broken and every test passes, so nobody notices — until the day the two need to ship on different schedules, or scale differently, or one has to be replaced, and it turns out they share state, types, and a deployment.
- **Two owners, one natural unit.** Two teams owning halves of something indivisible put a network call, a queue, or a versioned interface through the middle of it. Every change that should be one commit becomes two releases and a coordination meeting.

*(The quotations are from Conway's 1968 paper, "How Do Committees Invent?" The negotiation mechanism is his. What this book adds is the asymmetry that makes a partition stick — free to change inside an owner, expensive across — and the reading of "communication structure" as ownership, which is how his design-group argument lands in an organization that has teams rather than committees.)*

### One team per service, and where that heuristic breaks

Conway's Law is the reason behind the common advice that each service should have exactly one owning team, and the reasoning is sound as far as it goes: a deployment boundary that crosses a team boundary needs coordination on every release, which is the cost the boundary was supposed to remove.

But the advice is regularly applied in the wrong direction. It is a constraint on **who may own a service**, not a recipe for **how many services to have**.

Conway's homomorphism says why, if you follow the direction it runs. A map from the system to the organization assigns every subsystem exactly one design group — so several subsystems may share a group, and no subsystem may have two. *(Conway states the homomorphism; drawing this consequence out of its direction is this book's.)*

- **Many services owned by one team** is fine. It costs that team some operational overhead and nothing in coordination, because every release is theirs to schedule.
- **One service owned by many teams** is the failure the heuristic exists to prevent. Every release needs agreement from people with different priorities, so releases get slower, get batched, and eventually get scheduled.
- **Services sized to the team chart** is the failure the heuristic causes. If there are six teams, six services appear, whether or not the problem has six parts — and the seams land where the reporting lines are.

The honest form: let the problem decide how many parts there are, then make sure no part is owned by more than one team. If that turns out to be impossible with the teams you have, that is real information about the organization, and it is what the inverse manoeuvre is for.

### Coordination grows faster than the team

**Brooks's Law**, from Fred Brooks in 1975: adding people to a late software project makes it later.

The arithmetic underneath it is the same one behind [chapter 08](08_scale_637f.md)'s reversal. Any two people on a team may need to coordinate, so the number of pairs is `n(n−1)/2`:

```text
 people   pairs   paths the new person adds
     2        1        1
     3        3        2
     5       10        7
     8       28       18
    12       66       38
    20      190      124
```

The twentieth person adds 19 new relationships. Put a cost on each — half an hour a week, which is modest for two people who must stay aligned — and see what it does to the working week:

```text
 team of  5:  4 paths each,  2.0 h/wk =  5% of the week
 team of  8:  7 paths each,  3.5 h/wk =  9%
 team of 12: 11 paths each,  5.5 h/wk = 14%
 team of 20: 19 paths each,  9.5 h/wk = 24%
```

At twenty people, a quarter of everyone's time goes on staying aligned, before anyone writes anything. Add the ramp-up cost — a new person needs time from experienced people to become useful, which subtracts from the team's output for weeks — and a late project can genuinely go slower.

Note what the law does *not* say. It is not "adding people never works," which would be absurd — every team that has ever grown is a counter-example. It says adding people to a **late** project makes it later, and the word doing the work is *late*.

### What "late" actually means, worked

Here is a scenario worth putting numbers to, because it separates two situations that look identical on a status report.

A project was estimated at 100 hours. Two people work on it, five productive hours each per day, so ten hours a day. After twelve days, 120 hours have been spent and it is not finished. Two managers look at the plan and disagree:

- **Manager A:** roughly 80 hours of work remain. The estimate was 100, the truth is about 200.
- **Manager B:** the original estimate was wrong by an order of magnitude. The real total is about 1,000 hours, so 988 remain.

Both are looking at the same project on the same day. Now add one person to each, assuming they take about three working weeks to become independently productive and consume roughly a quarter of an existing person's time while they get there:

```text
A:  80h remaining    2 people:  8 days    +1 person:  9 days   -> later
B: 988h remaining    2 people: 99 days    +1 person: 71 days   -> sooner
```

**Same team, same new hire, opposite answers.** Under A the project ends before the new person becomes useful, so all you bought was the mentoring cost. Under B there are months of runway, so the onboarding is repaid many times over — and the honest reading is that the project was under-staffed from the start and should have grown sooner.

Sweeping the remaining work shows where it turns:

```text
 remaining  60h ->   6 vs  7 days   later
 remaining 100h ->  10 vs 11 days   later
 remaining 150h ->  15 vs 16 days   later
 remaining 200h ->  20 vs 19 days   sooner
 remaining 400h ->  40 vs 32 days   sooner
```

The break-even sits at roughly the length of the ramp-up itself. Which gives the sharper statement of the law:

> **"Late" means the remaining work is shorter than the time it takes a new person to become useful.**

That is a different question from *are we behind schedule*, and the two come apart exactly in case B. A project that is badly behind a wrong estimate may not be late in Brooks's sense at all; it is under-staffed, and the fix is people — added now rather than in three months, since the ramp-up cost is the same whenever you pay it and the runway only shrinks.

*(The ramp-up figures above are illustrative rather than measured — three weeks to productivity and a quarter of a mentor's time. Substitute your own and the shape holds; the break-even moves with them, which is the point of computing it rather than quoting it.)*

The other half of Brooks stands regardless of arithmetic: some work does not divide. Brooks's own line is that the bearing of a child takes nine months no matter how many women are assigned, and a task with one indivisible critical path does not care how many people are waiting on it.

---

## Why the claim holds

The four results have one thing in common: **their feedback loops are longer than the decisions that cause them.**

You can test a function in seconds and a deployment in hours. You cannot test a schema decision, because the evidence arrives when the table has four years of rows in it. You cannot test a published interface, because the evidence arrives when other people's software depends on it. You cannot test an organizational structure, because the evidence arrives in the architecture a year later.

That length is the entire difficulty. Everywhere else in engineering, being wrong is cheap because you find out quickly and try again. Here you find out after the cost is sunk, which is why these are the decisions worth slowing down for — and it is [chapter 02](02_forces_f4m5.md)'s reversibility question, applied at the timescale where it bites hardest.

The compatibility rule follows from something narrower and worth stating separately: **you cannot deploy other people's software.** Every other constraint in this book can be fixed by changing code you control. This one cannot, because the code that has to change is on a machine you have no access to and belongs to someone who has no reason to hurry.

---

## Where the claim doesn't apply

### Code with a known death date

A migration script that runs once. A spike written to answer a question. A report generated for one meeting. An import job for a system being decommissioned in March.

None of the four applies, and the reason is worth being precise about: **each of these laws is a claim about accumulated time**, and there is not going to be any. Lehman's ratchet needs years of additions to ratchet. Compatibility needs a second party. Conway needs a second team.

The failure here is not ignoring the laws — it is applying them. Versioning the output of a one-off report, or designing a spike for extension, spends the effort that these laws exist to justify on the one case where the justification is absent.

The dangerous version is a script that was going to be deleted and was not. That is not a failure of judgement about the script; it is what happens when nobody records the death date. If the plan is that this disappears, write down when, and what should be true when it does.

### Internal interfaces you can change atomically

"Once published, forever" applies to what you cannot recompile. A function called only from inside one repository, deployed as one unit, is not published in this sense — rename it, fix the call sites, ship all of it together, and no compatibility problem exists.

This is why the same change is trivial in one codebase and a six-month deprecation in another, and the difference is not code quality. It is [chapter 02](02_forces_f4m5.md)'s control-of-callers Force, at its most consequential.

The mistake in both directions is common. Teams version internal APIs that only they call, paying deprecation costs for nothing. Other teams treat a genuinely published interface as internal, and break customers.

### Small teams, where Brooks and Conway go quiet

At three people the pair count is three, coordination is a conversation, and Conway's Law predicts a structure with no visible seams — which is correct, because there are none to have.

Neither law is false at that size; they have nothing to act on ([Ch. 01](01_the-five-kinds_cjx4.md)). The failure is a three-person team adopting the service boundaries of a fifty-person one, paying the coordination cost of an organization it does not have.

---

## What the claim costs

**Backward compatibility costs you the design you now know is right.** Every deprecated function is a maintenance burden, a documentation footnote, and a thing that must keep working while the replacement is built beside it. Go carries 175 of them. That is the price of the promise, paid in every release, and Go's maintainers consider it worth paying — which is a judgement about their users, not a universal one.

**Reducing complexity is invisible work.** Lehman's second law says complexity grows unless work is done to reduce it, and that work produces no feature. It is the first thing cut under pressure and the hardest to justify afterwards, because the counterfactual — how bad it would have got — is not observable.

**Conway's manoeuvre costs people.** Reorganizing a company to shape its software means changing who reports to whom, who sits with whom, and who owns what. That is disruptive, slow, and lands on humans rather than on code. It is not a refactoring, whatever the diagram suggests.

**Versioning multiplies your test surface.** Supporting v1 and v2 means every change is tested twice, every bug is fixed twice or triaged, and the paths diverge quietly until they behave differently in a case nobody covered.

**Deferring a schema decision costs more the longer you wait**, which is the one cost here that grows on its own. Every day of rows makes the migration bigger and the reconciliation harder ([Ch. 02](02_forces_f4m5.md) on decisions that expire).

---

## How to recognize the failure

**In a codebase:**

- **A published field renamed in a minor release.** The clients that break do so silently, reading a zero or a null, and the reports arrive as data-quality complaints weeks later.
- **A required field added to a request payload.** Every caller that has not been updated now fails, and you find out from them.
- **An enum extended without a documented default.** Old consumers hold a value with no branch for it.
- **`v2` of an API with no plan for retiring `v1`**, which is how you get to `v4` while still supporting all of them.
- **Two services that cannot be released independently.** They are one system with a network call in the middle, and the deployment boundary does not match the design boundary.
- **A service whose boundary matches a team that no longer exists.** Conway's Law recording an organization from three reorganizations ago.
- **No dead-code removal in the history.** Lehman's ratchet, visible: additions every week, removals never.

**In a conversation:**

- **"It's just a rename."** For an internal symbol, yes. For anything published, it is a removal and an addition, and the removal is what breaks people.
- **"We'll add people to catch up."** How long until they are productive, and who trains them — from which team's capacity?
- **"We'll clean it up in the next quarter."** Ask which quarter this was first said in.
- **"Nobody uses that endpoint."** Measured how, and over what window? Quarterly jobs are invisible in a week of logs.
- **"Let's split it into services so teams can move independently."** That is the inverse Conway manoeuvre, and it works when the teams already have separable ownership. It does not create that ownership.

The question that does the work: **how long am I going to live with this, and who else has to agree to change it?**

A day and nobody — do whatever is quickest. A decade and strangers — that is the other end of the range, and it is worth an afternoon of argument now, because there will not be a second chance to have it cheaply.

Part III turns from laws to patterns, starting with the question the whole part depends on — [what a pattern is actually for](10_what-a-pattern-is-for_3xzc.md), and the two tests that separate a pattern name carrying real information from one that only sounds like it does.

---

## Sources

- Meir M. Lehman, *Programs, Life Cycles, and Laws of Software Evolution* — Proceedings of the IEEE 68(9), September 1980.
- Frederick P. Brooks Jr., *The Mythical Man-Month* — Addison-Wesley, 1975.
- Go, `io/ioutil` — [pkg.go.dev/io/ioutil](https://pkg.go.dev/io/ioutil).
- *Go 1 and the Future of Go Programs* — [go.dev/doc/go1compat](https://go.dev/doc/go1compat).
- Rob Pike, *What We Got Right, What We Got Wrong*, closing talk at GopherConAU, Sydney, 10 November 2023, published 4 January 2024. [Text and slides](https://commandcenter.blogspot.com/2024/01/what-we-got-right-what-we-got-wrong.html).
- Melvin E. Conway, *How Do Committees Invent?* — Datamation 14(4), April 1968. [melconway.com/Home/Committees_Paper.html](http://www.melconway.com/Home/Committees_Paper.html).

---

[← Ch. 08](08_scale_637f.md)  ·  [Contents](00_toc.md)  ·  [Ch. 10 →](10_what-a-pattern-is-for_3xzc.md)
