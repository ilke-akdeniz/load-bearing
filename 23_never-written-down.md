# What Was Never Written Down

## The claim

**A decision nobody stated can be recovered only while someone still remembers it — and when the author was an AI coding agent that remembers nothing between sessions, that recovery window was never open.**

Every chapter before this one works on a claim somebody made. A proverb, a review comment, a pattern name, a rule in a style guide — the technique throughout has been to find the condition behind the assertion and check whether it holds here. This chapter is about the case where there is no assertion, because the decision was taken without ever being said.

---

## The demonstration

### A decision nobody wrote down

Here is a function that fetches a workflow definition and its steps. It is two queries, and they are wrapped in a transaction.

```python
def get_definition(connection, definition_id):
    connection.execute("BEGIN")
    definition = connection.execute(
        "SELECT name, revision FROM definitions WHERE id = ?", (definition_id,)
    ).fetchone()
    steps = connection.execute(
        "SELECT position, label FROM steps WHERE definition_id = ? ORDER BY position",
        (definition_id,),
    ).fetchall()
    connection.execute("COMMIT")
    return definition, steps
```

The transaction looks like ceremony. Nothing is written, so there is nothing to roll back, and a reader who has been taught that transactions are for writes will see two harmless `SELECT`s inside a wrapper that does no work.

It is doing work. Definitions are edited while they are being read, so between the first query and the second an editor can commit a change. Without the wrapper the two queries take separate snapshots, and the function returns a definition assembled from both sides of that edit — a version number from before it and a step list from after it.

Somebody later removes the wrapper, because it does nothing:

```python
def get_definition(connection, definition_id):
    definition = connection.execute(
        "SELECT name, revision FROM definitions WHERE id = ?", (definition_id,)
    ).fetchone()
    steps = connection.execute(
        "SELECT position, label FROM steps WHERE definition_id = ? ORDER BY position",
        (definition_id,),
    ).fetchall()
    return definition, steps
```

Both versions run. Both pass a test suite that does not have a concurrent editor in it. With one committing an edit between the two reads, they differ:

```text
with the transaction:     revision 1, steps ['collect-id', 'verify']
without the transaction:  revision 1, steps ['collect-id', 'verify', 'approve']
```

The second row is revision 1 of a definition that has three steps. **No such definition was ever saved.** Revision 1 had two steps and revision 2 has three, and the function has returned a tree assembled from both. Nothing raised, nothing logged, and the caller has a workflow that never existed.

*(The interleaving is forced in the run above so that it happens every time. In a running system it happens when it happens, which is the part that makes it expensive to find.)*

Chapter 19 maps this same decision as a log entry, with its forces named and the transaction marked as forced rather than chosen. This is the same decision seen from the other end: in the code, where none of that is visible.

### Why asking afterwards does not get it back

If the transaction was put there by a person, there is a period during which you can find out why. They remember, or they wrote it down, or somebody who was in the room remembers. The period is finite and it is longer than nothing.

If it was put there by an AI coding agent, the intuition is that the same applies while the session is open — that you can ask, and the reason will come back. That intuition is wrong, and the reason is architectural rather than a matter of how good the tool is.

**A forward pass discards its activations.** Whatever computation selected the transaction over its absence produced a token and was not retained. The key-value cache holds values derived from tokens and exists to avoid recomputation; it is not a record of reasoning. Every mechanism an agentic coding tool has for persisting anything — the context window, the transcript, a memory file, a project instructions file — stores **text**. So there is never a replay. There is only whatever was written.

Which gives three cases, and they are not equally bad.

```text
 same session, reasoning was written out
   you are reading text. Real retrieval — of what was said,
   not of what happened.

 same session, nothing was written
   a fresh computation runs on overlapping input and produces
   a correlated answer. Not a recollection. Often right.

 new session
   only the artifact is in context. The prompt that produced
   the code is gone.
```

**The middle case is the one that does the damage**, because it is right often enough to be trusted and is a correlation rather than a memory. *Ask it while the context is fresh* is advice that works, until the day it does not, and there is no signal that distinguishes the two occasions.

There was a computation that produced this line rather than another one, and there was never a sentence saying why. Asking afterwards does not retrieve one. It produces one.

**This is narrower than the research question it sits next to, deliberately.** Whether a model's stated reasoning reflects its computation is contested. Miles Turpin and colleagues showed that chain-of-thought explanations *"can systematically misrepresent the true reason for a model's prediction"* — bias the input, and models rationalise the biased answer without mentioning what moved them. Kerem Zaman and Shashank Srivastava argue the standard measure confuses unfaithfulness with **incompleteness**, *"the lossy compression needed to turn distributed transformer computation into a linear natural language narrative"*, and that unstated influences still act causally through the reasoning. Nothing in this chapter needs that argument settled. It rests on the narrower fact that what persists is text, so what can be recovered is what was recorded.

And one thing does survive, which is worth separating out because it gets conflated with the other. **What the code does is re-derivable from the code**, by a person or by the agent, at any time. Asking for a description of behaviour is reading. Asking why this shape was chosen is not — that was never in the artifact, and no amount of freshness puts it there.

### The folk remedy [-- this section should simply be deleted, adds not much too the chapter, mostly distracts from the natural flow - reading of the chapter]

There is a name worth having for the thing that arrives instead of a decision.

A **folk remedy** is advice applied far outside the context it was made for, which stays misapplied because nobody rebuilds its scope. *Drink two litres of water a day* is the pattern — a number from a context nobody can now name, repeated by people who did not take it from a source and cannot say what it was for. The term is this book's author's rather than standard vocabulary. Chapter 15 shows a principle losing its scope in transmission and then having it rebuilt three times; a folk remedy is what the same process produces when nobody writes the page.

**A corpus default is the purest instance there is.** The convention arrives because it is what most code does, not because it answers anything about your situation, and nobody rebuilds the scope because nobody knows a scope existed — or that a choice was made. Chapter 02 names monoculture as the single most common source of confusion between the kinds and prescribes one cure: work in a second ecosystem long enough that its conventions stop feeling wrong and start feeling like conventions. That cure is unavailable to a model with one training distribution, and an agent built on it inherits the limit.

### Grilling: making the decision happen in the open

Chapter 19's procedure assumes you can name the forces before the design exists. Usually you cannot — not because you are careless, but because you do not yet know which decisions are about to be made, so you do not know which facts about your situation are about to matter.

One technique inverts the flow, and it is worth stating in full because it is the method's shape [-- which method? I know the answer but most reader's would not, need a reminder here] with the roles swapped. Instead of supplying forces up front, you have the decisions surfaced one at a time and supply the fact that settles each one as it arrives. The prompt, quoted as the author of this book uses it:

> Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.
>
> Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.
>
> If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.
>
> Do not act on it until I confirm we have reached a shared understanding.

The technique is not this book's. It comes from Matt Pocock's skills repository, as `skills/productivity/grilling/SKILL.md`, and this book's author encountered this use of it through a video by Jason Ku. The version quoted above is an earlier one, frozen here because the upstream text has since changed.

**The split between fact and decision is the load-bearing line.** Facts get looked up; decisions get put to the human. That is chapter 19's step one and step two, separated and given owners — and the separation is what makes the output auditable, because every decision arrives with a recommendation you either took or overrode.

The recommendation attached to each question is where the value is, and it takes an example to see why. Two questions from the start of a real library, with the answers that were actually given:

```text
> Should ids be generated by the application or by the database?
  Recommended: the database, via a column default. One less thing
  for a client to get wrong.

< The application. A client assembles a whole definition offline
  and hands it over in one call, so the ids have to exist before
  any of it reaches Postgres.

> Then UUIDv4 or UUIDv7?
  Recommended: v4. It is the common default.

< v7. These are primary keys on a table that only grows, and v4
  scatters inserts across the index.
```

Both recommendations were sensible, both were overridden, and the same kind of thing did the overriding each time: a fact about this library that is not in any corpus.

The first is about how the library is used — a client builds a whole definition in memory before any part of it exists, so ids cannot come from a column default without splitting the call. The second is a latency-budget reading at volume: these are primary keys on a table that only grows, and v4 scatters inserts across the index.

Only the second is one of chapter 03's seven, which is chapter 19's point that the seven are not a closed list. What makes both of them forces is that each is checkable, and each says what would have to change for the answer to change.

And note who supplied them. In both cases the human, because both are facts about this situation — which is the one thing a recommendation drawn from what is common cannot contain. The recommendation is the majority ecosystem's convention arriving in the voice of an answer, which is an Idiom (Ch. 02) with its locality stripped off.

The alternative is not that these two decisions go unmade. Without the interview both would still have been taken — a column default and a call to a v4 constructor, chosen by whatever is most common, with nothing in the file showing that anything was chosen at all. That is the case this chapter is about.

The narrower point here is the one worth keeping: **grilling does not produce better answers. It produces answers somebody can disagree with.**

And disagreeing with them later requires that they were written down. The interview produces a sequence of decisions with the reasoning attached, and the reasoning is the perishable half: an hour afterwards the code is still there and the override is not. So the last step of the loop is that each settled decision goes into the log — chapter 19's artifact, and the reason FlowCore's decision 12 was available to be mapped months after anyone made it.

That closes the circuit, and it is worth seeing as one thing rather than three. The interview surfaces the decision, the log records what settled it, and a standing instructions file promotes the answers that keep recurring into constraints so the same question stops being asked. Grilling without that second step is a conversation rather than a record, and a conversation is exactly what does not survive the session.

The upstream text has since changed in a way worth one line: it asks a round of questions at once where the frozen version asks one at a time. That is throughput against how much the reader has to hold in working memory, which is a force with a value, so neither version is a regression.

**The limit, and it is severe. Grilling is weakest against folk remedies**, because a folk remedy [-- if you agree on removing the folk remedy section above, the terms here should be changed accordingly. "mainstream advice that lost it's scope"] does not present itself as a branch point. The interview surfaces the decisions the agent treats *as* decisions, and that set comes from the same corpus, so a question settled uniformly across it is not offered at all — it is simply how things are done.

Which means the technique surfaces contested choices and conceals settled ones, and settled-in-the-corpus is the class most likely to be wrong outside the ecosystem it came from. This follows from chapter 02's mechanism rather than from any measurement, and it should be read as reasoning rather than as a finding.

---

## Why the claim holds

The claim rests on one asymmetry: a decision is a thing that happened, and a record is a thing that exists.

Code preserves the outcome perfectly and the reason not at all. The transaction is still there in the file, byte for byte, years later. What is not there — and was never there — is the sentence saying that concurrency and blast radius together left no alternative. Chapter 19 calls that distinction forced against chosen, and it is the one thing you cannot reconstruct from the artifact, because both kinds of decision compile to the same bytes.

For a human author, memory covers the gap for a while. It is unreliable and it fades, but it exists, and the fading is what makes *write it down while it is fresh* good advice rather than ceremony.

**Remove the memory and the advice stops being about diligence.** There is no interval during which the reason is available and undocumented, because there was never a moment when it existed anywhere but in a computation that has already been discarded. The record is not a backup of something. It is the only copy there has ever been.

### One decision, then all of them

The example above loses one reason. What matters is what happens when it is not one.

Each unrecorded decision constrains the next change without saying so. Someone removes the transaction; the next person notices intermittent bad reads and adds a retry; a third adds a cache to reduce the reads that are now being retried. Every step is locally reasonable and each adds a constraint nobody recorded either. The code accumulates behaviour that is load-bearing and undocumented, and the accumulation is faster than the removal, because removing anything requires knowing what it was for.

What that looks like from outside is a system that works and cannot be changed. The requests to the agentic coding tool become negative — *fix this, do not break that* — because the only thing anyone can specify is the observable behaviour they want preserved, which is another way of saying nobody knows which behaviour is intentional.

**And the agent is in the same position.** This is the part that has no equivalent in the pre-AI version of the story. A codebase that people wrote and failed to document is still readable by people, slowly and expensively. Here the artifact is equally opaque to the agent that produced it, because it kept nothing either. There is no party to the situation who knows more than the code says.

From there the honest options are guessing the design reasons or starting the development from scratch. [--deleted that sentence because low value, hard to prove claim.]

**None of this is new.** Undocumented design decisions, accumulated local reasonableness, and a rewrite at the end of it is the ordinary history of a great deal of software written entirely by people. What changed is not the failure. It is that the interval which used to be measured in years can now be measured in weeks, because the rate at which decisions get taken went up by orders of magnitude and the rate at which they get recorded did not move.

That is a force reading, not a verdict (Ch. 03). Whether to work this way is a fact about your situation rather than a position this book takes. [-- I find this a little bit cynical, knowing that a big majority uses ai to generate code and make design decisions, then showing how things can go terribly wrond if you don't record the decisions and then sating feel free to not use this method is not ok. I would just delete this paragraph. ]

---

## Where the claim doesn't apply

### The decision the artifact enforces

The claim says the reason has to survive somewhere. It does not, when the decision is written into something that refuses to be violated.

The transaction above is the bad case precisely because removing it compiles, passes, and runs. Compare a rule put into the schema instead:

```sql
CREATE TABLE revisions (
    definition_id INT,
    revision      INT,
    active        INT,
    UNIQUE (definition_id, active)
);
```

Somebody later decides a definition can have two active revisions at once, and finds out immediately:

```text
IntegrityError: UNIQUE constraint failed: revisions.definition_id, revisions.active
```

**Nobody needs to remember why.** The constraint states the decision, enforces it, and objects on its own behalf when a change contradicts it — and the objection arrives at the moment of the change rather than in production, which is the only feedback that reliably survives a hand-off to somebody who was not there.

So the claim has a corollary that is more useful than the claim: where a decision can be made self-enforcing, that is worth more than recording it, because the enforcement does not depend on anybody reading anything. Chapter 12 works the general technique as making illegal states unrepresentable, and chapter 20 shows the line-of-business profile pushing rules into the schema for the related reason that the schema outlives the code.

The boundary is real and it is narrow. Most design decisions cannot be expressed as a constraint — *four queries rather than one join, because a join fans out to fifteen rows to dedupe* is a judgement, not an invariant. For those the record is the only mechanism there is.

### A decision nobody needs

Most code embodies no decision worth recovering. The name of a local variable, the order of two independent statements, which of two equivalent library calls got used — there is nothing behind these, and treating every line as a lost decision produces a log nobody reads and a review that never ends. Chapter 19's test applies: what does being wrong here cost, and who finds out.

---

## What the claim costs

**Grilling is slow, and the cost is per decision rather than per project.** One question at a time, waiting for each answer, on work that a single sentence would otherwise have produced. On a small change it is absurd overhead, and the honest version of the advice includes the word *sometimes*.

**It requires you to hold opinions.** A person who accepts every recommendation has bought the silent defaults back with ceremony attached, and now has a record showing that each one was considered. That record is worse than none, because it looks like evidence. [-- maybe delete this. It look like the reversal of "even when you take only recommended options, it's still useful..." point made earlier.]

**The record is partial by construction.** The interview surfaces what the agent presents as a decision, and what it presents comes from the same place its recommendations do. A complete record is not on offer; a record of the contested decisions is.

**And writing it down does not make it right.** A recorded decision is one somebody can disagree with later, which is all that is claimed for it. The chapters before this one are what tell you whether the decision was any good; this one only says that if it goes unwritten, that question stops being askable.

---

## How to recognize the failure

**In a codebase:**

- **A commit that removes something as unnecessary, with no reason given either way.** The change and the thing it removed are now both undocumented, and the second one used to work.
- **Comments that say what the code does.** Restating the mechanism is what a reader could already get. The line that cannot be recovered is why this mechanism rather than another one. [-- don't agree, sometimes you really need a comment that say what the code does, because the code is simply crap and there is no time or safety net to refactor it.]
- **Defensive code nobody will touch.** A retry, a lock, a sleep, a `try` that catches everything — kept because removing it once caused something and nobody found out what.
- **A test suite that passes and a system nobody will change.** The tests encode the behaviour and none of the reasons, so they say a change is safe without being able to say a change is correct.

**In a conversation:**

- **"Fix this, don't break that."** The request is negative because the observable behaviour is the only thing anybody can still specify.
- **"I don't know why it does that, but leave it."** An accurate report of the situation, and the last point at which asking is cheap.
- **"Let's just regenerate it."** Sometimes correct. It is also the move that guarantees the next version has no recorded decisions either. [-- regenerate what? regenerate meaning write a new prompt to generate code?]
- **"It was working yesterday."** Said about a system whose working state nobody can characterise, which is what makes the sentence unanswerable.

The question that does the work: **if this turns out to be wrong, what would tell us why it was done?** [-- i don't get what the first part of the sentence contributes. I would prefer this : "who can tell us why it was done?"]

If the answer is a person, ask them now. If it is a document this chapter does not apply to you. If the answer is that somebody would read the code and infer — then what you have is the code, and the reason was never written down.
[-- this part could be worthy of an expansion: "If the answer is that somebody would read the code and infer — then what you have is the code, and the reason was never written down." I am that somebody very often and the process is very painful]
---

## Sources

Matt Pocock, *skills* — `skills/productivity/grilling/SKILL.md`. <https://github.com/mattpocock/skills> The text quoted here is an earlier version, frozen; upstream has since changed.

Jason Ku, on using the technique during development. <https://www.youtube.com/watch?v=ikGhv9kKFdU&t=356s>

Miles Turpin, Julian Michael, Ethan Perez and Samuel R. Bowman, *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting*, NeurIPS 2023. <https://arxiv.org/abs/2305.04388>

Kerem Zaman and Shashank Srivastava, *Is Chain-of-Thought Really Not Explainability? Chain-of-Thought Can Be Faithful without Hint Verbalization*, 28 December 2025. <https://arxiv.org/abs/2512.23032>

FlowCore, `docs/decisions.md`, decision 12. <https://github.com/ilke-akdeniz/flowcore>
