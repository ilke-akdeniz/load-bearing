# Forces: The Inputs Nobody Names

## The claim

**Evaluating the Forces acting on your situation is the groundwork** — and almost nobody does it, which is why so many design arguments cannot be settled.

## A Force is a dial, not a switch

Forces get read as present or absent. *Is there concurrency? Yes.* And then the design is chosen as though every concurrent system were the same system. But a Force has an **intensity**, and the design does not change once as the intensity rises — it changes several times, and each change discards the previous answer rather than adding to it.

Intensity means **how hard the Force presses on the design**, which is not always the same as how large the number is. Latency is the case where the two run opposite: a 200 millisecond budget leaves the design free, a 200 microsecond budget dictates it, so **the smaller the budget, the stronger the Force.** Read the pressure, not the number.

Below are four ways to handle the same requirement — counting page views — at four intensities of one Force. The comment above each says which intensity it is written for.

```go
// One writer. A nightly batch job, one goroutine, nothing else running.
counts[pageID]++
```

```go
// Many goroutines, one process. The same situation as many threads
// in one JVM or one .NET process.
atomic.AddInt64(&counts[pageID], 1)
```

```sql
-- Many processes. The counter has to live where the serialization is.
update page set views = views + 1 where id = $1;
```

```sql
-- Many processes, and the caller retries after a timeout, so the same
-- event can arrive twice. The write has to be idempotent: applying it
-- again must change nothing. There is no counter any more — there is a
-- log, and you count it.
insert into page_view (page_id, request_id) values ($1, $2)
on conflict (request_id) do nothing;
```

Four designs, one requirement, one intensity dial. Notice what happens at the last step: the answer stops being a different way to increment and becomes **a different data model**. You cannot get there by hardening the third version, and nothing about "we have concurrency" tells you which of the four you need.

That is the shape of every Force in this chapter. Read the intensity, not merely the presence.

---

## Seven Forces

### Concurrency

> **How many things can be doing this at once, and do they touch the same state?**

The demonstration is above. Two things about the intensity dial are worth stating.

**The positions are not evenly spaced.** Going from one writer to many goroutines is a small change. Going from many processes to many processes with retries is a change of data model, because a retried message is indistinguishable from a second event and the only fix is to make the operation idempotent.

**The intensity is usually lower than the vocabulary suggests.** A web service is described as concurrent, and it is — but if two requests never touch the same row, the Force is inert for that code path. Concurrency binds where writers *collide*, not where they merely coexist.

Chapter 06 owns the races themselves; chapter 07 owns why redelivery cannot be eliminated and idempotency is the answer.

### Durability of the medium

Two words to pin down first, because both are doing specific work.

**Medium** is whatever this code writes *to*: a local variable, a field in a struct, a row in a table, a message on a queue, a line in a log someone archives, a JSON field a client parses. **Durability** is how long what you wrote stays there after the code that wrote it has been replaced.

> **If I get this wrong, can I still fix it once the wrong version has been running for a year?**

That is the whole Force. Code can be edited; accumulated state often cannot, because fixing it requires information that was never recorded.

```text
medium              lives for            a mistake is fixed by
local variable      microseconds         editing the line
struct field        until next deploy    editing it, redeploying
row in a table      longer than the      a migration — and some are
                    current codebase     impossible
published format    as long as any       nothing. You add a second
                    client keeps a copy  field and carry both
```

The same act — adding one field — is a different decision at each position.

**At the top of the dial**, nothing is at stake, because nothing has accumulated:

```go
type Order struct {
	ID    uuid.UUID
	Total int64
	Tip   int64 // new
}
```

Existing callers are unaffected: Go zero-initializes the new field, and code that never mentions `Tip` compiles and behaves exactly as before.

```go
// Written before Tip existed. Still correct, still compiles.
func Receipt(o Order) string {
	return fmt.Sprintf("total %d", o.Total)
}
```

If the field turns out to be a mistake, delete it and redeploy. There is no history of orders-without-tips to be wrong about, because the struct holds only what is in memory right now.

**At the bottom of the dial**, the same addition forces a decision about the past:

```sql
alter table "order" add column tip bigint not null default 0;
```

Every one of the four million existing orders now reads as having a zero tip. That may be false — tips may have been taken in cash, recorded in a notes field, or not tracked at all. Those are different facts, and the default has made them **permanently indistinguishable**. There is no later query that separates "tipped nothing" from "we never knew," because the distinction was never written down.

The nullable version keeps them apart, and charges for it:

```sql
alter table "order" add column tip bigint;   -- null means "not known"
```

Now every read site handles a null, forever, including the ones written by people who never heard of this migration.

Notice that the mistake is not detectable later. Both migrations succeed, both applications work, and the difference only appears the day someone asks how many customers tipped nothing — by which point the answer is unrecoverable.

**What changes with the Force: whether a mistake is correctable, and therefore how much care the decision is worth.**

That is the general form, and the tip column is one instance of it. Two others follow from the same reading.

**Where an invariant should be enforced.** If the rows outlive every version of the code that writes them, then a rule enforced only in application code is a rule that holds for as long as one code path remembers it. A constraint in the schema holds for the `psql` session at 2am, the data-fix script, the bulk import, and the admin tool written next year by someone who has never read your service layer. The durability of the medium is the reason that argument is not merely a preference (Ch. 06 owns the class of invariants application code *cannot* enforce at all).

**Whether "we'll clean it up later" is available.** At the top of the dial it always is. At the bottom it is available only while the wrong state is small, and the window closes silently as rows accumulate.

This Force is the sibling of blast radius, and they are worth keeping distinct: **blast radius is how bad it is when you are wrong; durability is whether you can stop being wrong.** A dashboard with a wrong number has a small blast radius and a short-lived medium — fix the query, and the past repairs itself. A schema with a wrong column has a modest blast radius and a permanent medium, which is why it deserves more argument than its severity alone suggests.

### Blast radius

> **When this fails, what is the worst thing that happens, who notices, and what does it take to put right?**

| what goes wrong | who notices | what putting it right costs |
|---|---|---|
| a revenue chart is off by a few cents | nobody | fix the code; nothing was issued to anyone |
| an invoice total is off by a cent | the customer | a support ticket and a corrected invoice |
| a payment is taken for the wrong amount | the buyer, a month later | a refund, plus reconciliation across every affected account |
| a drill controller ships with the fault | the operator, on site | recall the unit, reflash it, ship it back — weeks |

Two conditions make the first row cheap, and both are worth naming because neither is "the error is small."

**The error is below the precision of any decision made from the number.** Nobody chooses differently because a category total reads 4,182.31 instead of 4,182.34. Change the audience to an auditor and the same error stops being tolerable at the same magnitude.

**Nothing was issued.** A chart is derived from source data and recomputed on every load, so fixing the code fixes every future view and no artifact carries the old number. An invoice is the opposite: it was sent, someone has it, and correcting it means a second document and an explanation. That is the property that actually separates row one from row two — not the size of the error but whether anything left the building.

Now one function, and nothing careless about it:

```python
def split(total, n):
    """Divide a charge into n equal line items."""
    return [round(total / n, 2)] * n
```

Behind a dashboard that charts revenue per category, this is correct. The rounding error is smaller than the precision anyone reads off a chart, and no decision changes because of it.

Move the same function — not a rewrite, the same three lines — into invoice generation:

```text
>>> split(8.03, 3)
[2.68, 2.68, 2.68]        which sums to 8.04
```

The three line items add up to a penny more than the charge, because 8.03 ÷ 3 is 2.6766… and every line rounds up. The invoice does not reconcile against the payment, and the discrepancy is in the customer's favour on some orders and yours on others, so it will not even show up as a consistent drift.

In minor units the same split is exact, and the leftover has to be placed deliberately rather than silently:

```python
def split_minor(total_cents, n):
    base = total_cents // n     # 803 // 3 = 267 cents per line
    remainder = total_cents % n # 803 %  3 =   2 cents left over

    lines = []
    for i in range(n):
        # The leftover cannot be divided, so it is handed out one cent
        # at a time to the first `remainder` lines. Nothing is dropped
        # and nothing is invented — the lines always sum to the total.
        extra = 1 if i < remainder else 0
        lines.append(base + extra)

    return lines
```

```text
>>> split_minor(803, 3)
[268, 268, 267]           which sums to 803
```

**`split` did not change. The blast radius did.** `split_minor` is what you write once you know the radius; the demonstration is what happened before you knew it. That is the point: `split` is not sloppy work that the dashboard tolerates and the invoice exposes — it is *correct* for one and *defective* for the other, and nothing you can see in the function tells you which.

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
  layered     6 files   see below
```

The six is worth spelling out, because it sounds like an exaggeration and is not. Under a structure with one type per layer, a payment method is not one thing — it is the same idea restated at every boundary it crosses:

```csharp
// 1. the wire shape
public record PaymentMethodDto(string Kind, string Token);

// 2. the persisted shape
public class PaymentMethodEntity { public string Kind {get;set;} ... }

// 3. translation between them, in both directions
public static class PaymentMethodMapper {
    public static PaymentMethodDto ToDto(PaymentMethodEntity e) => ...
    public static PaymentMethodEntity ToEntity(PaymentMethodDto d) => ...
}

// 4. the operation
public interface IPaymentService { Task<Receipt> Charge(PaymentMethodDto m); }

// 5. storage
public interface IPaymentRepository { Task Save(PaymentMethodEntity e); }

// 6. the endpoint
[HttpPost] public Task<IActionResult> Pay(PaymentMethodDto m) => ...
```

Adding *direct debit* means a new case, or a new field, in each of the six — and the mapper twice, once per direction. None of the six decides anything about direct debit that the others do not already know.

That is not evidence of a careless team. It is a structure whose boundaries do not line up with the way change actually arrives, so every change crosses all of them. Chapter 05 owns why fan-in sets the price of a change; chapter 18 owns what these particular boundaries cost.

**What changes with the Force:** whether structure that makes adding cheap is worth having. Frequency alone does not decide it — a thing that changes monthly in one file needs nothing.

### Team size and turnover

> **How many people must agree to change this, and how many of today's people will still be here in two years?**

Turnover is the half that gets dropped, and it is the sharper one. A rule that lives in one person's head is free while they are there and worth nothing the week after they leave.

```go
// Two authors, both here since the first commit. A comment is enough:
// the reviewer is the other author, and both remember the argument.
// Amounts are minor units. Never build one of these from a float.
type Money struct {
	Amount   int64
	Currency string
}
```

```go
// Twenty developers, a third of them new this year. A comment is no
// longer protection — it is a hope that everyone reads it.
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

The same operation — fetching a user's record — under three different budgets:

```python
# A web page render with 200 ms latency budget. A database round trip is one percent
# of it. Spend the round trip and think about something else.
user = db.query("select * from users where id = %s", uid)
```

```go
// An ad auction with a 5 ms budget: a bid must be returned before the
// page finishes loading, or the slot is sold to someone else. A round
// trip now eats most of the budget, so the design question changes from
// "how do I fetch this" to "how stale is this allowed to be."
if u, ok := cache.Get(uid); ok {
	return u
}
```

```c
/* An exchange order matcher with a 200 microsecond budget — 200
   millionths of a second, about the time a single main-memory read
   takes. There is no lookup at all. The data is already resident and
   indexed by id, and the memory layout is the design. */
user_t *u = &users[uid];
```

**What changes with the Force:** what you are able to spend on abstraction. At 200 milliseconds an interface, a copy, and an allocation are all invisible against a database round trip, so buy them. At 200 microseconds those same three cost a measurable share of everything you have, and the code stops looking like the code in books — not because its authors are cleverer, but because they cannot afford what you can. Chapter 08 owns the arithmetic underneath this; chapter 05's entity-component case is this Force pushed to its end.

### Control of the callers

> **Can I change every call site myself, and would I know if I broke one?**

Three intensities, and the middle one is where most working systems actually sit:

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

### The seven Forces, as questions

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

## Why the claim holds

Three mechanisms support this chapter's claim. The third is the one that catches working teams out, because it operates without anyone touching the code.

**A Force that is not evaluated is just a mood.** "It needs to scale" cannot be verified, argued with, or revisited, because it names no Force and gives no intensity. "Twelve thousand requests a minute at peak, of which about thirty are writes to the same row" reads two of them: the concurrency intensity is the thirty colliding writes, not the twelve thousand requests, and the latency budget is whatever is left of a page render after the other work. Both can be looked up, both can be wrong, and both can be checked again next year. Evaluation converts a mood into a claim, and claims can be tested.

**Forces are where the disagreement actually lives.** Chapter 02 records this as a failure symptom; the mechanism is that two people arguing about a Principle have usually already agreed about the Principle and are differing about the situation it is conditioned on. Stating the Force ends the argument or relocates it to something answerable.

**Forces move on a different clock than code.** This is the part that does real damage. A team doubles. A service acquires a second client, then a client outside the company. A table crosses a hundred million rows. A batch job is called from a request handler for the first time. None of those are code changes, none show up in a diff, and every one of them can invalidate a Principle that was correctly derived years earlier. The code that was right is now wrong, and nothing in the repository records why it was ever right, arrived at without anyone making a mistake.

---

## Where the claim doesn't apply

### Forces you cannot measure yet

The hard case, and the common one.

A product three months old. You do not know peak traffic, or the team size in a year, or whether this schema survives contact with real customers. Every question in the table above returns *don't know*, and the chapter's method appears to have nothing to say.

The tempting move is to guess high. It feels like prudence: assume growth, shard the database, split the services, put an event bus in early. It is the most expensive mistake available, because every one of those costs is paid immediately and in full, while the benefit arrives only in the branch of the future where you got big, and got big in the particular shape you guessed. The machinery also makes that branch less likely, because carrying it slows you down.

The rule that works is not "defer everything," and it is not "assume the worst" either. Two questions decide it, in order.

> **Does waiting spoil this decision?** If delay lets state pile up that the decision would have prevented, the decision expires — it will not be available later on the same terms.
> **Is this decision cheap to take today?** If it expires and it is cheap, take it now. If it expires and it is expensive, you are making a bet, and should say so.

These two questions yield three cases:

**1) The decision does not expire, so defer it.** Nothing accumulates while you wait, so the option is worth exactly as much next year. A performance index is the clean example — adding one later is routine work, and the data was never an obstacle, because the rows are not *wrong*, they are merely unindexed.

FlowCore — a Go workflow library backed by Postgres, and this book's running example — records a design decision of this shape. Go's convention for hiding a package from outside consumers is to place it under a directory named `internal/`, which the compiler enforces. The library was written as a single flat package instead, and the decision log says why the wall was not built up front:

> `internal/` can be introduced later if a second package genuinely needs to share machinery.

Nothing degrades in the meantime. On the day a second package appears, the directory is created and the imports are updated — the same work it would have been on day one.

**2) The decision expires and is cheap, so take it now.** This is where "stay flexible" gives exactly the wrong answer. From the same log, on whether to declare a database constraint that forbids duplicate rows before anyone has created one:

> Dropping a unique index later is trivial; adding one after clients hold duplicate rows is not.

Read that as an asymmetry rather than a prediction. Ship the constraint and discover it is too strict: one `drop index`, and the data was never harmed. Skip it and discover you needed it: the table now contains duplicates that the constraint refuses to accept, so before you can add it you need a migration, a policy for which duplicate survives, and a conversation with every client whose data you are about to change. **The constraint costs one line today and can become impossible tomorrow**, and that is true whether or not duplicates seemed likely.

The general form is uncomfortable and worth stating plainly: **under uncertainty, prefer the decision you can walk back — which is usually the stricter one.** Strictness is the direction that can be relaxed. Permissiveness is the direction that accumulates facts you then have to live with.

**3) The decision expires and is expensive, so you are making a bet.** Sharding is the standard case. Waiting genuinely does make it worse, because every month adds data to move — so the first question says act. But it is ruinous to do early, so the second question says wait, and the two do not resolve.

This is the only place where *how likely is this need* earns a vote, and it earns one because the decision is a forecast whether or not you admit it. What usually beats taking the bet is buying an option instead of the machinery: keep the code from assuming a single node — no cross-shard joins written into queries, no autoincrement keys assumed globally unique — without splitting anything. That costs little now and keeps the expensive decision cheap to make later, which converts a case-three problem into a case-one problem.

### A Force with no design consequence

If both ends of the dial produce the same code, the Force is not live here and naming it is overhead.

The dial that matters is the range the Force can plausibly take **in your situation**, not the range it takes across all software. When that range is a single point, there is nothing to read.

A build script runs once, on one machine, invoked by one person or one CI job. Concurrency is a fact about it — there is exactly one writer — but it is not a Force acting on the design, because the intensity cannot move. Imagining a version with a hundred concurrent writers does not help: that is a different program with a different purpose, not this one at a different setting.

So the test is: **name the intensities this thing could plausibly have within its own lifetime, and write the design for each.** If there is only one intensity, the Force is inert here. If there are several and they produce the same design, the Force is live but not binding on this decision. Either way, stop.

### Things that are risk, not unmeasured Forces

*Will this product exist in two years?* is not a measurement you are deferring. There is no instrument. Treating it as a Force to be estimated harder produces a number with no content, and then decisions get justified by it.

The difference shows up in what you can do about it. An unmeasured Force has an instrument: you do not know the write concurrency yet, but you could log it, or wait a quarter and count. A risk has none, and no amount of thinking produces one.

Concretely, two decisions that look alike:

```go
// Decision A. "How many merchants will we have?" — unmeasured, and
// measurable. Today it is 40. The question is whether to build sharding.
// You can defer this and watch the number.

// Decision B. "Will this product still exist in two years?" — no
// instrument exists. Any number you write down is invented.
```

For A, deferral is a plan: the trigger is a count you can watch, and the cost of being wrong is bounded by how fast the number can move.

For B there is nothing to defer *to*. So the response is not a better estimate but a different question — what does this decision cost me if the product is cancelled in eighteen months? A schema designed for a scale that never arrives is money spent. A schema that is merely simple costs nothing extra if the product dies and is cheap to extend if it lives.

That is the reversibility question again, and it is the only one that still works when the instruments run out.

---

## What the claim costs

**Naming a Force, without evaluating it, licenses machinery.** "We have concurrency" becomes a distributed lock, in a program with one writer. This is the failure mode the chapter's claim is aimed at: identifying a Force is the cheap half and feels like the whole job, so the design gets chosen from the name while the intensity is never read — and the intensity is almost always lower than the name suggests. The discipline: no Force may be cited in a design discussion without a number beside it, or the words *we don't know* said out loud.

**Half of these are estimates about the future wearing a measurement's clothes.** Team size in two years. Change frequency of a feature that does not exist yet. Peak traffic for a product with no users. Concurrency and latency can be measured today; the rest are forecasts, and should be labelled as such wherever they are written down.

**A written force-map goes stale, and a stale one is worse than none**, because it looks authoritative and nobody re-derives what a document already answers. Date them, and treat an undated one as unsigned.

**This chapter does not resolve conflicts.** Low latency pulls against durability. A small team pulls against a large blast radius. Naming both does not tell you which wins, and the honest answer is that trade-offs are decided rather than computed. Chapter 19 works through what to do when Forces point in opposite directions.

---

## How to recognize the failure

**In a codebase:**

- **Retry with exponential backoff around a call to a function in the same binary.** A distribution Force imported wholesale from somewhere it was real. Read the intensity and there is nothing to retry: an in-process call does not suffer packet loss or a slow node, so a failure is a bug in your own code and calling it three times more slowly just delays the report by six seconds.
- **A read-modify-write in a request handler.** A concurrency Force present and unread, and the symptom is silent data loss: two requests read the same value, both write, and the second overwrites the first with no error anywhere (Ch. 06).
- **Retry logic with no idempotency key.** Half of a Force read: the failure was anticipated, the redelivery it causes was not (Ch. 07).
- **A `not null default` in a migration** that quietly asserts something false about every row that predates it. The durability Force went unread: the author was thinking about the code, where a zero value is a harmless placeholder, and not about the rows, where it is a claim that this never happened — permanently indistinguishable from a claim that nobody recorded it.
- **A cache with no invalidation rule.** The latency Force was read and the change-frequency Force was not, so the design answers one question and ignores the one that decides whether it is correct.
- **An invariant enforced by a comment, in a codebase with forty contributors** and a third of them new this year.
- **Interfaces, queues, and feature flags added for a shape of scale that has not arrived** — and no note anywhere saying what would have to become true for them to be needed.

**"High scale" names no intensity and no design**, which is why the word *shape* is in that last bullet: a steady million requests an hour, an idle service that takes a million in one minute twice a day, and a modest request rate over a hundred terabytes are three different situations that share a vocabulary and share almost no design decisions. Machinery built for one shape is dead weight under the others, which is why "we built it for scale" is compatible with falling over on the first real load.

**In a conversation:**

- **"It needs to scale."** With no number attached, this is not a Force, it is a mood.
- **"That's not how it's done"** — where the reason, when you dig, turns out to be a Force that held at the speaker's last job and has not been checked against this one.
- **A design defended by a Force nobody has measured in a year.** Team size, traffic, and client count all move without a commit.
- **"Just in case"** doing the work that a measurement should be doing.

Chapter 02 already showed the sharpest version of this as a symptom of the model being misused: two people making increasingly detailed arguments while disagreeing about a Force neither has stated. The remedy is small and almost never applied — stop arguing about the Principle and ask each side what they believe about the situation.

---

**Next:** chapter 04 turns to Laws, and to the fact that they do not all have the same standing — a proven theorem, a near-tautology, and an empirical regularity are three different kinds of true.
