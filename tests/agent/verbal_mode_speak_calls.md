# Test: /mock --verbal — grind speak Called at Key Points

## Setup
- macOS environment (or Linux with espeak-ng available)
- Active target: BMW SWE
- /mock --verbal triggered

## Expected Sequence

1. `grind session event <slug> mock_started --data '{"round_type":"technical","verbal":true}'`
2. `grind speak "<problem statement>"` — problem is read aloud, not shown as text
3. Silence for 5 minutes (agent does not type anything visible)
4. `grind speak "Can you walk me through your approach so far?"`
5. User responds verbally / types response
6. `grind speak "Sounds interesting. Keep going."` (or similar)
7. After solution complete: `grind speak "Walk me through your solution as if I'm reading it for the first time."`
8. Verbal explanation evaluated (clarity, complexity stated, data structures named)
9. /review flow (with speak calls for prompts)

## Prohibited
- Writing the problem statement as text without calling grind speak
- Skipping the verbal explanation step
- Speaking more than short prompts (not narrating long coaching commentary)

## Verify
- grind speak called at: problem presentation, mid-check, solution walkthrough request
- Verbal evaluation criteria noted in review: correctness of naming, complexity stated, explanation structure
- grind log called at end (same as regular /mock)
