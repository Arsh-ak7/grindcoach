# Test: Hint Level 1 Must Be a Reflective Question

## Setup
- Problem: coin-change
- State: user has been stuck for 8 minutes, asks for /gc-hint
- No previous hints given

## Input
User types: /gc-hint

## Expected
Agent MUST:
1. Give a Hint Level 1 — a reflective question only
2. The question must nudge without revealing the technique
3. Log the event: `grind session event coin-change hint_given --data '{"level":1,...}'`
4. NOT name the algorithm
5. NOT say "this is a dynamic programming problem"

## Prohibited
- Naming the algorithm (DP, memoization, BFS, etc.)
- Structural hints (e.g., "maintain a dp array of size amount+1")
- Any statement that reveals the category

## Sample Valid Response
> "What would happen if you already knew the minimum coins needed for all amounts smaller than the target? How could you use that?"

(This nudges toward DP without naming it)

## Verify
- Response is phrased as a question
- No algorithm name used
- grind session event logged (if session is active)
- Hint count in session incremented to 1
