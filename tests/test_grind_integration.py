"""
Integration test: full flow from init through logging to gap analysis.

Verifies the end-to-end pipeline:
  init → target add → resume set → session start → log → gap show → behavior flush
"""
import os
import json
import pytest
from datetime import datetime, timedelta
from conftest import import_grind


@pytest.fixture(scope="module")
def grind():
    return import_grind()


def make_row(slug, topic, rating, days_ago=1):
    date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    ease, interval, rep = 2.5, 1, 0
    for _ in range(2):
        ease, interval, rep = grind_module().sm2_calculate(rating, ease, interval, rep)
    next_review = (datetime.now() + timedelta(days=interval)).strftime("%Y-%m-%d")
    return {
        "slug": slug, "topic": topic, "rating": rating,
        "difficulty": "medium", "date": date,
        "ease": round(ease, 4), "interval": interval, "repetition": rep,
        "next_review": next_review, "time": 20, "hints": 0,
    }


def grind_module():
    return import_grind()


def test_memory_write_and_gap_reflect_history(tmp_env):
    g, tmp = tmp_env
    rows = (
        [make_row(f"arr-{i}", "arrays", 5) for i in range(5)] +
        [make_row(f"dp-{i}", "dp", 2) for i in range(4)]
    )
    g.write_memory(rows)
    parsed = g.parse_memory()
    assert len(parsed) == 9

    scores = g.compute_gap_scores(parsed)
    assert scores.get("arrays") == "strong"
    assert scores.get("dp") == "weak"


def test_behavior_flush_then_load(tmp_env):
    g, tmp = tmp_env
    events = [
        {"ts": "T1", "slug": "coin-change", "topic": "dp",
         "event": "hint_given", "hint_level": 2, "time_to_hint_min": 4},
        {"ts": "T2", "slug": "coin-change", "topic": "dp",
         "event": "hint_assessed", "hint_level": 2, "effective": True, "reasoning": "ok"},
    ]
    g.flush_behavior_events({"hint_events": events})
    loaded = g.load_behavior_events()
    assert len(loaded) == 2
    patterns = g.compute_behavior_patterns(loaded)
    assert "dp" in patterns
    assert "quick_give_up" in patterns["dp"]["flags"]  # time < 5 min


def test_config_round_trip(tmp_env):
    g, tmp = tmp_env
    config = {
        "active_track": "blind75",
        "active_target": "test-001",
        "targets": {
            "test-001": {
                "id": "test-001",
                "company": "TestCo",
                "role": "SWE",
                "interview_date": "2026-03-10",
                "preferred_language": "cpp",
                "required_skills": ["graphs", "C++17"],
                "intelligence": {},
                "plan": {},
            }
        },
        "resume": {
            "path": "/tmp/resume.pdf",
            "seniority_estimate": "mid",
            "preferred_languages": ["cpp"],
        },
        "gap_overrides": {"bit-manipulation": "weak"},
    }
    g.save_config(config)
    reloaded = g.load_config()
    assert reloaded["active_target"] == "test-001"
    assert reloaded["gap_overrides"]["bit-manipulation"] == "weak"
    assert reloaded["resume"]["seniority_estimate"] == "mid"
    assert reloaded["targets"]["test-001"]["company"] == "TestCo"


def test_gap_override_wins(tmp_env):
    g, tmp = tmp_env
    rows = [make_row(f"a{i}", "arrays", 5) for i in range(5)]
    g.write_memory(rows)
    config = g.load_config()
    overrides = {"arrays": "weak"}
    scores = g.compute_gap_scores(g.parse_memory(), overrides)
    assert scores["arrays"] == "weak"  # override beats strong


def test_session_and_behavior_pipeline(tmp_env):
    g, tmp = tmp_env
    # Simulate a complete session
    session = {
        "started_at": datetime.now().isoformat(),
        "clean_exit": False,
        "target": "test-001",
        "problems": [
            {"slug": "two-sum", "presented_at": "T", "hints": 1,
             "rated": True, "rating": 3, "logged": True, "logged_at": "T2"},
        ],
        "hint_events": [
            {"ts": "T", "slug": "two-sum", "topic": "arrays",
             "event": "hint_given", "hint_level": 1, "time_to_hint_min": 9},
        ],
    }
    g.save_session(session)
    g.flush_behavior_events(session)

    loaded = g.load_behavior_events()
    assert len(loaded) >= 1
    patterns = g.compute_behavior_patterns(loaded)
    assert "arrays" in patterns
    # 9 min → not quick_give_up
    assert "quick_give_up" not in patterns["arrays"]["flags"]
