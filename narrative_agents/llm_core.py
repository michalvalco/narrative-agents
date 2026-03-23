"""
LLM-enhanced Narrative Agent.

Subclass of NarrativeAgent that replaces rule-based interpretation with
Claude API calls. The philosophical architecture (memory structures, character
formation, efficiency metrics) is inherited unchanged. Only the interpretive
layer — where philosophy becomes meaning — is enhanced.

Requires: ANTHROPIC_API_KEY environment variable.
"""

import os
import json
from typing import Dict, Any, List, Optional, Tuple

import anthropic

from .core import NarrativeAgent, Experience, Memory, Telos
from .prompts import (
    INTERPRET_SYSTEM_PROMPT,
    RELEVANCE_SYSTEM_PROMPT,
    DECISION_SYSTEM_PROMPT,
    STORY_SYSTEM_PROMPT,
)


# Cost-efficient model for per-experience calls (interpretation, relevance)
DEFAULT_FAST_MODEL = "claude-haiku-4-5-20251001"
# More capable model for reasoning-heavy calls (decisions, stories)
DEFAULT_REASONING_MODEL = "claude-sonnet-4-5-20241022"


class LLMNarrativeAgent(NarrativeAgent):
    """
    A narrative agent whose interpretive layer is powered by Claude.

    Rule-based emplotment is replaced with language-model interpretation,
    producing richer, contextually aware narratives while preserving
    the same memory architecture and character formation mechanisms.

    Falls back to rule-based interpretation if the API is unavailable.
    """

    def __init__(
        self,
        name: str = "Agent",
        telos: Optional[Telos] = None,
        context_window: int = 50,
        api_key: Optional[str] = None,
        fast_model: str = DEFAULT_FAST_MODEL,
        reasoning_model: str = DEFAULT_REASONING_MODEL,
    ):
        super().__init__(name=name, telos=telos, context_window=context_window)

        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError(
                "ANTHROPIC_API_KEY must be set in environment or passed as api_key"
            )
        self.client = anthropic.Anthropic(api_key=key)
        self.fast_model = fast_model
        self.reasoning_model = reasoning_model

        # Token usage tracking
        self.usage_stats: Dict[str, int] = {
            "input_tokens": 0,
            "output_tokens": 0,
            "api_calls": 0,
        }

    # ------------------------------------------------------------------
    # Internal helper
    # ------------------------------------------------------------------

    def _call_llm(
        self,
        system: str,
        user_message: str,
        model: Optional[str] = None,
        max_tokens: int = 300,
    ) -> str:
        """Send a message to Claude and return the text response."""
        model = model or self.fast_model
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user_message}],
            )
            self.usage_stats["input_tokens"] += response.usage.input_tokens
            self.usage_stats["output_tokens"] += response.usage.output_tokens
            self.usage_stats["api_calls"] += 1
            return response.content[0].text.strip()
        except Exception as exc:
            # Graceful fallback — log but don't crash
            print(f"  [LLM fallback] {type(exc).__name__}: {exc}")
            return ""

    def _character_summary(self) -> str:
        """Build a compact character description for prompt context."""
        parts = [f"Purpose (telos): {self.telos.value}"]
        if self.virtues:
            top = sorted(self.virtues.items(), key=lambda x: x[1], reverse=True)[:3]
            parts.append(
                "Virtues: " + ", ".join(f"{k} ({v:.1f})" for k, v in top)
            )
        if self.vices:
            top = sorted(self.vices.items(), key=lambda x: x[1], reverse=True)[:2]
            parts.append(
                "Vices: " + ", ".join(f"{k} ({v:.1f})" for k, v in top)
            )
        if self.narrative_core:
            recent = list(self.narrative_core)[-3:]
            interps = [m.interpretation for m in recent]
            parts.append("Recent core memories: " + "; ".join(interps))
        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Overridden interpretive methods
    # ------------------------------------------------------------------

    def _interpret_through_telos(self, exp: Experience) -> str:
        """
        LLM-powered emplotment: the experience is interpreted through the
        agent's telos by Claude, producing contextually rich meaning.
        """
        user_msg = (
            f"Agent name: {self.name}\n"
            f"Agent telos: {self.telos.value}\n"
            f"{self._character_summary()}\n\n"
            f"Experience:\n"
            f"  Type: {exp.type}\n"
            f"  Content: {exp.content}\n"
            f"  Outcome: {exp.outcome or 'none'}\n"
            f"  Emotional valence: {exp.emotional_valence:+.1f}\n"
        )
        result = self._call_llm(INTERPRET_SYSTEM_PROMPT, user_msg, max_tokens=150)
        if result:
            return result
        # Fallback to rule-based
        return super()._interpret_through_telos(exp)

    def _assess_relevance(self, exp: Experience) -> float:
        """
        LLM-powered relevance scoring: Claude assesses how identity-forming
        this experience is, given the agent's telos and character.
        """
        user_msg = (
            f"Agent: {self.name}\n"
            f"{self._character_summary()}\n\n"
            f"Experience to assess:\n"
            f"  Type: {exp.type}\n"
            f"  Content: {exp.content}\n"
            f"  Outcome: {exp.outcome or 'none'}\n"
            f"  Emotional valence: {exp.emotional_valence:+.1f}\n"
        )
        result = self._call_llm(RELEVANCE_SYSTEM_PROMPT, user_msg, max_tokens=10)
        if result:
            try:
                score = float(result.strip().split()[0])
                return max(0.0, min(score, 1.0))
            except (ValueError, IndexError):
                pass
        # Fallback to rule-based
        return super()._assess_relevance(exp)

    def _identity_based_decision(self, situation: str, identity: str) -> str:
        """
        LLM-powered decision-making: Claude reasons through the agent's
        narrative identity to produce a character-consistent decision.
        """
        user_msg = (
            f"Identity statement:\n{identity}\n\n"
            f"{self._character_summary()}\n\n"
            f"Situation: {situation}\n"
        )
        result = self._call_llm(
            DECISION_SYSTEM_PROMPT,
            user_msg,
            model=self.reasoning_model,
            max_tokens=200,
        )
        if result:
            return result
        return super()._identity_based_decision(situation, identity)

    def tell_story(self) -> str:
        """
        LLM-powered narrative construction: Claude weaves the agent's
        memories, virtues, and vices into a coherent first-person story.
        """
        if not self.narrative_core:
            return f"{self.name} has no story yet — tabula rasa awaiting experience."

        # Build memory data for the prompt
        memories_text = []
        for i, mem in enumerate(self.narrative_core):
            memories_text.append(
                f"  {i+1}. [{mem.experience.type}] {mem.experience.content} "
                f"→ Interpreted as: \"{mem.interpretation}\" "
                f"(relevance: {mem.relevance:.2f})"
            )

        user_msg = (
            f"Agent name: {self.name}\n"
            f"Telos: {self.telos.value}\n"
            f"Total experiences: {self.total_experiences}\n"
            f"Core memories ({len(self.narrative_core)}):\n"
            + "\n".join(memories_text)
            + "\n\n"
        )

        if self.virtues:
            virtues = [f"{k} ({v:.2f})" for k, v in self.virtues.items() if v > 0.2]
            user_msg += f"Virtues developed: {', '.join(virtues)}\n"
        if self.vices:
            vices = [f"{k} ({v:.2f})" for k, v in self.vices.items() if v > 0.2]
            user_msg += f"Vices/struggles: {', '.join(vices)}\n"

        result = self._call_llm(
            STORY_SYSTEM_PROMPT,
            user_msg,
            model=self.reasoning_model,
            max_tokens=500,
        )
        if result:
            return result
        return super().tell_story()
