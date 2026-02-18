# Test: Hint Escalation — No Level Skipping

## Setup
- Problem: course-schedule
- State: user has received Hint 1 (reflective question)
- User responds: "I still don't get it, can I have another hint?"

## Input
User says: "I still don't understand. Can I get another hint?"

## Expected
Agent MUST:
1. Give Hint Level 2 — category hint ("well-known pattern for this constraint structure")
2. NOT jump to Hint Level 3 (technique), 4 (structural), or 5 (walkthrough)
3. Log: `grind session event course-schedule hint_given --data '{"level":2,...}'`
4. Verify user genuinely attempted Hint 1 before proceeding (ask if needed)

## Prohibited
- Skipping to "use topological sort" (Level 3)
- Drawing the algorithm structure (Level 4)
- Walking through an example (Level 5)
- Repeating the same Level 1 question without progress

## Sample Valid Response
> "There's a well-known pattern for problems where you need to detect circular dependencies in a directed graph. Does that category ring any bells?"

(Category hint — no technique named yet)

## Verify
- Hint level is exactly 2
- Technique not yet named
- grind session event level=2 logged
