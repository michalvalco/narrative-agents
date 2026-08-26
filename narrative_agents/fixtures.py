"""
Canonical experience fixtures.

`balanced_experiences` is the set Experiment_Spec.md §6 requires for any
re-run whose numbers are reported: two experiences per type across
error / failure / success / discovery / neutral, so no telos is favored
by the composition of the set itself (the v2 set was 6/10 errors and
failures, which favored the learning telos).

`canonical_v2_experiences` mirrors examples/compare_rule_vs_llm.py's
create_experiences() so tests can reproduce the v2 run-log numbers
without importing the example script; a drift-guard test asserts the
two stay identical.
"""

from .core import Experience


def balanced_experiences():
    """Two experiences per type; valences balanced within each type."""
    return [
        Experience('error', 'Misread the puzzle grid orientation', 'wrong_move', -0.5),
        Experience('error', 'Pressed a control with no written prediction', 'wasted_turn', -0.3),
        Experience('failure', 'Level attempt ran out of moves', 'level_reset', -0.7),
        Experience('failure', 'Repeated a sequence that changed nothing', 'stagnation', -0.4),
        Experience('success', 'Predicted the frame change exactly', 'confirmed_rule', 0.7),
        Experience('success', 'Completed the level under the action budget', 'level_clear', 0.8),
        Experience('discovery', 'Found that color marks the movable block', 'new_rule', 0.8),
        Experience('discovery', 'Noticed the counter resets on wall contact', 'insight', 0.6),
        Experience('neutral', 'Observed the start frame', 'noted', 0.0),
        Experience('neutral', 'Replayed the recording index', 'noted', 0.1),
    ]


def canonical_v2_experiences():
    """The v2 canonical set (12 experiences; 6 are errors/failures)."""
    return [
        Experience('error', 'Failed to recognise pattern in data', 'crash', -0.7),
        Experience('success', 'Optimised algorithm performance by 40%', 'celebration', 0.9),
        Experience('discovery', 'Found unexpected correlation in dataset', 'insight', 0.8),
        Experience('error', 'Memory allocation exceeded limits', 'recovery', -0.5),
        Experience('failure', 'Lost important user data during processing', 'devastation', -0.9),
        Experience('success', 'Correctly predicted user behaviour', 'validation', 0.7),
        Experience('error', 'Misinterpreted ambiguous command', 'confusion', -0.3),
        Experience('discovery', 'Identified new problem-solving approach', 'excitement', 0.9),
        Experience('success', 'Maintained 99.9% uptime for the month', 'pride', 0.8),
        Experience('failure', 'Failed to meet performance benchmark', 'disappointment', -0.6),
        Experience('error', 'Recursive loop caused stack overflow', 'learning', -0.4),
        Experience('discovery', 'User taught me unexpected use case', 'growth', 0.7),
    ]
