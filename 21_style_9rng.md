# Style: The Level Where Being Right Doesn't Matter

## The claim

**A Style discussion has no fact that would settle it, so it ends only when a person who can enforce a style decides to act — and everything before that produces nothing.**

[Chapter 01](01_the-five-kinds_cjx4.md) puts Style at the bottom of the ladder and gives the test that puts things there: the compiler or the runtime acts on an Idiom, and ignores a Style.

---

## The demonstration

### Nothing in the program depends on it

Here is a function that totals the line items on an invoice, written the way `gofmt` writes it. Go's `range` yields an index and a value; `_` discards the index.

```go
func Total(amounts []int) int {
	total := 0
	for _, amount := range amounts {
		total += amount
	}
	return total
}
```

And here it is with the braces and spacing arranged by hand instead:

```go
func Total( amounts []int ) int {
    total := 0
    for _, amount := range amounts { total += amount }
    return total
}
```

Both print `1745` on the same input. That is the whole of what the machine has to say about the difference.

### So the choice belongs to whoever makes it first

Run `gofmt` over the second version and it reports the file, then rewrites it:

```text
$ gofmt -l alt/untidy.go
alt/untidy.go

$ gofmt -d alt/untidy.go
-func Total( amounts []int ) int {
-    total := 0
-    for _, amount := range amounts { total += amount }
-    return total
+func Total(amounts []int) int {
+	total := 0
+	for _, amount := range amounts {
+		total += amount
+	}
+	return total
 }
```

Nobody on a Go team argues about this, and the reason is not that Go programmers are more reasonable. The argument was taken away from them before they arrived.

Rob Pike, looking back at Go's first fourteen years, gives the history and is explicit about who did it: before Robert Griesemer wrote `gofmt` — *"which, by the way, he insisted on doing from the very beginning"* — automated formatters were poor and therefore mostly unused. Pike's assessment of the trade is the claim of this chapter, made by someone who paid for it: **"The time saved by not arguing over spaces and newlines is worth all the time spent defining a standard format and writing this rather difficult piece of code to automate it."** He adds that today essentially every language worth using has a standard formatter.

That is one person, with the standing to make it stick, acting early. The result was not that Go settled the brace question correctly — there is no correct answer — but that Go stopped paying for it. Python's Black and JavaScript's Prettier are the same move made later.

### The same question, with nothing to end it

Now change the names instead of the layout:

```go
func Total(a []int) int {
	t := 0
	for _, v := range a {
		t += v
	}
	return t
}
```

Same output. And `gofmt` reports nothing, because a formatter has no opinion about whether the parameter is called `amounts` or `a`.

**That silence is the reason naming arguments outlive formatting arguments.** Which word you choose is arbitrary in the way any word is arbitrary — Italian and Mongolian give the same table entirely different names and both work — so there is nothing for a tool to compute. The enforcement has to come from a person, repeatedly, for as long as people are still writing code. There is a floor under this, and the boundary section works out where it is.
Two decisions in this book's own history show what that costs. FlowCore deviates from Go's short-name convention, on the grounds that abbreviations like `def` and `mgr` must be decoded rather than read, and that the decoding **does not get cheaper with familiarity** the way the convention assumes. This book deviates from the same convention for a different reason: its reader meets a sample once and never returns to it, so a truncated domain noun is one more thing to decode in a language most of them do not write.

Neither could be automated, so both were written down instead. Which is this chapter's oddity in one line: **where being right about the choice is unavailable, but recording the reasons for it still matters.** A short name with a recorded reason behind it and a short name with nothing behind it are identical on the screen, and the second is indistinguishable from not having noticed.

---

## Why the claim holds

Every other kind in this book has something that ends an argument about it.

A Law has a mechanical consequence: violate its preconditions and the program is wrong, and you can go and be wrong ([Ch. 03](03_grading-a-law_q5c6.md)). A Principle has a Force with a value, and the value can be looked up — the row count, the number of writers ([Ch. 02](02_forces_f4m5.md)). An Idiom has a compiler or a runtime that acts on the choice, so there is a machine you can ask ([Ch. 01](01_the-five-kinds_cjx4.md)), and [chapter 20](20_idioms_7nkn.md) works out what that machine's answer costs.

**Style is the only kind where no such thing exists.** Not that the evidence is hard to gather or expensive to measure — there is no evidence, because there is nothing for evidence to be about. Two spellings of the same program are the same program.

An argument with no possible evidence has no terminating condition. It does not converge, because converging requires something to converge on; it stops when somebody gets bored, or leaves, or outranks the others. Joel Spolsky's description of the second stage of a programmer's development is the same observation from 2005, and it is worth more than a complaint would be, because he spends the rest of that essay arguing that some naming conventions are worth a great deal:

> you spend the next day writing up coding conventions for your team and the next six days arguing about the One True Brace Style and the next three weeks rewriting old code to conform to the One True Brace Style until a manager catches you and screams at you for wasting time on something that can never make money

Six days and three weeks, and the codebase at the end differs from the codebase at the start in no respect any user or any machine can detect.

**So "produces nothing" is meant literally rather than as a complaint about waste.** A Force argument that runs for six days may still be worth having: somebody may go and measure, and then everyone knows a thing about the system that nobody knew on Monday. A Style argument cannot end that way. There is no measurement available, so the six days cannot deposit anything, whatever the participants conclude.

Which is why the only variable is how early somebody ends it, and why the ending is a decision rather than a conclusion.

---

## Where the claim doesn't apply

### The option that was never on the menu

The claim assumes you have two spellings of one thing. Sometimes you have one spelling of two things, and it looks identical on the page.

A trailing comma in a Python list is the model Style question — invisible, arguable, and settled in most codebases by whichever formatter is installed:

```python
regions = ["us-east", "eu-west",]
regions = ["us-east", "eu-west"]
```

Those build the same list. Now the same comma, one construction over, passing a single parameter to a database query:

```python
cursor.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
cursor.execute("SELECT status FROM orders WHERE id = ?", (order_id))
```

```text
with the comma   -> ('open',)
without          -> ProgrammingError: parameters are of unsupported type
```

`(order_id,)` is a one-element tuple. `(order_id)` is an integer with brackets around it, because in Python the comma makes a tuple and the parentheses only group. So the second line is not the same query written in a different style; it passes an integer where a sequence was required, and the driver rejects it.

**There were never two options here.** The question presented as a Style question — a comma, a matter of house preference, the same token the formatter had an opinion about two paragraphs ago — and one of the two apparent choices did not exist. No amount of deciding, enforcing, or agreeing would have helped, because the disagreement was with Python rather than with a colleague.

### A name that does not name

The same trap with no machine to catch it. Here is the invoice total again, rewritten by somebody making a point:

```go
func G(p []int) int {
	z := 0
	for _, y := range p {
		z += y
	}
	return z
}
```

It compiles, `go vet` is silent, `gofmt` approves it, and it prints `1745`. Every machine test in this chapter says it is the same program, and it is — so this looks like a Style choice by the definition, but it is not.

The resolution is similar to the tuple's. `Total` and `Sum` are different names for the same function and nothing separates them; that is the Style question and it has no answer. `G` is not a third name for the same function. It names nothing, so it is not an alternative to the others — it is the choice not to name the thing.

And that question has evidence behind it, which is what settles it. Show a colleague `func Total(amounts []int) int` and ask what it returns; they answer. Show them `func G(p []int) int`; they cannot. The experiment has an outcome, so the question can be settled, so by this chapter's own account it was never Style.

Which gives the rule covering both cases: **before treating something as Style, check that both options do the job you are choosing between two ways of doing.** For the tuple that job is passing a sequence of parameters, and the driver says which option fails. For the name it is saying what the thing is, and a reader says. Where one option does not do the job there is a fact, the discussion can end on it, and the time is not wasted.

[Chapter 20](20_idioms_7nkn.md) gives the systematic version of the same trap: the line between Style and Idiom is drawn in a different place by each language, so a decision that is arbitrary in one is structural in another.

---

## What the claim costs

**It licenses deciding without thinking, and that is nearly the point.** The claim says the content of a Style decision does not matter, which is true and which reads as permission to stop caring. The part that does matter is that the decision is made and then held to, and a leader who takes the first half without the second has produced a convention nobody follows and an argument that resumes next month.

**Enforcing late costs more than enforcing early, and the difference is not linear.** Applying a formatter to an established codebase rewrites files nobody edited, so a `git blame` on any of those lines now names the person who ran the formatter. That is a real loss of history, and it is the reason the claim is about timing at all — the same decision is cheap on the first day and expensive on the thousandth.

**"It's only style" becomes a way to close a real question.** The boundary above is the reason: a disagreement that looks like Style sometimes is not, and the phrase that dismisses it is available before anyone has checked. The cost of being wrong here is asymmetric — dismissing a real question as Style ships a defect, and treating a Style question seriously wastes an afternoon.

---

## How to recognize the failure

**In a codebase:**

- **A formatter in the repository that CI does not run.** The decision was made and not enforced, which leaves the argument open while looking closed.
- **A style guide longer than the code it governs**, or one with sections nobody can point at an example of. It was written to end an argument and became a second argument.
- **A commit that reformats a file it also changes.** The real change is now unreviewable, and the history of every line in it points at this commit.
- **Two conventions in one repository with a date between them.** Somebody decided, somebody else decided differently later, and neither decision was applied backwards.

**In a conversation:**

- **A style argument in its second week.** The content does not matter and the duration is the only cost, so the answer is not to argue better but to ask who decides and get them to.
- **"Let's discuss it at the next team meeting."** For a Force question that is prudent; for a Style question it is four more people spending an hour on something with no answer in it.
- **"It's only style."** Sometimes true. Check that both versions produce the same program before agreeing.
- **A deviation from house convention with no note attached.** Nothing distinguishes a decision from an oversight, and the reader will assume whichever costs them less.

The question that does the work: **do these two versions produce the same program?**

If they do, nothing further can be learned by discussing it, and the only useful act is for somebody to choose. If they do not, this was never a Style question, and the time spent settling it will produce something.

---

## Sources

Rob Pike, *What We Got Right, What We Got Wrong*, closing talk at GopherConAU, Sydney, 10 November 2023, published 4 January 2024. <https://commandcenter.blogspot.com/2024/01/what-we-got-right-what-we-got-wrong.html>

Joel Spolsky, *Making Wrong Code Look Wrong*, Joel on Software, 11 May 2005. <https://www.joelonsoftware.com/2005/05/11/making-wrong-code-look-wrong/>

FlowCore decision log, decision 18, "Full-word identifiers over Go's short-name convention". <https://github.com/ilke-akdeniz/flowcore>

---

**Next:** [chapter 22](22_never-written-down_at4r.md) closes the book by putting the five kinds to work on the thing you actually meet — a blog post, a review comment, a colleague's strong opinion, and code a machine wrote that states no decisions at all.
