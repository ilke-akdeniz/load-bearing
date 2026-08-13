# Change: Evolution, Organization, Compatibility

*This chapter is **Law**, and almost all of it is the empirical kind (Ch. 04). That matters more than usual. An empirical law is a pattern somebody observed, in particular systems, at a particular time — so the pattern may transfer while the numbers do not, and it is worth knowing what was studied before leaning on the result.*

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

**On how much weight these carry.** Lehman's laws are empirical, and the study population was mainframe systems, decades ago, with release cycles measured in years. There are eight of them, and they are not equally solid — the two above are widely recognizable, and several of the others ("conservation of familiarity," "conservation of organizational stability") are vague enough that they resist being checked at all. Cite the two; treat the rest as observations of their era. [claude the last sentence reads like a prompt for you, should be removed in my opinion.]

### Once published, it is forever

This is the sharpest constraint in the chapter, and the one that is most often discovered late.

[claude below example is another failure of assuming the reader knows go. You have to explain what the `json:` does.]

Here is a client written against version 1 of an API. It is installed on machines you do not control and will not be recompiled:

```go
type OldClient struct {
	ID     string `json:"id"`
	Amount int64  `json:"amount_minor"`
	Status string `json:"status"`
}
```

Now change the server four ways and watch what reaches that client: 
[claude you say what reaches that client but then you say "parsed"
My suggestion is to us pare here as well" "watch what client parses". 
The distinction matters, because server is sending new fields but client is not able to parse them.]

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

That is what the commitment costs when it is kept. Chapter 05 covers the other half of this problem: users depend on behaviour you never documented, so the surface you are committed to is larger than the one you published.

### The organization ends up in the software

**Conway's Law**, from Melvin Conway in 1968: organizations produce designs that copy their own communication structures.

It is a description, not advice — chapter 04 uses exactly this distinction, since a law describes what happens while a principle tells you to do something. Conway's Law tells nobody to do anything.

The mechanism is ordinary. Two engineers at neighbouring desks who talk twenty times a day will build things that call each other directly, share types, and assume each other's invariants — because that is the cheap thing to do when coordination is free. Two teams in different time zones who talk through a ticket queue will build things that communicate through a versioned interface, because everything else is unbearable. Neither team decided on an architecture. **The interface between two pieces of software ends up as expensive to cross as the conversation between the people who own them.**
[claude this example sounds unreal. Maybe it's true but I just want to confirm, are the examples above canonical and attested? I fail to grasp how this works. Does this mean that the only way to develop maintainable software with a team is to let each team member talk to each other in carefully crafted messages, in given times, in preset coversational topics? (encapsulation, public API). To me this logical extension of the example sounds absurd.]

That gives the manoeuvre the TOC calls the inverse: if you want a particular architecture, arrange the teams to match it and let the structure follow. It is used deliberately when organizations split a monolith — reorganize into teams that own separable areas, and the seams appear because crossing them has become expensive.

Worth being honest that the inverse manoeuvre is far less established than the observation. Conway's Law is widely recognized; the claim that you can reliably *drive* architecture by reshaping teams is a strategy, not a finding, and it is slow, disruptive, and easy to get wrong.

### Coordination grows faster than the team

**Brooks's Law**, from Fred Brooks in 1975: adding people to a late software project makes it later.

The arithmetic underneath it is the same one behind chapter 08's reversal. Any two people on a team may need to coordinate, so the number of pairs is `n(n−1)/2`:

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

Note what the law does *not* say. It is not "adding people never works," which would be absurd. It is that adding people **to a late project** makes it later, because the ramp-up and coordination costs land immediately and the extra capacity arrives after the deadline. Teams do grow, and it works when there is time to absorb it and the work can be split along a seam that already exists — which is Conway's Law being used on purpose.

[claude a tought exercise: Project was estimated 100 hours. 2 people started, producing 2 x 5 = 10 hours of work everyday. 
After 12 days project is not finished yet altought 120 hours was spent.
Then two managers study the project plan and come up with different forecast: A says remaining work is 80 hours more, so 200 in total.
B says a huge mistake was made in the inital estimate, total is 1000 hours and remaining is 988 hours.
Now how do you assess this with Brook's Law? What is late when A is right vs B is right? Does adding people make the project late in each case?
What's the optimal approach for each case? ]

---

## Why it holds

The four results have one thing in common: **their feedback loops are longer than the decisions that cause them.**

You can test a function in seconds and a deployment in hours. You cannot test a schema decision, because the evidence arrives when the table has four years of rows in it. You cannot test a published interface, because the evidence arrives when other people's software depends on it. You cannot test an organizational structure, because the evidence arrives in the architecture a year later.

That length is the entire difficulty. Everywhere else in engineering, being wrong is cheap because you find out quickly and try again. Here you find out after the cost is sunk, which is why these are the decisions worth slowing down for — and it is chapter 03's reversibility question, applied at the timescale where it bites hardest.

The compatibility rule follows from something narrower and worth stating separately: **you cannot deploy other people's software.** Every other constraint in this book can be fixed by changing code you control. This one cannot, because the code that has to change is on a machine you have no access to and belongs to someone who has no reason to hurry.

---

## Where this doesn't apply

### Code with a known death date

A migration script that runs once. A spike written to answer a question. A report generated for one meeting. An import job for a system being decommissioned in March.

None of the four applies, and the reason is worth being precise about: **each of these laws is a claim about accumulated time**, and there is not going to be any. Lehman's ratchet needs years of additions to ratchet. Compatibility needs a second party. Conway needs a second team. 

The failure here is not ignoring the laws — it is applying them. Versioning the output of a one-off report, or designing a spike for extension, spends the effort that these laws exist to justify on the one case where the justification is absent.

The dangerous version is a script that was going to be deleted and was not. That is not a failure of judgment about the script; it is what happens when nobody records the death date. If the plan is that this disappears, write down when, and what should be true when it does.

### Internal interfaces you can change atomically

"Once published, forever" applies to what you cannot recompile. A function called only from inside one repository, deployed as one unit, is not published in this sense — rename it, fix the call sites, ship all of it together, and no compatibility problem exists.

This is why the same change is trivial in one codebase and a six-month deprecation in another, and the difference is not code quality. It is chapter 03's control-of-callers Force, at its most consequential.

The mistake in both directions is common. Teams version internal APIs that only they call, paying deprecation costs for nothing. Other teams treat a genuinely published interface as internal, and break customers.

### Small teams, where Brooks and Conway go quiet

At three people the pair count is three, coordination is a conversation, and Conway's Law predicts a structure with no visible seams — which is correct, because there are none to have.

Neither law is false at that size; they have nothing to act on (Ch. 02). The failure is a three-person team adopting the service boundaries of a fifty-person one, paying the coordination cost of an organization it does not have.

---

## What it costs

**Backward compatibility costs you the design you now know is right.** Every deprecated function is a maintenance burden, a documentation footnote, and a thing that must keep working while the replacement is built beside it. Go carries 175 of them. That is the price of the promise, paid in every release, and Go's maintainers consider it worth paying — which is a judgement about their users, not a universal one.

**Reducing complexity is invisible work.** Lehman's second law says complexity grows unless work is done to reduce it, and that work produces no feature. It is the first thing cut under pressure and the hardest to justify afterwards, because the counterfactual — how bad it would have got — is not observable.

**Conway's manoeuvre costs people.** Reorganizing a company to shape its software means changing who reports to whom, who sits with whom, and who owns what. That is disruptive, slow, and lands on humans rather than on code. It is not a refactoring, whatever the diagram suggests.

**Versioning multiplies your test surface.** Supporting v1 and v2 means every change is tested twice, every bug is fixed twice or triaged, and the paths diverge quietly until they behave differently in a case nobody covered.

**Deferring a schema decision costs more the longer you wait**, which is the one cost here that grows on its own. Every day of rows makes the migration bigger and the reconciliation harder (Ch. 03 on decisions that expire).

---

## How to recognize the failure

**In a codebase:**

- **A published field renamed in a minor release.** The clients that break do so silently, reading a zero or a null, and the reports arrive as data-quality complaints weeks later.
- **A required field added to a request payload.** Every caller that has not been updated now fails, and you find out from them.
- **An enum extended without a documented default.** Old consumers hold a value with no branch for it.
- **`v2` of an API with no plan for retiring `v1`**, which is how you get to `v4` while still supporting all of them.
- **Two services that cannot be released independently.** They are one system with a network call in the middle, and the deployment boundary does not match the design boundary.
- **A service whose boundary matches a team that no longer exists.** Conway's Law recording an organization from three reorganizations ago.
[claude should each service owned by separate teams ideally? If so I think this idea of team structure and software architecture - org could be worthy of an expansion with examples inside this chapter. Unless we have other places talking about this in the ledger.]
- **No dead-code removal in the history.** Lehman's ratchet, visible: additions every week, removals never.

**In a conversation:**

- **"It's just a rename."** For an internal symbol, yes. For anything published, it is a removal and an addition, and the removal is what breaks people.
- **"We'll add people to catch up."** How long until they are productive, and who trains them — from which team's capacity?
- **"We'll clean it up in the next quarter."** Ask which quarter this was first said in.
- **"Nobody uses that endpoint."** Measured how, and over what window? Quarterly jobs are invisible in a week of logs.
- **"Let's split it into services so teams can move independently."** That is the inverse Conway manoeuvre, and it works when the teams already have separable ownership. It does not create that ownership. [claude could be treated in the same expansion section I refer in my previous comment]

The question that does the work: **how long am I going to live with this, and who else has to agree to change it?**

A day and nobody — do whatever is quickest. A decade and strangers — that is the other end of the range, and it is worth an afternoon of argument now, because there will not be a second chance to have it cheaply.

---

**Next:** Part III turns from laws to patterns, starting with the question the whole part depends on — what a pattern is actually for, and the two tests that separate a name worth having from a name that only sounds like one. [claude a name? What do you mean?]
