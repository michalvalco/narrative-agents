"""
Basic core tests, ported 2026-08-26 from
_Archive/.../old files/tests/test_narrative_agents.py (October 2025)
into pytest form and extended for the selection-rule defaults.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from narrative_agents.core import NarrativeAgent, Experience, Telos


def test_agent_creation():
    agent = NarrativeAgent("TestAgent", Telos.LEARNING)
    assert agent.name == "TestAgent"
    assert agent.telos == Telos.LEARNING
    assert agent.total_experiences == 0
    # Post-2026-08-22 defaults: budgeted selection, floor 0.30,
    # budget = ceil(context_window / 3) when expected_n is not given
    assert agent.selection == "budgeted"
    assert agent.floor == 0.30
    assert agent.budget == 17


def test_experience_processing():
    agent = NarrativeAgent("Learner", Telos.LEARNING)

    exp = Experience('error', 'Test error occurred', emotional_valence=-0.5)
    memory = agent.experience(exp)

    assert agent.total_experiences == 1
    assert memory.interpretation == "valuable lesson about limitations"
    assert memory.relevance == agent.raw_scores[0]
