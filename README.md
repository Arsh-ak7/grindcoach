# grindcoach

**Your AI coding coach that never gives you the answer.**

An open-source, CLI-native LeetCode coaching system that uses AI agents (Claude Code or Gemini CLI) as Socratic tutors — not answer machines. Built-in spaced repetition, curated problem tracks, and timed mock interviews.

> Meta, Google, and others now allow AI tools in coding interviews. The question isn't whether to use AI — it's whether you've trained *with* AI in a way that builds real problem-solving skill. That's what grindcoach does.

## 30-Second Quickstart

```bash
git clone https://github.com/YOUR_USERNAME/grindcoach.git
cd grindcoach

# Open Claude Code or Gemini CLI, then:
/gc-setup
```

Full onboarding in one command. The agent runs everything — resume parsing, job description analysis, study plan generation. You don't type a single terminal command.

Or skip setup and go straight to a problem:

```bash
/gc-solve two-sum cpp
```

No pip install, no API keys, no config files. Just Python 3 and an AI agent.

## How It Works

```
You ←→ AI Agent (Claude Code / Gemini CLI)
          ↕
      coach_persona.md    ← Socratic rules: never reveal answers
          ↕
        grind CLI          ← Everything deterministic (Python 3, zero deps)
          ↕
      problems.json        ← Curated tracks (Blind 75, NeetCode 150)
      memory.md            ← SM-2 spaced repetition schedule
      behavior.jsonl       ← Your hint history and behavioral patterns
      .lc_config.json      ← Targets, plan, gap scores
```

The AI agent follows strict coaching rules:
- **Present the problem, then shut up.** Wait for you to think first.
- **Never volunteer hints.** Only when you ask, and even then, progressively.
- **Never give the answer.** Guide with questions, not solutions.
- **Never skip hint levels.** Each hint earned, not handed out.

The `grind` CLI handles everything deterministic — scaffolding, compilation, SM-2 math, session tracking, plan generation, gap analysis. The AI handles everything that needs judgment — coaching, hints, behavioral interviews, company research.

## Commands

### Agent Commands (in Claude Code or Gemini CLI)

| Command | What it does |
|---------|-------------|
| `/gc-setup [--resume <path>] [--jobs <url,...>]` | Full onboarding: resume + targets + study plan |
| `/gc-solve two-sum cpp` | Scaffold + coach through any problem |
| `/gc-solve <leetcode-url> python` | Works with ANY LeetCode problem, not just the bank |
| `/gc-hint` | Progressive hint (question → category → technique → structural → walkthrough) |
| `/gc-review` | Solution review + rating calibration + immediate logging |
| `/gc-mock [--topic dp] [--verbal]` | Timed mock interview, optionally spoken aloud |
| `/gc-behavioral [--company Google]` | STAR behavioral coaching calibrated to company values |
| `/gc-research [--company BMW]` | Fetch + synthesize company interview intelligence |
| `/gc-plan [show|today|regenerate]` | Study plan: what to work on and why |
| `/gc-progress` | Gap scores + behavioral patterns + today's agenda |

### CLI Commands (all run by the agent — you rarely type these directly)

```bash
grind init                                                 # First-time setup
grind new <slug> <lang>                                    # Scaffold a problem
grind run <slug>                                           # Compile and run
grind log <slug> <rating> [--time] [--hints]               # Log with SM-2
grind list [--track X] [--topic Y] [--diff Z]              # Browse problem bank
grind progress                                             # Gap scores + patterns
grind target add --company <n> --role <r> --date <d>       # Add interview target
grind target merge <id1> <id2>                             # Combine prep tracks
grind session start / end / recover                        # Session tracking
grind behavior summary                                     # Behavioral coaching model
grind gap show / set <topic> <weak|strong>                 # Gap analysis
grind plan generate / show / today                         # Study plan
grind speak "<text>"                                       # TTS (macOS/Linux/Windows)
grind behavior reset [--force]                             # Clear behavior event log
grind reset [--force]                                      # Wipe all user data and start fresh
```

## Problem Bank

Two curated tracks included, with more coming:

| Track | Problems | Focus |
|-------|----------|-------|
| **Blind 75** | 75 | Classic interview prep essentials |
| **NeetCode 150** | 150 | Comprehensive topic coverage |

**The bank is guidance, not a gate.** Any LeetCode URL works with `/gc-solve`. The bank just helps with "what should I do next?"

## Architecture

```
grindcoach/
├── grind                 # CLI tool (Python 3, zero external deps)
├── coach_persona.md      # Socratic coaching rules + anti-spoiler rules
├── problems.json         # Problem bank index (Blind 75, NeetCode 150)
├── CLAUDE.md             # Claude Code agent config
├── GEMINI.md             # Gemini CLI agent config
├── AGENTS.md             # Canonical agent config (any agent)
├── templates/            # Starter files (C++, Python, Java)
├── utils/                # Language helpers (STL printing, debug macros)
├── .claude/skills/       # Claude Code slash commands (9 skills)
├── .gemini/commands/     # Gemini CLI commands (9 commands, parity)
└── tests/                # 79 unit tests + agent red-team test suite
```

**User data (gitignored — never committed):**
- `problems/` — Your solutions
- `memory.md` — Your SM-2 spaced repetition schedule
- `.lc_config.json` — Targets, plan, gap overrides
- `.session.json` — Ephemeral session state (deleted on clean exit)
- `behavior.jsonl` — Your hint history and behavioral patterns

**Key design rule:** All stateful writes go through `grind`. The agent never writes to config files directly. This is what makes it agent-agnostic.

## Why Not Just Use ChatGPT?

| | grindcoach | Raw ChatGPT/Claude | LeetCopilot | Anki + LeetCode |
|---|---|---|---|---|
| **Socratic coaching** | Strict rules, never reveals answers | Will give answer if you ask | N/A | N/A |
| **Spaced repetition** | Built-in SM-2 (behavior-driven) | None | None | Manual card creation |
| **Company intelligence** | Fetches + synthesizes interview reports | None | None | None |
| **Behavioral coaching** | STAR + company calibration | Generic | N/A | N/A |
| **Study plan** | Gap-driven, adapts to your history | None | None | Manual |
| **CLI-native** | Runs in your terminal | Browser-based | Browser extension | Separate apps |
| **Problem scaffolding** | Auto-scaffolds with test harness | Copy-paste | N/A | N/A |
| **Mock interviews** | Timed + verbal mode + company-calibrated | No structure | N/A | N/A |
| **Behavioral analytics** | Tracks hint patterns per topic | None | None | None |
| **Agent-agnostic** | Claude Code + Gemini CLI | Locked to one | Locked to one | N/A |
| **Cost** | Free + your existing AI subscription | Subscription | Subscription | Free/Paid |

## Supported Languages

- **C++** (g++ -std=c++17) — with STL pretty-printing and `DBG()` macro
- **Python** — with ListNode, TreeNode, and parsing utilities
- **Java** — with LcUtils data structures

## Requirements

- Python 3.6+
- One of: [Claude Code](https://claude.ai/code) or [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- A C++/Python/Java compiler (for whichever language you use)

## License

MIT
