"""
The five ablation metrics (Experiment_Spec.md §3) over normalized events
(see metrics.events for the schema). Pure functions; offline; tested on
synthetic fixtures in tests/test_metrics.py.
"""

from typing import Any, Dict, List, Optional

from hexis.detector import stagnation_count  # noqa: F401  (metric 3 lives in hexis)

from .events import actions, compactions


def actions_per_level(events: List[Dict[str, Any]]) -> Dict[int, int]:
    """Metric 1a: action count per level."""
    counts: Dict[int, int] = {}
    for ev in actions(events):
        counts[ev["level"]] = counts.get(ev["level"], 0) + 1
    return counts


def vs_human_baseline(
    per_level: Dict[int, int], human_baseline: Dict[int, int]
) -> Dict[int, Optional[float]]:
    """Metric 1b: agent/human action ratio per level (RHAE-style, as ARC
    Prize computes it — human baselines come from the VISTA per-game table,
    Sources/VISTA_2026.md). None where the baseline is missing."""
    return {
        level: (count / human_baseline[level] if human_baseline.get(level) else None)
        for level, count in per_level.items()
    }


def post_handoff_burn(
    events: List[Dict[str, Any]], window: int = 20
) -> List[int]:
    """Metric 2: per compaction, the number of actions within the first
    `window` turns after the handoff before the first state-changing press
    (the cost of discontinuity). `window` if nothing changed state."""
    acts = actions(events)
    burns = []
    for comp in compactions(events):
        after = [a for a in acts if a["turn"] > comp["turn"]][:window]
        burn = window if after else 0
        for i, a in enumerate(after):
            if a["frame_changed"]:
                burn = i
                break
        burns.append(burn)
    return burns


def prediction_accuracy(
    events: List[Dict[str, Any]], post_window: int = 20
) -> Dict[str, Optional[float]]:
    """Metric 4: fraction of graded predictions correct, split by pre- vs
    post-handoff (post = within `post_window` turns after any compaction)."""
    comp_turns = [c["turn"] for c in compactions(events)]

    def is_post(turn: int) -> bool:
        return any(ct < turn <= ct + post_window for ct in comp_turns)

    buckets: Dict[str, List[bool]] = {"pre": [], "post": [], "overall": []}
    for ev in actions(events):
        if ev.get("prediction_correct") is None:
            continue
        correct = ev["prediction_correct"]
        buckets["overall"].append(correct)
        buckets["post" if is_post(ev["turn"]) else "pre"].append(correct)

    return {
        k: (sum(v) / len(v) if v else None) for k, v in buckets.items()
    }


def note_tokens_per_compaction(events: List[Dict[str, Any]]) -> List[int]:
    """Metric 5: note tokens at each compaction (the memory-efficiency
    question, now with a task attached)."""
    return [c["note_tokens"] for c in compactions(events)]
