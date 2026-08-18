# How a Principle Loses Its Scope

## The claim

**A compressed principle does not contain the scope of its own key words. A reader without the author's context has to supply that scope, and the widest reading is the only one available without it.** [claude we later say: "Scope lives either inside the sentence..." so this claim needs an update to remove the inconsistency.]

Part IV is three case studies, and this chapter is the mechanism they share, stated once.

The book has met the result before: a theorem repeated without its quantifier (Ch. 04), a count repeated without its *for at least some uses* (Ch. 13), a diagnosis repeated without the payment that justified it (Ch. 14). Those chapters own the instances. This one follows a single sentence from the person who wrote it to the people who received it, and the whole path is on the record — which is unusual, and is the reason for using this example rather than a better-known one. [claude I suggest removal of this paragraph. I also wnat to warn you that I'm not sure if Pike actuall coined the "don't share..." slogan. He says "we have this sayings" but that doesn't matter as far as I can see, he is in the end one who defines - approves the somewhat "official" meaning of the saying. ]

---

## The demonstration

### The form Pike borrowed, and what it was for

In November 2015 Rob Pike gave a talk at Gopherfest that produced the Go proverbs. He opens by naming his source: a book translated from Japanese about fifty years earlier, called *Go Proverbs Illustrated* — Kensaku Segoe's — and the slide behind him shows it.

He reads out two of Segoe's, about board positions, and then says this about whether the audience is following:

> don't worry whether you understand that or not

That is the form, described by the person borrowing it. **A proverb of this kind is not self-contained and was never meant to be.** Segoe's foreword says as much: the phrases compress measures that apply across the enormous variety of positions on the board, and a single one of them may be worth ten games of teaching. The phrase indexes the teaching. It does not replace it.

Pike also says what a proverb buys a player who *does* have the context: seeing a shape on the board tells you what will happen if you play into it, *and it may or may not be a good thing.*

That last clause is the point. The proverb tells you the consequence; whether you want it is a judgement it declines to make. Board proverbs are predictive. Several of Pike's are imperative — *don't communicate by sharing memory*, *clear is better than clever* — and that change of mood is the first thing that crossed over unremarked.

### What the first proverb means, according to its author

> Don't communicate by sharing memory, share memory by communicating.

Pike spends about forty seconds on what it takes to read that sentence, and the content is narrow. You pass the address of a data structure over a channel. And then the part that does the work:

> when you send that object over a channel if you don't keep the pointer then you don't have access to it anymore

So the proverb is about **transferring ownership**. One goroutine has the thing, hands it off, and no longer has it. That handoff is what makes the concurrency safe. He is explicit that reading the sentence is not trivial — *there's actually a lot behind there*.

Two items later comes a separate proverb, *channels orchestrate, mutexes serialize*, with its own explanation and its own scope. It answers a different question — which primitive for which job — and in explaining it Pike says a mutex is often very important and sometimes exactly what you want.

### What the sentence says when its author is not present

Near the end of the talk, Pike guesses what will become of the idea of "Go Proverbs":

> maybe this will turn into something that the community maintains on the wiki or maybe when you leave tonight this will be the end of the idea I don't know

It became the wiki. There is now a canonical page of the nineteen proverbs, credited to that talk, carrying the nineteen sentences and nothing else. Not the forty seconds on what the first one means. Not *don't worry whether you understand that or not*. And not this, from two minutes earlier:

> I don't think of these things that you guys need to know I think you know them already but think about them as ideas that you might use to explain to somebody

**The proverbs were built for people holding the wider context of the idea so that they can explain it to others.** The speaker carries the scope; the proverb is the handle. Detached, the handle travels alone.

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

**There is the mechanism, self-reported.** And it is more specific than channel over-use. The phrase *sharing memory* has no fixed extent in the sentence containing it. Does writing to your own index in a shared slice count? Pike's forty seconds answer no — the proverb is about handing off a pointer and losing access to it. The eleven words alone do not answer it, and the reader resolved it outward, to any memory two goroutines can both reach.

The same post asks a second question worth as much: is the proverb about maintainability and safety, or is there some other reason for it? **They cannot tell what kind of claim it is.** That is chapter 02's subject arriving in the wild — the compressed form does not say the reason, and placing a claim is prerequisite to knowing what authority to give it. [claude "placing a claim" be clear what do you mean? Place where?]

### The scope gets rebuilt by hand, more than once

The Go project's own wiki has a page for this, and its first line is the proverb. Immediately after comes the qualification — the language also ships traditional locks in `sync` — and then this:

> A common Go newbie mistake is to over-use channels and goroutines just because it's possible

It tells you not to be afraid of a mutex, and gives a table of what each tool is for. Channels: passing ownership of data, distributing units of work, communicating async results. Mutexes: caches, state.

**That table is Pike's forty seconds, reconstructed.** *Passing ownership of data* is what he said the proverb meant. The Go project needed a wiki page and a comparison table to restore a scope its author had given in one sentence on stage — because the sentence did not travel and the proverb did.

Then it happens a third time, in the reddit thread itself. One commenter, unprompted, says channels are about ownership, and that where ownership is not clear — a shared cache is their example — a mutex may be the better tool. Another states Pike's condition exactly, including what breaks without it: send a pointer over a channel while still holding it yourself and the race is back.

And one reply reaches for a **meta-proverb** to bound the proverb, along the lines that a good developer follows the rules and a great one knows when to break them. That improvisation has an institutional form elsewhere. Sensei's Library, a wiki for the go board game - not the langiage, sorts its proverbs into scope categories, italicizes the ones amateurs devised so you can see which have centuries behind them, and keeps a *Meta Proverbs* group whose entries include *don't follow proverbs blindly*. Its introduction says the proverbs apply often — and then that one must always evaluate whether they apply in a particular situation, and that sometimes they are contradictory.

None of that apparatus in the game wiki was designed in, and the oldest collection did without it in a different way. The Tang-dynasty *Wei Qi Shi Jue* is ten rules of four Chinese characters each, and most of them spend part of that budget on the situation they apply to — *when in danger, sacrifice*; *against strong positions, play safely*; *take care of oneself when attacking*. The scope is inside the sentence rather than around the collection.

Which is the more useful way to put the whole progression. **Scope lives either inside the sentence or in an apparatus around the proverb collection, and where it is in neither, the reader supplies it.** Segoe's book puts it in worked game diagrams beside each phrase. The game wiki puts it in categories, provenance marks, and a warning to evaluate before applying. The list of nineteen on the go language wiki has none of the three.

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

The left column names a package. *Syscall* is a specific import, and a sentence whose subject is that import **has nowhere to drift to** — you cannot resolve *syscall* outward, because the word fixes the domain. The right column takes a whole way of working as its subject, and the extent is wherever the reader puts it.

This is a structural claim rather than an empirical one. It says the left column cannot lose its scope, not that nobody ever misapplies those sentences. But it is the strongest control available here: same author, same talk, same form, same afternoon, and the only variable is whether the sentence carries its own extent. The proverb this chapter followed is in the right column.

So the test gets sharper, and becomes something you can check rather than hope for. **Look at the grammatical subject.** If it names a package, a file format, a specific operation, the extent arrived with the sentence. If it names a style of programming, it did not, and supplying it is your job.

**On what these sources are worth**, because they are not equal. Pike's talk is primary. The Go project's wiki page is an official artifact and the strongest evidence that the misreading was real enough to be worth correcting — though note that it attributes the over-use to enthusiasm rather than to the proverb, and this chapter does not claim the proverb caused it. The forum thread is community anecdote: one instance, dated, and useful only because the over-application is self-reported rather than attributed by somebody else. It shows the confusion exists and what shape it takes. It establishes nothing about how often, and nothing here claims otherwise.

---

## Why the claim holds

Compression fixes words. It does not fix their extent.

*Sharing memory* is two words in Pike's sentence and about a paragraph in his explanation of it. The sentence survives repetition; the paragraph does not. So what circulates is a term whose boundary was set somewhere the reader cannot see — and the reader still has to act, so they resolve it. With no context to narrow it, the widest reading is the only one available. That is why the error has a direction. Nobody reads a proverb too narrowly.

**The form causes this, and the form was chosen deliberately.** Pike sets out his criteria near the end: really short, kind of poetic, a little saying, something memorable. Those are constraints on shape, indifferent to whether the surviving sentence is complete. A statement of extent is longer, does not scan, and is useless to anyone not in the situation it names. It is the first thing that will not fit.

He also says of the whole list that the entries might be contradictory, and that sometimes one engineering decision is right and sometimes its exact opposite is. **That is a scope statement covering the entire collection, made once, at the end of a talk, and it is not on the page that carries the proverbs.**

Which gives the test worth keeping: **does this advice say how wide it is?**

- *Use dependency injection.* No extent. You cannot tell whether your situation is one it fits.
- *Channels are for passing ownership of data; mutexes are for caches and state.* States its own extent — which is why the Go project wrote that, and not another proverb.

---

## Where the claim doesn't apply

### Advice with no scope to lose

Some advice is unconditional, and then nothing is missing from the compressed form.

*Gofmt's style is no one's favorite, yet gofmt is everyone's favorite* is on the same list of nineteen, and it became a norm — mandatory automatic formatting, no configuration — without incident. There is no situation in which one consistent format is wrong, so a reader who receives only the sentence has received all of it. Chapter 14 reached this boundary from the other side: a compressed statement is safe exactly when its condition is *always*. Chapter 22 is the general case.

### The domains are not alike, and it explains the lag

Board go is one rule set, fixed for centuries, with a single objective and a bounded space. Software has domains that share almost nothing, tools that turn over in a decade, and no settled agreement about what counts as better.

So a proverb about the board can accumulate a stable scope, while a proverb about software aims at a target moving faster than any apparatus can follow. That predicts what the two collections actually show: twenty-five years of accretion in one, a flat list in the other. It explains the lag rather than excusing it, and it does not change what a reader should do — if anything it raises the odds that the scope you need has not been written down by anyone.

### The repair sometimes arrives

This chapter ends in repair, which is why it does not claim that a principle stripped of its scope stays that way. The scope was rebuilt twice here: officially, in a wiki page with a table, and informally, by strangers answering a question.

Where that does not happen — where the wide reading hardens and nobody writes the page — you get what chapter 23 calls a folk remedy. Chapters 16, 17, and 18 are three cases that travelled further than this one did.

### This book is doing it too

Twenty-three chapters arguing that advice arrives without its scope, ending in a method with a name, is this mechanism with the author as the source.

The answer is not modesty but stating the extent where it is hard to skip, so **two of them are not negotiable.** Chapter 02's classification model is a lens rather than a finding, and that chapter says so — it cannot be proved, only used. And the review practice this book runs on requires the expertise it appears to replace: the errors in these drafts were caught by someone who already knew the material well enough to be suspicious, and a reviewer without that knowledge reads the same confident paragraph and approves it.

If those get compressed away in the retelling, the retelling will sound exactly like this does now. [claude I'm not sure about "This book is doing it too" section. This seems part like splitting hairs, part self-flattery, and part trying to counter every possible argument against the book pre-emptively like a paranoid to me. My recommendation is to delete this section.]

---

## What the claim costs

**Recovering a scope is slow, and usually nobody wrote it down.** Pike's is recoverable because the talk was recorded. For most advice the context is a mailing list that no longer resolves, or a conversation. At that point you are reconstructing rather than reading, which is how a plausible mechanism gets attached to somebody else's sentence — this chapter's first draft did exactly that, asserting a relationship between two of Pike's proverbs that he never claimed.

**The test rejects nearly everything.** Almost no advice states its own extent, because the extent was compressed out before it reached you. *Does this say how wide it is* discards most of what is true along with what is not. It sorts. It does not accept or reject.

**Noticing is cheap and answers nothing.** Observing that a saying has lost its scope takes no work. Finding what the scope was takes a recorded talk, a wiki page, or an afternoon, and that is the part people skip while keeping the posture.

**Compression is not the enemy, and this reads as though it might be.** A sentence that fits in a review comment is how most real knowledge moves between people, and the alternative is everybody re-deriving everything, which is worse and does not happen anyway. The finding is about what to do on receipt.

---

## How to recognize the failure

**In a codebase:**

- **A structure that only makes sense as obedience** — machinery whose justification is a saying rather than a property of this program.
- **A comment citing a rule instead of a reason.** If the line needed the rule written beside it, the rule was not explaining the line.
- **A convention nobody can date.** When nobody can say who decided it or what it was for, the scope is gone and the convention is being maintained rather than used.
- **An argument about what a word in the rule covers.** The whole question in the reddit thread was whether a slice index counts as *sharing memory*. When that is the dispute, the rule is not deciding anything and has not been for a while.[claude this is too simplistic or maybe I misread your wording but the argument in the reddit was not what you stated, the argument is mainly the poster questioning his understanding of the proverb using that code as an example, and it sounds like the example intrigues him because he can't find fault with it but he thinks it contradicts the proverb:
  "I recently came across a piece of code in lo's parallel module that seems to violate this approach... I understand that these proverbs are not set in stone, and that for this simple case, it might very well be worth doing because of the communication overhead, but I'm still curious: would you have written it like this or with channels?

Another question I have is: is this proverb solely related to maintainability/safety concerns (it is safer and more maintanable to use channels instead of shared state) or are there some other reasons?"]

**In a conversation:**

- **A saying offered as the end of a discussion.** The useful follow-up is not *I disagree* but *could you explain how we would apply that saying in this situation concretely and what would that improve?*
- **"That's just how it's done here."** Sometimes a real Idiom with reasons behind it (Ch. 21), sometimes a wide reading nobody has revisited. One question separates them.
- **An appeal to who said it.** The credibility is usually genuine and answers a question nobody asked: it suggests the original observation was sound, and says nothing about whether the sentence you received still contains it.
- **Anyone, including this book, saying a practice always applies.**

The question that does the work: **what more did the person who first uttered this sentence said just after that one?**

If the source can be reached, go and look. The scope is often still there, in the forty seconds after the sentence, in the talk nobody re-watched.

---

**Next:** chapter 16 is the first of the three cases, where object orientation's advice about where behaviour belongs meets the Direction Rule, and produces dependency graphs that point both ways.
