# CLAUDE.md

@coach_persona.md

This file provides guidance to Claude Code when working with code in this repository.

## What This Is

An AI-powered LeetCode coaching system with a CLI tool (`grind`) that scaffolds and runs solutions in C++, Python, and Java. Solutions live in `problems/<slug>/` with companion `input.txt` files.

## Key Commands

```bash
# First-time setup
grind init

# Create a new problem (creates problems/<slug>/solution.<ext> + input.txt)
grind new <slug> <lang>    # lang: cpp, python, java

# Run a solution (auto-reads from input.txt sidecar if non-empty)
grind run <slug>

# Log a solved problem with self-assessment (writes to memory.md)
grind log <slug> <rating> [--time <minutes>] [--hints <count>] [--topic <topic>] [--difficulty <diff>]

# Browse problem bank (grouped by topic, shows solved/unsolved)
grind list [--track <name>] [--topic <topic>] [--difficulty <diff>]

# View or switch active track
grind track [name]

# Show progress summary (due reviews, streak, track-aware suggestions)
grind progress

# Archive old rows from memory.md to memory_archive.md
grind archive
```

- C++ is compiled with `g++ -std=c++17`
- Python runs with `PYTHONPATH` set to project root
- Java compiles with `utils/java/LcUtils.java` on classpath

## Architecture

- **`grind`** — Python 3 CLI (`init`, `new`, `run`, `log`, `list`, `track`, `progress`, `archive`). Handles scaffolding from templates, compilation, execution, and spaced repetition tracking.
- **`coach_persona.md`** — Shared Socratic coaching persona (imported above). Defines coaching rules, hint progression, and rating scale.
- **`problems.json`** — Problem bank index (Blind 75, NeetCode 150). Navigation only — problem descriptions are fetched live.
- **`memory.md`** — Spaced repetition progress table. Written exclusively by `grind log`. Read by agents and `grind progress`.
- **`templates/`** — Starter files (`cpp.txt`, `python.txt`, `java.txt`) with placeholders.
- **`utils/`** — Language-specific helpers:
  - `cpp/lc_utils.h` — `operator<<` overloads for STL containers, `DBG()` macro, `read_line()`, `parse_vector<T>()`
  - `python/lc_utils.py` — Input parsing utilities, ListNode, TreeNode
  - `java/LcUtils.java` — Data structures and debug helpers
- **`problems/`** — Per-problem folders. Each folder contains `solution.<ext>`, `input.txt`, and optionally `README.md`.

## Conventions

- Problem folders use snake_case derived from the slug: `two-sum` → `problems/two_sum/`
- Solution files: `solution.cpp`, `solution.py`, or `Solution.java`
- C++ solutions include `../../utils/cpp/lc_utils.h` for magic printing (`cout << vector`) and `DBG()` macro
- Never reveal solutions to the user — follow the Socratic coaching method in `coach_persona.md`
