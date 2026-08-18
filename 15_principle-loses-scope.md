# How a Principle Loses Its Scope

## The claim

**A compressed principle carries its scope only when it names the situation it applies to. Where it doesn't, the reader has to reconstruct that scope from the surrounding context. Without that context, only the widest reading is available.**

**A word on *scope*, because the book has used a different one for this.** Earlier chapters say a Principle has **conditions** — what must be true for it to hold, which is always some fact about your Forces. Chapter 05's information-hiding Principle has a sharp one: *you do not control your callers.*

**Scope is the same boundary seen from the other side: the situations the advice reaches.** State the conditions and you have given the scope; name the situation and you have given it too. This chapter says *scope* rather than *conditions* because it tracks what the wording carries rather than what the advice requires — and a principle can carry that boundary either way. *Don't store money in a float* names a situation and states no condition, and it passes the test below regardless.

Part IV is three case studies, and this chapter is the mechanism they share, stated once.

---

## The demonstration

### The form Pike borrowed, and what it was for

In November 2015 Rob Pike gave a talk at Gopherfest that produced the Go proverbs. He opens by naming his source: a book about the Japanese board game go, translated into English about fifty years earlier, called *Go Proverbs Illustrated*. The author is Kensaku Segoe and the slide behind Pike shows the book's cover.

He reads out two of Segoe's proverbs, and then says this about whether the audience is following:

> don't worry whether you understand that or not

That is the form, described by the person borrowing it. **A proverb of this kind is not self-contained and was never meant to be.** Segoe's foreword says as much: the phrases compress measures that apply across the enormous variety of positions on the board, and a single one of them may be worth ten games of teaching. The phrase indexes the teaching. It does not replace it.

Pike also says what a proverb buys a player who *does* have the context: seeing a shape on the board tells you what will happen if you play into it, *and it may or may not be a good thing.*

That last clause is the point. The proverb tells you the consequence; whether you want it is a judgement it declines to make. Board proverbs are predictive. Several of Pike's are imperative — *don't communicate by sharing memory*, *clear is better than clever* — and that change of mood is the first thing that crossed over unremarked.

### What the first proverb means, according to Pike

> Don't communicate by sharing memory, share memory by communicating.

Pike introduces it as something that already exists — *there is already one proverb you all know* — so he is glossing rather than coining, which makes the gloss more interesting rather than less: this is the language's designer saying what the sentence is taken to mean. He spends about forty seconds on what it takes to read that sentence, and the scope is narrow. You pass the address of a data structure over a channel. And then the part that does the work:

> when you send that object over a channel if you don't keep the pointer then you don't have access to it anymore

So the proverb is about **transferring ownership**. One goroutine has the thing, hands it off, and no longer has it. That handoff is what makes the concurrency safe. He is explicit that reading the sentence is not trivial — *there's actually a lot behind there*.

Two items later comes a separate proverb, *channels orchestrate, mutexes serialize*, with its own explanation and its own scope. It answers a different question — which primitive for which job — and in explaining it Pike says a mutex is often very important and sometimes exactly what you want.

### What the proverb says when nobody is there to gloss it

Near the end of the talk, Pike guesses what will become of the idea of "Go Proverbs":

> maybe this will turn into something that the community maintains on the wiki or maybe when you leave tonight this will be the end of the idea I don't know

It became the wiki. There is now a canonical page of the nineteen proverbs, credited to that talk, carrying the nineteen sentences and nothing else. Not the forty seconds on what the first one means. Not *don't worry whether you understand that or not*. And not this, from two minutes earlier:

> I don't think of these things that you guys need to know I think you know them already but think about them as ideas that you might use to explain to somebody

**The proverbs were built for people who already hold the context, as tools for explaining it to people who do not.** The speaker carries the scope; the proverb is the handle. Detached, the handle travels alone.

### A reader supplying the missing scope

In late 2023 someone posted a genuine question to the Go subreddit. They had found a parallel map in a real library where each goroutine writes its result straight into a shared slice, with no channel anywhere, and asked whether that violates the proverb.

The shape in question is this:

```go
func ParallelMap(input []int, transform func(int) int) []int {
	results := make([]int, len(input))

	var waitGroup sync.WaitGroup
	for index, value := range input {
		waitGroup.Add(1)
		go func(index, value int) {
			defer waitGroup.Done()
			results[index] = transform(value)
		}(index, value)
	}
	waitGroup.Wait()

	return results
}
```

Every goroutine writes into the same backing array. Nothing is sent and nothing is locked. Run it under Go's race detector across a thousand elements and it reports nothing, because each goroutine writes one index and reads none — there is no unsynchronized access to any single location, which is the only thing correctness requires here.

The code is fine. What is interesting is the reading that made it look wrong, which the poster states themselves, twice:

> I thought the proverb meant something more literal, as in the goroutines should not ever be allowed to share memory

> I thought the proverb related to not even having the possibility of sharing memory, not that you shouldn't intentionally share memory

**There is the mechanism, self-reported.** And it is more specific than channel over-use. The proverb never says what counts as sharing memory. Does writing to your own index in a shared slice count? Pike's forty seconds answer no — the proverb is about handing off a pointer and losing access to it. The eleven words alone do not answer it, and the reader resolved it outward, to any memory two goroutines can both reach.

The same post asks a second question worth as much: is the proverb about maintainability and safety, or is there some other reason for it? **They cannot tell what kind of claim the proverb is.** That is chapter 02's subject arriving in the wild. Sorting the proverb into one of the five kinds is what tells you how much authority it has — a Law binds regardless, a Principle holds only under certain Forces, an Idiom is local — and the compressed form gives you nothing to sort it with.

### The same failure, twice more, admitted by the same person

Eight years after the proverbs talk, Pike gave a closing talk at GopherConAU looking back on fourteen years of Go. Two passages in it are this chapter's mechanism, and he is the one naming it.

The first is about somebody else's advice. Around 2002 Google had effectively banned threads, and engineers doing the banning cited John Ousterhout, who had written that threads were bad. Pike's diagnosis is that Ousterhout made two mistakes — that he was **generalizing beyond the domain he was interested in**, and that his complaint was really about clumsy low-level packages like pthreads rather than about the underlying idea. Then, in one line: it is a mistake common to engineers everywhere to confuse the solution with the problem.

Read that as an instance rather than as an opinion about Ousterhout. The advice had a situation — pthreads, in a particular kind of program. The situation did not travel. What arrived at Google was *threads are bad*, applied to everything, and it held for years with a name attached to it.

The second passage is about his own project, and it is the more useful one because the source is admitting it.

On concurrency, he says the use cases the team had in mind were mostly server software, and that they **should have explained up front** that this was what the feature brought to the table — that programmers who tried it elsewhere struggled to see how it helped them, and that the lack of guidance was theirs. On the confusion between concurrency and parallelism, he is blunter: people parallelised with goroutines expecting speed, were baffled by the slowdown, and the team did a terrible job explaining it. He adds that it probably drove some of them away.

**That is the author of a piece of advice saying the situation was never named, and stating what it cost.** Not a reader's complaint, not an inference from a codebase — the source, on the record, eight years later.

It also produced the third repair in this chapter. He gave an entire talk in 2012, *Concurrency is not Parallelism*, whose job was to supply the missing distinction, and says of it that it should have happened earlier.

**One thing this is not.** It is not more evidence about the proverbs. *Don't communicate by sharing memory* and *concurrency support in the language* are different artifacts, and nothing here says the proverb caused what Pike is describing. **But the mechanism is the same, and that is the whole of it: a principle arrives without its scope, the reader takes the widest reading available, and the damage follows from the reading rather than from the advice.** Ousterhout was not wrong about pthreads and the Go team were not wrong about concurrency — in both cases what did the harm was a reading neither of them wrote.

### The scope gets rebuilt by hand, more than once

The Go project's own wiki has a page for this, and its first line is the proverb. Immediately after comes the qualification — the language also ships traditional locks in `sync` — and then this:

> A common Go newbie mistake is to over-use channels and goroutines just because it's possible

It tells you not to be afraid of a mutex, and gives a table of what each tool is for. Channels: passing ownership of data, distributing units of work, communicating async results. Mutexes: caches, state.

**That table is Pike's forty seconds, reconstructed.** *Passing ownership of data* is what he said the proverb meant. The Go project needed a wiki page and a comparison table to restore a scope Pike had given in one sentence on stage — because the sentence did not travel and the proverb did.

Then it happens a third time, in the Reddit thread itself. One commenter, unprompted, says channels are about ownership, and that where ownership is not clear — a shared cache is their example — a mutex may be the better tool. Another states Pike's condition exactly, including what breaks without it: send a pointer over a channel while still holding it yourself and the race is back.

And one reply reaches for a **meta-proverb** to bound the proverb, along the lines that a good developer follows the rules and a great one knows when to break them. That improvisation has an institutional form elsewhere. Sensei's Library, a wiki for go the board game rather than the language, sorts its proverbs into scope categories, italicizes the ones amateurs devised so you can see which have centuries behind them, and keeps a *Meta Proverbs* group whose entries include *don't follow proverbs blindly*. Its introduction says the proverbs apply often — and then that one must always evaluate whether they apply in a particular situation, and that sometimes they are contradictory.

None of that apparatus in the game wiki was designed in, and the oldest collection did without it in a different way. The Tang-dynasty *Wei Qi Shi Jue* is ten rules of four Chinese characters each, and most of them spend part of that budget on the situation they apply to — *when in danger, sacrifice*; *against strong positions, play safely*; *take care of oneself when attacking*. The scope is inside the principle rather than around the collection.

Which is the more useful way to put the whole progression. **Scope lives either inside the principle or in an apparatus around the collection it belongs to, and where it is in neither, the reader reconstructs it — or fails to.** Segoe's book puts it in worked game diagrams beside each phrase. The game wiki puts it in categories, provenance marks, and a warning to evaluate before applying. The list of nineteen on the go language wiki has none of the three.

### The same list contains proverbs this cannot happen to

Pike's nineteen are not uniform, and the difference is visible in the grammar.

```text
 scope in the sentence            scope not in the sentence
 ------------------------------   ------------------------------
 Syscall must always be guarded   Don't communicate by sharing
   with build tags                  memory
 Cgo must always be guarded       Clear is better than clever
   with build tags                Errors are values
 With the unsafe package there    Don't panic
   are no guarantees
 Reflection is never clear
```

The left column names a package. *Syscall* is a specific import, and a proverb whose subject is that import **has nowhere to drift to** — you cannot resolve *syscall* outward, because the word fixes the domain. The right column takes a whole way of working as its subject, and the scope is wherever the reader puts it.

This is a structural claim rather than an empirical one. It says the left column cannot lose its scope, not that nobody ever misapplies those proverbs. But it is the strongest control available here: same author, same talk, same form, same afternoon, and the only variable is whether the proverb names the situation it applies to. The proverb this chapter followed is in the right column.

So the test gets sharper, and becomes something you can check rather than hope for. **Look at the grammatical subject.** If it names a package, a file format, a specific operation, the situation arrived with the proverb. If it names a style of programming, it did not, and reconstructing it is your job.

### Past proverbs, to principles nobody wrote to be memorable

Everything above is a proverb, and a proverb is a special case — short and poetic on purpose, because Pike said those were his criteria. So the obvious objection is that the finding belongs to the genre rather than to advice in general.

It does not, and the test settles it without leaving the page. Asking whether a principle names the situation it applies to is a question about its wording. It needs no history, no author to interview, and no claim about what anyone did with it.

Run it on advice nobody compressed for memorability:

```text
 principle                      situation named   what you must ask
 ----------------------------   ---------------   ------------------
 single responsibility          —                 one responsibility of
                                                  what? a method, a
                                                  class, a service?
 don't repeat yourself          —                 repeat what, and is
                                                  twice a repetition?
 depend on abstractions         —                 which dependencies?
 prefer composition over        —                 prefer how strongly?
   inheritance
 don't store money in a float   a money value     —
 guard cgo with build tags      a file using cgo  —
```

The top four are not proverbs. Nobody wrote the single responsibility principle to scan, and it does not. They fail the test anyway, and for the reason the Go proverb did: none of them says which situation it is about, so before you can apply one you have to answer a question it never asked. Two engineers who both accept the single responsibility principle can disagree about every class in the codebase and neither is misreading it — they answered *of what?* differently, and the principle does not arbitrate.

The bottom two are not proverbs either, and they pass. *Money* and *cgo* name situations. There is nowhere to resolve them outward to.

**So the property belongs to the wording, not to the genre.** Being built for memorability makes it more likely that the situation gets left out, because a situation is the longest part and the first to go. It is not what causes the omission. Chapters 16, 17, and 18 are three principles from the second column, each traced to what its wide reading produced.

**On what these sources are worth**, because they are not equal. Pike's talk is primary. The Go project's wiki page is an official artifact and the strongest evidence that the misreading was real enough to be worth correcting — though note that it attributes the over-use to enthusiasm rather than to the proverb, and this chapter does not claim the proverb caused it. The Reddit thread is community anecdote: one instance, dated, and useful only because the over-application is self-reported rather than attributed by somebody else. It shows the confusion exists and what shape it takes. It establishes nothing about how often, and nothing here claims otherwise.

---

## Why the claim holds

Compression fixes the wording. It does not fix the scope.

*Sharing memory* is two words in Pike's sentence and about a paragraph in his explanation of it. The sentence survives repetition; the paragraph does not. So what circulates is a term whose boundary was set somewhere the reader cannot see — and the reader still has to act, so they resolve it. With no context to narrow it, the widest reading is the only one available. That is why the error has a direction. Nobody reads a proverb too narrowly.

**The mechanism does not care what kind of vocabulary it works on.** Chapter 14's case is not a proverb at all. *Anemic domain model* is a verdict noun, and its author gave it a clear antecedent — you already paid for a domain model and are collecting none of the return. That antecedent is absent from every use of the term, and what circulates is the conviction.

Different artifact, different missing piece — an antecedent there, a situation here — and the same selection running on both. **What survives is the part that tells you what to do. What goes is the part that tells you whether to do it.**

Which explains why neither failure runs the other way. Nobody under-applies a principle they received without its scope, because the fragment that would have narrowed them is precisely the fragment that was dropped.

**The form causes this, and the form was chosen deliberately.** Pike sets out his criteria near the end: really short, kind of poetic, a little saying, something memorable. Those are constraints on shape, indifferent to whether the surviving proverb is complete. A statement of scope is longer, does not scan, and is useless to anyone not in the situation it names. It is the first thing that will not fit.

He also says of the whole list that the entries might be contradictory, and that sometimes one engineering decision is right and sometimes its exact opposite is. **That is a scope statement covering the entire collection, made once, at the end of a talk, and it is not on the page that carries the proverbs.**

Which gives the test worth keeping: **does this advice say how wide it is?**

- *Use dependency injection.* No scope. You cannot tell whether your situation is one it fits.
- *Channels are for passing ownership of data; mutexes are for caches and state.* States its own scope — which is why the Go project wrote that, and not another proverb.

---

## Where the claim doesn't apply

### Advice with no scope to lose

Some advice is unconditional, and then nothing is missing from the compressed form.

*Gofmt's style is no one's favorite, yet gofmt is everyone's favorite* is on the same list of nineteen, and it became a norm — mandatory automatic formatting, no configuration — without incident. There is no situation in which one consistent format is wrong, so a reader who receives only the proverb has received all of it. Chapter 14 reached this boundary from the other side: a compressed statement is safe exactly when its condition is *always*. Chapter 22 is the general case.

### A named situation is a proxy, and proxies fit badly

The test above asks whether a principle names the situation it applies to. It does not ask whether that situation is the right one, and those come apart.

A named situation is a **proxy** for the conditions — cheaper to state, easier to recognize, and chosen for both of those rather than for fit. Pike's own list shows the seam. Two of the nineteen are the same instruction with a different noun in front:

```text
 Syscall must always be guarded with build tags
 Cgo must always be guarded with build tags
```

Introducing the second, he says it is for exactly the same reason as the first. One condition — the code is platform-specific — and two proverbs, because he was naming situations and the condition covered more than one of them.

**So the proxy can be narrower than the conditions**, and then the advice under-applies. A third platform-specific thing that is neither syscall nor cgo has no proverb, and somebody who follows both faithfully still ships it unguarded, having misread nothing.

It can also be wider. *Don't store money in a float* names money; the condition is that an exact decimal representation is authoritative and errors accumulate. A rough total on a dashboard, never summed and never reconciled, is inside the named situation and outside the condition. That direction is the milder failure, because obeying the proverb there costs almost nothing.

**Which makes the chapter's test weaker than it reads, and worth restating honestly.** Passing it means the principle handed you something checkable, not that it handed you the right extent. With *guard cgo with build tags* you can ask what your case has in common with cgo and get an answer. With *clear is better than clever* there is nothing to compare against, because no situation was named at all.

That is still a real difference, and it is the one the chapter is about. A proxy you can test beats an extent nobody stated.

### The domains are not alike, and it explains the lag

Board go is one rule set, fixed for centuries, with a single objective and a bounded space. Software has domains that share almost nothing, tools that turn over in a decade, and no settled agreement about what counts as better.

So a proverb about the board can accumulate a stable scope, while a proverb about software aims at a target moving faster than any apparatus can follow. That predicts what the two collections actually show: twenty-five years of accretion in one, a flat list in the other. It explains the lag rather than excusing it, and it does not change what a reader should do — if anything it raises the odds that the scope you need has not been written down by anyone.

### The repair sometimes arrives

This chapter ends in repair, which is why it does not claim that a principle stripped of its scope stays that way. The scope was rebuilt three times here: officially, in a wiki page with a table; informally, by strangers answering a question; and by the source himself, in a talk given to supply a distinction he had left out.

Where that does not happen — where the wide reading hardens and nobody writes the page — you get what chapter 23 calls a folk remedy. Chapters 16, 17, and 18 are three cases that travelled further than this one did.

---

## What the claim costs

**Recovering a scope is slow, and usually nobody wrote it down.** Pike's is recoverable because the talk was recorded. For most advice the context is a mailing list that no longer resolves, or a conversation. At that point you are reconstructing rather than reading, which is how a plausible mechanism gets attached to somebody else's words.

**The test rejects nearly everything.** Almost no advice states its own scope, because the scope was compressed out before it reached you. *Does this say how wide it is* discards most of what is true along with what is not. It sorts. It does not accept or reject.

**Noticing is cheap and answers nothing.** Observing that a saying has lost its scope takes no work. Finding what the scope was takes a recorded talk, a wiki page, or an afternoon, and that is the part people skip while keeping the posture.

**Compression is not the enemy, and this reads as though it might be.** A saying that fits in a review comment is how most real knowledge moves between people, and the alternative is everybody re-deriving everything, which is worse and does not happen anyway. The finding is about what to do on receipt.

---

## How to recognize the failure

**In a codebase:**

- **A structure that only makes sense as obedience** — machinery whose justification is a saying rather than a property of this program.
- **A comment citing a rule instead of a reason.** If the line needed the rule written beside it, the rule was not explaining the line.
- **A convention nobody can date.** When nobody can say who decided it or what it was for, the scope is gone and the convention is being maintained rather than used.
- **Code you cannot fault that seems to break the rule anyway.** This is the tell, and it is quieter than an argument. The Reddit poster was not disputing anything — they found working code, could not identify what was wrong with it, and still suspected it violated the proverb, so they went and asked. When a competent reader cannot reconcile a rule with code they have no complaint about, the rule's scope is the thing that is missing, not their judgement.

**In a conversation:**

- **A saying offered as the end of a discussion.** The useful follow-up is not *I disagree* but *how would we apply that here, concretely, and what would it improve?* — which is answerable from the code in front of you, where a dispute about the saying is not.
- **"That's just how it's done here."** Sometimes a real Idiom with reasons behind it (Ch. 21), sometimes a wide reading nobody has revisited. One question separates them.
- **An appeal to who said it.** The credibility is usually genuine and answers a question nobody asked: it suggests the original observation was sound, and says nothing about whether the version that reached you still contains it.
- **Anyone, including this book, saying a practice always applies.**

The question that does the work: **what did the person who said this go on to say next?**

If the source can be reached, go and look. The scope is often still there, in the forty seconds after the sentence, in the talk nobody re-watched.

---

**Next:** chapter 16 is the first of the three cases, where object orientation's advice about where behaviour belongs meets the Direction Rule, and produces dependency graphs that point both ways.
