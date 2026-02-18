"""
Tests for slug_to_folder() — the hyphen/underscore naming convention.

Design decision: user-facing slugs use hyphens (LeetCode canonical).
Internal folders use underscores (Java package name validity).
"""
import pytest
from conftest import import_grind


@pytest.fixture(scope="module")
def grind():
    return import_grind()


def test_simple_slug(grind):
    assert grind.slug_to_folder("two-sum") == "two_sum"


def test_multi_word_slug(grind):
    assert grind.slug_to_folder("best-time-to-buy-and-sell-stock") == "best_time_to_buy_and_sell_stock"


def test_single_word_slug(grind):
    assert grind.slug_to_folder("palindrome") == "palindrome"


def test_no_double_conversion(grind):
    # Underscore input is already internal form — passes through
    assert grind.slug_to_folder("two_sum") == "two_sum"


def test_valid_java_package_name(grind):
    result = grind.slug_to_folder("course-schedule-ii")
    assert "-" not in result
    assert result.replace("_", "").isalnum()


def test_known_problem_slugs(grind):
    cases = [
        ("two-sum", "two_sum"),
        ("valid-parentheses", "valid_parentheses"),
        ("longest-substring-without-repeating-characters",
         "longest_substring_without_repeating_characters"),
        ("coin-change", "coin_change"),
        ("number-of-islands", "number_of_islands"),
    ]
    for slug, expected in cases:
        assert grind.slug_to_folder(slug) == expected
