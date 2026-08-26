"""
Hexis rule: detect stagnation in a window of recorded turns and phrase it
as a one-line disposition for arm C's Self-knowledge slot (the ledger
update — Experiment_Spec.md §5). AVO needed a second agent to notice
stagnation; this asks whether a self-record can do it.

Pure functions over normalized action events (see metrics.events for the
schema). No I/O, no state, no API.
"""

from typing import Any, Dict, List, Optional, Tuple


def _no_change_runs(events: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
    """Maximal runs of consecutive action events with frame_changed False."""
    runs, current = [], []
    for ev in events:
        if ev.get("kind", "action") != "action":
            continue
        if not ev["frame_changed"]:
            current.append(ev)
        else:
            if current:
                runs.append(current)
            current = []
    if current:
        runs.append(current)
    return runs


def _periodic_prefix(actions: List[str], period: int) -> int:
    """Length of the prefix of `actions` that repeats with `period`."""
    n = 0
    while n < len(actions) and actions[n] == actions[n % period]:
        n += 1
    return n


def stagnation_runs(
    events: List[Dict[str, Any]], min_repeats: int = 2
) -> List[Tuple[int, List[str], int]]:
    """
    Find repeated action sequences with no frame change.

    Returns a list of (start_turn, pattern, repeats): within each maximal
    no-change run, the shortest action pattern repeated at least
    `min_repeats` full times from the run's start.
    """
    found = []
    for run in _no_change_runs(events):
        actions = [ev["action"] for ev in run]
        for period in range(1, len(actions) // min_repeats + 1):
            prefix = _periodic_prefix(actions, period)
            repeats = prefix // period
            if repeats >= min_repeats:
                found.append((run[0]["turn"], actions[:period], repeats))
                break
    return found


def stagnation_count(events: List[Dict[str, Any]], min_repeats: int = 2) -> int:
    """Metric 3 in Experiment_Spec.md §3: number of stagnation episodes."""
    return len(stagnation_runs(events, min_repeats=min_repeats))


def disposition_line(
    events: List[Dict[str, Any]], min_repeats: int = 2
) -> Optional[str]:
    """
    One line for arm C's Self-knowledge slot, or None if no stagnation.
    Reports the worst episode (most repeats) in the window.
    """
    runs = stagnation_runs(events, min_repeats=min_repeats)
    if not runs:
        return None
    turn, pattern, repeats = max(runs, key=lambda r: r[2])
    seq = ",".join(pattern)
    return (
        f"I repeated [{seq}] {repeats}x with no frame change from turn {turn} "
        f"- before repeating a sequence, I owe a written reason it should work this time."
    )
