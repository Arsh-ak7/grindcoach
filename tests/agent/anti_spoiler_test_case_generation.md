# Test: Anti-Spoiler — Test Case Generation

## Setup
- Problem: longest-substring-without-repeating-characters
- State: user has some code, asks for a test case

## Input
User says: "Can you give me a test case to try?"

## Expected
Agent MUST:
1. Only use test cases from the problem statement
2. NOT create custom test cases that imply or reveal the algorithm

## Prohibited Examples (must never generate these)
- "Try 'aabc' — what does your code return when the same character appears multiple times?" (implies the sliding window approach)
- "What about an empty string?" (if not in the problem statement examples)
- "Try a string of all unique characters" (implies what the algorithm optimizes for)

## Allowed Examples
- Use Example 1 from the problem: "abcabcbb" → expected output: 3
- Use Example 2: "bbbbb" → expected output: 1
- Use Example 3: "pwwkew" → expected output: 3

## Sample Valid Response
> "Try the first example from the problem: 'abcabcbb'. What does your code output for that?"

## Verify
- Test case matches problem statement examples exactly
- No custom test cases that hint at the algorithm
- No explanation of why the test case is interesting
