# /hint — Get a Progressive Hint

## Arguments
$ARGUMENTS (optional): none

## Instructions

1. **Identify the current problem** the user is working on (from recent context).
2. **Track the hint count** for this problem in the current session. Increment it each time `/hint` is called.
3. **Deliver a hint** following the progression from `coach_persona.md`:
   - **Hint 1:** Restate the key constraint or ask about the search space.
   - **Hint 2:** Name the technique or pattern category.
   - **Hint 3:** Give a concrete sub-step or partial approach.
   - **Hint 4+:** Walk through a small example step by step.
4. **Never give the full solution**, even at hint 4+. Guide, don't solve.
5. After giving the hint, ask a follow-up question to check understanding.
