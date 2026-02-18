# /gc-setup — Full Onboarding

## Arguments
$ARGUMENTS (optional): [--resume <path>] [--jobs <url1,url2,...>]

## Purpose
Complete first-time setup in one command. The user types nothing in a terminal.
You run every grind command. You fetch every URL. You ask only what you can't infer.

## Steps

### 1. Initialize
```bash
./grind init
```
Always use `./grind init` (not `grind init`) — this is the bootstrap step that creates the symlink
so that bare `grind` works for all subsequent commands. Safe to re-run if already initialized.

### 2. Check for existing session
```bash
grind session recover
```
If there is unlogged work from a previous session, surface it and handle it before proceeding.

### 3. Read behavior model (if data exists)
```bash
grind behavior summary
```
Internalize any patterns before the session starts. Adjust coaching stance accordingly.

### 4. Resume ingestion

If `--resume <path>` was provided, use that path.
Otherwise ask: "Share your resume — a file path, a URL, or paste the text directly."

Read the resume using your native tools:
- File path → use Read tool on the path (supports PDF, .txt, .docx natively)
- URL → use WebFetch to fetch the content
- Pasted text → process inline

Extract this JSON profile from whatever you receive:
```json
{
  "years_experience": <number>,
  "seniority_estimate": "junior|mid|senior|staff",
  "preferred_languages": ["C++", "Python"],
  "domains": ["backend", "distributed-systems"],
  "behavioral_context": "brief summary of projects and responsibilities",
  "education": "BS Computer Science"
}
```

Then store it:
```bash
grind resume set --path "<path_or_url>" --profile '<json>'
```

### 5. Job target ingestion

If `--jobs` was provided, use those URLs.
Otherwise ask: "Share the job link(s) you're preparing for. One URL or several — all fine."

For EACH URL provided:
1. Fetch with WebFetch
2. Extract: company, role, team, required_skills, tech_stack_signals, seniority, interview_date (if visible)
3. If interview date not in the JD, ask: "When is your interview at <company>? (e.g. 2026-03-10)"
4. Run:
   ```bash
   grind target add --company "<company>" --role "<role>" --date "<YYYY-MM-DD>" --url "<url>" --lang <inferred_from_jd_or_resume>
   ```
5. Store required skills:
   ```bash
   grind target update <id> --field required_skills --value '["skill1", "skill2"]'
   ```

### 6. Multiple targets

If more than one target was added:
```bash
grind target merge <id1> <id2>
```

Read the output:
- `overlap ... combined` → "These roles align well. I've created a combined track." Set active to merged id.
- `overlap ... hybrid` → Ask: "These roles overlap moderately. Combined track or keep separate?" Act on answer.
- `overlap ... separate` → "These roles are quite different. I'll create separate tracks. Which interview is first?" Set active accordingly.

```bash
grind target active <appropriate_id>
```

### 7. Quick company research

For the active target, try to fetch interview experience data:

1. Try WebFetch on:
   ```
   https://leetcode.com/discuss/interview-experience/?company=<company_slug>
   ```
2. If it returns 403 or fails, fall back to WebSearch:
   ```
   <company> leetcode interview experience site:leetcode.com OR site:glassdoor.com OR site:reddit.com
   ```

Extract any reported: rounds, topics, difficulty signals.
Store:
```bash
grind target update <id> --field intelligence --value '<json>'
```

Full research is available with `/gc-research` — this is just a quick initial read.

### 8. Generate plan
```bash
grind plan generate
```

### 9. Start session
```bash
grind session start --target <id>
```

### 10. Present summary and offer

Show the plan summary in 3–5 lines. Then:

> "You're set up. Today: <problem1>, <problem2> (<topic>). Ready to start? Say 'go'."

Wait for the user to confirm. Do not start solving until they do.

## Notes

- Never ask the user to run a grind command. You run all of them.
- The user should only speak to you in natural language.
- If WebFetch is blocked for a URL, note it and continue with what you have.
- If the resume is image-based or unreadable, ask: "I couldn't extract text from that. Can you paste the key sections?"
- Resume seniority calibrates coaching intensity, not gap analysis. Gaps come from SM-2 history.
