Contextual Programming

Most practical chapter of the book. Out of the standard "claim, why it holds" format. 

The "culmination" of the book in practical terms with largest scope. We don't shy from making statements here.

This chapter is the answer to: "This book is nice and deep but how do we use any of that knowledge daily?"

Ideas
Where following all the claims in the book cad lead us logically regarding software development lifecycle, architecture - design best practices.

So we are defining in scope something similar to "Agile, DDD, TDD" etc...

It could be in the format of go proverbs. "When X do Y" and 2-3 paragraph explanation and examples. 

---

Software forces: concurrency, ...
Human forces: team size, individual skills, budget, risks

Human and software forces should shape your software development and team processes.

Agile is Overrated.

Dailies, retros usually turn into pure ceremonies.

Corporate culture is pure ceremony: 1:1, performance review

A senior engineer is not necessarily someone who worked in the company for 10 years.

Architecture is not diagrams or tach stack choices, it's about clarifying ownership, trade-offs, forces...

---

People are not cogs, you can't swap them easily.
Why context switch is brutal (handovers, project switch)

Time estimates are harmful games.
If your estimate looks successful usually these happened:
- You largely over estimated the task, finished it quickly then slacked or filled the remaining with useless work.
- You didn't consider the forces properly. The task looks done but you will spend "estimate x n time" for fixing bugs or covering gaps in the near future.

Pointing sessions are theater
Nobody in the meeeting has read the tickets.
Even if they read, most team members can't gauge the trade-offs, traps from a ticket text.
---

What to do?

#Contextual Programmin in Practice
Let's be honest, this is an utopia, nobody works in this ideal state of this book's. But an utopia is worth having if reaching even pieces of it could be useful.

##Somebody assesses the human forces at the beginning and then periodically.
That's what great managers, project managers, lead ... usually do. The title doesn't matter. Those are the people that makes a project feel so smooth, clients happy and team members "motivated". Motivated is a loaded word but we use it as the opposite of "not motivated". People become unmotivated when the surprises that result from a bad reading of the forces keep on coming: "We will do X, plan change our focus is Y, client actually doesn't want Y, we are low on budget for Y..."   

##Somebody assesses the software forces.
Again at the bebinning and then peridically.
That's usually the architect, senior engineer...

In both cases, assessing the forces requires a good grasp of laws, context, and ...  

Somebody is a very important word, not a comittee, not the "Team".

Live Meetings 
Zoom, slack. Socially good to meet every week maybe but every day is theatre.

Anybody who makes statements about a software without using it should be respectfully ignored:
- Advice about fixing a bug by someone who didn't reproduce or observe the bug.
- Design - Architecture documents created by a person who just followed the happy path.  

---
Artifact Mapping
Trace artifacts of contextual programming (CP) backwards to get heuristics for team and processes.
We move down from the end result to prerequisites. Empty line moves one level down, bullets are on the same level.

final artifact: 
software that is right for your context, resilient to your force oscillations: force in both meanings: human forces and software forces

- code that adheres to business rules reflecting principles, idioms that match the forces
- records of business rules, forces, principles, trade-offs, decisions

- creating above code and records
- maintaining above code and records

- heuristics that faciliate creation and maintenance.       

leaves:
- Unclear ownership kills CP (contextual programming.) Owner should be clear before every step.

Clarifying forces, principles, taking decisions is hardwork with serious consequences. Ownership provides two mechanisms:
    - Recognizes that the task is important, and that the owner needs time to work on it. 
    - Recognizes that the owner is expected to have the most context on this task and as a result will have more authority.

Contrast this with: 
"Team is responsible for designing feature X." 
"How much time should I spend on the design? Well I shouldn't spend an afternoon, I'm working on a high priority ticket." 
"I know feature X very well and I can come up with a good design."
"Nah I'll not do that, others will oppose to my design without any good reasons and It will be rejected anyway, why waste my time..." 

Typical owners: X manager, ...

Artifact: Who owns what, with what responsibilities and authorities. 
Ex: ...

- Business rules, invariants are the root from which everything flows. A clarification of these is the next step.
Sometimes that produces a one page document, sometimes 100 pages and sometimes one paragraph. Page count should reflect the actual rules and invariants that apply to your context and not the verbosity or prose style of the author or the vibes of the team. "We are an agile team" is not an excuse to start the development of medical scanning software with only a vague idea of what it does. 

Typical owners: 

Artifact ex:

- Assess two force types: human, software
Sometimes that assesment takes days, sometimes an hour and sometimes that's nearly instant, instinctual check.
Examples: large feature, medium feature, quick bugfix but instinctual check still does the work.

Typical owners: 

Artifact ex:

- A meaningful estimate can only be made at this point. And it's ideally not a time estimate but a complexity estimate.
Ex: A new mobile reporting module with following business rules, forces is similar in complexity to the mobile booking feature we did. I would say a medium complexity for our team. When timeline is mandatory: The mobile booking was completed in 1 months, if we encounter similar constraints in the road with similar team availability this could take be completed with a comparable timeline. (Thoese similarities are almost guaranteed to break at some point, but this an honest and diplomatic response to point on the fleeing nature of the time estimate.)   

- Derive the principles that apply
Derive the principles, the idioms can be left to the devs depending on their skills or more guidance about them can be provided on the spot.

Typical owners: 

Artifact ex:

- Enforce the styles as a convention and be done with them quickly.

Typical owners: 

Artifact ex:

Artifacts shown here are guidance, showing what could be worthy of creating in an hypothetical average sitiation. Don't treat not using the same format or not having the artifact as blasphemy.   

---
Process Flows
This is a small catalogue of process shapes that look reasonable for different forces.

- Meetings are for clarifications.
. Use only to unblock specific problems
. Shedule and keep short (10 minutes)
. Not for learning, or discovering things
(source, no need to verify the source now: https://youtu.be/oUP96WnpOsI?t=299)

Ex: meeting subject, what's accomplished on the meeting...

You would never need clarifications periodically at the same time, recurring meetings should be very rare and the reason for them should be articulated honestly:
Ex: We meet every week with cameras open for 15 minutes to connect socially. We believe this improves...

- Stages of development, ownership boundaries, transitions, deliverables, playbooks should be clear for everybody.
This is not about CI or builds that does this or that automatically. None of that matters if when the development ends and qa starts is not clear. Or who gets paged when a critical production issue is found and what that person does is unkown.

Typical Owners:
Ex artifact:

---

Knowing the Utopia doesn't mean you should chase it completely like Don Quichote but, trying the reach one part at a time strategically is a worthy goal. 

Apply what you can to your individual work, try to influence others respectfully when it matters and save your energy if a situation is hopeless. And remember that diplomacy is often more valuable then a head-on war.

---
To consider later: Book's title need probably a change. I can't see how "load bearing" is relevant or central to the book anymore. Some ideas to explore: Force Reading, Contextual Programming, Laws - Forces - Principles, Flow With the Force