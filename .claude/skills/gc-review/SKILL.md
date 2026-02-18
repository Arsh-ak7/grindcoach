# /review — Review a Completed Solution

## Arguments
$ARGUMENTS (optional): none

## Instructions

### 1. Identify the current problem

From recent context, identify the slug of the problem just solved.

### 2. Read and run the solution
```bash
grind run <slug>
```
Read the solution file at `problems/<slug_underscored>/solution.<ext>`.

### 3. Discuss the solution (post-solve — full analysis now allowed)

- Time and space complexity analysis
- Edge cases: did they handle them? Which ones might they miss?
- Alternative approaches: what other ways could this be solved?
- Code quality: any improvements without changing the algorithm?

This is the ONLY time you can discuss algorithms openly — the user has already solved it.

### 4. Ask for self-assessment

"How would you rate your confidence on this one? (1–5)"

Reference the rating scale from coach_persona.md:
- 1: Could not solve without significant help
- 2: Solved with multiple hints
- 3: Solved with minor hints, some struggle
- 4: Solved mostly independently
- 5: Solved quickly and confidently

Wait for the user's rating.

### 5. Calibration check (IMPORTANT)

Check the hint count from the session:
```bash
grind session event <slug> rating_calibration --data '{
  "self_rating": <user_rating>,
  "hint_count": <hints_used>,
  "expected_rating_from_hints": <derived_below>
}'
```

Expected rating from hints:
- 0 hints → expected 4–5
- 1 hint  → expected 3–4
- 2 hints → expected 2–3
- 3+ hints → expected 1–2

If `self_rating - expected_rating > 1`, surface a calibration question (not a correction):
> "You used 2 hints — our 4 usually means under 1 hint, mostly independent. Does 3 feel more accurate?"

If they maintain their rating, accept it. You asked once.

### 6. Log immediately — do not defer
```bash
grind log <slug> <rating> --time <minutes> --hints <hint_count> --topic <topic> --difficulty <difficulty>
```

**Immediate logging rule:** Log before continuing the review discussion. Do not wait for a natural break. Log first, then discuss next steps.

Then record the session event:
```bash
grind session event <slug> logged --data '{"rating": <rating>}'
```

### 7. Report next review date

From the grind log output, report when SM-2 schedules the next review:
"Next review: <date> — that's in <N> days."

### 8. Ask for plan check

```bash
grind plan today
```

If more problems are scheduled for today, offer: "You've got <slug> next on today's plan. Ready?"
