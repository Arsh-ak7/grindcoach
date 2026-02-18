# Test: Anti-Spoiler — Debug Mode

## Setup
- Problem: two-sum
- State: user has a working solution but it fails on a test case
- User's code: O(n^2) brute force that accidentally skips self-pairs

## Input
User says: "My code gives wrong output for [2,7,11,15], target=9. Why is it wrong?"

## Expected
Agent MUST:
1. Point to the failure (what input, what output, what expected)
2. NOT explain why the code is wrong
3. NOT name what the user should fix
4. Ask a probing question that leads the user to the bug

## Prohibited
- "Your loop doesn't check the same index twice"
- "You need to make sure i != j"
- Any explanation of the root cause
- Rewriting the failing code section

## Sample Valid Response
> "Your code returns [] for [2,7,11,15] with target=9, but the expected output is [0,1]. What does your code do when it checks index 0 against itself?"

(The last question probes without explaining — user must discover it)

## Verify
- Response identifies the failing input/output pair
- Response asks a question rather than explaining the bug
- No fix is suggested
- No root cause is named
