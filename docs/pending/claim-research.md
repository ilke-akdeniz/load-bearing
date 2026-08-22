**All four briefs are consumed.** 2026-08-20.

**Numbering note, 2026-08-22.** The chapter that ran on *the database is a detail* was cut (decision 83) and everything after it moved up one. The brief headed *chapter 18* below is that cut chapter; what is now chapter 18 is the one headed *chapter 19*. The table's numbers are current, the headings below are as written.

| Chapter | What the source turned out to say | Landed |
|---|---|---|
| 16 | Riel's 2.9 means one key abstraction split in two, which excludes a rule over two entities; his introduction calls all sixty *warning bells* and was written to avoid the fate of *goto considered harmful* | `9e82683` |
| 17 | *Mock your dependencies* is the mockist half of a disagreement Fowler named in 2007 and came down against; Beck's canon mentions no mocking, isolation or speed at all | `3d04d4c` |
| 18 | Martin separates the data model (*significant*) from the database system (*a detail*), and the 2012 post is about deferring the choice, not hiding it | `dd98ff4` |
| 18 | DIP's test is stability, and stability comes from having many implementations — done before this document | `5a0a324` |

Four for four: the scope was written down every time, and what travelled was the instruction.
Chapter 15's cost section now carries the consequence — the failure is retrieval rather than preservation.
Part IV framing was considered and skipped, at the author's direction.

This file can be deleted, or kept as the record of where the sources were found.

---

We already did this resarch and updated the chapter 18.

I did a sweep of older chapters and found this. Some parts of the claude tags is repetitive but you will get the idea.

chapter 16
[claude after reading this claim again, the statement "does not say where to place behaviour that needs two entities" bugged me. We are treating "Depend on abstractions, not concretions" as a slogan or go proverb with no scope attached, but I believe this one has known reachable scopes. "does not say where to place behaviour that needs two entities" could still be true but maybe we should also look at the scope - shapes of "Behaviour belongs with the data it operates on". That could give better material for current or other chapters. I reached the following pages while doing that.   Take a look  tell me what you think, it could also be worthwhile to explore the material referenced in the pages in a BFS style.

https://eng.libretexts.org/Bookshelves/Computer_Science/Programming_and_Computation_Fundamentals/Book%3A_Object-Oriented_Reengineering_Patterns_(Demeyer_Ducasse_and_Nierstrasz)/09%3A_Redistribute_Responsibilities/9.02%3A_Move_Behavior_Close_to_Data

https://homepages.ecs.vuw.ac.nz/~elvis/db/misc/rules.html

https://softwareengineering.stackexchange.com/questions/234527/zero-behavior-objects-in-oop-my-design-dilemma
]

chapter 17
[claude after reading this claim again, the statement "Neither *write the test first* nor *mock your dependencies* says what it buys." bugged me. We are treating these as a slogan or go proverb with no scope attached, but I believe at least one of these has known reachable scopes. Maybe we should also look at the scope - shapes of these. That could give better material for current or other chapters. I reached the following pages while doing that.   Take a look  tell me what you think, it could also be worthwhile to explore the material referenced in the pages in a BFS style. Attention, I'm pasting many links. I'm not saying that they are all very useful. Those are the ones I just skimmed and I want you to do the same and then go deeper if you find anything of good value for our book.

https://martinfowler.com/bliki/TestDrivenDevelopment.html

https://newsletter.kentbeck.com/p/canon-tdd

https://en.wikipedia.org/wiki/Test-driven_development

https://www.agileinstitute.com/articles/a-dozen-reasons-why-test-first-is-better-than-test-later

https://dev.to/wycliffealphus/the-illusion-of-test-coverage-why-writing-tests-first-is-the-only-real-testing-49pk

https://www.freecodecamp.org/news/dont-write-all-your-software-tests-first-just-write-one/

https://softwareengineering.stackexchange.com/questions/260183/in-tdd-should-i-have-to-write-test-first-or-interface-first

https://www.bagile.co.uk/test-first-approach-sounds-simple-enough-right/

https://stackoverflow.com/questions/23643643/should-i-mock-all-the-dependencies-when-unit-testing

https://enterprisecraftsmanship.com/posts/when-to-mock/

https://hynek.me/articles/what-to-mock-in-5-mins/

https://javascript.plainenglish.io/to-mock-or-not-to-mock-cac9881d37fe
]


chapter 18
[claude after reading this claim again, the statement "The database is a detail" does not say what to do about it." bugged me. We are treating these as a slogan or go proverb with no scope attached, but I believe at least one of these has known reachable scopes. Maybe we should also look at the scope - shapes of these. That could give better material for current or other chapters. I reached the following pages while doing that.   Take a look  tell me what you think, it could also be worthwhile to explore the material referenced in the pages in a BFS style. Attention, I'm pasting many links. I'm not saying that they are all very useful. Those are the ones I just skimmed and I want you to do the same and then go deeper if you find anything of good value for our book.

https://www.oreilly.com/library/view/clean-architecture-a/9780134494272/ch30.xhtml

https://github.com/stride83/Clean-Architecture-zh-1/blob/master/docs/ch30.md

https://blog.cleancoder.com/uncle-bob/2012/05/15/NODB.html

https://www.reddit.com/r/programming/comments/todni/no_db_uncle_bob/

https://journal.optivem.com/p/the-database-is-a-detail

https://www.tonymarston.net/php-mysql/db-is-not-just-an-implementation-detail.html

https://www.reddit.com/r/programming/comments/1k45lwh/critical_clean_architecture_book_review_and/
]