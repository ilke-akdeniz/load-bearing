# Patterns That Are Missing Language Features

## The claim

**Much of the Gang of Four catalogue is scaffolding that mimics a language feature, and you can see the scaffold disappaear when building the design in a language with that feature.**

Chapter 12 claimed that patterns that are answer to Forces survive. This chapter claims that the pattern can be expressed as a scaffold or as a language feature. Notice that the two claims are independent: A shape can answer a real Force and still be assembled out of scaffolding that is not needed on another language.

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

Two things in that slide do not survive into the version people quote.

**Being simpler is not the same as being invisible.** The folk version *patterns are just missing language features*, asserts complete disappearance. Norvig's own taxonomy has three levels, not two: a pattern is **invisible** when it is "so much a part of the language that you don't notice", **informal** when it exists as prose you reimplement by hand each time, and **formal** when the language lets you implement the pattern itself once and call it. Moving from informal to formal is a real gain and is not disappearance.

**The qualifier is a quantifier.** The preceding slide reads: "16 of 23 patterns have qualitatively simpler implementation in Lisp or Dylan than in C++ *for at least some uses of each pattern*." Not every use. Chapter 04 works through what happens to a claim when a folk version drops a quantifier, using the halting problem; this is the same failure applied to a smaller result, and it is the reason the strong version is easy to disprove and the real one is not. [claude explain what qualifier and quantifier mean here concretely or use other simpler words to convey the same meaning. I also don't get your Chapter 04 example, you have to explain the example with enough context here if the example needs to stay. Nobody will go back to chapter 4 and read the example again.]

Norvig also lists five things patterns are for, and "to avoid limitations of implementation language" is one of them, alongside recording design tradeoffs and describing what experienced designers know. The talk does not claim patterns are *only* workarounds. That is a claim its readers added.

So the honest form is narrower than the slogan and still worth having: for a specific list of patterns, in a language with a specific feature, the code you write to get the pattern's effect is not needed anymore.

---

## The demonstration

### Visitor got simplified in the same language

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

**The line count is not the only argument.** The argument is: can we have the same or better guarantee with less manual scaffold?. Visitor's guarantee was that adding a node type breaks every operation that has not been updated, at compile time, instead of at run time on the one input nobody tested. Add a `Neg` node to the first version and leave `EvalVisitor` alone:

```text
Old.java:31: error: EvalVisitor is not abstract and does not override
abstract method visitNeg(Neg) in Visitor
```

Add it to the second version and leave `eval` alone:

```text
New.java:11: error: the switch expression does not cover all possible input values
```

Identical guarantee. One costs an interface, a method per node type, and a callback protocol every reader has to hold in their head; the other costs a keyword. Nothing about the design changed — there is still a closed set of node types and an operation defined over all of them, which is the idea Visitor was carrying. What went away was the machinery for expressing it.

And notice which language this happened in. Not Lisp, not Dylan — Java, the language where Visitor was most entrenched. The pattern did not fail to survive translation into some language more expressive. It expired in place in Java.

### Strategy, in four languages

Strategy is a family of interchangeable algorithms with a common interface, selected at run time. In a language with a class system and nothing else, that is an interface, a class per algorithm, and a field:

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

In Java 26, `ShippingPolicy` has one method, so a lambda satisfies it and the two implementing classes have nothing left to do:

[claude the following examples are technically and from a pure logical perspective correct but most reader will object that two versions don't offer the same guarantee or maintainability. In the first example the shipping formulas are defined in one place, they are named and can be reused easily. Any developer sees what are different policies and how to apply them quickly. In the second example, policies are not named and they are not reusable easily. Adding another policy, modifying existing policies and reusing policies are risky and not straightforward for a new developer. 

If the main difference is that old Java required you to have the formulas a "Home" but new Java doesn't require it so you can have the lambda version if you don't need the named, reusable formulas and so on..., stating the trade-off explicity. But if there is a trade-off then does our claim that the pattern became simpler still hold here?

Or maybe there is another new version that offers the same or better guarantees and maintainability with reduced scaffolding, then use those examples.]

```java
final class Checkout {
    private final IntToLongFunction shippingCost;
    Checkout(IntToLongFunction shippingCost) { this.shippingCost = shippingCost; }
    long total(long goodsMinor, int weightGrams) {
        return goodsMinor + shippingCost.applyAsLong(weightGrams);
    }
}

new Checkout(weightGrams -> 499).total(2000, 3000);
new Checkout(weightGrams -> 200 + weightGrams / 10).total(2000, 3000);
```

Go has no inheritance to organize away from, so the field is a function type directly. (A `func(int) int64` is a value like any other — Go functions can be stored, passed, and returned, and a function literal written inline captures the variables around it.)

```go
type Checkout struct {
	shippingCost func(weightGrams int) int64
}

func (c Checkout) Total(goodsMinor int64, weightGrams int) int64 {
	return goodsMinor + c.shippingCost(weightGrams)
}

flatRate := Checkout{shippingCost: func(weightGrams int) int64 { return 499 }}
byWeight := Checkout{shippingCost: func(weightGrams int) int64 { return 200 + int64(weightGrams)/10 }}
```

And Python, where the annotation is the only trace that anything was ever a strategy:

```python
@dataclass
class Checkout:
    shipping_cost: Callable[[int], int]

    def total(self, goods_minor: int, weight_grams: int) -> int:
        return goods_minor + self.shipping_cost(weight_grams)

Checkout(lambda weight_grams: 499).total(2000, 3000)
Checkout(lambda weight_grams: 200 + weight_grams // 10).total(2000, 3000)
```

All four print `2499` and `2500`. The design is the same in all four: the caller decides how shipping is priced, and the checkout does not know which rule it got. Two of the four require you to name the concept `ShippingPolicy` and give it a home; two do not, and in those the word *Strategy* names nothing that exists in the file.

Chapter 11 reaches the same place from the other direction — it observes that Strategy and Template Method have no form on the far side of an ownership boundary, and concludes they are code-organization devices rather than system structure. This is what that looks like from inside one file. [claude is this paragraph really necessary? I find this abrupt flashback to past chapters annoying, unless they offer a very good insight for the current chapter.]

### Decorator becomes function composition if the interface is one function

Decorator wraps an object in something that has the same interface, adds behaviour, and forwards the rest. When the interface is a single function, the wrapper is a function that returns a function: [claude you have to show first the pattern in the language without the function composition]

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

func WithCache(cache map[string]string, inner Fetcher) Fetcher {
	return func(url string) (string, error) {
		if body, ok := cache[url]; ok {
			return body, nil
		}
		body, err := inner(url)
		if err == nil {
			cache[url] = body
		}
		return body, err
	}
}

// When fetch is called against a source that fails twice and then succeeds,
// WithRetry returns sucessfully after three upstream calls and then 
// WithCache returns the fetched body with 0 calls. 
fetch := WithCache(map[string]string{}, WithRetry(5, flaky))
```

**The boundary is inside this example, and it is the interface width.** [claude I understood the previous sentence after reading the whole paragraph but that's not ideal. Try to be more explicit and clear in that sentence: what boundary? interface width?] Composition works here because `Fetcher` has one method. Give the wrapped thing twenty methods and there is no composition available: you are writing twenty forwarding methods, nineteen of which do nothing, which is the shape chapter 05 works through under `LoggingOrderService`. So Decorator does not dissolve into a language feature. It dissolves into a language feature *when the thing being decorated is narrow enough*, and the width of that interface is a fact about your design rather than about your language. [claude consider showing what happens whern the thing being decorated is not narrow enough with a code example]

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

The tell is in the names. **A pattern that is simulating a feature has parts with no counterpart in the problem.** There is no `accept` in arithmetic, no `ConcreteStrategy` in shipping, no `visitNum` in an expression tree. Those names come from the pattern, and their presence is a sign that some of the file is about the language rather than about the domain. Chapter 10's second test asks what a name rules out; this is a different question about the same file — what does this name *cost me in code*, and would that cost exist somewhere else. [claude another chapter flashback, you decide if it's worth keeping]

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

Both print `6700` for the same tree. The dispatch mechanism changed completely between the two and the containment did not, because the containment is not a mechanism. Directories contain files. That is a fact about filesystems, and no language feature has anything to say about it — which is chapter 12's category of patterns that answer the shape of the problem rather than a Force.

So the test does not partition the catalogue into *real* and *fake*. It separates the patterns whose substance is a language workaround from the patterns whose substance is a claim about the domain, and the second group is untouched by anything a compiler does.

### Observer dissolves in one process and not across a machine

Norvig lists Observer as dissolved, and inside one process it is: a Go channel, a C# event, a callback list. The word adds nothing to `orders.Subscribe(handler)`.

Move the observer to another machine and every part of that comes back, in a worse form. The notification can be lost, so somebody has to decide between at-least-once and at-most-once. It can arrive twice, so the handler needs to be idempotent. It can arrive out of order. The publisher now has to decide what happens when a subscriber is slow, and the answer is either unbounded buffering or dropping. None of these is a language question and no feature makes them go away — they are chapter 07's material, arriving because the shape crossed a boundary, which is chapter 11's.

The lesson is about the test rather than about Observer. **The test is scoped, and running it at the wrong scope returns a confident wrong answer.** "Observer is just events" is true of the version that lives in one address space and false of the version that lives in two, and the sentence does not say which one it is talking about.

### The test names the language you moved to, not the pattern

*Visitor is a workaround for missing sum types* is a claim about a pair — that pattern, and a language that has sum types. It is not a property Visitor carries around. [claude what is "sum types". If we didn't define it briefly in the first occurence of the term we should do it.]

This matters because the language you are actually in is not a free variable. If you are maintaining a Java 8 service, "Visitor is a workaround" is completely true and completely useless: the feature that would dissolve it does not exist in your compiler, so the workaround is the correct code and writing it is not a failure of taste. The audit tells you where the boundary of your language is. It does not tell you to stand outside it.

The honest use of the test is diagnostic rather than prescriptive — it explains *why* a piece of your codebase is shaped the way it is, and it tells you what would happen to that shape if you moved. Neither is an instruction to delete anything.

---

## What the claim costs

**You lose the pattern name, and the name was an index.** `WithRetry` and `WithCache` are two functions composed; nobody reading them will search for "decorator failure modes" and find twenty years of writing about wrapper ordering and interface drift. Chapter 10 makes the case that some names are mediocre descriptions and excellent search terms, and a dissolved pattern gives that up silently. The mitigation is a comment naming the pattern you dissolved, which most people do not write. [claude I'm not sure about your prescription. When the pattern was simplified I'm guessing most of the complications that came with the old manual scaffold are gone as well. So I don't see what naming that and looking for the failure modes of that buys you. For me the right prescription is to be aware that most of the time, the language feature replacing the scaffold has the more general scaffold built-in the language itself. So now that's the updated catalogue - failure mode you need to be aware of: "decorator gotchas => function composition gotchas" ]

**A closure has no name in a stack trace.** The class-per-strategy version puts `FlatRate` in the profile, in the exception, and in the debugger. The lambda version puts `Checkout$$Lambda$14`. When the strategies are three lines each this is a fair trade, and when one of them is two hundred lines of pricing rules it is not — at which point you may want the class back, for reasons that have nothing to do with patterns. [this falls in line with my previous tag about the code examples and lambda so you decision there can also modify this paragraph]

**Erasing the construction erases the announcement.** An interface named `ShippingPolicy` with two implementations tells the next person that variation was anticipated here and where to add the third. A `func(int) int64` field says the same thing to someone who is looking at it and nothing to someone grepping for extension points. The pattern's apparatus was partly documentation, and documentation was one of the five purposes Norvig listed. [this falls in line with my previous tag about the code examples and lambda so you decision there can also modify this paragraph. Also worth remembering that this is not only about documentaion. It's about maintainability and reuse as well.]

**Running the audit as a cleanup is a category error.** The catalogue is a description of shapes that occurred (Ch. 10). Finding that some entries were language workarounds is a fact about the languages of 1994, not a licence to remove those shapes from a codebase that still compiles with the compiler it has. The finding is worth having because it changes what you conclude when you meet the pattern, not because it generates work.

---

## How to recognize the failure

**In a codebase:**

- **An interface with one method and one implementation, injected as a field.** That is Strategy with the variation never having arrived. In a language with function values there is nothing left to name.
- **`accept` methods on a type hierarchy in a language with pattern matching.** The double dispatch is being paid for and the compiler would do it.
- **A `Factory` whose `create` method contains a single `new` with no branching.** The pattern is a workaround for languages where a class is not a value; if yours are, the factory is a function that could be the constructor.
- **Per-method forwarding classes** — twenty methods, nineteen of which call straight through. Either the interface is too wide to decorate or the concern is not a decoration at all (Ch. 05).
- **Class names built from pattern names** — `PricingStrategyImpl`, `OrderVisitor`, `ConfigBuilderFactory`. When the pattern has dissolved, these are the residue: names describing apparatus that is no longer there.

**In a conversation:**

- **"We should use the Strategy pattern here."** In which language? If the answer is one with first-class functions, the proposal is "pass a function," and it should be said that way, because then someone can disagree with the actual design.
- **"That's just a closure."** Frequently correct, and it is a claim about the implementation rather than about the design. The design question — should this vary at all, and who decides — is untouched by the observation.
- **"Design patterns are obsolete."** The strong folk version of Norvig, and the seven patterns he did not list are the counter-evidence. So is every pattern in chapter 12 that answers a Force rather than a language gap.
- **A design document specifying patterns before specifying a language.** The catalogue is not language-independent, and half of it is a description of what you will have to build if you pick a language without the feature.

The question that does the work: **if I wrote this in a language with first-class functions and sum types, what would be left?**

Whatever survives is the design. Whatever vanishes was the cost of expressing it. [claude what does this bullet point imply in real world? I think we need to describe the right move without ambuguity: "Make the design document language independant and remove language specific patterns from it? State the language in the design document so that the language specific parts are obvious? Or...?"]

---

**Next:** chapter 14 turns from names that describe a shape to names that arrive with a verdict already attached — vocabulary like *anemic domain model*, where accepting the word means accepting the conclusion, and the argument was over before anyone noticed it had started.
