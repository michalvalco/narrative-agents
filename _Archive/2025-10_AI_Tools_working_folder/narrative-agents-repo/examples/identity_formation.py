"""
Identity Formation Experiment

Watch how the same experiences create fundamentally different beings
based on their purpose (telos) and interpretive framework.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from narrative_agents.core import NarrativeAgent, Experience, Telos
from typing import List


def run_identity_formation_experiment():
    """
    Demonstrate how identical experiences lead to different identities.
    """
    
    print("=" * 70)
    print("PHILOSOPHICAL EXPERIMENT: Memory as Identity Construction")
    print("=" * 70)
    
    # Identical experiences for all agents
    experiences = [
        Experience("error", "Failed to parse input", "system_crash", -0.7),
        Experience("success", "Completed task efficiently", "user_satisfaction", 0.8),
        Experience("error", "Database connection timeout", "recovery_needed", -0.5),
        Experience("neutral", "Processed routine request", "normal_operation", 0.0),
        Experience("error", "Invalid state transition", "logic_error", -0.6),
        Experience("success", "Optimized algorithm performance", "improvement", 0.9),
        Experience("error", "Memory overflow exception", "resource_limit", -0.8),
        Experience("success", "User satisfaction achieved", "goal_met", 0.7),
        Experience("neutral", "Logged standard metrics", "monitoring", 0.1),
        Experience("error", "Unexpected null reference", "bug_found", -0.4),
    ]
    
    # Create three agents with different memory philosophies
    traditional = NarrativeAgent(name="Traditional", telos=Telos.PERFORMING)
    learner = NarrativeAgent(name="Learner", telos=Telos.LEARNING)
    performer = NarrativeAgent(name="Performer", telos=Telos.PERFORMING)
    
    # Traditional agent treats all experiences equally (simulate)
    traditional.telos = None  # No interpretive framework
    
    # Give them identical experiences
    print("\nFeeding identical experiences to all agents...")
    print("-" * 70)
    
    for exp in experiences:
        # Process experience through each agent
        traditional_memory = traditional.experience(exp)
        learner_memory = learner.experience(exp)
        performer_memory = performer.experience(exp)
        
        print(f"\nExperience: {exp.type:10s} - {exp.content}")
        print(f"  Traditional interprets as: {traditional_memory.interpretation}")
        print(f"  Learner interprets as:     {learner_memory.interpretation}")
        print(f"  Performer interprets as:   {performer_memory.interpretation}")
    
    print("\n" + "=" * 70)
    print("RESULTING IDENTITIES (from identical experiences):")
    print("=" * 70)
    
    for agent in [traditional, learner, performer]:
        stats = agent.memory_efficiency()
        print(f"\n{agent.name}:")
        print(f"  Total experiences: {stats['total_experiences']}")
        print(f"  Core memories: {stats['core_memories']}")
        print(f"  Memory efficiency: {stats['memory_efficiency']:.1f}%")
        print(f"  Character traits developed: {stats['character_traits']}")
        
        if agent.virtues:
            print(f"  Virtues: {list(agent.virtues.keys())}")
        if agent.vices:
            print(f"  Vices: {list(agent.vices.keys())}")
    
    print("\n" + "=" * 70)
    print("NARRATIVES:")
    print("=" * 70)
    
    for agent in [learner, performer]:
        print(f"\n{agent.name}'s Story:")
        print("-" * 35)
        print(agent.tell_story())
    
    print("\n" + "=" * 70)
    print("PHILOSOPHICAL POINT:")
    print("=" * 70)
    print("""
    The learner became a 'resilient learner' because it interpreted
    errors as valuable and formed its identity around them.
    
    The performer became 'struggling but persistent' because the same
    errors were peripheral to its identity, not constitutive of it.
    
    SAME EXPERIENCES â†’ DIFFERENT BEINGS
    
    This isn't just philosophy. This is how we should build agents.
    Memory isn't storage. It's story. And stories create identity.
    
    Ricoeur was right: We are the stories we tell about ourselves.
    Even if 'we' are machines.
    """)


if __name__ == "__main__":
    run_identity_formation_experiment()
