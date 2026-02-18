"""
Tests for target management and merge overlap algorithm.

Merge classification:
- overlap >= 60% → combined
- 30% <= overlap < 60% → hybrid
- overlap < 30% → separate
"""
import json
import pytest
from conftest import import_grind


@pytest.fixture(scope="module")
def grind():
    return import_grind()


def make_target(skills):
    return {"required_skills": skills, "company": "TestCo", "role": "SWE"}


def compute_overlap(skills_a, skills_b):
    a = set(skills_a)
    b = set(skills_b)
    shared = a & b
    total = a | b
    if not total:
        return 0.0
    return len(shared) / len(total)


def test_next_target_id_first(tmp_env):
    g, tmp = tmp_env
    config = {"targets": {}}
    tid = g._next_target_id(config, "google")
    assert tid == "google-001"


def test_next_target_id_increments(tmp_env):
    g, tmp = tmp_env
    config = {"targets": {"google-001": {}, "google-002": {}}}
    tid = g._next_target_id(config, "google")
    assert tid == "google-003"


def test_next_target_id_company_slug(tmp_env):
    g, tmp = tmp_env
    config = {"targets": {}}
    tid = g._next_target_id(config, "BMW Group")
    # Slug is derived from company name — just verify it ends with -001
    assert tid.endswith("-001")


# --- Overlap calculation ---

def test_full_overlap_is_combined():
    skills = ["C++", "graphs", "distributed-systems"]
    ratio = compute_overlap(skills, skills)
    assert ratio == 1.0
    assert ratio >= 0.6  # combined


def test_high_overlap_is_combined():
    a = ["C++", "graphs", "distributed-systems", "REST"]
    b = ["C++", "graphs", "distributed-systems", "ML"]
    ratio = compute_overlap(a, b)
    assert ratio >= 0.6


def test_moderate_overlap_is_hybrid():
    # shared={"graphs","distributed"} total=6 → ratio=2/6≈0.33
    a = ["C++", "graphs", "distributed", "REST"]
    b = ["Python", "graphs", "distributed", "ML"]
    ratio = compute_overlap(a, b)
    assert 0.3 <= ratio < 0.6


def test_low_overlap_is_separate():
    a = ["C++", "RTOS", "embedded", "automotive"]
    b = ["Python", "ML", "TensorFlow", "data-pipelines"]
    ratio = compute_overlap(a, b)
    assert ratio < 0.3


def test_empty_skills_both():
    ratio = compute_overlap([], [])
    assert ratio == 0.0


def test_empty_skills_one_side():
    ratio = compute_overlap(["C++", "graphs"], [])
    assert ratio == 0.0


def test_identical_single_skill():
    ratio = compute_overlap(["graphs"], ["graphs"])
    assert ratio == 1.0


# --- Config round-trip for targets ---

def test_target_saved_to_config(tmp_env):
    g, tmp = tmp_env
    config = {"targets": {}, "active_target": None}
    tid = "bmw-001"
    config["targets"][tid] = {
        "id": tid,
        "company": "BMW Group",
        "role": "SWE",
        "interview_date": "2026-03-10",
        "preferred_language": "cpp",
        "required_skills": ["C++17", "graphs", "REST"],
        "intelligence": {},
        "plan": {},
    }
    g.save_config(config)
    reloaded = g.load_config()
    assert "bmw-001" in reloaded["targets"]
    assert reloaded["targets"]["bmw-001"]["company"] == "BMW Group"


def test_target_update_field(tmp_env):
    g, tmp = tmp_env
    # Set up a config with a target first
    config = {
        "active_track": "blind75",
        "targets": {
            "bmw-001": {
                "id": "bmw-001",
                "company": "BMW Group",
                "role": "SWE",
                "interview_date": "2026-03-10",
                "preferred_language": "cpp",
                "required_skills": ["C++17", "graphs"],
                "intelligence": {},
                "plan": {},
            }
        },
    }
    g.save_config(config)
    config = g.load_config()
    config["targets"]["bmw-001"]["required_skills"] = ["C++17", "REST", "graphs", "distributed"]
    g.save_config(config)
    reloaded = g.load_config()
    assert "distributed" in reloaded["targets"]["bmw-001"]["required_skills"]
