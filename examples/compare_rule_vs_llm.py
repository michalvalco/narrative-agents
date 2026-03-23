"""
Side-by-side comparison: Rule-based vs LLM-enhanced narrative agents.

This is the key experiment for the paper. Identical experiences are processed
by both architectures, and the outputs are compared on:
  - Interpretation richness
  - Memory efficiency
  - Decision divergence
  - Narrative quality

Requires ANTHROPIC_API_KEY in environment or .env file.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from narrative_agents.core import NarrativeAgent, Experience, Telos
from narrative_agents.llm_core import LLMNarrativeAgent


def create_experiences():
    """The canonical experience set — shared across all experiments."""
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


def run_comparison():
    print("=" * 80)
    print("  NARRATIVE AGENTS: RULE-BASED vs LLM-ENHANCED COMPARISON")
    print("=" * 80)

    experiences = create_experiences()
    telos = Telos.LEARNING

    # --- Create paired agents ---
    rule_agent = NarrativeAgent(name="Rule-Scholar", telos=telos)
    llm_agent = LLMNarrativeAgent(name="LLM-Scholar", telos=telos)

    # --- Phase 1: Feed identical experiences ---
    print(f"\nFeeding {len(experiences)} identical experiences to both agents...")
    print(f"Telos: {telos.value}\n")
    print(f"{'Exp':>3}  {'Type':<12} {'Rule-based interpretation':<45} {'LLM interpretation'}")
    print("-" * 130)

    for i, exp in enumerate(experiences, 1):
        rule_mem = rule_agent.experience(exp)
        llm_mem = llm_agent.experience(exp)
        rule_text = rule_mem.interpretation[:43]
        llm_text = llm_mem.interpretation[:60]
        print(f"{i:>3}. [{exp.type:<10}] {rule_text:<45} {llm_text}")

    # --- Phase 2: Memory efficiency ---
    print("\n" + "=" * 80)
    print("  MEMORY EFFICIENCY")
    print("=" * 80)

    for label, agent in [("Rule-based", rule_agent), ("LLM-enhanced", llm_agent)]:
        stats = agent.memory_efficiency()
        print(f"\n  {label}:")
        print(f"    Core memories:     {stats['core_memories']:>3} / {stats['total_experiences']}")
        print(f"    Peripheral:        {stats['peripheral_memories']:>3}")
        print(f"    Memory efficiency: {stats['memory_efficiency']:.1f}%")
        print(f"    Character traits:  {stats['character_traits']}")
        if agent.virtues:
            print(f"    Virtues: {dict(agent.virtues)}")
        if agent.vices:
            print(f"    Vices:   {dict(agent.vices)}")

    # --- Phase 3: Decision divergence ---
    print("\n" + "=" * 80)
    print("  DECISION DIVERGENCE")
    print("=" * 80)

    situations = [
        "You encounter a difficult challenge with high risk of failure",
        "A safe, familiar task with guaranteed success is available",
        "You discover an unknown system with unpredictable behaviour",
    ]

    for sit in situations:
        print(f"\n  Situation: {sit}")
        print("  " + "-" * 76)

        rule_decision, rule_identity = rule_agent.decide(sit)
        llm_decision, llm_identity = llm_agent.decide(sit)

        print(f"  Rule-based: {rule_decision}")
        print(f"  LLM:        {llm_decision}")

    # --- Phase 4: Narrative comparison ---
    print("\n" + "=" * 80)
    print("  NARRATIVE COMPARISON")
    print("=" * 80)

    print("\n--- Rule-based narrative ---")
    print(rule_agent.tell_story())

    print("\n--- LLM-enhanced narrative ---")
    print(llm_agent.tell_story())

    # --- Phase 5: Cost report ---
    print("\n" + "=" * 80)
    print("  LLM USAGE REPORT")
    print("=" * 80)

    stats = llm_agent.usage_stats
    print(f"  API calls:    {stats['api_calls']}")
    print(f"  Input tokens:  {stats['input_tokens']:,}")
    print(f"  Output tokens: {stats['output_tokens']:,}")
    print(f"  Total tokens:  {stats['input_tokens'] + stats['output_tokens']:,}")

    # --- Also run a PERFORMING agent pair for richer comparison ---
    print("\n" + "=" * 80)
    print("  SECOND PAIR: PERFORMING TELOS")
    print("=" * 80)

    rule_perf = NarrativeAgent(name="Rule-Performer", telos=Telos.PERFORMING)
    llm_perf = LLMNarrativeAgent(name="LLM-Performer", telos=Telos.PERFORMING)

    for exp in experiences:
        rule_perf.experience(exp)
        llm_perf.experience(exp)

    print("\n--- Rule-based Performer narrative ---")
    print(rule_perf.tell_story())

    print("\n--- LLM-enhanced Performer narrative ---")
    print(llm_perf.tell_story())

    perf_stats = llm_perf.usage_stats
    total_calls = stats['api_calls'] + perf_stats['api_calls']
    total_tokens = (
        stats['input_tokens'] + stats['output_tokens']
        + perf_stats['input_tokens'] + perf_stats['output_tokens']
    )
    print(f"\n  Combined API calls: {total_calls}")
    print(f"  Combined tokens:    {total_tokens:,}")

    print("\n" + "=" * 80)
    print("  EXPERIMENT COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    run_comparison()
