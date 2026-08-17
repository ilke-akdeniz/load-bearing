# How a Principle Becomes a Movement

## The claim

**The conditions are what made the advice true, and they are the first thing lost — because what travels is selected for being short, and a condition makes a saying longer.**

Part IV is three case studies, and this chapter is the mechanism they share, stated once so that each of them can be about its own subject instead of re-deriving this.

The book has met the result of this several times: a theorem repeated without its quantifier (Ch. 04), a count repeated without its *for at least some uses* (Ch. 13), a diagnosis repeated without the payment that justified it (Ch. 14). Those chapters own the instances. **This one owns the transmission** — not that conditions get lost, but why losing them is the normal outcome rather than a lapse by careless people.

---

## The demonstration

### A proverb, and the condition published beside it

In November 2015 Rob Pike gave a talk at Gopherfest that became the Go proverbs. Nineteen sayings, and the first is the one everybody knows:

> Don't communicate by sharing memory, share memory by communicating.

Two things he said in the same talk did not travel with it. The first is what he thought a proverb was for:

> as ideas you might use to explain. Maybe in a code review, or when you're teaching someone new about something, or trying to stop an argument on Stack Overflow or whatever.

The second is stronger, and it is a direct statement that the sayings are not rules:

> they might be contradictory. Proverbs aren't always — real proverbs in the real world you can find lots that are exactly the opposite. And that's okay too, because sometimes one engineering decision is right, sometimes the exact opposite is right.

*Sometimes the exact opposite is right*, said by the author, in the talk that produced the list.

And he was not being vague about which opposite. It is the third item on the same slide deck:

> Channels orchestrate; mutexes serialize.

**The condition was published beside the proverb, by the same person, on the same afternoon.** One of the two is quoted in code reviews a decade later and the other is not, and the difference between them is not correctness. It is length, rhythm, and the fact that the first one is a complete instruction while the second requires you to already know what your problem is.

Pike also said what he was selecting for. A proverb has to be "really short", "kind of poetic", "memorable", "a little saying". Those are the criteria, stated plainly — and **they are the criteria a condition cannot survive.** A conditional is longer than an imperative, it does not scan, and it is not memorable, because the thing that makes it useful is exactly the thing that makes it specific to a situation the listener may not be in.

### What the proverb costs when the condition is missing

Take a counter that several goroutines increment. The state is one integer, there is no orchestration to do, and by the third proverb this is a mutex.

```go
type Counter struct {
	mu    sync.Mutex
	value int64
}

func (c *Counter) Add(delta int64) {
	c.mu.Lock()
	c.value += delta
	c.mu.Unlock()
}

func (c *Counter) Value() int64 {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.value
}
```

Now the version the first proverb asks for, where the state is owned by a goroutine and reached only by messages. (Chapter 06 owns why this is a correct way to protect state — here the question is only what it costs when it was not the right one.)

```go
type ChanCounter struct {
	adds  chan int64
	reads chan chan int64
	done  chan struct{}
}

func NewChanCounter() *ChanCounter {
	counter := &ChanCounter{
		adds:  make(chan int64),
		reads: make(chan chan int64),
		done:  make(chan struct{}),
	}
	go counter.run()
	return counter
}

func (c *ChanCounter) run() {
	var value int64
	for {
		select {
		case delta := <-c.adds:
			value += delta
		case reply := <-c.reads:
			reply <- value
		case <-c.done:
			return
		}
	}
}

func (c *ChanCounter) Add(delta int64) { c.adds <- delta }

func (c *ChanCounter) Value() int64 {
	reply := make(chan int64)
	c.reads <- reply
	return <-reply
}

func (c *ChanCounter) Close() { close(c.done) }
```

Both are correct. The second is thirty-four lines against fourteen, and it introduces a goroutine that must be started, a shutdown path that must be called, and a reply channel allocated on every read. It also does this:

```text
BenchmarkMutexAdd-10        300000       145.4 ns/op
BenchmarkChannelAdd-10      300000       354.7 ns/op
```

One machine, one run, and the ratio held between 2.4 and 2.5 across repeats — call it two and a half times the cost, for a program that gained nothing, written by somebody following published advice from the language's designer. **The advice was not wrong. It arrived without the sentence that said when it applied**, and that sentence was available the whole time, three lines further down the same list.

### The four steps, and why none of them is a mistake

Nobody in this sequence does anything unreasonable.

```text
 1  an observation is true, under conditions its author knows
 2  it gets compressed into a name or a saying, to be teachable
 3  the name acquires a community, which teaches the name
 4  the conditions are not in the name, so they stop being taught
```

Step 2 is the load-bearing one and it is also the one nobody can skip. Advice that is not compressed does not get transmitted at all — an unabridged account of when to prefer channels over mutexes is a chapter, and chapters do not get quoted in code reviews. **The compression is what makes the advice useful and is the same operation that strips it**, which is why this keeps happening to careful people.

By step 4 the community is not withholding the conditions. It does not have them. They were never in the artifact that was passed along, and the person who knew them said them once, out loud, in a talk that is now a decade old and has been watched by a small fraction of the people repeating its output.

### The case where there were never any conditions

Run the same test on generated code and it returns something the four steps cannot describe.

Ask a model for a workflow library and you get a repository interface, a service layer, and a dependency-injection wiring file. Every one of those is a decision, and none is announced. There is no name to look up, no talk to re-watch, no author who once stated the conditions. **The answer to *what were the conditions* is not that they were forgotten but that none were ever formed** — the artifact is the output of a corpus in which that shape was common, and commonness is not a derivation.

That makes it a harder case than a movement, not an easier one. A slogan at least leaves a thread to pull: you can find who said it and what they said around it, which is what this chapter just did to Pike. Generated code leaves no thread, because a taken branch leaves no mark. There is nothing to be suspicious of, since nothing was asserted.

---

## Why the claim holds

The mechanism is selection, and it operates on sayings rather than on people.

Of everything a practitioner knows, only some of it is short enough to repeat. Of what is repeated, the memorable survives. Pike named the filter himself — short, poetic, memorable — and it is a filter on *form*, entirely indifferent to whether the surviving sentence is complete.

A condition is the part that loses. It makes the saying longer, it breaks the rhythm, and it is useless to anyone not in the situation it names. So the same saying, transmitted twice, arrives shorter each time, and what falls off is not random.

**This is why practitioner credibility provides no protection.** The usual defence of a movement is that its originator had built real things — Pike had Unix, Plan 9, and UTF-8 behind him before Go, and the proverbs are compressed scar tissue rather than theory. All of that is true and none of it helps, because the filter is applied downstream of the author by everyone who repeats them. The Go community produced its own cargo cults inside a decade, from a source with about as much credibility as is available.

Which gives the test that survives, and it is the one to keep from this chapter: **does the idea arrive with the conditions under which it is wrong?**

- *Use dependency injection.* No conditions. A slogan, and you cannot tell from it whether your situation is one of the ones it fits.
- *Channels orchestrate; mutexes serialize.* States its own boundary in four words, which is why it is worth more than the proverb that outran it.

---

## Where the claim doesn't apply

### Advice with no conditions loses nothing in transmission

The mechanism only bites when there were conditions to lose. Some advice has none, and it compresses perfectly because there is nothing to strip.

The clearest case is on the same list of proverbs:

> Gofmt's style is no one's favorite, yet gofmt is everyone's favorite.

That became a movement — mandatory automatic formatting, no configuration, no argument — and the movement was an improvement, unambiguously. It works because there is no situation in which having one consistent format is wrong. The advice is unconditional, so a reader who receives only the slogan has received all of it.

This is chapter 14's boundary in a different costume: a compressed statement is safe exactly when its condition is *always*. Chapter 22 is the general case, where being right matters less than being consistent, and the compression loses nothing because there was nothing underneath.

### Movements that were right, and the mirror-image error

Automated testing, version control, code review, and memory-safe languages by default all arrived as movements, with advocacy and slogans and people who overdid it. All four were improvements, and the field is better for the overdoing.

**Dismissing methodology as such is the same error running the other way.** *All movements are cargo cults* is itself a compressed claim with its conditions removed, and it fails the test in this chapter exactly as *use dependency injection* does. The chapter's finding is that a movement's slogan is not evidence about the underlying observation — in either direction. You still have to go and find the conditions, and *find them* is the work, not *dismiss the movement*.

The specific error to avoid is treating this chapter as permission to ignore advice from people who have organized. Organization is not evidence of wrongness. It is evidence that compression happened, which tells you where to look.

### This book is running the same mechanism

Twenty-three chapters arguing that advice arrives stripped of its conditions, ending with a method and a name for it, is step 2 of the sequence above with the author as the originator.

The honest response is not modesty, it is to state the conditions here where they are hard to skip. **Two of them are not negotiable.**

The classification model in chapter 02 is a lens rather than a finding, and that chapter says so — it cannot be proved, only used, and where it stops being useful is where you stop using it. And the review practice this book runs on requires the expertise it appears to replace: the errors in these drafts were caught by somebody who already knew the material well enough to be suspicious, and a reviewer without that knowledge reads the same confident paragraph and approves it.

If either of those gets compressed away in the retelling, this book will have become an instance of its own subject, and the retelling will sound exactly like it does now.

---

## What the claim costs

**Finding the conditions is slow, and often they are not written down anywhere.** Pike's are recoverable because the talk was recorded and transcribed. For most advice the original context is a mailing list that no longer resolves, a team that dispersed, or a conversation. At that point you are reconstructing rather than reading, and reconstruction is how a plausible mechanism gets attached to somebody else's claim.

**The test rejects most usable advice.** Almost nothing arrives with its conditions attached, because the conditions were compressed out before it reached you. Applied strictly, *does this state when it is wrong* discards nearly everything, including things that are true. It is a sorting instrument, not an acceptance test — a saying that fails it is unfinished, not false.

**Suspicion of movements is cheap and feels like rigour.** Noticing that something has become a movement takes no work and produces no answer. The work is finding what the original observation was and under what conditions it held, and that is the part people skip while keeping the posture.

**Compression is genuinely valuable and this chapter can be read as an argument against it.** It is not. A saying that fits in a code review comment is how a large amount of real knowledge actually moves between people, and the alternative — everybody re-deriving everything — is worse and does not happen anyway. The finding is about what to do when you receive one, not about refusing to make them.

---

## How to recognize the failure

**In a codebase:**

- **A structure that only makes sense as obedience.** A goroutine and three channels guarding one integer; an interface with one implementation and no second in prospect; a package layout that costs an export on every helper (Ch. 18).
- **Advice cited by name rather than by consequence.** A code comment reading *// don't communicate by sharing memory* explains nothing about this program, and the fact that it needed a comment suggests the author knew that.
- **A convention nobody can date.** If nobody on the team can say who decided it or what problem it was for, the conditions are gone, and the convention is now being maintained rather than used.

**In a conversation:**

- **A saying offered as the end of a discussion.** The follow-up that works is not *I disagree* but *what does that rule out here* — the constraint question from chapter 10, aimed at a slogan instead of a pattern name.
- **"That's just how it's done in X."** Sometimes a genuine Idiom with real reasons behind it (Ch. 21), and sometimes step 4 with no memory of steps 1 through 3. Asking which costs one question.
- **An appeal to who said it.** The credibility is usually real and it is answering a question nobody asked. What the originator built tells you the observation was probably sound; it tells you nothing about whether the compressed version you were handed still contains it.
- **Anyone, including this book, telling you a practice always applies.** That sentence is the diagnostic, and it does not have exceptions for authors you like.

The question that does the work: **what did this cost the person who first said it, and would they say it here?**

If the advice has a source you can reach, go and read what they said around it. The conditions are frequently still there, three lines further down, in the same talk.
