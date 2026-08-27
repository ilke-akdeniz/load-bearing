Contextual Programming

Most practical chapter of the book. Out of the standard "claim, why it holds" format. 

Ideas
Where following all the claims in the book leas us logically regarding software development lifecycle, architecture - design best practices.

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

software that is right for your context, resilient to your force oscillations: force in both meanings: human forces and software forces
    V
code that adheres to business rules reflecting principles, idioms that match the forces
    V                                                                       
records of business rules, 
forces, principles, trade-offs, decisions
    V                               V                 V
processes for creating these     processes for maintaining these
                           \     /
                            \   /
                            



---
Book's title need probably a change. I can't see how "load bearing" is relevant or central to the book anymore.