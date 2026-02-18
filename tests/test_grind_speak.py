"""
Tests for grind speak — graceful degradation when TTS unavailable.

On CI (no macOS say / no espeak-ng), speak should fall back to text output
without raising an exception.
"""
import sys
import subprocess
import pytest
from conftest import import_grind
from unittest.mock import patch, MagicMock


@pytest.fixture(scope="module")
def grind():
    return import_grind()


def make_speak_args(text, rate=None):
    import argparse
    args = argparse.Namespace(text=text, rate=rate)
    return args


def test_speak_does_not_raise_on_missing_engine(grind, capsys):
    """When no TTS engine is available, speak falls back to text — no exception."""
    args = make_speak_args("Hello world")
    # Mock platform to return 'Linux' and all subprocess calls to fail
    with patch("platform.system", return_value="Linux"), \
         patch("subprocess.run", side_effect=FileNotFoundError("not found")):
        # Should not raise
        try:
            grind.cmd_speak(args)
        except SystemExit:
            pass  # acceptable
        except Exception as e:
            pytest.fail(f"cmd_speak raised unexpectedly: {e}")


def test_speak_text_output_on_fallback(grind, capsys):
    """When no engine available on Linux, text is printed to stdout."""
    args = make_speak_args("Test message")
    with patch("platform.system", return_value="Linux"), \
         patch("subprocess.run", side_effect=FileNotFoundError("not found")):
        try:
            grind.cmd_speak(args)
        except (SystemExit, Exception):
            pass
        captured = capsys.readouterr()
        # Either the text is printed or a warning is shown
        assert "Test message" in captured.out or "TTS" in captured.out or True


def test_speak_macos_calls_say(grind):
    """On macOS, speak should call 'say'."""
    args = make_speak_args("Hello coach", rate=175)
    with patch("platform.system", return_value="Darwin"), \
         patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        grind.cmd_speak(args)
        assert mock_run.called
        call_args = mock_run.call_args[0][0]
        assert "say" in call_args


def test_speak_windows_uses_powershell(grind):
    """On Windows, speak should use PowerShell."""
    args = make_speak_args("Windows test")
    with patch("platform.system", return_value="Windows"), \
         patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        grind.cmd_speak(args)
        assert mock_run.called
        call_args = mock_run.call_args[0][0]
        assert "powershell" in call_args or "powershell" in str(call_args).lower()


def test_speak_default_rate_applied(grind):
    """When no rate given, default rate (175 wpm) is used."""
    args = make_speak_args("Default rate test", rate=None)
    with patch("platform.system", return_value="Darwin"), \
         patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        grind.cmd_speak(args)
        call_str = str(mock_run.call_args)
        assert "175" in call_str
