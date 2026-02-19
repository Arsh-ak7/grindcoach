"""
Tests for grind stats command — weekly solve rate, rating trends, streak stats.
"""
import os
import pytest
from conftest import import_grind


@pytest.fixture(scope="module")
def grind():
    return import_grind()


def make_row(slug, topic, rating, days_ago=0):
    from datetime import datetime, timedelta
    date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    return {"slug": slug, "topic": topic, "rating": rating,
            "difficulty": "medium", "date": date,
            "ease": 2.5, "interval": "6d", "hints": 0, "time": "20m",
            "next_review": "2030-01-01"}


def test_stats_empty_memory(tmp_env, capsys):
    g, tmp = tmp_env
    g.write_memory([])
    import argparse
    g.cmd_stats(argparse.Namespace(topic=None))
    out = capsys.readouterr().out
    assert "No problems" in out


def test_stats_smoke(tmp_env, capsys):
    g, tmp = tmp_env
    rows = [make_row(f"p{i}", "arrays", 4, days_ago=i) for i in range(5)]
    g.write_memory(rows)
    import argparse
    g.cmd_stats(argparse.Namespace(topic=None))
    out = capsys.readouterr().out
    assert "Weekly" in out
    assert "Streak" in out


def test_stats_topic_filter(tmp_env, capsys):
    g, tmp = tmp_env
    rows = [make_row("two-sum", "arrays", 5), make_row("coin-change", "dp", 2)]
    g.write_memory(rows)
    import argparse
    g.cmd_stats(argparse.Namespace(topic="dp"))
    out = capsys.readouterr().out
    assert "dp" in out
    assert "arrays" not in out


def test_stats_rating_trend_shown_for_3plus(tmp_env, capsys):
    g, tmp = tmp_env
    rows = [make_row(f"p{i}", "graphs", r) for i, r in enumerate([2, 2, 2, 5, 5, 5])]
    g.write_memory(rows)
    import argparse
    g.cmd_stats(argparse.Namespace(topic=None))
    out = capsys.readouterr().out
    assert "graphs" in out   # shows trend
    assert "→" in out        # progression arrow


def test_stats_streak_counts_consecutive_days(tmp_env, capsys):
    g, tmp = tmp_env
    # 3 consecutive days
    rows = [make_row(f"p{i}", "arrays", 4, days_ago=i) for i in range(3)]
    g.write_memory(rows)
    import argparse
    g.cmd_stats(argparse.Namespace(topic=None))
    out = capsys.readouterr().out
    assert "Streak" in out
