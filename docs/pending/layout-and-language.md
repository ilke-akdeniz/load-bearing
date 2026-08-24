# A Directory Costs What the Language Ties to It

Working document, in the shape of the others in this folder.

**Owed to:** chapter 21, *Idioms: why ecosystems diverge*. One section, not a chapter.

**Origin.** This was a chapter — *Clean Architecture versus the language*, numbered 18 at the time and since cut, with everything after it moved up one. Do not read that number as the current chapter 18. Decision 83 records why: the chapter ran on *the database is a detail*, and the demonstration below does not follow from that advice. The export bill is a property of Go's package semantics and is paid identically whatever the motive for the split — which the chapter's own boundary section conceded.

**What survives, and why it belongs to 21.** A directory means a different thing in each ecosystem, so the same layout instruction costs a different amount in each. That is not an architecture finding wearing a language costume; it is the reverse, and *why ecosystems diverge* is the chapter for it.

**Everything here has been run.** The Go compile error and the `go doc` output are real. Nothing needs re-verifying, though re-running before publication would be cheap.

**Already stated elsewhere, so 21 must not re-derive it.** Chapter 05 carries the bill in one sentence at *Enforced boundaries cost more than unenforced ones* — package walls force exports and mapping code, worth paying at some team sizes — and again in its recognition list, as the same entity re-typed once per layer with mappers between. Chapter 05 also owns *layer ≠ directory*. What 21 adds is the per-language price, not the existence of a price.

**FlowCore's decision 1** is the source for the `internal/` reasoning and for the mapping tax as a reason not to split. Chapter 03 already uses the same decision for the reversibility rule, so 21's use must show a different facet: not *the decision can wait*, but *the wall costs a different amount depending on the language you are waiting in*.

---

## The wall publishes what it was meant to hide

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

## What `internal/` is actually for

The usual reply is that Go has a mechanism for this, and it does: a package under `internal/` cannot be imported from outside its module. FlowCore's decision 1 considered exactly that placement and rejected it, and the reasoning is the point:

> In Go, privacy comes from identifier case, not directory. A lowercase type in the root package is exactly as unreachable to a client as one under `internal/`.

So `internal/` is not the tool for hiding a type from clients — lowercase already does that, for free, with no directory at all. What `internal/` solves is narrower and specific:

> `internal/` solves a narrower problem — hiding a package when several packages must call each other by exported name — which a single-package module doesn't have.

Which is worth stating plainly, because it inverts how the directory is usually reached for. **`internal/` is not what you use to get privacy. It is what you use to get some of it back after a split has already taken it away.** Reaching for it is a signal that the wall was drawn somewhere the language charges for.

## The mapping tax

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

## The same layout costs three amounts

Everything above is Go's bill. It is not the bill in the languages the doctrine is usually taught in, and that is the finding in one table.

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
