[claude Placing "depend on abstractions" and "database is a detail" idea unders chapter 18 didn't work. They are different ideas, not much ties both together and "the database is a detail" does not fit chapter's 18's main idea. I recommend taking the "database is a detail" out of chapter 18 and putting it into somewhere else, new chapter or existing chapter, but only if it fits to an existing chapter. I don't want the same mistake to happen again, artifically binding two claims with "and" and hoping that it works out. Don't blindly follow my recommendations, understand them but use your own judgment as well. Also a new alternative you can consider, if an idea-claim is good and it fits in a chapter with already claim in it, you can consider having two claim in the chapter. Ex: "Chapter A title: Umbrealla Idea - Claim - Category.  Claim A, Claim B both claims supporting the Umbrella"]
# Clean Architecture Versus the Language

## The claim

**Neither *depend on abstractions, not concretions* nor *the database is a detail* says what counts as one. Under the wide reading of both, the directory wall meant to hide a layer's helpers is what forces them to be published, and the interface bought as insurance against changing the database cannot pay out when the change arrives, because it was shaped by the database it was insuring against.**

This is Part IV's third case. The terms with no fixed extent are **abstraction** and **detail**, and the wide reading of them produces two artifacts that arrive together: a folder per layer, and an interface at every boundary.

---

## The demonstration

### The wall publishes what it was meant to hide

Here is an order lookup, in one Go package. `scanOrder` maps a row into an `Order`, and nothing outside this file should need it, so it is lowercase — in Go, an identifier starting with a lowercase letter is visible only inside its own package:

```go
func scanOrder(id int, status string) Order {
	return Order{ID: id, Status: status}
}

func getOrder(id int) (Order, error) {
	if id <= 0 {
		return Order{}, fmt.Errorf("no such order: %d", id)
	}
	return scanOrder(id, "open"), nil
}
```

The helper is private, the caller cannot reach it, and no discipline is required to keep it that way. The compiler holds it.

Now apply the layout. Persistence is its own concern, so it goes in its own package, `store/`, and the service layer imports it. The service also needs to build an `Order` from a row it fetched itself:

```go
direct := store.scanOrder(8, "closed")
```

```text
./service.go:14:18: undefined: store.scanOrder
```

In Go a package boundary *is* the visibility boundary, so the only way to make that compile is to rename the helper `ScanOrder`. It compiles. And here is what the package now advertises:

```text
package store // import "shop/store"

type Order struct{ ... }
    func Get(id int) (Order, error)
    func ScanOrder(id int, status string) Order
```

**The helper was private until it was put behind a wall.** Splitting the code to hide persistence is what published its internals — and an exported identifier is a commitment (Ch. 05), so the wall converted a detail nobody could reach into a promise the package now keeps.

That is not an argument against packages. It is the bill for one particular reason to draw them, and the reason usually given — *this layer should be sealed off* — is the one that produces the opposite result.

### The same layout costs three different amounts

The bill above is Go's. It is not the same in the languages the doctrine is usually taught in, and this is the chapter's title in one paragraph.

```text
 language   what a directory means      what hiding is tied to
 --------   -------------------------   -----------------------
 Go         a package                   the package
 C#         nothing in particular       the assembly
 Python     a module or subpackage      nothing enforced
```

In C#, folders carry no access meaning at all. `internal` is scoped to the assembly, so you can arrange twelve layer folders and pay nothing — until someone splits the layers into separate projects, at which point the Go bill arrives in full. In Python there is no enforcement to lose: a leading underscore is a request, so the layout costs a directory listing and nothing else.

So *put each layer in its own folder* is an instruction whose price runs from zero to a published API depending on a language the instruction never names. That is chapter 13's finding in a different domain — a piece of advice that is a claim about a pair, the design and the language, stated as though it were a claim about the design.

### Injection is not abstraction

Before the second half, a distinction the argument fails without, because chapter 05 otherwise refutes it in a sentence.

Two decisions get bundled under one word:

1. **Is the dependency passed in, or does the component construct it?**
2. **Is it passed in behind an interface, or as a concrete type?**

Chapter 05 argues for the first, and for a reason that has nothing to do with swapping anything: a component reaching for `os.Getenv("DATABASE_URL")` is holding decisions that were never its to make. That argument stands.

But the two are separable, and separating them is the whole point:

```go
func NewOrders(database *sql.DB) *Orders   // injected, concrete
func NewOrders(database Repository) *Orders // injected, abstract
```

The first is fully injected. The composition root decides which database, the component is testable, nothing is reached for. What the second adds is the interface, and only that addition is what the rest of this chapter is about.

### Two implementations at once, or one after another

The interface is nearly always justified by the same sentence: *we might need to switch databases.* That sentence describes one of two different situations, and only one of them is a Force.

- **Simultaneous plurality.** Two implementations exist at the same time and something chooses between them at run time. Tenant A on Oracle, tenant B on SQL Server. A vendor shipping on-premises software onto whatever the customer already runs. Here the interface is *exercised*: both implementations load, and dispatch is a real decision.
- **Sequential replacement.** SQL Server today, Postgres forever after. At every moment there is exactly one implementation. The interface is never exercised as an interface. It is a shape the code is held in, not a decision anything makes.

*We need to support two databases* is the first. *We might need to switch databases* is the second, and it is the one that gets said.

**Everything below is about the second.** The distinction is this book's own, and it is not standard vocabulary — but the machinery is identical in both cases, which is why the argument for it survives so easily.

### Why the insurance cannot pay out

Four reasons, and none of them is *you will not need it*. Assume you do.

**The abstraction was shaped by the thing it was insuring against.** A repository interface written over Postgres encodes Postgres — its transaction semantics, its isolation levels, its type mapping, its error taxonomy. That is Hyrum's Law (Ch. 05) operating on an interface you own: what leaked through became part of the contract, and it leaked from the engine you were planning to replace.

**The swap is a data problem; the abstraction is in the code layer.** Chapter 09's rate layers put the schema below the code, changing more slowly. The interface sits in the fast layer. What actually has to move — rows, types, constraints, indexes, the queries the planner was tuned for — sits in the slow one. The insurance is filed in the wrong layer to cover the loss.

**Staying swappable costs you the engine you are running.** Keeping the interface honest means restricting yourself to what every candidate supports: no `jsonb`, no partial indexes, no advisory locks, no `on conflict`. That premium is paid every day, in features you have already bought and cannot use.

**If the swap comes, it comes for a reason the abstraction defeats.** Nobody changes engines for entertainment. They change for different scaling, different consistency, or a different invoice — and a lowest-common-denominator interface is precisely what prevents using the thing they moved for.

Which gives the inversion worth keeping: **the more thoroughly you abstract for portability, the less portability is worth to you.**

### The rollback objection

*We need to be able to switch back quickly.* This is the strongest form of the argument, and answering it requires naming what actually does the job, because the reply is not *you won't need to roll back.*

The rollback mechanism for an engine migration is operational rather than architectural:

- Logical replication or change data capture into the new engine, running for weeks before anything is cut over.
- Both engines serving reads, results compared, until the diff is empty.
- Cutting over per-tenant or per-route rather than all at once — chapter 12's strangler fig.
- Keeping the old engine running and receiving writes for a defined window.

You roll back by pointing at a database that is still there and still current. A repository interface enables none of that, and none of it can usefully be built in advance, because all of it is specific to the pair of engines and the shape of the data on the day.

That is chapter 03's reversibility rule doing its work: the job is cheap at migration time and expensive speculatively, so deferring it is a plan rather than a bet.

---

## Why the claim holds

*Abstraction* and *detail* are both relational words with the relation left out. Something is an abstraction *of* something, and a detail *relative to* some decision — and neither slogan supplies the second half. Chapter 15's mechanism applies unchanged: with nothing to narrow the reading, the widest one is the only one available, and the widest reading of *the database is a detail* is that the database should be invisible from everywhere.

Two things follow, and they are the two artifacts.

**The interface at every boundary** comes from reading *depend on abstractions* as a rule about syntax rather than about stability. Chapter 05's version is narrower and checkable: put what changes least at the bottom. An interface is not automatically the thing that changes least — a repository interface over an evolving schema changes every time the schema does, and it changes in two files instead of one.

**The folder per layer** comes from reading a rule about call direction as a rule about file location. Chapter 05 already separates those: a layer is a constraint on which way dependencies point, and a directory is neither necessary nor sufficient for it. What this chapter adds is the price of confusing them, and in Go that price is an export.

The reason the doctrine is hard to argue with is that both artifacts are *visible* and the thing they were meant to buy is not. A folder tree can be shown in a slide. An interface count can be pointed at in review. Whether the system could actually change engines cannot be demonstrated until the day it has to, and by then whoever chose the layout has usually moved on.

---

## Where the claim doesn't apply

### Portability is a contract term

If you sell software that customers install against their own database, supporting three engines is something you have promised, not something you are guessing about. That is simultaneous plurality, the interface is exercised, and it is load-bearing.

The Force is chapter 03's *control of the callers*, pointed at the substrate instead: you do not control the environment your code runs in. Everything in this chapter assumes you do — that there is one production database and you are the one who picks it.

### The migration is funded and dated

Once the move is decided, scheduled, and staffed, the abstraction stops being speculative. It may still be the wrong tool — the rollback section applies unchanged — but the objection has changed from *this will never happen* to *this is not how to do it*, and those need different arguments.

### A compiler-enforced boundary across a large team

The export bill above assumes the wall bought nothing. On a large codebase with many teams, it buys something a convention cannot: an import that will not compile is a rule nobody can violate in a hurry on a Friday, and chapter 09's Conway material says the seams will land somewhere regardless.

The trade is real and it runs both ways. You get an enforced boundary and you pay for it in exported surface, and the balance depends on how many people could cross the line and how likely they are to. For three people in one repository the wall prevents something nobody was going to do.

### One implementation is not the same as speculative

The claim here is about interfaces justified by a future substitution, not about interfaces. Chapter 05 owns the legitimate uses, and they are common: narrowing what a consumer can reach, breaking a cycle, declaring a seam whose shape the consumer owns. Any of those can be right with exactly one implementation and no plan for a second.

### Tests are a second implementation

The honest reason most repository interfaces exist is not a future database. It is that the test suite needs something the production code does not — and Postgres in production with a fake in tests *is* simultaneous plurality, which is the case this chapter concedes.

Chapter 17 owns that argument and answers it differently: test against the real database, and the doubles that remain are for dependencies you cannot run. This chapter does not re-open it. But if you reject 17's position, the interface has a justification that has nothing to do with insurance, and the rest of this chapter does not reach it.

---

## What the claim costs

**Concrete types in signatures spread.** `func NewOrders(database *sql.DB)` names a library in the constructor of something that is not about that library, and every component doing the same makes the dependency visible everywhere. That is the honest cost, and it is the thing the interface was hiding. Chapter 05's question decides whether it matters: how many things break when it changes.

**You lose a seam you might have wanted for something else.** The interface you did not write for the database swap was also the interface you did not have when you wanted to add caching, or metrics, or a read replica. Those are real uses and they are 05's, not this chapter's — but the abstraction is now a change rather than a configuration.

**Deciding takes knowledge the moment does not supply.** *Is this plurality or replacement* is answerable, but it needs someone to say what the product actually promises customers, and that person is often not in the room when the layout is chosen.

**Arguing this position costs more than holding it.** The doctrine has books, diagrams, and a name; this has a compile error and an argument. Being right is not the same as being able to win a design review in ten minutes, and the honest move is usually to price the specific interface in front of you rather than to take on the architecture.

---

## How to recognize the failure

**In a codebase:**

- **An interface with exactly one implementation, and a name that is the implementation's name with a prefix or suffix.** `IOrderRepository` / `OrderRepository`, `Store` / `PostgresStore`. When the abstraction and the concretion can only be told apart by an affix, no decision was made about what to hide.
- **Exported identifiers whose doc comments say they are internal.** The export was forced by a layout, and the comment is where somebody noticed.
- **A mapping function per boundary crossing, converting a type into a structurally identical type.** `store.Order` → `domain.Order` → `api.Order`, with the same five fields. The tax is paid per field per boundary and it is invisible in review because each function is trivial.
- **The interface changes in the same commit as the schema, every time.** Then it is not insulating the code from the database; it is a second file that has to agree with it.
- **`internal/` used to undo a split.** Reaching for it is the compiler telling you the boundary was drawn in the wrong place — worth reading as a signal rather than a fix.

**In a conversation:**

- **"We might need to switch databases."** The question that separates the two cases: *would two of them ever be running at once?*
- **"The database is a detail."** A detail relative to which decision? The schema is where most systems keep their constraints (Ch. 17), and those are not details in any sense the sentence supports.
- **"It's just an interface, it's cheap."** The interface is cheap. The lowest-common-denominator feature set it commits you to is not, and that is the part nobody prices.
- **"This way we're not coupled to Postgres."** Ask what the code does when a query needs `on conflict`.

The question that does the work: **if the swap happened next quarter, what would this interface save?**

Answer it concretely — name the migration steps, and mark which ones the abstraction touches. The usual answer is that it touches the smallest of them, and that the large ones were always going to be about data.

---

## Sources

- Go, package visibility and `go doc` — [go.dev/ref/spec#Exported_identifiers](https://go.dev/ref/spec#Exported_identifiers).
- C#, access modifiers and assemblies — [learn.microsoft.com/dotnet/csharp/language-reference/keywords/access-modifiers](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/access-modifiers).
- FlowCore, `docs/decisions.md`, decisions 1 and 10 — [github.com/ilke-akdeniz/flowcore](https://github.com/ilke-akdeniz/flowcore).

---

**Next:** Part V turns from diagnosis to method — chapter 19 sets out how to read the Forces in front of you, derive the Principles they support, and check the Idioms of the language you are actually writing in, in that order.
