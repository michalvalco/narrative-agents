"""Offline tests for run_step0: the dry run must pass with zero side
effects, and the live flag must refuse (Gotchas #276)."""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import run_step0


def test_compaction_turns_schedule():
    assert run_step0.compaction_turns(100, 30) == [30, 60, 90]
    assert run_step0.compaction_turns(30, 30) == [30]
    assert run_step0.compaction_turns(29, 30) == []


def test_write_cost_record_validates_fields(tmp_path):
    path = str(tmp_path / "cost.jsonl")
    with pytest.raises(ValueError):
        run_step0.write_cost_record(path, {"turn": 1})
    run_step0.write_cost_record(path, {
        "turn": 1, "input_tokens": 10, "output_tokens": 2,
        "cache_read_tokens": 8, "cache_write_tokens": 0,
    })
    rec = json.loads(open(path, encoding="utf-8").read())
    assert rec["turn"] == 1 and "recorded_at" in rec


def test_dry_run_passes(capsys):
    assert run_step0.main(["--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "checks passed" in out
    assert "NOT executed" in out


def test_live_refuses(capsys):
    assert run_step0.main(["--live"]) == 2
    out = capsys.readouterr().out
    assert "REFUSED" in out
