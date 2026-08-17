# Smuggled Verdicts

## The claim

**Some vocabulary carries its verdict inside the noun. You can use a word like that or you can disagree with it, but not both — so whoever picked the word has already settled the argument.**

Chapter 10 says a pattern name is not one of the five kinds, because names are not true or false. This chapter is about the exception: a name built so that using it asserts something. Those behave like claims while keeping a name's exemption from having to be defended.

## Three tiers, and the test that separates them

Not standard vocabulary — this grading is the book's own, and it exists because "loaded language" is too coarse to be useful. Terms differ in how much room they leave you.

The test is one sentence long. **Apply the term to your own code, then say the code is fine as it stands, and see whether the result means anything.**

- *"This is a Transaction Script, and that is the right shape here."* Means something. **The term is a shape name.** It says what the code is and stops.
- *"That is a code smell, and it is fine here."* Means something, slightly uncomfortably. **The term is a hint word.** It leans, and it lets you push back.
- *"This is an anemic domain model, and that is correct here."* Means nothing. **The term is a verdict noun.** *Anemic* means sick; the sentence contradicts itself, so the word cannot be used by anyone who disagrees with it.

The test yields three tiers: shape name, hint word, verdict noun. The third tier is the subject of this chapter. The first two are here to show that the problem is not judgment in vocabulary — it is judgment that cannot be answered without abandoning the vocabulary.

---

## The demonstration

### The same code, named twice

Here is an invoice, in the style a great many working systems are built in. Plain data, functions that operate on it, and constraints in the database.

```go
// The whole type.
type Invoice struct {
	Number   string
	Year     int
	Lines    []Line
	VoidedAt *time.Time
}

type Line struct {
	Description string
	AmountMinor int64
}

func (i Invoice) TotalMinor() int64 {
	var total int64
	for _, line := range i.Lines {
		total += line.AmountMinor
	}
	return total
}

func (i Invoice) IsVoided() bool { return i.VoidedAt != nil }

var ErrNoLines = errors.New("an invoice must have at least one line")

func Issue(invoice Invoice) error {
	if len(invoice.Lines) == 0 {
		return ErrNoLines
	}
	return nil
}
```

```sql
create unique index ux_invoice_number_per_year on invoice (year, number);
```

Now two sentences about that code. Both are accurate.

> It is a Transaction Script over a table gateway. Value-scoped rules are methods on the type, the whole-invoice rule is in the operation, and the uniqueness rule is a database constraint.

> It is an anemic domain model — objects with hardly any behaviour, a bag of getters and setters, with the logic pulled out into services.

The first describes the file. The second describes the file *and convicts it*, and the difference is not the content. It is that the second sentence has an answer built into it, so a reply has to start by rejecting the vocabulary before it can get to the design. In a code review, the first invites *why is the rule there?* The second invites agreement or a fight.

**That is the whole mechanism.** A name that convicts does not have to argue, because the argument arrives already finished.

### What Fowler actually argued, and the condition that does not travel

Worth reading the source rather than the reputation, because the original is careful and narrow.

Fowler's *AnemicDomainModel*, November 2003, states the problem in one sentence:

> In essence the problem with anemic domain models is that they incur all of the costs of a domain model, without yielding any of the benefits.

Read that as the conditional it is. **It has an antecedent: you already paid for a domain model.** The object-relational mapping layer, the object graph, the identity management, the lazy loading. Having paid, you then put the behaviour somewhere else and collected none of the return. The complaint is about a wasted payment, not about behaviour on objects being right in general.

And the article says so directly:

> Domain Models aren't always the best tool.

So the argument is: *if* you bought the machinery, use it. Applied to the invoice above, the antecedent is absent. There is no mapping layer, no object graph, no identity map, no lazy loading — a struct, some functions, and a table. Nothing was paid, so nothing was wasted, and the cost-benefit argument has nothing to attach to.

**The verdict travels and the condition does not.** That is not a fact about Fowler; it is a fact about the shape of the term. *Incurring the costs of a domain model without the benefits* is nine words carrying a condition. *Anemic* is one word carrying the conclusion, and it is the one word that survives being repeated.

### The third option the binary cannot see

The term offers two positions: behaviour on the objects, or behaviour nowhere. The invoice above is in neither, and the reason it looks like the second is that the term has no name for the third.

**Behaviour is not absent, it is placed** — and what decides the placement is **scope**, meaning how much data you have to be looking at before you can tell whether a business rule holds. This is the author's formulation, developed while building FlowCore, and it is not standard vocabulary.

Ask the question of any rule and it answers where the rule can live:

```text
 how much you must see        where it goes   invoice example
 --------------------------   -------------   ----------------------
 one value, in hand           on the type     the total is the sum
                                              of the lines
 the whole object at once     the operation   an invoice needs at
                                              least one line
 rows you have not loaded,    the schema      invoice numbers are
 and writers running now                      unique within a year
```

The first two are preferences. The third is not: a rule about rows you have not read cannot be enforced by code that has not read them, and chapter 06 works through why the check-then-write version races. So the placement is a fact about what each layer can see rather than a doctrine anyone adopted.

Run it, and the uniqueness rule is enforced exactly where it has to be:

```sql
insert into invoice (year, number) values (2026, '2026-0001');
insert into invoice (year, number) values (2026, '2026-0001');
```

```text
Runtime error near line 9: UNIQUE constraint failed: invoice.year, invoice.number (19)
```

The first insert says nothing, because it worked. The second is refused by the index, in the one component that can see both the rows already there and the writer arriving at the same moment.

That constraint is a business rule, fully enforced, and it is behaviour by any definition that is not circular. It is invisible to a term whose only measure is how many methods hang off the entity. **The design is not short of behaviour; the term is short of places to look.**

Chapter 05 reaches the same place from the structural side, where a `completed_at is null` gate makes the lower layer the more capable one and inverts layering doctrine. Here the point is narrower: a term that cannot see the third option will misclassify every design that uses it.

### "Code smell" carries its own dissent, and usage removes it

This is a hint word, and it fails differently — which is why it is worth putting next to the first.

Fowler's definition, crediting Kent Beck with the coinage:

> A code smell is a surface indication that usually corresponds to a deeper problem in the system.

*Surface indication.* *Usually.* And elsewhere in the same piece, that smells "don't *always* indicate a problem" and "aren't inherently bad on their own — they are often an indicator of a problem rather than the problem themselves."

The definition is built to be arguable. A smell is a reason to look, and the word was chosen for exactly that: you investigate a smell, you do not convict on one. So *"that is a smell and it is fine here"* is a sentence the definition licenses.

What happens in practice is that the hedge is dropped and the metaphor is not. *Smell* belongs to a family — rot, hygiene, cleanliness, clean code — and that family does not have a neutral setting. Told your code smells, you are not being handed a place to look. Chapter 15 traces how a name outlives the conditions it was issued with; this is the special case where the leftover word is one that implies dirt.

The difference from *anemic* is worth keeping, because it decides what to do:

- With **code smell**, the qualifier exists and can be restored. *A smell is a place to look* is a defensible reading with the author on your side.
- With **anemic domain model**, there is no qualifier to restore, because the judgment is in the noun rather than in the sentence around it.

---

## Why the claim holds

A word does two jobs at once: it picks out a thing, and it comes with a stance. Most technical vocabulary keeps the second job near zero. *Hash table*, *mutex*, *idempotent*, *Transaction Script* — each names something and asserts nothing about whether you should want it.

A verdict noun bundles them, and the bundling is what makes it hard to answer. To disagree you first have to refuse the word, and refusing a word looks like evasion. **The cost of the term is borne by whoever is right and did not pick the vocabulary.**

Two properties follow, and they are why this is worth a chapter rather than a complaint.

**It is not a claim, so it never has to be defended.** Chapter 10's point is that names sit outside the five kinds — they are not true or false. A verdict noun exploits that: it does the work of a claim while keeping a name's exemption. Nobody has to state the condition, because on the surface nothing has been asserted.

**It compresses well, which is why it spreads.** Run chapter 10's first test on it and *anemic domain model* passes easily — three words standing in for a paragraph. It is a good name by that measure. That is the uncomfortable part: the terms that travel furthest are the ones that compress best, and compression is exactly the operation that leaves conditions behind.

---

## Where the claim doesn't apply

### When the verdict is warranted, because the term names a Law

Some loaded terms are loaded correctly, and the test is whether the condition can fail.

**A verdict noun naming a Law violation.** *SQL injection* — building a query by pasting user input into the text of it, so that input containing a quote can close the string and start a statement of its own. The judgment is in the name: *injection* is something done to you. And it is warranted, because there is no configuration of Forces that makes it right. Not on an internal tool, not on an admin page nobody outside can reach, not at any size of team or any latency budget. The condition attached to the verdict is *always*, so compressing it away costs nothing. *Data race* and *buffer overflow* work the same way.

**A verdict noun naming a Principle violation.** *Premature optimization* — where the judgment is in the first word. Chapter 02 classifies the slogan it comes from as a Principle routinely quoted with its conditions removed; here the interest is the noun phrase, which asserts that the timing question is settled.

Whether an optimization is premature is a latency-budget question, and chapter 03 works that budget across four orders of magnitude — a page render with 200 milliseconds to spend, against an order matcher with 200 microseconds. Hand-tuning a loop on the first day is waste in the first case and is the entire job in the second.

Same work, same point in the schedule, opposite verdicts. So the term does not describe the code — it announces a conclusion about a Force it never asked anyone to measure, and somebody who disagrees has to reject the word before they can say which case they are in.

That gives the claim's boundary a form the book already has: **a verdict noun is legitimate when it names a Law violation, and dangerous when it names a Principle violation.** A Law has no conditions that can fail (Ch. 02), so a term naming one loses nothing by compressing. A Principle is conditional by definition, so a term naming its violation drops exactly the part that mattered.

*Anemic domain model* fails on the same grounds as *premature optimization*: its condition — you already paid for a domain model — is a Force question, and the answer varies by project.

### Refusing all judgment-laden vocabulary is its own over-correction

The reading to avoid is that technical language should be neutral. It should not, always. Some code is bad, some designs are mistakes, and a vocabulary with no way to say so is worse than one that occasionally says so wrongly.

*Never use a loaded term* is a slogan of the same kind as the ones this chapter is about — a compressed rule with its conditions removed. The working version is narrower: **when you use a term that convicts, say the condition out loud in the same breath**, because the term will not carry it for you. *This is anemic in Fowler's sense — you are paying for the mapping layer and getting nothing back* is a sentence somebody can answer. *This is anemic* is not.

### A term's tier is not fixed, so the test has to be re-run

The grading above describes words as they are used now, by the people around you. It is not a property the word carries permanently, and the clearest evidence is a term that has moved in both directions inside fifteen years.

*Monolith* began as a shape name. A single deployable unit — that is all it meant, and *"it is a monolith, and that is the right shape here"* was an unremarkable sentence. Through the middle of the 2010s it became a verdict noun: the thing you were migrating away from, the answer to what went wrong, and saying your system was a monolith was conceding a point. Then *modular monolith* arrived and pulled it partly back, and the neutral sentence is sayable again in some rooms and not in others.

Nothing about the word changed. What changed is what a listener assumes you have conceded by using it.

Two consequences. **The test is about a term in a community at a time**, so running it once and remembering the answer will eventually be wrong. And **a word can be a shape name in one room and a verdict in the next** — which is not a flaw in the test, it is the thing the test measures, and it is why the answer has to come from the people you are actually talking to rather than from a glossary.

---

## What the claim costs

**Auditing vocabulary is a way to avoid answering.** "That term smuggles a verdict" can be true and can also be a refusal to discuss the code. If someone calls a design anemic and the design *is* an object graph with an ORM and no behaviour, they are right, and the etymology of their word is not the topic.

**The three tiers are a spectrum, and the middle is genuinely contested.** *Code smell* is a hint word here because its author defined it with the hedge attached. Someone could argue it is a verdict noun, on the grounds that the hygiene metaphor overwhelms the definition in every real use — and that is a reasonable position rather than a misreading.

**Watching your own words is a tax on saying anything.** Stating the condition every time you use a compressed term is correct and it is slower, and in a review with forty comments it will not happen. The realistic version is to spend it on the load-bearing ones: the comment that will decide whether something gets rewritten.

**A term with the verdict removed sometimes has nothing left.** Strip *anemic* of its judgment and what remains is *behaviour is not on the entities*, which is a neutral fact about a file and not worth a name. That is a real finding rather than a loss — the compression was doing the convicting — but it does mean the replacement is a sentence rather than a word, and sentences do not travel.

---

## How to recognize the failure

**In a codebase and its documents:**

- **A review comment naming a defect with no statement of what breaks.** "This is anemic," "this smells," "this is not clean" — none of which say what goes wrong or under what conditions.
- **An architecture decision record whose rationale is a diagnosis.** *We rejected X because it produced an anemic model* records the verdict and not the reasoning, so nobody can revisit it when the Forces change.
- **A style guide with a banned-shapes list and no conditions attached.** The shapes are usually right and the missing conditions are what somebody needed.
- **A term whose opposite has no name.** *Anemic* has no antonym in use — nobody says a model is *robust* as a technical classification — which is a sign the word exists to fail things rather than to sort them.

**In a conversation:**

- **"That is an anti-pattern."** Which one, and what did its author say the conditions were? The word *anti-pattern* is itself a verdict.
- **"This isn't clean."** Against what definition, and what happens if it stays?
- **A design defended by renaming it.** If *Transaction Script* and *anemic domain model* describe the same file, the argument is about the word and the design was never in question.
- **Agreement reached suspiciously fast after a term is introduced.** Nobody wants to be the person defending sick code, which is what the word is for.

The question that does the work: **what would have to be true for this to be fine, and does the term let me say it?**

If the answer is a condition you can state and check, you have a claim and can argue with it. If the term forbids the sentence, you have been handed a conclusion.

---

**Next:** chapter 15 opens Part IV with the mechanism behind all of this — how a true observation acquires a name, the name acquires a community, and the community forgets the conditions that made the observation true.
