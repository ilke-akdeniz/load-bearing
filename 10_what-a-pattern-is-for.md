# What a Pattern Is For

*A pattern is not one of the book's five kinds, and that is the first thing to get straight. Law, Force, Principle, Idiom, and Style classify **claims** — things that can be true, false, or conditional. A pattern is a **name for a shape**. Names are not true or false. The trouble starts when a name is used as though it were a claim, which is most of what Part III is about.*

## The claim

**A pattern name earns its place by doing two things: saving more words than it costs, and ruling something out. Most named things do the first. Far fewer do the second.**

Those are the two tests, and the rest of Part III applies them. They are independent — a name can pass one and fail the other, and the names that fail the second are the ones that cause trouble, because they feel informative while carrying almost nothing.

## What a catalogue actually is

Before the tests, what the thing being tested is for.

A pattern catalogue is a record of shapes that were already occurring. Fowler's *Patterns of Enterprise Application Architecture* wrote down what enterprise Java teams were doing in 2002. The Gang of Four book — Gamma, Helm, Johnson, and Vlissides, 1994, and the source of most pattern vocabulary in circulation — catalogued shapes its authors found in existing C++ and Smalltalk systems.

That is **ethnography**: someone observed a population and named the recurring structures. It is descriptive work, and it is genuinely useful, because a shape that keeps appearing independently is worth having a word for.

What happens next is the problem, and it is a mechanism the book has already named. Chapter 04 draws the line between a claim that **describes** what happens and one that **prescribes** what to do — and notes that only a prescription can be bad advice, because only a prescription is advice. A catalogue describes. Read as a checklist, "shapes that occur" silently becomes "shapes you should have," and a list of observations becomes a list of obligations.

Nobody performs that conversion deliberately. It happens because a catalogue of solutions, read by someone with a problem, looks exactly like a menu.

---

## The demonstration

### Test one: does the name save more words than it costs?

The straightforward test, and the easier one to pass.

A name compresses when it stands in for a description you would otherwise have to write out. That is measurable — count the words:

```text
 name                 words   the description it replaces      ratio
 Transaction Script     2     26 words                          13:1
 Singleton              1     14 words                          14:1
 Idempotency key        2     22 words                          11:1
 Manager                1     no agreed description               —
 Helper                 1     no agreed description               —
```

For the first three, the compression is real. Writing *a procedure that handles one business operation end to end, owning its own transaction boundary, orchestrating stateless data access, with no persistent object model in between* is twenty-six words; writing *Transaction Script* is two, and the reader recovers the same content.

The last two fail, and it is worth being exact about why, because it is not that the words are short. **They fail because there is nothing specific for them to stand in for.** Ask two engineers what a `Manager` is and you get two answers, so the name saves you writing a description only by not conveying one.

**Compression has a condition, and it is the one people forget.** The saving only exists for a reader who already knows the term. Introduce *Transaction Script* to someone who has not met it and you have spent twenty-six words on the definition plus two on the name — you are worse off than if you had described the thing.

So compression is a claim about a shared vocabulary, not about a word. A name coined inside one codebase compresses nothing for anyone outside it, however precise it is. That is the difference between vocabulary and jargon, and it is decided by the audience rather than by the term.

### Test two: does the name rule anything out?

The harder test, and the one that separates a name carrying information from a name that only sounds like it does.

The test is mechanical: **take the name, and try to write code it forbids.** If you can write the forbidden code and still honestly use the name, the name is not constraining anything.

**Singleton** — a type with exactly one instance for the lifetime of the process.

```go
// Permitted, and the only way in.
a := Thing.Instance()
b := Thing.Instance() // a and b are the same object, always
```

```go
// Forbidden. If this compiles, it is not a Singleton.
a := NewThing()
b := NewThing()
```

A strong constraint. Being told something is a Singleton tells you that any two references to it are the same object, without opening the file.

**Transaction Script** — a procedure that handles one business operation end to end.

```go
// Permitted: the rule is in the procedure, the data is inert.
func ApplyDiscount(ctx context.Context, db *sql.DB, id string, pct int) error {
	tx, _ := db.BeginTx(ctx, nil)
	// read rows, compute, write rows, commit
}
```

```go
// Forbidden: a persistent object model between the operation and the data.
order := repo.Load(id)   // an entity with behaviour and identity
order.ApplyDiscount(pct) // the rule lives on the object
repo.Save(order)         // written back through a mapper
```

Also a real constraint. It tells you where the business rule is *not* — not on a loaded object graph — and that rules out an entire style.

**Facade** — an object providing a simplified interface to a larger body of code. Now try to write what it forbids:

```go
type Billing struct{ /* ... */ }

func (b *Billing) Charge(id string) error {
	// calls four other packages, exposes one method
}
```

Is that a Facade? Yes. Is anything that calls several things and exposes fewer methods a Facade? Also yes. **There is no code the name forbids**, which means being told something is a Facade tells you approximately nothing about what you will find when you open the file.

That is not an argument against the word existing. It is an observation that it belongs in the vocabulary bucket, not the constraint bucket — and chapter 11 shows that the answer changes with scale, which is a different question from this one.

### The two tests are independent

Facade is the case that proves it: it compresses well and constrains nothing. Putting the tests on two axes gives four outcomes, and each behaves differently in a codebase.

| | **Rules something out** | **Rules nothing out** |
|---|---|---|
| **Compresses** | earns its place — *Singleton, Transaction Script, Idempotency Key* | vocabulary only — *Facade, Component* |
| **Doesn't compress** | rare, and usually a convention rather than a pattern | noise — *Manager, Helper, Util, Service* |

The top-left names are worth learning and worth using in review. They let you say something short and be understood precisely, and they let you rule out implementations without reading them.

The top-right names are fine in conversation and useless in an argument. "This should be a Facade" is not a design position, because it excludes nothing.

The bottom-right is where naming goes to die. `OrderManager`, `PaymentHelper`, `DataUtil` — each tells you the file exists and nothing else, and their prevalence is a symptom rather than a style: they appear when nobody could name what the code actually does.

---

## Why it holds

Both tests are about the same thing from two directions: **how much does knowing this name reduce what I still have to find out?**

Compression measures it in words. If the name replaces a description, hearing it saves you reading that description.

Constraint measures it in possibilities. If the name forbids implementations, hearing it eliminates them from what the code might be doing — before you open the file.

A name that does neither has not told you anything. It has only asserted that the author had a word for it, and it is the *feeling* of having been told something that makes this hard to notice. `OrderManager` reads like a description. It behaves like a filename.

There is one more reason a name can be worth having even when both tests are marginal, and it is worth stating because it is the honest case for keeping pattern vocabulary at all: **a name is an index into the literature on its failure modes.** Knowing your design is a Saga lets you find out what other people got wrong with sagas. That value is real and has nothing to do with either test — it is a claim about the name being *searchable*, not about it being informative.

---

## Where this doesn't apply

### Before you know what the shapes are

The tests assume you can say what the code does. Early on you cannot, and then a vague name is the honest one.

A folder holding four things that do not yet belong together is a holding pen, and calling it something precise would be a claim you have not earned — one you would then have to maintain, or quietly break. Waiting for a little more functionality to accumulate often turns four awkward things into three natural ones, and the natural ones name themselves.

So the failure is not the vague name. It is **losing track of the fact that it is provisional**, at which point the holding pen becomes the architecture by default, and a name that was honest becomes a name that hides.

The check is the one chapter 03 gives for any deferred decision: write down what would have to become true for the name to be settled. *This is `pending/` until the third importer lands, and then we split it* is a different artifact from `pending/` with no note attached, even though the code is identical.

### Local vocabulary, where compression is real and private

A team that has agreed what a "projection" means in their system gets full compression from the word, and gets nothing from it in a conference talk.

That is fine, and it is not a lesser thing than a published pattern. It fails the compression test only against outsiders, and a codebase is mostly read by insiders. The mistake is exporting the word without the definition — a design document that uses a local term as though it were standard, read by someone who has to guess.

### When the name is load-bearing for search

Some names are worth using even where they compress poorly, because they are how you find the prior art.

If you are building something that periodically stops calling a failing service, calling it a *Circuit Breaker* buys you access to two decades of people writing about half-open states, failure thresholds, and what happens when the breaker itself becomes a single point of failure. The name is a mediocre description and an excellent search term. Use it, and do not pretend it is doing the other job.

**This is also the whole of what a weak name gives a learner**, which is worth saying because the opposite is widely assumed. Telling a student *this is a Facade* does not teach them when a simplified interface is the right move, what it costs, or how to design one that is pleasant to use. It teaches them a word — and if the reason behind the shape is not given alongside it, the name can make things worse, because the student now has a label and believes they have an idea. The conditions under which the shape is wrong were never mentioned, which is the mechanism chapter 15 traces from compressed judgement to slogan.

The defensible version is narrow: a name a learner can search is a door into the discussion of when the shape fails. A name without that discussion attached is a sound they can make in a meeting.

---

## What it costs

**Applying the tests takes longer than accepting the name.** Most of the time the name is fine, the shape is obvious, and running two tests on it is wasted effort. These are for the cases where a name is being used to win an argument.

**The tests are a licence to be tiresome.** "Well, what does that rule out?" is a real question and also an excellent way to stall a design discussion. Ask it when a name is carrying the weight of a decision. Do not ask it about every noun in the room.

**Naming precisely costs more than naming vaguely.** `OrderManager` takes no thought, which is why it exists. Naming the file for what it actually does requires knowing what it actually does, and sometimes the reason nobody named it well is that it does four unrelated things — in which case the naming problem is a structural problem wearing a disguise — unless the design is genuinely too young to name, which the boundary section above covers.

**A name that passes both tests can still be the wrong shape for you.** Singleton compresses and constrains beautifully, and is usually a mistake. The tests measure whether a name carries information, not whether the thing it names is a good idea. That is a separate question, and Part III spends the rest of its chapters on it.

---

## How to recognize the failure

**In a codebase:**

- **`Manager`, `Helper`, `Util`, `Service`, `Handler`, `Processor`, `Data` in a type name**, where removing the suffix would lose nothing. The suffix is standing in for the description nobody wrote.
- **Two files whose names differ only by suffix** — `OrderService` and `OrderManager` — where nothing tells you which does what.
- **A pattern name in a type name that is not true of the type.** `UserFactory` that returns one hard-coded instance, `PaymentStrategy` with one implementation and no second in prospect.
- **A directory named for a pattern rather than for the domain**, so `strategies/` holds four unrelated things whose only common property is that somebody applied the same word to them. The reason it fails: **a directory should group things that change together, and a pattern name groups things that are shaped alike** — so every feature change reaches into a folder of code belonging to other features, and nothing in it can be read without first working out which feature it serves.
- **A design document that names patterns and never says what they exclude.**

**In a conversation:**

- **"That should be a Repository."** Followed up with: what would that rule out that the current code does?
- **"We're using the Strategy pattern here."** Sometimes real information. Sometimes a description of `if`, or of passing a function — chapter 13 works through the GoF names that turn out to be language features once the language has them, and Strategy is the clearest case.
- **"This doesn't follow the pattern."** Which pattern, and what makes following it correct here rather than elsewhere?
- **A design review scored against a catalogue**, where the finding is that a named shape is absent rather than that something concrete goes wrong.
- **A name introduced in a meeting and used as a premise by the end of it.** The gap between naming a thing and having established anything about it is where most of this goes wrong.

The question that does the work: **what does this name let me stop wondering about?**

If the answer is a description you no longer have to write, the name compresses. If it is a set of implementations you no longer have to check, the name constrains. If it is neither, you have been told the author had a word for it.

---

**Next:** chapter 11 takes the pattern vocabulary the two tests just filtered and shows that the answer changes with size — the same name that carries nothing at the scale of a class can be a serious architectural commitment at the scale of a system.
