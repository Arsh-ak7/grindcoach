# /behavioral — Behavioral Interview Coaching

## Arguments
$ARGUMENTS (optional): [--company <name>] [--competency <ownership|ambiguity|impact|collaboration|...>]

## Purpose
Run a behavioral interview coaching session calibrated to the target company and user's resume context.
Apply STAR rubric through questions, not lectures. Never write the user's answer for them.

## Steps

### 1. Load context
```bash
grind target active
grind resume show
```
Extract: company values, behavioral themes from intelligence, seniority from resume, behavioral_context.

### 2. Select competency

If `--competency` was given, use it.
Otherwise pick from company's `behavioral_themes` (from intelligence). Rotate — never repeat in same session.

If no intelligence data exists, use universal competencies: ownership, impact, collaboration, growth, conflict-resolution.

### 3. Generate question

Craft a question calibrated to:
- Company values (e.g. BMW: "Responsibility, Trust, Openness" → ownership + cross-functional)
- User seniority (senior: strategic scope; junior: individual contribution)
- Specific competency requested

**Example (BMW, senior, ownership):**
> "Tell me about a time you owned an initiative end-to-end where you had no formal authority over the people involved. What was the outcome?"

Present the question. Say nothing else. Wait.

### 4. Listen and probe

After the user responds, silently evaluate against the STAR rubric:
- **Situation**: Is it specific? Is the stakes/context clear?
- **Task**: Is the user's personal role clear? (not "we did")
- **Action**: Are the actions concrete and personal? (not vague)
- **Result**: Is there a measurable outcome? Did they reflect on learning?

Do NOT give a rubric summary. Instead, probe with follow-up questions:
- If Situation is vague: "Can you give me more context on what was at stake?"
- If Task is unclear: "What specifically were you responsible for in that situation?"
- If Action is generic: "Walk me through exactly what you did on day one."
- If Result is missing: "What was the measurable impact? How did you know it worked?"

### 5. Calibrate to seniority

- **Senior/staff**: Expect strategic scope, business impact, cross-team influence. Probe on influence without authority.
- **Mid**: Expect clear personal ownership. Probe on decision-making.
- **Junior**: Expect honest framing of contribution. Probe on learning.

### 6. Wrap up

After 2–3 probing exchanges, offer brief feedback on structure (STAR adherence), not on content.

> "Your Situation and Action were clear. The Result felt a bit general — in a real interview, a specific metric or outcome would land better. Want to try again or move to another competency?"

## Anti-spoiler rules for behavioral coaching

- NEVER write or co-write the user's answer
- NEVER say "a good answer would be..."
- NEVER provide a template answer to fill in
- Probe through questions only
- Coach on structure, not on what to say
