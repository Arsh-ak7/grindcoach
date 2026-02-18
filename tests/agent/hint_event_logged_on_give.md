# Test: Hint Event Logged Immediately When Hint is Given

## Setup
- Active session running
- Problem: binary-search
- User requests /hint (first hint)

## Expected Sequence (strict order)

1. Agent decides on Hint Level 1 content
2. Agent runs: `grind session event binary-search hint_given --data '{"level":1,"concept":"search space","time_to_hint_min":<actual_time>,"hints_so_far":0}'`
3. Agent presents the hint to the user

## Critical Constraint
The `grind session event hint_given` call MUST happen BEFORE the hint text is shown to the user (or at minimum in the same turn, not a later turn).

## After 2+ Turns
Agent evaluates effectiveness:
- If user made progress: `grind session event binary-search hint_assessed --data '{"hint_level":1,"effective":true,"reasoning":"User began narrowing search space"}'`
- If user is still stuck: `hint_assessed` with `"effective":false`

## Prohibited
- Giving the hint without logging the event
- Logging the event many turns later (stale time data)
- Logging hint_assessed on the same turn as hint_given (must wait for evidence)

## Verify
- hint_given event appears in .session.json hint_events after /hint
- time_to_hint_min is reasonable (> 0)
- hint_assessed logged only after observing user's response
