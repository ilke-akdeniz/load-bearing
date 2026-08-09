# Structure: Dependency and Hiding

*This chapter is mostly **Law**, with a **Principle** and an **Idiom** attached — and the attaching is the problem. "Layered architecture" is all three at once under one name, which is why it is simultaneously the most reliable structural advice in software and the source of some of the worst structure you will read.*

## The claim

**The dependency graph must be acyclic**, and **what a module makes observable is what it has committed to** — everything else people say about architecture is a shape or a convention layered on top of those two.

The first is a Law. The second is a Principle with one sharp condition. Neither of them says anything about folders.

## Three claims wearing one name

Say "we use a layered architecture" and you have made three claims at three different levels. Splitting them this way is this book's, not standard vocabulary:

| Claim | Kind | Standing |
|---|---|---|
| If A depends on B, then B must not depend on A — directly or through any chain | **Law** | near-tautology, Grade B (Ch. 04) |
| The parts can be stacked into layering ranks, each depending only on the rank beneath it | **Principle** | true when the graph is that shape, and often it isn't |
| The ideal ranking, top to bottom, is `presentation → business → data`, and each rank becomes a physical boundary | **Idiom** | 1990s enterprise Java and C#, and arbitrary |

Claim two is the one that needs stating carefully, because it has a loose reading and a strict one and only the strict one says anything new. Loosely — "dependencies should flow downward" — it is claim one with a picture attached.

The strict reading needs the word **rank**, so here it is precisely. A rank is a whole number attached to each part, assigned by one rule:

> The **bottom rank** is 1: everything that depends on nothing.
> Every other part sits **one rank above the topmost part it depends on.**

Bottom and top are worth fixing in place, because the numbers run the opposite way to the everyday phrase "high-level code." The bottom rank is the foundation — rank 1, depends on nothing, everything rests on it. The top rank is the entry points, carrying the largest number, depending on everything beneath. `main` is at the top; `money` is at the bottom.

That is all a rank is. Not a folder, not a team, not a tier of importance — a number that falls out of the arrows.

Two things follow, and they are the difference between the two claims:

- **Claim one is exactly the condition that ranks can be assigned at all.** Try the rule on a cycle and it never terminates: A's rank needs B's, which needs A's. Acyclic and rankable are the same property.
- **Claim two adds that every arrow crosses exactly one rank.** Rank 4 may use rank 3. It may not reach down to rank 1, even though nothing about acyclicity forbids that.

The second is a real constraint, most systems do not satisfy it, and Part three works through one that doesn't.

Claim three is where the physical boundary arrives, and it varies by ecosystem in a way worth noticing. In Java and C# it was usually separate projects, assemblies, or shipped libraries; elsewhere it shows up as top-level directories or packages. The mechanism is the same whichever form it takes, and chapter 18 works through what that boundary costs.

Most real architecture damage is a violation of the first. Most harm done by *architecture advocacy* comes from the third, applied to a program whose graph does not have the shape claim two describes — which then generates pass-through classes and mapping code to fill out the ranks.

They are usually taught together and defended together. Separating them is the whole content of this chapter.

## Reading a dependency graph

Two pieces of vocabulary, because the rest of the chapter leans on them and both are usually left implicit.

**An arrow from A to B means A depends on B.** A names B, A cannot be compiled or understood without B, and deleting B breaks A. The arrow points the way the *need* runs.

```text
                 main              fan-in 0, fan-out 2
                ↙    ↘             nothing needs it
         billing      reports      fan-in 1, fan-out 1
                ↘    ↙
                 money             fan-in 2, fan-out 0
                                   it needs nothing
```

**Fan-in** is how many arrows point at you — how many things break if you change. **Fan-out** is how many you point at — how much you need in order to work at all.

"Bottom" means where the arrows terminate: high fan-in, low fan-out, like `money`. Everything needs it; it needs nothing. "Top" means the entry points: low fan-in, high fan-out, like `main`. This is the sense in which the rest of the chapter says *put stable things at the bottom* — it is a claim about fan-in, not about file layout or importance.

One warning, because it causes the most confusion in review: **this graph is about source-level dependency, not about who calls whom at runtime.** The two usually agree. Where they disagree, the graph is what matters, and the boundary section on inversion of control works through the case.

### The nodes can be anything you handle separately

The claims in this chapter are often heard as being about "layers," or about services, or about whatever unit the reader's current architecture diagram happens to use. They are not. The graph exists at every size at once:

```text
functions → types → files → packages → assemblies → libraries → services
```

A cycle between two functions is the same structural fact as a cycle between two services. What changes with size is **what detects the violation** and **how much it costs**, not whether the Law binds.

Note that "layer" is absent from that list, deliberately. A layer is a *rule about which direction arrows may go*, not a size — a layer might be one function or forty packages. Treating it as a size is how the third of the three claims above gets smuggled in.

The one thing that does vary with size is whether the two nodes are ever handled apart, and that turns out to be the whole question of when the Law goes quiet. The boundary section returns to it.

---

## The demonstration

### Part one: a cycle, and what notices it

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
two functions, Go           compiles. No warning, no error, ever.
two package-level vars, Go  build error: initialization cycle for A
two packages, Go            build error: import cycle not allowed
two assemblies, C#          build error: circular project reference
two modules, Python         works or fails, depending on which one
                            you import first
two modules, CommonJS       silently produces wrong values
```

Six outcomes for one structural fact. Go is the strictest of these and it is still partial: it rejects an import cycle between packages and an initialization cycle between package-level variables, but two mutually recursive *functions* in one file compile without comment. The detector runs where the language happened to put a boundary.

The bottom two rows are the dangerous ones, and they are worth seeing run.

The Law does not care about any of this. The compiler is a partial detector operating at whatever granularity that language happens to check. **The damage is the same at every granularity; only the detection varies.**

### What the damage actually is

That sentence is worth cashing out, because "damage" is doing a lot of work and most of it is not what people expect.

**First, the small part: cycles that crash.**

A cycle across module boundaries can break initialization, because something has to be built first and a cycle says nothing can be. Python shows it plainly:

```python
# a.py
BASE = 5          # defined BEFORE the import
import b
TIMEOUT = b.LIMIT * 2

# b.py
import a
LIMIT = a.BASE + 1
```

Import `a` first and it works — `TIMEOUT` is 12. Import `b` first and it does not:

```text
AttributeError: module 'b' has no attribute 'LIMIT'
```

The asymmetry is worth seeing, because it is the whole reason this bug survives. Entering through `a` means `BASE` is already set by the time `b` runs and reaches back into the half-built `a`. Entering through `b` means `a` starts running immediately, gets to `b.LIMIT` before `b` has defined it, and fails. **Same code, same machine, and the outcome is decided by which module the process happened to touch first** — so it passes every test and fails in production, where the entry point is different.

Note also what makes the placement of `BASE` load-bearing: move it below the `import b` line and *both* orders fail. The bug's behaviour depends on the order of lines within a file, which is not a property anyone tracks.

**A worse version: cycles that produce wrong values in silence.**

Node's CommonJS modules do not raise at all. A module mid-initialization hands out a partially filled `exports` object, and reads of anything not yet assigned come back `undefined`:

```javascript
// a.js
const b = require('./b');
exports.TIMEOUT = b.LIMIT * 2;

// b.js
const a = require('./a');
exports.LIMIT = 5;
exports.DOUBLE = a.TIMEOUT * 2;
```

```text
require a first  →  a.TIMEOUT = 10    b.DOUBLE = NaN
require b first  →  a.TIMEOUT = NaN   b.DOUBLE = NaN
```

No exception, no stack trace, a warning on stderr that nobody reads, and a number that is wrong in a different way depending on entry order. C# and Java have the same shape in static initializers: a type initializer that re-enters itself observes its own fields at their default values, so instead of an exception you get a field silently holding zero.

That class of bug is real, and the silent version is genuinely nasty. It is also the *minority* of the damage, and if it were the whole argument, "avoid cycles" would be a tip rather than a Law.

**Second, the large part: cycles that never crash at all.**

Assume the program is correct, fast, and stable. The cost still arrives — not at runtime, but on every future change.

Take a system with two modules that depend on each other. `billing` charges merchants and needs to read a merchant's plan, which `accounts` owns. `accounts` decides whether a merchant may be suspended and needs to ask `billing` whether that merchant is behind on payments. Each genuinely needs something the other has, so each imports the other. Nothing here is broken, and no test fails.

Then a ticket arrives: *make the payment retry limit configurable per merchant.*

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

### Does the damage actually spread?

The usual claim at this point is that dependency damage compounds — that a cycle grows on its own until nothing can be moved. That claim needs splitting, because half of it is mechanical and half of it is a habit, and only the first half is this chapter's business.

The reasonable objection is: if `billing` and `accounts` are tangled, why should that spread? A third module `C` that needs both can simply take both, and no new cycle is created.

That is correct. **A cycle does not spawn further cycles by itself, and injecting both into `C` creates nothing new.** The graph does not deteriorate unattended.

What *is* mechanical is narrower and still expensive: **weight is inherited.** Every new dependent of `billing` also depends on `accounts`, transitively, whether or not it names it. `C` cannot be compiled, tested, extracted, or reasoned about without both — and neither can anything that depends on `C`. The cycle's cost is now paid at every one of those sites, and that follows from the graph rather than from anyone's discipline.

What is *not* mechanical, but is common enough to be worth naming, is that the first cycle makes placement ambiguous. Once `billing` and `accounts` are effectively one unit, the question "which of these does this new code belong in?" has no principled answer, so it gets answered by convenience — and answers by convenience produce edges in whatever direction was handy. That is a tendency the first cycle creates, not a law it enforces. Discipline resists it. Discipline cannot do anything about the inherited weight.

So the honest version: a missing test is a static cost that does not get worse on its own, and a cycle is a cost that is re-paid by every future dependent. That is enough to justify the Law without claiming the graph rots by itself.

### Breaking the cycle

The cycle shows up first at the construction site:

```go
type Accounts struct{ billing *Billing }
type Billing struct{ accounts *Accounts }

a := &Accounts{}
b := &Billing{accounts: a}
a.billing = b // two-phase construction: neither can be built first
```

That last assignment is the tell. There is now a window in which `a.billing` is nil, and nothing in the type system says when the window closes — anything running during it sees a half-built object. Moving the wiring out to a caller does not help, because it changes who *constructs*, not who *depends*: `Billing`'s type still names `Accounts`, so the compiler still needs `Accounts` in hand, the test still has to build one, and the reader still has to know both.

What removes the edge is an interface **declared by the module that needs it**:

```go
package billing

// billing states what it requires, in its own terms.
type PlanLookup interface {
	PlanFor(ctx context.Context, merchantID uuid.UUID) (Plan, error)
}

type Billing struct{ plans PlanLookup }
```

`accounts` implements `PlanLookup`. Now `billing` depends on nothing, `accounts` depends on `billing`, and there is one edge where there were two. Construction is single-phase, `billing` tests with a five-line fake, and `billing` can be extracted into its own service without dragging anything.

The difference is not that an interface appeared. It is **which module owns it.** An interface declared by `accounts` and handed to `billing` would leave the arrow pointing exactly where it was; what reverses the direction is `billing` declaring what it needs, in its own terms. That distinction is the whole of dependency inversion, and it is the reason `net/http` may call up into your handler without a violation.

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

FlowCore's graph, for comparison, with arrows pointing down at what is needed:

```text
A LINE

rank 3     service
              ↓
rank 2      store
              ↓
rank 1      errmap
```

The compiler's, drawn the same way:

```text
NOT A LINE

rank 4     codegen
              ↓
rank 3    typecheck
              ↓
rank 2     printer        parser
              ↓              ↓
rank 1        └───→ ast ←────┘

           plus two arrows that skip ranks:
              codegen   ──→ ast    (4 to 1)
              typecheck ──→ ast    (3 to 1)
```

Read these as dependency arrows, not as the order things happen in. Source text flows *forward* through parser, typecheck, and codegen at runtime; the arrows here run the other way, from each part to what it needs in order to compile. That is why `codegen` sits at the top rather than the end.

The two skipping arrows are pulled out on their own because they are what the rest of this section is about. The two surprising ones in the main picture are what make the shape.

**`printer` depends on `ast` and on nothing else.** It is the inverse of `parser` — one turns text into a tree, the other a tree into text. Neither calls the other. Ask which is above the other and the question is empty; they are peers over a shared type.

**`typecheck` depends on `printer`.** To emit `cannot use name (string) as int`, the type checker has to render the offending expression back into source text. That is printing, and there is no reason to have two implementations of it.

So `ast` sits at the bottom with four things depending on it and nothing below. That is not an accident of drawing — it is the shape you want, because `ast` is the most stable part and everything else is a consumer of it. Adding a sixth part later — a linter, a documentation generator, a language server — costs exactly one new edge into `ast` and changes nothing that already exists.

Be precise about what fails here, because the graph is acyclic and ranks *can* be assigned. Run the rule from earlier — bottom rank 1 for whatever needs nothing, and every other part one rank above the topmost thing it needs:

```text
                                        topmost
part       needs                        thing needed   rank
ast        nothing                      —                 1
parser     ast (1)                      1                 2
printer    ast (1)                      1                 2
typecheck  printer (2), ast (1)         2                 3
codegen    typecheck (3), ast (1)       3                 4
```

Every arrow now runs from a higher number to a lower one, so claim one is satisfied. The graph is acyclic, as promised.

What fails is claim two. It requires every arrow to cross **exactly one** rank, and two arrows here do not: `typecheck` reaches from 3 down to `ast` at 1, and `codegen` reaches from 4 down to `ast` at 1. Those are the reaches strict layering forbids, and they are not accidents you could refactor away — every part needs the node types, which is what it means for `ast` to be the shared vocabulary.

The ranks also turn out to carry no meaning. Rank 2 holds `parser` and `printer`, which have nothing in common: one reads text, the other writes it, and neither touches the other. They share a number because they happen to be the same distance from `ast`, which is a fact about counting arrows rather than a statement about abstraction, ownership, or rate of change. There is nothing to call rank 2 — and being unable to name a rank is how you know it is an artifact of the arithmetic rather than a real division.

Now force it anyway, and each way of doing so costs something concrete.

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

The printer is now a parameter passed down through `typecheck` into every function that might report an error — four call levels deep, in service of a diagram. This is the pass-through class, and nobody set out to write it — it was the only way to satisfy a shape that was wrong.

It also supplies the test that catches the type, here and later in the chapter: **does this thing decide something, or does it only forward?** `CompilationService` decides nothing — every line of it hands work to something else. A part that forwards is not a part.

All three costs come from the same mistake: the real graph was a DAG, and a line was imposed on it. The failure mode is not sloppiness — it is discipline applied to the wrong claim.

Sharpened:

> **Managed, acyclic dependency direction is the Law. Layering is its most common shape, not its definition.**

### Part four: what you expose

Parts one to three were about which way the arrows point. This one is about how many arrows exist at all.

That is the connection between the chapter's two claims, and it is worth stating plainly because they are usually taught as separate subjects. A cycle is two arrows where there should be one. Information hiding is about not creating an arrow in the first place. Same graph, same cost: a dependency that was never created costs nothing to change, forever.

Parnas, 1972 — the founding paper, and still the clearest statement: decompose a system by what each module *hides*, not by the steps of the process it performs. The value of a module is the decision it keeps to itself, because that is the decision you can change later without telling anyone.

The mechanism is fan-in again. A decision that nothing can observe has a fan-in of zero and is therefore free to change. A decision that is visible has as many dependents as care to look, and nobody tells you when someone starts looking.

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

Exporting `querier` would have bought nothing and tied the library's freedom to a third party's release schedule.

### "Doesn't dependency injection contradict hiding?"

It looks like it should. Injection means the caller has to be told about the thing being injected, and hiding says to know as little as possible. Both cannot be right.

The apparent conflict comes from asking *who knows more*. Ask instead *whose decisions are being respected*, and it dissolves.

```go
// Without injection: billing reaches through the boundary and makes
// decisions that were never its to make.
func NewBilling() *Billing {
	pool, _ := pgxpool.New(ctx, os.Getenv("DATABASE_URL"))
	return &Billing{plans: &PostgresPlanStore{pool: pool}}
}
```

Four decisions belonged to whoever owns plan storage: that plans live in Postgres, that the connection comes from a pool, that the pool is configured from that environment variable, that `PostgresPlanStore` is the implementation. `billing` has helped itself to all four. If plan storage moves to a cache, or the pool is shared, or the variable is renamed, `billing` breaks — not because its own job changed, but because it was depending on decisions it had no business holding.

```go
// With injection: billing states what it needs to do its own job,
// and stops there.
func NewBilling(plans PlanLookup) *Billing {
	return &Billing{plans: plans}
}
```

Read this version as `billing` saying: *those were never my decisions. Where plans are stored, how they are fetched, what is configured — none of that is my business. I need exactly the operations in this interface in order to decide what I actually decide, which is what to charge.*

That is the resolution. Hiding is about what a *module* is coupled to, and injection reduces that: `billing` unlearned four decisions and learned one interface. What grows is what the **composition root** knows, and the composition root is one file whose entire job is knowing how the pieces fit — the one place where knowing everything is correct.

The contradiction only survives if you read hiding as "less information anywhere." Parnas proposed something narrower: each module hides a decision, and other modules stop depending on it. Injection is how a module *declines to hold* a decision that belongs elsewhere.

### Hyrum's Law

**With a sufficient number of users, every observable behaviour of your system will be depended upon by somebody, regardless of what you documented.** The name comes from Hyrum Wright at Google; the observation is standard and uncontroversial.

Not the documented behaviour. The observable one. Iteration order of a map that you never promised was stable. The exact wording of an error message, parsed by someone's log alert. The fact that a call currently takes 40ms, which somebody's timeout was tuned against. Whether IDs happen to be sequential.

A user testing against your implementation cannot distinguish your contract from your behaviour — the running system is the only specification they have direct access to. So they encode what they observe, and after enough users, every observable is encoded somewhere.

Two practical corollaries.

**Any behaviour you can't afford to keep, you must prevent from being observed.** Randomizing map iteration order, as Go does, is Hyrum's Law taken seriously: the only way to keep a freedom is to make its absence impossible to depend on.

**Your export surface is a liability inventory, not a feature list.** Every capital letter is a commitment you did not necessarily mean to make, and taking one back is a breaking change even if no document ever mentioned it.

Worth noticing that two of the book's kinds are sitting side by side here, because the names invite confusion. Hyrum's Law is a **Law** in this book's sense — though an empirical regularity about what people do, not a theorem, which is a distinction chapter 04 grades. What to do about it is a different claim.

That claim — hide what you cannot afford to commit to — is a **Principle**, and it has a sharp condition: *you do not control your callers.* When you do control every caller — a single application, one team, one repository, one deploy — the condition weakens, and hiding starts trading against convenience rather than against catastrophe. This is why library design and application design genuinely differ, and why advice from one arrives wrong in the other. (Chapter 03 takes control-of-callers seriously as a Force in its own right.)

---

## Why it holds

### Both halves are fan-in

Changing something costs roughly in proportion to how many things depend on it. A leaf with fan-in zero is free to change: nothing else can notice. Fan-in forty costs forty inspections, and it is paid on *every* change, not once.

Both halves of this chapter are that one number, approached from two directions.

**A cycle makes the number mutual, and no discipline reduces it.** If A and B point at each other, each is the other's dependent. Neither can be read, tested, built, or moved without the other, and nothing short of removing an arrow changes that.

**Exposure makes the number unknowable.** Inside your repository `grep` gives you the count, and the count tells you what a change costs. Once something is published you cannot count at all — and Hyrum's Law says the real number is larger than the documented one, because people depend on what they can observe rather than on what you wrote down.

That is why direction and hiding belong in one chapter. They are the only two things you control about the graph — which way the arrows point, and how many there are — and both are priced the same way.

### Stability belongs at the bottom

The highest-fan-in node is the most expensive to change, so it should be the one that changes least. Not because stability is a virtue, but because you pay for instability there over and over.

This is the real content behind "depend on abstractions," and that phrase is badly misleading, because it is routinely read as *add an interface*. What lowers the bill is **stability**, not indirection:

```text
   40 modules                    40 modules
      ↓ ↓ ↓                        ↓ ↓ ↓
      Money                     IUserService

  fan-in 40, fan-out 0        fan-in 40, fan-out 0
  last changed 4 years ago    last changed this sprint
  cost per year: nothing      cost per year: 40 inspections,
                              three times over
```

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

Both sit at the bottom with the same fan-in. The second is an interface and buys nothing: every added method is a change at the highest-fan-in point in the system, which is the exact cost the advice exists to avoid. The `I` prefix made it *look* like a stable boundary while the concept behind it was still moving.

So the usable form is: *put the thing that changes least at the bottom.* Sometimes that is an interface. Often it is a data type, a constant, or a function signature that has earned its shape. Whether it is an interface is not the question.

### Why one is a Law and the other a Principle

They share a cost model and they do not share a standing, which is worth being exact about.

The acyclicity claim follows from what a graph is. Its only precondition is that the two nodes are things you handle apart — and where that fails, the claim goes quiet rather than going wrong. No situation makes it false.

The hiding claim has a precondition about the world: whether you control your callers. Change that and the advice does not go quiet, it can reverse — the ECS case below is one where exposing the representation is the correct answer and hiding it is the mistake.

That is the difference chapter 02 draws, arrived at from the mechanism rather than asserted: **a Law can be irrelevant but never wrong; a Principle can be wrong.**

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

The test is not "is there a cycle in the call graph." It is: **will these ever be understood, tested, or changed apart?** If the honest answer is no, the cycle is free. If the honest answer is "not today, but yes within a year," the cost has not been avoided — it has been postponed, and by then there will be more code depending on both.

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

That is a genuine loss, accepted deliberately. You gave up the ability to change the representation quietly, and what you bought is the speed that comes from every system agreeing on it.

The Force is the memory hierarchy. Where it dominates, "hide the representation" inverts: hiding it is precisely what you must not do. Chapter 20 works through the rest of that domain's inversions.

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

It is fine, and it is the same move `billing` made. Read `net/http` as saying: *I cannot decide what any future client's request handling should do, and it is not my job to. I need exactly one operation — hand me a request and a place to write, get a response back — in order to decide what I actually decide, which is how to speak HTTP.*

So `net/http` does not depend on your code. It depends on `Handler`, an interface **it declares itself**, and your code depends on that same interface. The *call* goes up while the *dependency* goes down, because the interface sits at the bottom and both parties point at it. Plugin systems, callback APIs, and UI frameworks are all built this way: in a framework, inversion of control is not an implementation detail, it is the product.

**Injection and inversion are not the same thing**, and the pages above have now shown both, so it is worth separating them in one place.

- **Dependency injection is about who constructs.** A dependency is supplied from outside rather than built inside. It changes where the `new` happens and nothing else — you can inject a concrete `*PostgresPlanStore` and the arrow still points from `billing` at Postgres.
- **Dependency inversion is about who declares the interface.** The module that *needs* the operation defines it, in its own vocabulary, and the provider implements it. That reverses the arrow.

Only the second changes the graph. The two travel together so often that they get one name in conversation, but injecting a concrete type buys you a seam for testing and nothing structural, while inversion is what lets `billing` be extracted or `net/http` be written before your handler exists.

The diagnostic for both: draw the graph in terms of *what breaks when you delete something*, not what calls what at runtime. Delete your handler and `net/http` still compiles. That settles it.

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

There are four ways to pay, and they are genuinely different bills. All four are shown on the same cycle — the one from earlier, reduced to the two calls that create it:

```go
package billing
func (b *Billing) Charge(m uuid.UUID) error {
	plan := b.accounts.PlanFor(m) // billing → accounts
	// ...
}

package accounts
func (a *Accounts) Suspend(m uuid.UUID) error {
	if a.billing.IsBehind(m) { // accounts → billing
		return ErrBehindOnPayments
	}
	// ...
}
```

Each option below removes the second arrow, `accounts → billing`, and keeps the first. That is the mirror of the fix shown earlier, which removed the other one — either arrow can be the one you turn around, and which you pick is a judgement about which module the operation more naturally belongs to.

**One — `accounts` declares the operation it needs, and `billing` implements it.**

```go
package accounts

// accounts states its requirement in its own vocabulary.
type PaymentStatus interface {
	IsBehind(m uuid.UUID) bool
}

type Accounts struct{ payments PaymentStatus }
```

*The bill:* one more name to know, and "go to definition" lands on a declaration instead of the code that runs. Debugging gains a hop at every such boundary.

**Two — `billing` announces instead of being asked.**

```go
package billing

// billing publishes. It does not know who listens, and it names
// nothing belonging to whoever does.
func (b *Billing) Charge(m uuid.UUID, onBehind func(uuid.UUID)) error {
	// ...
	onBehind(m)
}
```

```go
// main wires the two. Neither package names the other.
billing.Charge(id, accounts.MarkBehind)
```

`accounts` records what it is told and never needs to ask. Note that the callback takes a plain value: if `billing` had published an event *type*, `accounts` would have to import `billing` to receive it, and the arrow would still be there.

*The bill:* the stack trace stops telling you who reacts. Tracing an effect goes from reading up the stack to grepping for subscribers, and subscriber ordering becomes something you have to think about.

**Three — move the shared decision into a third module both depend on.**

```go
package standing // depends on neither

type Tier int

func MaySuspend(t Tier, unpaidCents int64) bool
```

Both callers pass in what they hold, and neither needs the other.

*The bill:* a new place to put things, and a recurring argument about what belongs in it. Note also that `standing` had to declare its own `Tier` rather than accept the caller's — taking `accounts.Plan` would point an arrow straight back and rebuild the cycle. So each caller now translates into this module's vocabulary at the call site. Modules like this attract unrelated code, which is how they end up named `common` or `shared`.

**Four — replace a reference with an identifier.**

The first three break a cycle between *calls*. This one breaks a cycle between *types*, which is the form the same problem takes in data models. Suppose the two packages also hold each other's structs:

```go
package billing
type Invoice struct {
	Merchant *accounts.Merchant // billing → accounts
}

package accounts
type Merchant struct {
	Invoices []*billing.Invoice // accounts → billing
}
```

Neither package compiles without the other, and no method call is involved — the cycle is in the field types alone. Replacing one of the pointers with the identity it stands for removes that arrow:

```go
package billing
type Invoice struct {
	MerchantID uuid.UUID // names no other package
}
```

*The bill:* `invoice.Merchant.Name` becomes a lookup that can fail and can be stale. "What if the merchant was deleted?" is now a question you answer explicitly, where the pointer answered it by existing. Chapter 16 works through the version of this that appears in object-oriented domain models, where the mutual pointers are the design rather than an accident.

Pick deliberately. The failure is paying in interfaces by reflex — an interface at every boundary whether or not the boundary was real, which is how a codebase acquires forty interfaces with one implementation each (Ch. 17 traces where that reflex comes from).

### Hiding costs you the day you need what you hid

Every decision you hide is a decision your users cannot reach when they turn out to need it. A library that exposes a connection pool but not the underlying socket has hidden the socket options too, and the user who needs `TCP_NODELAY` is stuck. This is a real and recurring cost, not a hypothetical one.

The tempting answer is a disclaimer:

```go
// UnderlyingConn returns the raw connection.
//
// NOT covered by this package's compatibility promise. May change or
// disappear in any release, including a patch release.
func (c *Client) UnderlyingConn() net.Conn { return c.conn }
```

**This does not work, and the reason is in this chapter.** Hyrum's Law does not read comments. Ship that method, and people call it; once they call it, removing it breaks them, and a disclaimer changes only whose fault that is. You have exported the field and written a note saying you didn't. The freedom the comment claims to preserve was already gone the moment the method existed.

So the honest options are three, and none of them is a disclaimer.

**One — find the actual need and expose exactly that.** The user did not want "the connection," they wanted a socket option. Ship the option, with the same compatibility promise as everything else in the package:

```go
// Supported, documented, and kept.
func (c *Client) SetNoDelay(on bool) error
```

One method, one narrow promise, and one you can keep across versions because you control what is behind it. Most escape-hatch requests turn out to be this once someone asks what the caller was actually trying to do.

**Two — if the need really is open-ended, lend the internals instead of giving them away.** The standard library does this. From `database/sql`:

```go
// Raw is a real method of *sql.Conn in the standard library.
func (c *Conn) Raw(f func(driverConn any) error) error
```

Read it as: *you give me a function, and I will call it with the driver's own connection object.* You never receive the connection as a return value — it is handed to your function as an argument, and taken back the moment your function returns.

```go
err := conn.Raw(func(dc any) error {
	pg, ok := dc.(*pgx.Conn) // the driver's concrete type
	if !ok {
		return errors.New("not a pgx connection")
	}

	return pg.CopyFrom(ctx, ...) // do the unexposed thing, here and now
})
```

The difference from a disclaimer is not politeness, it is control. `database/sql` still owns the connection's lifetime: it knows exactly when you hold it, it takes it back afterwards, and it can return it to the pool. What the package promised — *you may reach the driver, for the duration of a call* — is a promise it can keep in every future version, because nothing about the driver's identity or lifetime was ever handed over. Compare `UnderlyingConn`, which gives you a pointer and hopes.

The cost is real and worth naming: your users now write type assertions against a driver you did not choose, so their code is coupled to the driver rather than to you. That is the correct place for that coupling to sit.

**Three — say no.** If serving the need would commit you to something you cannot hold across versions, "we don't support that" is a legitimate answer and a more honest one than a method with a warning label. Users who genuinely cannot proceed will fork, and a fork costs you nothing you were entitled to: it is visible, it is theirs to maintain, and it does not constrain your next release.

All three have the same property, and the disclaimer is the only option that lacks it: **what the package promises is what the package can deliver.** That is the whole difference, and it is why the warning label is a marketing answer rather than an engineering one.

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

### Everything starts looking like a layer

Once a team owns the word "layer," everything becomes one, including things that are stages, cross-cutting concerns, or nothing at all. Logging is the usual one:

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
- **Two-phase construction** — `a := &A{}; b := &B{a}; a.b = b`. The constructor cannot express the graph, and there is a window in which a field is nil.
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
