# /solve — Start a New Problem

## Arguments
$ARGUMENTS: <slug-or-url-or-description> [lang]

- First argument: One of three formats:
  1. **LeetCode slug** (e.g. `two-sum`) — looks up in `problems.json`, fetches from LeetCode
  2. **LeetCode URL** (e.g. `https://leetcode.com/problems/valid-parentheses/`) — works for ANY problem
  3. **Inline description** — user pastes a problem description directly
- Second argument (optional): Language — `cpp`, `python`, or `java`. Defaults to active target's `preferred_language`, then `cpp`.

## Instructions

### 0. Session and behavior setup (before anything else)

Check if a session is running. If not:
```bash
grind session start
```

Read the behavior model for this session:
```bash
grind behavior summary
```
Internalize the output. Adjust your coaching stance:
- `quick_give_up` on a topic → wait longer before engaging after silence
- `hint_positive` → hints are effective; honor requests promptly
- `hint_negative` → hints aren't helping; step further back when asked
- `overconfident` → ask calibration question after user provides self-rating
- `chronic_hint` → treat topic as more critical in today's plan

Read active target for language and seniority context:
```bash
grind target active
grind resume show
```
Use `preferred_language` from target (or resume signal) as default language if not specified.
Use `seniority_estimate` from resume to calibrate patience:
- `senior`/`staff` → strict silence; no scaffolding hints
- `mid` → silence; shorter patience
- `junior` → silence; offer "Any questions about the problem?" slightly sooner

### 1. Determine input mode

- If argument is a URL (`https://`): extract the slug from the path
- If argument looks like a slug (lowercase-with-dashes, no spaces): use directly
- Otherwise: treat as an inline description

### 2. Look up metadata

If slug mode: look up in `problems.json` for topic, difficulty, LC number.

### 3. Fetch problem description

Fetch from `https://leetcode.com/problems/<slug>/` using WebFetch.
If blocked, try `https://algo.monster/liteproblems/<number>` as fallback.
Skip for inline descriptions.

### 4. Scaffold the problem
```bash
grind new <slug> <lang>
```

### 5. Edit the solution file (CRITICAL)

Read the scaffolded solution file from `problems/<slug_underscored>/solution.<ext>`.
Replace the `TODO` placeholder with:
- **Exact method signature** from LeetCode (function name, parameter types, return type)
- Body: `// TODO` comment only — no solution logic, no hints, no algorithm names
- Replace test cases in `main` with one working example from the problem

Do NOT write any solution logic.

### 6. Write a README.md

In `problems/<slug_underscored>/README.md`:
- Problem title and difficulty
- Problem description (cleaned from web fetch)
- Example inputs/outputs
- Constraints

### 7. Check memory.md

Has the user attempted this problem before? If so, mention it briefly.

### 8. Record session event
```bash
grind session event <slug> presented
```

### 9. Check plan context
```bash
grind plan today
```
Note internally if this problem is on today's plan (affects urgency framing in review).

### 10. Present the problem (Socratic rules — coach_persona.md)

Show: problem statement, constraints, one example. Nothing else.
Optionally: "Any questions about the problem?"
**Stop. Wait. Say nothing more.**

The user's first words reveal their understanding. Do not pre-empt this.

## Anti-spoiler rules (enforced at all times)

- NEVER name the algorithm or data structure before the user mentions it
- NEVER say "this is similar to X problem"
- NEVER provide hints about approach, pattern, or technique upfront
- NEVER offer preemptive encouragement like "this one's tricky"
- If the user asks for the solution directly: refuse, offer /hint instead

## Example
```
/solve two-sum cpp
/solve https://leetcode.com/problems/binary-watch/ python
/solve <user pastes problem description>
```
