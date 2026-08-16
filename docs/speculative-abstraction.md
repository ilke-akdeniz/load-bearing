# Speculative Abstraction: Source Material

Working document, in the shape of `docs/ai-material.md`.
The argument is worked here once so that the chapters that owe a piece of it agree with each other.

**Owed to:** chapter 18 (primary), chapter 20's line-of-business section (one line), chapter 17 (the testing objection).
Read this before drafting any of them.

**Origin.** The author's, from experience in line-of-business software: decades of building machinery to permit a database swap that never happened.
The refinements below marked as the draft's are corrections made when the claim was tested against chapters the book has already shipped.

## The claim

**An abstraction bought as insurance against a future change usually cannot pay out when the change arrives, because it was shaped by the thing it was insuring against.**

This is not YAGNI.
YAGNI says you paid for something you did not need.
This says the insurance does not cover the event — you paid, the event happened, and the policy was void.
The two are often confused, and the second is the more interesting claim because it survives the reply *but what if we do need it*.

## The distinction that does the work

The author's, and the sharpest part of the argument.

**Swapping forms permanently is not having multiple forms.**

- **Simultaneous plurality** — two implementations live at the same time, dispatched between at run time. Tenant A on Oracle and tenant B on SQL Server. A vendor shipping on-premises software onto whatever database the customer already runs. Here the interface is *exercised*: both implementations are loaded and something chooses.
- **Sequential replacement** — SQL Server today, Postgres forever after. At every moment in time there is exactly one implementation. The interface is never exercised as an interface; it is a shape the code is held in, not a decision anything makes at run time.

The same machinery is justified by the first and not by the second, and the argument for it is almost always stated as if the second were the first.
*We might need to switch databases* describes sequential replacement; *we need to support two databases* describes plurality.
Only the second is a Force.

## Injection is not abstraction

The draft's correction, made because the author's first formulation — *if your system does not need multiple forms today, injection is over-engineering* — contradicts chapter 05.

Two independent decisions get bundled:

1. **Is the dependency passed in, or does the component construct it?** Chapter 05 already argues for passing it in, and the reason has nothing to do with swapping: a component that reaches for `os.Getenv("DATABASE_URL")` is making decisions that were never its to make.
2. **Is it passed in behind an interface, or as a concrete type?**

You can inject `*sql.DB` and get all of (1) with none of (2).
So the over-engineering is the **abstraction**, not the injection, and the claim has to say so or chapter 05 refutes it in one sentence.

This is the same conflation the author caught in chapter 13's Strategy example, where the draft changed the scaffolding and the naming at once and called the difference a win.
Worth noting as a recurring failure shape: **when a comparison bundles two changes, the argument gets credit for the wrong one.**

## Why the insurance does not pay out

Four mechanisms, each leaning on something the book already owns.

**The abstraction is shaped by the engine it was written against.**
A repository interface over Postgres encodes its transaction semantics, its isolation levels, its type mapping, and its error taxonomy.
That is Hyrum's Law (Ch. 05) operating on your own internal interface: what leaked through became part of the contract, and it leaked from the thing you were planning to replace.

**The swap is a data problem and the abstraction is in the code layer.**
Chapter 09's rate layers put the schema below the code and moving more slowly.
The interface lives in the fast layer; what actually has to be migrated — rows, types, constraints, indexes — lives in the slow one.
The abstraction is in the wrong layer to help with the thing it was bought for.

**Staying swappable costs you the engine you are running.**
To keep the interface honest you restrict yourself to what every candidate engine supports: no `jsonb`, no partial indexes, no advisory locks, no `on conflict`.
The premium is paid daily, in features you already own and do not use.

**If the swap ever comes, it comes for a reason the abstraction defeats.**
Nobody changes engines for fun; they change to get different scaling, different consistency, or a different bill.
A lowest-common-denominator interface is exactly what prevents using the thing you moved for.

Which gives the inversion worth stating in the chapter: **the more thoroughly you abstract for portability, the less portability is worth to you.**

## The rollback objection, answered

*We need to be able to switch back quickly* is the usual follow-up, and it does not hold — but only because there are concrete alternatives, so they have to be named rather than gestured at.

The real rollback mechanism for an engine migration is operational, not architectural:

- Logical replication or change data capture into the new engine, running for weeks before anything is cut over.
- Verification by comparison — both engines serving reads, results diffed, until the diff is empty.
- Cut over per-tenant or per-route rather than all at once, which is chapter 12's strangler fig.
- Keep the old engine running and receiving writes for a defined window.

You roll back by pointing at a database that is still there and still current.
None of this is enabled by a repository interface, and none of it can be built in advance usefully, because it is specific to the pair of engines and the shape of the data on the day.

That is chapter 03's reversibility rule applied: the work is cheap to do at migration time and expensive to do speculatively, so deferring it is a plan rather than a bet.

## Where the claim stops

Mandatory, and the boundaries are real rather than polite.

**Portability as a stated requirement.**
If you sell software that customers install against their own database, supporting three engines is a contract term, not a guess.
That is simultaneous plurality and the abstraction is load-bearing.
The Force is chapter 03's *control of the callers*, pointed at the substrate: you do not control the environment your code runs in.

**A funded, dated migration.**
Once the move is decided and scheduled, the abstraction stops being speculative.
It is still probably the wrong tool — see the rollback section — but the objection changes from *this will never happen* to *this is not how to do it*.

**The testing case, which is the strongest legitimate one and belongs to chapter 17.**
Postgres in production and a fake in tests *is* simultaneous plurality, and it is the honest reason most of these interfaces exist.
This document does not resolve it; chapter 17 does, and its position — test against the real database — is what makes the rest of this argument survive.
**Chapter 18 must not pre-empt that argument**, and should cite 17 rather than restating it.

**Not every one-implementation interface is speculative.**
Chapter 05 owns the legitimate uses: narrowing what a consumer can reach, breaking a cycle, declaring a seam the consumer owns.
The claim here is about interfaces justified by a future substitution, not about the keyword.

## Where each piece lands

| Piece | Chapter | Note |
|---|---|---|
| The full worked argument | 18 | Needs 18's contents line in `00_toc.md` extended — the author's call |
| Plurality vs sequential replacement | 18 | The definitional distinction; everything else follows from it |
| Injection is not abstraction | 18 | Must be stated, or chapter 05 refutes the claim |
| The four mechanisms | 18 | Each cites 05, 09, or 03 rather than re-deriving |
| The rollback alternatives | 18 | Cites 12 for strangler fig |
| The LOB inversion, one line | 20 | *The schema outlives the code* already promised there |
| The testing case | 17 | 18 cites it; 17 owns it |

**Open question for the author.**
Chapter 18's stated subject is a structural idea expressed as directories, which is file layout.
This argument is about speculative abstraction, which is adjacent but not the same thing.
Either 18's scope widens by a paragraph in the TOC, or this wants a different home.
The alternative is chapter 20, where it fits the domain but would unbalance a chapter that gives each domain a short treatment.
