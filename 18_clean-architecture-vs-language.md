# Clean Architecture Versus the Language

## The claim

**"The database is a detail" does not say what to do about it. Read as an instruction to put persistence behind a directory wall, that costs nothing in Python, nothing in C# until assemblies split, and in Go it publishes the helpers the wall was drawn to hide — then charges a mapping layer for every entity the two sides can no longer share.**

This is Part IV's third case. The term with no fixed extent is **detail**, and the wide reading turns a rule about which way dependencies point into a rule about where files go.

---

## The demonstration

### The wall publishes what it was meant to hide

Here is an order lookup in one Go package. `scanOrder` maps a row into an `Order`, and nothing outside these lines should need it, so it is lowercase — in Go, an identifier beginning with a lowercase letter is visible only inside its own package:

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

The helper is private, no caller can reach it, and no discipline is needed to keep it that way. The compiler holds it.

Now apply the layout. Persistence is its own concern, so it moves to `store/`, and the service layer imports it. The service also has a row of its own to turn into an `Order`:

```go
direct := store.scanOrder(8, "closed")
```

```text
./service.go:14:18: undefined: store.scanOrder
```

In Go a package boundary *is* the visibility boundary, so the only way to compile that is to rename the helper `ScanOrder`. It compiles. And this is what the package now advertises:

```text
package store // import "shop/store"

type Order struct{ ... }
    func Get(id int) (Order, error)
    func ScanOrder(id int, status string) Order
```

**The helper was private until it was put behind a wall.** Splitting the code to hide persistence is what published its internals, and an exported identifier is a commitment (Ch. 05) — so the split converted something nobody could reach into something the package now promises.

### What `internal/` is actually for

The usual reply is that Go has a mechanism for this, and it does: a package under `internal/` cannot be imported from outside its module. FlowCore's decision 1 considered exactly that placement and rejected it, and the reasoning is the point:

> In Go, privacy comes from identifier case, not directory. A lowercase type in the root package is exactly as unreachable to a client as one under `internal/`.

So `internal/` is not the tool for hiding a type from clients — lowercase already does that, for free, with no directory at all. What `internal/` solves is narrower and specific:

> `internal/` solves a narrower problem — hiding a package when several packages must call each other by exported name — which a single-package module doesn't have.

Which is worth stating plainly, because it inverts how the directory is usually reached for. **`internal/` is not what you use to get privacy. It is what you use to get some of it back after a split has already taken it away.** Reaching for it is a signal that the wall was drawn somewhere the language charges for.

### The mapping tax

The export is the visible cost. The larger one is what the two sides can no longer share.

Once `store` and the service are separate packages, an entity type has to be *somewhere*. If it lives in `store`, then the service's public API is returning types owned by the persistence layer, which is the coupling the split was meant to remove. If each side owns its own, there are two of them, and something has to convert:

```go
// store/order.go
type Order struct {
	ID     int
	Status string
}

// domain/order.go — the same five fields, again
type Order struct {
	ID     int
	Status string
}

func fromStore(row store.Order) Order {
	return Order{ID: row.ID, Status: row.Status}
}
```

FlowCore's decision 1 names this as the reason it kept one package:

> Splitting store from façade across a package boundary would force two representations of each entity and a mapping layer between them: the exact duplication-and-drift the owner was worried about.

The tax is charged per field, per entity, per boundary crossed, and it is invisible in review because every individual mapping function is trivial. It is also where drift lives: add a column, and nothing fails to compile until you reach the second definition, if you reach it at all.

### The same layout costs three amounts

Everything above is Go's bill. It is not the bill in the languages the doctrine is usually taught in, and that is this chapter's title in one table.

```text
 language   what a directory is        what hiding is tied to
 --------   ------------------------   ----------------------
 Go         a package                  the package
 C#         no access meaning          the assembly
 Python     a module or subpackage     nothing enforced
```

In C#, folders carry no access meaning at all. `internal` is scoped to the assembly, so twelve layer folders cost nothing — until someone splits the layers into separate projects, at which point Go's bill arrives in full and for the same reason. In Python there is no enforcement to lose: a leading underscore is a request, so the layout costs a directory listing.

So *put each layer in its own folder* is an instruction whose price runs from nothing to a published API and a mapping layer, decided entirely by a language the instruction never names. That is chapter 13's finding in a different domain — advice that is really a claim about a pair, the design and the language, delivered as though it were a claim about the design.

---

## Why the claim holds

*Detail* is a relational word with the relation left out. Something is a detail *relative to* some decision, and the slogan never says which. With nothing to narrow it, the widest reading is the only one available, and the widest reading of *the database is a detail* is that persistence should be invisible from everywhere — which sounds like a statement about visibility and gets implemented as a statement about file paths.

Chapter 05 already separates the two ideas that get merged here: a layer is a constraint on which way dependencies point, and a directory is neither necessary nor sufficient for it. What this chapter adds is the price of confusing them, and in Go the price has a compiler message attached.

The confusion survives because **the mechanism that enforces hiding is not the mechanism that draws the picture.** A folder tree is the architecture as drawn — it can be shown in a slide, reviewed in a pull request, and checked by looking. Whether anything is actually hidden depends on what the language attaches to a directory, which is invisible in the diagram and different in every language the diagram gets used in.

And the failure runs one way. Nobody splits a package and discovers they have accidentally hidden something; the split can only publish. Go's compiler at least announces it, which makes Go the language where the bill is easiest to see rather than the language where it is highest.

---

## Where the claim doesn't apply

### A compiler-enforced boundary across a large team

The argument above assumes the wall bought nothing. On a large codebase with many contributors it buys something a convention cannot: an import that will not compile is a rule nobody can violate under deadline, and no amount of review discipline is equivalent.

FlowCore states its own condition for going the other way, and it is a size condition:

> For a library this size with one author and a reviewer, that's cheaper than the mapping tax a wall would charge.

That is the trade, and it is a real one. Enforced boundaries cost exported surface and mapping code; conventions cost vigilance that scales with headcount. Chapter 09's Conway material says the seams will land where the teams are regardless, so a wall between two teams is describing something that already exists, while a wall between two files in one person's repository is inventing a rule to obey.

### The wall was drawn for a different reason

Splitting a package to break a dependency cycle is chapter 05's third option, and it works — the cycle is gone whatever the export cost. The same goes for a package that exists to be a published API, or to be compiled separately, or to carry a different licence.

The claim here is about walls drawn *to hide*, which is the reason usually given and the one the language may not honour. A wall drawn for any other reason should be priced on that reason instead.

### Languages that charge nothing

In Python the entire argument evaporates, because nothing was being enforced in the first place. The layout is then a filing decision, and filing decisions are worth making well — chapter 10's point that directories group by change while names group by shape still applies. There is simply no hidden bill, because there is no mechanism to trigger it.

---

## What the claim costs

**One package gets big.** FlowCore's answer moves the discipline from the compiler to the author, and says so:

> Discipline moves from the compiler to the author: nothing stops code reaching into the store directly, since there's no package wall.

That is a real cost and it grows with the number of people who could do the reaching.

**You lose the map.** A folder tree is a genuinely useful orientation device for someone arriving at a codebase, and a single package with forty files is worse at that, whatever it saves in exports. The alternative is naming conventions and file organisation inside the package, which nothing enforces and everyone must agree to.

**Arguing it costs more than holding it.** The doctrine arrives with books, diagrams, and a name. This arrives with a compile error. In a design review the honest move is usually to price the specific split in front of you — what does this wall publish, and what will it charge in mapping — rather than to take on the architecture.

---

## How to recognize the failure

**In a codebase:**

- **Exported identifiers whose doc comments say they are internal.** The export was forced by a layout, and the comment is where somebody noticed and settled for a note.
- **Two structurally identical types with a function between them.** `store.Order` → `domain.Order`, same fields, plus `fromStore`. Multiply by entities and by boundaries; that product is the mapping tax.
- **`internal/` introduced after a split rather than before one.** It is the compiler being asked to give back what the directory took.
- **A package whose exported surface is larger than its useful API.** Compare what `go doc` prints with what a caller actually calls.
- **A field added in one representation and not the other**, found at run time. This is the drift the tax was quietly accruing.

**In a conversation:**

- **"Persistence should be its own package."** The question that separates the two cases: what becomes public if we do that, and what will we have to map?
- **"The database is a detail."** A detail relative to which decision? Most systems keep their constraints in the schema (Ch. 17), and those are not details in any sense that licenses hiding them.
- **"That's just how you structure a project."** Followed usefully by: in which language was that structure invented, and what did a directory mean there?
- **"We'll put it in `internal/`."** Fine, and worth asking what it is being hidden from — a client, or another package you created a moment ago.

The question that does the work: **what does this directory boundary enforce that identifier naming does not?**

In Go, for a single module, the honest answer is often nothing, and the split is then paid for in exports and mapping with no compiler guarantee bought. In C# it is nothing until the assemblies split. In Python it is nothing at all. Where the answer is *an import that cannot compile, across teams that have to be kept apart*, the wall is doing work and the bill is worth paying.

---

## Sources

- Go, exported identifiers — [go.dev/ref/spec#Exported_identifiers](https://go.dev/ref/spec#Exported_identifiers); `internal` packages — [go.dev/doc/go1.4#internalpackages](https://go.dev/doc/go1.4#internalpackages).
- C#, access modifiers — [learn.microsoft.com/dotnet/csharp/language-reference/keywords/access-modifiers](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/access-modifiers).
- FlowCore, `docs/decisions.md`, decision 1 — [github.com/ilke-akdeniz/flowcore](https://github.com/ilke-akdeniz/flowcore).

---

**Next:** chapter 19 takes the other half of the doctrine — the interface at the boundary, bought against a database swap that has not been scheduled, and shaped by the database it was meant to insure you against.
