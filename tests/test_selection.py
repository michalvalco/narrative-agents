"""
Offline tests for the selection rule (Experiment_Spec.md §6, ruled 2026-08-22).

No API calls anywhere in this file: LLM scoring is simulated by
ScriptedAgent, which replays a fixed score sequence through the same
admission path the live scorer would feed.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from narrative_agents.core import Experience, NarrativeAgent, Telos
from narrative_agents.fixtures import balanced_experiences, canonical_v2_experiences


class ScriptedAgent(NarrativeAgent):
    """Replays synthetic relevance scores in order (offline LLM stand-in)."""

    def __init__(self, scores, **kwargs):
        super().__init__(**kwargs)
        self._scores = list(scores)

    def _assess_relevance(self, exp: Experience) -> float:
        return self._scores.pop(0)


# The LLM Performer profile from the v2 run log: every score at or below
# 0.7, so the absolute rule admits nothing (the 0/10 artifact).
PERFORMER_LIKE_SCORES = [0.30, 0.55, 0.40, 0.10, 0.35, 0.60, 0.45, 0.65, 0.15, 0.50]


def test_cold_start_performer_acquires_inaugural_memory():
    """(1) An empty-core Performer must acquire an inaugural memory from
    the balanced set under synthetic scores — the cold-start bistability
    is broken by budgeted selection."""
    agent = ScriptedAgent(
        PERFORMER_LIKE_SCORES,
        telos=Telos.PERFORMING,
        selection="budgeted",
        expected_n=10,
    )
    for exp in balanced_experiences():
        agent.experience(exp)

    assert len(agent.narrative_core) > 0
    assert agent.narrative_core[0].inaugural
    assert len(agent.narrative_core) <= agent.budget
    # Character formation started (the loop the absolute rule never entered)
    assert agent.dispositions


def test_displacement_flags_the_weakest_non_inaugural():
    """(2) A full core admits a stronger memory and flags the displaced one."""
    agent = ScriptedAgent(
        [0.50, 0.40, 0.90],
        telos=Telos.LEARNING,
        selection="budgeted",
        budget=2,
    )
    exps = balanced_experiences()[:3]
    for exp in exps:
        agent.experience(exp)

    core_scores = [m.relevance for m in agent.narrative_core]
    assert sorted(core_scores) == [0.50, 0.90]
    assert agent.narrative_core[0].inaugural  # 0.50 stays pinned
    displaced = [m for m in agent.peripheral if m.displaced]
    assert len(displaced) == 1
    assert displaced[0].relevance == 0.40
    # Displaced memories keep their interpretation
    assert displaced[0].interpretation


def test_floor_keeps_trivia_out_of_an_empty_core():
    """(3) Below-floor scores never enter, even into an empty core."""
    agent = ScriptedAgent(
        [0.10, 0.20, 0.35],
        telos=Telos.EXPLORING,
        selection="budgeted",
        expected_n=10,
    )
    exps = balanced_experiences()[:3]
    agent.experience(exps[0])
    agent.experience(exps[1])
    assert len(agent.narrative_core) == 0
    assert len(agent.peripheral) == 2

    agent.experience(exps[2])  # 0.35 ≥ floor 0.30 → inaugural
    assert len(agent.narrative_core) == 1
    assert agent.narrative_core[0].inaugural


def test_absolute_reproduces_v2_run_log_counts():
    """(4) selection='absolute' reproduces the run-log counts.

    Rule-scorer path: canonical 12-set → LEARNING 6/12, PERFORMING 3/12
    (both re-verified live against the pre-change code, 2026-08-26).
    Synthetic path: the Performer-like all-≤0.7 profile → 0/10, the
    artifact the spec diagnoses; the same scores under budgeted → non-empty.
    """
    scholar = NarrativeAgent(telos=Telos.LEARNING, selection="absolute")
    performer = NarrativeAgent(telos=Telos.PERFORMING, selection="absolute")
    for exp in canonical_v2_experiences():
        scholar.experience(exp)
        performer.experience(exp)
    assert len(scholar.narrative_core) == 6
    assert len(performer.narrative_core) == 3

    llm_like = ScriptedAgent(
        PERFORMER_LIKE_SCORES, telos=Telos.PERFORMING, selection="absolute"
    )
    for exp in balanced_experiences():
        llm_like.experience(exp)
    assert len(llm_like.narrative_core) == 0  # the 0/10 artifact

    fixed = ScriptedAgent(
        PERFORMER_LIKE_SCORES,
        telos=Telos.PERFORMING,
        selection="budgeted",
        expected_n=10,
    )
    for exp in balanced_experiences():
        fixed.experience(exp)
    assert len(fixed.narrative_core) > 0


def test_budget_of_one_keeps_inaugural_pinned():
    """Re-choosing the beginning is re-emplotment — reserved for a later
    version. With budget 1 the inaugural memory is never displaced."""
    agent = ScriptedAgent(
        [0.40, 0.95, 0.99],
        telos=Telos.LEARNING,
        selection="budgeted",
        budget=1,
    )
    for exp in balanced_experiences()[:3]:
        agent.experience(exp)
    assert len(agent.narrative_core) == 1
    assert agent.narrative_core[0].relevance == 0.40
    assert agent.narrative_core[0].inaugural
    assert not any(m.displaced for m in agent.peripheral)


def test_raw_scores_always_logged_and_metrics_extended():
    """Raw score logged per experience; memory_efficiency reports budget,
    floor, raw-score distribution, and core composition by type."""
    agent = ScriptedAgent(
        PERFORMER_LIKE_SCORES,
        telos=Telos.PERFORMING,
        selection="budgeted",
        expected_n=10,
    )
    for exp in balanced_experiences():
        agent.experience(exp)

    stats = agent.memory_efficiency()
    assert stats['raw_scores'] == PERFORMER_LIKE_SCORES
    assert stats['raw_score_summary']['n'] == 10
    assert stats['raw_score_summary']['min'] == 0.10
    assert stats['raw_score_summary']['max'] == 0.65
    assert stats['budget'] == agent.budget
    assert stats['floor'] == 0.30
    assert stats['selection'] == 'budgeted'
    assert stats['telos'] == 'performing'
    assert sum(stats['core_composition_by_type'].values()) == len(agent.narrative_core)
    assert stats['displaced_count'] == sum(1 for m in agent.peripheral if m.displaced)


def test_invalid_selection_rejected():
    with pytest.raises(ValueError):
        NarrativeAgent(selection="competitive")


def test_fixture_matches_example_canonical_set():
    """Drift guard: canonical_v2_experiences mirrors the example script's
    create_experiences. If the example changes, this fails loudly instead
    of the two sets drifting apart silently (Gotchas #270)."""
    import importlib.util

    example_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'examples', 'compare_rule_vs_llm.py'
    ))
    spec = importlib.util.spec_from_file_location("compare_rule_vs_llm", example_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    ours = canonical_v2_experiences()
    theirs = module.create_experiences()
    assert len(ours) == len(theirs)
    for a, b in zip(ours, theirs):
        assert (a.type, a.content, a.outcome, a.emotional_valence) == (
            b.type, b.content, b.outcome, b.emotional_valence
        )
