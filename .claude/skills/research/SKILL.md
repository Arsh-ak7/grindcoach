# /research — Company Intelligence Refresh

## Arguments
$ARGUMENTS (optional): [--company <name>]

## Purpose
Fetch and synthesize company interview intelligence from public sources.
Update the active target's intelligence JSON. Report what's new.

## Steps

### 1. Identify target
If `--company` is given, find matching target by company name.
Otherwise use active target:
```bash
grind target active
```

### 2. Fetch sources sequentially

For each source, use WebFetch. Skip gracefully if blocked (4xx/5xx).

**Source 1 — LeetCode Discuss (highest signal)**
```
https://leetcode.com/discuss/interview-experience/?company=<company_slug>
```
Extract: reported rounds, reported problem slugs/topics, difficulty signals, recency.

**Source 2 — Company engineering blog**
If known (e.g. engineering.bmw.com, engineering.atspotify.com): fetch and extract tech stack signals.

**Source 3 — Company About/Values page**
Extract: company values, mission statements (for behavioral coaching).

**Source 4 — Glassdoor interview section**
```
https://www.glassdoor.com/Interview/<company>-interview-questions-SRCH_KE0,<n>.htm
```
Skip gracefully if blocked — note `"sources_blocked": ["glassdoor"]` in output.

### 3. Synthesize intelligence JSON

Build this object from everything fetched:
```json
{
  "rounds": ["technical", "system-design", "behavioral"],
  "reported_topics": ["lru-cache", "binary-search", "graphs-bfs"],
  "reported_difficulty": "medium-hard",
  "recent_reports_summary": "4 reports (last 90 days). Topics: LRU cache, binary search.",
  "behavioral_themes": ["ownership", "ambiguity", "cross-functional"],
  "company_values": ["Responsibility", "Trust", "Openness"],
  "sources_blocked": [],
  "fetched_at": "<today's date>"
}
```

### 4. Store and report

```bash
grind target update <id> --field intelligence --value '<json>'
```

Report delta: "Found N new interview reports since last fetch. Key topics: X, Y, Z."

## Notes

- Claude Code fetches sources sequentially (WebFetch one at a time).
- Never fabricate interview reports. Only extract from fetched content.
- If no data found for a company, say so clearly rather than guessing.
