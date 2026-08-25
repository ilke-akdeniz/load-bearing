# Smuggled Verdicts

## The claim

**Some vocabulary arrives with its verdict attached, so accepting the word concedes the argument — and how much you have conceded depends on whether the word also names something you can go and check.**

Part III has been about names. [Chapter 09](09_what-a-pattern-is-for_3xzc.md) asked what a name buys and answered in two tests, which it ran on `Manager` and `Helper` as readily as on Singleton — because the tests are about names, and patterns are only the richest supply of them. The three chapters since graded the catalogue's names against ownership, against Forces, and against the language you write them in.

This is the last thing a name can do. [Chapter 09](09_what-a-pattern-is-for_3xzc.md)'s finding was that a name sits outside the five kinds: it picks out a shape, and a shape is not true or false. Some names are built to break that — using one asserts something — and they do it while keeping a name's exemption from ever having to be defended. Pattern culture produces the densest supply of those too, which is why the chapter sits in this part; the mechanism is not confined to patterns, which is why its boundary cases come from outside.

## Two questions about any term

[Chapter 09](09_what-a-pattern-is-for_3xzc.md) graded names on two independent properties and refused to put them on one line — a name can compress well and constrain nothing, and Facade is the case that proves it. The same discipline is needed here, because two different things are being asked and they come apart.

**Does the term pick out something in the code?** Something you could open the file and confirm or deny.

**Does the term carry a verdict?** Something you would be agreeing with by using it.

Four combinations, and all four are occupied:

```text
                    no verdict              carries a verdict
 -----------------  ----------------------  --------------------
 names a shape      Decorator               anemic domain model
 you can inspect    Transaction Script      SQL injection

 names no shape     "interesting approach"  code smell
 nothing to check   "a lot of work in this" anti-pattern
                                            "not clean"
```

**The bottom-left is easy to miss, because the words in it are not doing a technical job.** *Interesting approach.* *A lot of work has clearly gone into this.* They name no shape and pass no verdict, and that is their function rather than their failure — they are what gets said when a response is required and a position is not.

Recognizing the cell is worth something, because of what a word from it tells you: **no design feedback was given.** Rewriting something because a senior reviewer called it interesting is acting on a statement that was never about the code. The check is the same one used everywhere else in this chapter — if you accept the word, what have you agreed is true? Here the answer is nothing, and that is the finding rather than a gap in the grid.

**The top-right cell is this chapter's subject.** A term there names a shape *and* convicts it, which is the combination that does damage inside pattern vocabulary: you can check the shape, so the term looks like a description, and the verdict rides along unexamined.

The bottom-right is a different failure, and reaching it means leaving the territory Part III has been about. Those terms name no shape, so there is nothing to open the file and check. The chapter deals with them at the end of the demonstration, where the crossing is marked.

Two tests follow from the two questions, and they are worth keeping separate.

**For the verdict.** Apply the term to your own code, then say the code is fine as it stands, and see whether the result means anything. *"This is a Transaction Script, and that is the right shape here"* means something. *"This is an anemic domain model, and that is correct here"* does not — *anemic* means sick, so the sentence argues with itself, and the word is unavailable to anyone who disagrees with it.

**For the shape.** Ask what you would be agreeing is true about the code if you accepted the word. For *Decorator*, that is answerable: something wraps something else with the same interface. For *anemic*, it is answerable: behaviour is not on the entities. For *smell*, there is no answer, which is the whole of the bottom-right cell's problem.

This grading is the book's own, and the axes are not standard vocabulary.

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

> It is a Transaction Script over a table gateway. Rules checkable from one value are methods on the type, the whole-invoice rule is in the operation, and the uniqueness rule is a database constraint.

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

**The verdict travels and the condition does not.** *Incurring the costs of a domain model without the benefits* is nine words carrying a condition; *anemic* is one word carrying the conclusion. [Chapter 14](14_principle-loses-scope_b86v.md) is about why the second outlives the first in transmission. This chapter's interest is narrower and starts where that leaves off: the word that survived **convicts**, so a reply has to reject the vocabulary before it can reach the design.

### The third option the binary cannot see

The term offers two positions: behaviour on the objects, or behaviour nowhere. The invoice above is in neither, and the reason it looks like the second is that the term has no name for the third.

**Behaviour is not absent, it is placed** — and what decides the placement is **what the rule must see**: how much data you have to be looking at before you can tell whether a business rule holds. This is the author's formulation, developed while building FlowCore, and it is not standard vocabulary.

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

The first two are preferences. The third is not: a rule about rows you have not read cannot be enforced by code that has not read them, and [chapter 05](05_time_mdbn.md) works through why the check-then-write version races. So the placement is a fact about what each layer can see rather than a doctrine anyone adopted.

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

[Chapter 04](04_structure_agjy.md) reaches the same place from the structural side, where a `completed_at is null` gate makes the lower layer the more capable one and inverts layering doctrine. Here the point is narrower: a term that cannot see the third option will misclassify every design that uses it.

### Off the map: when the word names nothing at all

This is the bottom-right cell, and reaching it means leaving pattern territory. *Decorator* and *code smell* are not two grades of the same thing; on the grid above they sit diagonally opposite, and the difference matters more than the similarity.

Fowler's definition, crediting Kent Beck with the coinage:

> A code smell is a surface indication that usually corresponds to a deeper problem in the system.

**A surface indication is a hunch, described accurately.** Elsewhere in the same piece: smells "don't *always* indicate a problem", and they "aren't inherently bad on their own — they are often an indicator of a problem rather than the problem themselves." The definition is built to be arguable, and it is right about what it is defining.

What the definition does not say, and what the word will not carry, is **whose state it reports**. *This smells* says that something in the file tripped an experienced reader's pattern-matching before they could say what. That is real evidence and worth having — compressed experience is why senior reviewers are worth their salary. But it is evidence about the reader, not a property of the file, and no amount of it can be checked by opening the file.

The tell is that the book's own classification test has nothing to grip. Run [chapter 01](01_the-five-kinds_cjx4.md)'s five questions on *this smells* and it will not place: it is not a Law, a Force, a Principle, an Idiom, or a Style, because it is not a claim about software at all. **If the test cannot take it, you were not handed a design claim.**

So the practical difference is not whether the word gets used. It is whether it is marked as what it is:

> This code has smells, it should be rewritten from scratch.

> This part has code smells, but I can't work out what would go wrong. Can you walk me through why you chose this shape?

The first goes from hunch to conclusion in one step with nothing checkable in between, so the only moves available are deference and refusal, and seniority decides which. The second declares its own status — *I can't work out what would go wrong* — which keeps the hunch labelled, and then converts it into a request for the reasoning. That second question is the one [chapter 02](02_forces_f4m5.md) says should have been asked anyway: which Forces produced this shape.

**A no-shape term is admissible when it is stated as the speaker's state and turned into a question.** Unmarked, it is a verdict with no subject, and there is no design discussion available until somebody supplies the missing shape.

One consequence worth stating, because it inverts the ordering the rest of this chapter implies. Measured by *can you dissent*, the top-right is worse: *anemic* forbids the sentence that disagrees with it and *smell* does not. Measured by *is there anything here to check*, the bottom-right is worse: with *anemic* you can at least open the file, establish that behaviour is off the entities, and argue about whether that is a defect. With *smell* there is nothing to establish. Two axes give two orderings, and neither is the ordering.

---

## Why the claim holds

A word does two jobs at once: it picks out a thing, and it comes with a stance. Most technical vocabulary keeps the second job near zero. *Hash table*, *mutex*, *idempotent*, *Transaction Script* — each names something and asserts nothing about whether you should want it.

A verdict noun bundles them, and the bundling is what makes it hard to answer. To disagree you first have to refuse the word, and refusing a word looks like evasion. **The cost of the term is borne by whoever is right and did not pick the vocabulary.**

Two properties follow, and they are why this is worth a chapter rather than a complaint.

**It is not a claim, so it never has to be defended.** [Chapter 09](09_what-a-pattern-is-for_3xzc.md)'s point is that names sit outside the five kinds — they are not true or false. A verdict noun exploits that: it does the work of a claim while keeping a name's exemption. Nobody has to state the condition, because on the surface nothing has been asserted.

**It compresses well, which is why it spreads.** Run [chapter 09](09_what-a-pattern-is-for_3xzc.md)'s first test on it and *anemic domain model* passes easily — three words standing in for a paragraph. It is a good name by that measure. That is the uncomfortable part: the terms that travel furthest are the ones that compress best, and compressing well is what got this one into every code review it appears in ([Ch. 14](14_principle-loses-scope_b86v.md)).

---

## Where the claim doesn't apply

### When the verdict is warranted, because the term names a Law

Some loaded terms are loaded correctly, and the test is whether the condition can fail.

**A verdict noun naming a Law violation.** *SQL injection* — building a query by pasting user input into the text of it, so that input containing a quote can close the string and start a statement of its own. The judgment is in the name: *injection* is something done to you. And it is warranted, because there is no configuration of Forces that makes it right. Not on an internal tool, not on an admin page nobody outside can reach, not at any size of team or any latency budget. The condition attached to the verdict is *always*, so compressing it away costs nothing. *Data race* and *buffer overflow* work the same way.

**A verdict noun naming a Principle violation.** *Premature optimization* — where the judgment is in the first word. [Chapter 01](01_the-five-kinds_cjx4.md) classifies the slogan it comes from as a Principle routinely quoted with its conditions removed; here the interest is the noun phrase, which asserts that the timing question is settled.

Whether an optimization is premature is a latency-budget question, and [chapter 02](02_forces_f4m5.md) works that budget across four orders of magnitude — a page render with 200 milliseconds to spend, against an order matcher with 200 microseconds. Hand-tuning a loop on the first day is waste in the first case and is the entire job in the second.

Same work, same point in the schedule, opposite verdicts. So the term does not describe the code — it announces a conclusion about a Force it never asked anyone to measure, and somebody who disagrees has to reject the word before they can say which case they are in.

That gives the claim's boundary a form the book already has: **a verdict noun is legitimate when it names a Law violation, and dangerous when it names a Principle violation.** A Law has no conditions that can fail ([Ch. 01](01_the-five-kinds_cjx4.md)), so a term naming one loses nothing by compressing. A Principle is conditional by definition, so a term naming its violation drops exactly the part that mattered.

*Anemic domain model* fails on the same grounds as *premature optimization*: its condition — you already paid for a domain model — is a Force question, and the answer varies by project.

### Refusing all judgment-laden vocabulary is its own over-correction

The reading to avoid is that technical language should be neutral. It should not, always. Some code is bad, some designs are mistakes, and a vocabulary with no way to say so is worse than one that occasionally says so wrongly.

*Never use a loaded term* is a slogan of the same kind as the ones this chapter is about — a compressed rule with its conditions removed. The working version is narrower: **when you use a term that convicts, say the condition out loud in the same breath**, because the term will not carry it for you. *This is anemic in Fowler's sense — you are paying for the mapping layer and getting nothing back* is a sentence somebody can answer. *This is anemic* is not.

### A term's cell is not fixed, so the tests have to be re-run

The grading above describes words as they are used now, by the people around you. It is not a property the word carries permanently, and the clearest evidence is a term that has moved in both directions inside fifteen years.

*Monolith* began in the left column. A single deployable unit — that is all it meant, and *"it is a monolith, and that is the right shape here"* was an unremarkable sentence. Through the middle of the 2010s it crossed to the right: the thing you were migrating away from, the answer to what went wrong, and saying your system was a monolith conceded a point before you had made one. Then *modular monolith* arrived and pulled it partway back, and the neutral sentence is sayable again in some rooms and not in others.

Note which way it moved. It stayed on the top row the whole time — *monolith* always named a shape you could go and check, and the shape never changed. What moved is what a listener assumes you have agreed to by using the word.

Two consequences. **The tests measure a term in a community at a time**, so running them once and remembering the answer will eventually be wrong. And **a word can sit in different cells in two adjacent rooms** — which is not a flaw in the tests, it is the thing they measure, and it is why the answer has to come from the people you are talking to rather than from a glossary.

---

## What the claim costs

**Auditing vocabulary is a way to avoid answering.** "That term smuggles a verdict" can be true and can also be a refusal to discuss the code. If someone calls a design anemic and the design *is* an object graph with an ORM and no behaviour, they are right, and the etymology of their word is not the topic.

**Which cell a term sits in is genuinely contested for some of them.** *Code smell* is placed as carrying a mild verdict here, because its author defined it as an indication rather than a finding. Someone could argue the hygiene metaphor overwhelms that definition in every real use, which would move it toward the strength of *anemic* without moving it off the bottom row — and that is a reasonable position rather than a misreading.

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

- **"That is an anti-pattern."** Which one, and what did its author say the conditions were? *Anti-pattern* names no shape of its own — it is a verdict with a filing category attached.
- **"This isn't clean."** Against what definition, and what happens if it stays?
- **A design defended by renaming it.** If *Transaction Script* and *anemic domain model* describe the same file, the argument is about the word and the design was never in question.
- **Agreement reached suspiciously fast after a term is introduced.** Nobody wants to be the person defending sick code, which is what the word is for.

Two questions do the work, and they are the two axes.

**If I accept this word, what have I agreed is true about the code?** If there is an answer, you can go and check it, and the disagreement has a subject. If there is no answer, nothing has been said about the code yet and the discussion has not started.

**What would have to be true for this to be fine, and does the term let me say it?** If you can state the condition, you have a claim and can argue with it. If the word forbids the sentence, you have been handed a conclusion.

---

**Next:** [chapter 14](14_principle-loses-scope_b86v.md) opens Part IV with the mechanism behind this one — why the fragment that survives repetition is always the part telling you what to do, and never the part telling you when.
