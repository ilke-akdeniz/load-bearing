# Structure: Dependency and Hiding

*This chapter is mostly **Law**, with a **Principle** and an **Idiom** attached — and the attaching is the problem. "Layered architecture" is all three at once under one name, which is why it is simultaneously the most reliable structural advice in software and the source of some of the worst structure you will read.*

## The claim

**The dependency graph must be acyclic**, and **what a module makes observable is what it has committed to** — everything else people say about architecture is a shape or a convention layered on top of those two.

The first is a Law. The second is a Principle with one sharp condition. Neither of them says anything about folders.

## Three claims wearing one name

Say "we use a layered architecture" and you have made three claims at three different levels. Splitting them this way is this book's, not standard vocabulary:

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

### What the damage actually is

That sentence is worth cashing out, because "damage" is doing a lot of work and most of it is not what people expect.

**First, the small part: cycles that crash.**

A cycle across module boundaries can break initialization, because something has to be constructed first and a cycle says nothing can be. Python is the clearest case:

```python
# a.py
import b
TIMEOUT = b.BASE * 2

# b.py
import a
BASE = 5
LIMIT = a.TIMEOUT + 1
```

Import `a` first and it works. Import `b` first and you get:

```text
AttributeError: partially initialized module 'a' has no attribute
'TIMEOUT' (most likely due to a circular import)
```

Same code, same machine, and the outcome depends on which module the process happened to touch first — so it can pass every test and fail in production, where the entry point differs. C# and Java have a nastier version of the same thing in static initializers, where instead of an exception you can get a field silently holding its zero value, because the type was still being initialized when it was read.

That class of bug is real. It is also the *minority* of the damage, and if it were the whole argument, "avoid cycles" would be a tip rather than a Law.

**Second, the large part: cycles that never crash at all.**

Assume the program is correct, fast, and stable. The bill still arrives, and it arrives on every future change. Concretely.

Suppose `billing` and `accounts` depend on each other — `billing` reads the merchant's plan, `accounts` asks `billing` whether the merchant is in arrears. Nothing about this is broken. Then a ticket arrives: *make the payment retry limit configurable per merchant.*

- **The test you expected to write does not exist.** To test the new retry logic you need a merchant, which needs `accounts`, which needs `billing`, which needs a database. What should have been a unit test is now an integration test with fixtures, so it is slower, flakier, and less likely to be written at all.
- **You cannot read one without the other.** The retry code calls into `accounts`, which calls back into `billing`. Following it means holding both in your head, so the fifteen-minute change becomes a morning.
- **You cannot move it.** The roadmap says billing becomes its own service. It cannot: extracting `billing` drags `accounts` with it, and extracting both is a different project than the one that was estimated.
- **You cannot delete it.** Six months later the plan lookup is dead code, but nothing proves that, because the call graph loops.
- **The next person adds a second path.** They read `billing`, do not understand why it calls back into `accounts`, and write their own retry limit rather than disturb it. Now there are two, and they disagree.

None of that is a bug report. It shows up as estimates being wrong by a factor of five, as a refactor that gets abandoned, as a service extraction that slips two quarters. **The damage is denominated in future change, not in incorrect output** — which is exactly why it accumulates unnoticed, and why no single commit in the history looks like the culprit.

### The mechanism, stated once

If A depends on B and B depends on A, four things become true at once:

- **You cannot understand A without understanding B.** The unit of comprehension is A+B, whatever the file layout says.
- **You cannot test A without B.** The unit of test is A+B.
- **You cannot change A's contract without changing B's, which changes A's.** The unit of change is A+B.
- **You cannot always initialize or build one before the other.** Sometimes the toolchain refuses outright; sometimes, worse, it doesn't.

That is the whole argument, and it is why this is a Law rather than a strong opinion: it is a property of graphs, restated in the vocabulary of software. Nothing about a language, a team, or a decade changes it.

It also explains why the advice is more reliable than most: **dependency damage compounds.** A missing test is a static cost — it sits there, costing what it costs, and it does not get worse on its own. A cycle spreads, in a way worth being precise about, since the obvious objection is that you can just wire things together and move on.

### "Can't I just inject A and B into C?"

No, and the reason is the useful part.

```go
// The cycle is between these two. C is not in it.
type Accounts struct{ billing *Billing }
type Billing struct{ accounts *Accounts }

// Injecting both into C changes who constructs them.
// It does not remove either edge.
func NewReports(a *Accounts, b *Billing) *Reports
```

Injection moves *construction* to the caller. It does not move *dependency*. `Billing`'s type still names `Accounts`, so the compiler still has to have `Accounts` in hand to compile `Billing`, the test still has to build one, and the reader still has to know both.

You can see the cycle admitting itself at the construction site:

```go
a := &Accounts{}
b := &Billing{accounts: a}
a.billing = b // two-phase construction, because neither can be built first
```

That assignment is the tell. There is now a window in which `a.billing` is nil, and nothing in the type system says when the window closes. Any code that runs during it — an init hook, a background goroutine started in a constructor, a log line — sees a half-built object.

What *does* break the cycle is injecting an **interface declared by the module that needs it**:

```go
package billing

// billing states what it requires, in its own terms.
type PlanLookup interface {
	PlanFor(ctx context.Context, merchantID uuid.UUID) (Plan, error)
}

type Billing struct{ plans PlanLookup }
```

`accounts` implements `PlanLookup`. Now `billing` depends on nothing, `accounts` depends on `billing`, and there is one edge where there were two. Construction is single-phase, `billing` tests with a five-line fake, and `billing` can be extracted into its own service without dragging anything.

The difference is not that an interface appeared. It is **which module owns it.** An interface declared by `accounts` and consumed by `billing` leaves the arrow pointing exactly where it was. The same manoeuvre appears twice more in this chapter — as one of the four ways to pay for breaking a cycle, and as the reason `net/http` may call up into your handler without a violation.

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

FlowCore's graph happens to be a line. A compiler's is not, and it is worth walking through why, because this is the case where insisting on a line does visible damage.

Five parts, and what each one does:

| Part | Job | Needs |
|---|---|---|
| `ast` | the node types — `BinaryExpr`, `IfStmt`, `FuncDecl` | nothing |
| `parser` | source text → tree | `ast` |
| `printer` | tree → source text | `ast` |
| `typecheck` | walk the tree, resolve types, report errors | `ast`, `printer` |
| `codegen` | typed tree → output | `ast`, `typecheck` |

```text
LAYERED (a line)        DAG BUT NOT A LINE

  service                 parser ──→ ast ←── printer
     ↓                      │                  ↑
   store                    ↓                  │
     ↓                   typecheck ────────────┘
   errmap                   ↓
                         codegen
```

The two surprising edges are the ones that make the shape.

**`printer` depends on `ast` and on nothing else.** It is the inverse of `parser` — one turns text into a tree, the other a tree into text. Neither calls the other. Ask which is above the other and the question is empty; they are peers over a shared type.

**`typecheck` depends on `printer`.** To emit `cannot use name (string) as int`, the type checker has to render the offending expression back into source text. That is printing, and there is no reason to have two implementations of it.

So `ast` sits at the bottom with four things depending on it and nothing below. That is not an accident of drawing — it is the shape you want, because `ast` is the most stable part and everything else is a consumer of it. Adding a sixth part later — a linter, a documentation generator, a language server — costs exactly one new edge into `ast` and changes nothing that already exists.

Now force it into a line. You must put `printer` and `parser` in some order, and each choice costs something concrete.

**Option A: move printing into `ast`.**

```go
// ast now knows about formatting.
func (e *BinaryExpr) String() string {
	return e.X.String() + " " + e.Op.String() + " " + e.Y.String()
}
```

The line is restored — `ast` is at the bottom and everyone can print. But `ast` now owns indentation, spacing, comment preservation, and line width. Every formatting change edits the node types, and the node types are the highest-fan-in thing in the system. You have taken the one part that should change least and made it the part that changes on every formatting bug.

**Option B: give `typecheck` its own small printer.**

Now there are two printers, and they drift. The formatter emits `x + y*2`; the error message says `x+y*2`. Users report that the compiler suggests code the formatter immediately rewrites, and the fix requires finding both implementations and keeping them in sync forever.

**Option C: invent a coordinator above both.**

```csharp
// The layer that exists to hold the thing that didn't fit.
public class CompilationService {
    public void Compile(string src) {
        var tree = _parser.Parse(src);
        _typecheck.Check(tree, _printer);   // printer threaded through
        _codegen.Emit(tree);
    }
}
```

The printer is now a parameter passed down through `typecheck` into every function that might report an error — four call levels deep, in service of a diagram. This is the pass-through class, arrived at honestly: nobody set out to write it, it was the only way to satisfy a shape that was wrong.

All three costs come from the same mistake: the real graph was a DAG, and a line was imposed on it. The failure mode is not sloppiness — it is discipline applied to the wrong claim.

Sharpened:

> **Managed, acyclic dependency direction is the Law. Layering is its most common shape, not its definition.**

---

## Why it holds

### Cost of change scales with dependents

Changing a module costs roughly in proportion to how many things depend on it. A leaf with no dependents is free to change: nothing else can notice. A module with forty dependents costs forty inspections, and the cost is paid on *every* change, not once.

Two consequences follow.

**Stability belongs at the bottom.** The highest-fan-in node is the most expensive to change, so it should be the one that changes least — not because stability is a virtue, but because you pay for instability there repeatedly. This is the real content behind "depend on abstractions," and that phrase is badly misleading, because it is routinely read as "add an interface."

What lowers the bill is **stability**, not indirection. Compare two things sitting at the bottom of a graph with high fan-in:

```go
// A good abstraction, and not an interface. Forty things depend on it.
// It has not changed in four years, and there is no reason it would.
type Money struct {
	Amount   int64  // minor units
	Currency string // ISO 4217
}
```

```go
// An "abstraction" by vocabulary and by nothing else. Forty things
// depend on it, and it changes every sprint.
type IUserService interface {
	GetUser(id string) (*User, error)
	GetUserWithPreferences(id string) (*User, error)         // added in March
	GetUserWithPreferencesAndRoles(id string) (*User, error) // added in May
}
```

The second is an interface and buys nothing. Every added method is a change at the highest-fan-in point in the system, which is the exact cost the advice exists to avoid. The `I` prefix made it *look* like a stable boundary while the concept behind it was still moving.

So the usable form of the advice is: *put the thing that changes least at the bottom.* Sometimes that is an interface. Often it is a data type, a constant, or a function signature that has earned its shape. Whether it is an interface is not the question.

**You can count internal dependents. You cannot count external ones.** Inside your repository, `grep` gives you the number, and the number tells you what a change costs. Once something is published, the count is unknown, unbounded, and growing — which is where the second half of this chapter starts.

### From direction to surface

The first half of this chapter is about which way the edges point. The second is about how many edges exist at all.

That is the whole connection, and it is worth stating plainly because the two halves are usually taught as separate subjects. A cycle is two edges where there should be one. Information hiding is about not creating an edge in the first place. Same graph, same cost model: a dependency that was never created costs nothing to change, forever.

### Information hiding, and why it's a Principle

Parnas, 1972 — the founding paper, and still the clearest statement: decompose a system by what each module *hides*, not by the steps of the process it performs. The value of a module is the decision it keeps to itself, because that is the decision you can change later without telling anyone.

The mechanism is the previous section, applied. A decision that nothing can observe has a fan-in of zero and is therefore free to change. A decision that is visible has as many dependents as care to look, and you will not be told when someone starts looking.

This is why the export surface, not the design document, is the real API:

```go
// Go: privacy is per-package, and the marker is the first letter.
type Catalog struct{}          // exported — a contract
func NewCatalog(...) *Catalog  // exported — a contract
type querier interface{}       // unexported — free to change
func insertStepDefinition(...) // unexported — free to change
```

FlowCore's decision log records the reasoning for keeping `querier` private, and it is a cost calculation rather than a preference:

> An exported interface would be a public commitment to a shape pgx defines, so a pgx v6 signature change would trap the library between their break and its promise; private means free resignaturing.

That is the whole of API design, stated as a bill. Exporting `querier` would have bought nothing and mortgaged the library's freedom to a third party's release schedule.

### "Doesn't dependency injection contradict hiding?"

It looks like it should. Injection means the caller has to know about the thing being injected, and hiding says to know as little as possible. Both cannot be right.

They are, because they are about different parties. Look at what each arrangement knows.

```go
// Without injection: billing hides nothing from itself.
// It depends on Postgres, on the pool, on the driver, on the DSN format.
func NewBilling() *Billing {
	pool, _ := pgxpool.New(ctx, os.Getenv("DATABASE_URL"))
	return &Billing{plans: &PostgresPlanStore{pool: pool}}
}
```

```go
// With injection: billing depends on three method signatures
// and knows nothing about what is behind them.
func NewBilling(plans PlanLookup) *Billing {
	return &Billing{plans: plans}
}
```

The caller learned one thing — that a `PlanLookup` must be supplied. `Billing` unlearned four. Hiding is about what a *module* is coupled to, and injection reduces that; what it increases is what the *composition root* knows, and the composition root is one file whose entire job is knowing.

The contradiction only appears if you read hiding as "less information anywhere," rather than what Parnas actually proposed: each module hides a decision, and the decision `Billing` no longer holds is *where plans come from*.

### Hyrum's Law: hiding is not optional, only the mechanism is

**With a sufficient number of users, every observable behaviour of your system will be depended upon by somebody, regardless of what you documented.** The name comes from Hyrum Wright at Google; the observation is standard and uncontroversial.

Not the documented behaviour. The observable one. Iteration order of a map that you never promised was stable. The exact wording of an error message, parsed by someone's log alert. The fact that a call currently takes 40ms, which somebody's timeout was tuned against. Whether IDs happen to be sequential.

The mechanism is not carelessness. It is that a user testing against your implementation cannot distinguish your contract from your behaviour — the running system is the only specification they have direct access to. So they encode what they observe, and after enough users, every observable is encoded somewhere.

Two practical corollaries.

**Any behaviour you can't afford to keep, you must prevent from being observed.** Randomizing map iteration order, as Go does, is Hyrum's Law taken seriously: the only way to keep a freedom is to make its absence impossible to depend on.

**Your export surface is a liability inventory, not a feature list.** Every capital letter is a commitment you did not necessarily mean to make, and taking one back is a breaking change even if no document ever mentioned it.

Hiding is a **Principle** rather than a Law, and it has a sharp condition: *you do not control your callers.* When you do control every caller — a single application, one team, one repository, one deploy — the condition weakens, and hiding starts trading against convenience rather than against catastrophe. This is why library design and application design genuinely differ, and why advice from one arrives wrong in the other. (Chapter 03 takes control-of-callers seriously as a Force in its own right.)

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

Nobody sane calls this an architecture violation, and the reason is precise rather than a matter of degree. A cycle hurts because it forces two things you wanted to handle separately to be handled as one. Here there is nothing to force together: you were never going to read one without the other, test one without the other, or change one's signature without the other's. They were a single unit before the cycle existed, so the cycle takes nothing away.

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

Be exact about what was traded away. In the class version the field layout is private: you could reorder the fields, widen `lifetime` to a double, or delete `tint` entirely, and no other file would need editing. In the array version the layout *is* the interface — a dozen systems index those arrays directly, so changing the layout means editing every one of them.

That is a genuine loss, accepted deliberately. You gave up the ability to change the representation quietly, and what you bought is the speed that comes from every system agreeing on it. There is no hidden decision left to protect, because the decision is the contract.

The Force is the memory hierarchy, and it does not negotiate. Where it dominates, "hide the representation" inverts: hiding it is precisely what you must not do. Chapter 20 works through the rest of that domain's inversions.

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

It is fine, and the reason is the one from the `PlanLookup` example earlier. `net/http` does not depend on your code. It depends on `Handler` — an interface **it declares itself** — and your code depends on that same interface. The *call* goes up while the *dependency* goes down, because the interface sits at the bottom and both parties point at it.

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

### Breaking a cycle is never free

There are four ways to pay, and they are genuinely different bills. Take the `billing` ↔ `accounts` cycle from earlier.

**One — an interface at the boundary, declared by the module that needs it.**

```go
package billing

type PlanLookup interface {
	PlanFor(ctx context.Context, merchantID uuid.UUID) (Plan, error)
}
```

*The bill:* one more name, and "go to definition" now lands on a declaration instead of the code that runs. Debugging gains a hop.

**Two — an event or callback, so the lower module announces instead of calling.**

```go
type ArrearsDetected struct {
	MerchantID uuid.UUID
	Amount     Money
}

func (b *Billing) Charge(ctx context.Context, emit func(ArrearsDetected)) error {
	// ...
	emit(ArrearsDetected{MerchantID: id, Amount: owed})
}
```

*The bill:* the stack trace stops telling you who reacts. Tracing an effect goes from reading up the stack to grepping for subscribers, and the ordering of subscribers becomes a thing you have to think about.

**Three — a third module both depend on.**

```go
package pricing // depends on neither billing nor accounts

func ArrearsThreshold(tier Tier, lifetime Money) Money
```

*The bill:* a new place to put things, and a recurring argument about what belongs in it. These modules attract unrelated code, and `common` or `shared` is how they end up named.

**Four — replace a reference with an identifier.**

```go
type Invoice struct {
	MerchantID uuid.UUID // was *Merchant
}
```

*The bill:* `invoice.merchant.Name` becomes a lookup that can fail and can be stale. You now have to answer "what if the merchant was deleted?" explicitly, where the pointer answered it for you by existing.

Pick deliberately. The failure is paying in interfaces by reflex — an interface at every boundary whether or not the boundary was real, which is how a codebase acquires forty interfaces with one implementation each (Ch. 17 traces where that reflex comes from).

### Hiding costs you the day you need what you hid

A well-encapsulated module is opaque at 3am, and the thing you need is behind exactly the wall you built. Sealed libraries with no way through are a real and recurring frustration.

The honest answer is not to stop hiding. It is to provide a way through, and name it so nobody mistakes it for supported:

```go
type Client struct {
	conn net.Conn // unexported: not part of the API
}

// UnderlyingConn returns the raw connection.
//
// It is NOT covered by this package's compatibility promise and may
// change or disappear in any release, including a patch release. It
// exists because setting a socket option we do not expose is a real
// need, and the alternative is that you fork the package.
func (c *Client) UnderlyingConn() net.Conn { return c.conn }
```

The comment is doing load-bearing work. It converts an implicit dependency — the kind Hyrum's Law says forms whether you like it or not — into an explicit one that its users accepted knowingly. Without the hatch they reach through reflection, unsafe casts, or a fork, and then you are bound by their dependency without ever having agreed to it.

### Acyclicity discipline slows some changes down

Sometimes the cheap fix genuinely is to let the lower thing call up.

```go
// Ten minutes. Ship it before lunch.
func insertStepDefinition(ctx context.Context, q querier, c *Catalog, s StepDefinition) error {
	if !c.validate(s) {
		return ErrInvalidStep
	}
	// ...
}
```

```go
// An afternoon. Validation moves above both, and the store
// never learns that Catalog exists.
func (c *Catalog) Create(ctx context.Context, d WorkflowDefinition) error {
	if err := validate(d); err != nil {
		return err
	}

	for _, step := range d.Steps {
		if err := insertStepDefinition(ctx, tx, step); err != nil {
			return err
		}
	}
	// ...
}
```

The second is right when the code has years ahead of it. On a migration script that gets deleted next month, the ten-minute version is the correct engineering call and the afternoon is waste (Ch. 09 owns the known-short-life case).

### Enforced boundaries cost more than unenforced ones

Expressing the graph in the type system, as `querier` does, is nearly free. Expressing it as package or assembly walls forces exports and mapping code — a real bill, worth paying at some team sizes and not at others (Ch. 18).

### The line shape is seductive

Once a team owns the word "layer," everything becomes one, including things that are stages, cross-cutting concerns, or nothing at all. Logging is the standard casualty:

```csharp
// Logging as a layer. One method per method of the thing it wraps,
// and not one of them decides anything.
public class LoggingOrderService : IOrderService {
    private readonly IOrderService _inner;

    public Task<Order> Get(Guid id) {
        _log.LogInformation("Get {Id}", id);
        return _inner.Get(id);
    }

    public Task<Order> Place(OrderRequest r) {
        _log.LogInformation("Place {Customer}", r.CustomerId);
        return _inner.Place(r);
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

The test from Part three applies unchanged: does this thing decide something, or does it forward? Logging forwards. It is not a layer.

---

## How to recognize the failure

**In a codebase:**

- **Two modules that always appear in the same commits.** The directory structure says they are independent and the commit history says they are one unit. Trust the history — it is measuring the unit of change directly.
- **A class whose every method forwards to one other object.** It was invented to fill a slot in a shape, and it charges a file edit on every change while deciding nothing.
- **The same entity re-typed once per layer, with mappers between.** Every boundary that isn't a real dependency boundary still bills you a type and a mapper, plus the bug where someone adds a field to two of the three (Ch. 18).
- **A test that has to construct half the system to exercise one function.** This is the cycle showing up as a fixture: the unit of test has grown to match the unit of dependency, and the fixture is measuring it for you.
- **Two-phase construction** — `a := &A{}; b := &B{a}; a.b = b`. The constructor cannot express the graph, which is the cycle admitting itself, and there is a window where a field is nil.
- **"Partially initialized module" errors, or a static field holding zero.** The runtime version of the same cycle, and the one that reaches production.
- **An `import` at the top of a file that surprises you.** A leaf reaching for something it should not know exists — usually the first of the two edges.
- **An `internal` or `impl` package that everything imports.** A wall with everything on the same side of it is not a wall; the real boundary is somewhere else, unmarked.
- **A published API whose documented and observable behaviour differ.** Hyrum's Law is already running, callers depend on the observable one, and the document is now fiction.

**In a conversation:**

- **"Which layer does this go in?"** — asked about a pipeline stage or a cross-cutting concern, where the question has no answer. The shape is wrong, not the placement.
- **A design defended by the diagram it matches** rather than by what depends on what. Authority substituting for mechanism.
- **"We can't change that, things depend on it."** True, and incomplete — ask how many. Two dependents is an afternoon's work. Forty is a project needing a plan, a deprecation window, and someone to own it. The sentence sounds identical in both cases; the number is the entire difference, and nobody has looked it up.
- **Someone calling an inversion-of-control callback a layering violation.** The call goes up; the dependency does not.
- **Two people arguing about folder structure** when neither has drawn the dependency graph. They are arguing about the Idiom while believing they are arguing about the Law.

The question that catches real damage is not *does this match the diagram?* It is: **can this piece be understood without that piece?**

The first question generates folders. The second finds the cycle.

---

**Next:** chapter 06 does for concurrency what this chapter did for structure — turns "be careful with shared state" into a rule you can check, starting with the fact that check-then-act is not atomic.
