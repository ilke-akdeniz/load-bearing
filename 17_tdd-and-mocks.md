# TDD, Mocks, and What Testing Actually Buys

## The claim

**Neither *write the test first* nor *mock your dependencies* says what it buys. Under the wide reading of each, a mocked dependency deletes exactly the failures the test was written to catch, and the ordering turns out to be the one dimension the best-instrumented study of it could not find an effect for — under conditions that study states and its popular version drops.**

This is Part IV's second case, and it is kept fair. Tests are worth writing, the two principles below are worth following in most situations, and neither of those is in dispute here. The terms with no fixed extent are what **first** buys, and what counts as a **dependency**.

---

## The demonstration

### What a mocked test is about

A registration service enforces one account per email address. The uniqueness is the database's — a `unique` constraint on the column:

```python
SCHEMA = """
create table account (
    id      integer primary key,
    email   text not null unique
)
"""
```

```python
class Registration:
    """One account per email address. The uniqueness is the database's."""

    def __init__(self, accounts):
        self.accounts = accounts

    def register(self, email):
        try:
            self.accounts.insert(email)
        except sqlite3.IntegrityError:
            raise DuplicateEmail(email)
```

Here is the test a reasonable engineer writes for that, with the repository mocked so the suite does not need a database:

```python
def test_with_a_mocked_repository(self):
    accounts = Mock(spec=AccountRepository)
    accounts.insert.side_effect = [
        None,
        sqlite3.IntegrityError("UNIQUE constraint failed: account.email"),
    ]
    registration = Registration(accounts)

    registration.register("ada@example.com")

    with self.assertRaises(DuplicateEmail):
        registration.register("ada@example.com")
```

Nothing about it is lazy. It names the behaviour, it exercises the real `Registration`, it asserts a real exception type. It passes.

Now delete the constraint it is named after. One word out of the schema:

```python
SCHEMA = """
create table account (
    id      integer primary key,
    email   text not null
)
"""
```

The database will now happily store the same email twice. Running both tests:

```text
FAIL: test_against_the_database (DuplicateEmailIsRejected.test_against_the_database)
AssertionError: DuplicateEmail not raised

Ran 2 tests in 0.001s

FAILED (failures=1)
```

One failure, not two. **`test_with_a_mocked_repository` still passes**, and it will keep passing for as long as the line `accounts.insert.side_effect = [...]` is in it.

The reason is not subtle once stated. That line is where the `IntegrityError` comes from. The test asserts that `Registration` converts an `IntegrityError` into a `DuplicateEmail`, which is true and which is roughly four lines of the system. Whether an `IntegrityError` ever arrives is a fact about the schema, and the mock supplied it by hand.

**A test can only fail for a reason it can reach.** Mocking a dependency removes the reasons that live inside it. What is left is a test of the seam.

### What counts as a dependency

That is the mechanism. The reason it is widespread is the second principle, and the term in it with no fixed extent.

*Mock your dependencies* does not say what a dependency is. Under the widest reading — anything your unit does not itself compute — the database is a dependency, the clock is a dependency, the file system is a dependency, and so is the other class you wrote last Tuesday. Under a narrow reading, a dependency you must replace is one you **cannot run**: it costs money per call, it needs hardware you do not have, or it belongs to somebody else.

The two readings differ on exactly one thing, and it is the thing this chapter is about: whether the rule you care about lives inside the dependency or outside it.

FlowCore takes the narrow reading and states it as a rule: its tests run against a real Postgres, not a fake. The reason is visible in its schema. Its decision 4 pushes same-definition integrity into composite foreign keys, and decision 9 puts uniqueness — scoped, case-insensitive, length-capped — into constraints. A fake repository would be a second implementation of every one of those rules, written by the same person who wrote the first, agreeing with it by construction, and unable to disagree with the schema when the schema is wrong.

That is the general form. **A double can only encode the constraints its author already knows about.** The constraints worth testing are the ones somebody will get wrong.

### The test that never reaches its condition

The mocked test above at least asserts something. The more common failure is a test that reaches nothing at all, and it is hard to see by reading.

FlowCore's decision 37 records one, caught late. A workflow fixture declared a single status, `"in progress"`, and pointed both of its terminal actions at it. So a run reported `"in progress"` before finishing and `"in progress"` after finishing, and the assertion checking the terminal status could not tell a correctly stamped status from one that was never written.

It was found by mutation — breaking the code deliberately to see whether anything notices:

> Established by mutation rather than by inspection: `completeWorkflow` was changed to stamp `completed_at` but never the status columns, and **the entire suite passed**.

Nothing anywhere covered terminal-status stamping. After the fixture was given three distinct statuses, the same mutation fails properly: `terminal status = "in progress", want "rejected"`.

Two things in that entry are worth more than the fix.

The first is the count. It says this was **the fifth toothless or invalid test in one iteration**, and that the first mutation used to investigate it was itself invalid — it broke SQL parameter type inference rather than the behaviour, so its failure proved nothing until casts were added. Even the check needed checking.

The second is what the code said about itself. A comment sat directly above the weak fixture:

```go
// twoStepDefinition's terminal action ends in its only status
```

The weakness had been noticed at the time and written down instead of fixed. The entry's own verdict:

> A comment explaining why an assertion is weak is not a substitute for an assertion that is not.

**The recurring shape is a test that never reaches the condition it names**, and neither reading it nor counting it detects that. Coverage reports the line was executed, not that the assertion could have failed. Mutation is the check that answers the actual question, which is whether this test can fail at all.

### What the ordering was measured to buy

The other principle is about order, and here there is real evidence, which makes it a better case than an argument.

Fucci, Erdogmus, Turhan, Oivo, and Juristo instrumented the question directly rather than comparing two groups of people. Thirty-nine professional developers — averaging 7.3 years of Java experience — worked through programming tasks in an IDE recording every action, producing 82 usable data points. Instead of asking *did the TDD group do better*, they decomposed what the developers actually did into four measurable dimensions:

```text
 GRA  granularity        median cycle duration in minutes
 UNI  uniformity         median absolute deviation of cycle duration
 SEQ  sequencing         percentage of cycles that were test-first
 REF  refactoring        prevalence of refactoring activity
```

Then they asked which of the four explain the variation in external quality and in productivity.

**Sequencing dropped out of both models.** Granularity, uniformity, and refactoring effort survived; the test-first fraction did not, for quality or for productivity. Shorter cycles helped — the improvement reaches about 14% as median cycle length falls from around 50 minutes to around 8 — and steadier cycles helped. Refactoring effort, counter-intuitively, was *negatively* associated with external quality.

Their own summary of the practical upshot:

> We think that this aspect should be emphasised over religiously focusing on leading each production cycle with unit tests.

This travels as *TDD doesn't work* or *the order doesn't matter*. Here is what is in the same paper, and mostly in the same paragraph:

> The absence of sequencing as an influential dimension does not imply that a strictly develop-then-test (test-last) strategy should be preferred over a test-first strategy: this advice would require a negative (statistically significant) coefficient, which the models did not produce.

> Our results simply state that the order in which unit tests and production code are written may not be as important as commonly thought so long as the process is iterative, granular, and uniform.

> A test-first dynamic may provide long-term advantages not addressed by or detected in our study.

They name three of those advantages they did not measure: resolving requirements uncertainty, formalizing design decisions, and encouraging writing more tests. And they state two limits of the design: it is a single-group study with no control group, and two of the three tasks were artificial rather than representative of professional work.

**Read the conditions and the finding is narrower and more useful than either slogan.** It does not say the ordering is worthless. It says the ordering is not where the measured benefit came from, that the benefit came from small steady steps, and that this holds *given* a process which is already iterative, granular, and uniform — which is a condition a team that has abandoned the ritual may no longer meet.

Chapter 15's mechanism, running on a peer-reviewed paper rather than a proverb. The conditions were published beside the finding, by the same authors, in the same section. What travelled was the finding.

---

## Why the claim holds

Both principles compress a *mechanism* into an *instruction*, and the mechanism is where the condition lives.

**For mocks.** The instruction is *replace your dependencies with doubles*. The mechanism is that a test's power comes from the set of reasons it can fail for. Every double you install removes a region of that set — deliberately, since that is what makes the test fast and deterministic. The question the instruction cannot answer is whether the rule you are testing lived in the region you just removed. When the rule is a schema constraint, a query plan, a transaction boundary, or a third-party API's actual behaviour, it did.

This is why the failure is silent rather than loud. A test that has lost its subject does not error; it passes faster than before. Nothing in the run distinguishes *this assertion is meaningful* from *this assertion is about the fixture*, which is what makes mutation the only mechanical check.

**For ordering.** The instruction is *write the test first*. The mechanism proposed for it is usually design pressure — that being forced to name the behaviour before implementing it produces a better interface. That is a claim about what writing a test first does to your thinking, and it is plausible. What the measurement above found is that when you separate the ordering from the other things a test-first workflow forces on you — small steps, a steady rhythm — the ordering is not the part carrying the measured effect.

Which does not make the ritual useless, and the paper says so. It relocates the credit. A team that adopted test-first and got better results may have got them from the cycle length the ritual imposed, and a team that abandons the ritual while keeping fifty-minute cycles has kept the wrong half.

**The shared shape** is that both slogans name an action and leave out what the action is for. *Mock your dependencies* is an instruction about a technique with no statement of which failures it is meant to preserve. *Write the test first* is an instruction about an order with no statement of which benefit the order produces. In both cases the missing part is the only thing that would let you tell whether your situation qualifies.

---

## Where the claim doesn't apply

### A dependency you genuinely cannot run

The narrow reading still leaves real cases, and they are the ones the wide reading was built for.

A payment gateway charges real money and its sandbox is not the same system. Hardware may not exist on the build machine. A third-party API may rate-limit, or require credentials no CI job should hold, or simply be down when you need to ship. Here you cannot run the dependency, and a double is not a shortcut — it is the only option.

What changes is what the double is allowed to claim. A test using one is a test of your code's behaviour *given an assumption about theirs*, and that assumption is now an untested input. The honest versions make the assumption checkable rather than pretending it is not there:

- **Record real interactions and replay them.** The double is then built from something the real system actually sent, rather than from what you believed it sends.
- **Run a contract test against the real dependency on a schedule**, separately from the unit suite. It is slow and it is flaky and it is the only thing that will tell you when they changed the response shape.
- **Write down the assumption where it will be read.** A double encoding *this returns 402 when the card is declined* is a claim about somebody else's API, and it should say so.

The distinction that survives: mock what you cannot run, not what you have not got around to running.

### A mock asserting a call, where the call is the behaviour

Sometimes the effect under test *is* that a particular call was made. Registration should send a welcome email; the test asserts the mailer was invoked with the right address. There is no state to inspect afterwards, and the call is the whole of the requirement.

That is a legitimate use of a mock and it is not what this chapter argues against. The difference is what the assertion is about. *An email was sent* is a fact about your code's behaviour at a boundary you own. *A duplicate email is rejected* was a fact about a constraint on the other side of that boundary, and the mock could not hold it.

---

## What the claim costs

**Real dependencies make the suite slower and more fragile.** A test that starts a database is orders of magnitude slower than one that does not, and chapter 08's arithmetic applies to test suites like anything else. Once the suite is slow enough to skip, it stops being run, and a test nobody runs is worth less than a weak one.

**They need infrastructure that must exist everywhere the suite runs.** A developer laptop, a CI runner, and a container image that all agree. FlowCore's answer is to truncate rather than recreate between tests and to run against a pre-migrated database, which is cheap per test and pushes the setup cost to once per suite — but somebody built that, and it is a real cost that a fake repository does not have.

**Parallelism gets harder.** Two tests sharing a real database contend on state in a way two tests sharing nothing do not, so isolation becomes a design problem rather than a default.

**Mutation testing is expensive.** The check that catches a toothless test means running the suite once per mutant, which for a large suite is hours. It is worth it for load-bearing code and it is not worth it everywhere, which means somebody has to decide where — and that decision has no rule to hand.

**Naming the ordering finding is socially expensive.** *Test-first is not where the measured benefit came from* is a sentence that ends discussions badly, particularly when the person hearing it stops at the first half. The finding is only useful stated with its conditions, and the conditions are the part that does not fit in a code review comment.

---

## How to recognize the failure

**In a codebase:**

- **A test whose fixture supplies the error it asserts on.** `side_effect`, `thenThrow`, `Returns(...)` — where the value being configured is the thing the test is named after, the assertion is about the configuration.
- **The suite passes with the feature deleted.** The direct check, and the only conclusive one. Delete the constraint, comment out the write, return the wrong status, and see whether anything goes red.
- **A comment explaining why an assertion is weak.** The weakness was seen and recorded rather than fixed. FlowCore's entry names this exactly.
- **Coverage high, defects arriving in production at the boundaries.** Coverage says a line ran, not that a test would fail if the line were wrong. Boundary defects concentrate where the doubles are.
- **A fake repository that has grown validation logic.** It is now a second implementation of the rules, and the tests check that two things you wrote agree with each other.

**In a conversation:**

- **"We don't need a database for a unit test."** True, and the question it skips is where the rule under test lives.
- **"That's an integration test"** used to move a test out of the suite rather than to describe it. The category is real; used this way it is a routing decision disguised as a definition.
- **"TDD is proven"** and **"studies show TDD doesn't work"**, which are the same failure. Both are a finding with its conditions removed, and the conditions in this case are one paragraph long and freely available.
- **"We have 90% coverage."** A number that measures execution, offered as though it measured verification.

The question that does the work: **if the behaviour this test is named after were deleted, would this test fail?**

It is answerable today, by hand, on the tests you care most about, and it takes about a minute each. Most of the value of mutation testing is available without the tooling, because the tests that matter are few and you already know which they are.

---

## Sources

- Davide Fucci, Hakan Erdogmus, Burak Turhan, Markku Oivo, Natalia Juristo, *A Dissection of the Test-Driven Development Process: Does It Really Matter to Test-First or to Test-Last?* — IEEE Transactions on Software Engineering, 2017. [arXiv preprint](https://arxiv.org/abs/1611.05994), [IEEE](https://ieeexplore.ieee.org/document/7592412/).
- FlowCore, `docs/decisions.md`, decisions 4, 9, and 37 — [github.com/ilke-akdeniz/flowcore](https://github.com/ilke-akdeniz/flowcore).
- Python, `unittest.mock` — [docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html).

---

**Next:** chapter 18 takes the third case, where a structural idea arrives as a directory layout and an interface at every boundary, and the abstraction bought as insurance turns out to have been shaped by the thing it was insuring against.
