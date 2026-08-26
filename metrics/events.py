"""
Normalized event stream for the ablation metrics.

Two raw inputs merge into one ordered stream of plain dicts:

1. The toolkit recording — `runs/<scorecard>/<game>-<guid>.jsonl`, one line
   per event shaped `{"timestamp": <iso>, "data": {...}}` (envelope
   verified against arc-agi==0.9.9 `wrapper.py::_record`; the `data`
   payload's field inventory is documented in Sources/ARC_toolkit_notes.md
   and has no formal upstream schema).
2. The harness annotations — predictions, grades, compaction boundaries,
   and note snapshots, which the toolkit recording does not carry.

Normalized schema (what every metric consumes):

  action event:      {"kind": "action", "turn": int, "level": int,
                      "action": str, "frame_changed": bool,
                      "prediction": str | None,
                      "prediction_correct": bool | None}
  compaction event:  {"kind": "compaction", "turn": int,
                      "note_tokens": int}

Events are ordered by turn; a compaction event sits between the turn it
follows and the next action.
"""

import json
from typing import Any, Dict, List


def load_toolkit_jsonl(path: str) -> List[Dict[str, Any]]:
    """Read a toolkit recording; validate the envelope; return the payloads."""
    payloads = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            event = json.loads(line)
            if "timestamp" not in event or "data" not in event:
                raise ValueError(
                    f"{path}:{i + 1}: not a toolkit recording line "
                    f"(missing timestamp/data envelope)"
                )
            payloads.append(event["data"])
    return payloads


def actions(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [e for e in events if e.get("kind", "action") == "action"]


def compactions(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [e for e in events if e.get("kind") == "compaction"]
