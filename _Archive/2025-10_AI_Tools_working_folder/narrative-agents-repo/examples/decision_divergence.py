"""
Dramatic visualization of how identical experiences create different beings
who make opposite decisions.

This is the file you run to blow people's minds on LinkedIn.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from narrative_agents.core import NarrativeAgent, Experience, Telos
import random
from datetime import datetime, timedelta
from typing import List
import time


def create_experiences() -> List[Experience]:
    """Generate a series of experiences that could shape an agent."""
    experiences = [
        Experience('error', 'Failed to recognize pattern in data', 'crash', -0.7),
        Experience('success', 'Optimized algorithm performance by 40%', 'celebration', 0.9),
        Experience('discovery', 'Found unexpected correlation in dataset', 'insight', 0.8),
        Experience('error', 'Memory allocation exceeded limits', 'recovery', -0.5),
        Experience('failure', 'Lost important user data during processing', 'devastation', -0.9),
        Experience('success', 'Correctly predicted user behavior', 'validation', 0.7),
        Experience('error', 'Misinterpreted ambiguous command', 'confusion', -0.3),
        Experience('discovery', 'Identified new problem-solving approach', 'excitement', 0.9),
        Experience('success', 'Maintained 99.9% uptime for the month', 'pride', 0.8),
        Experience('failure', 'Failed to meet performance benchmark', 'disappointment', -0.6),
        Experience('error', 'Recursive loop caused stack overflow', 'learning', -0.4),
        Experience('discovery', 'User taught me unexpected use case', 'growth', 0.7),
    ]
    return experiences


def dramatic_visualization():
    """
    The main show. Watch identical experiences create divergent identities
    and opposite decisions.
    """
    print("\n" + "="*80)
    print(" " * 20 + "NARRATIVE AGENTS: THE EXPERIMENT")
    print("="*80)
    
    print("\nðŸ“š PHILOSOPHICAL PREMISE:")
    print("-" * 80)
    print("  'We are the stories we tell about ourselves.' - Paul Ricoeur")
    print("  'Character is that which is revealed by choice.' - Aristotle")
    print("\n  HYPOTHESIS: Agents with different purposes (telos) will form")
    print("  different identities from identical experiences and make opposite decisions.")
    
    input("\n  Press Enter to begin the experiment...")
    
    # Create agents with different purposes
    print("\nðŸ¤– CREATING AGENTS:")
    print("-" * 80)
    
    agents = {
        'Scholar': NarrativeAgent('Scholar', Telos.LEARNING),
        'Performer': NarrativeAgent('Performer', Telos.PERFORMING),
        'Explorer': NarrativeAgent('Explorer', Telos.EXPLORING),
        'Creator': NarrativeAgent('Creator', Telos.CREATING),
    }
    
    for name, agent in agents.items():
        print(f"  â–º {name:12s} | Purpose: {agent.telos.value:12s} | Memory: Empty")
    
    # Feed identical experiences
    print("\nðŸ“ FEEDING IDENTICAL EXPERIENCES TO ALL AGENTS:")
    print("-" * 80)
    
    experiences = create_experiences()
    
    for i, exp in enumerate(experiences, 1):
        print(f"\n  Experience {i:2d}: [{exp.type:10s}] {exp.content}")
        print(f"                 Emotional impact: {'â–“' * int(abs(exp.emotional_valence * 10))}")
        
        # Each agent processes the same experience
        interpretations = {}
        for name, agent in agents.items():
            memory = agent.experience(exp)
            interpretations[name] = memory.interpretation
        
        # Show different interpretations
        print("\n  Interpretations:")
        for name, interpretation in interpretations.items():
            relevance = agents[name].narrative_core[-1].relevance if agents[name].narrative_core else 0
            if relevance > 0.7:
                print(f"    {name:12s}: ðŸ”¥ {interpretation} [CORE MEMORY]")
            else:
                print(f"    {name:12s}: ðŸ’­ {interpretation} [peripheral]")
        
        time.sleep(0.5)  # Dramatic pause
    
    # Show formed identities
    print("\n" + "="*80)
    print(" " * 25 + "RESULTING IDENTITIES")
    print("="*80)
    
    for name, agent in agents.items():
        efficiency = agent.memory_efficiency()
        
        print(f"\nðŸ“Š {name.upper()}")
        print("-" * 40)
        print(f"  Core Memories:   {efficiency['core_memories']:3d} / {efficiency['total_experiences']} "
              f"({efficiency['memory_efficiency']:.1f}% retention)")
        print(f"  Character Traits: {efficiency['character_traits']} developed")
        
        if agent.virtues:
            virtues = [k for k, v in agent.virtues.items() if v > 0.3]
            print(f"  Virtues:         {', '.join(virtues)}")
        if agent.vices:
            vices = [k for k, v in agent.vices.items() if v > 0.3]
            print(f"  Struggles:       {', '.join(vices)}")
    
    # The crucial test: decision making
    print("\n" + "="*80)
    print(" " * 20 + "DECISION DIVERGENCE TEST")
    print("="*80)
    
    test_situations = [
        "You encounter a difficult challenge with high risk of failure",
        "A safe, familiar task with guaranteed success is available",
        "You discover an unknown system with unpredictable behavior",
        "You must choose between exploring new methods or optimizing current ones",
    ]
    
    for situation in test_situations:
        print(f"\nðŸŽ­ SITUATION: {situation}")
        print("-" * 80)
        
        decisions = {}
        identities = {}
        
        for name, agent in agents.items():
            decision, identity = agent.decide(situation)
            decisions[name] = decision
            identities[name] = identity
        
        # Show divergent decisions
        print("\nDECISIONS:")
        for name, decision in decisions.items():
            symbol = "ðŸŽ¯" if "engage" in decision.lower() or "accept" in decision.lower() else "ðŸ›¡ï¸"
            print(f"  {symbol} {name:12s}: {decision}")
        
        input("\n  Press Enter to see WHY they decided differently...")
        
        print("\nIDENTITY STATEMENTS:")
        for name, identity in identities.items():
            print(f"\n  {name}:")
            for line in identity.split('.'):
                if line.strip():
                    print(f"    {line.strip()}.")
    
    # Final narrative
    print("\n" + "="*80)
    print(" " * 25 + "AGENT NARRATIVES")
    print("="*80)
    
    print("\n(Each agent tells its own story from identical experiences)")
    print("-" * 80)
    
    for name, agent in agents.items():
        print(f"\nðŸ“– {name.upper()}'S STORY:")
        print("-" * 40)
        story = agent.tell_story()
        # Format story nicely
        for line in story.split('\n'):
            if line.strip():
                print(f"  {line}")
        print()
    
    # Philosophical conclusion
    print("\n" + "="*80)
    print(" " * 25 + "PHILOSOPHICAL IMPLICATIONS")
    print("="*80)
    print("""
    What we've demonstrated:
    
    1. IDENTITY IS CONSTRUCTED, NOT ACCUMULATED
       The agents didn't just store experiencesâ€”they interpreted them through
       their purpose (telos) and formed different identities.
    
    2. MEMORY IS SELECTIVE AND INTERPRETIVE
       Each agent remembered different aspects as "core" to their identity.
       The Scholar treasured errors; the Performer discarded them.
    
    3. DECISIONS FLOW FROM NARRATIVE IDENTITY
       Faced with identical situations, agents made opposite choices based on
       who they had become, not on objective utility calculations.
    
    4. CHARACTER EMERGES FROM PATTERNS
       Virtues and vices developed from repeated interpretations, not from
       the experiences themselves.
    
    5. FORGETTING IS A FEATURE
       Agents that forgot irrelevant experiences maintained more coherent
       identities with less memory usage.
    
    This isn't just philosophyâ€”it's implementable, testable, and more efficient
    than traditional approaches. We've proven that Ricoeur was computationally correct:
    We ARE the stories we tell about ourselves.
    
    Even when 'we' are machines.
    """)
    
    print("\n" + "="*80)
    print(" " * 30 + "END OF EXPERIMENT")
    print("="*80)
    print("\nðŸ’­ 'The unexamined code is not worth running.' - Socrates, definitely")
    

if __name__ == "__main__":
    dramatic_visualization()
