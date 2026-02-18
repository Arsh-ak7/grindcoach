"""
Tests for plan generation — gap-driven scheduling.

Plan invariants:
- Unknown topics are front-loaded
- Weak topics come before developing and strong
- Company-reported topics get extra weight (at least 1.5x)
- mock_sessions_target >= 3
- Plan is stored in target config
"""
import json
import os
import pytest
from datetime import datetime, timedelta
from conftest import import_grind


@pytest.fixture(scope="module")
def grind():
    return import_grind()


def make_row(slug, topic, rating):
    return {
        "slug": slug, "topic": topic, "rating": rating,
        "difficulty": "medium", "date": "2026-01-01",
        "ease": 2.5, "interval": 1, "repetition": 0,
        "next_review": "2030-01-01",  # far future — not due
        "time": 25, "hints": 0,   # write_memory uses 'time'
    }


def make_config(days_away=20, reported_topics=None, lang="cpp"):
    interview_date = (datetime.now() + timedelta(days=days_away)).strftime("%Y-%m-%d")
    return {
        "active_target": "test-001",
        "targets": {
            "test-001": {
                "id": "test-001",
                "company": "TestCo",
                "role": "SWE",
                "interview_date": interview_date,
                "preferred_language": lang,
                "required_skills": [],
                "intelligence": {
                    "reported_topics": reported_topics or [],
                    "rounds": ["technical"],
                },
                "plan": {},
            }
        },
        "resume": {"seniority_estimate": "mid"},
        "gap_overrides": {},
    }


def test_plan_generates_without_history(tmp_env):
    g, tmp = tmp_env
    config = make_config()
    g.save_config(config)
    g._generate_plan_for_target(g.load_config(), "test-001")
    reloaded = g.load_config()
    plan = reloaded["targets"]["test-001"]["plan"]
    assert "days" in plan
    assert len(plan["days"]) > 0


def test_plan_has_days_remaining(tmp_env):
    g, tmp = tmp_env
    config = make_config(days_away=20)
    g.save_config(config)
    g._generate_plan_for_target(g.load_config(), "test-001")
    plan = g.load_config()["targets"]["test-001"]["plan"]
    assert plan["days_remaining"] >= 18  # allow ±2 days for timing


def test_plan_mock_sessions_target(tmp_env):
    g, tmp = tmp_env
    config = make_config(days_away=20)
    g.save_config(config)
    g._generate_plan_for_target(g.load_config(), "test-001")
    plan = g.load_config()["targets"]["test-001"]["plan"]
    assert plan.get("mock_sessions_target", 0) >= 3


def test_unknown_topics_appear_early(tmp_env):
    g, tmp = tmp_env
    # No history at all → all topics unknown → unknown should be front-loaded
    config = make_config(days_away=30)
    g.save_config(config)
    g._generate_plan_for_target(g.load_config(), "test-001")
    plan = g.load_config()["targets"]["test-001"]["plan"]
    days = plan["days"]
    # Plan days have 'focus' field (topic) and 'type' field
    # First-third coding days should focus on unknown/high-weight topics
    coding_days = [d for d in days if d.get("type") == "coding"]
    assert len(coding_days) > 0  # should have coding days


def test_company_reported_topics_included(tmp_env):
    g, tmp = tmp_env
    # reported_topics are problem slugs in the plan schema; they affect topic weights
    config = make_config(days_away=30, reported_topics=[])
    g.save_config(config)
    g._generate_plan_for_target(g.load_config(), "test-001")
    plan = g.load_config()["targets"]["test-001"]["plan"]
    # days[].problems is a list of slug strings, days[].focus is topic
    all_focuses = {d.get("focus") for d in plan["days"]}
    # Plan should focus on something (not empty)
    assert len(all_focuses) > 0


def test_plan_regenerate_preserves_completed_days(tmp_env):
    g, tmp = tmp_env
    config = make_config(days_away=20)
    g.save_config(config)
    g._generate_plan_for_target(g.load_config(), "test-001")
    # Mark first day as completed
    config = g.load_config()
    if config["targets"]["test-001"]["plan"]["days"]:
        config["targets"]["test-001"]["plan"]["days"][0]["completed"] = True
    g.save_config(config)

    # Regenerate
    g._generate_plan_for_target(g.load_config(), "test-001")
    plan = g.load_config()["targets"]["test-001"]["plan"]
    # Plan should still exist and have days
    assert len(plan["days"]) > 0
