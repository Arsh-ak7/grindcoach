# /progress — Show Progress Summary

## Arguments
$ARGUMENTS (optional): none

## Instructions

### 1. Run progress commands
```bash
grind progress
grind plan today
grind behavior summary
```

### 2. Present conversationally

Synthesize all three outputs into a human-readable summary:

**Interview readiness:**
- Company and days until interview (if active target)
- Plan progress (Day N of M, % complete)
- Mock sessions completed vs target

**Today's agenda:**
- What's on today's plan and why
- Any SM-2 reviews due (overdue ones flagged clearly)
- Suggested next action

**Gap analysis:**
- Which topics need work (unknown/weak) — explain what this means in practice
- Which are developing or strong — affirm progress
- "The plan is front-loading <topic> because it's your weakest area based on practice history"

**Behavioral insights (if data exists):**
- If `quick_give_up` on any topic: "You've been getting hints on <topic> faster than your other topics — consider sitting with it longer before asking"
- If `hint_positive` on any topic: "Hints are working well for <topic> — keep asking when you're stuck"
- If `overconfident` on any topic: "You've been rating <topic> higher than your hint usage suggests — worth recalibrating"

### 3. Offer next action

One clear suggestion:
- If SM-2 reviews due → "Want to start with <slug>? It's been N days since you last practiced it."
- If plan has problems today → "Today's first problem is <slug> (<topic>). /solve <slug>?"
- If no plan → "No plan active. Want me to run /setup to get you set up for your next interview?"

## Notes

- Keep the summary encouraging but honest per coach_persona.md
- Never give false praise. Progress is real only if the data shows it.
- Behavioral patterns are observations, not judgements
