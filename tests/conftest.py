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
    # Ensure grind_paths is importable from the repo root
    if REPO_ROOT not in sys.path:
        sys.path.insert(0, REPO_ROOT)

    patches = {
        "PROJECT_ROOT":  str(tmp_path),
        "MEMORY_FILE":   str(tmp_path / "memory.md"),
        "ARCHIVE_FILE":  str(tmp_path / "memory_archive.md"),
        "CONFIG_FILE":   str(tmp_path / ".lc_config.json"),
        "SESSION_FILE":  str(tmp_path / ".session.json"),
        "BEHAVIOR_FILE": str(tmp_path / "behavior.jsonl"),
    }

    # Patch the shared constants module so grind_data / grind_algos see temp paths
    try:
        import grind_paths
        for attr, val in patches.items():
            monkeypatch.setattr(grind_paths, attr, val)
    except ImportError:
        pass  # grind_paths not yet split out — no-op

    g = import_grind()

    # Also patch g directly (monolith grind keeps its own module-level constants)
    for attr, val in patches.items():
        monkeypatch.setattr(g, attr, val)

    return g, tmp_path
