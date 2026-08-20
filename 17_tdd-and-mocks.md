# TDD, Mocks, and What Testing Actually Buys

## The claim

**Neither *write the test first* nor *mock your dependencies* says what it buys. Under the wide reading of each, a mocked dependency puts the rule you meant to test beyond the test's reach, and the benefit credited to writing tests first turns out, when measured, to come from working in small steady steps rather than from the order.**

This is Part IV's second case, and it is kept fair. Tests are worth writing, the two principles below are worth following in most situations, and neither of those is in dispute here. The terms with no fixed extent are what writing the test **first** buys, and what counts as a **dependency**.

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
    # Mock(spec=...) is a stand-in object carrying the same method names as
    # AccountRepository, and none of its behaviour. Nothing here reaches a
    # database.
    accounts = Mock(spec=AccountRepository)
    # side_effect scripts successive calls: the first insert returns None,
    # the second raises. This line is the test author deciding, by hand,
    # that a second insert of the same address fails.
    accounts.insert.side_effect = [
        None,
        sqlite3.IntegrityError("UNIQUE constraint failed: account.email"),
    ]
    registration = Registration(accounts)

    registration.register("ada@example.com")

    with self.assertRaises(DuplicateEmail):
        registration.register("ada@example.com")
```

The mock does not mimic SQLite's constraint. It has no idea a constraint exists. The `IntegrityError` is written into the test.

Nothing about it is lazy. It names the behaviour, it exercises the real `Registration`, it asserts a real exception type. It passes.

Beside it, the same behaviour tested against a real database:

```python
def test_against_the_database(self):
    registration = Registration(AccountRepository(a_database()))

    registration.register("ada@example.com")

    with self.assertRaises(DuplicateEmail):
        registration.register("ada@example.com")
```

Both pass. So far the two look interchangeable, and the mocked one is faster.

Now delete the constraint it is named after from the real database. One word out of the schema:

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

Mocking the database means nothing that happens inside the database is covered. The duplicate rule is enforced in the database. So the mocked test covers only what happens after the insert returns — four lines, in which `Registration` turns an `IntegrityError` into a `DuplicateEmail`. That much is true, and it stays true whether or not any database anywhere would ever raise one.

**A test can only fail for a reason it can reach.** Mocking a dependency removes the reasons that live inside it. What is left is a test of the seam.

### What counts as a dependency

*Mock your dependencies* does not say what a dependency is. Under the widest reading — anything your unit does not itself compute — the database is a dependency, the clock is a dependency, the file system is a dependency, and so is the other class you wrote last Tuesday. Under a narrow reading, a dependency you must replace is one you **cannot run**: it costs money per call, it needs hardware you do not have, or it belongs to somebody else.

The two readings differ on exactly one thing, and it is the thing this chapter is about: whether the rule you care about lives inside the dependency or outside it.

FlowCore takes the narrow reading and states it as a rule: its tests run against a real Postgres, not a fake. The reason is visible in its schema. Its decision 4 pushes same-definition integrity into composite foreign keys, and decision 9 puts uniqueness — scoped, case-insensitive, length-capped — into constraints. A fake repository would be a second implementation of every one of those rules, written by the same person who wrote the first, agreeing with it by construction, and unable to disagree with the schema when the schema is wrong.

That is the general form. **A test double — a mock, a stub, or a hand-written fake — can only encode the constraints its author already knows about.** The constraints worth testing are the ones somebody will get wrong, and the drift between the real constraint and its stand-in is what costs you.

### The test that never reaches its condition

The mocked test above at least asserts something. The more common failure is a test that cannot fail at all, and reading it will not tell you.

Registration leaves an account `pending` until the address is verified, at which point it becomes `active`. Here is the test, and the fixture it runs against:

```python
STARTING_STATUS = "active"   # the fixture's choice


def an_account(email):
    connection = sqlite3.connect(":memory:")
    connection.execute(SCHEMA)
    connection.execute(
        "insert into account (email, status) values (?, ?)", (email, STARTING_STATUS)
    )
    connection.commit()
    return connection


class VerificationActivatesTheAccount(unittest.TestCase):
    def test_status_is_active_after_verifying(self):
        accounts = AccountRepository(an_account("ada@example.com"))
        registration = Registration(accounts)

        registration.verify("ada@example.com")

        self.assertEqual(accounts.status_of("ada@example.com"), "active")
```

It passes. It uses a real database, no mock anywhere, and it asserts on state it read back rather than on a call it made — which is everything this chapter has recommended so far.

It also cannot fail. The fixture creates the account already `active`, so the assertion is satisfied before `verify` is called. Gut the method entirely:

```python
def verify(self, email):
    pass
```

```text
Ran 1 test in 0.000s

OK
```

That is a **mutation**: break the code deliberately and see whether any test notices. This one did not. Change the fixture's one word to `"pending"` and run the same broken code:

```text
AssertionError: 'pending' != 'active'
- pending
+ active

FAILED (failures=1)
```

The test was always this weak. Nothing in the passing run said so, and neither would coverage — the line ran, which is all coverage measures.

**This is not a hypothetical shape.** FlowCore hit it, in a workflow fixture that declared one status and pointed both of its terminal actions at it, so a run reported the same status before and after finishing. It was caught the same way: `completeWorkflow` was changed to stamp `completed_at` and never the status columns, and **the entire suite passed**. Its decision 37 records two things worth more than the fix.

The first is the count — it was **the fifth toothless test in one iteration**, meaning the fifth that asserted nothing, and the first mutation used to investigate it was itself broken, so its failure proved nothing until it was repaired. Even the check needed checking.

The second is that the code had said so. A comment sat directly above the weak fixture:

```go
// twoStepDefinition's terminal action ends in its only status
```

The weakness was noticed at the time and written down instead of fixed. The entry's own verdict:

> A comment explaining why an assertion is weak is not a substitute for an assertion that is not.

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

**Sequencing dropped out of both models.** Granularity, uniformity, and refactoring effort survived; the test-first fraction did not, for quality or for productivity. Shorter cycles helped — the improvement reaches about 14% as median cycle length falls from around 50 minutes to around 8 — and steadier cycles helped.

Their own summary of the practical upshot:

> We think that this aspect should be emphasised over religiously focusing on leading each production cycle with unit tests.

This travels as *TDD doesn't work* or *the order doesn't matter*. Here is what is in the same paper, and mostly in the same paragraph:

> The absence of sequencing as an influential dimension does not imply that a strictly develop-then-test (test-last) strategy should be preferred over a test-first strategy: this advice would require a negative (statistically significant) coefficient, which the models did not produce.

> Our results simply state that the order in which unit tests and production code are written may not be as important as commonly thought so long as the process is iterative, granular, and uniform.

> A test-first dynamic may provide long-term advantages not addressed by or detected in our study.

They name three of those advantages they did not measure: resolving requirements uncertainty, formalizing design decisions, and encouraging writing more tests. And they state two limits of the design: it is a single-group study with no control group, and two of the three tasks were artificial rather than representative of professional work.

**Read the conditions and the finding is narrower and more useful than either slogan.** It does not say the ordering is worthless. It says the ordering is not where the measured benefit came from, that the benefit came from small steady steps, and that this holds *given* a process which is already iterative, granular, and uniform. A team that drops the ritual and goes back to hour-long cycles no longer has such a process, so the finding does not cover them.

Chapter 15's "principle loses scope" mechanism, running on a peer-reviewed paper rather than a proverb. The conditions were published beside the finding, by the same authors, in the same section. What travelled was the finding.

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

The distinction that survives: mock what you cannot run, not what would merely be inconvenient to run.

### A mock asserting a call, where the call is the behaviour

Sometimes the effect under test *is* that a particular call was made. Registration should send a welcome email; the test asserts the mailer was invoked with the right address. There is no state to inspect afterwards, and the call is the whole of the requirement.

That is a legitimate use of a mock and it is not what this chapter argues against. The difference is what the assertion is about. *An email was sent* is a fact about your code's behaviour at a boundary you own. *A duplicate email is rejected* was a fact about a constraint on the other side of that boundary, and the mock could not hold it.

---

## What the claim costs

**Real dependencies make the suite slower and more fragile.** A test that starts a database is orders of magnitude slower than one that does not, and chapter 08's arithmetic applies to test suites like anything else. Once the suite is slow enough to skip, it stops being run, and a test nobody runs is worth less than a weak one.

**They need infrastructure that must exist everywhere the suite runs.** A developer laptop, a CI runner, and a container image that all agree. FlowCore's answer is to truncate rather than recreate between tests and to run against a pre-migrated database, which is cheap per test and pushes the setup cost to once per suite — but somebody built that, and it is a real cost that a fake repository does not have.

**Parallelism gets harder.** Two tests sharing a real database contend on state in a way two tests sharing nothing do not, so isolation becomes a design problem rather than a default.

**Mutation testing is expensive.** Catching a test that cannot fail means running the whole suite once for every deliberate break, which for a large suite is hours. It is worth it for load-bearing code and it is not worth it everywhere, which means somebody has to decide where — and that decision has no rule to hand.

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
- **"That's an integration test, we don't do that"** used to move a test out of the suite rather than to describe it. The category is real; used this way it is filtering disguised as a definition.
- **"TDD is proven"** and **"studies show TDD doesn't work"**, which are the same failure. Both are a finding with its conditions removed, and the conditions in this case are one paragraph long and freely available.
- **"We have 90% coverage."** A number that measures execution, offered as though it measured verification.

The question that does the work: **if this behaviour broke, would this test fail?**

Broken the way code actually breaks, not deleted in the abstract: someone drops the constraint in a migration, someone returns early, someone updates the wrong column. Pick the likeliest one, make that change, run the test, put it back. It takes about a minute, and most of the value of mutation testing is available without the tooling, because the tests that matter are few and you already know which they are.

The wider version is worth asking before a release: **if this behaviour is broken in production tomorrow, can we say the cause is not in our code, because these tests would have caught it?** That one reaches what the narrow question misses — the dependency that is faked in every environment below production, the fixture data that is tidier than anything real. The honest answer is usually more specific, and less comfortable, than a coverage number.

---

## Sources

- Davide Fucci, Hakan Erdogmus, Burak Turhan, Markku Oivo, Natalia Juristo, *A Dissection of the Test-Driven Development Process: Does It Really Matter to Test-First or to Test-Last?* — IEEE Transactions on Software Engineering, 2017. [arXiv preprint](https://arxiv.org/abs/1611.05994), [IEEE](https://ieeexplore.ieee.org/document/7592412/).
- FlowCore, `docs/decisions.md`, decisions 4, 9, and 37 — [github.com/ilke-akdeniz/flowcore](https://github.com/ilke-akdeniz/flowcore).
- Python, `unittest.mock` — [docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html).

---

**Next:** chapter 18 takes the third case, where a structural idea arrives as a directory layout and an interface at every boundary, and the abstraction bought as insurance was in fact shaped by the thing it was insuring against.
