"""
grind_paths — shared path constants for grindcoach.
All other modules import from here so monkeypatching propagates everywhere.
"""
import os

_HERE = os.path.dirname(os.path.realpath(__file__))

PROJECT_ROOT      = _HERE
MEMORY_FILE       = os.path.join(_HERE, 'memory.md')
ARCHIVE_FILE      = os.path.join(_HERE, 'memory_archive.md')
CONFIG_FILE       = os.path.join(_HERE, '.lc_config.json')
SESSION_FILE      = os.path.join(_HERE, '.session.json')
BEHAVIOR_FILE     = os.path.join(_HERE, 'behavior.jsonl')
PROBLEMS_FILE     = os.path.join(_HERE, 'problems.json')
ARCHIVE_THRESHOLD = 50
