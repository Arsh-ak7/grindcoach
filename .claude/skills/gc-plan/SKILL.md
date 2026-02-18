# /gc-plan — Study Plan View and Management

## Arguments
$ARGUMENTS (optional): [show | today | regenerate | --target <id>]

## Purpose
Display, interpret, and manage the active study plan conversationally.
The agent reads the plan output and explains it — the user never needs to parse raw CLI output.

## Steps

### 1. Show plan
```bash
grind plan show
```
Interpret the output conversationally:
- How many days remain until the interview
- Which topics are front-loaded and why (gap scores drive ordering)
- How many mock sessions are planned
- What today's problems are

### 2. Today's agenda
```bash
grind plan today
```
Walk the user through today's recommended problems:
- Why each problem is scheduled today (gap score, company-reported, SM-2 review)
- Suggest starting: "Ready to start with <slug>? Type /gc-solve <slug> or just say go."

### 3. Regenerate (if user asks to adjust)

If the user wants to regenerate (e.g., interview date changed, new problems added):
```bash
grind plan regenerate
```
Then show the new plan with `grind plan show`.
Explain what changed.

### 4. Gap context

After showing the plan, always show gap context:
```bash
grind gap show
```
Explain the connection: "The plan front-loads DP and graphs because those are your weakest topics based on your SM-2 history."

## Notes

- The plan is generated from SM-2 history, not the resume. Explain this if asked.
- Completed days are preserved on regenerate.
- The user can override gap scores manually: "grind gap set dp weak" — but you run the command, not them.
