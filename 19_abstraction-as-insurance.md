# Abstraction as Insurance

## The claim

**"Depend on abstractions, not concretions" does not say what the abstraction is insulating you from. Bought as insurance against a future database change, the interface cannot pay out when that change arrives — it was shaped by the database it was insuring against — and it charges a premium every day in features of the engine you are actually running.**
[claude after reading this claim again, the statement "does not say what the abstraction is insulating you from" bugged me. We are treating "Depend on abstractions, not concretions" as a slogan or go proverb with no scope attached, but I believe this one has known reacheaable scopes. I'm still behind the "abstraction as insurance" idea but maybe we should also look at the scope - shapes of "Depend on abstractions, not concretions". That could give better material for current or other chapters. I reached the following wikipedia page while doing that: https://en.wikipedia.org/wiki/Dependency_inversion_principle   Take a look at that page and tell me what you think, it could also be worthwhile to explore the material referenced in the wikipedia page in a BFS style.]

This is Part IV's fourth case, and the one that survives the reply that usually ends the argument: *but what if we do need it.* Assume you do need it. The claim is that the policy is void, not that the event never happens.

It is also not YAGNI. That says you paid for something you did not need. This says you paid, the event occurred, and the cover did not apply.

---

## The demonstration

### Two implementations at once, or one after another

Almost every repository interface is justified by the same sentence: *we might need to switch databases.* That sentence covers two different situations, and the machinery is only earned by one of them.

- **Simultaneous plurality.** Two implementations exist at the same time and something chooses between them while the program runs. Tenant A on Oracle, tenant B on SQL Server. A vendor shipping on-premises software onto whatever the customer already has. Here the interface is *exercised* — both implementations load, and dispatch is a real decision the program makes.
- **Sequential replacement.** SQL Server today, Postgres from next March, forever after. At every instant there is exactly one implementation. The interface is never exercised as an interface. It is a shape the code is held in, not a choice anything makes.

*We need to support two databases* is the first. *We might need to switch databases* is the second, and it is the one that gets said in the meeting.

**This distinction is the book's own and not standard vocabulary**, so it will not be found under these names elsewhere. Everything below concerns the second case. The two are easy to conflate because the code they produce is identical — the same interface, the same constructor, the same dependency arrow — and only the run-time behaviour differs, which nobody looks at.

### Injection is not abstraction

Before going further: a distinction without which chapter 05 refutes this chapter in one sentence.

Two decisions travel under one word, and they are separable:

1. **Is the dependency passed in, or does the component construct it?**
2. **Is it passed in behind an interface, or as a concrete type?**

Chapter 05 argues for the first, for a reason with nothing to do with substitution: a component reaching for `os.Getenv("DATABASE_URL")` is holding decisions that were never its to make. That argument stands and this chapter does not touch it.

```go
func NewOrders(database *sql.DB) *Orders     // injected, concrete
func NewOrders(database Repository) *Orders  // injected, abstract
```

The first is fully injected. The composition root chooses the database, the component reaches for nothing, and the wiring is explicit. What the second adds is the interface — and only that addition is what follows.

### The interface is shaped by the engine it was written against

Here is a repository interface, of the kind written to keep the database swappable:

```go
type Accounts interface {
	Get(ctx context.Context, id int64) (Account, error)
	// GetForUpdate locks the row until the surrounding transaction ends.
	GetForUpdate(ctx context.Context, id int64) (Account, error)
	Debit(ctx context.Context, id int64, amount int64) error
}
```

`GetForUpdate` is there because somewhere a balance is read and then written, and chapter 06 owns why that needs the row held still. Against Postgres it is one clause:

```sql
select balance from account where id = ? for update
```

Now try to satisfy the same interface with SQLite, which is the second implementation this design exists to permit:

```text
OperationalError: near "for": syntax error
```

SQLite has no row-level locking to offer, so `GetForUpdate` cannot be implemented — not implemented differently, not implemented slowly, but not implemented. The method is on the interface because Postgres has the feature. **The abstraction did not abstract over the engine; it published one of the engine's capabilities as a promise to its own callers.**

This is Hyrum's Law (Ch. 05) operating on an interface you own. What leaked through became part of the contract, and it leaked from the thing you were planning to replace. The same happens to error taxonomies, to isolation-level names that mean different things in different engines, to whether a returned id is populated before or after commit, and to every timeout whose value was tuned against one planner.

### The premium is paid daily

The way to keep the interface honest is to restrict yourself to what every candidate engine supports. That restriction is not free and it is not deferred: it is paid every day, in features of the database you are running right now.

It is also harder to compute than it looks. `for update` is unavailable in SQLite, so it is out. But `on conflict` — the clause usually named first when people list Postgres-specific things to avoid — runs perfectly well there:

```text
plain select           OK
select ... for update  OperationalError: near "for": syntax error
on conflict            OK
```

So the lowest common denominator is not a list anyone knows in advance. It is the intersection of the feature sets of engines you have not chosen, which means in practice it gets approximated by superstition — a team avoiding `jsonb`, partial indexes, advisory locks, and generated columns because those *sound* proprietary, while the actual boundary sits somewhere nobody has checked.

### The swap is a data problem and the abstraction is in the code layer

Chapter 09's rate layers put the schema below the code and moving more slowly. The interface lives in the fast layer. What has to move on migration day — rows, types, constraints, indexes, the queries a planner was tuned for, the operational runbook — lives in the slow one.

Counting what a repository interface covers in an engine migration is a short exercise. It covers the call sites. It does not cover the schema translation, the data copy, the verification, the cutover, or the rollback. The insurance was filed against the smallest line item on the invoice.

### If the swap comes, it comes for a reason the abstraction defeats

Nobody changes database engines for entertainment. They change for different scaling behaviour, different consistency guarantees, or a different bill — and each of those cashes out as *we need to use something the new engine can do*.

A lowest-common-denominator interface is precisely the thing standing between you and that capability. You arrive at the migration you prepared for, and the preparation is what prevents the migration paying off.

Which gives the inversion worth keeping: **the more thoroughly you abstract for portability, the less portability is worth to you.**

### The rollback objection

*We need to be able to switch back quickly.* This is the strongest version of the argument, and the answer is not *you will not need to roll back*. It is that the interface is not what gives you the ability.

Rollback for an engine migration is operational rather than architectural:

- Logical replication or change data capture into the new engine, running for weeks before anything moves.
- Both engines serving reads, results compared, until the diff is empty.
- Cutting over per-tenant or per-route rather than all at once — chapter 12's strangler fig.
- Keeping the old engine running and receiving writes for a defined window.

You roll back by pointing at a database that is still there and still current. A repository interface enables none of that, and none of it can usefully be built in advance, because every part of it is specific to the pair of engines and to the shape of the data on the day.

That is chapter 03's reversibility rule doing its work: this is cheap to do at migration time and expensive to do speculatively, so deferring it is a plan rather than a bet.

---

## Why the claim holds

*Abstraction* is a relational word with the relation left out. You abstract *over* a set of things that vary — and the slogan never says which set. With nothing to narrow it, the widest reading is available: abstract over everything that might ever vary, which includes a database nobody has chosen and features nobody has enumerated.

Chapter 05's version of the same advice is narrower and checkable: put what changes least at the bottom. An interface is not automatically the thing that changes least. A repository interface over an evolving schema changes every time the schema does, and now changes in two files rather than one.

**The mechanism that makes this hard to see is that the cost and the benefit arrive at different times, and only one of them ever arrives.** The premium is paid continuously, in small amounts, by people who do not know they are paying it — a query not written, a feature not used, a mapping function maintained. The payout is a single event, in the future, that mostly does not occur; and on the rare occasion it does, the payout fails for reasons that are only visible at that moment.

So the practice is never disconfirmed by experience. A team that abstracted and never migrated concludes the insurance was cheap. A team that abstracted and did migrate concludes the migration was hard, which it was, and rarely audits how much of the difficulty the abstraction removed.

---

## Where the claim doesn't apply

### Portability is a contract term

If you sell software customers install against their own database, supporting three engines is something you have promised. That is simultaneous plurality: the implementations both load, the dispatch is real, and the interface is exercised on every deployment.

The Force is chapter 03's *control of the callers* pointed at the substrate instead — you do not control the environment your code runs in. Everything above assumes you do, and that there is one production database whose name you chose.

Note what this boundary also buys: because the interface is exercised, the lowest-common-denominator restriction stops being a cost with no benefit and becomes the actual product requirement. You are not giving up `for update` speculatively. You are giving it up because a customer runs something that lacks it.

### The migration is funded and dated

Once the move is decided, scheduled, and staffed, the abstraction stops being speculative. It may still be the wrong tool — the rollback section applies unchanged — but the objection has moved from *this will never happen* to *this is not how to do it*, and those need different conversations.

### Tests are a second implementation

The honest reason most repository interfaces exist is not a future engine. It is that the test suite wants something the production code does not, and Postgres in production with a fake in tests *is* simultaneous plurality by the definition above.

Chapter 17 owns that argument and answers it: test against the real database, and reserve doubles for dependencies you cannot run. This chapter does not reopen it. But the dependency runs the other way — if you reject 17's position, the interface has a justification that has nothing to do with insurance, and none of this chapter reaches it.

### One implementation is not the same as speculative

The claim is about interfaces justified by a future substitution, not about interfaces. Chapter 05 owns the legitimate uses and they are common: narrowing what a consumer can reach, breaking a cycle, declaring a seam whose shape the consumer owns. Any of those can be right with exactly one implementation and no plan for a second — and the test is whether you can state the reason without using the word *later*.

---

## What the claim costs

**A library name appears in signatures that are not about that library.** `func NewOrders(database *sql.DB)` puts `database/sql` in the constructor of something that is about orders, and every component doing the same makes the dependency visible everywhere. That is the honest bill, and chapter 05's question prices it: how many things break when it changes.

**You give up a seam you might have wanted for something else.** The interface you did not write for the swap was also the one you did not have when you wanted caching, or metrics, or a read replica, or a second-level audit. Those are real uses, they are chapter 05's rather than this chapter's, and adding the seam later is a change rather than a configuration.

**Deciding needs information the moment does not supply.** *Is this plurality or replacement* is answerable, but answering it means knowing what the product promises customers, and the person who knows that is often not in the room when the layout is chosen.

**Being right does not make it arguable.** The doctrine has books, a diagram, and a name; this has a syntax error and an argument. In a design review the practical move is usually to price the specific interface in front of you — what does it forbid, and what did we give up to keep it honest — rather than to take on the architecture.

---

## How to recognize the failure

**In a codebase:**

- **An interface and its only implementation differ by an affix.** `IOrderRepository` / `OrderRepository`, `Store` / `PostgresStore`. When the two can only be told apart by a prefix, nobody decided what to hide; a shape was applied.
- **A method that names a capability rather than a need.** `GetForUpdate`, `Upsert`, `BulkCopy`. Each is an engine feature promoted to a contract, and each is a thing the second implementation must have.
- **The interface changes in the same commit as the schema, every time.** Then it is not insulating code from the database; it is a second file that must agree with the first.
- **A "we don't use that here" convention with no written reason.** Ask which engine the avoidance was protecting against, and whether anyone checked the feature is actually unsupported there.
- **A second implementation that exists only in tests.** That is chapter 17's subject, and it means the insurance framing was never the real reason.

**In a conversation:**

- **"We might need to switch databases."** The question that separates the cases: *would two of them ever be running at once?* If no, it is sequential replacement and the interface is a shape, not a decision.
- **"It's just an interface, it's cheap."** The interface is cheap. The feature set it commits you to is not, and that is the part nobody prices.
- **"This way we're not coupled to Postgres."** Ask what happens when a query needs `for update`.
- **"We'll swap it out later if we need to."** *Later* is the tell. An interface with a reason that survives deleting that word is one chapter 05 would defend.

The question that does the work: **if the swap happened next quarter, which of its steps would this interface remove?**

Answer it by listing the steps — schema translation, data copy, verification, cutover, rollback, retuning — and marking the ones the abstraction touches. The usual answer is the call sites, which were never the expensive part, and the usual reaction to seeing the list is more useful than any argument in this chapter.

---

## Sources

- SQLite, unsupported SQL — [sqlite.org/omitted.html](https://www.sqlite.org/omitted.html); upsert support — [sqlite.org/lang_upsert.html](https://www.sqlite.org/lang_upsert.html).
- PostgreSQL, `SELECT … FOR UPDATE` — [postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE](https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE).
- Go, `database/sql` — [pkg.go.dev/database/sql](https://pkg.go.dev/database/sql).

---

**Next:** Part V turns from diagnosis to method — chapter 20 sets out how to read the Forces in front of you, derive the Principles they support, and check the Idioms of the language you are writing in, in that order.
