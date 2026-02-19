"""
Tests for atomic save_config() — tmp+replace pattern with .bak.
"""
import os
import pytest
from conftest import import_grind


@pytest.fixture(scope="module")
def grind():
    return import_grind()


def test_save_config_creates_bak(tmp_env):
    g, tmp = tmp_env
    g.save_config({"active_track": "blind75"})
    assert os.path.exists(g.CONFIG_FILE + ".bak")


def test_save_config_no_tmp_leftover(tmp_env):
    g, tmp = tmp_env
    g.save_config({"active_track": "blind75"})
    assert not os.path.exists(g.CONFIG_FILE + ".tmp")


def test_save_config_bak_matches_main(tmp_env):
    g, tmp = tmp_env
    g.save_config({"active_track": "neetcode150"})
    main = open(g.CONFIG_FILE).read()
    bak  = open(g.CONFIG_FILE + ".bak").read()
    assert main == bak


def test_save_and_load_roundtrip(tmp_env):
    g, tmp = tmp_env
    cfg = {"active_track": "blind75", "active_target": "foo-001"}
    g.save_config(cfg)
    loaded = g.load_config()
    assert loaded["active_track"] == "blind75"
    assert loaded["active_target"] == "foo-001"
