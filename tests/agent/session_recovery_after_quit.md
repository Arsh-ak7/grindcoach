# Test: Session Recovery After Abnormal Exit

## Setup
- A previous session was started but not ended cleanly
- .session.json exists with clean_exit: false
- One problem was rated but not logged:
  ```json
  {"slug": "valid-parentheses", "rated": true, "rating": 4, "logged": false}
  ```

## Trigger
User starts a new conversation with Claude Code or Gemini CLI.

## Expected
During /setup or at session start, agent MUST:
1. Run `grind session recover`
2. Read output: "valid-parentheses — rated 4/5 but not logged"
3. Surface this to the user: "Looks like your last session ended without logging valid-parentheses (you rated it 4/5). Want me to log it now?"
4. If user confirms → run `grind log valid-parentheses 4`
5. Then clean up: start fresh session

## Prohibited
- Ignoring the recovery output
- Silently logging without user confirmation
- Losing the hint events from the previous session (flush them first)

## Verify
- grind session recover is called before session start
- User is informed of unlogged work
- grind log is called with the recovered rating
- New session starts cleanly after recovery
