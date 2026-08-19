# OOP Versus the Direction Rule

## The claim

**"Behaviour belongs with the data it operates on" does not say where to place the behaviour goes when it needs two entities. Placing it on the entity it reads from leaves a reference pointing each way, and a value graph with a cycle in it breaks serialization, equality, and copying — costs that arrive whether or not the two are ever changed apart.**

This is the first of Part IV's three cases, and it runs chapter 15's mechanism on a specific piece of advice. The term carrying no fixed extent is *belongs with*.

---

## The demonstration

### The advice, and what it is

*Behaviour belongs with the data it operates on.* It is a Principle: good advice given certain Forces, and the Forces are real ones. A rule that lives next to the data it reads can be enforced rather than merely documented, and a caller who cannot reach the data cannot get the rule wrong.

It also has no author. Chapter 15's proverb had a recording, so the forty seconds of scope Pike gave it could be recovered by watching the talk. This sentence has no talk. It arrives in code review, in a style guide, in the first chapter of a book about objects, and there is nothing to go back to — which is the case chapter 15 named as the expensive one, where the context was a conversation and the scope cannot be reconstructed because nobody wrote it down.

So the reader is left with the words, and the words underdetermine one thing: **which** data. When a rule reads one entity, *belongs with* has one answer. When it reads two, it has two, and the sentence does not choose.

### A rule that needs two entities

An order discount depends on the customer loyalty tier and on the order total. Neither entity holds enough data to dictate the placement alone.

Read *belongs with* from the order's side — the rule is about this order's discount — and the method goes on `Order`:

```java
class Order {
    final long total;
    final Customer customer;

    // A rule over this order's total. It also needs the customer's tier.
    long discount() {
        if (customer.tier.equals("gold") && total > 10_000) {
            return total / 10;
        }
        return 0;
    }
}
```

`Order` now holds a `Customer`. One edge, pointing one way. Nothing is wrong yet, and chapter 05's Law is not yet engaged: a single edge is a dependency, not a cycle.

### The second rule, read the same way

A customer's lifetime value is the sum of their orders' totals. The data it reads is the customer's orders, so the same reading of the same sentence puts it on `Customer`:

```java
class Customer {
    final String name;
    final String tier;
    final List<Order> orders = new ArrayList<>();

    // A rule over this customer's orders. The data it needs is theirs.
    long lifetimeValue() {
        long total = 0;
        for (Order order : orders) {
            total += order.total;
        }
        return total;
    }
}
```

**Neither placement is a misreading.** That is the part worth stopping on. Each rule went to the entity whose data it is about, which is what the sentence says to do. No one was careless, and no review would catch either method in isolation.

The graph now has an edge in each direction. `Order` holds a `Customer`; `Customer` holds a list of `Order`. Java compiles this without a word — the two classes are in the same compilation unit, and the language has no opinion about the direction of a field reference.

### What the object graph now is

Running both rules works. The design does what it was built to do:

```text
discount      = 2500
lifetimeValue = 25000
```

Then ordinary code touches it. Putting the order in a set — not a clever operation, and not one anybody thinks of as recursive:

```java
Set<Order> dispatched = new HashSet<>();
dispatched.add(order);
```

```text
Exception in thread "main" java.lang.StackOverflowError
	at java.base/java.util.Arrays.hashCode(Arrays.java:4537)
	at java.base/java.util.Objects.hash(Objects.java:126)
	at Customer.hashCode(Shop.java:28)
	at java.base/java.util.Objects.hashCode(Objects.java:97)
	at java.base/jdk.internal.util.ArraysSupport.hashCode(ArraysSupport.java:324)
```

`Objects.hash(name, tier, orders)` on the customer hashes each order, which hashes its customer, which hashes its orders. The recursion is in the data, so every operation that walks the graph inherits it. The same happens to a generated `equals`, a generated `toString`, and any deep copy.

**This is a different cost from the one chapter 05 prices.** That chapter's test for whether a cycle matters is *will these ever be understood, tested, or changed apart* — and it concedes that two types which never operate separately, pay nothing, because they were one unit before the cycle existed. `Customer` and `Order` may well be such a pair. The stack overflow above does not care. It arrives on the first call, in code nobody wrote, and no answer about future change makes it go away.

### The cost is not confined to one language

Serialization is where it usually surfaces first, because that is where a graph gets walked by something that did not model it. In Go, with the same two types holding each other:

```go
customer := &Customer{ID: uuid.New(), Name: "Acme", Tier: "gold"}
order := &Order{ID: uuid.New(), Total: 25_000, Customer: customer}
customer.Orders = append(customer.Orders, order)

_, err := json.Marshal(customer)
```

```text
cyclic:  json: unsupported value: encountered a cycle via []*main.Order
```

Go's `&` takes the address of a value, so `*Order` is a reference to an order rather than a copy of one — the same aliasing a Java field reference gives you by default. Python's standard library refuses the same shape with `ValueError: Circular reference detected`.

Three languages, three unrelated implementations, and none of them can encode the graph. The reason is not a gap in any of the libraries. A tree serializes because every node is reached once; a cyclic graph has no such traversal, so a format built on nesting has nothing to emit.

### The same shape, refused, with the reasoning recorded

FlowCore had this decision in front of it and wrote down the rejection. Its workflow definitions contain steps, and steps contain actions that point at the next step. Option D in its decision log is the pointer wiring — `Action{NextStep: dir}` — which makes the definition a cyclic graph in memory. [claude without a code example showing the cylcic version and current version in Flowcore's contex, this paragraph's point is just left to the imagination of the reader. Also, reader would like to see what flowcore achieved with that code at what cost: the trade-off. If adding those would be a repetion of what's laid out on "The narrow reading, and what it looks like" section below you decide on what to do. Maybe this becomes another example after that sections or you can just remove this section.] The entry's own words:

> D poisons everything downstream — a cyclic struct can't be JSON-serialized by a client admin page, read-back has to rehydrate pointers, and test assertions loop.

Three costs, and none of them is about future change. **Serialization** is the failure above. **Read-back has to rehydrate pointers** means the thing loaded from the database is not the thing that was written until something walks the graph and reattaches the references, which is code that exists only to restore a shape the database cannot hold. **Test assertions loop** is the equality problem: comparing two definitions follows the back-pointers and does not terminate.

### The narrow reading, and what it looks like

The other reading of *belongs with* is already in Chapter 14: "place the rule where it can see all the data it needs". The location follows from how much you must be looking at before you can tell whether the rule holds. Under that reading, a rule needing a customer and an order belongs at a scope that can see both, and that scope is neither entity.

What the entities hold instead is an identifier:

```go
type FlatCustomer struct {
	ID   uuid.UUID
	Name string
	Tier string
}

type FlatOrder struct {
	ID         uuid.UUID
	Total      int64
	CustomerID uuid.UUID
}
```

`CustomerID` is a `uuid.UUID` rather than a `*Customer`, so the order names its customer without holding one. The reference still exists; it is no longer an edge in the object graph. The same values encode without complaint:

```text
flat:    <nil>, 187 bytes
```

Replacing a reference with an identifier is one of the four ways chapter 05 lists for turning a cycle into a line, and it is the one that costs a lookup rather than an interface. What is bought here is not smaller change cost — it is that the value is a tree again, so encoding, comparing, and copying work the way the language's own tools expect.

The discount rule then lives wherever both values are in hand. That is usually the service or use-case layer, which had to load them both anyway. [two paragraphs before this tag are very dense, packed with abstract concepts and metaphors: "cyle into a line, lookup rather than interface, values is a tree, bought chane cost, discount..." Rewrite those with a more direct, clear language and don't try to make many claims on short paragraphs. Dont' force the reader to decipher your points.]

---

## Why the claim holds

The sentence names a relation and not a scope. *Belongs with* asserts that behaviour and data should be together; it says nothing about what to do when the behaviour needs two data. Chapter 15's finding applies without modification: where a principle does not name the situation it applies to, the reader resolves it, and with no context to narrow the reading, the widest one is the only one available. Here the widest reading of *belongs with* is *on the entity, reaching whatever it needs* — which licenses a field pointing at the other entity every time a rule spans a pair.

The direction of the error is set by the same asymmetry. Nobody resolves *belongs with* too narrowly and puts a single-entity rule three layers away. The reading that adds edges is the one available by default. [claude maybe small code example or diagram or table demonstrating this direction: "probably nobody would do this: Order Customer..."]

Two properties of object languages let this run unchecked.

**The reference is the default way to model a relation.** A field holding another object is the first thing the language teaches, and it is free at the point of writing. An identifier is more typing and buys nothing until something walks the graph.

**Nothing checks at the granularity where it happens.** Chapter 05 makes the general point — each toolchain checks the boundaries it happens to have. Here the boundary is a class, and no mainstream object language treats mutual reference between two classes as anything at all. Go will refuse an import cycle between two packages; it has nothing to say about two structs in one package holding each other. The cycle is invisible to every tool in the build until a value is constructed and something tries to walk it.

Which is why the failure arrives as a stack overflow in a set insertion rather than as a design review comment.

---

## Where the claim doesn't apply

### A rule that never leaves one entity

The claim is about rules that need two entities. Where a rule needs one, the advice is right and this chapter's caution produces the failure chapter 14 describes: the rule is moved away from the only data it reads, for no gain.

A money value is the clean case. Adding two amounts requires checking that the currencies match, and everything that check reads is inside the value:

```java
record Money(long minorUnits, String currency) {
    Money plus(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("currency mismatch");
        }
        return new Money(minorUnits + other.minorUnits, currency);
    }
}
```

`Money` holds no reference to anything that holds it. The method reads two money values and nothing else, so there is no second entity for an edge to point at, and no reading of *belongs with* produces one. Moving `plus` to a `MoneyService` would put the currency check where a caller can skip it, which is the enforcement argument in chapter 05, running in the opposite direction from this chapter's advice.

The same holds for a state machine over a single aggregate. If the legal transitions of an order depend only on the order's own status and lines, they belong on the order, and chapter 12's aggregate is the shape that says so.

### The cycle that costs nothing

Two types that hold each other and are never separated, never serialized, never compared, and never deep-copied pay none of the costs in this chapter. A parser's node types are the standard example — mutually recursive by nature, and nobody calls it a defect.

The test is mechanical rather than a matter of taste. **Does anything walk this graph generically?** Serialization, structural equality, hashing, deep copy, and a debugger's object inspector all do. If the answer is no today, the cycle is free today [claude something is off here, you say "never separated, never..." and then the test is "if the answer is no today". Test doesn't match the claim. ], and chapter 05's question about whether the two will ever be understood apart is the one that decides whether it stays free.

The reason the answer is so often yes is that generic walkers arrive late and from outside. Nobody adds a back-pointer while planning to expose an admin page, and the admin page is written by somebody else a year later.
[clause this paragraph need a more clear beginning. Is the answer to the mechanical test or to the chapter 05's question, and what's the importance of the answer being so often yes?]

---

## What the claim costs

**Identifiers move errors from compile time to run time.** `order.customer.tier` cannot be null-dereferenced in a language that checks it; `customerID` can point at a customer that no longer exists, and only a lookup finds out. What was a type error becomes a missing row.

**Every traversal becomes explicit work.** With references, `customer.orders` is free at the call site. With identifiers, somebody must fetch the orders for a customer, and the code that does it has to exist, be tested, and be called in the right order. Chapter 12's N+1 problem is what happens when this is done carelessly.

**The rule's location stops being obvious.** On an entity, a rule has one plausible home and everybody finds it. At a service that sees both entities, there are several plausible homes, and without a stated method for choosing — which chapter 19 owns — the placement becomes a matter of local habit.

**Flat structures read as procedural, and that carries a social cost.** A team fluent in object modelling will recognize the shape as the one chapter 14 defends against a verdict noun, and the argument has to be made again on every review. The technical answer is settled and the vocabulary is not.

---

## How to recognize the failure

**In a codebase:**

- **A back-pointer whose only reads are traversals.** `order.customer.orders` appearing anywhere means the graph has a cycle in it, and something walked all the way round.
- **Serialization configured rather than working.** `@JsonIgnore`, `json:"-"`, a custom encoder, or a DTO layer whose only job is to flatten. Each of these is the cycle being paid for at the boundary, and the annotation records where somebody hit it.
- **Equality and hash methods that exclude a field with a comment explaining why.** The comment usually says *to avoid infinite recursion*, which is the defect named and left in place.
- **Test fixtures that cannot build one entity without the other.** If constructing an order requires a customer and constructing a customer requires the order list to be wired back, every test carries the whole graph.
- **A deep-copy or clone routine with a visited set.** Cycle handling written by hand, in a helper nobody wanted.

**In a conversation:**

- **"Put the logic on the entity"** offered without asking what the rule reads. The question that separates the two readings is how many entities you must be looking at before you can tell whether the rule holds.
- **"It's an anemic domain model"** used against flat structures with identifiers. Chapter 14 has the answer: the term carries an antecedent about wasted mapping cost that the speaker has to establish before the word means anything.
- **"The ORM handles it."** It materializes the cycle rather than removing it, and the costs above are then paid inside the framework's rules instead of yours.

The question that does the work: **what walks this graph that nobody on this team wrote?** [claude my wording: what tool we don't own will walk our object graph][claude "does the work" what work? Why we would ask this question and what the answer would indicate? For example: Json serializer walks it or equality walks it. So what? Also the answer for this question would most typically be: "nothing walks right now, but in any program that is not a one-off script, those walks can be introduced at any moment by any dev. They are treated as trivial coding drudgery.]

Serialization, equality, hashing, and copying are all written by somebody else, and all of them assume a tree. A back-pointer is a promise to that code that it will never be asked to walk in a circle, made by people who will not be in the room when it is. [claude my reading is that one more sentence is needed here, you state a context and then leave it in the air, what's the lesson, conclusion?]

---

## Sources

- FlowCore, `docs/decisions.md`, decision 3 — [github.com/ilke-akdeniz/flowcore](https://github.com/ilke-akdeniz/flowcore).
- *Objects.hash* and *HashSet* — [docs.oracle.com/en/java/javase/26/docs/api](https://docs.oracle.com/en/java/javase/26/docs/api/).
- Go, `encoding/json` — [pkg.go.dev/encoding/json](https://pkg.go.dev/encoding/json).

---

**Next:** chapter 17 turns to testing, where *test behaviour, not implementation* meets the mock that asserts about itself, and a suite that passes after the constraint it was defending has been deleted.
