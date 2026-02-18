"""
Tests for SM-2 spaced repetition algorithm.

SM-2 rules:
- Rating < 3 → reset: interval=1, repetition=0, ease stays (min 1.3)
- Rating >= 3 → interval grows, ease factor adjusts
- Ease factor never drops below 1.3
- Interval sequence for first repetitions: 1 → 6 → ... (grows by ease factor)
"""
import pytest
from conftest import import_grind


@pytest.fixture(scope="module")
def grind():
    return import_grind()


def test_first_attempt_rating5(grind):
    ease, interval, rep = grind.sm2_calculate(5, prev_ease=2.5, prev_interval=0, repetition=0)
    assert interval == 1
    assert rep == 1
    assert ease > 2.5  # rating 5 increases ease


def test_second_attempt_rating5(grind):
    ease, interval, rep = grind.sm2_calculate(5, prev_ease=2.6, prev_interval=1, repetition=1)
    assert interval == 6
    assert rep == 2


def test_third_attempt_grows_by_ease(grind):
    import math
    ease, interval, rep = grind.sm2_calculate(5, prev_ease=2.6, prev_interval=6, repetition=2)
    # SM-2 uses ceil(prev_interval * new_ease)
    assert interval == math.ceil(6 * ease)
    assert rep == 3


def test_rating3_keeps_increasing(grind):
    ease, interval, rep = grind.sm2_calculate(3, prev_ease=2.5, prev_interval=6, repetition=2)
    assert interval > 6
    assert rep == 3


def test_rating2_resets(grind):
    ease, interval, rep = grind.sm2_calculate(2, prev_ease=2.5, prev_interval=30, repetition=5)
    assert interval == 1
    assert rep == 0


def test_rating1_resets(grind):
    ease, interval, rep = grind.sm2_calculate(1, prev_ease=2.5, prev_interval=100, repetition=10)
    assert interval == 1
    assert rep == 0


def test_ease_never_below_1_3(grind):
    # After many bad ratings, ease should not go below 1.3
    ease = 2.5
    for _ in range(20):
        ease, _, _ = grind.sm2_calculate(2, prev_ease=ease, prev_interval=1, repetition=0)
    assert ease >= 1.3


def test_ease_increases_on_rating5(grind):
    ease1, _, _ = grind.sm2_calculate(5, prev_ease=2.5, prev_interval=6, repetition=2)
    ease2, _, _ = grind.sm2_calculate(3, prev_ease=2.5, prev_interval=6, repetition=2)
    assert ease1 > ease2


def test_all_valid_ratings_produce_valid_output(grind):
    for rating in range(1, 6):
        ease, interval, rep = grind.sm2_calculate(
            rating, prev_ease=2.5, prev_interval=6, repetition=2
        )
        assert ease >= 1.3
        assert interval >= 1
        assert rep >= 0
