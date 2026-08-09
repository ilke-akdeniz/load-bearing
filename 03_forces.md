# Forces: The Inputs Nobody Names

*This chapter is entirely about **Force** — the one kind in the model that is not advice. Chapter 02 established what a Force is and how it acts on Laws and Principles differently. This chapter says which Forces there are, how to read the value of each, and what changes when the value changes.*

## The claim

**Evaluating the forces that apply currently is crucial for any design** — but almost nobody does it, which is why so many design arguments cannot be settled.

## A Force is a dial, not a switch

Forces get read as present or absent. *Is there concurrency? Yes.* And then the design is chosen as though every concurrent system were the same system. But a Force has an **intensity**, [claude I changed the term "force value" to "force intensity". If you agree that this is better, apply that change for the rest of this chapter and then for the entire book] and the design does not change once as the value moves — it changes several times, and each change discards the previous answer rather than adding to it.

Let's take a look at different ways to handle concurrency for a single line of code that tracks "page view counts".

Comments in top of each line describes which value of the Force is present.

```go
// One writer. A nightly batch job, one goroutine, nothing else running.
counts[pageID]++
```

```go
// Many goroutines, one process. [claude is this similar to "many threads" situation for Java C#? If so add: "(Or many threads in Java, C#)" here.]
atomic.AddInt64(&counts[pageID], 1)
```

```sql
-- Many processes. The counter has to live where the serialization is.
update page set views = views + 1 where id = $1;
```

```sql
-- Many processes, and the caller retries after a timeout. [claude can we add this here: (Idempotency is important.)]
-- There is no counter any more. There is a log, and you count it.
insert into page_view (page_id, request_id) values ($1, $2)
on conflict (request_id) do nothing;
```

Four designs, one requirement, one intensity dial. Notice what happens at the last step: the answer stops being a different way to increment and becomes **a different data model**. You cannot get there by hardening the third version, and nothing about "we have concurrency" tells you which of the four you need.

That is the shape of every Force in this chapter. Read the value, not merley the presence.

---

## Seven Forces

### Concurrency

> **How many things can be doing this at once, and do they touch the same state?**

The demonstration is above. Two things about the intensity dial are worth stating.

**The positions are not evenly spaced.** Going from one writer to many goroutines is a small change. Going from many processes to many processes with retries is a change of data model, because a retried message is indistinguishable from a second event and the only fix is to make the operation idempotent.

**The value is usually lower than the vocabulary suggests.** A web service is described as concurrent, and it is — but if two requests never touch the same row, the Force is inert for that code path. Concurrency binds where writers *collide*, not where they merely coexist.

Chapter 06 owns the races themselves; chapter 07 owns why redelivery cannot be eliminated and idempotency is the answer.

### Durability of the medium 
[Claude this subsection needs many improvements. Clarify "durability" and "medium". What do these mean concretely?]

> **How long does what this writes outlive the code that wrote it?**
[Claude, above is an obscure, enigmatic sentence. Be explicit and simple.]

The intensity dial runs further than people expect:

```text
a local variable        microseconds [Missing code example]
a struct field          until the next deploy
a row in a table        longer than the current codebase
a published format      as long as anyone keeps a copy [Missing code example]
```

Adding a field looks like the same act at every position. It is not.

```go
// Code. Add it, ship it, done. Nothing has to be decided. 
// [claude can't just say "Nothing has to be decided". That's obviously not true. 
// Maybe you need to show the caller code who could be affected by those changes and has to decide tthins for all those examples.
// Then here you can show how those places has nothing to decide. ]
type Order struct {
	ID    uuid.UUID
	Total int64
	Tip   int64 // new
}
```

```sql
-- Rows. Adding it forces an answer to a question the struct never asked.
alter table "order" add column tip bigint not null default 0;
```

Every one of the four million existing orders now reads as having a zero tip. That may be false — tips may have been taken in cash, or recorded in a notes field, or simply not tracked. Those are different facts, and the default has made them **permanently indistinguishable**: no later query separates "tipped nothing" from "we did not know."

The nullable version keeps them apart, and charges for it:

```sql
alter table "order" add column tip bigint;   -- null means "not known"
```

Now every read site handles a null, forever, including the ones written by people who never heard of this migration.

**What changes with the Force:** whether *unknown* needs to be representable. At the top of the dial the question does not arise, because there is no history to be wrong about. At the bottom it is the whole decision, and it is one you get to make once. 
[Claude is this really the only thing that changes: "What changes with the Force:** whether *unknown* needs to be representable"?
 If so, I'm not sure if this is really a Force or you are just conflating something more minor to be a Force. 
 Or maybe you are missing the real Force which this minor thing is a small part of it. ]

### Blast radius

> **When this fails, what is the worst thing that happens, who is the victim and what would be the resolution?**

```text [claude if you think of a better formatting for this piece do it. (table?)]
sum is wrong by an order of cents in a report -> an analyst notices it -> no resolution needed, dashboard is expected to have variations of cents
an invoice total is wrong -> customer sees the discrepancy. -> a support ticket is created
a payment processed with incorrect amount -> buyer sees the difference one month later -> a refund, and a reconciliation
a drill controler ships to an offline field -> drill operator notices malfunction -> fetch the controller back, update, re-send in weeks 
```

The same arithmetic sits at every position, and is correct at some and disqualifying at others:

```python
# Blast radius: a dashboard. Nobody reconciles this against anything.
total = sum(float(r["amount"]) for r in rows)
```

```python
# Blast radius: an invoice. The same code is now a defect. [claude this is not the same code...]
total = sum(int(r["amount_minor"]) for r in rows)
```

```text
sum of ten 0.1        = 0.9999999999999999    != 1.0 [claude maybe you should show these under each code and frame this clearly as a sentence rather then this weird mixture of sentence and formula]
sum of ten 10 (minor) = 100                   == 100 [claude what does this even mean? "ten 10 (minor) = 100" !?]
```

The float version is not sloppy work that the dashboard tolerates. It is *correct* for a dashboard, where a rounding error below display precision cannot produce a wrong decision — and adding decimal arithmetic there costs real time and buys nothing measurable.

**What changes with the Force:** how much prevention is worth buying. This is the Force that decides whether a defensive check is diligence or noise, and it is the one most often read from habit rather than from the situation.

### Change frequency, and its shape

> **How often does this change, and when it does, how many places change with it?**

Two readings, and the second is the one that gets skipped.

```go
// Two payment methods in six years. The switch is correct, and a
// registry here would be structure paid for and never used.
switch method {
case "card":
	return chargeCard(ctx, order)
case "invoice":
	return raiseInvoice(ctx, order)
}
```

```go
// A new method every quarter, each with its own config and webhook.
// The registry pays for itself in the second year.
var methods = map[string]Method{}

func Register(name string, m Method) { methods[name] = m }
```

Now the shape. The same change, under three structures:

```text
adding one payment method touches
  switch      1 file
  registry    2 files   the implementation, and one registration line
  layered     6 files   dto, entity, mapper, service, repository, controller [claude there is no code example for this and I think this the ones that needs that the most. I fail to visualize why adding a payment method would touch all those. Not a full complete code but stubs that explains the case]
```

The third row is not a worse team. [claude what does the word "team" do here? Looks like an hallucination to me.] It is a structure whose boundaries do not line up with the way change actually arrives, so every change crosses all of them. Chapter 05 owns why fan-in sets the price of a change; chapter 18 owns what those particular boundaries cost.

**What changes with the Force:** whether structure that makes adding cheap is worth having. Frequency alone does not decide it — a thing that changes monthly in one file needs nothing.

### Team size and turnover

> **How many people must agree to change this, and how many of today's people will still be here in two years?**

Turnover is the half that gets dropped, and it is the sharper one. A rule that lives in one person's head is free while they are there and worth nothing the week after they leave.

```go
// Team of two, nobody leaving. A comment is enough — the reviewer is [claude nobody leaving is useless here, there is no way to know in advance if anybody leaving tomorrow or not in the real world]
// the other author, and both remember why.
// Amounts are minor units. Never build one of these from a float.
type Money struct {
	Amount   int64
	Currency string
}
```

```go
// Team of twenty, a third of them new this year. The comment is a wish. [claude Did you mean this: "Portection by just a comment would only be wish."]
package money

type Money struct {
	amount   int64 // unexported: nothing outside can set these
	currency string
}

func FromMinorUnits(a int64, c string) Money {
	return Money{amount: a, currency: c}
}

// There is deliberately no FromFloat.
```

**What changes with the Force:** where the rule lives. It migrates from a comment, to a review habit, to the type system, as the number of people who must know it rises and the chance that any of them was present for the original conversation falls.

The second version is not free: it costs a package boundary and a constructor call at every site, and it is worth that only at some sizes. Chapter 12 catalogues the technique; the point here is that **the same rule needs a different mechanism at a different team size**, and neither mechanism is the better engineering in general.

### Latency budget

> **What is the budget for this operation, and what fraction of it does one mechanism cost?**

Consider following operations with different budgets and the same "fetching user's data" operation performed:

```python
# A web page render with 200 ms latency budget. A database round trip is one percent
# of it. It's ok to spend it and think about something else.
user = db.query("select * from users where id = %s", uid)
```

```go
// A ... [claude use a simple business description here like I did for the "web page render"] with 5 ms budget. The round trip is now most of the
// budget, so the operation has a narrower latency room. The design question changes from "how do I fetch this"
// to "how stale is this allowed to be."
if u, ok := cache.Get(uid); ok {
	return u
}
```

```c
/* A ... [claude add simple business description here like I did for the "web page render"], 200 us [clarify us, is it nano-seconds?] budget. There is no lookup. The data is resident, indexed by id, and the memory layout is the design. */
user_t *u = &users[uid];
```

**What changes with the Force:** at the top of the range, abstraction is free and you should buy it. At the bottom, the abstraction *is* the budget [claude are you using "budget" to mean cost here? In any case, this is confusing when we have seen that budget was used for the latency. If this is a different usage, find another word], and the code stops looking like the code in books. Chapter 08 owns the arithmetic underneath this; chapter 05's entity-component case is this Force pushed to its end.

### Control of the callers

> **Can I change every call site myself, and would I know if I broke one?**

Three values, and the middle one is where most working systems actually sit:

```text
you control every caller       change it, fix the call sites, done
you can see them but not
  change them                  you can deprecate with evidence
you can neither see nor
  change them                  you can only add
```

Here is a defect that makes the difference concrete. A server sends a 64-bit identifier as a JSON number:

```json
{"id": 9007199254740993, "amount": 1234}
```

Every JavaScript client silently reads a different number:

```text
wire says       9007199254740993
JS client reads 9007199254740992
```

JavaScript has one number type, a double, exact only to 2^53−1. Postgres `bigint` runs to 2^63−1. Identifiers in the gap arrive wrong, without an error, in any browser.

The fix is to send it as a string:

```json
{"id": "9007199254740993"}
```

The Force decides whether you can apply it:

- **You own every client.** Change both sides, deploy together, delete the old field the same afternoon.
- **You can see your clients.** Ship both fields, log which one each caller reads, remove the number when the count reaches zero. Weeks, and a dashboard.
- **You can see nothing.** The numeric field is permanent. You add `id_string`, document that `id` is lossy above 2^53, and carry both indefinitely — and every future field faces the same question before it ships.

Same defect, same fix, three different projects. Nothing about the code told you which one you were in.

**What changes with the Force:** not the design, the *plan*. This is the Force that decides how much a mistake costs to correct, which is why it belongs in the room before the API is designed rather than after. Chapter 05 owns what this implies for what you expose in the first place.

### The seven forces, as questions

| Force | The question that reads it |
|---|---|
| Concurrency | How many at once, and do they touch the same state? |
| Durability of the medium | How long does this outlive the code that wrote it? |
| Blast radius | When it is wrong, what happens and who finds out? |
| Change frequency and shape | How often, and how many places at a time? |
| Team size and turnover | How many must agree, and how many will still be here? |
| Latency budget | What is the budget, and what does one mechanism cost of it? |
| Control of the callers | Can I change every call site, and would I know if I broke one? |

---

## Why it holds

Three mechanisms support this chapter's claim and the third one is crucial.

**A Force that is not evaluated is just a mood.** "It needs to scale" cannot be verified, argued with, or revisited. "Twelve thousand requests a minute at peak, of which about thirty are writes to the same row" can be looked up, can be wrong, and can be checked again next year. [claude which of our 7 force(s) plays in this example? I couldn't decipher.] Evaluation converts a mood into a claim, and claims can be tested.

**Forces are where the disagreement actually lives.** Chapter 02 records this as a failure symptom; the mechanism is that two people arguing about a Principle have usually already agreed about the Principle and are differing about the situation it is conditioned on. Stating the Force ends the argument or relocates it to something answerable.

**Forces move on a different clock than code.** This is the part that does real damage. A team doubles. A service acquires a second client, then a client outside the company. A table crosses a hundred million rows. A batch job is called from a request handler for the first time. None of those are code changes, none show up in a diff, and every one of them can invalidate a Principle that was correctly derived years earlier. The code that was right is now wrong, and nothing in the repository records why it was ever right, arrived at without anyone making a mistake.

---

## Where this doesn't apply

### Forces you cannot measure yet

The hard case, and the common one.

A product three months old. You do not know peak traffic, or the team size in a year, or whether this schema survives contact with real customers. Every question in the table above returns *don't know*, and the chapter's method appears to have nothing to say.

The tempting move is to guess high. It feels like prudence: assume growth, shard the database, split the services, put an event bus in early. It is the most expensive mistake available, because every one of those costs is paid immediately and in full, while the benefit arrives only in a particular branch of the future where you got big in a certain way. What's ironic is that this artificial machinery slows you down considerably to make that branch less likely.

The rule that works is not "defer everything." It is:

> **Defer any machinery that is not needed today, and can be added later with minimal cost.** 
> **If future removal is free but future addition is costly and the need is likely to arise add the machinery now.**

Both halves have a worked case in FlowCore's decision log. [claude, we are familiar with flowcore's codebase and understand following examples, but the readers of the book won't. Introduce the examples with more context and details so that the readers can understand the point.]

Reversible, so deferred, with the trigger written down:

> `internal/` can be introduced later if a second package genuinely needs to share machinery.

Irreversible, so decided on day one, and decided strictly:

> Dropping a unique index later is trivial; adding one after clients hold duplicate rows is not.

The second is the one worth internalizing. Ship without the constraint and let two years of duplicate rows accumulate, and adding it later needs a data migration, a reconciliation policy, and a conversation with every client about which duplicate wins. Ship with it and discover it is too strict, and the fix is one `drop index`. **Under uncertainty, prefer the decision you can walk back** — which is usually the stricter one, not the more permissive one, and that is the opposite of what "stay flexible" suggests.

### A Force with no design consequence

If both ends of the dial produce the same code, the Force is not live here and naming it is overhead.

A build script runs concurrently with nothing and touches no shared state. Concurrency is a fact about it and not a Force acting on it. The test is mechanical: name a value at each end and write the two designs. If they are the same design, stop. 
[claude I'm confused by this part. Changing the dial would evolve the build script to something else with more concurrency intensity on it. Then your mechanical test is useless and "both ends of the dial producing the same code" is meaningless. Am I missing something?]

### Things that are risk, not unmeasured Forces

*Will this product exist in two years?* is not a measurement you are deferring. There is no instrument. Treating it as a Force to be estimated harder produces a number with no content, and then decisions get justified by it.

The honest response to genuine uncertainty is not a better estimate. It is to keep the cost of being wrong low, and to know which decisions those are — which is the reversibility question again, doing the only work available.
[claude this sounds like an interesting distinction. Worth putting a concrete smalle example maybe with code]

---

## What it costs

**A named Force licenses machinery.** "We have concurrency" becomes a distributed lock, in a program with one writer. Naming a Force is not the same as reading its value, and the value is almost always lower than the name suggests. The discipline: no Force may be cited in a design discussion without the number, or the answer *don't know* said out loud. [claude worth noticing that I suggested changing "named" to "evaluated" which encompasses reading its value. I don't think there is much value at purely "naming" as it adds not much, the exact point you are making here. And following same line of thought, I don't think we should focus the chapter on "naming". It should be obvious that to evaluate something, you shoule identify and name it first. This cost description is still valuable tough becaus that's precisely what loosy architects do all the time: Just naming the force and jumping into conclusions.]

**Half of these are estimates about the future wearing a measurement's clothes.** Team size in two years. Change frequency of a feature that does not exist yet. Peak traffic for a product with no users. Concurrency and latency can be measured today; the rest are forecasts, and should be labelled as such wherever they are written down.

**A written force-map goes stale, and a stale one is worse than none**, because it looks authoritative and nobody re-derives what a document already answers. Date them, and treat an undated one as unsigned.

**This chapter does not resolve conflicts.** Low latency pulls against durability. A small team pulls against a large blast radius. Naming both does not tell you which wins, and the honest answer is that trade-offs are decided rather than computed. Chapter 19 works through what to do when Forces point in opposite directions.

---

## How to recognize the failure

**In a codebase:**

- **Retry with exponential backoff around a call to a function in the same binary.** A distribution Force imported wholesale from somewhere it was real. [claude add a sentence showing why this machinery is absurd in this position when we evaluate the force.]
- **A read-modify-write in a request handler.** A concurrency Force present and unread (Ch. 06). [claude add the severe cause: "and unread, results in data loss."]
- **Retry logic with no idempotency key.** Half of a Force read: the failure was anticipated, the redelivery it causes was not (Ch. 07).
- **A `not null default` in a migration** that quietly asserts something false about every row that predates it. [claude what was the force related failure here?]
- **A cache with no invalidation rule.** The latency Force was read and the change-frequency Force was not, so the design answers one question and ignores the one that decides whether it is correct.
- **An invariant enforced by a comment, in a codebase with forty contributors** and a third of them new this year.
- **Interfaces, queues, and feature flags added for a shape of scale that has not arrived** — and no note anywhere saying what would have to become true for them to be needed.
[claude notice I added the word "shape" above. My reasoning is that you can't just say high scale and come up with an identical design. A high scale can come in different shapes. Frequent bursts vs high average, data size etc... And your specific queue - interface deisng won't match all of those shapes.]

**In a conversation:**

- **"It needs to scale."** With no number attached, this is not a Force, it is a mood.
- **"That's not how it's done"** — where the reason, when you dig, turns out to be a Force that held at the speaker's last job and has not been checked against this one.
- **A design defended by a Force nobody has measured in a year.** Team size, traffic, and client count all move without a commit.
- **"Just in case"** doing the work that a measurement should be doing.

Chapter 02 already showed the sharpest version of this as a symptom of the model being misused: two people making increasingly detailed arguments while disagreeing about a Force neither has stated. The remedy is small and almost never applied — stop arguing about the Principle and ask each side what they believe about the situation.

---

**Next:** chapter 04 turns to Laws, and to the fact that they do not all have the same standing — a proven theorem, a near-tautology, and an empirical regularity are three different kinds of true, and conflating them repeats the exact error this book is about. [claude delete this yourself: ", and conflating them repeats the exact error this book is about." I hope you understand why the deletion is better. Also recommend a claude.md addition to prevent these.]
