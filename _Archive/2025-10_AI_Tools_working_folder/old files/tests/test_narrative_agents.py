"""
Basic tests for Narrative Agents
"""

import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from narrative_agents.core import NarrativeAgent, Experience, Telos, Memory


def test_agent_creation():
    """Test basic agent creation."""
    agent = NarrativeAgent("TestAgent", Telos.LEARNING)
    assert agent.name == "TestAgent"
    assert agent.telos == Telos.LEARNING
    assert agent.total_experiences == 0
    print("✓ Agent creation test passed")


def test_experience_processing():
    """Test experience interpretation and memory formation."""
    agent = NarrativeAgent("Learner", Telos.LEARNING)
    
    exp = Experience('error', 'Test error occurred', emotional_valence=-0.5)
    memory = agent.experience(exp)
    
    assert agent.total_experiences == 1
    assert memory.interpretation == "valuable lesson about limitations"
    print("✓ Experience processing test passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*50)
    print("RUNNING NARRATIVE AGENTS TESTS")
    print("="*50 + "\n")
    
    test_agent_creation()
    test_experience_processing()
    
    print("\n" + "="*50)
    print("ALL TESTS PASSED ✓")
    print("="*50)


if __name__ == "__main__":
    run_all_tests()
