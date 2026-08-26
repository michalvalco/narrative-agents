"""Offline tests for the hexis stagnation detector."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hexis import disposition_line, stagnation_count, stagnation_runs


def act(turn, action, changed):
    return {"kind": "action", "turn": turn, "level": 1, "action": action,
            "frame_changed": changed, "prediction": None, "prediction_correct": None}


def test_detects_repeated_single_action():
    events = [act(1, "ACTION1", True),
              act(2, "ACTION4", False), act(3, "ACTION4", False), act(4, "ACTION4", False),
              act(5, "ACTION2", True)]
    runs = stagnation_runs(events)
    assert runs == [(2, ["ACTION4"], 3)]
    assert stagnation_count(events) == 1


def test_detects_repeated_sequence():
    events = [act(1, "ACTION1", False), act(2, "ACTION2", False),
              act(3, "ACTION1", False), act(4, "ACTION2", False)]
    runs = stagnation_runs(events)
    assert runs == [(1, ["ACTION1", "ACTION2"], 2)]


def test_state_change_breaks_the_run():
    events = [act(1, "ACTION4", False), act(2, "ACTION4", True),
              act(3, "ACTION4", False), act(4, "ACTION4", True)]
    assert stagnation_runs(events) == []
    assert disposition_line(events) is None


def test_disposition_line_names_worst_episode():
    events = [act(1, "ACTION3", False), act(2, "ACTION3", False),
              act(3, "ACTION5", True),
              act(4, "ACTION4", False), act(5, "ACTION4", False),
              act(6, "ACTION4", False), act(7, "ACTION4", False)]
    line = disposition_line(events)
    assert line is not None
    assert "[ACTION4] 4x" in line
    assert "turn 4" in line
    assert line.count("\n") == 0  # one line, fit for the Self-knowledge slot


def test_compaction_events_are_ignored():
    events = [act(1, "ACTION4", False),
              {"kind": "compaction", "turn": 1, "note_tokens": 100},
              act(2, "ACTION4", False)]
    assert stagnation_runs(events) == [(1, ["ACTION4"], 2)]
