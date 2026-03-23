"""
Narrative Agents: When Philosophy Drives Architecture

An implementation of Paul Ricoeur's narrative identity theory as agent architecture.
"""

from .core import NarrativeAgent, Experience, Memory, Telos

try:
    from .llm_core import LLMNarrativeAgent
except ImportError:
    # anthropic SDK not installed — LLM agent unavailable
    LLMNarrativeAgent = None

__version__ = "0.2.0"
__author__ = "Michal Valčo"
__all__ = ["NarrativeAgent", "LLMNarrativeAgent", "Experience", "Memory", "Telos"]
