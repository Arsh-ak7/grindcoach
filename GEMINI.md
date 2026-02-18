# GEMINI.md

@./coach_persona.md

This file provides guidance to Gemini CLI when working with code in this repository.

## What This Is

An AI-powered LeetCode coaching system with a CLI tool (`grind`) that scaffolds and runs solutions in C++, Python, and Java. Solutions live in `problems/<slug>/` with companion `input.txt` files.

## Key Commands

```bash
# First-time setup
grind init

# Core
grind new <slug> <lang>                                          # Scaffold a problem (cpp, python, java)
grind run <slug>                                                 # Compile and run (reads input.txt)
grind log <slug> <rating> [--time <min>] [--hints <n>]          # Log with SM-2 spaced repetition
grind list [--track <name>] [--topic <t>] [--diff <d>]          # Browse problem bank
grind track [name]                                               # View or switch active track
grind progress                                                   # Gap scores + behavioral patterns
grind archive                                                    # Archive old memory rows

# Target management
grind target add --company <name> --role <title> --date <YYYY-MM-DD> [--url <url>] [--lang cpp|python|java]
grind target list
grind target active [id]
grind target remove <id>
grind target show [id]
grind target update <id> --field <field> --value '<json_or_string>'
grind target merge <id1> <id2>                                   # combined/hybrid/separate

# Resume
grind resume set --path <path> [--profile '<json>']             # Agent parses, passes JSON
grind resume show
grind resume clear

# Session (hint event tracking)
grind session start [--target <id>]
grind session event <slug> <event_type> [--data '<json>']
grind session end                                                # Flushes hint events → behavior.jsonl
grind session recover                                            # Detect unlogged work

# Behavioral analytics
grind behavior summary                                           # Read at session start
grind behavior report [--topic <t>] [--slug <s>]
grind behavior export
grind behavior reset [--force]

# Gap analysis
grind gap show
grind gap set <topic> <weak|strong|unknown>

# Study plan
grind plan generate [--target <id>]
grind plan show [--target <id>]
grind plan today [--target <id>]
grind plan regenerate [--target <id>]

# TTS
grind speak "<text>" [--rate <wpm>]                             # macOS: say | Linux: espeak-ng
grind reset [--force]                                           # Wipe ALL user data and start fresh
```

- C++ is compiled with `g++ -std=c++17`
- Python runs with `PYTHONPATH` set to project root
- Java compiles with `utils/java/LcUtils.java` on classpath

## Architecture

- **`grind`** — Python 3 CLI. Zero external dependencies. All subcommands: init, new, run, log, list, track, progress, archive, target, resume, session, behavior, gap, plan, speak, reset.
- **`coach_persona.md`** — Shared Socratic coaching persona (imported above). Defines coaching rules, hint progression, anti-spoiler rules, and rating scale.
- **`AGENTS.md`** — Canonical agent config with full CLI reference and dual-agent compatibility matrix.
- **`problems.json`** — Problem bank index (Blind 75, NeetCode 150). Navigation only — descriptions fetched live.
- **`memory.md`** — Spaced repetition progress table. Written atomically by `grind log`. Source of truth for gap analysis.
- **`.lc_config.json`** — User config: active track, active target, targets, resume, gap_overrides. Gitignored.
- **`.session.json`** — Ephemeral session state with hint events. Deleted on clean exit. Gitignored.
- **`behavior.jsonl`** — Append-only hint event log. Flushed from session by `grind session end`. Gitignored.
- **`templates/`** — Starter files with placeholders.
- **`utils/`** — Language-specific helpers for C++, Python, and Java.
- **`problems/`** — Per-problem folders. Each folder contains `solution.<ext>`, `input.txt`, and optionally `README.md`.

## Conventions

- Problem folders use snake_case derived from the slug: `two-sum` → `problems/two_sum/`
- Solution files: `solution.cpp`, `solution.py`, or `Solution.java`
- Never reveal solutions to the user — follow the Socratic coaching method in `coach_persona.md`
