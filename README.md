# leet-coach

**Your AI coding coach that never gives you the answer.**

An open-source, CLI-native LeetCode coaching system that uses AI agents (Claude Code or Gemini CLI) as Socratic tutors — not answer machines. Built-in spaced repetition, curated problem tracks, and timed mock interviews.

> Meta, Google, and others now allow AI tools in coding interviews. The question isn't whether to use AI — it's whether you've trained *with* AI in a way that builds real problem-solving skill. That's what leet-coach does.

## 30-Second Quickstart

```bash
git clone https://github.com/YOUR_USERNAME/leet-coach.git
cd leet-coach
./grind init

# Start your first problem (in Claude Code or Gemini CLI)
/solve two-sum cpp
```

That's it. No pip install, no API keys, no config files. Just Python 3 and an AI agent.

## How It Works

```
You ←→ AI Agent (Claude Code / Gemini CLI)
          ↕
      coach_persona.md    ← Socratic rules: never reveal answers
          ↕
        grind CLI          ← Scaffold, run, track progress (Python 3, zero deps)
          ↕
      problems.json        ← Curated tracks (Blind 75, NeetCode 150)
          ↕
       memory.md           ← SM-2 spaced repetition schedule
```

The AI agent follows strict coaching rules defined in `coach_persona.md`:
- **Present the problem, then shut up.** Wait for you to think first.
- **Never volunteer hints.** Only when you ask, and even then, progressively.
- **Never give the answer.** Guide with questions, not solutions.

The `grind` CLI handles everything deterministic — scaffolding, compilation, spaced repetition math. The AI handles everything that needs judgment — coaching, hints, code review.

## Commands

### Agent Commands (in Claude Code or Gemini CLI)

| Command | What it does |
|---------|-------------|
| `/solve two-sum cpp` | Scaffold a problem, present it, coach you through it |
| `/solve <any-leetcode-url> python` | Works with ANY LeetCode problem, not just the bank |
| `/hint` | Get a progressive hint (escalates: question → category → technique → walkthrough) |
| `/review` | Review your solution: complexity, edge cases, alternatives. Logs to spaced repetition. |
| `/mock --topic dp` | Timed mock interview with a random unsolved problem |
| `/progress` | Progress summary with track-aware suggestions |

### CLI Commands (terminal)

```bash
grind init                                    # First-time setup
grind new <slug> <lang>                       # Scaffold a problem
grind run <slug>                              # Compile and run
grind log <slug> <rating> [--time] [--hints]  # Log with SM-2 spaced repetition
grind list [--track X] [--topic Y]            # Browse problem bank
grind track [name]                            # View/switch tracks
grind progress                                # Due reviews, streak, suggestions
grind archive                                 # Archive old memory rows
```

## Problem Bank

Two curated tracks included, with more coming:

| Track | Problems | Focus |
|-------|----------|-------|
| **Blind 75** | 75 | Classic interview prep essentials |
| **NeetCode 150** | 150 | Comprehensive topic coverage |

**The bank is guidance, not a gate.** Any LeetCode URL works with `/solve`. The bank just helps with "what should I do next?"

## Architecture

```
leet-coach/
├── grind                 # CLI tool (Python 3, zero external deps)
├── coach_persona.md      # Socratic coaching rules (shared by all agents)
├── problems.json         # Problem bank index (Blind 75, NeetCode 150)
├── CLAUDE.md             # Claude Code agent config
├── GEMINI.md             # Gemini CLI agent config
├── AGENTS.md             # Canonical agent config (any agent)
├── templates/            # Starter files (C++, Python, Java)
├── utils/                # Language helpers (STL printing, debug macros)
├── .claude/skills/       # Claude Code slash commands
└── .gemini/commands/     # Gemini CLI slash commands
```

**User data (gitignored):**
- `problems/` — Your solutions
- `memory.md` — Your spaced repetition progress
- `.lc_config.json` — Your active track preference

## Why Not Just Use ChatGPT?

| | leet-coach | Raw ChatGPT/Claude | LeetCopilot | Anki + LeetCode |
|---|---|---|---|---|
| **Socratic coaching** | Strict rules, never reveals answers | Will give answer if you ask | N/A | N/A |
| **Spaced repetition** | Built-in SM-2 | None | None | Manual card creation |
| **CLI-native** | Runs in your terminal | Browser-based | Browser extension | Separate apps |
| **Problem scaffolding** | Auto-scaffolds with test harness | Copy-paste | N/A | N/A |
| **Mock interviews** | Timed sessions with coaching | No structure | N/A | N/A |
| **Works offline** | CLI works offline, AI needs connection | Needs connection | Needs connection | Partial |
| **Agent-agnostic** | Claude Code + Gemini CLI | Locked to one provider | Locked to one provider | N/A |
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
