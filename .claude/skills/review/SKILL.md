# /review — Review a Completed Solution

## Arguments
$ARGUMENTS (optional): none

## Instructions

1. **Identify the current problem** the user just solved (from recent context).
2. **Read the solution file** from `problems/<slug>/solution.<ext>`.
3. **Run the solution** to verify it works:
   ```bash
   grind run <slug>
   ```
4. **Discuss the solution** following `coach_persona.md`:
   - Time and space complexity analysis
   - Edge cases: did they handle them? Which ones might they miss?
   - Alternative approaches: what other ways could this be solved?
   - Code quality: any improvements without changing the algorithm?
5. **Ask for self-assessment**: "How would you rate your confidence on this problem? (1-5)"
6. **After the user rates**, log the result:
   ```bash
   grind log <slug> <rating> --time <minutes> --hints <hint_count> --topic <topic> --difficulty <difficulty>
   ```
   - Estimate time from session if the user doesn't specify
   - Use the hint count tracked during the session
   - Infer topic and difficulty from the problem (or look up in `problems.json`)
7. **Report the next review date** from the log output.
