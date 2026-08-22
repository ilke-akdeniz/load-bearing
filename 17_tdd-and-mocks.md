# TDD, Mocks, and What Testing Actually Buys

## The advice

> **Write the test first.**
>
> **Mock your dependencies.**

Two sentences, and they arrive together. This chapter is Part IV's second case and it is kept fair: tests are worth writing, and both practices are worth following in most situations. What is examined is that each travels as a settled default when the literature behind it records a stated purpose for one and an open disagreement about the other.

---

## What the wide reading produces

Take both sentences at face value. Write the test first, and replace what it depends on.

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

---

## What the sources said

Both of those failures come from following the two sentences literally. Both sentences arrive in code review as though they were consensus, and neither is.

**Writing the test first has a stated purpose, and it is not that the order improves the code.** Fowler's definition gives two benefits: self-testing code, and that *"thinking about the test first forces us to think about the interface to the code first."* Beck's own recent minimal statement of the loop says what it is for in terms of confidence — that everything which used to work still works, that the new behaviour works, that the system is ready for the next change. Neither claims the sequence itself makes the resulting code better. That is the claim that travels, and the next section is what happened when somebody measured it.

**Mocking is not a default at all. It is one side of a disagreement with names.** Fowler set them out in 2007 and they have been the vocabulary since:

> The classical TDD style is to use real objects if possible and a double if it's awkward to use the real thing. […] A mockist TDD practitioner, however, will always use a mock for any object with interesting behavior.

He also says which side he is on, and why:

> I don't see any compelling benefits for mockist TDD, and am concerned about the consequences of coupling tests to implementation.

So *mock your dependencies* is the mockist default stated as if it were the only one. The position this chapter argues for — use the real thing where you can run it — is the classical default, and it has had a name for nearly two decades.

Which reframes the registration test above. It is not what happens when someone follows the consensus. It is what happens when one school's *mock by default* approach is applied to a dependency that Fowler and later writers say should be left real.

---

## What the ordering was measured to buy

The ordering has been measured on its own, separately from everything bundled with it, by a study whose title is the question: *A Dissection of the Test-Driven Development Process: Does It Really Matter to Test-First or to Test-Last?*

In it, Fucci, Erdogmus, Turhan, Oivo and Juristo went at it differently. Rather than split people into a TDD group and a control group, they recorded what developers actually did. Thirty-nine professional developers — averaging 7.3 years of Java experience — worked through programming tasks in an IDE recording every action, producing 82 usable data points. Instead of asking *did the TDD group do better*, they broke the work itself into four things they could measure:

```text
 granularity   how long one cycle usually was
 uniformity    how much the cycle length varied
 sequencing    what share of cycles put the test first
 refactoring   how much of the work was refactoring
```

They scored two outcomes: how much of a supplied acceptance suite the finished code passed, and how quickly those assertions were earned. Then they asked which of the four predicted either.

**Sequencing predicted neither.** Cycle length, cycle evenness, and refactoring survived the analysis; the test-first share did not, for quality or for speed. Quality improves by about 14% as the typical cycle falls from around 50 minutes to around 8.

The authors are careful about how much weight that carries, and the chapter should be too. Short cycles and even ones *"go hand in hand, meaning these two characteristics together make a difference. In isolation, they may not be as effective"* — two of the four factor-outcome pairings have coefficients too weak to stand alone. And there is a floor: cutting cycles below the *"often suggested values of five to ten minutes results in little improvement."*

Their own conclusion puts it better than a summary could. The secret of TDD, they write, *"might not be centered on its test-first nature, but rather on its ability to encourage developers to consistently take fine-grained steps, what Kent Beck calls baby steps, provided that they keep writing tests."*

And the corollary they draw is the sharpest sentence in the paper: writing tests last and writing them first *"could be substitutes and equally effective provided that they are performed at the same level of granularity and uniformity."*

Not *the order is irrelevant*. **Two practices are interchangeable once matched on step size — and both of them include writing the tests.**

It travels as *TDD doesn't work* or *the order doesn't matter*. Five things in the paper forbid both readings, three of them in that same closing passage.

**The tests are not the variable.** Every process measured here wrote tests. The comparison is test-first against test-last, never against not testing, and the conclusion says so in the clause that is easiest to drop: *provided that they keep writing tests*.

**The result carries a condition.** Substitutable *"at the same level of granularity and uniformity"* — short steps, of roughly even length, one after another. A team that abandons the ritual and returns to hour-long cycles has changed the thing that mattered rather than the thing that didn't.

**Finding nothing is not finding against.** They looked for a link between the order and the outcomes and got none in either direction. Had writing tests first been actively harmful, more of it would have gone with worse results, and it did not.

**They measured hours, not careers.** The gains may be *"small or uncertain in the short term,"* and a test-first dynamic *"may provide long-term advantages not addressed by or detected in our study"* — they name three: working out what the requirements actually are, forcing design decisions into the open, and getting more tests written at all.

**The cycle it measures is a code change, not a decision.** A cycle here is *"delimited by the successful execution of a regression test suite (the green bar in JUnit),"* and the observed lengths ran from about one minute to forty-nine, median four and a half. So the finding is about how often code comes back green. Applying it to how often anything else should happen — how often you settle an interface, size a queue, choose a storage model — takes a word that was pinned to one unit and resolves it outward to a scope nobody measured. Nobody designs a video pipeline in eight-minute increments, and nothing in this paper says they should.

Two limits of the design, which they also state: it is a single-group study with no control group, and two of the three tasks were artificial rather than representative of professional work. They also report that earlier work — Rafique and Mišić among others — had already speculated that granularity was the thing doing the work, and say these findings support it, so this is not a lone result.

**Read those and the finding is narrower, and more useful, than either slogan.** It does not say the ritual is worthless. It says the ritual's value is in what it makes you do — small steps, evenly sized, with tests — and that you can have that without the ritual, if you actually do it. Which is a harder instruction than either *always write the test first* or *test-first is a myth*, and the only one of the three that tells you what to change on Monday.

This is chapter 15's mechanism — a principle losing its scope — running on a peer-reviewed paper rather than a proverb. The conditions were published beside the finding, by the same authors, in the same section. What travelled was the finding.

---

## What the narrow reading looks like

*Mock your dependencies* does not say what a dependency is. Under the widest reading — anything your unit does not itself compute — the database is a dependency, the clock is a dependency, the file system is a dependency, and so is the other class you wrote last Tuesday. Under a narrow reading, a dependency you must replace is one you **cannot run**: it costs money per call, it needs hardware you do not have, or it belongs to somebody else.

The two readings differ on exactly one thing, and it is the thing this chapter is about: whether the rule you care about lives inside the dependency or outside it.

FlowCore takes the narrow reading and states it as a rule: its tests run against a real Postgres, not a fake. The reason is visible in its schema. Its decision 4 pushes same-definition integrity into composite foreign keys, and decision 9 puts uniqueness — scoped, case-insensitive, length-capped — into constraints. A fake repository would be a second implementation of every one of those rules, written by the same person who wrote the first, agreeing with it by construction, and unable to disagree with the schema when the schema is wrong.

That is the general form. **A test double — a mock, a stub, or a hand-written fake — can only encode the constraints its author already knows about.** The constraints worth testing are the ones somebody will get wrong, and the drift between the real constraint and its stand-in is what costs you.

## Why the wide reading gets taken

Both principles compress a *mechanism* into an *instruction*, and the mechanism is where the condition lives.

**For mocks.** The instruction is *replace your dependencies with doubles*. The mechanism is that a test's power comes from the set of reasons it can fail for. Every double you install removes a region of that set — deliberately, since that is what makes the test fast and deterministic. The question the instruction cannot answer is whether the rule you are testing lived in the region you just removed. When the rule is a schema constraint, a query plan, a transaction boundary, or a third-party API's actual behaviour, it did.

This is why the failure is silent rather than loud. A test that has lost its subject does not error; it passes faster than before. Nothing in the run distinguishes *this assertion is meaningful* from *this assertion is about the fixture*, which is what makes mutation the only mechanical check.

**For ordering.** The instruction is *write the test first*. The mechanism proposed for it is usually design pressure — that being forced to name the behaviour before implementing it produces a better interface. That is a claim about what writing a test first does to your thinking, and it is plausible. What the measurement above found is that when you separate the ordering from the other things a test-first workflow forces on you — small steps, a steady rhythm — the ordering is not the part carrying the measured effect.

Which does not make the ritual useless, and the paper says so. It relocates the credit. A team that adopted test-first and got better results may have got them from the cycle length the ritual imposed, and a team that abandons the ritual while keeping fifty-minute cycles has kept the wrong half.

**The shared shape** is that both slogans name an action and leave out what the action is for. *Mock your dependencies* is an instruction about a technique with no statement of which failures it is meant to preserve. *Write the test first* is an instruction about an order with no statement of which benefit the order produces. In both cases the missing part is the only thing that would let you tell whether your situation qualifies.

**The two are not independent — they arrive as one practice.** What is taught is not an ordering but a loop, run at minutes: write a failing test, make it pass, refactor, repeat. Keeping that loop turning needs a suite that answers in seconds, and *replace the slow dependency with a double* is what usually follows. Worth noting that it does not follow in the canon: Beck's own statement of the loop mentions no mocking, no isolation requirement and no speed requirement anywhere. The bundling is in the teaching rather than in the definition. The median cycle in the study was about eight minutes, and short cycles are the part the evidence credits.

So the ingredient that works is also the ingredient that produces the pressure to mock. The granularity carrying the measured benefit is the same granularity that pushes the database out of the test, and pushing the database out of the test is what produced a test that passes with the constraint deleted.

### Same mechanism, in a shape that escapes the instructions in ever direction

This is the subtle "the test that never reaches its condition." case.

Previous mocked test example at least asserted something. This one asserts nothing about a specific business rule, although the test case looks good until you dig in.

The rule is that the registration leaves an account `pending` until the address is verified. Verfication makes it `active`. Here is the test, and the fixture it runs against:

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

Nothing is mocked here and nothing turns on the order it was written in. It is a third route to the same place, and worth having because it survives every instruction this chapter has given so far.

It passes. It uses a real database, no mock anywhere, and it asserts on state read back afterwards rather than on a call it made.

It also cannot fail, and the reason is in the fixture. `an_account` does not create an account; it writes a row that resembles one, with a status chosen by hand. **The precondition was fabricated rather than established** — and the value fabricated happens to be the value the assertion expects, so `verify` has nothing left to do.

That is this chapter's own subject arriving where nobody invited it. The fixture is standing in for the part of the system that produces a new account, and standing in for it is what removes the reason this test could fail. There is no `Mock` object anywhere; the substitution is a hand-written `insert`.

Gut the method entirely:

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

Changing that one word makes the test work, but it is the smaller fix. The larger one is to stop writing the row by hand and let the system make the account:

```python
def test_status_is_active_after_verifying(self):
    accounts = AccountRepository(a_database())
    registration = Registration(accounts)
    registration.register("ada@example.com")

    registration.verify("ada@example.com")

    self.assertEqual(accounts.status_of("ada@example.com"), "active")
```

The starting status is now whatever registration actually produces, and the test fails the moment `verify` stops working — `AssertionError: 'pending' != 'active'` — with no fixture value that anyone chose, and so none that can go stale against the code.

**This is not a hypothetical shape.** FlowCore hit it, in a workflow fixture that declared one status and pointed both of its terminal actions at it, so a run reported the same status before and after finishing. It was caught the same way: `completeWorkflow` was changed to stamp `completed_at` and never the status columns, and **the entire suite passed**. Its decision 37 records two things worth more than the fix.

The first is the count — it was **the fifth toothless test in one iteration**, meaning the fifth that asserted nothing, and the first mutation used to investigate it was itself broken, so its failure proved nothing until it was repaired. Even the check needed checking.

The second is that the code had said so. A comment sat directly above the weak fixture:

```go
// twoStepDefinition's terminal action ends in its only status
```

The weakness was noticed at the time and written down instead of fixed. The entry's own verdict:

> A comment explaining why an assertion is weak is not a substitute for an assertion that is not.

---

## Where the wide reading is right

Two situations sit outside everything above, and in both the compressed sentence gives the right answer.

### A dependency you genuinely cannot run

The narrow reading still leaves real cases, and they are the ones the wide reading was built for.

A payment gateway charges real money and its sandbox is not the same system. Hardware may not exist on the build machine. A third-party API may rate-limit, or require credentials no CI job should hold, or simply be down when you need to ship. Here you cannot run the dependency, and a double is not a shortcut — it is the only option.

What changes is what the double is allowed to claim. A test using one is a test of your code's behaviour *given an assumption about theirs*, and that assumption is now an untested input. The honest versions make the assumption checkable rather than pretending it is not there:

- **Record real interactions and replay them.** The double is then built from something the real system actually sent, rather than from what you believed it sends.
- **Run a contract test against the real dependency on a schedule**, separately from the unit suite. It is slow and it is flaky and it is the only thing that will tell you when they changed the response shape.
- **Write down the assumption where it will be read.** A double encoding *this returns 402 when the card is declined* is a claim about somebody else's API, and it should say so.

The distinction that survives: mock what you cannot run, not what would merely be inconvenient to run.

Vladimir Khorikov states a sharper version of the same line, and it is worth having because it says *why* rather than *which*. He splits out-of-process dependencies into **managed** — ones you control, such as your own database — and **unmanaged** — ones other systems also reach, such as an SMTP server. Use real instances of the first; replace only the second. The reason:

> Communications with managed dependencies are implementation details; communications with unmanaged dependencies are part of your system's observable behavior.

### A mock asserting a call, where the call is the behaviour

Sometimes the effect under test *is* that a particular call was made. Registration should send a welcome email; the test asserts the mailer was invoked with the right address. There is no state to inspect afterwards, and the call is the whole of the requirement.

That is a legitimate use of a mock and it is not what this chapter argues against. The difference is what the assertion is about. *An email was sent* is a fact about your code's behaviour at a boundary you own. *A duplicate email is rejected* was a fact about a constraint on the other side of that boundary, and the mock could not hold it.

---

## What following the advice costs

**Writing the test first couples the test to a structure being designed as you write it.** The test names an interface before that interface has settled, so it encodes the shape as well as the behaviour. Structural change then costs test change in proportion: add a field and you touch every test that constructs the object, split a class and its tests split with it. This follows from the method rather than being a failure of it — the tests are fine-grained because the loop is, and fine-grained tests attach to the shape of the thing they test.

**The loop is hard to run, and the study shows how hard.** Across all 82 sessions — both arms, test-first and test-last — the highest share of test-first cycles anyone reached was 87.5%, so no session in the study was run purely test-first, and the authors describe the upper quarter as writing test-first *"approximately half of the time."* The third step fares worse: subjects refactored about a third of the time and a quarter of them refactored in under a tenth of their cycles, which the authors call unsurprising because it is what happens in real projects. These were professionals given ten hours of training for it — a five-hour hands-on tutorial on unit testing with JUnit, and five hours on applying TDD — then working observed, on tasks chosen for the purpose. Whatever the discipline costs, it is enough that it is mostly not performed as described.

## What taking the alternative costs

**Real dependencies make the suite slower and more fragile.** A test that starts a database is orders of magnitude slower than one that does not, and chapter 08's arithmetic applies to test suites like anything else. Once the suite is slow enough to skip, it stops being run, and a test nobody runs is worth less than a weak one.

**They need infrastructure that must exist everywhere the suite runs.** A developer laptop, a CI runner, and a container image that all agree. FlowCore's answer is to truncate rather than recreate between tests and to run against a pre-migrated database, which is cheap per test and pushes the setup cost to once per suite — but somebody built that, and it is a real cost that a fake repository does not have.

**Parallelism gets harder.** Two tests sharing a real database contend on state in a way two tests sharing nothing do not, so isolation becomes a design problem rather than a default.

**Mutation testing is expensive.** Catching a test that cannot fail means running the whole suite once for every deliberate break, which for a large suite is hours. It is worth it for load-bearing code and it is not worth it everywhere, which means somebody has to decide where — and that decision has no rule to hand.

---

## How to recognize it

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
- Martin Fowler, *Mocks Aren't Stubs*, 2007 — [martinfowler.com/articles/mocksArentStubs.html](https://martinfowler.com/articles/mocksArentStubs.html).
- Martin Fowler, *TestDrivenDevelopment* — [martinfowler.com/bliki/TestDrivenDevelopment.html](https://martinfowler.com/bliki/TestDrivenDevelopment.html).
- Kent Beck, *Canon TDD*, 2023 — [newsletter.kentbeck.com/p/canon-tdd](https://newsletter.kentbeck.com/p/canon-tdd).
- Vladimir Khorikov, *When to Mock* — [enterprisecraftsmanship.com/posts/when-to-mock](https://enterprisecraftsmanship.com/posts/when-to-mock/).
- Python, `unittest.mock` — [docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html).

---

**Next:** the remaining two cases come from the same doctrine and split along the language.

- **Chapter 18** — a structural idea that arrives as a directory layout, and costs a different amount in every language it is applied to.
- **Chapter 19** — an abstraction bought as insurance, shaped by the thing it was insuring against.
