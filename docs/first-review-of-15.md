claude I checked the primary source for chapter 15, Pike's talk at Gopherfest.

#I' m pasting below important timestamps and my comments:

https://youtu.be/PAAkCSZUG1c 
"but they carry a lot of information... so if you see this thing on the board, I know what happens if I have this position because I can create a Co and It may or may not be a good thing"

- Definitely he is not talking about proverbs in the usual sense. That just happens to be the name of the Japanese "go game" book with "proverbs" in the title but the author meant something very specific on that book with the word "proverb" and Pike chases the same meaning.

from https://youtu.be/PAAkCSZUG1c?t=165     to https://youtu.be/PAAkCSZUG1c?t=211
really understanding what a [proverb] says is a fairly big deal because you have to understand what you means by...so ther's actually a lot behind there

---
important failure on your part: The example - context he gives for "don't communicate by sharing memory" is totally different then the one you assume in the book.

In the beginning of the chapter you say: "Channels orchestrate; mutexes serialize.

**The condition was published beside the proverb, by the same person, on the same afternoon.**" 

You ignored the conditions of the "don't communicate ...." proverb, then you assumed that another proverb Pike presents: "channels orchestrate; mutexes serialize" is a condition of the "don't communicate" which is not, it's just another proverb with other conditions.

---

https://youtu.be/PAAkCSZUG1c?t=344
"the really important thing about go's interfaces is the culture around them that's capture by this proverb, the smaller the interface is the more useful it is"

---

# A page describing a "go game proverb" in great detail: https://senseis.xmp.net/?SenteGainsNothing
List  of the proverbs, pay attention to the introduction and to the categorization:  https://senseis.xmp.net/?GoProverbs

---

https://youtu.be/PAAkCSZUG1c?t=873
"Clear is better than clever"
A very general proverb. "It's philosophical point but it really is part of the go philosophy"

---

https://youtu.be/PAAkCSZUG1c?t=970
"errors are values"
This is an interesting one as Pike says "beginners struggle with why do I have to type  iferr != nil all the time"
Then tells about a dev complaining about this: "he just wasn't writing programs, he was writing code, they're not the same. ... he wasn't thinking about errors as values and programming to good effects"
This again show's me why a proverbs target audience is not beginners if we agree that a beginner in any language is still in the stage of writing code. 

---

https://youtu.be/PAAkCSZUG1c?t=1223
"I think you know them [proverbs] already. Think bout them as ideas you might use to explain to somebody why seomthing... you may be in a code review or when you're teaching someone new about something..."

---

https://youtu.be/PAAkCSZUG1c?t=1280
"You also want them [proverbs] to be general. Some of them are specific about a particular thing but there are kind of thins that almost every example should have an example in somewhere of what that prover represents."

Pay attention Pike's explanation of "General" above.

---

https://youtu.be/PAAkCSZUG1c?t=1320
"but also they might be contradictory you know... and that's ok too because sometimes one engineering decision is right sometimes it's exact opposite is the right thing "

---

#my comments follow

Those "proverbs" I actually short "titles, slogans" to remember advice ranging from applies most of the time to applies for a very specific context.
I'm gonna guess that the chapter's claim for the mechanism could be: Principle becomes a movement because the context get's lost in the transmission over time, and a principle without it's conditions sounds like general advice. 

Very important failure of the chapter: Title is "How a Principle Becomes a Movement", Nothing on it shows a concrete example of that process. Which principle stated on the chapter became a movement? How? What's the name of the movement? How do we prove that it originated from that principle?

Maybe the title should be: "How a Principle Becomes a Folk Remedy"
Folk Remedy: An advice applied to a much wider context then it was conceived for and often results in negative outcomes.
Ex: "drink at least 2 litres of water a day". 
Does this apply for everybody? How is this anymore useful than drinking water when you are thirsty?
What if I'm a sedentary small person working in an office and drinking lots of coffee, should I force myself to finish 2 litre additional water everyday. (This sounds absurd but there are many people who do exactly this because they believe in the folk remedy.)

Pike's mistake is saying that the proverbs are helpful for the beginners. The original go game book says the proverbs are for intermediate players. I agree with the game book. It could be that Pike's concept of beginner is different than ours if he is grading the skills relative to his skills. My understanding is that most beginners deal with basic issues like: "What the heck is a channel? How do I try and catch exceptions on Go..." When they see the proverb "Channels orchestrate; mutexes serialize" even if they tried to reach for the context around it they wouldn't be able to grasp the meaning yet. 

And maybe some part of the mechanism is that a beginner, trying to find his way around those "proverbs" or more generally similar "slogans", interprets it in a more generalized way. As the years pass it becomes a habit and a belief packaged as a principle. And then those habits and beliefs that are share by many people sometimes become a movement. By then, it's too late to detect this, show the provenance and the evolution and undo the damage completely.

---

We should add something in claude.md to prevent this failure mode happening again. Something similar to: "For the chapter's important claims, read the original primary source in it's full first. Second hand accounts or inferences made from partial leadings are misleading. If you can't find the primary source say so, offer alternatives and halt. Also key sources need author reading, provide the links at the end of the prompt response as 'Must be read by author before chapter is marked as draft' . Never combine primary sources, original words of a person and secondary sources or derivations silently and then present them as the original words or thesis of the authors. If you have to do the combination, always make the gap and assumptions explicit."

---

#Foreword and a sample "proverb" from the book Pike refers as inspiration "Go Proverbs Illustrated": 

Anyone who has played the old game of “proverbs” will
remember such sayings as “Even a stone will soften a bit
if you sit on it for three years”, or “He studies Heaven
through the eye of a needle”, or “Even Buddha’s smile will
fade if you go begging to him three times in a row”. These
old sayings in colloquial language teach in a vivid and easy
way a rough and ready philosophy of life and essential
points of conduct even better perhaps, than profound and
difficult lectures on sacred scriptures.
In Go also there are many such proverbs, for instance:
“Six will die, eight will live”, or “Strike at the waist of
the knight’s move”, or “The most urgent play for my
opponent is the most urgent play for me”.
This book is a collection of such short expressions which
compress into a few words measures applicable to the infinite variety of occurrences on the go-board and hand down
from the past broad hints for the discovery of winning plays
and combinations (tesuji), useable in innumerable cases. I
have also added some of my own, adapted to forms arising
in actual play and all are extensively illustrated and explained by means of diagrams.
Unlike other works, although it may be taken for light
reading, a single phrase may be worth ten games of teaching, and whatever you learn will be immediately useful in
actual play regardless of your strength or weakness. I hope
that those interested in the subject will enjoy reading this
book.
Kensaku Segoe

“SIX DIE EIGHT LIVE”
AND “FOUR DIE SIX LIVE”
A player crawls along on the second line in order to
make eyes rather than to take territory, since stones in
that position are of less value in capturing territory than
the opponent’s stones that shut them in from the outside.
However, such play may not be considered unprofitable
when the question of the life and death of the stones is
involved.
The saying “Six die, eight live” refers to those cases
where a row of six stones on the second line would die if
left as they stand, but could live if the row were extended
to eight stones.
The saying “Four die, six live’ refers to the similar
cases where a player has a base in the corner and a row
of stones on the second line that would die if there were
only four of them, but that could live if there were six in
the row.
+44) 44-+8OOO +4441 @88000 ce DIAGRAM 1
DIAGRAM 1 Since six stones will die while eight can
live on the second line the six White stones in this diagram
are dead just as they stand.
aDIAGRAM 2
DIAGRAM 2 Even if White 1-is played downward, by
the exchange of White 3... Black 4, White’s space for
making eyes is so narrowed that his group is simply dead.
Since this is the most fundamental life-or-death formation
no doubt this is quite clear.
4th +@@000e00000 iettt DIAGRAM ear 3 fttt CEL rt
QOOOOOOO008+
DIAGRAM 3 Since there are eight White stones on the
second line in this case, they are alive just as they stand.
DIAGRAM 4
DIAGRAM 4 Even if Black tries to narrow White’s
space with Black 1 and 3, White’s reply with White 2
and 4 produces the basic formation with four eyes in a
row so that the White group is alive.
ex Of =DIAGRAM 5
e
|
++
DIAGRAM 5_ This shows the intermediate case where
there are seven stones in a row on the second line. The
result is that if White plays first his stones can live, but
if Black plays first the White group will die. That is, if
White plays first, White 1 and 3 produce the live formation
of four eyes in a row.
HEE tte+ @@eeeeeee DIAGRAM tp tt 6 tt tf
ETFO QO000Q08 +--+
—— 64-08-20
DIAGRAM 6 If Black plays first, Black 1 and 3 so
narrow White’s room for making eyes that after White
4 Black kills the White stones with Black 5.
DIAGRAM 7 DIAGRAM 7 If the stones
tar on the second line have a base
oeece _|_| in the corner, then four will
OOO0C+
Seae es
die but six can live.DIAGRAM 8 DIAGRAM 8 The White
| aa EY | stones cannot live even if White
_| | | ~~ plays first since Black 2 will
ave kill them.
SCO The importance of the
L@—a) _|. corner can be seen in the fact
that if more than four stones
in a row have a base there they have a chance to live,
while on the side the number of stones must exceed six
for this to be true.
DIAGRAM 9 DIAGRAM 10
poe pot
eee eee eoccce_.
SOOO eT Poo e
DIAGRAM 9 These White stones are alive because
they have a base in the corner. This is an example where
six in a row are alive.
DIAGRAM 10 Even if Black attacks with Black 1,
White 2 gives White four eyes in a row.
On the side, six are dead but eight will live, and seven
in a row will live or die depending on who plays first,
but in the corner this is true of five stones in a row.

---