# /hint — Get a Progressive Hint

## Arguments
$ARGUMENTS (optional): none

## Instructions

### 1. Identify current problem and hint count

From recent context, identify the slug of the problem the user is working on.
Track the hint count for this problem in the current session.

### 2. Note the time elapsed

Estimate how long the user has been on this problem (from session context or timestamps).
Record `time_to_hint_min` — this is behavioral signal.

### 3. Deliver the hint

Follow the progression from `coach_persona.md`. Each level requires the user to have genuinely attempted the previous level first. Never skip ahead.

| Level | Type | Rule |
|-------|------|------|
| 1 | Reflective question | Must be a question. Never a statement. Does NOT name algorithm. |
| 2 | Category hint | May name the technique ONLY after level 1 was asked and user responded. |
| 3 | Technique hint | Names the specific pattern (e.g. "two pointers"). |
| 4 | Structural hint | Describes data structure layout or loop invariant. |
| 5 | Walkthrough | Steps through a small example, still asking questions. |

**Never say:** "You should use X approach" or "The trick is..."
**Always say:** "What happens if you think about it as X?" or "What if the input were Y?"

### 4. Log the hint event immediately
```bash
grind session event <slug> hint_given --data '{
  "hint_level": <n>,
  "hint_concept": "<what the hint was about in 2-4 words>",
  "time_to_hint_min": <minutes_since_problem_presented>,
  "hints_so_far": <count_before_this_hint>
}'
```

This must happen immediately after giving the hint. Do not defer.

### 5. Ask a follow-up question

After giving the hint, ask one question to check understanding:
"Does that reframing help? What does it suggest to you?"

Do not say more than this. Wait for the user's response.

### 6. Assess hint effectiveness (2+ turns later)

After the user has had 2 or more turns to respond to the hint, assess whether it helped:
- Did the user make visible progress?
- Did they ask for another hint immediately (suggests it didn't help)?
- Did they start writing code in a different direction?

Then log:
```bash
grind session event <slug> hint_assessed --data '{
  "hint_level": <n>,
  "effective": <true|false>,
  "reasoning": "<one sentence: what happened after the hint>"
}'
```

## Anti-spoiler rules for hints

- **Hint 1**: Must be a question, never a statement
- **Hint 2**: May name the technique category ONLY if level 1 was given and user responded
- **Never**: Say "you should use X approach" — always frame as "what happens if you..."
- **Never**: Reveal the algorithm name before hint level 3
- **Never**: Give the full solution, even at hint 5
- **If user asks directly for the answer**: Refuse. Offer the next hint level instead.

## Calibration reminder (from behavior model)

- `quick_give_up` on this topic → you waited less than 5 min before hinting; note this pattern
- `hint_negative` on this topic → hints aren't effective; after hint 2, consider stepping further back instead
- `chronic_hint` on this topic → flag for gap analysis and rating calibration
