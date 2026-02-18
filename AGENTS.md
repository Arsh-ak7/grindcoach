# AGENTS.md — Canonical Agent Configuration

This is the canonical agent configuration for `grindcoach`. It defines the shared coaching persona, CLI interface, and conventions that all AI agents (Claude Code, Gemini CLI, or any compatible agent) should follow.

## Persona

@coach_persona.md

## CLI Reference

`grind` is the CLI tool. Zero external dependencies — Python 3 only.

### Commands

**Core (unchanged):**
```bash
grind init                                              # First-time setup (agent runs, not user)
grind new <slug> <lang>                                 # Scaffold a problem (cpp, python, java)
grind run <slug>                                        # Compile and run (reads input.txt automatically)
grind log <slug> <rating> [--time <min>] [--hints <n>] # Log with SM-2 spaced repetition
grind list [--track <name>] [--topic <t>] [--diff <d>] # Browse problem bank
grind track [name]                                      # View or switch tracks
grind progress                                          # Enhanced: gap scores + behavioral patterns
grind archive                                           # Archive old memory rows
```

**Target management:**
```bash
grind target add --company <name> --role <title> --date <YYYY-MM-DD> [--url <url>] [--lang cpp|python|java]
grind target list
grind target active [id]
grind target remove <id>
grind target show [id]
grind target update <id> --field <field> --value '<json_or_string>'  # nested: --field intelligence.rounds
grind target merge <id1> <id2>                          # Computes overlap, classifies combined/hybrid/separate
```

**Resume:**
```bash
grind resume set --path <path> [--profile '<json>']    # Agent parses resume, passes extracted JSON
grind resume show
grind resume clear
```

**Session (hint event tracking + recovery):**
```bash
grind session start [--target <id>]
grind session event <slug> <event_type> [--data '<json>']
  # event_type: presented | hint_given | hint_assessed | rating_calibration | mock_started | logged
grind session end                                       # Flushes hint events → behavior.jsonl, clean close
grind session recover                                   # Detect unlogged work after abnormal exit
```

**Behavioral analytics:**
```bash
grind behavior summary                                  # User model: patterns by topic (agent reads at session start)
grind behavior report [--topic <t>] [--slug <s>]       # Detailed hint history
grind behavior export                                   # Markdown report
grind behavior reset [--force]                          # Clear behavior.jsonl
```

**Gap analysis:**
```bash
grind gap show                                          # Per-topic: unknown/weak/developing/strong
grind gap set <topic> <weak|strong|unknown>             # Explicit override
```

**Study plan:**
```bash
grind plan generate [--target <id>]                    # Build plan from SM-2 history + company intelligence
grind plan show [--target <id>]                        # Display with progress
grind plan today [--target <id>]                       # Today's problems
grind plan regenerate [--target <id>]                  # Rebuild preserving completed days
```

**TTS:**
```bash
grind speak "<text>" [--rate <wpm>]                    # macOS: say | Linux: espeak-ng | Windows: PowerShell
```

### Architecture

- **`grind`** — Python 3 CLI. Zero external dependencies. Handles scaffolding, compilation, execution, SM-2, sessions, behavior analytics, gap analysis, study plans.
- **`coach_persona.md`** — Shared Socratic coaching persona. The rules that govern agent behavior.
- **`problems.json`** — Problem bank index (Blind 75, NeetCode 150). Navigation only — no problem content stored.
- **`memory.md`** — SM-2 progress table. Written atomically by `grind log`. Read by agents and `grind progress`. Source of truth for gap analysis.
- **`.lc_config.json`** — User config: active track, active target, targets, resume, gap_overrides. Written by grind. Gitignored.
- **`.session.json`** — Ephemeral session state. Accumulates hint events during session. Deleted on clean exit. Used for recovery. Gitignored.
- **`behavior.jsonl`** — Append-only hint event log. Flushed from `.session.json` by `grind session end`. Source of truth for user behavioral model. Gitignored.
- **`templates/`** — Starter files for C++, Python, Java.
- **`utils/`** — Language-specific helpers (STL printing, debug macros, data structures).
- **`problems/`** — Per-problem folders (gitignored). Each contains `solution.<ext>`, `input.txt`, optionally `README.md`.

### Conventions

- Problem folders use snake_case: `two-sum` → `problems/two_sum/`
- Solution files: `solution.cpp`, `solution.py`, or `Solution.java`
- C++ solutions include `../../utils/cpp/lc_utils.h` for magic printing and `DBG()` macro
- Never reveal solutions — follow the Socratic coaching method
- The problem bank is guidance, not a gate. Any LeetCode URL works.

### Agent Skills / Commands

All agents support these commands. The agent orchestrates everything — users type commands in natural language, never in terminal.

| Command | Description |
|---------|-------------|
| `/gc-setup [--resume <path>] [--jobs <url,...>]` | **NEW** Full onboarding: resume + targets + plan in one command |
| `/gc-solve <slug-or-url> [lang]` | Start a problem with Socratic coaching + session tracking |
| `/gc-hint` | Progressive hint with behavioral event logging |
| `/gc-review` | Review solution, rating calibration, immediate logging |
| `/gc-mock [--round X] [--verbal]` | Company-calibrated mock interview |
| `/gc-progress` | Progress summary with gap analysis + behavioral patterns |
| `/gc-plan [show|today|regenerate]` | **NEW** Study plan view and management |
| `/gc-behavioral [--company X] [--competency Y]` | **NEW** Behavioral interview coaching |
| `/gc-research [--company X]` | **NEW** Fetch and synthesize company interview intelligence |

### Dual Agent Compatibility Matrix

| Operation | Claude Code | Gemini CLI | Notes |
|-----------|------------|------------|-------|
| Read file | `Read` tool | Shell `cat` or file read | Both read resume natively |
| Fetch 1 URL | `WebFetch(url, prompt)` | `web_fetch` with URL | Output format differs; both sufficient |
| Fetch N URLs | N sequential `WebFetch` calls | Single `web_fetch` (up to 20) | **Gemini is faster for `/gc-research`** |
| Run terminal | `Bash` tool | `run_shell_command` | Both call `grind` commands |
| Write config | Via `grind` CLI only | Via `grind` CLI only | Never write .lc_config.json directly |
| Agent context | `CLAUDE.md` auto-loaded | `GEMINI.md` auto-loaded | Both import `coach_persona.md` |

**Key rule:** All stateful writes go through `grind`. Neither agent writes to `.lc_config.json`, `memory.md`, `.session.json`, or `behavior.jsonl` directly. This is the compatibility guarantee.

### Slug Naming Convention

User-facing / LeetCode canonical: **hyphens** → `two-sum`
Internal folders / Java packages: **underscores** → `two_sum`

The conversion is transparent via `slug_to_folder()` inside `grind`. Users always type and see hyphens. Underscores are an implementation detail required for Java package name validity and Python import paths. This is a deliberate design decision, not a bug.

### Rating Scale

| Rating | Meaning |
|--------|---------|
| 1 | Could not solve without significant help |
| 2 | Solved with multiple hints |
| 3 | Solved with minor hints, some struggle |
| 4 | Solved mostly independently |
| 5 | Solved quickly and confidently |
