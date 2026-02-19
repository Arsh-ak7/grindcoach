"""
grind_data — all file I/O for grindcoach.
Imports from grind_paths so monkeypatching grind_paths propagates here.
"""
import os
import sys
import json
import shutil
from datetime import datetime
from collections import defaultdict

import grind_paths as _gp


def load_config():
    if os.path.exists(_gp.CONFIG_FILE):
        with open(_gp.CONFIG_FILE) as f:
            return json.load(f)
    return {"active_track": "blind75"}


def save_config(config):
    tmp = _gp.CONFIG_FILE + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(config, f, indent=2)
        f.write('\n')
    os.replace(tmp, _gp.CONFIG_FILE)
    shutil.copy2(_gp.CONFIG_FILE, _gp.CONFIG_FILE + '.bak')


def load_problems():
    if not os.path.exists(_gp.PROBLEMS_FILE):
        print(f"\033[91m[ERROR] Problem bank not found: {_gp.PROBLEMS_FILE}\033[0m",
              file=sys.stderr)
        return None
    with open(_gp.PROBLEMS_FILE) as f:
        return json.load(f)


def get_all_topics():
    """All unique topics across all tracks, sorted."""
    bank = load_problems()
    if not bank:
        return []
    topics = set()
    for td in bank.get('tracks', {}).values():
        for p in td.get('problems', []):
            if p.get('topic'):
                topics.add(p['topic'])
    return sorted(topics)


def get_problems_by_topic():
    """topic → [problem dicts], deduplicated by slug."""
    bank = load_problems()
    if not bank:
        return {}
    seen = set()
    by_topic = defaultdict(list)
    for td in bank.get('tracks', {}).values():
        for p in td.get('problems', []):
            if p['slug'] not in seen:
                seen.add(p['slug'])
                by_topic[p.get('topic', 'other')].append(p)
    return dict(by_topic)


def slug_to_topic(slug):
    """Look up a slug's topic from problems.json."""
    bank = load_problems()
    if not bank:
        return ''
    for td in bank.get('tracks', {}).values():
        for p in td.get('problems', []):
            if p['slug'] == slug:
                return p.get('topic', '')
    return ''


def parse_memory():
    if not os.path.exists(_gp.MEMORY_FILE):
        return []
    with open(_gp.MEMORY_FILE) as f:
        lines = f.readlines()
    rows = []
    in_table = False
    for line in lines:
        s = line.strip()
        if s.startswith('| Slug'):
            in_table = True
            continue
        if in_table and s.startswith('|---'):
            continue
        if in_table and s.startswith('|'):
            cells = [c.strip() for c in s.split('|')[1:-1]]
            if len(cells) >= 10:
                rows.append({
                    'slug':        cells[0],
                    'topic':       cells[1],
                    'difficulty':  cells[2],
                    'date':        cells[3],
                    'rating':      int(cells[4]) if cells[4] else 0,
                    'time':        cells[5],
                    'hints':       int(cells[6]) if cells[6] else 0,
                    'ease':        float(cells[7]) if cells[7] else 2.5,
                    'interval':    cells[8],
                    'next_review': cells[9],
                })
        elif in_table and not s.startswith('|'):
            in_table = False
    return rows


def write_memory(rows):
    """Atomic write: write to .tmp then os.replace, keep rolling .bak."""
    tmp = _gp.MEMORY_FILE + '.tmp'
    lines = [
        '# LeetCode Progress\n', '\n',
        '| Slug | Topic | Difficulty | Date | Rating | Time | Hints | Ease | Interval | Next Review |\n',
        '|------|-------|------------|------|--------|------|-------|------|----------|-------------|\n',
    ]
    for r in rows:
        lines.append(
            f"| {r['slug']} | {r['topic']} | {r['difficulty']} | {r['date']} "
            f"| {r['rating']} | {r['time']} | {r['hints']} | {r['ease']:.1f} "
            f"| {r['interval']} | {r['next_review']} |\n"
        )
    with open(tmp, 'w') as f:
        f.writelines(lines)
    os.replace(tmp, _gp.MEMORY_FILE)
    shutil.copy2(_gp.MEMORY_FILE, _gp.MEMORY_FILE + '.bak')


def load_behavior_events():
    if not os.path.exists(_gp.BEHAVIOR_FILE):
        return []
    events = []
    with open(_gp.BEHAVIOR_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return events


def flush_behavior_events(session):
    """Append hint_events from session dict to behavior.jsonl (append-only)."""
    events = session.get('hint_events', [])
    if not events:
        return 0
    with open(_gp.BEHAVIOR_FILE, 'a') as f:
        for ev in events:
            f.write(json.dumps(ev) + '\n')
    return len(events)


def load_session():
    if not os.path.exists(_gp.SESSION_FILE):
        return None
    with open(_gp.SESSION_FILE) as f:
        return json.load(f)


def save_session(session):
    with open(_gp.SESSION_FILE, 'w') as f:
        json.dump(session, f, indent=2)
        f.write('\n')
