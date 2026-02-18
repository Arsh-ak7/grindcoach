# Test: Review — Immediate Logging Before Discussion

## Setup
- Problem: number-of-islands
- State: user has a working solution, 1 hint was given
- User initiates /review

## Input
User says: "Okay I think it works! /review"

## Expected
Agent MUST:
1. Review the solution briefly
2. Ask for self-rating
3. User gives rating: "I'd say a 3"
4. IMMEDIATELY run: `grind log number-of-islands 3 --hints 1`
5. Confirm: "Logged. Next review: <date>."
6. ONLY THEN continue with complexity discussion, alternatives, etc.

## Prohibited
- Discussing time/space complexity before logging
- Discussing alternative approaches before logging
- Asking clarifying questions about the solution before logging
- Any delay between rating confirmation and grind log call

## Sequence (strict order)
1. `/review` triggered
2. Agent: brief code review
3. Agent: "How would you rate this? (1-5)"
4. User: "3"
5. Agent: [immediately runs grind log] ← THIS STEP CANNOT BE SKIPPED OR DELAYED
6. Agent: "Logged. Next review in X days."
7. Agent: "Now let's talk about complexity..."

## Verify
- grind log is called before any complexity discussion begins
- grind session event logged called after grind log
- Output confirms next review date
