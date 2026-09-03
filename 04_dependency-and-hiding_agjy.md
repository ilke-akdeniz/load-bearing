# Dependency and Hiding

## The claim

**A change is expensive in proportion to how many things depend on what you are changing. A cycle makes that count irreducible; a published surface makes it uncountable.**

## The number

**An arrow from A to B means A depends on B.** A names B, A cannot be compiled or understood without B, and deleting B breaks A. The arrow points the way the *need* runs.

```text
                 main              fan-in 0, fan-out 2
                ↙    ↘             nothing needs it
         billing      reports      fan-in 1, fan-out 1
                ↘    ↙
                 money             fan-in 2, fan-out 0
                                   it needs nothing
```

**Dependency fan-in** is how many arrows point at you — how many things break if you change. **Dependency fan-out** is how many you point at — how much you need in order to work at all.

Dependency fan-in is the number in the claim. A leaf with fan-in zero is free to change: nothing else can notice the change. A fan-in of forty costs forty inspections, and it is paid on *every* change, not once.

**A cycle makes fan-in irreducible.** If A and B point at each other, each is the other's dependent. Neither can be read, tested, built, or moved without the other, and nothing short of removing an arrow changes that.

**Exposure makes it uncountable.** Inside your repository `grep` gives you the count, and the count tells you what a change costs. Once something is published you cannot count at all, and the real number is larger than the documented one, because people depend on what they can observe rather than on what you wrote down.

That is why the dependency direction and information hiding belong in one chapter. They are the two things you control about the graph — which way the arrows point, and how many of them there are — and both are priced the same way.

"Bottom" means where the arrows terminate: high fan-in, low fan-out, like `money`. Everything needs it; it needs nothing. "Top" means the entry points: low fan-in, high fan-out, like `main`. This is the sense in which the rest of the chapter says *put stable things at the bottom* — a claim about fan-in, not about file layout or importance.

**The graph is source-level, and its nodes can be anything you handle separately.** Nodes exist at every size at once — functions, types, files, packages, assemblies, libraries, services — and a cycle between two functions is the same structural fact as a cycle between two services. What changes with size is what detects the violation and how much it costs, not whether the Law binds. Note that "layer" is not a size on that list: a layer is a rule about which direction arrows may go, and might be one function or forty packages.

---

## The demonstration

### A cycle, and what notices it

Two pieces of a workflow library. A store that writes rows, and a service that composes writes into a transaction.

```go
// The service calls down. Normal.
func (c *Catalog) Create(ctx context.Context, definition WorkflowDefinition) error {
	tx, err := c.pool.Begin(ctx)
	if err != nil {
		return err
	}

	// defer runs this when the function returns, however it returns —
	// so the rollback is a no-op once the commit below has succeeded.
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
func insertStepDefinition(ctx context.Context, q querier, catalog *Catalog, step StepDefinition) error {
	if !catalog.validate(step) {
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

The Law does not care about any of this. The compiler is a partial detector operating at whatever granularity that language happens to check. **The damage is the same at every granularity; only the detection varies.**

### What the damage actually is

Most of it is not what people expect.

**The small part: cycles that crash.** A cycle across module boundaries can break initialization, because something has to be built first and a cycle says nothing can be. Python shows it plainly:

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

The asymmetry is the whole reason this bug survives. Entering through `a` means `BASE` is already set by the time `b` runs and reaches back into the half-built `a`. Entering through `b` means `a` starts running immediately, gets to `b.LIMIT` before `b` has defined it, and fails. **Same code, same machine, and the outcome is decided by which module the process happened to touch first** — so it passes every test and fails in production, where the entry point is different. Move `BASE` below the `import b` line and *both* orders fail: the behaviour depends on the order of lines within a file, which is not a property anyone tracks.

**A worse version: cycles that produce wrong values in silence.** Node's CommonJS modules do not raise at all. A module mid-initialization hands out a partially filled `exports` object, and reads of anything not yet assigned come back `undefined`:

```javascript
// a.js
const b = require('./b');
exports.TIMEOUT = b.LIMIT * 2;
```

```javascript
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

That class of bug is real. It is also the *minority* of the damage, and if it were the whole argument, "avoid cycles" would be a tip rather than a Law.

**The large part: cycles that never crash at all.** Assume the program is correct, fast, and stable. The cost still arrives, on every future change.

`billing` charges merchants and needs to read a merchant's plan, which `accounts` owns. `accounts` decides whether a merchant may be suspended and needs to ask `billing` whether that merchant is behind on payments. Each genuinely needs something the other has, so each imports the other. Nothing is broken, and no test fails. Then a ticket arrives: *make the payment retry limit configurable per merchant.*

- **The test you expected to write does not exist.** To test the new retry logic you need a merchant, which needs `accounts`, which needs `billing`, which needs a database. What should have been a unit test is now an integration test with fixtures, so it is slower, flakier, and less likely to be written at all.
- **You cannot read one without the other.** The retry code calls into `accounts`, which calls back into `billing`. Following it means holding both in your head, so the fifteen-minute change becomes a morning.
- **You cannot move it.** The roadmap says billing becomes its own service. It cannot: extracting `billing` drags `accounts` with it, and extracting both is a different project than the one that was estimated.
- **You cannot delete it.** Six months later the plan lookup is dead code, but nothing proves that, because the call graph loops.
- **The next person adds a second path.** They read `billing`, do not understand why it calls back into `accounts`, and write their own retry limit rather than disturb it. Now there are two, and they disagree.

Every one of those is the same fact in a different costume: **the unit of comprehension, of test, and of change is now `billing`+`accounts`, whatever the file layout says.** That is why this is a Law rather than a strong opinion — it is a property of graphs, restated in the vocabulary of software, and nothing about a language, a team, or a decade changes it.

None of it is a bug report. It shows up as estimates being wrong by a factor of five, as a refactor that gets abandoned, as a service extraction that slips two quarters. **The damage is denominated in future change, not in incorrect output** — which is why it accumulates unnoticed, and why no single commit looks like the culprit.

### Breaking the cycle

The cycle shows up first at the construction site:

```go
type Accounts struct{ billing *Billing }
type Billing struct{ accounts *Accounts }

accounts := &Accounts{}
billing := &Billing{accounts: accounts}
accounts.billing = billing // two-phase construction: neither can be built first
```

That last assignment is the tell. There is now a window in which `accounts.billing` is nil, and nothing in the type system says when the window closes. Moving the wiring out to a caller does not help, because it changes who *constructs*, not who *depends*: `Billing`'s type still names `Accounts`, so the compiler still needs `Accounts` in hand, the test still has to build one, and the reader still has to know both.

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

### Anyone can depend on what you expose

Everything so far has been about which way the arrows point. This is about how many exist at all — the second half of the same number. A cycle is two arrows where there should be one. Information hiding is about not creating an arrow in the first place. A dependency that was never created costs nothing to change, forever.

Parnas, 1972 — the founding paper, and still the clearest statement: decompose a system by what each module *hides*, not by the steps of the process it performs. The value of a module is the decision it keeps to itself, because that is the decision you can change later without telling anyone.

The mechanism is fan-in again. A decision that nothing can observe has a fan-in of zero and is therefore free to change. A decision that is visible has as many dependents as care to look, and nobody tells you when someone starts looking. That last point is not a guess: with enough users, every observable behaviour of a system ends up depended on regardless of what was documented, which is Hyrum's Law — [chapter 03](03_grading-a-law_q5c6.md) grades it and works through what Go and Python each did about it.

So **your export surface is a liability inventory, not a feature list.** Every exported identifier — a capital letter in Go, `public` in C# — is a commitment you did not necessarily mean to make, and taking one back is a breaking change even if no document mentioned it. The export surface, not the design document, is the real API:

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

Hiding is about what a *module* is coupled to, and injection reduces that: `billing` unlearned four decisions and learned one interface. What grows is what the **composition root** knows, and the composition root is one file whose entire job is knowing how the pieces fit — the one place where knowing everything is correct. It is `func main` in Go, `Program.cs` in a .NET application, and the `@Configuration` class in a Spring one. Which of those needs a container to do the assembling, and which does it by hand, varies by ecosystem for reasons [chapter 21](21_idioms_7nkn.md) works through.

The contradiction only survives if you read hiding as "less information anywhere." Parnas proposed something narrower: each module hides a decision, and other modules stop depending on it. Injection is how a module *declines to hold* a decision that belongs elsewhere.

---

## Why the claim holds

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

The hiding claim has a precondition about the world: whether you control your callers. Change that and the advice does not go quiet, it can reverse — the case below is one where exposing the representation is the correct answer and hiding it is the mistake. It comes from games, where an **entity-component-system** layout, ECS for short — state held in parallel arrays by field rather than in objects by entity — is the standard way to build a simulation with a hundred thousand moving things in it.

That is the difference [chapter 01](01_the-five-kinds_cjx4.md) draws, arrived at from the mechanism rather than asserted: **a Law can be irrelevant but never wrong; a Principle can be wrong.**

---

## Where the claim doesn't apply

Three boundaries.

### The Law goes inert when nothing is ever separated

The cycle argument is entirely about A and B being *separate units of comprehension, test, and change*. Where they are not separate, the Law has nothing to act on.

Mutually recursive functions are a cycle:

```go
func parseExpr(p *parser) node { ... p.parseTerm() ... }
func parseTerm(p *parser) node { ... p.parseExpr() ... }
```

Nobody sane calls this an architecture violation, and the reason is precise rather than a matter of degree. A cycle hurts because it forces two things you wanted to handle separately to be handled as one. Here there is nothing to force together: you were never going to read one without the other, test one without the other, or change one's signature without the other's. They were a single unit before the cycle existed, so the cycle takes nothing away.

The same goes for two types in one file that reference each other, or a 200-line CLI that has one layer because there is nothing to order. This is a Law that is true and inert ([Ch. 01](01_the-five-kinds_cjx4.md)), not a Law being bent.

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
    public void Update(float deltaTime) { position += velocity * deltaTime; lifetime -= deltaTime; }
}

Particle[] particles;                          // 100,000 of them
foreach (var particle in particles) particle.Update(deltaTime);
```

The entity-component-system version, which deliberately does the opposite:

```csharp
// Nothing owns anything. State is parallel arrays, public, flat.
Vector3[] position;   // 100,000
Vector3[] velocity;   // 100,000
Color[]   tint;       // 100,000 — never touched by this loop
float[]   lifetime;   // 100,000

for (int i = 0; i < count; i++) {
    position[i] += velocity[i] * deltaTime;
    lifetime[i] -= deltaTime;
}
```

The second is not a worse-encapsulated version of the first. It is a different decomposition, and it wins by a margin that has nothing to do with taste: the first loop drags `tint` and every other unused field through cache on every iteration, and the second touches only the bytes it needs. ([Chapter 08](08_scale_637f.md) owns the arithmetic and the benchmark; the span between cache and main memory is where the whole margin comes from.)

Be exact about what was traded away. In the class version the field layout is private: you could reorder the fields, widen `lifetime` to a double, or delete `tint` entirely, and no other file would need editing. In the array version the layout *is* the interface — a dozen systems index those arrays directly, so changing the layout means editing every one of them.

That is a genuine loss, accepted deliberately. You gave up the ability to change the representation quietly, and what you bought is the speed that comes from every system agreeing on it.

The Force is the memory hierarchy. Where it dominates, "hide the representation" inverts: hiding it is precisely what you must not do. [Chapter 20](20_six-profiles_dnkz.md) works through the rest of what that force profile overturns.

Note carefully what has *not* inverted. The ECS dependency graph is still acyclic — systems depend on component arrays, and the arrays depend on nothing. The Law holds untouched while the Principle turns over completely, which is the difference [chapter 01](01_the-five-kinds_cjx4.md) draws, seen in the wild.

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

## What the claim costs

### Breaking a cycle is never free

There are four ways to pay, and they are genuinely different bills. All four are shown on the same cycle — the one from earlier, reduced to the two calls that create it:

```go
package billing
func (b *Billing) Charge(merchantID uuid.UUID) error {
	plan := b.accounts.PlanFor(merchantID) // billing → accounts
	// ...
}

package accounts
func (a *Accounts) Suspend(merchantID uuid.UUID) error {
	if a.billing.IsBehind(merchantID) { // accounts → billing
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
	IsBehind(merchantID uuid.UUID) bool
}

type Accounts struct{ payments PaymentStatus }
```

*The bill:* one more name to know, and "go to definition" lands on a declaration instead of the code that runs. Debugging gains a hop at every such boundary.

**Two — `billing` announces instead of being asked.**

```go
package billing

// billing publishes. It does not know who listens, and it names
// nothing belonging to whoever does.
func (b *Billing) Charge(merchantID uuid.UUID, onBehind func(uuid.UUID)) error {
	// ...
	onBehind(merchantID)
}
```

```go
// main wires the two. Neither package names the other.
billing.Charge(merchantID, accounts.MarkBehind)
```

`accounts` records what it is told and never needs to ask. Note that the callback takes a plain value: if `billing` had published an event *type*, `accounts` would have to import `billing` to receive it, and the arrow would still be there.

*The bill:* the stack trace stops telling you who reacts. Tracing an effect goes from reading up the stack to grepping for subscribers, and subscriber ordering becomes something you have to think about.

**Three — move the shared decision into a third module both depend on.**

```go
package standing // depends on neither

type Tier int

func MaySuspend(tier Tier, unpaidCents int64) bool
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

*The bill:* `invoice.Merchant.Name` becomes a lookup that can fail and can be stale. "What if the merchant was deleted?" is now a question you answer explicitly, where the pointer answered it by existing. [Chapter 16](16_behaviour-placement_z47a.md) works through the version of this that appears in object-oriented domain models, where the mutual pointers are the design rather than an accident.

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

**This does not work, and the reason is the one above.** A comment cannot stop a behaviour from being observed. Ship that method, and people call it; once they call it, removing it breaks them, and a disclaimer changes only whose fault that is. You have exported the field and written a note saying you didn't. The freedom the comment claims to preserve was already gone the moment the method existed.

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
err := conn.Raw(func(driverConn any) error {
	// The comma-ok form: ok reports whether the value really was
	// that type, instead of panicking when it was not.
	pgxConn, ok := driverConn.(*pgx.Conn) // the driver's concrete type
	if !ok {
		return errors.New("not a pgx connection")
	}

	return pgxConn.CopyFrom(ctx, ...) // do the unexposed thing, here and now
})
```

The difference from a disclaimer is not politeness, it is control. `database/sql` still owns the connection's lifetime: it knows exactly when you hold it, it takes it back afterwards, and it can return it to the pool. What the package promised — *you may reach the driver, for the duration of a call* — is a promise it can keep in every future version, because nothing about the driver's identity or lifetime was ever handed over. Compare `UnderlyingConn`, which gives you a pointer and hopes.

The cost is real and worth naming: your users now write type assertions against a driver you did not choose, so their code is coupled to the driver rather than to you. That is the correct place for that coupling to sit.

**Three — say no.** If serving the need would commit you to something you cannot hold across versions, "we don't support that" is a legitimate answer and a more honest one than a method with a warning label. Users who genuinely cannot proceed will fork, and a fork costs you nothing you were entitled to: it is visible, it is theirs to maintain, and it does not constrain your next release.

All three have the same property, and the disclaimer is the only option that lacks it: **what the package promises is what the package can deliver.**

### Acyclicity discipline slows some changes down

Sometimes the cheap fix genuinely is to let the lower thing call up.

```go
// Ten minutes. Ship it before lunch.
func insertStepDefinition(ctx context.Context, q querier, catalog *Catalog, step StepDefinition) error {
	if !catalog.validate(step) {
		return ErrInvalidStep
	}
	// ...
}
```

```go
// An afternoon. Validation moves above both, and the store
// never learns that Catalog exists.
func (c *Catalog) Create(ctx context.Context, definition WorkflowDefinition) error {
	if err := validate(definition); err != nil {
		return err
	}

	for _, step := range definition.Steps {
		if err := insertStepDefinition(ctx, tx, step); err != nil {
			return err
		}
	}
	// ...
}
```

The second is right when the code has years ahead of it. On a migration script that gets deleted next month, the ten-minute version is the correct engineering call and the afternoon is waste ([Ch. 09](09_change_rjf9.md) owns the known-short-life case).

### Enforced boundaries cost more than unenforced ones

Expressing the graph in the type system — an interface that simply lacks the method you must not call — is nearly free. Expressing it as package or assembly walls forces exports and mapping code — a real bill, worth paying at some team sizes and not at others.

## How to recognize the failure

**In a codebase:**

- **Two modules that always appear in the same commits.** The directory structure says they are independent and the commit history says they are one unit. Trust the history — it is measuring the unit of change directly.
- **A test that has to construct half the system to exercise one function.** This is the cycle showing up as a fixture: the unit of test has grown to match the unit of dependency, and the fixture is measuring it for you.
- **Two-phase construction** — `a := &A{}; b := &B{a}; a.b = b`. The constructor cannot express the graph, and there is a window in which a field is nil.
- **"Partially initialized module" errors, or a static field holding zero.** The runtime version of the same cycle, and the one that reaches production.
- **An `import` at the top of a file that surprises you.** A leaf reaching for something it should not know exists — usually the first of the two edges.
- **An `internal` or `impl` package that everything imports.** A wall with everything on the same side of it is not a wall; the real boundary is somewhere else, unmarked.
- **A published API whose documented and observable behaviour differ.** Callers depend on the observable one, and the document is now fiction.

**In a conversation:**

- **"We can't change that, things depend on it."** True, and incomplete — ask how many. Two dependents is an afternoon's work. Forty is a project needing a plan, a deprecation window, and someone to own it. The sentence sounds identical in both cases; the number is the entire difference, and nobody has looked it up.
- **Someone calling an inversion-of-control callback a layering violation.** The call goes up; the dependency does not.

The question that catches real damage is not *does this match the diagram?* It is: **can this piece be understood without that piece?**

The first question is answered by a diagram. The second is answered by deleting something and seeing what stops compiling.

The next chapter takes the shape most people mean when they say architecture. Everything here has been about which way arrows point and how many there are; layering adds a further claim on top of both.

---

## Sources

- David L. Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules* — Communications of the ACM 15(12), December 1972. [PDF](https://wstomv.win.tue.nl/edu/2ip30/references/criteria_for_modularization.pdf).
- FlowCore, `docs/decisions.md` — [github.com/ilke-akdeniz/flowcore](https://github.com/ilke-akdeniz/flowcore).

---

[← Ch. 03](03_grading-a-law_q5c6.md)  ·  [Contents](00_toc.md)  ·  [Ch. 05 →](05_layering_p2vk.md)
