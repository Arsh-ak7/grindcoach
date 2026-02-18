# Contributing to grindcoach

Thanks for your interest in contributing! Here's how to get started.

## Ways to Contribute

- **Add problems to tracks** — Submit PRs to expand `problems.json` with new tracks or problems
- **Add language support** — New templates in `templates/` and utils in `utils/`
- **Improve the CLI** — Better error messages, new commands, output formatting
- **Improve coaching prompts** — Refine `coach_persona.md` or agent skills/commands
- **Report bugs** — Open an issue with reproduction steps

## Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/grindcoach.git
cd grindcoach
./grind init
```

No dependencies to install. The CLI is pure Python 3.

## Adding a New Track to `problems.json`

Tracks are navigation indices — they don't contain problem descriptions. Each problem entry needs:

```json
{
  "slug": "two-sum",
  "topic": "arrays",
  "difficulty": "easy",
  "number": 1
}
```

- `slug`: The LeetCode URL slug (e.g. `two-sum` from `leetcode.com/problems/two-sum/`)
- `topic`: A lowercase topic tag
- `difficulty`: `easy`, `medium`, or `hard`
- `number`: The LeetCode problem number

## Adding Language Support

1. Create a template in `templates/<lang>.txt` with placeholders: `{{PROBLEM_NAME}}`, `{{PROBLEM_SLUG}}`, `{{PROBLEM_CLASS}}`, `{{PROBLEM_FOLDER}}`
2. Add a utility file in `utils/<lang>/` with common data structures and helpers
3. Add the language to the `cmd_new` and `_run_file` functions in `grind`
4. Update the agent skills and commands to reference the new language

## Modifying the Coaching Persona

`coach_persona.md` is the shared coaching ruleset. Changes here affect all agents. Be conservative — the "shut up and wait" philosophy is core to the project's value.

## Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR
- Test your changes: `grind init`, `grind new test-problem cpp`, `grind run test-problem`, `grind list`
- Don't commit user data (`problems/`, `memory.md`, `.lc_config.json`)
- Match the existing code style (no linters enforced, just be consistent)
