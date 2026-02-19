"""
grind_algos — all algorithms for grindcoach.
SM-2, gap analysis, behavior patterns, plan generation, notes, plan progress.
"""
import os
import math
from datetime import datetime, timedelta
from collections import defaultdict

import grind_paths as _gp
from grind_data import (
    load_config, save_config, parse_memory, load_problems,
    get_all_topics, get_problems_by_topic, slug_to_topic,
    flush_behavior_events,
)


def sm2_calculate(rating, prev_ease=2.5, prev_interval=0, repetition=0):
    """Returns (new_ease, new_interval, new_repetition). Rating 1–5."""
    new_ease = prev_ease + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02))
    new_ease = max(1.3, new_ease)
    if rating < 3:
        return new_ease, 1, 0
    new_rep = repetition + 1
    if new_rep == 1:   new_interval = 1
    elif new_rep == 2: new_interval = 6
    else:              new_interval = math.ceil(prev_interval * new_ease)
    return new_ease, new_interval, new_rep


def compute_gap_scores(rows, overrides=None, today=None):
    """Classify topics, weighting recent evidence more than stale evidence."""
    overrides = overrides or {}
    if today is None:
        today = datetime.now().date()

    topic_weighted = defaultdict(list)  # topic → [(rating, weight)]
    for r in rows:
        if not r.get('topic') or not r.get('rating'):
            continue
        try:
            nr = datetime.strptime(r['next_review'], '%Y-%m-%d').date()
            days_overdue = max(0, (today - nr).days)
        except (ValueError, KeyError):
            days_overdue = 0
        weight = math.exp(-days_overdue / 30.0)
        topic_weighted[r['topic']].append((r['rating'], weight))

    scores = {}
    for topic in get_all_topics():
        if topic in overrides:
            scores[topic] = overrides[topic]
            continue
        pairs = topic_weighted.get(topic, [])
        if not pairs:
            scores[topic] = 'unknown'
            continue
        total_w = sum(w for _, w in pairs)
        wavg    = sum(r * w for r, w in pairs) / total_w
        n       = len(pairs)
        if n < 3 or wavg < 3.0:
            scores[topic] = 'weak'
        elif wavg < 4.0:
            scores[topic] = 'developing'
        else:
            scores[topic] = 'strong'
    return scores


def compute_behavior_patterns(events):
    """Compute per-topic flags from behavior.jsonl events."""
    hint_times  = defaultdict(list)
    hint_levels = defaultdict(list)
    effective   = defaultdict(list)
    calibration = defaultdict(list)

    for e in events:
        topic = e.get('topic', 'unknown')
        ev    = e.get('event', '')
        if ev == 'hint_given':
            if 'time_to_hint_min' in e:
                hint_times[topic].append(e['time_to_hint_min'])
            if 'hint_level' in e:
                hint_levels[topic].append(e['hint_level'])
        elif ev == 'hint_assessed':
            effective[topic].append(bool(e.get('effective', False)))
        elif ev == 'rating_calibration':
            div = abs(e.get('self_rating', 0) - e.get('expected_rating_from_hints', 0))
            calibration[topic].append(div)

    patterns = {}
    all_topics = set(list(hint_times) + list(hint_levels))
    for topic in all_topics:
        avg_time  = (sum(hint_times[topic]) / len(hint_times[topic])
                     if hint_times[topic] else None)
        avg_level = (sum(hint_levels[topic]) / len(hint_levels[topic])
                     if hint_levels[topic] else None)
        eff_rate  = (sum(1 for x in effective[topic] if x) / len(effective[topic])
                     if effective[topic] else None)
        cal_delta = (sum(calibration[topic]) / len(calibration[topic])
                     if calibration[topic] else None)

        flags = []
        if avg_time is not None and avg_time < 5:        flags.append('quick_give_up')
        if avg_level is not None and avg_level > 2.5:   flags.append('chronic_hint')
        if eff_rate is not None and eff_rate > 0.75:    flags.append('hint_positive')
        if eff_rate is not None and eff_rate < 0.40:    flags.append('hint_negative')
        if cal_delta is not None and cal_delta > 1.5:   flags.append('overconfident')

        patterns[topic] = {
            'avg_time_to_hint_min': round(avg_time, 1)  if avg_time  is not None else None,
            'avg_hint_level':       round(avg_level, 2) if avg_level is not None else None,
            'hint_effectiveness':   round(eff_rate, 2)  if eff_rate  is not None else None,
            'calibration_delta':    round(cal_delta, 1) if cal_delta is not None else None,
            'sample_count':         len(hint_levels.get(topic, [])),
            'flags':                flags,
        }
    return patterns


def _has_design_round(intelligence):
    return any('design' in r for r in intelligence.get('rounds', []))


def _generate_plan_for_target(config, tid):
    """
    Generate a day-by-day study plan. Saves to config.
    Returns (success: bool, message: str).
    """
    target = config.get('targets', {}).get(tid)
    if not target:
        return False, f"Target '{tid}' not found."

    date_str = target.get('interview_date', '')
    if not date_str:
        return False, ("Target has no interview_date. Set it: "
                       "grind target update <id> --field interview_date --value YYYY-MM-DD")
    try:
        interview_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return False, f"Invalid date format: {date_str} (expected YYYY-MM-DD)"

    rows         = parse_memory()
    overrides    = config.get('gap_overrides', {})
    gap_scores   = compute_gap_scores(rows, overrides)
    intelligence = target.get('intelligence', {})

    days_remaining = max(1, (interview_date - datetime.now().date()).days)

    reported_set = set(intelligence.get('reported_topics', []))
    reported_topic_set = set()
    bank = load_problems()
    if not bank:
        return False, "Problem bank not found — cannot generate plan."
    for td in bank.get('tracks', {}).values():
        for p in td.get('problems', []):
            if p['slug'] in reported_set:
                reported_topic_set.add(p.get('topic', ''))

    score_weight = {'unknown': 2.5, 'weak': 3.0, 'developing': 1.0, 'strong': 0.3}
    weights = {}
    for topic, score in gap_scores.items():
        w = score_weight.get(score, 1.0)
        if topic in reported_topic_set:
            w = max(w, 1.5)
        weights[topic] = w

    reserve_mock    = min(3, days_remaining // 7)
    practice_days   = max(1, days_remaining - reserve_mock)
    has_design      = _has_design_round(intelligence)
    coding_days     = int(practice_days * 0.6)
    design_days     = int(practice_days * 0.2) if has_design else 0
    behavioral_days = practice_days - coding_days - design_days

    solved_slugs  = {r['slug'] for r in rows}
    sorted_topics = sorted(weights.keys(), key=lambda t: -weights.get(t, 0))
    problems_by_topic = get_problems_by_topic()
    topic_queues  = {
        t: [p for p in problems_by_topic.get(t, []) if p['slug'] not in solved_slugs]
        for t in sorted_topics
    }

    days    = []
    day_num = 1
    today   = datetime.now().date()

    weight_tiers = {}
    for t in sorted_topics:
        w = round(weights.get(t, 0), 1)
        weight_tiers.setdefault(w, []).append(t)
    tier_indices = {w: 0 for w in weight_tiers}

    def pick_day_problems(n=2):
        picked = []
        seen_tiers = set()
        for t in sorted_topics:
            if len(picked) >= n:
                break
            w = round(weights.get(t, 0), 1)
            if w in seen_tiers:
                continue
            seen_tiers.add(w)
            tier = weight_tiers[w]
            start = tier_indices[w]
            for i in range(len(tier)):
                candidate = tier[(start + i) % len(tier)]
                if topic_queues.get(candidate):
                    picked.append((topic_queues[candidate].pop(0), candidate))
                    tier_indices[w] = (start + i + 1) % len(tier)
                    break
        if len(picked) < n:
            for t in sorted_topics:
                if len(picked) >= n:
                    break
                if topic_queues.get(t) and not any(pp[1] == t for pp in picked):
                    picked.append((topic_queues[t].pop(0), t))
        return picked

    for _ in range(coding_days):
        day_problems = pick_day_problems(2)
        if not day_problems:
            break
        focus  = day_problems[0][1]
        slugs  = [p['slug'] for p, _ in day_problems]
        days.append({
            'day': day_num,
            'date': (today + timedelta(days=day_num - 1)).strftime('%Y-%m-%d'),
            'type': 'coding',
            'problems': slugs,
            'focus': focus,
            'completed': False,
        })
        day_num += 1

    for _ in range(design_days):
        days.append({
            'day': day_num,
            'date': (today + timedelta(days=day_num - 1)).strftime('%Y-%m-%d'),
            'type': 'system-design',
            'problems': [],
            'focus': 'system-design',
            'completed': False,
        })
        day_num += 1

    for _ in range(behavioral_days):
        days.append({
            'day': day_num,
            'date': (today + timedelta(days=day_num - 1)).strftime('%Y-%m-%d'),
            'type': 'behavioral',
            'problems': [],
            'focus': 'behavioral',
            'completed': False,
        })
        day_num += 1

    for _ in range(reserve_mock):
        days.append({
            'day': day_num,
            'date': (today + timedelta(days=day_num - 1)).strftime('%Y-%m-%d'),
            'type': 'mock',
            'problems': [],
            'focus': 'mock-interview',
            'completed': False,
        })
        day_num += 1

    target['plan'] = {
        'generated_at':            datetime.now().isoformat(),
        'days_remaining':          days_remaining,
        'mock_sessions_target':    max(3, days_remaining // 5),
        'mock_sessions_completed': 0,
        'days':                    days,
    }
    save_config(config)
    return True, f"Plan generated: {len(days)} days until {date_str}"


def _mark_plan_progress(config, solved_set):
    """
    Check if any plan days are fully solved. Mark them complete and save config.
    Returns True if any day was newly marked complete.
    """
    tid    = config.get('active_target')
    target = config.get('targets', {}).get(tid) if tid else None
    days   = (target or {}).get('plan', {}).get('days', [])
    if not days:
        return False

    changed = False
    for day in days:
        if day.get('completed') or not day.get('problems'):
            continue
        if all(s in solved_set for s in day['problems']):
            day['completed'] = True
            changed = True

    if changed:
        save_config(config)
        done  = sum(1 for d in days if d.get('completed'))
        total = len(days)
        print(f"\033[96m[INFO] Plan progress: {done}/{total} days complete.\033[0m")
    return changed


def _append_notes(slug, notes, date, rating):
    """Append a timestamped note to problems/<slug>/notes.md."""
    folder       = slug.replace('-', '_')
    problem_dir  = os.path.join(_gp.PROJECT_ROOT, 'problems', folder)
    os.makedirs(problem_dir, exist_ok=True)
    notes_file   = os.path.join(problem_dir, 'notes.md')
    entry = f"\n## {date} (rating {rating})\n\n{notes}\n"
    with open(notes_file, 'a') as f:
        f.write(entry)
