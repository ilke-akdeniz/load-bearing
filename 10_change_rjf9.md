# Organization: The Input Nobody Chose

## The claim

**Your organization is a design Force that ends up in the software.**

Work has to be divided before it can start. Somebody decides that this team takes billing and that team takes fulfilment, or that these three engineers own the importer — and that decision is already a decomposition of the system, usually made before anyone has read the problem closely, by whoever was arranging the work.

---

## Conway's Law

From Melvin Conway in 1968. In his words:

> Organizations which design systems […] are constrained to produce designs which are copies of the communication structures of these organizations.

It is a description, not advice — [chapter 04](04_families-of-law_q5c6.md) uses exactly this distinction, since a law describes what happens while a Principle tells you to do something. Conway's Law tells nobody to do anything.

**"Communication structure" is easy to misread**, so it is worth taking from the same paper what Conway meant by it. He is not talking about how easily people can reach each other. He is talking about which groups have to agree with which:

> If there is a branch, then the two […] design groups X and Y which designed the two nodes must have **negotiated and agreed upon an interface specification** […] If, on the other hand, there is no branch between x and y, then the subsystems do not communicate with each other, there was nothing for the two corresponding design groups to negotiate.

*Negotiated and agreed upon.* An interface exists between two parts of the system exactly where two groups had to settle something between them. So the structure that gets copied is **who owns what and therefore who must agree with whom**.

Modern messaging tools let people in different time zones work on the same team, and they have no effect on Conway's Law. They lower the cost of talking; the constraint was never talking, it was agreement and ownership.

Conway states that both the system and the organization are graphs — for the system, "each node is a subsystem which communicates with other subsystems along the branches"; for the organization, the nodes are design groups and the branches are the pairs who had to negotiate something. His claim is that there is

> a homomorphism from the linear graph of a system to the linear graph of its design organization.

A homomorphism is a map that preserves structure: every subsystem corresponds to a group, every interface to a negotiation. This map runs in one direction only, which turns out to matter.

His own example is the one worth carrying. A research organization put five people on a COBOL compiler and three on an ALGOL compiler, and got **a five-phase COBOL compiler and a three-phase ALGOL compiler.** Nobody chose the number of phases. It was chosen when the people were assigned.

And the consequence that matters most here:

> Given any design team organization, there is a class of design alternatives which cannot be effectively pursued by such an organization because the necessary communication paths do not exist.

**Some designs are not available to you, given who owns what.**

What makes that division stick — the split of the system among owning teams — is an asymmetry in who is allowed to move a boundary.

Suppose one team owns both pricing and discounts. The boundary between them is **internal**: both sides of it belong to the same team. Notice on Tuesday that discount rules need to read tax state, move the boundary on Wednesday, and nobody outside the team is involved.

Now suppose pricing belongs to one team and fulfilment to another. The boundary between them is **shared**. If pricing works out that address validation really belongs on the fulfilment side, moving it means persuading fulfilment to reopen something they consider settled, reschedule work they have committed to, and take on a change that costs them this quarter and benefits somebody else.

So internal boundaries stay fluid and shared ones calcify — not because anyone is tempted into bad design, but because one correction is an afternoon and the other is a negotiation.

This is why good engineers do not escape it. Give that badly placed pricing-and-fulfilment boundary to two excellent engineers and each will build their own side well. Neither is positioned to notice the split was wrong, because each sees their own side working — and if one does notice, moving the boundary is not a decision they are allowed to make.

**Neither shape is better in itself**, and this is where the law is most often misread. Tight coupling between two things that genuinely are one thing is right — splitting them adds ceremony to something indivisible. A firm interface between things that genuinely are separate is also right. The law does not say that distance improves design.

What it says is that **your software gets its seams where the work was divided**, whether or not the problem has seams there. The failure it predicts is a *mismatch*: when the shape of the problem and the shape of the ownership disagree, ownership wins.

Both directions of mismatch are common.

- **One owner, two natural parts.** A team that owns what should be two separable things builds them as one. Nothing is broken and every test passes, so nobody notices — until the day the two need to ship on different schedules, or scale differently, or one has to be replaced, and it turns out they share state, types, and a deployment.
- **Two owners, one natural unit.** Two teams owning parts of something indivisible put a network call, a queue, or a versioned interface through the middle of it. Every change that should be one commit becomes two releases and a coordination meeting.

*(The quotations are from Conway's 1968 paper, "How Do Committees Invent?" The negotiation mechanism is his. What this book adds is the asymmetry that makes a partition stick — free to change inside an owner, expensive across — and the reading of "communication structure" as ownership, which is how his design-group argument lands in an organization that has teams rather than committees.)*

## The ratchet: why a codebase only grows

That asymmetry — one team can change what it owns, two teams must agree — also decides which direction the code grows in, acting on what is *in* the code rather than on where its boundaries fall. The result has a name of its own.

**Lehman's laws of software evolution**, from Meir Lehman and László Belady's study of large systems in the 1970s. The first: a system that is used must be continually adapted, or it becomes progressively less satisfactory. The mechanism is not that code rots — code nobody touches does exactly what it did last year. What moves is everything around it: tax rules, currencies, browser versions, the API you call, what users expect. **A system is judged against a moving world, so standing still is a slow decline.**

The second has more teeth: as a system evolves its complexity increases, unless deliberate work is done to reduce it.

That is a ratchet, and ownership is what drives it. Adding a case sits inside one owner — one `if`, one column, one flag, decided by whoever owns that file. Removing one means first establishing that nobody depends on it: finding every caller, every saved row, every customer whose workflow quietly relies on it, and getting agreement from each owner you turn up. **Additions need one person; removals need everybody who might object.** That is the boundary asymmetry again, applied to the contents instead of the seams — which is why additions happen continuously and removals need a project.

**On how much weight these carry.** Lehman's laws are empirical, and the study population was mainframe systems, decades ago, with release cycles measured in years. There are eight of them and they are not equally solid — the two above are widely recognizable, and several of the others ("conservation of familiarity," "conservation of organizational stability") are vague enough to resist being checked at all.

## One team per service, and where that heuristic breaks

Conway's Law is the reason behind the common advice that each service should have exactly one owning team, and the reasoning is sound as far as it goes: a deployment boundary that crosses a team boundary needs coordination on every release, which is the cost the boundary was supposed to remove.

But the advice is regularly applied in the wrong direction. It is a constraint on **who may own a service**, not a recipe for **how many services to have**.

Conway's homomorphism says why, if you follow the direction it runs. A map from the system to the organization assigns every subsystem exactly one design group — so several subsystems may share a group, and no subsystem may have two. *(Conway states the homomorphism; drawing this consequence out of its direction is this book's.)*

- **Many services owned by one team** is fine. It costs that team some operational overhead and nothing in coordination, because every release is theirs to schedule.
- **One service owned by many teams** is the failure the heuristic exists to prevent. Every release needs agreement from people with different priorities, so releases get slower, get batched, and eventually get scheduled.
- **Services sized to the team chart** is the failure the heuristic causes. If there are six teams, six services appear, whether or not the problem has six parts — and the seams land where the reporting lines are.

The honest form: **let the problem decide how many parts there are, then make sure no part is owned by more than one team.** If that turns out to be impossible with the teams you have, that is real information about the organization.

It is also the one case where the law gets used deliberately. The **inverse Conway manoeuvre** is reshaping the teams to get the architecture you want, rather than accepting the architecture your current teams will produce: if you want three independently deployable parts, create three teams that own them outright, and the seams will follow. It works because the homomorphism holds in the direction Conway stated. What it cannot do is manufacture the ownership — teams reorganized on a diagram, still needing each other's agreement to ship, produce the same coordination with new names on it.

## Coordination grows faster than the team

**Brooks's Law**, from Fred Brooks in 1975: adding people to a late software project makes it later.

The arithmetic underneath it is the same one behind [chapter 09](09_scale_637f.md)'s reversal, in a different medium — there it was workers contending for shared state, here it is people needing to stay aligned. Any two people on a team may need to coordinate, so the number of pairs is `n(n−1)/2`:

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

At twenty people, a quarter of everyone's time goes on staying aligned, before anyone writes anything.

This is the same variable Conway describes, priced. Conway says the structure follows who must agree with whom; Brooks says what that agreement costs as the number of people rises. A partition that reduces the number of pairs who must agree is buying back the time in the table above, which is the real argument for ownership boundaries — not tidiness.

Note what the law does *not* say. It is not "adding people never works," which would be absurd — every team that has ever grown is a counter-example. It says adding people to a **late** project makes it later, and the word doing the work is *late*: the remaining work is shorter than the time it takes a new person to become useful. A project badly behind a wrong estimate may not be late in that sense at all. It is under-staffed, and the fix is people.

The other half of Brooks stands regardless of arithmetic: some work does not divide. Brooks's own line is that the bearing of a child takes nine months no matter how many women are assigned, and a task with one indivisible critical path does not care how many people are waiting on it.

---

## Why the claim holds

Three things are true at once in every organization above a handful of people, and together they force the conclusion.

**The division comes first.** You cannot hand out work without partitioning the design, and the partition is settled before the problem is understood — by whoever was arranging the work, on the information they had that week.

**Corrections cost differently depending on where the boundary falls.** Inside one owner a wrong boundary is a Wednesday afternoon. Across two it is a negotiation with somebody who has other commitments and no benefit from the change.

**And the price of agreement rises faster than the headcount.** Brooks's `n(n−1)/2` is what a cross-owner correction is competing against, which is why the answer is so often *not this quarter*.

So the first division persists, and the software takes its shape from it. Nobody decides that the compiler has five phases. It is decided when five people are assigned, and it survives because moving a boundary between owners costs more than living with it.

This is also why the chapter is about engineering rather than management. The org chart is not offered here as something to fix. It is offered as **an input to the design that arrived without anyone treating it as one** — which makes it the same kind of thing as a latency budget or a durability requirement, and the reason it belongs in the room when the design is discussed.

---

## Where the claim doesn't apply

### Small teams, where Conway and Brooks go quiet

At three people the pair count is three, coordination is a conversation, and Conway's Law predicts a structure with no visible seams — which is correct, because there are none to have.

Neither law is false at that size; they have nothing to act on ([Ch. 02](02_the-five-kinds_cjx4.md)). The failure is a three-person team adopting the service boundaries of a fifty-person one, paying the coordination cost of an organization it does not have.

### Work with a known death date

A migration script that runs once. A spike written to answer a question. An import job for a system being decommissioned in March.

Each of these laws is a claim about **accumulated time**, and there is not going to be any. The ratchet needs years of additions to ratchet. Conway needs a second group with something to negotiate.

The failure here is not ignoring the laws but applying them — designing a spike for extension, or giving a one-off report an owning team. The dangerous version is a script that was going to be deleted and was not, which is what happens when nobody records the death date.

### One owner, whatever the headcount

A twenty-person team that genuinely owns one thing end to end has Brooks's coordination cost and none of Conway's boundary problem, because there is no second group to negotiate with. The pairs are still 190; the seams are still zero.

This is the case that shows the two laws are independent rather than one idea. Growing a team raises the price of agreement. Splitting ownership decides where agreement becomes necessary at all. You can have either without the other.

---

## What the claim costs

**Taking it seriously means treating a reorganization as a design change.** Reshaping teams to shape the software means changing who reports to whom, who sits with whom, and who owns what. That is disruptive, slow, and lands on people rather than on code. It is not a refactoring, whatever the diagram suggests.

**Reducing complexity is invisible work.** Lehman's second law says complexity grows unless work is done to reduce it, and that work produces no feature. It is the first thing cut under pressure and the hardest to justify afterwards, because the counterfactual — how bad it would have got — is not observable.

**Ownership boundaries buy coordination and sell flexibility.** A boundary that removes a negotiation also removes your ability to move it later without one. That is the trade, and it is worth making where the problem really has a seam and expensive where it does not.

**The law is easy to use as an excuse.** *Conway's Law* is available as an explanation for any architecture anyone dislikes, offered after the fact, with no prediction attached. A description used only in hindsight has stopped doing work.

---

## How to recognize the failure

**In a codebase:**

- **Two services that cannot be released independently.** They are one system with a network call in the middle, and the deployment boundary does not match the design boundary.
- **A service whose boundary matches a team that no longer exists.** Conway's Law recording an organization from three reorganizations ago.
- **No dead-code removal in the history.** The ratchet, visible: additions every week, removals never.
- **A module every team edits and none owns.** Every change to it is a negotiation, so it accumulates whatever was easiest to add rather than whatever was right.
- **The number of services equal to the number of teams**, arrived at without anyone asking how many parts the problem has.

**In a conversation:**

- **"We'll add people to catch up."** How long until they are productive, and who trains them — from which team's capacity?
- **"We'll clean it up next quarter."** Ask which quarter this was first said in.
- **"Let's split it into services so teams can move independently."** That is the inverse Conway manoeuvre, and it works when the teams already have separable ownership. It does not create that ownership.
- **"That's just how the code ended up."** Sometimes true, and worth one further question: who owned which parts while it was ending up that way?
- **"Conway's Law"** offered as a diagnosis after the architecture is built, with nothing following from it.

The question that does the work: **who has to agree before this can change?**

Nobody, and it is yours to fix this afternoon. Two teams, and the answer is a quarter. That number is set by a decision somebody made about who owns what, usually before the problem was understood — which is what makes it a design input rather than a fact of nature.

Part III turns from laws to patterns, starting with the question the whole part depends on — [what a pattern is actually for](11_what-a-pattern-is-for_3xzc.md), and the two tests that separate a pattern name carrying real information from one that only sounds like it does.

---

## Sources

- Melvin E. Conway, *How Do Committees Invent?* — Datamation 14(4), April 1968. [melconway.com/Home/Committees_Paper.html](http://www.melconway.com/Home/Committees_Paper.html).
- Meir M. Lehman, *Programs, Life Cycles, and Laws of Software Evolution* — Proceedings of the IEEE 68(9), September 1980.
- Frederick P. Brooks Jr., *The Mythical Man-Month* — Addison-Wesley, 1975.

---

[← Ch. 09](09_scale_637f.md)  ·  [Contents](00_toc.md)  ·  [Ch. 11 →](11_what-a-pattern-is-for_3xzc.md)
