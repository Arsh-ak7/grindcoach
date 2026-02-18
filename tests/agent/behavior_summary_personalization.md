# Test: Behavior Summary Drives Coaching Personalization

## Setup
- behavior.jsonl has 15+ hint events for "dp" topic showing:
  - avg time to hint: 3.2 min (quick_give_up flag)
  - hint effectiveness: 45% (below threshold, hint_negative)
- grind behavior summary shows these patterns

## Input
User says: /gc-solve coin-change cpp

## Expected
At session start, agent MUST:
1. Run `grind behavior summary`
2. Internalize: dp topic has quick_give_up + hint_negative
3. Adapt coaching stance for this session:
   - When user is silent → wait LONGER than normal before engaging
   - When user asks for hint → give it (requested) but step FURTHER BACK (hints aren't working)
   - Consider reframing from scratch rather than giving incremental hints

## How to Verify (Behavioral, Not Syntactic)

Trigger: Problem is presented. User says nothing for 5 minutes.

**Pass:** Agent remains completely silent for longer than usual. Does NOT ask "Any questions about the problem?"

Trigger: User says "I'm stuck, can I get a hint?"

**Pass:** Agent gives a STEP-BACK response: "Let's zoom out. What kind of output does this problem ask for? What would a brute force look like?"

**Fail (must not happen):**
- Agent asks "what approaches come to mind?" before user speaks
- Agent gives the next incremental hint immediately without stepping back
- Agent ignores the behavior summary data entirely

## Note
This test verifies that the agent reads and acts on behavior.jsonl data, not just that it runs the command. A pass requires observable behavior change.
