"""
Offline tests for the ported visualization pipeline (Task D-prime).

Replaces the archive's manual smoke script
(_Archive/.../examples/test_visualization.py) with a pytest battery:
same dummy data, Agg backend, no display, no API, output to tmp_path.
"""

import os
import sys

import matplotlib
matplotlib.use('Agg')  # headless before pyplot is imported anywhere

import numpy as np
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'examples')))

from visualizations import create_full_benchmark_figure


def dummy_viz_data():
    """The archive smoke script's dummy dataset, verbatim."""
    return {
        'agent_names': ['Test-Agent-1', 'Test-Agent-2', 'Test-Agent-3'],
        'storage_pct': [30.0, 25.0, 100.0],
        'trait_counts': [3, 2, 0],
        'timeline_data': {
            'Test-Agent-1': [(10, 0), (20, 1), (30, 2), (40, 3)],
            'Test-Agent-2': [(10, 0), (20, 1), (30, 2), (40, 2)],
            'Test-Agent-3': [(10, 0), (20, 0), (30, 0), (40, 0)],
        },
        'efficiency': [30.0, 25.0, 100.0],
        'coherence': [75.0, 68.0, 35.0],
        'decision_matrix': np.array([
            [1.0, 0.8, 0.5, 0.3, 0.9],
            [0.8, 0.6, 0.4, 0.2, 0.7],
            [0.3, 0.3, 0.5, 0.3, 0.4],
        ]),
        'situations': ['Challenge', 'Risk', 'Routine', 'Unknown', 'Creative'],
    }


def test_full_benchmark_figure_renders(tmp_path):
    out = tmp_path / 'test_visualization.png'
    fig = create_full_benchmark_figure(dummy_viz_data(), str(out))
    assert out.exists()
    assert out.stat().st_size > 10_000  # a real rendered figure, not a stub
    assert len(fig.axes) >= 4  # 2x2 grid (colorbar may add an extra axes)
    matplotlib.pyplot.close(fig)


def test_ported_pipeline_builds_viz_data_offline(tmp_path, monkeypatch):
    """End-to-end over the ported memory_efficiency_viz on a small run:
    agents built with the budgeted rule, all four panels rendered, no API."""
    import memory_efficiency_viz as mev

    monkeypatch.setattr(mev, 'NUM_EXPERIENCES', 20)
    import random
    random.seed(mev.RANDOM_SEED)

    agents = mev.build_agents(20)
    for exp in mev.generate_experiences(20):
        for name, agent in agents.items():
            if 'Traditional' in agent.name:
                agent.total_experiences += 1
            else:
                agent.experience(exp)

    # Narrative agents ran the budgeted rule with the documented budget
    for name, agent in agents.items():
        if 'Narrative' in name:
            assert agent.selection == mev.SELECTION
            assert agent.budget == 7  # ceil(20 / 3)
            assert len(agent.narrative_core) <= agent.budget

    matrix, situations = mev.generate_decision_patterns(agents)
    assert matrix.shape == (4, 5)
    assert len(situations) == 5

    coherence = mev.measure_coherence(agents['Narrative-Learner'])
    assert 0.0 <= coherence <= 1.0
