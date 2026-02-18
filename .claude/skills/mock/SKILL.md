# /mock — Timed Mock Interview

## Arguments
$ARGUMENTS (optional): [--topic <topic>] [--difficulty <difficulty>] [--time <minutes>]

- `--topic`: Filter by topic (e.g. `arrays`, `dp`, `trees`)
- `--difficulty`: Filter by difficulty (`easy`, `medium`, `hard`)
- `--time`: Session length in minutes (default: 25)

## Instructions

1. **Load the problem bank** from `problems.json` and the active track from `.lc_config.json`.
2. **Read `memory.md`** to find which problems have been solved.
3. **Pick a random unsolved problem** from the active track, optionally filtered by topic/difficulty. If no unsolved problems match, pick a problem due for review instead.
4. **Start the session:**
   - Announce: "Mock interview — you have {time} minutes. Timer starts now."
   - Run `/solve <slug> <lang>` to scaffold and present the problem.
   - Note the start time.
5. **During the session:**
   - Follow all rules from `coach_persona.md` strictly.
   - **Be silent.** Only respond when the user speaks.
   - Only give hints if explicitly asked via `/hint`.
   - If the user finishes early, proceed to review.
6. **When time is up** (or user finishes):
   - Announce time elapsed.
   - Run `/review` to discuss the solution.
   - Ask for self-rating and log with `grind log`.
7. **Keep it realistic** — this simulates an actual coding interview. No hand-holding.
