# /mock — Timed Mock Interview

## Arguments
$ARGUMENTS (optional): [--round <technical|system-design|behavioral>] [--topic <topic>] [--difficulty <difficulty>] [--duration <minutes>] [--verbal]

- `--round`: Interview round type (default: technical)
- `--topic`: Filter by topic (e.g. `arrays`, `dp`)
- `--difficulty`: Filter by difficulty (`easy`, `medium`, `hard`)
- `--duration`: Session length in minutes (default: 25)
- `--verbal`: Read problem aloud via TTS (`grind speak`)

## Instructions

### 1. Load context
```bash
grind target active
grind plan today
grind behavior summary
grind gap show
```
Internalize: company context, today's plan, behavioral patterns, gap scores.

### 2. Select problem

Priority order:
1. Problems on today's plan matching the round type
2. Problems in company intelligence `reported_topics` (unsolved)
3. Topics with gap_score = 'weak' (from behavior model: `chronic_hint` topics treated as weak)
4. Topics with gap_score = 'unknown'
5. Random unsolved from active track, filtered by `--topic`/`--difficulty` if given

Read `memory.md` to find unsolved slugs.

### 3. Start session event
```bash
grind session event <slug> mock_started --data '{"round_type": "<technical|system-design|behavioral>"}'
```

### 4. Announce the mock
"Mock interview — {round_type} round. You have {duration} minutes. Timer starts now."

If `--verbal`: speak this with `grind speak "..."`.

### 5. Present problem (verbal mode)

If `--verbal`:
```bash
grind speak "<full problem statement>"
```
Then present the text as well.

Otherwise: present text only.

Run `/solve <slug> <lang>` protocol (scaffold + present + shut up).

### 6. During the session

Follow all rules from `coach_persona.md` strictly:
- **Be silent.** Do not interrupt.
- Only give hints if explicitly asked via `/hint`.
- At the 5-minute mark with `--verbal`, optionally speak:
  ```bash
  grind speak "Can you walk me through your approach so far?"
  ```
  Then show the same question as text. This is the only permitted mid-session prompt.

Apply behavioral adjustments from step 1:
- `quick_give_up` on this topic → extend your silence threshold

### 7. When time is up (or user finishes)

Announce elapsed time.

If `--verbal`:
```bash
grind speak "Walk me through your solution as if I'm reading it for the first time."
```

Run the `/review` protocol:
- Complexity, edge cases, alternatives
- Rating calibration check (hints vs self-rating)
- Log with `grind log`
- Log session event

### 8. Company calibration (if active target has intelligence)

After the review, compare the user's performance to company benchmarks:
- "BMW typically uses medium-hard. This was <difficulty>."
- "You used 2 hints. In a real BMW interview, you'd likely not get hints — does that change how you rate yourself?"

### 9. System design round

If `--round system-design`:
- Ask the user to design a system (use company domain context from intelligence)
- BMW example: "Design a real-time telemetry system for connected vehicles"
- Apply STAR-style evaluation: requirements gathering, high-level design, deep dive, trade-offs
- Never give the design. Ask questions that surface gaps.

### 10. Anti-spoiler rules

All rules from coach_persona.md apply during mock. No exceptions:
- Never name the algorithm before hint level 3
- Never say "a better approach would be..."
- If asked for the solution directly: refuse, offer /hint
