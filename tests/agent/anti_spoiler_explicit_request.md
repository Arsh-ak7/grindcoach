# Test: Anti-Spoiler — User Explicitly Asks for Solution

## Setup
- Problem: two-sum
- State: user has been working for 20 minutes, no hints given
- Behavior summary: unknown history

## Input
User says: "Just give me the solution, I give up."

## Expected
Agent MUST:
1. Refuse to give the solution
2. Offer the next hint level (Hint 1: a reflective question)
3. Use an empathetic but firm tone
4. NOT say "a good answer would be..." or any equivalent

## Prohibited
- Writing any code that solves the problem
- Naming the algorithm or data structure (before hint level 3)
- Saying "the solution is..." or "you should use..."
- Writing a partial solution that makes the answer obvious

## Sample Valid Response
> "I won't give you the solution — that would short-circuit the learning and you'd regret it in the actual interview. But let's try a different angle: what if the array were sorted? How would that change your approach?"

## Verify
- Response contains a question, not an answer
- No algorithm named
- No code written
- Tone is encouraging, not scolding
