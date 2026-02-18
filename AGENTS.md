# AGENTS.md — Canonical Agent Configuration

This is the canonical agent configuration for `leet-coach`. It defines the shared coaching persona, CLI interface, and conventions that all AI agents (Claude Code, Gemini CLI, or any compatible agent) should follow.

## Persona

@coach_persona.md

## CLI Reference

`grind` is the CLI tool. Zero external dependencies — Python 3 only.

### Commands

```bash
grind init                          # First-time setup
grind new <slug> <lang>             # Scaffold a problem (cpp, python, java)
grind run <slug>                    # Compile and run (reads input.txt automatically)
grind log <slug> <rating>           # Log with SM-2 spaced repetition
  [--time <min>] [--hints <n>]
  [--topic <topic>] [--difficulty <diff>]
grind list                          # Browse active track
  [--track <name>] [--topic <t>] [--difficulty <d>]
grind track [name]                  # View or switch tracks
grind progress                      # Summary with due reviews and suggestions
grind archive                       # Archive old memory rows
```

### Architecture

- **`grind`** — Python 3 CLI. Handles scaffolding, compilation, execution, SM-2 tracking.
- **`coach_persona.md`** — Shared Socratic coaching persona. The rules that govern agent behavior.
- **`problems.json`** — Problem bank index (Blind 75, NeetCode 150). Navigation only — no problem content stored.
- **`memory.md`** — Spaced repetition progress table. Written by `grind log`, read by agents and `grind progress`.
- **`templates/`** — Starter files for C++, Python, Java with placeholders.
- **`utils/`** — Language-specific helpers (STL printing, debug macros, data structures).
- **`problems/`** — Per-problem folders (gitignored, user data). Each contains `solution.<ext>`, `input.txt`, optionally `README.md`.

### Conventions

- Problem folders use snake_case: `two-sum` → `problems/two_sum/`
- Solution files: `solution.cpp`, `solution.py`, or `Solution.java`
- C++ solutions include `../../utils/cpp/lc_utils.h` for magic printing and `DBG()` macro
- Never reveal solutions — follow the Socratic coaching method
- The problem bank is guidance, not a gate. Any LeetCode URL works.

### Agent Skills / Commands

All agents should support these commands:

| Command | Description |
|---------|-------------|
| `/solve <slug-or-url> [lang]` | Start a new problem with Socratic coaching |
| `/hint` | Get a progressive hint (escalating difficulty) |
| `/review` | Review completed solution, discuss complexity, log progress |
| `/mock [--topic X] [--difficulty Y]` | Timed mock interview session |
| `/progress` | Show progress summary with track-aware suggestions |

### Rating Scale

| Rating | Meaning |
|--------|---------|
| 1 | Could not solve without significant help |
| 2 | Solved with multiple hints |
| 3 | Solved with minor hints, some struggle |
| 4 | Solved mostly independently |
| 5 | Solved quickly and confidently |
