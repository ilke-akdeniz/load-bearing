# Patterns That Are Missing Language Features

## The claim

**Much of the Gang of Four catalogue is scaffolding that mimics a language feature. Build the same design in a language that has the feature and the scaffold disappears while the design stays — and that difference is how you tell one from the other.**

[Chapter 12](12_patterns-that-survive-translation_us2k.md) claimed that patterns which answer a Force survive. This chapter claims that a pattern can be expressed as a scaffold or as a language feature. The two claims are independent: a shape can answer a real Force and still be assembled out of scaffolding that another language does not need.

## What Norvig actually counted

The claim above is a version of an observation that already exists, and it is worth getting the original right before leaning on it, because the popular retelling is stronger than what was originally said.

Peter Norvig, in a 1996 talk called *Design Patterns in Dynamic Programming*, worked through the Gang of Four book and reported this:

> 16 of 23 patterns are either invisible or simpler, due to:
> First-class types (6): Abstract-Factory, Flyweight, Factory-Method, State, Proxy, Chain-Of-Responsibility.
> First-class functions (4): Command, Strategy, Template-Method, Visitor.
> Macros (2): Interpreter, Iterator.
> Method Combination (2): Mediator, Observer.
> Multimethods (1): Builder.
> Modules (1): Facade.

Three distinctions in the talk do not survive into the version people quote.

**Being simpler is not the same as being invisible.** The folk version — *patterns are just missing language features* — asserts complete disappearance. Norvig's own taxonomy has three levels, not two: a pattern is **invisible** when it is "so much a part of the language that you don't notice", **informal** when it exists as prose you reimplement by hand each time, and **formal** when the language lets you implement the pattern itself once and call it. Moving from informal to formal is a real gain and is not disappearance.

**Five words were dropped from Norvig's preceding slide, and they were the ones that mattered.** The slide reads: "16 of 23 patterns have qualitatively simpler implementation in Lisp or Dylan than in C++ *for at least some uses of each pattern*."

*For at least some uses.* Not all uses. With those words the claim survives you finding a Visitor somewhere that a first-class function does not improve, because Norvig never said every one. Without them it becomes *these patterns are always simpler*, and a single stubborn case knocks it over.

Norvig also lists five things patterns are for, and one of them is "to avoid limitations of implementation language", alongside recording design tradeoffs and describing what experienced designers know. The talk does not claim patterns are *only* workarounds. That is a claim its readers added.

So the honest form is narrower than the slogan and still worth having: for a specific list of patterns, in a language with a specific feature, the code you write to get the pattern's effect is not needed anymore.

---

## The demonstration

### Visitor got simplified in the language that needed it

Visitor exists because a program sometimes has to do different work for each member of a fixed set of types, and 1994 Java could not switch on a type. The way around that was **double dispatch**: every node type gets an `accept` method that calls back into the operation, so the node's own method dispatch chooses which branch runs.

Here is an expression evaluator in that style.

```java
// The 1994 shape: double dispatch, because the language cannot switch on type.
interface Expr {
    <R> R accept(Visitor<R> visitor);
}

interface Visitor<R> {
    R visitNum(Num num);
    R visitAdd(Add add);
    R visitMul(Mul mul);
}

final class Num implements Expr {
    final int value;
    Num(int value) { this.value = value; }
    public <R> R accept(Visitor<R> visitor) { return visitor.visitNum(this); }
}

final class Add implements Expr {
    final Expr left, right;
    Add(Expr left, Expr right) { this.left = left; this.right = right; }
    public <R> R accept(Visitor<R> visitor) { return visitor.visitAdd(this); }
}

final class Mul implements Expr {
    final Expr left, right;
    Mul(Expr left, Expr right) { this.left = left; this.right = right; }
    public <R> R accept(Visitor<R> visitor) { return visitor.visitMul(this); }
}

final class EvalVisitor implements Visitor<Integer> {
    public Integer visitNum(Num num) { return num.value; }
    public Integer visitAdd(Add add) { return add.left.accept(this) + add.right.accept(this); }
    public Integer visitMul(Mul mul) { return mul.left.accept(this) * mul.right.accept(this); }
}
```

Twenty-eight lines as shown, not counting blanks, comments, or the `main` that runs it. `new Add(new Num(2), new Mul(new Num(3), new Num(4)))` evaluates to 14.

Now the same design in Java 26. Three features arrived in the intervening years: `record`, which is a class whose fields, constructor, and accessors are generated from one line; `sealed`, which fixes the set of types allowed to implement an interface; and pattern matching in `switch`, which can test a value's type and pull its fields out in the same breath.

Together those give Java a **sum type** — a type whose values are one of a fixed, known list of alternatives. An expression is a number *or* an addition *or* a multiplication and nothing else, and because the list is closed the compiler can check that you handled every branch. Rust's `enum`, F#'s discriminated union, and TypeScript's tagged union are the same idea. It is worth having the name, because it is the feature this chapter keeps returning to.

```java
// The same design in Java 26. No Visitor, no accept, no double dispatch.
sealed interface Expr permits Num, Add, Mul {}

record Num(int value) implements Expr {}
record Add(Expr left, Expr right) implements Expr {}
record Mul(Expr left, Expr right) implements Expr {}

static int eval(Expr expr) {
    return switch (expr) {
        case Num(int value) -> value;
        case Add(Expr left, Expr right) -> eval(left) + eval(right);
        case Mul(Expr left, Expr right) -> eval(left) * eval(right);
    };
}
```

Eleven lines by the same count, and the same expression evaluates to 14.

**The line count is not the only argument.** The argument is whether the same guarantee survives with less scaffolding holding it up. Visitor's guarantee was that adding a node type breaks every operation that has not been updated, at compile time, instead of at run time on the one input nobody tested. Add a `Neg` node to the first version and leave `EvalVisitor` alone:

```text
Old.java:31: error: EvalVisitor is not abstract and does not override
abstract method visitNeg(Neg) in Visitor
```

Add it to the second version and leave `eval` alone:

```text
New.java:11: error: the switch expression does not cover all possible input values
```

Identical guarantee. One costs an interface, a method per node type, and a callback protocol every reader has to hold in their head; the other costs a keyword. Nothing about the design changed — there is still a closed set of node types and an operation defined over all of them, which is the idea Visitor was carrying. What went away was the machinery for expressing it.

And notice which language this happened in. Not Lisp, not Dylan — Java, the language where Visitor was most entrenched. The pattern did not fail to survive translation into some more expressive language. It expired in place.

### Strategy, in four languages

Strategy is a family of interchangeable algorithms with a common interface, selected at run time. In a language with a class system and nothing else, that is an interface, a class per algorithm, and a field to hold the chosen one:

```java
interface ShippingPolicy {
    long costMinor(int weightGrams);
}

final class FlatRate implements ShippingPolicy {
    public long costMinor(int weightGrams) { return 499; }
}

final class ByWeight implements ShippingPolicy {
    public long costMinor(int weightGrams) { return 200 + weightGrams / 10; }
}

final class Checkout {
    private final ShippingPolicy policy;
    Checkout(ShippingPolicy policy) { this.policy = policy; }
    long total(long goodsMinor, int weightGrams) {
        return goodsMinor + policy.costMinor(weightGrams);
    }
}
```

**Before showing the Java 26 version, one thing has to be separated out, because conflating the two is how this comparison is usually rigged.** Two independent things could change here. One is the scaffolding — the interface and the classes implementing it. The other is whether the two policies keep their names and their home. Those are not the same decision, and replacing named classes with lambdas dropped into call sites changes both at once, which is not a fair trade and is worth objecting to.

So keep the names:

```java
// Still named, still in one place, still callable from anywhere.
final class ShippingPolicies {
    static long flatRate(int weightGrams) { return 499; }
    static long byWeight(int weightGrams) { return 200 + weightGrams / 10; }
}

final class Checkout {
    private final IntToLongFunction shippingCost;
    Checkout(IntToLongFunction shippingCost) { this.shippingCost = shippingCost; }
    long total(long goodsMinor, int weightGrams) {
        return goodsMinor + shippingCost.applyAsLong(weightGrams);
    }
}

new Checkout(ShippingPolicies::flatRate).total(2000, 3000);
new Checkout(ShippingPolicies::byWeight).total(2000, 3000);
```

Nine lines of interface and implementing classes became four lines of named methods. Both print `2499` and `2500`. A reader can still list the policies by opening one file, still reuse `byWeight` from a second call site, and still add a third policy by adding one method.

The scaffolding that disappeared was `interface ShippingPolicy` and the two classes whose only content was one method each. What that interface bought — a name for the concept and a place to gather the implementations — the class `ShippingPolicies` still buys, without requiring every policy to be a type.

**And the names survive into the tooling, which is the objection people raise next.** `ShippingPolicies::flatRate` is a method reference rather than an inline lambda, and a method reference has a real name at run time. Throwing from inside each:

```text
method reference to a named method:
   Trace.byWeight(Trace.java:4)
inline lambda:
   Trace.lambda$main$0(Trace.java:19)
```

So anonymity in a stack trace is a consequence of writing the policy inline, not of using a function value. Both options exist in the new version and only one exists in the old, which is the shape of the whole chapter: the feature removed a requirement rather than a capability.

Go has no inheritance to organize away from, so the field holds a function directly. (A `func(int) int64` is a value like any other — Go functions can be stored in fields, passed, and returned. A plain top-level `func` can be used wherever such a value is wanted.)

```go
type Checkout struct {
	shippingCost func(weightGrams int) int64
}

func (c Checkout) Total(goodsMinor int64, weightGrams int) int64 {
	return goodsMinor + c.shippingCost(weightGrams)
}

// Still named, still reusable, still one place to find them.
func FlatRate(weightGrams int) int64 { return 499 }
func ByWeight(weightGrams int) int64 { return 200 + int64(weightGrams)/10 }

fmt.Println(Checkout{shippingCost: FlatRate}.Total(2000, 3000))
fmt.Println(Checkout{shippingCost: ByWeight}.Total(2000, 3000))
```

And Python, where the type annotation is the only trace that anything was ever a strategy:

```python
@dataclass
class Checkout:
    shipping_cost: Callable[[int], int]

    def total(self, goods_minor: int, weight_grams: int) -> int:
        return goods_minor + self.shipping_cost(weight_grams)

def flat_rate(weight_grams: int) -> int: return 499
def by_weight(weight_grams: int) -> int: return 200 + weight_grams // 10

print(Checkout(flat_rate).total(2000, 3000))
print(Checkout(by_weight).total(2000, 3000))
```

All four print `2499` and `2500`, and all four keep the policies named and reusable. The design is identical in each: the caller decides how shipping is priced and the checkout does not know which rule it got. What differs is whether the language obliges you to make each policy a type. One of the four does. Three do not, and in those the word *Strategy* names nothing that appears in the file.

### The rest of the catalogue, compactly

Norvig's sixteen, with what makes each one invisible, and the seven he did not include:

```text
 what makes it invisible   the patterns
 -----------------------   ----------------------------------------
 first-class functions     Command, Strategy, Template Method,
                           Visitor
 first-class types         Abstract Factory, Factory Method,
                           Flyweight, State, Proxy,
                           Chain of Responsibility
 syntax or macros          Interpreter, Iterator
 method combination        Mediator, Observer
 multimethods              Builder
 modules                   Facade

 on none of the above      Adapter, Bridge, Composite, Decorator,
                           Memento, Prototype, Singleton
```

The second group is the interesting one, and the next section is about why those seven are there.

Two entries in the first group are worth a sentence each because their dissolution is so complete that the word has fallen out of use. **Iterator** is `for x in y` — Java got it in 2004, and almost nobody who writes that line knows they are invoking a pattern with a four-method interface behind it. **Command** is a closure: an operation plus the arguments it was going to be called with, packaged as a value you can store and invoke later, which is what a function literal capturing its surroundings already is.

---

## Why the claim holds

A pattern is something you **construct**. A feature is something you **get**.

That is the whole mechanism, and everything above is an instance of it. The Visitor's `accept` methods, the `Visitor` interface, and the callback protocol are three pieces of apparatus that exist only to produce an effect — dispatch on a value's type — that the language did not offer. When the language offers it, the apparatus has nothing to do. The effect was never the apparatus.

The tell is in the names. **A pattern that is simulating a feature has parts with no counterpart in the problem.** There is no `accept` in arithmetic, no `ConcreteStrategy` in shipping, no `visitNum` in an expression tree. Those names come from the pattern, and their presence is a sign that some of the file is about the language rather than about the domain.

There is a reason the dissolving ones cluster. Look at the four that first-class functions handle: Command, Strategy, Template Method, Visitor. All four are the same underlying request — *let the caller supply behaviour* — differing only in when and how it is supplied. A language with function values answers all four with one feature, because there was only ever one question. The catalogue lists four patterns because in a language without function values, the four workarounds genuinely do look different.

---

## Where the claim doesn't apply

### The same feature that dissolved Visitor leaves Composite standing

The clearest limit is visible in one file, because sum types dissolve one of these patterns and not the other.

```java
// Composite: a Directory holds Nodes, and is itself a Node.
sealed interface Node permits FileNode, Directory {}

record FileNode(String name, long bytes) implements Node {}
record Directory(String name, List<Node> children) implements Node {}

// The Visitor is gone — this switch is what replaced it.
static long totalBytes(Node node) {
    return switch (node) {
        case FileNode file -> file.bytes();
        case Directory directory ->
            directory.children().stream().mapToLong(child -> totalBytes(child)).sum();
    };
}
```

The Visitor is gone. The Composite is not: a `Directory` still holds a list of `Node` and is still a `Node` itself, and that recursion is the pattern. Take the same design to Go, which has no sum types at all and therefore dissolves nothing:

```go
type Node interface{ TotalBytes() int64 }

type FileNode struct {
	Name  string
	Bytes int64
}

func (f FileNode) TotalBytes() int64 { return f.Bytes }

type Directory struct {
	Name     string
	Children []Node
}

func (d Directory) TotalBytes() int64 {
	var total int64
	for _, child := range d.Children {
		total += child.TotalBytes()
	}
	return total
}
```

Both print `6700` for the same tree. The dispatch mechanism changed completely between the two and the containment did not, because the containment is not a mechanism. Directories contain files. That is a fact about filesystems, and no language feature has anything to say about it — which is [chapter 12](12_patterns-that-survive-translation_us2k.md)'s category of patterns that answer the shape of the problem rather than a Force.

So the test does not partition the catalogue into *real* and *fake*. It separates the patterns whose substance is a language workaround from the patterns whose substance is a claim about the domain, and the second group is untouched by anything a compiler does.

### Decorator, where the test returns no

Decorator is not one of Norvig's sixteen, and writing it both ways shows why.

Decorator wraps something in another thing with the same interface, adds behaviour, and forwards the rest. Without function values, that is an interface and a struct per decoration holding the thing it wraps:

```go
type Fetcher interface {
	Fetch(url string) (string, error)
}

type retryFetcher struct {
	attempts int
	inner    Fetcher
}

func (r retryFetcher) Fetch(url string) (string, error) {
	var err error
	for attempt := 0; attempt < r.attempts; attempt++ {
		var body string
		if body, err = r.inner.Fetch(url); err == nil {
			return body, nil
		}
	}
	return "", err
}
```

With function values, the interface becomes a function type and each decoration becomes a function returning a function:

```go
type Fetcher func(url string) (string, error)

func WithRetry(attempts int, inner Fetcher) Fetcher {
	return func(url string) (string, error) {
		var err error
		for attempt := 0; attempt < attempts; attempt++ {
			var body string
			if body, err = inner(url); err == nil {
				return body, nil
			}
		}
		return "", err
	}
}
```

Both compile, both behave identically against a source that fails twice and then succeeds — three upstream calls, and none on the second fetch once a cache is added outside. **And the function version is longer.** Counting the interface or function type plus two decorations, non-blank and non-comment: thirty-one lines for the structs, thirty-seven for the functions.

That is the opposite of what happened to Visitor and Strategy, and the reason is that Go asks almost nothing for a one-method interface. There is no `implements` clause, no separate declaration of intent — a type with the right method satisfies it. When the ceremony around the scaffold is already near zero, a feature that removes ceremony has nothing to collect.

So the language feature bought something here, but it was not less code. It was **composability at the call site**: `WithCache(WithRetry(source))` is an expression, where the struct version needs a nested literal naming both types. That is a real gain and it is not the gain this chapter's claim is about.

There is a second limit, and it decides more cases in practice: **the interface has to be one function for any of this to apply.** Decorate something with five methods and the wrapper has to supply all five, however few of them do anything:

```go
type loggingStore struct{ inner Store }

func (l loggingStore) Get(id string) (string, error) {
	fmt.Println("get", id)
	return l.inner.Get(id)
}

func (l loggingStore) Put(id, body string) error            { return l.inner.Put(id, body) }
func (l loggingStore) Delete(id string) error               { return l.inner.Delete(id) }
func (l loggingStore) List(prefix string) ([]string, error) { return l.inner.List(prefix) }
func (l loggingStore) Count() (int, error)                  { return l.inner.Count() }
```

Four forwarding methods that exist to be forwarded through. No language feature removes them, because they are not simulating anything — they are the price of the interface being five methods wide, which is a fact about the design rather than about the compiler. [Chapter 04](04_dependency-and-hiding_agjy.md) works through where that leaves you.

Decorator therefore sits outside the claim from two directions at once, and Norvig's list was right to omit it.

### Observer dissolves in one process and not across a machine

Norvig lists Observer as dissolved, and inside one process it is: a Go channel, a C# event, a callback list. The word adds nothing to `orders.Subscribe(handler)`.

Move the observer to another machine and every part of that comes back, in a worse form. The notification can be lost, so somebody has to decide between at-least-once and at-most-once. It can arrive twice, so the handler needs to be idempotent. It can arrive out of order. The publisher now has to decide what happens when a subscriber is slow, and the answer is either unbounded buffering or dropping. None of these is a language question and no feature makes them go away — they are [chapter 07](07_distribution_49yh.md)'s material, arriving because the shape crossed a boundary, which is [chapter 11](11_patterns-that-cross_r8dw.md)'s.

The lesson is about the test rather than about Observer. **The test is scoped, and running it at the wrong scope returns a confident wrong answer.** "Observer is just events" is true of the version that lives in one address space and false of the version that lives in two, and the sentence does not say which one it is talking about.

### The test names the language you moved to, not the pattern

*Visitor is a workaround for missing sum types* is a claim about a pair — that pattern, and a language that has sum types. It is not a property Visitor carries around.

This matters because the language you are actually in is not a free variable. If you are maintaining a Java 8 service, "Visitor is a workaround" is completely true and completely useless: the feature that would dissolve it does not exist in your compiler, so the workaround is the correct code and writing it is not a failure of taste. The audit tells you where the boundary of your language is. It does not tell you to stand outside it.

The honest use of the test is diagnostic rather than prescriptive — it explains *why* a piece of your codebase is shaped the way it is, and it tells you what would happen to that shape if you moved. Neither is an instruction to delete anything.

---

## What the claim costs

**The failure modes do not vanish with the scaffold; they move to the feature.** The instinct is to say you have lost the pattern name and with it the literature on the pattern's failure modes. That is mostly wrong, because when the scaffold goes, the scaffold's own problems go with it — there is no wrapper class to drift out of sync with the interface it wraps if there is no wrapper class. What you inherit instead is the failure modes of the language feature, and those are usually more general and better documented.

So the catalogue you need updates rather than disappears: *decorator gotchas* becomes *function composition gotchas*. The largest of those is order, and it is easy to get wrong because both orders compile and only one is right:

```go
outer := WithLog(WithCache(cache, source)) // logs every call
inner := WithCache(cache, WithLog(source)) // logs only the misses
```

Two fetches of the same URL through each:

```text
outer, two fetches of the same URL:
  fetching https://example.com
  fetching https://example.com
inner, two fetches of the same URL:
  fetching https://example.com
```

Neither is a bug. They answer different questions — one measures demand, the other measures load on the source — and choosing without noticing there was a choice is the failure. That is the thing to look up, and it is a property of composing functions rather than of Decorator.

**Inlining is now available, and it is a real way to make things worse.** The demonstration above kept the policies named, which is what makes the comparison fair. Nothing forces that. The old version could not express `new Checkout(weightGrams -> 499)` at a call site and the new one can, so a codebase can acquire fifteen anonymous pricing rules scattered across the files that happen to use them, with no list of what the policies are and `Checkout$$Lambda$14` in the profiler. The feature did not cause this and it did enable it, and "you can now write it inline" is heard as "write it inline" more often than not.

The rule that survives is about size rather than about patterns: a policy of three lines is fine inline, and one of two hundred lines of pricing rules wants a name, a file, and a test, whatever the language permits.

**Erasing the construction erases the announcement.** An interface named `ShippingPolicy` with two implementations tells the next person that variation was anticipated here, where to add the third, and what the contract is. A field typed `func(int) int64` says the same thing to somebody reading that line and nothing to somebody searching the repository for extension points, because there is no name to search for. This is not only a documentation cost — it is reuse and maintenance. A named type is what an IDE lists implementations of, what a reviewer greps for before changing a signature, and what stops a fourth policy being written from scratch somewhere else because nobody knew the first three existed. Keeping the policies in one named place, as above, recovers most of this; keeping nothing recovers none of it.

**Running the audit as a cleanup is a category error.** The catalogue is a description of shapes that occurred ([Ch. 10](10_what-a-pattern-is-for_3xzc.md)). Finding that some entries were language workarounds is a fact about the languages of 1994, not a licence to remove those shapes from a codebase that still compiles with the compiler it has. The finding is worth having because it changes what you conclude when you meet the pattern, not because it generates work.

---

## How to recognize the failure

**In a codebase:**

- **`accept` methods on a type hierarchy in a language with pattern matching.** The double dispatch is being paid for and the compiler would do it.
- **A `Factory` whose `create` method contains a single `new` with no branching.** The pattern is a workaround for languages where a class is not a value; if yours are, the factory is a function that could be the constructor.
- **Per-method forwarding classes** — twenty methods, nineteen of which call straight through. Either the interface is too wide to decorate or the concern is not a decoration at all ([Ch. 04](04_dependency-and-hiding_agjy.md)).
- **Class names built from pattern names** — `PricingStrategyImpl`, `OrderVisitor`, `ConfigBuilderFactory`. When the pattern has dissolved, these are the residue: names describing apparatus that is no longer there.

**In a conversation:**

- **"We should use the Strategy pattern here."** In which language? If the answer is one with first-class functions, the proposal is "pass a function," and it should be said that way, because then someone can disagree with the actual design.
- **"That's just a closure."** Frequently correct, and it is a claim about the implementation rather than about the design. The design question — should this vary at all, and who decides — is untouched by the observation.
- **"Design patterns are obsolete."** The strong folk version of Norvig, and the seven patterns he did not list are the counter-evidence. So is every pattern in [chapter 12](12_patterns-that-survive-translation_us2k.md) that answers a Force rather than a language gap.
- **A design document specifying patterns before specifying a language.** The catalogue is not language-independent, and half of it is a description of what you will have to build if you pick a language without the feature.

The question that does the work: **if I wrote this in a language with first-class functions and sum types, what would be left?**

Whatever survives is the design. Whatever vanishes was the cost of expressing it.

Which gives a concrete move, and it is not *strip patterns out of your design documents*. The catalogue is not language-independent, so a document that says "use Strategy here" without saying what it is being written in has underspecified the work: in one language that sentence means an interface and three classes, and in another it means passing a function. **Name the language first, then the design.** Where a pattern name is doing real work, say which part is the design and which part is what your compiler makes you write to get it — because the second part is the part that changes when the language does, and the first part is the part you are actually deciding.

The same reading applies in reverse to advice you receive. A blog post recommending a pattern was written in some language, and if it does not say which, you cannot tell whether you are being given a design idea or a workaround for a compiler you do not use.

And *language* here does not have to mean a different one. Visitor changed status between two releases of Java, so the version you compile with is part of the answer — a design document naming Java and not naming the version has answered half the question.

[Chapter 14](14_smuggled-verdicts_8y69.md) turns from names that describe a shape to names that arrive with a verdict already attached — vocabulary like *anemic domain model*, where accepting the word concedes the conclusion, and how much that costs depends on whether the word also names something you can go and check.

---

## Sources

- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software* — Addison-Wesley, 1994.
- Peter Norvig, *Design Patterns in Dynamic Programming* — Object World, 5 May 1996. [Slides](https://www.norvig.com/design-patterns/), where the landing page carries the later title *Design Patterns in Dynamic Languages*.

---

[← Ch. 12](12_patterns-that-survive-translation_us2k.md)  ·  [Contents](00_toc.md)  ·  [Ch. 14 →](14_smuggled-verdicts_8y69.md)
