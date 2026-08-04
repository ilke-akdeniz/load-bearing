# Structure: Dependency and Hiding

*This chapter is mostly **Law**, with a **Principle** and an **Idiom** attached — and the attaching is the problem. "Layered architecture" is all three at once under one name, which is why it is simultaneously the most reliable structural advice in software and the source of some of the worst structure you will read.*

## The claim

**The dependency graph must be acyclic**, and **what a module makes observable is what it has committed to** — everything else people say about architecture is a shape or a convention layered on top of those two.

The first is a Law. The second is a Principle with one sharp condition. Neither of them says anything about folders.

## Three claims wearing one name

Say "we use a layered architecture" and you have made three claims at three different levels `(ours)`:

| Claim | Kind | Standing |
|---|---|---|
| Dependencies flow one way — no cycles | **Law** | near-tautology, Grade B (Ch. 04) |
| The acyclic graph is a straight line | **Principle** | true when the shape genuinely is a line |
| The line is `presentation → business → data`, expressed as directories | **Idiom** | 1990s enterprise Java, and arbitrary |

Most real architecture damage is a violation of the first. Most harm done by *architecture advocacy* comes from the third, applied to a program whose dependency graph looks nothing like a line — which then generates pass-through classes and mapping code to fill out the shape.

They are usually taught together and defended together. Separating them is the whole content of this chapter.

---

## The demonstration

### Part one: a cycle, at three granularities

Two pieces of a workflow library. A store that writes rows, and a service that composes writes into a transaction.

```go
// The service calls down. Normal.
func (c *Catalog) Create(ctx context.Context, definition WorkflowDefinition) error {
	tx, err := c.pool.Begin(ctx)
	if err != nil {
		return err
	}

	defer func() { _ = tx.Rollback(ctx) }()

	for _, step := range definition.Steps {
		if err := insertStepDefinition(ctx, tx, step); err != nil {
			return err
		}
	}

	return tx.Commit(ctx)
}
```

Now someone needs validation inside the insert, and the validation logic lives on `Catalog`:

```go
// The store reaching back up.
func insertStepDefinition(ctx context.Context, q querier, c *Catalog, step StepDefinition) error {
	if !c.validate(step) {
		return ErrInvalidStep
	}

	_, err := q.Exec(ctx, `insert into flowcore.step_definition ...`)

	return mapInsertErr(err, step.Name, "workflow_definition", step.WorkflowDefinitionID)
}
```

That is a cycle. `Catalog` needs `insertStepDefinition`; `insertStepDefinition` needs `Catalog`.

Here is the part worth noticing: **whether anything complains depends entirely on where the boundary happens to fall.**

```text
same package, Go            compiles. No warning, no error, ever.
separate packages, Go       build error: import cycle not allowed
separate assemblies, C#     build error: circular project reference
separate modules, Python    sometimes works, sometimes ImportError,
                            depending on which module you import first
```

Four outcomes for one structural fact. Go's import-cycle error is famously strict, and it is strict at exactly one granularity — the package. Below that, the same cycle is invisible to it. Python's behaviour is the worst of the set, because it is *conditional*: the cycle is tolerated or fatal depending on entry order, so it can survive for months and then break when someone adds an import to a test file.

The Law does not care about any of this. The compiler is a partial detector operating at whatever granularity that language happens to check. **The damage is the same at every granularity; only the detection varies.**

### Part two: layering, without directories

FlowCore's dependency graph is a line — service, then store, then error mapping. It is also one flat Go package with no subdirectories, so nothing about the file system enforces it.

The enforcement is in the type system instead.

```go
// store.go — the interface the store helpers take.
type querier interface {
	Exec(ctx context.Context, sql string, args ...any) (pgconn.CommandTag, error)
	Query(ctx context.Context, sql string, args ...any) (pgx.Rows, error)
	QueryRow(ctx context.Context, sql string, args ...any) pgx.Row
}
```

`Begin` is absent, deliberately. Both `*pgxpool.Pool` and `pgx.Tx` satisfy this interface, so a store helper composes into either — and no store helper can start a transaction, because the type it was handed has no method to start one. Transaction control lives in the service and cannot leak downward, and that is enforced by the compiler rather than by review.

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

Two things follow, and they are the point of the example.

**The layering is real and checkable.** Ask whether the lower piece compiles without the upper one: delete `catalog.go`, and `insertStepDefinition` still builds — it needs `querier`, `StepDefinition`, and `mapInsertErr`, none of which live in the service. Delete the store, and `Catalog.Create` does not build. That asymmetry *is* the layering.

**None of it is expressed as directories.** The boundary that matters — who may open a transaction — is a method that is not on an interface. A folder could not have enforced it, and would have introduced a different problem instead (Ch. 18 works through what package walls cost).

So: **layer ≠ directory.** A layer is a rule about which direction calls may go. Nothing about that rule requires, implies, or is helped by a file hierarchy.

### Part three: when the shape isn't a line

FlowCore's graph happens to be a line. A compiler's is not:

```text
LAYERED (a line)        DAG BUT NOT A LINE

  service                 parser ──→ ast ←── printer
     ↓                      │                  ↑
   store                    ↓                  │
     ↓                   typecheck ────────────┘
   errmap                   ↓
                         codegen
```

Both are acyclic. Both are fine. Only the left one is layered.

`ast` is depended on by parser, printer, typecheck, and codegen; it depends on none of them. Ask "is `ast` above or below `printer`?" and the question has no answer — which does not mean the design is unprincipled. It means the principle is acyclicity and the shape simply isn't a line.

The failure mode is insisting on the left-hand picture when the truth is the right-hand one. You invent a layer to hold the thing that doesn't fit, and you get a class whose job is to forward calls.

Sharpened:

> **Managed, acyclic dependency direction is the Law. Layering is its most common shape, not its definition.**

---

## Why it holds

### The cycle mechanism

If A depends on B and B depends on A, then four things become true at once, and none of them is a matter of taste:

- **You cannot understand A without understanding B.** The unit of comprehension is now A+B, whatever the file layout says.
- **You cannot test A without B.** The unit of test is A+B.
- **You cannot change A's contract without changing B's, which changes A's.** The unit of change is A+B.
- **You cannot always initialize or build one before the other.** Sometimes the toolchain refuses outright.

That is the entire argument, and it is why this is a Law rather than a strong opinion: it is a property of graphs, restated in the vocabulary of software. Nothing about a language, a team, or a decade changes it.

It also explains why the advice feels so much more reliable than most: **dependency damage compounds.** A missing test is a static cost — it sits there, costing what it costs. A cycle spreads. Once A and B are mutually dependent, any C that touches either one inherits both, and the tangle grows monotonically. Ten years of individually forgivable violations produce a system in which no piece can be moved, and no single commit in that history looks like the culprit.

### Cost of change scales with dependents

The second half of the mechanism, and the one that decides where to put effort.

Changing a module costs roughly in proportion to how many things depend on it. A leaf with no dependents is free to change: nothing else can notice. A module with forty dependents costs forty inspections, and the cost is paid on *every* change, not once.

Two consequences follow immediately.

**Depth is expensive at the bottom.** The lowest node in the graph is the most expensive to change and should be the most stable — not because stability is virtuous, but because you have to pay for instability there over and over. This is the real content behind "depend on abstractions": an abstraction is cheap to keep stable, so putting one at a high-fan-in position lowers the recurring bill.

**The count is what matters, not the count of *your* dependents.** Once a module is published, the number of dependents is unknown and growing, which is where the next section starts.

### Information hiding, and why it's a Principle

`(established)` Parnas, 1972: decompose a system by what each module *hides*, not by the steps of the process it performs. The value of a module is the decision it keeps to itself, because that is the decision you can change later without telling anyone.

The mechanism is exactly the previous section. A hidden decision has zero dependents by construction. An exposed one has as many as care to look.

This is why the export surface, not the design document, is the real API:

```go
// Go: privacy is per-package, and the marker is the first letter.
type Catalog struct{}          // exported — a promise
func NewCatalog(...) *Catalog  // exported — a promise
type querier interface{}       // unexported — free to change
func insertStepDefinition(...) // unexported — free to change
```

FlowCore's decision log records the reasoning for keeping `querier` private, and it is a cost calculation rather than a preference:

> An exported interface would be a public commitment to a shape pgx defines, so a pgx v6 signature change would trap the library between their break and its promise; private means free resignaturing.

That is the whole of API design, stated as a bill. Exporting `querier` would have bought nothing and mortgaged the library's freedom to a third party's release schedule.

### Hyrum's Law: hiding is not optional, only the mechanism is

`(established)` **With a sufficient number of users, every observable behaviour of your system will be depended upon by somebody, regardless of what you promised.**

Not the documented behaviour. The observable one. Iteration order of a map that you never promised was stable. The exact wording of an error message, parsed by someone's log alert. The fact that a call currently takes 40ms, which somebody's timeout was tuned against. Whether IDs happen to be sequential.

The mechanism is not carelessness. It is that a user testing against your implementation cannot distinguish your contract from your behaviour — the running system is the only specification they have direct access to. So they encode what they observe, and after enough users, every observable is encoded somewhere.

Two practical corollaries.

**Any behaviour you can't afford to keep, you must prevent from being observed.** Randomizing map iteration order, as Go does, is Hyrum's Law taken seriously: the only way to keep a freedom is to make its absence impossible to depend on.

**Your export surface is a liability inventory, not a feature list.** Every capital letter is a promise you did not necessarily mean to make, and taking one back is a breaking change even if no document ever mentioned it.

Hiding is a **Principle** rather than a Law, and it has a sharp condition: *you do not control your callers.* When you do control every caller — a single application, one team, one repository, one deploy — the condition weakens, and hiding starts trading against convenience rather than against catastrophe. This is why library design and application design genuinely differ, and why advice from one arrives wrong in the other.

---

## Where this doesn't apply

Four boundaries.

### The Law goes inert when nothing is ever separated

The cycle argument is entirely about A and B being *separate units of comprehension, test, and change*. Where they are not separate, the Law has nothing to act on.

Mutually recursive functions are a cycle:

```go
func parseExpr(p *parser) node { ... p.parseTerm() ... }
func parseTerm(p *parser) node { ... p.parseExpr() ... }
```

Nobody sane calls this an architecture violation, and the reason is precise rather than a matter of degree. You will never comprehend one without the other, never test one without the other, never change one's contract without the other's. They were already one unit. The cycle costs nothing because the cost of a cycle *is* the forced merging of units — and there is no merging to force.

The same goes for two types in one file that reference each other, or a 200-line CLI that has one layer because there is nothing to order. This is a Law that is true and inert (Ch. 02), not a Law being bent.

The test is not "is there a cycle in the call graph." It is: **will these ever be understood, tested, or changed apart?** If the honest answer is no, the cycle is free. If the honest answer is "not today, but obviously yes in a year," you are paying for the merge on the schedule your future self chose.

### ECS: hiding inverted by the memory hierarchy

The clearest case of the *hiding* Principle being wrong rather than merely inert.

The encapsulated version, which any object-oriented style guide would endorse:

```csharp
// Each entity owns its state. Nothing outside can see the fields.
class Particle {
    private Vector3 position;
    private Vector3 velocity;
    private Color    tint;
    private float    lifetime;
    public void Update(float dt) { position += velocity * dt; lifetime -= dt; }
}

Particle[] particles;                          // 100,000 of them
foreach (var p in particles) p.Update(dt);
```

The entity-component-system version, which deliberately does the opposite:

```csharp
// Nothing owns anything. State is parallel arrays, public, flat.
Vector3[] position;   // 100,000
Vector3[] velocity;   // 100,000
Color[]   tint;       // 100,000 — never touched by this loop
float[]   lifetime;   // 100,000

for (int i = 0; i < count; i++) {
    position[i] += velocity[i] * dt;
    lifetime[i] -= dt;
}
```

The second is not a worse-encapsulated version of the first. It is a different decomposition, and it wins by a margin that has nothing to do with taste: the first loop drags `tint` and every other unused field through cache on every iteration, and the second touches only the bytes it needs. (Chapter 08 owns the arithmetic and the benchmark; the span between cache and main memory is where the whole margin comes from.)

Notice what has been given up. `position` is public, mutable, and touched by a dozen systems. There is no module hiding the decision "how is a particle laid out," because that decision is the *interface* — every system agrees on the layout, and that agreement is the design.

The Force is the memory hierarchy, and it does not negotiate. Where it dominates, "hide the representation" inverts: hiding the representation is precisely what you must not do, because the representation is the shared contract that makes the whole thing fast. Chapter 20 works through the rest of that domain's inversions.

Note carefully what has *not* inverted. The ECS dependency graph is still acyclic — systems depend on component arrays, and the arrays depend on nothing. The Law holds untouched while the Principle turns over completely, which is the difference chapter 02 draws, seen in the wild.

### Inversion of control: the call goes up, the dependency doesn't

The most common false positive in review.

```go
// net/http. YOUR code is the leaf, and the framework calls up into it.
type Handler interface {
	ServeHTTP(ResponseWriter, *Request)
}

http.Handle("/approve", approveHandler(engine, catalog))
```

At runtime the call direction is upward: `net/http`, which you might draw as the lower layer, invokes your handler, which you would draw above it. Strictly, the lower thing calls the higher thing.

It is fine, and the reason is worth stating exactly. `net/http` does not depend on your code. It depends on `Handler` — an interface it declares itself — and your code depends on that same interface. The *call* goes up while the *dependency* goes down, because the interface sits at the bottom and both parties point at it.

This is what dependency inversion is for, and it is the legitimate version of the thing that usually signals a violation. Plugin systems, callback APIs, and UI frameworks are all built on it: in a framework, inversion of control is not an implementation detail, it is the product.

The diagnostic: draw the graph in terms of *what breaks when you delete something*, not in terms of what calls what at runtime. Delete your handler and `net/http` still compiles. That settles it.

### When the lower layer is more capable

Layered doctrine says business logic belongs in the business layer and the data layer is dumb persistence. Under that rule, this is a violation:

```sql
-- The gate is in the bottom layer.
update flowcore.step_visit
   set completed_at = now(), completed_by = $2
 where id = $1
   and completed_at is null
```

"A visit can be completed only once" is a business rule. Doctrine says it belongs in the service. Putting it in the service produces a read, then a write, with a window between them — and the audit history quietly corrupts under concurrency (Ch. 06 owns why that window is unclosable from above).

So the orthodoxy is wrong here, and it is wrong for a principled reason:

> **Layering assumes the lower layer is a dumber, more general version of the upper one.**

Postgres is not dumber. It has capabilities — atomicity, row locking, constraint evaluation — that the layer above cannot replicate at all. When the lower layer is *more* capable along the axis that matters, "keep logic out of it" stops being good advice and becomes an instruction to reimplement a correct mechanism incorrectly.

The Law is untouched again: the dependency still points one way. What inverted is the taxonomy claim about what kind of thing belongs where — the Idiom, borrowed from an era when the bottom layer really was a file.

---

## What it costs

**Breaking a cycle is never free, and the bill has a shape.** You pay in one of four currencies: an interface at the boundary (indirection, one more name to know), an event or callback (the flow becomes non-obvious in a stack trace), a third module both depend on (one more thing to place), or replacing a reference with an identifier (a lookup where you used to have a pointer, and a lifetime question you now have to answer). Pick deliberately. The failure is paying in interfaces by reflex — an interface per boundary regardless of whether the boundary was real, which is how a codebase acquires forty interfaces with one implementation each (Ch. 17 traces where that reflex comes from).

**Hiding costs you the day you need what you hid.** A well-encapsulated module is opaque when you are debugging it at 3am, and the thing you need is behind exactly the wall you built. Sealed libraries with no escape hatch are a real and recurring frustration, and the honest answer is an explicitly unsupported access point rather than pretending the need won't arise.

**Acyclicity discipline slows some changes down.** Sometimes the cheap fix genuinely is to let the lower thing call up, and refusing costs an afternoon of restructuring for a benefit measured in years. That trade is usually right and is not always right — a script with a known death date does not need it (Ch. 09).

**Enforced boundaries cost more than unenforced ones.** Expressing the graph in the type system, as `querier` does, is nearly free. Expressing it as package or assembly walls forces exports and mapping code — a real bill, worth paying at some team sizes and not at others (Ch. 18).

**The line shape is seductive.** Once a team owns the word "layer," everything becomes a layer, including the things that are stages, cross-cutting concerns, or nothing at all. Logging is not a layer. Making it one produces the pass-through classes that gave layering its bad name.

---

## How to recognize the failure

**In a codebase:**

- Two modules that always appear together in commits, whatever the directory structure claims about their independence.
- A class whose every method forwards to one other object without deciding anything — an invented layer holding the thing that didn't fit the shape.
- The same entity re-typed once per layer, with mappers between, and a bug where someone added a field to two of the three.
- A test that requires constructing half the system to exercise one function.
- `import` statements at the top of a file that surprise you — the leaf reaching for something it should not know exists.
- An `internal` or `impl` package that everything imports, which means it is neither.
- A published API where the documented contract and the observable behaviour differ, and the callers depend on the observable one.

**In a conversation:**

- "Which layer does this go in?" asked about something that is a stage in a pipeline, or a cross-cutting concern, and therefore has no answer.
- A design defended by the diagram it matches rather than by what depends on what.
- "We can't change that, things depend on it" — accurate, and worth converting into the count. Forty dependents is a decision; two is an afternoon.
- Someone calling an inversion-of-control callback a layering violation.
- Two people arguing about a folder structure, when neither has drawn the dependency graph.

The question that catches real damage is not *does this match the diagram?* It is: **can this piece be understood without that piece?**

The first question generates folders. The second finds the cycle.

---

**Next:** chapter 06 does for concurrency what this chapter did for structure — turns "be careful with shared state" into a rule you can check, starting with the fact that check-then-act is not atomic.
