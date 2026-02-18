"""
Shared test fixtures and grind module import helper.
grind has no .py extension; import via importlib.
"""
import os
import sys
import importlib.util
import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def import_grind():
    """Import the grind executable as a Python module.
    Uses SourceFileLoader because grind has no .py extension.
    """
    import importlib.machinery
    path = os.path.join(REPO_ROOT, "grind")
    loader = importlib.machinery.SourceFileLoader("grind", path)
    spec = importlib.util.spec_from_loader("grind", loader)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def grind():
    return import_grind()


@pytest.fixture()
def tmp_env(tmp_path, monkeypatch):
    """Redirect all file paths to a temp directory for isolation."""
    g = import_grind()
    monkeypatch.setattr(g, "PROJECT_ROOT", str(tmp_path))
    monkeypatch.setattr(g, "MEMORY_FILE", str(tmp_path / "memory.md"))
    monkeypatch.setattr(g, "ARCHIVE_FILE", str(tmp_path / "memory_archive.md"))
    monkeypatch.setattr(g, "CONFIG_FILE", str(tmp_path / ".lc_config.json"))
    monkeypatch.setattr(g, "SESSION_FILE", str(tmp_path / ".session.json"))
    monkeypatch.setattr(g, "BEHAVIOR_FILE", str(tmp_path / "behavior.jsonl"))
    return g, tmp_path
