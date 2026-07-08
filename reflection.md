# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
User:
1. Track tasks
2. Register Pet
3. Create Schedule


- Briefly describe your initial UML design.

My early UML design was kinda more complicated then what it needed to be. It didn't exactly fit criteria of actions I put for each class.
- What classes did you include, and what responsibilities did you assign to each?
There is the four classes of Owner, Pet, Task, Scheduler.

Owner:
Attributes:
Time Availability 
Owner Preferences
Methods:
Add pet
Add task to schedule

Pet:
Attributes:
Name
Type of Breed (it should be tied to needs)
Their needs (diet, meds, enrichment)
Methods:
Assigned to said task on the schedule



Task:
Attributes:
What type of task it is
Methods:
First priority: Specific to the pets need 
Second priority: Owner Preferences


Scheduler:
Attributes:
What schedule it is
Methods:
Creates a plan
Includes explanation for the plan
Fits the task due to time availability
Reminds the owner


**b. Design changes**

- Did your design change during implementation?
Yes.
- If yes, describe at least one change and why you made it.
I made many changes and one the which is I simplified the priority of the task.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
time, priority and preferences
- How did you decide which constraints mattered most?
I decided tha time and priority would matter the most because the owner time avaibility really depends on the schedule they are able to care for their pet 
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
It doesn't really consider preferences that much
- Why is that tradeoff reasonable for this scenario?
Because its based on the time and makes it easier for the owner to follow the schedule
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
Brainstorming and debugging
- What kinds of prompts or questions were most helpful?
Asking what the problem with the errors so I could figure out how to later prompt on how to fix them.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
There was one ai suggestion that made the schedule button which made it worse then before and I didn't like how it made it complicated
- How did you evaluate or verify what the AI suggested?
I looked at the details the Ai suggested and see what it removed and added and test it.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
priotization, conflict detection, bug lookup, sorting, recurring tasks
- Why were these tests important?
Because it ensure the function works as intended and doesn't crash. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
4/5
- What edge cases would you test next if you had more time?
Flitering tasks would be very important to test
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I im proud part of function where I added the pets and it worked properly for different pets.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?


**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
