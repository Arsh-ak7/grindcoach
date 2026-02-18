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


# --- Merge bug fixes (interview_date + skills breakdown) ---

def _setup_two_targets(g, date1="2026-04-01", date2="2026-03-15"):
    """Helper: create two targets with skills in config."""
    config = {
        "active_track": "blind75",
        "targets": {
            "g-001": {
                "id": "g-001", "company": "Google", "role": "SWE",
                "interview_date": date1, "preferred_language": "python",
                "required_skills": ["Python", "graphs", "distributed-systems", "ML"],
                "intelligence": {}, "plan": {},
            },
            "b-001": {
                "id": "b-001", "company": "BMW", "role": "SWE",
                "interview_date": date2, "preferred_language": "cpp",
                "required_skills": ["C++", "graphs", "distributed-systems", "automotive"],
                "intelligence": {}, "plan": {},
            },
        },
    }
    g.save_config(config)
    return g.load_config()


def test_merge_creates_merged_target(tmp_env):
    g, tmp = tmp_env
    _setup_two_targets(g)
    import argparse
    args = argparse.Namespace(target_cmd="merge", id1="g-001", id2="b-001")
    g.cmd_target(args)
    config = g.load_config()
    assert "merged-g-001-b-001" in config["targets"]


def test_merge_inherits_earliest_interview_date(tmp_env):
    g, tmp = tmp_env
    _setup_two_targets(g, date1="2026-04-01", date2="2026-03-15")
    import argparse
    args = argparse.Namespace(target_cmd="merge", id1="g-001", id2="b-001")
    g.cmd_target(args)
    merged = g.load_config()["targets"]["merged-g-001-b-001"]
    # Should inherit the earlier date (BMW's 2026-03-15)
    assert merged["interview_date"] == "2026-03-15"


def test_merge_has_company_and_role(tmp_env):
    g, tmp = tmp_env
    _setup_two_targets(g)
    import argparse
    args = argparse.Namespace(target_cmd="merge", id1="g-001", id2="b-001")
    g.cmd_target(args)
    merged = g.load_config()["targets"]["merged-g-001-b-001"]
    assert "company" in merged
    assert "role" in merged
    assert "Google" in merged["company"] or "BMW" in merged["company"]


def test_merge_skills_breakdown_keys(tmp_env):
    g, tmp = tmp_env
    _setup_two_targets(g)
    import argparse
    args = argparse.Namespace(target_cmd="merge", id1="g-001", id2="b-001")
    g.cmd_target(args)
    merged = g.load_config()["targets"]["merged-g-001-b-001"]
    assert "shared_skills" in merged
    assert "graphs" in merged["shared_skills"]
    assert "distributed-systems" in merged["shared_skills"]
    assert "required_skills" in merged  # union of all skills


def test_merge_plan_generate_works(tmp_env):
    """Merged target must have interview_date so plan generate doesn't fail."""
    g, tmp = tmp_env
    _setup_two_targets(g)
    import argparse
    args = argparse.Namespace(target_cmd="merge", id1="g-001", id2="b-001")
    g.cmd_target(args)
    config = g.load_config()
    mid = "merged-g-001-b-001"
    ok, msg = g._generate_plan_for_target(config, mid)
    assert ok, f"Plan generation failed: {msg}"
