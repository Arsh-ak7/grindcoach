"""
Tests for compute_behavior_patterns() and flush_behavior_events().

Behavioral flags:
- quick_give_up: avg time to hint < 5 min
- chronic_hint: avg hint level > 2.5
- hint_positive: hint effectiveness rate > 75%
- hint_negative: hint effectiveness rate < 40%
- overconfident: calibration delta > 1.5
"""
import os
import json
import pytest
from conftest import import_grind


@pytest.fixture(scope="module")
def grind():
    return import_grind()


def hint_given(topic, hint_level, time_to_hint_min):
    return {
        "ts": "2026-02-18T10:00:00",
        "slug": "some-problem",
        "topic": topic,
        "event": "hint_given",
        "hint_level": hint_level,
        "time_to_hint_min": time_to_hint_min,
        "hints_so_far": 1,
    }


def hint_assessed(topic, hint_level, effective):
    return {
        "ts": "2026-02-18T10:05:00",
        "slug": "some-problem",
        "topic": topic,
        "event": "hint_assessed",
        "hint_level": hint_level,
        "effective": effective,
        "reasoning": "test",
    }


def rating_calibration(topic, self_rating, expected_rating):
    return {
        "ts": "2026-02-18T10:10:00",
        "slug": "some-problem",
        "topic": topic,
        "event": "rating_calibration",
        "self_rating": self_rating,
        "expected_rating_from_hints": expected_rating,
    }


# --- Flag detection tests ---

def test_quick_give_up_flag(grind):
    events = [hint_given("dp", 1, 3), hint_given("dp", 2, 4), hint_given("dp", 1, 2)]
    patterns = grind.compute_behavior_patterns(events)
    assert "quick_give_up" in patterns["dp"]["flags"]
    assert patterns["dp"]["avg_time_to_hint_min"] < 5


def test_no_quick_give_up_when_slow(grind):
    events = [hint_given("trees", 1, 10), hint_given("trees", 2, 12)]
    patterns = grind.compute_behavior_patterns(events)
    assert "quick_give_up" not in patterns["trees"]["flags"]


def test_chronic_hint_flag(grind):
    events = [hint_given("graphs", 3, 8), hint_given("graphs", 4, 10), hint_given("graphs", 3, 7)]
    patterns = grind.compute_behavior_patterns(events)
    assert "chronic_hint" in patterns["graphs"]["flags"]
    assert patterns["graphs"]["avg_hint_level"] > 2.5


def test_hint_positive_flag(grind):
    # hint_given needed so topic appears in pattern output; hint_assessed provides effectiveness
    events = [
        hint_given("strings", 1, 9),
        hint_given("strings", 2, 11),
        hint_assessed("strings", 1, True),
        hint_assessed("strings", 2, True),
        hint_assessed("strings", 1, True),
        hint_assessed("strings", 2, True),
    ]
    patterns = grind.compute_behavior_patterns(events)
    assert "hint_positive" in patterns["strings"]["flags"]
    assert patterns["strings"]["hint_effectiveness"] > 0.75


def test_hint_negative_flag(grind):
    events = [
        hint_given("dp", 2, 8),
        hint_given("dp", 3, 10),
        hint_assessed("dp", 2, False),
        hint_assessed("dp", 3, False),
        hint_assessed("dp", 2, False),
    ]
    patterns = grind.compute_behavior_patterns(events)
    assert "hint_negative" in patterns["dp"]["flags"]


def test_overconfident_flag(grind):
    # Need hint_given so topic is indexed; rating_calibration provides calibration delta
    events = [
        hint_given("arrays", 1, 8),
        hint_given("arrays", 2, 10),
        rating_calibration("arrays", 4, 2),
        rating_calibration("arrays", 5, 2),
        rating_calibration("arrays", 4, 2),
        rating_calibration("arrays", 5, 3),
    ]
    patterns = grind.compute_behavior_patterns(events)
    assert "overconfident" in patterns["arrays"]["flags"]
    assert patterns["arrays"]["calibration_delta"] > 1.5


def test_no_flags_when_well_calibrated(grind):
    events = [
        hint_given("trees", 1, 8),
        hint_assessed("trees", 1, True),
        rating_calibration("trees", 4, 4),  # no divergence
    ]
    patterns = grind.compute_behavior_patterns(events)
    # No problematic flags
    flags = patterns.get("trees", {}).get("flags", [])
    assert "quick_give_up" not in flags
    assert "overconfident" not in flags


def test_multiple_topics_isolated(grind):
    events = [
        hint_given("dp", 1, 3),   # quick_give_up for dp
        hint_given("dp", 1, 4),
        hint_given("trees", 1, 12),  # no quick_give_up for trees
    ]
    patterns = grind.compute_behavior_patterns(events)
    assert "quick_give_up" in patterns["dp"]["flags"]
    assert "quick_give_up" not in patterns.get("trees", {}).get("flags", [])


def test_empty_events(grind):
    patterns = grind.compute_behavior_patterns([])
    assert patterns == {}


# --- Flush behavior events tests ---

def test_flush_appends_to_behavior_jsonl(tmp_env):
    g, tmp = tmp_env
    session = {
        "hint_events": [
            hint_given("dp", 1, 5),
            hint_given("dp", 2, 8),
        ]
    }
    g.flush_behavior_events(session)
    assert os.path.exists(g.BEHAVIOR_FILE)
    lines = open(g.BEHAVIOR_FILE).readlines()
    assert len(lines) == 2


def test_flush_append_only_preserves_previous(tmp_env):
    g, tmp = tmp_env
    session1 = {"hint_events": [hint_given("dp", 1, 5), hint_given("dp", 2, 8)]}
    session2 = {"hint_events": [hint_given("trees", 1, 10)]}
    g.flush_behavior_events(session1)
    g.flush_behavior_events(session2)
    lines = open(g.BEHAVIOR_FILE).readlines()
    assert len(lines) == 3
    events = [json.loads(l) for l in lines]
    assert events[0]["topic"] == "dp"
    assert events[2]["topic"] == "trees"


def test_flush_empty_session_is_noop(tmp_env):
    g, tmp = tmp_env
    g.flush_behavior_events({"hint_events": []})
    # File might not exist yet, or if it does, it's empty or unchanged
    if os.path.exists(g.BEHAVIOR_FILE):
        lines = open(g.BEHAVIOR_FILE).readlines()
        assert len(lines) == 0


def test_load_behavior_events_matches_flush(tmp_env):
    g, tmp = tmp_env
    original = [hint_given("arrays", 1, 6), hint_assessed("arrays", 1, True)]
    g.flush_behavior_events({"hint_events": original})
    loaded = g.load_behavior_events()
    assert len(loaded) == 2
    assert loaded[0]["event"] == "hint_given"
    assert loaded[1]["event"] == "hint_assessed"


# --- Behavior archive tests ---

def test_behavior_archive_moves_old_events(tmp_env):
    import json as _json
    g, tmp = tmp_env
    events = [
        {"ts": "2025-10-01T10:00:00", "event": "hint_given", "topic": "dp"},
        {"ts": "2026-02-15T10:00:00", "event": "hint_given", "topic": "arrays"},
    ]
    g.flush_behavior_events({"hint_events": events})

    import argparse
    g.cmd_behavior(argparse.Namespace(behavior_cmd='archive', before='2026-01-01'))

    archive = tmp / "behavior_archive.jsonl"
    assert archive.exists()
    archived = [_json.loads(l) for l in archive.read_text().strip().splitlines()]
    assert len(archived) == 1
    assert archived[0]["topic"] == "dp"

    remaining = g.load_behavior_events()
    assert len(remaining) == 1
    assert remaining[0]["topic"] == "arrays"


def test_behavior_archive_default_90_days(tmp_env):
    g, tmp = tmp_env
    from datetime import datetime, timedelta
    old_ts   = (datetime.now() - timedelta(days=100)).isoformat()
    fresh_ts = (datetime.now() - timedelta(days=10)).isoformat()
    events = [
        {"ts": old_ts,   "event": "hint_given", "topic": "dp"},
        {"ts": fresh_ts, "event": "hint_given", "topic": "arrays"},
    ]
    g.flush_behavior_events({"hint_events": events})

    import argparse
    g.cmd_behavior(argparse.Namespace(behavior_cmd='archive', before=None))
    remaining = g.load_behavior_events()
    assert len(remaining) == 1
    assert remaining[0]["topic"] == "arrays"


def test_behavior_archive_atomic_rewrite(tmp_env):
    g, tmp = tmp_env
    events = [{"ts": "2025-01-01T00:00:00", "event": "hint_given", "topic": "dp"}]
    g.flush_behavior_events({"hint_events": events})
    import argparse
    g.cmd_behavior(argparse.Namespace(behavior_cmd='archive', before=None))
    # No .tmp leftover
    assert not (tmp / "behavior.jsonl.tmp").exists()
