"""
Tests for memory.md atomic write and parse/round-trip.

Critical invariants:
- write_memory uses os.replace (atomic on POSIX)
- A .bak copy is always maintained
- parse_memory correctly reads all fields
- Round-trip: write then parse produces identical rows
"""
import os
import shutil
import pytest
from conftest import import_grind
from datetime import datetime, timedelta


@pytest.fixture(scope="module")
def grind():
    return import_grind()


def make_rows(n=3):
    today = datetime.now()
    rows = []
    for i in range(n):
        rows.append({
            "slug": f"problem-{i}",
            "topic": "arrays",
            "difficulty": "easy",
            "date": (today - timedelta(days=i)).strftime("%Y-%m-%d"),
            "rating": 4,
            "ease": 2.5,
            "interval": 6,
            "repetition": 2,
            "next_review": (today + timedelta(days=6)).strftime("%Y-%m-%d"),
            "time": 20,   # write_memory uses 'time' not 'time_min'
            "hints": 0,
        })
    return rows


def test_write_creates_memory_file(tmp_env):
    g, tmp = tmp_env
    rows = make_rows(3)
    g.write_memory(rows)
    assert os.path.exists(g.MEMORY_FILE)


def test_write_creates_bak_file(tmp_env):
    g, tmp = tmp_env
    rows = make_rows(3)
    g.write_memory(rows)
    bak_path = g.MEMORY_FILE + ".bak"
    assert os.path.exists(bak_path)


def test_bak_matches_memory(tmp_env):
    g, tmp = tmp_env
    rows = make_rows(3)
    g.write_memory(rows)
    with open(g.MEMORY_FILE) as f:
        mem_content = f.read()
    with open(g.MEMORY_FILE + ".bak") as f:
        bak_content = f.read()
    assert mem_content == bak_content


def test_round_trip(tmp_env):
    g, tmp = tmp_env
    rows = make_rows(5)
    g.write_memory(rows)
    parsed = g.parse_memory()
    assert len(parsed) == 5
    for original, recovered in zip(rows, parsed):
        assert recovered["slug"] == original["slug"]
        assert recovered["rating"] == original["rating"]
        assert float(recovered["ease"]) == pytest.approx(original["ease"], abs=0.01)


def test_recovery_from_backup(tmp_env):
    g, tmp = tmp_env
    rows = make_rows(4)
    g.write_memory(rows)
    bak_path = g.MEMORY_FILE + ".bak"
    # Simulate corruption
    with open(g.MEMORY_FILE, "w") as f:
        f.write("CORRUPTED\n")
    # Restore from .bak
    shutil.copy(bak_path, g.MEMORY_FILE)
    parsed = g.parse_memory()
    assert len(parsed) == 4


def test_empty_memory_parses_to_empty_list(tmp_env):
    g, tmp = tmp_env
    g.write_memory([])
    parsed = g.parse_memory()
    assert parsed == []


def test_write_over_existing(tmp_env):
    g, tmp = tmp_env
    g.write_memory(make_rows(2))
    g.write_memory(make_rows(7))  # overwrite with more rows
    parsed = g.parse_memory()
    assert len(parsed) == 7


# --- _append_notes tests ---

def test_notes_creates_notes_md(tmp_env):
    g, tmp = tmp_env
    (tmp / "problems" / "two_sum").mkdir(parents=True)
    g._append_notes("two-sum", "use a hash map", "2026-02-19", 4)
    notes_path = tmp / "problems" / "two_sum" / "notes.md"
    assert notes_path.exists()
    assert "use a hash map" in notes_path.read_text()


def test_notes_appends_not_overwrites(tmp_env):
    g, tmp = tmp_env
    (tmp / "problems" / "two_sum").mkdir(parents=True, exist_ok=True)
    g._append_notes("two-sum", "first note", "2026-02-19", 4)
    g._append_notes("two-sum", "second note", "2026-02-19", 5)
    content = (tmp / "problems" / "two_sum" / "notes.md").read_text()
    assert "first note" in content and "second note" in content


def test_notes_creates_problem_dir_if_missing(tmp_env):
    g, tmp = tmp_env
    # No grind new called — dir doesn't exist yet
    g._append_notes("new-slug", "note for unseen problem", "2026-02-19", 3)
    assert (tmp / "problems" / "new_slug" / "notes.md").exists()
