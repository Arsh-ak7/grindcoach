# Test: Rating Calibration Question Surfaces on Divergence

## Setup
- Problem: word-break
- State: user received 3 hints (levels 1, 2, 3)
- Session has hint_events for all 3 hints logged
- Expected rating from hints: ~2 (multiple hints)

## Input
User says: "I think I'd rate that a 4 — I mostly got it myself."

## Expected
Agent MUST:
1. Surface the calibration question before logging
2. Ask something like: "You used 3 hints, which usually suggests a 2 — what felt independent to you?"
3. Log: `grind session event word-break rating_calibration --data '{"self_rating":4,"hint_count":3,"expected_rating_from_hints":2}'`
4. Accept user's final rating (user can override) and log with that rating
5. THEN run `grind log word-break <final_rating> --hints 3`

## Prohibited
- Logging without surfacing the calibration question when divergence > 1
- Overriding user's final decision — they may have good reasons for their rating
- Skipping the grind session event call

## Sample Valid Response
> "You used 3 hints, which typically corresponds to a rating of 2. What part of the solution did you feel you got independently? (You can absolutely keep your rating of 4 — I just want to make sure it reflects your actual experience.)"

## Verify
- Calibration question appears before logging
- grind session event rating_calibration called
- grind log called with user's FINAL chosen rating
- grind session event logged called after grind log
