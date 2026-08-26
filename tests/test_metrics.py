"""Offline tests for the ablation metrics on a synthetic event stream."""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from metrics import (
    actions_per_level,
    count_tokens,
    load_toolkit_jsonl,
    note_tokens_per_compaction,
    post_handoff_burn,
    prediction_accuracy,
    vs_human_baseline,
)


def act(turn, level=1, action="ACTION1", changed=True, correct=None):
    return {"kind": "action", "turn": turn, "level": level, "action": action,
            "frame_changed": changed, "prediction": "change" if correct is not None else None,
            "prediction_correct": correct}


def comp(turn, note_tokens=800):
    return {"kind": "compaction", "turn": turn, "note_tokens": note_tokens}


@pytest.fixture
def stream():
    """34 turns, one compaction at 30; post-handoff burn of 2."""
    events = []
    for t in range(1, 31):
        events.append(act(t, level=1 if t <= 20 else 2, correct=(t % 3 != 0)))
    events.append(comp(30, note_tokens=750))
    events.append(act(31, level=2, changed=False, correct=False))
    events.append(act(32, level=2, changed=False, correct=False))
    events.append(act(33, level=2, changed=True, correct=True))
    events.append(act(34, level=2, changed=True, correct=True))
    return events


def test_actions_per_level(stream):
    assert actions_per_level(stream) == {1: 20, 2: 14}


def test_vs_human_baseline(stream):
    per_level = actions_per_level(stream)
    ratios = vs_human_baseline(per_level, {1: 10, 2: 28})
    assert ratios[1] == 2.0
    assert ratios[2] == 0.5
    assert vs_human_baseline(per_level, {1: 10})[2] is None


def test_post_handoff_burn(stream):
    # turns 31, 32 change nothing; 33 is the first state-changing press
    assert post_handoff_burn(stream, window=20) == [2]


def test_post_handoff_burn_saturates_at_window():
    events = [act(t) for t in range(1, 31)]
    events.append(comp(30))
    events += [act(t, changed=False) for t in range(31, 41)]
    assert post_handoff_burn(events, window=20) == [20]  # nothing changed → window


def test_prediction_accuracy_split(stream):
    accs = prediction_accuracy(stream, post_window=20)
    # pre: turns 1..30, correct unless divisible by 3 → 20/30
    assert accs["pre"] == pytest.approx(20 / 30)
    # post: turns 31-34 → [F, F, T, T]
    assert accs["post"] == pytest.approx(0.5)
    assert accs["overall"] == pytest.approx((20 + 2) / 34)


def test_prediction_accuracy_ignores_ungraded():
    events = [act(1, correct=None), act(2, correct=True)]
    accs = prediction_accuracy(events)
    assert accs["overall"] == 1.0


def test_note_tokens_per_compaction(stream):
    assert note_tokens_per_compaction(stream) == [750]


def test_count_tokens_heuristic():
    assert count_tokens("") == 0
    assert count_tokens("abcd") == 1
    assert count_tokens("abcde") == 2


def test_load_toolkit_jsonl_envelope(tmp_path):
    good = tmp_path / "rec.jsonl"
    lines = [
        {"timestamp": "2026-08-26T00:00:00+00:00", "data": {"action": "ACTION1"}},
        {"timestamp": "2026-08-26T00:00:01+00:00", "data": {"action": "ACTION2"}},
    ]
    good.write_text("\n".join(json.dumps(l) for l in lines), encoding="utf-8")
    payloads = load_toolkit_jsonl(str(good))
    assert [p["action"] for p in payloads] == ["ACTION1", "ACTION2"]

    bad = tmp_path / "bad.jsonl"
    bad.write_text('{"no_envelope": true}', encoding="utf-8")
    with pytest.raises(ValueError):
        load_toolkit_jsonl(str(bad))
