*Part V — Conventions*

# Idioms: Why Ecosystems Diverge

## The claim

**An Idiom's condition is a fact about your surroundings rather than about your system, so no measurement of your own system can settle an argument about one.**

[Chapter 02](02_the-five-kinds_cjx4.md) defines an Idiom as an ecosystem convention: locally correct, non-transferable, and usually traceable to a language feature that is present or absent.

What this chapter adds is the *condition*. A Principle's condition is a fact about your system: how much concurrency, how long the data lives, what a mistake costs ([Ch. 03](03_forces_f4m5.md)). An Idiom's condition is a fact about your surroundings — the language you are writing in, the tools you have, and the people who will read what you write. Both kinds of advice are conditional. They differ in where you go to look the condition up.

That is why ecosystems diverge on the same question, and it is why an Idiom does not travel. The condition stays behind.

---

## One split, two languages, opposite bills

Here is an order lookup in one Go package. In Go, an identifier beginning with a lower-case letter is visible only inside its own package — that is the whole of the language's access control, and there is no `private` keyword anywhere in it.

```go
// scanOrder is lower-case, so nothing outside this package can call it.
func scanOrder(orderID int, status string) Order {
	return Order{ID: orderID, Status: status}
}

func Get(orderID int) (Order, error) {
	if orderID <= 0 {
		return Order{}, fmt.Errorf("no such order: %d", orderID)
	}
	return scanOrder(orderID, "open"), nil
}
```

The helper is unreachable from outside and no discipline is required to keep it that way. The compiler holds it.

Now apply the instruction that persistence belongs in its own place. The code moves to a `store/` directory, which in Go makes it a separate package, and the service imports it.

The service has a reporting path of its own — a join that `Get` does not cover — so it holds rows that have to become `Order` values. While both lived in one package it called the helper directly, and it still wants to:

```go
direct := store.scanOrder(8, "closed")
```

```text
./service.go:9:18: undefined: store.scanOrder
```

A Go package boundary *is* the visibility boundary, so the only way to compile that line is to rename the helper `ScanOrder`. That works. It also changes what the package tells the world about itself:

```text
package store // import "shop/store"

type Order struct{ ... }
    func Get(orderID int) (Order, error)
    func ScanOrder(orderID int, status string) Order
```

**The helper was private until it was put behind a wall.** Nothing about the design changed: `scanOrder` is still an implementation detail, and the service is still the only caller that wants it. What changed is that the split put a visibility boundary between them, and Go has no way to open that boundary for one caller. Exporting it opens it for everyone, permanently, and an exported identifier is a commitment ([Ch. 05](05_dependency-and-hiding_agjy.md)). The instruction bought a boundary and paid for it with an API.

Now the same split in Python. A leading underscore is the convention for "internal", and it is a message to human readers:

```python
# store/__init__.py
def _scan_order(order_id, status):
    return {"id": order_id, "status": status}


def get(order_id):
    if order_id <= 0:
        raise ValueError(f"no such order: {order_id}")
    return _scan_order(order_id, "open")
```

```python
# service.py
import store

order = store.get(8)
row = store._scan_order(9, "closed")
print(order)
print(row)
```

```text
{'id': 8, 'status': 'open'}
{'id': 9, 'status': 'closed'}
```

Same split, same intent, and no bill at all. Nothing was published because nothing was hidden in the first place. The underscore survives the move because it never did anything a machine could enforce.

C# lands in a third place, and the reason is worth stating because it looks like the Python answer and is not. Folders carry no access meaning; `internal` is scoped to the assembly. So twelve layer folders in one project cost nothing — until somebody splits the layers into separate projects, at which point Go's bill arrives in full and for the same reason. The toolchain is not available here, so this is the mechanism rather than a run.

```text
 language   what a directory is        what hiding is tied to
 --------   ------------------------   ----------------------
 Go         a package                  the package
 C#         no access meaning          the assembly
 Python     a module or subpackage     nothing enforced
```

There is an objection to all of this, and it is worth taking, because Go does have a mechanism for exactly the problem — the `internal/` directory, whose rule [chapter 03](03_forces_f4m5.md) gives while putting the same FlowCore decision to a different use. FlowCore considered exactly that placement and rejected it, and the reasoning is the useful part — in Go, privacy comes from identifier case rather than from a directory, so a lower-case type in the root package is already exactly as unreachable to a client as one under `internal/`. What `internal/` solves is narrower: hiding a package when several packages must call each other by exported name. **It is not the tool you use to get privacy. It is the tool you use to get some of it back after a split has taken it away.** Reaching for it is a signal that the wall was drawn where the language charges.

The export is the visible cost and the smaller one. [Chapter 05](05_dependency-and-hiding_agjy.md) prices enforced boundaries in a sentence — walls force exports and mapping code, worth paying at some team sizes and not others — and this is the second half of that bill, itemised. Once `store` and the service are separate packages, an entity type has to live somewhere. If it lives in `store`, the service's public API returns types owned by persistence, which is the coupling the split was meant to remove. If each side owns its own, there are two of them and something converts between them. FlowCore's decision names this as its reason for keeping one package: splitting would force two representations of each entity and a mapping layer between them, which is the duplication the split was supposed to prevent. The charge is per field, per entity, per boundary, and it is invisible in review because every individual mapping function is trivial. It is also where drift lives — add a column, and nothing fails to compile until you reach the second definition.

*Put each layer in its own folder* is one instruction whose price runs from nothing to a published API, decided by a language the instruction never names — and no fact about your own system moves that price by a cent.

## Where the line between Idiom and Style falls

Look again at what fixed the Go compile error. Renaming `scanOrder` to `ScanOrder` is a change of one character's case, which is the definition of a Style decision everywhere else. The Go specification says an identifier is exported if "the first character of the identifier's name is a Unicode uppercase letter" and it is declared in the package block. So in Go, capitalization is an access modifier.

That is not a curiosity. It means **the line between Idiom and Style is drawn in a different place by each language**, and the two places it moves are exactly the two things everyone files under Style.

Python does the same to formatting. Indentation is not a convention there; it is syntax:

```python
def get(order_id):
return order_id
```

```text
IndentationError: expected an indented block after function definition on line 1
```

In Go or C# that is a formatting preference, settled by running the formatter. In Python it is a compile error.

## One decision, three ecosystems

[Chapter 02](02_the-five-kinds_cjx4.md) shows the demonstration already — a Go `main` that wires its dependencies by hand is unremarkable, and the same shape in C# gets sent back in review. Neither version is more correct. What [chapter 02](02_the-five-kinds_cjx4.md) does not do is say why the two ecosystems ended up on opposite sides, and the answer is a condition each of them can name.

**In Go you own `main`.** Nothing constructs your handlers but your own code, so wiring by hand is available. The condition that would make a container pay — something else builds your objects — is absent.

**In C# it is usually present.** The web framework instantiates your controllers, which means it must supply their constructor arguments, so the container is not an addition to the framework but the mechanism by which the framework can call you at all. [Chapter 18](18_six-profiles_dnkz.md) owns the general form of this: under a framework you are the callee, and its lifecycle is a Force rather than a convention.

**Python has both conditions in different projects**, which is why it never settled. A module-level object is a process-wide singleton for free, because imports are cached, and that covers most of what a container is reached for. Where Python does adopt injection is where a second condition appears — a per-request lifetime, such as a database session that must be opened and closed around one request — and the frameworks that grew that feature are the ones serving requests.

Three answers, three conditions, and no argument about the underlying advice — nobody in any of the three disputes that dependencies should be supplied rather than constructed. What differs is the container, and the conditions above are what it is conditioned on.

---

## Why the claim holds

An Idiom is advice with a condition attached, the same as a Principle. The difference is what the condition is about, and it decides everything downstream.

**A Principle's condition is a fact about your system.** You look it up by measuring your system: the row count, the number of writers, how long the data outlives the code.

**An Idiom's condition is a fact about your surroundings.** You look it up by asking about the language, the toolchain, or the people. And those do not move when you carry the code somewhere else — they move when *you* do.

Which is why measuring your own system settles nothing here. Every instrument the previous chapters reach for — the row count, the writer count, the latency budget — is pointed at the wrong object. What decides a container, an exported identifier or a folder layout is the language, the toolchain and the people who will read the code, and two engineers with identical systems answer differently because those three differ.

That accounts for the non-transferability [chapter 02](02_the-five-kinds_cjx4.md) asserts. An Idiom carried into a new ecosystem is advice whose condition was left behind, so it arrives as a bare instruction with nothing to check it against. It also accounts for something the model does not obviously predict: **two ecosystems can be at opposite ends of an argument with neither of them wrong**, because they are reading different conditions and both readings are correct where they are taken.

And it gives the reason obedience is the default, which is stronger than deference. One condition holds nearly everywhere: **other people will read this, and they expect the convention.** That is a fact about your surroundings of exactly the same kind as the others, so it is not an appeal to conformity — it is the condition still holding. Winning an argument about whether the convention is good does not touch it. The people are still there, and the code still has to be read by them, hired for, and reviewed.

So an argument you can win is not a licence — winning it is a fact about your system, and the condition is not. What licences deviation is showing that a condition about the surroundings has failed.

### A deviation with its condition named

The Idiom here belongs to the programming-language community rather than to a language: a compiler is written either in the language it compiles or on top of an established toolkit. Its condition is about surroundings — a finished language to write in, or a toolkit whose calling convention suits you. Both were absent, and the Go team said so.

The early Go compiler was written in C. Pike is direct about how that landed: the programming language community thought the proper approach was LLVM or a similar toolkit, or self-hosting — writing the compiler in the language it compiles.

His reasons are conditions, stated without the vocabulary. Bootstrapping a new language requires an existing one, and C was the obvious choice because Ken Thompson had already written a C compiler whose internals could serve as the basis. Writing a compiler in the language you are simultaneously designing, he says, "tends to result in a language that is good for writing compilers", which was not the language they wanted. And one specific thing decided it: segmented stacks that grew automatically were easy to add to their own compiler, and through a toolkit like LLVM the same change would have been infeasible, because of what it required of the calling convention and the garbage collector.

Then the part that makes it usable rather than merely defensible. It was narrow — one component, not a way of working. It was declared, in public, repeatedly. It cost something real: "Some people were offended by this choice, but it was the right one for us at the time."

And the condition expired. By Go 1.5 the language was finished, so the worry about a compiler-shaped language no longer applied, and Russ Cox wrote a tool that translated the compiler from C to Go semi-automatically. The deviation ended when the reason for it did.

That is the whole procedure. Name the condition, say so out loud, keep it to one place, and write down what would end it — because a deviation whose condition has quietly expired is indistinguishable from one that never had a reason.

---

## Where the claim doesn't apply

### Naming the condition does not make you able to act on it

Knowing where to look is not the same as being able to act on what you find. The clearest evidence comes from the people best placed to manage both.

Pike, on why generics took Go more than a decade: "Although I wouldn't change a thing about how interfaces worked, they colored our thinking in ways it took more than a decade to correct." Interfaces were the bedrock, so every proposed form of polymorphism had to be reconciled with them, and getting through it took several aborted implementations and eventually outside help from type theorists.

The detail that makes this a boundary rather than an anecdote is that the alternative was named early, from inside. Pike says Ian Taylor pushed them to face the problem "from early on", and links the difficulty directly to the convention's standing: it was hard "given the presence of interfaces as the bedrock of Go programming". So this is not a case of nobody noticing. Someone did notice, said so, and was right, and the convention held for a decade anyway.

An Idiom's cost is not that people follow it without thinking. It is that it shapes which alternatives get generated at all, including by the people who wrote it. So the claim buys less than it looks like it buys: it tells you where the condition lives and therefore which arguments are unwinnable, and it does not tell you how to move a convention once you have read the condition correctly.

### An Idiom can be a bad inference from a true condition

The claim says no measurement of your system settles an Idiom. It does not promise that checking the surroundings will. Sometimes the condition about the surroundings is true, and the convention still does not follow from it.

In Java and C#, a field is not exposed directly. It gets a getter and a setter:

```java
public class Account {
    private long balance;

    public long getBalance()              { return balance; }
    public void setBalance(long balance)  { this.balance = balance; }
}
```

The condition behind that is real, and it is a fact about the surroundings rather than about your system: the tooling finds fields by looking for `getX` and `setX` pairs. That is the JavaBeans convention, and serializers, object-relational mappers, template engines and IDE property editors have looked for it ever since. A plain public field is invisible to all of them.

What rode in with that condition is the claim that the pair is encapsulation. It is not. Anything a caller could do to a public field, it can do through the setter:

```java
account.setBalance(-500);
```

The getter earns its place on the condition: it is the half that lets the stored representation change later without touching callers. The setter gives that back. A type with a setter for every field cannot hold a single invariant about its own state, because any caller can put it in any state — which is the property the field was made private to get.

So the test has a second step. Name the condition, and then check that the convention actually follows from it — because *the tooling has to find the field* does not imply *every field stays writable by everyone*, and the second rode in with the first. **An Idiom you merely dislike survives that check. An Idiom encoding a mistake fails it, and fails it in a way you can show someone**, which is the difference between a defect report and a preference.

---

## What the claim costs

**Most of the time the answer is obey, and you did the work anyway.** Naming the condition is a real cost paid on every convention you decide to question, and it returns nothing visible in the overwhelming majority of cases, because the condition holds. The return comes entirely from the few where it does not, and you cannot tell which those are without doing it.

**"I can name the condition" becomes the new licence.** [Chapter 18](18_six-profiles_dnkz.md) records the same failure one level up, where *it's a different profile* excuses anything. Here it is *our situation is different*, followed by a condition that was never checked and would not survive being written down. The defence is that the condition has to be the kind of thing someone could contradict.

**Deviations are individually cheap and collectively expensive.** Each one is defensible on its own terms, and the codebase they add up to is one that nobody hired for the ecosystem can read. Neither Pike's compiler nor FlowCore's naming rule is a counter-example to this: both are single, declared, documented deviations in a body of otherwise conventional code, and that is the shape that stays affordable.

---

## How to recognize the failure

**In a codebase:**

- **A layout that publishes what it was meant to hide.** Exported identifiers that exist so a sibling package can reach them, and nothing outside the module ever calls. The wall was drawn where the language charges.
- **`internal/` introduced after a split.** It is the receipt for a boundary that cost more than expected.
- **The same entity defined twice with a mapper between**, where neither definition has a field the other lacks. The mapping tax, being paid on a boundary nobody has priced.
- **A deviation with no record.** If nothing says why the code does it differently, the next person cannot tell a decision from an accident, and will either preserve it forever or undo it in a cleanup commit.
- **A deviation whose reason is stated and no longer true.** Harder to see and more common than the previous one, because it looks like it has been handled.

**In a conversation:**

- **"That's not idiomatic."** A true statement that has not yet said anything. The question that moves it forward is which condition the convention rests on, and whether that condition holds here.
- **"That's just a convention."** Also true, and it is being used to mean *therefore ignorable*. [Chapter 02](02_the-five-kinds_cjx4.md) names this: a classification without its mechanism is a dismissal.
- **An argument about a convention that neither side can trace to a feature or a tool.** Good odds it is a Style question, in which case there is nothing to win and the correct move is to pick one.
- **A deviation defended by how good the code is.** The argument may be right and it is not responsive. What licences the deviation is a condition that failed, not a design that is better.

The question that does the work: **what is true about my surroundings that made this the convention here, and is it still true?**

If the answer names a language feature, a tool, or a person who will read the code, you have something to check. If nothing comes back, you have not found an Idiom — you have found a habit, and you are about to argue with it as though it could answer.

[Chapter 20](20_style_9rng.md) takes the level below this one — the decisions no compiler and no runtime can see, where being right is worth less than being consistent, and where the arguments are fiercest for exactly that reason.

---

## Sources

- Rob Pike, *What We Got Right, What We Got Wrong*, closing talk at GopherConAU, Sydney, 10 November 2023, published 4 January 2024. [Text and slides](https://commandcenter.blogspot.com/2024/01/what-we-got-right-what-we-got-wrong.html).
- *The Go Programming Language Specification*, "Exported identifiers". [go.dev/ref/spec#Exported_identifiers](https://go.dev/ref/spec#Exported_identifiers).
- FlowCore decision log, decision 1, "Single root package, not `internal/`". [github.com/ilke-akdeniz/flowcore](https://github.com/ilke-akdeniz/flowcore).

---

[← Ch. 18](18_six-profiles_dnkz.md)  ·  [Contents](00_toc.md)  ·  [Ch. 20 →](20_style_9rng.md)
