# Layered Architecture

## The claim

**The term "layered architecture" can be used as a Law, a Principle or an Idiom. Most of the harm done in layering's name is the Idiom applied with the authority of the Law.**

## The three layering claims, separated

| Claim | Kind | Standing |
|---|---|---|
| **Acyclicity Law**: If A depends on B, then B must not depend on A — directly or through any chain | **Law** | true by definition ([Ch. 03](03_grading-a-law_q5c6.md)) |
| **Ranking Principle**: The parts can be stacked into layering ranks, each depending only on the rank beneath it | **Principle** | true when the graph is that shape, and often it isn't |
| **Three-Tier Idiom**: The ideal ranking, top to bottom, is `presentation → business → data`, and each rank becomes a physical boundary | **Idiom** | 1990s enterprise Java and C# |

The Ranking Principle is the one that needs stating carefully, because it has a loose reading and a strict one and only the strict one says anything new. Loosely — "dependencies should flow downward" — it is claim one with a picture attached.

The strict reading needs the word **rank**, so here it is precisely. A rank is a whole number attached to each part, assigned by the rules:

> - Parts that depend on nothing are the **bottom** rank, 1.
> - Every other part's rank is **the rank of the topmost part it depends on, plus 1**.

That is all a rank is. Not a folder, not a team, not a tier of importance — a number that falls out of the arrows. Run the rule on the graph from [chapter 04](04_dependency-and-hiding_agjy.md) and the numbers assign themselves:

```text
rank 3           main            depends on both below it
                ↙    ↘
rank 2    billing      reports   each depends only on money
                ↘    ↙
rank 1           money           depends on nothing
```

`money` depends on nothing, so it is rank 1. `billing` and `reports` each depend on it, so both are rank 2 — sharing a number because they are the same distance from the bottom, not because they have anything to do with each other. `main` depends on both, so it is rank 3. Every arrow here crosses exactly one rank, which is the case the next two sections are measured against.

Two things follow, and they are the difference between the first two claims:

- **The Acyclicity Law is exactly the condition that ranks can be assigned at all.** Try the rule on a cycle and it never terminates: A's rank needs B's, which needs A's. Acyclic and rankable are the same property.
- **The Ranking Principle adds that every arrow crosses exactly one rank.** Rank 4 may use rank 3. It may not reach down to rank 1, even though nothing about acyclicity forbids that. This is a real constraint and most systems do not satisfy it.

The Three-Tier Idiom is where the physical boundary arrives, and it varies by ecosystem. In Java and C# it was usually separate projects, assemblies, or shipped libraries; elsewhere it shows up as top-level directories or packages. What each form actually enforces differs — a directory is a package in Go, carries no access meaning in C# until assemblies split, and enforces nothing in Python — and [chapter 21](21_idioms_7nkn.md) works through why ecosystems diverge like this.

The three are taught together, defended together, and heard as one sentence. Separating them is what the rest of this chapter does.

---

## The demonstration

### When the shape isn't a line

The dependency graph of a compiler's own source — the packages the compiler is built from, not anything it reads or emits — is not a line, and it is worth walking through why, because this is the case where insisting on one does visible damage.

| Part | Job | Needs |
|---|---|---|
| `ast` | the node types — `BinaryExpr`, `IfStmt`, `FuncDecl` | nothing |
| `parser` | source text → tree | `ast` |
| `printer` | tree → source text | `ast` |
| `typecheck` | walk the tree, resolve types, report errors | `ast`, `printer` |
| `codegen` | typed tree → output | `ast`, `typecheck` |

Drawn with arrows pointing down at what is needed, beside a graph that *is* a line:

```text
A LINE                    NOT A LINE

rank 3   service          rank 4   codegen
            ↓                         ↓
rank 2    store           rank 3   typecheck
            ↓                         ↓
rank 1   errmap           rank 2   printer     parser
                                      ↓           ↓
                          rank 1      └──→ ast ←──┘

                          plus two arrows that skip ranks:
                             codegen   ──→ ast   (4 to 1)
                             typecheck ──→ ast   (3 to 1)
```

Read these as dependency arrows, not as the order things happen in. Source text flows *forward* through parser, typecheck, and codegen at runtime; the arrows run the other way, from each part to what it needs in order to compile. That is why `codegen` sits at the top rather than at the end.

Two dependencies make the shape.

**`printer` depends on `ast` and on nothing else.** It is the inverse of `parser` — one turns text into a tree, the other a tree into text. Neither calls the other. Ask which is above the other and the question is empty; they are peers over a shared type.

**`typecheck` depends on `printer`.** To emit `cannot use name (string) as int`, the type checker has to render the offending expression back into source text. That is printing, and there is no reason to have two implementations of it.

So `ast` sits at the bottom with four things depending on it and nothing below. That is the shape you want, because `ast` is the most stable part and everything else consumes it. Adding a sixth part later — a linter, a documentation generator, a language server — costs exactly one new edge into `ast` and changes nothing that exists.

Be precise about what fails here, because the graph is acyclic and ranks *can* be assigned. Claim one holds. What fails is claim two, which requires every arrow to cross exactly one rank. Two arrows do not: `typecheck` reaches from 3 down to `ast` at 1, and `codegen` from 4 down to 1. Those are not accidents you could refactor away — every part needs the node types, which is what it means for `ast` to be the shared vocabulary.

The ranks also carry no meaning. Rank 2 holds `parser` and `printer`, which have nothing in common: one reads text, the other writes it, and neither touches the other. They share a number because they are the same distance from `ast`, which is a fact about counting arrows rather than a statement about abstraction, ownership, or rate of change. There is nothing to call rank 2 — and being unable to name a rank is how you know it is an artifact of the arithmetic.

Force the line anyway, and each way of doing so costs something concrete.

**Option A: move printing into `ast`.**

```go
// ast now knows about formatting.
func (e *BinaryExpr) String() string {
	return e.X.String() + " " + e.Op.String() + " " + e.Y.String()
}
```

The line is restored, and `ast` now owns indentation, spacing, comment preservation, and line width. Every formatting change edits the node types, and the node types are the thing with the most dependents in the system. You have taken the part that should change least and made it the part that changes on every formatting bug.

**Option B: give `typecheck` its own small printer.** Now there are two printers, and they drift. The formatter emits `x + y*2`; the error message says `x+y*2`. Users report that the compiler suggests code the formatter immediately rewrites, and the fix requires keeping both implementations in sync forever.

**Option C: invent a coordinator above both.**

```csharp
// The layer that exists to hold the thing that didn't fit.
public class CompilationService {
    public void Compile(string source) {
        var tree = _parser.Parse(source);
        _typecheck.Check(tree, _printer);   // printer threaded through
        _codegen.Emit(tree);
    }
}
```

The printer is now a parameter passed down through `typecheck` into every function that might report an error — four call levels deep, in service of a diagram. Nobody set out to write this; it was the only way to satisfy a shape that was wrong.

It also supplies the test this chapter uses twice more: **does this thing decide something, or does it only forward?** `CompilationService` decides nothing — every line hands work to something else. A part that forwards is not a part.

All three costs come from one mistake: the real graph was a directed acyclic graph, and a line was imposed on it. The failure is not sloppiness — it is discipline applied to the wrong claim.

> **Managed, acyclic dependency direction is the Law. Layering is its most common shape, not its definition.**

### Layering, without directories

The previous case had the Ranking Principle failing. This one has it holding and the Three-Tier Idiom absent, which is the combination that shows how little the physical boundary was doing.

FlowCore's dependency graph is a line — service, then store, then error mapping. It is also one flat Go package with no subdirectories, so nothing about the file system enforces it. The enforcement is in the type system instead.

```go
// store.go — the interface the store helpers take.
type querier interface {
	Exec(ctx context.Context, sql string, args ...any) (pgconn.CommandTag, error)
	Query(ctx context.Context, sql string, args ...any) (pgx.Rows, error)
	QueryRow(ctx context.Context, sql string, args ...any) pgx.Row
}
```

`Begin` is absent, deliberately. Both `*pgxpool.Pool` and `pgx.Tx` satisfy this interface, so a store helper composes into either — and no store helper can start a transaction, because the type it was handed has no method to start one. Transaction control lives in the service and cannot leak downward, enforced by the compiler rather than by review.

A later revision added a second tier of the same trick:

```go
// A helper that issues several statements is correct ONLY inside a transaction.
type txQuerier interface {
	querier
	Conn() *pgx.Conn
}

func advance(ctx context.Context, q txQuerier, workflowID uuid.UUID, action actionRow) error
func readState(ctx context.Context, q txQuerier, workflowID uuid.UUID) (WorkflowState, error)
```

`Conn` is not meaningful — it is a discriminator. `pgx.Tx` has it, `*pgxpool.Pool` does not, so passing the pool fails to build:

```text
cannot use e.pool (variable of type *pgxpool.Pool) as txQuerier value in
argument to readState: *pgxpool.Pool does not implement txQuerier
(missing method Conn)
```

`Begin` is still absent from both. `txQuerier` does not let a helper start a transaction; it lets a helper *require that its caller already did*.

**The layering is real and checkable.** Ask whether the lower piece compiles without the upper one: delete `catalog.go`, and `insertStepDefinition` still builds — it needs `querier`, `StepDefinition`, and `mapInsertErr`, none of which live in the service. Delete the store, and `Catalog.Create` does not build. That asymmetry *is* the layering.

**None of it is expressed as directories.** The boundary that matters — who may open a transaction — is a method that is not on an interface. A folder could not have enforced it, and would have introduced a different problem instead: two representations of every entity and a mapping layer between them.

So: **layer ≠ directory.** A layer is a rule about which direction calls may go. Nothing about that rule requires, implies, or is helped by a file hierarchy.

### When the lower layer is more capable

The third case has claim three not merely absent but inverted. Layered doctrine says business logic belongs in the business layer and the data layer is dumb persistence. Under that rule, this is a violation:

```sql
-- The gate is in the bottom layer.
update flowcore.step_visit
   set completed_at = now(), completed_by = $2
 where id = $1
   and completed_at is null
```

"A visit can be completed only once" is a business rule. Doctrine says it belongs in the service. Putting it in the service produces a read, then a write, with a window between them — and the audit history quietly corrupts under concurrency ([Ch. 06](06_time_mdbn.md) owns why that window is unclosable from above).

So the orthodoxy is wrong here, and it is wrong for a principled reason:

> **Layering assumes the lower layer is a dumber, more general version of the upper one.**

Postgres is not dumber. It has capabilities — atomicity, row locking, constraint evaluation — that the layer above cannot replicate at all. When the lower layer is *more* capable along the axis that matters, "keep logic out of it" stops being good advice and becomes an instruction to reimplement a correct mechanism incorrectly.

The Law is untouched again: the dependency still points one way. What inverted is the taxonomy claim about what kind of thing belongs where — the Idiom, borrowed from an era when the bottom layer really was a file.

---

## Why the claim holds

A Law, a Principle and an Idiom loaded into one sentence would be harmless if a listener unpacked all three on hearing it. The mechanism that stops them being unpacked is worth stating.

**The Law lends its authority to the other two, and nothing in the sentence marks the transfer.** "Dependencies must not be circular" is checkable, mechanical, and true everywhere. "Business logic goes in the business layer" is a convention of one ecosystem in one decade. Both arrive inside "we use a layered architecture," in the same tone, from the same person. A listener who agrees with the first has already agreed with the third without a separate decision having been made.

**The ranks are arithmetic, and arithmetic looks like structure.** A rank is the count of arrows between a part and the bottom. That number always exists in an acyclic graph, so a ranking can always be produced — which is why the diagram never fails to be drawable and never signals that it means nothing. The compiler's rank 2 held `parser` and `printer`, two parts with nothing whatever in common. The test is whether the rank can be named: `presentation` and `data` are names, and `things two hops from ast` is not.

**The physical boundary is the only one of the three you can see in a repository**, so it becomes the thing people check. A folder tree is visible in a file browser; the dependency graph is not visible anywhere without a tool. Reviews then measure the claim that is easiest to observe rather than the one that carries the cost, which is how a codebase acquires the shape of the Idiom and the damage of a violated Law at the same time.

---

## Where the claim doesn't apply

The claim is that harm comes from the Idiom borrowing the Law's authority. The boundary is the case where the Idiom is simply correct.

### When the Three-Tier Idiom is the right one

A form-over-data web application, with users, roles, invoices and a reporting page. Requests arrive at handlers, handlers call service functions that enforce rules, service functions read and write rows. The graph really is `presentation → business → data`, because that is what the program does.

Here the Idiom is right, and it is right for reasons that have nothing to do with its being popular:

- **The ranking matches the graph**, so the Ranking Principle holds without anyone forcing it, and no pass-through class is needed to fill a rank.
- **The names are real.** Somebody can say what belongs in the service layer and what does not, which is the test the compiler's rank 2 failed.
- **A new contributor already knows it.** The convention costs nothing to learn and answers the placement question the same way every time, which is worth more than a better arrangement nobody shares ([Ch. 21](21_idioms_7nkn.md) argues this at length — an Idiom you can out-argue is usually still the one to follow).

This is the common case, and saying so matters. Most applications that call themselves layered are layered, and their teams are not making the mistake this chapter describes. The failure is not in using the ranking. It is in carrying it into a program whose graph has a different shape, and defending it there with the Law's certainty.

The test that separates the two takes one question: **can you name each rank, and does every arrow cross exactly one?** Both yes, and the Idiom is doing real work. Either no, and it is a diagram being enforced against the program.

---

## What the claim costs

### Everything could start looking like a layer

Once a team owns the word "layer," everything tends to become a layer, including things that are stages, cross-cutting concerns, or nothing at all. Logging is the usual one:

```csharp
// Logging as a layer. One method per method of the thing it wraps,
// and not one of them decides anything.
public class LoggingOrderService : IOrderService {
    private readonly IOrderService _inner;

    public Task<Order> Get(Guid id) {
        _log.LogInformation("Get {Id}", id);
        return _inner.Get(id);
    }

    public Task<Order> Place(OrderRequest request) {
        _log.LogInformation("Place {Customer}", request.CustomerId);
        return _inner.Place(request);
    }
    // ... and twenty more
}
```

Add a method to `IOrderService` and you now edit two files, one of which forwards. That tax is paid per method, forever, and it buys nothing that this does not:

```go
// Logging as what it is: something that cuts across, applied once
// at the edge, with no per-method cost.
mux.Handle("/orders", logging(ordersHandler))
```

The test applies unchanged: does this thing decide something, or does it forward? Logging forwards. It is not a layer.

### The physical boundary bills you whether or not it was needed

Expressing a rank as a package or assembly wall forces exports and mapping code. Where the wall matches a real dependency boundary, that is a price for something. Where it was drawn to complete a diagram, you pay the same amount for nothing, and the bill recurs on every change that crosses it ([Ch. 04](04_dependency-and-hiding_agjy.md) prices the export half).

---

## How to recognize the failure

**In a codebase:**

- **A class whose every method forwards to one other object.** It was invented to fill a slot in a shape, and it charges a file edit on every change while deciding nothing.
- **The same entity re-typed once per layer, with mappers between.** Every boundary that isn't a real dependency boundary still bills you a type and a mapper, plus the bug where someone adds a field to two of the three ([Ch. 18](18_abstraction-as-insurance_4jk6.md)).
- **A rank nobody can name.** A real rank has a job you can state: `presentation` renders, `service` enforces rules, `data` persists. Where the best available description is *the things two hops from `ast`*, the rank is a count of arrows rather than a division of work — and enforcing it puts parts in one box that have nothing to do with each other, then asks what belongs in that box.
- **A folder tree that does not match the import graph.** The tree is the claim; the imports are what is true. Where they disagree, the tree is decoration and the review that checked it found nothing.
- **A `core` or `domain` package that imports the *web framework*.** The standard library is not the tell: `System.Collections`, `System.Threading` and Go's `sync` are part of the platform and sit below everything, so depending on them says nothing. The tell is an import of something the ranking places *above* this package — an HTTP attribute, a controller base class, a request type. The ranking says it is at the bottom; the import says it is not, and the import is the one the compiler acts on.

**In a conversation:**

- **"Which layer does this go in?"** — asked about a pipeline stage or a cross-cutting concern, where the question has no answer. The shape is wrong, not the placement.
- **A design defended by the diagram it matches** rather than by what depends on what. Authority substituting for mechanism.
- **"That's a layering violation."** Which of the three? The word covers a Law you cannot break, a Principle that may not hold here, and a convention from somebody else's decade.
- **A discussion about folder structure** without the dependency graph in sight. The subject is an Idiom treated as a Law.

The question that does the work is not *which layer does this belong to?* It is: **what would break if this piece stopped existing?**

[Chapter 06](06_time_mdbn.md) does for concurrency what these two chapters did for structure.

---

## Sources

- FlowCore — [github.com/ilke-akdeniz/flowcore](https://github.com/ilke-akdeniz/flowcore).

---

[← Ch. 04](04_dependency-and-hiding_agjy.md)  ·  [Contents](00_toc.md)  ·  [Ch. 06 →](06_time_mdbn.md)
