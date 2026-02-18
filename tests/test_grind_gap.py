"""
Tests for compute_gap_scores() — gap analysis from SM-2 history.

Classification rules:
- No ratings → 'unknown'
- < 3 ratings OR avg < 3.0 → 'weak'
- avg < 4.0 → 'developing'
- avg >= 4.0 → 'strong'
- Explicit override wins over computed score
"""
import pytest
from conftest import import_grind


@pytest.fixture(scope="module")
def grind():
    return import_grind()


def make_row(slug, topic, rating):
    return {
        "slug": slug,
        "topic": topic,
        "rating": rating,
        "difficulty": "medium",
        "date": "2026-01-01",
        "ease": 2.5,
        "interval": 1,
        "repetition": 0,
        "next_review": "2026-01-02",
        "time": 25,   # write_memory uses 'time'
        "hints": 0,
    }


def test_unknown_when_no_history(grind):
    scores = grind.compute_gap_scores([])
    for score in scores.values():
        assert score == "unknown"


def test_weak_when_few_ratings(grind):
    # Only 2 ratings — fewer than threshold of 3
    rows = [make_row("two-sum", "arrays", 4), make_row("contains-duplicate", "arrays", 5)]
    scores = grind.compute_gap_scores(rows)
    assert scores.get("arrays") == "weak"


def test_weak_when_low_average(grind):
    rows = [make_row(f"p{i}", "dp", r) for i, r in enumerate([1, 2, 2, 2, 1])]
    scores = grind.compute_gap_scores(rows)
    assert scores.get("dp") == "weak"


def test_developing_when_mid_average(grind):
    rows = [make_row(f"p{i}", "graphs", r) for i, r in enumerate([3, 4, 3, 4, 3])]
    scores = grind.compute_gap_scores(rows)
    assert scores.get("graphs") == "developing"


def test_strong_when_high_average(grind):
    rows = [make_row(f"p{i}", "arrays", r) for i, r in enumerate([4, 5, 5, 4, 5])]
    scores = grind.compute_gap_scores(rows)
    assert scores.get("arrays") == "strong"


def test_override_wins_over_computed(grind):
    # SM-2 says 'strong' but override says 'weak'
    rows = [make_row(f"p{i}", "arrays", 5) for i in range(5)]
    overrides = {"arrays": "weak"}
    scores = grind.compute_gap_scores(rows, overrides)
    assert scores.get("arrays") == "weak"


def test_multiple_topics_independent(grind):
    rows = (
        [make_row(f"a{i}", "arrays", 5) for i in range(5)] +
        [make_row(f"d{i}", "dp", 2) for i in range(5)]
    )
    scores = grind.compute_gap_scores(rows)
    assert scores.get("arrays") == "strong"
    assert scores.get("dp") == "weak"


def test_boundary_avg_exactly_3(grind):
    # avg exactly 3.0 with 3+ ratings → 'weak' (< 3.0 is weak, >= 3.0 and < 4.0 is developing)
    rows = [make_row(f"p{i}", "strings", 3) for i in range(3)]
    scores = grind.compute_gap_scores(rows)
    # avg == 3.0: should be developing (not < 3.0)
    assert scores.get("strings") == "developing"


def test_topics_not_in_rows_remain_unknown(grind):
    rows = [make_row(f"p{i}", "arrays", 5) for i in range(5)]
    scores = grind.compute_gap_scores(rows)
    # dp, graphs etc. not in rows — should be 'unknown'
    unknown_topics = [t for t, s in scores.items() if t != "arrays" and s == "unknown"]
    assert len(unknown_topics) > 0
