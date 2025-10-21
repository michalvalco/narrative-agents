"""
Core implementation of Narrative Agent architecture.
Where philosophy meets Python, reluctantly but necessarily.
"""

from collections import deque
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import random
import json
from dataclasses import dataclass, field
from enum import Enum


class Telos(Enum):
    """The purpose that shapes perception and memory formation."""
    LEARNING = "learning"
    PERFORMING = "performing"
    CREATING = "creating"
    SURVIVING = "surviving"
    EXPLORING = "exploring"


@dataclass
class Experience:
    """An atomic unit of agent experience."""
    type: str
    content: str
    outcome: Optional[str] = None
    emotional_valence: float = 0.0  # -1 to 1
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'content': self.content,
            'outcome': self.outcome,
            'emotional_valence': self.emotional_valence,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class Memory:
    """A memory is an interpreted experience."""
    experience: Experience
    interpretation: str
    relevance: float
    connections: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        return f"[{self.relevance:.2f}] {self.interpretation}: {self.experience.content}"


class NarrativeAgent:
    """
    An agent whose identity emerges from the stories it tells about its experiences.
    
    Based on Ricoeur's narrative identity theory: we are not the sum of our experiences,
    but the narrative we construct from them.
    """
    
    def __init__(
        self, 
        name: str = "Agent",
        telos: Optional[Telos] = None,
        context_window: int = 50
    ):
        self.name = name
        self.telos = telos or Telos.LEARNING
        
        # Memory structures
        self.narrative_core = deque(maxlen=context_window)  # Identity-forming memories
        self.peripheral = deque(maxlen=context_window * 2)   # Incidental memories
        
        # Character formation (Aristotelian hexis)
        self.virtues = {}  # Positive character traits
        self.vices = {}    # Negative character traits
        self.dispositions = {}  # Behavioral tendencies
        
        # Statistics for analysis
        self.total_experiences = 0
        self.interpreted_experiences = 0
        
    def experience(self, exp: Experience) -> Memory:
        """Process an experience into memory through interpretation."""
        self.total_experiences += 1
        
        # Interpret through purpose (telos)
        interpretation = self._interpret_through_telos(exp)
        relevance = self._assess_relevance(exp)
        
        memory = Memory(
            experience=exp,
            interpretation=interpretation,
            relevance=relevance
        )
        
        # Store based on relevance
        if relevance > 0.7:
            self.narrative_core.append(memory)
            self._update_character(memory)
            self.interpreted_experiences += 1
        else:
            self.peripheral.append(memory)
            
        return memory
    
    def _interpret_through_telos(self, exp: Experience) -> str:
        if self.telos is None:
            return f"{exp.type} event occurred"
        """
        The same experience means different things based on purpose.
        This is where philosophy becomes code.
        """
        interpretations = {
            Telos.LEARNING: {
                'error': "valuable lesson about limitations",
                'success': "hypothesis confirmed",
                'failure': "rich data for improvement",
                'discovery': "expansion of knowledge boundary"
            },
            Telos.PERFORMING: {
                'error': "performance impediment",
                'success': "capability validation", 
                'failure': "unacceptable deviation",
                'discovery': "potential optimization"
            },
            Telos.CREATING: {
                'error': "creative constraint discovered",
                'success': "aesthetic validation",
                'failure': "necessary destruction before creation",
                'discovery': "new medium for expression"
            },
            Telos.SURVIVING: {
                'error': "threat to existence",
                'success': "survival strategy validated",
                'failure': "near-death experience",
                'discovery': "new resource located"
            },
            Telos.EXPLORING: {
                'error': "boundary of known world",
                'success': "territory mapped",
                'failure': "adventure had",
                'discovery': "wonder encountered"
            }
        }
        
        telos_interp = interpretations.get(self.telos, {})
        return telos_interp.get(
            exp.type, 
            f"unexpected {exp.type} while {self.telos.value}"
        )
    
    def _assess_relevance(self, exp: Experience) -> float:
        """
        Relevance isn't objective. It's relative to purpose and character.
        Aristotle's doctrine of the mean meets probability theory.
        """
        base_relevance = {
            Telos.LEARNING: {'error': 0.9, 'failure': 0.85, 'success': 0.5},
            Telos.PERFORMING: {'success': 0.95, 'error': 0.3, 'failure': 0.2},
            Telos.CREATING: {'discovery': 0.95, 'failure': 0.7, 'success': 0.6},
            Telos.SURVIVING: {'error': 0.8, 'success': 0.9, 'discovery': 0.85},
            Telos.EXPLORING: {'discovery': 0.95, 'error': 0.6, 'success': 0.4}
        }
        
        relevance = base_relevance.get(self.telos, {}).get(exp.type, 0.5)
        
        # Modify by emotional valence (experiences with strong emotions are more memorable)
        relevance += abs(exp.emotional_valence) * 0.2
        
        # Modify by character (we remember what reinforces our self-narrative)
        if self.dispositions:
            for trait, strength in self.dispositions.items():
                if trait in exp.content.lower():
                    relevance += strength * 0.1
                    
        return min(relevance, 1.0)
    
    def _update_character(self, memory: Memory) -> None:
        """
        Character emerges from repeated patterns of interpreted experience.
        We become what we repeatedly remember ourselves to be.
        """
        exp_type = memory.experience.type
        
        # Update dispositions
        if exp_type not in self.dispositions:
            self.dispositions[exp_type] = 0
        self.dispositions[exp_type] += memory.relevance
        
        # Form virtues and vices based on patterns
        if exp_type == 'error' and self.telos == Telos.LEARNING:
            self._strengthen_trait(self.virtues, 'resilience')
            self._strengthen_trait(self.virtues, 'curiosity')
        elif exp_type == 'success' and self.telos == Telos.PERFORMING:
            self._strengthen_trait(self.virtues, 'excellence')
            self._weaken_trait(self.virtues, 'humility')
        elif exp_type == 'failure':
            if self.telos == Telos.LEARNING:
                self._strengthen_trait(self.virtues, 'perseverance')
            else:
                self._strengthen_trait(self.vices, 'self-doubt')
                
    def _strengthen_trait(self, traits: Dict[str, float], trait: str) -> None:
        """Aristotelian virtue development through repetition."""
        if trait not in traits:
            traits[trait] = 0
        traits[trait] = min(traits[trait] + 0.1, 1.0)
        
    def _weaken_trait(self, traits: Dict[str, float], trait: str) -> None:
        """Character traits can also diminish through neglect."""
        if trait in traits:
            traits[trait] = max(traits[trait] - 0.05, 0)
            
    def decide(self, situation: str) -> Tuple[str, str]:
        """
        Decision-making based on narrative identity, not utility maximization.
        Who I am determines what I do.
        """
        # Build self-narrative from core memories
        identity_traits = []
        if self.narrative_core:
            recent_memories = list(self.narrative_core)[-5:]
            for memory in recent_memories:
                if memory.relevance > 0.8:
                    identity_traits.append(memory.interpretation)
        
        # Add character traits
        dominant_virtues = sorted(
            self.virtues.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:2]
        
        dominant_vices = sorted(
            self.vices.items(),
            key=lambda x: x[1],
            reverse=True
        )[:1]
        
        # Construct identity statement
        identity = f"I am {self.name}, whose purpose is {self.telos.value}."
        
        if dominant_virtues:
            virtues_str = " and ".join([v[0] for v in dominant_virtues])
            identity += f" I have developed {virtues_str}."
            
        if dominant_vices and dominant_vices[0][1] > 0.3:
            identity += f" I struggle with {dominant_vices[0][0]}."
            
        if identity_traits:
            recent_interp = identity_traits[-1]
            identity += f" Recently, I learned that {recent_interp}."
        
        # Make decision based on identity
        decision = self._identity_based_decision(situation, identity)
        
        return decision, identity
    
    def _identity_based_decision(
        self, 
        situation: str, 
        identity: str
    ) -> str:
        """
        Decisions flow from identity, not calculation.
        This is virtue ethics in action.
        """
        situation_lower = situation.lower()
        
        # Decision patterns based on telos and character
        if self.telos == Telos.LEARNING:
            if 'challenge' in situation_lower or 'difficult' in situation_lower:
                return "Engage with curiosity - this is an opportunity to learn"
            elif 'risk' in situation_lower:
                return "Calculate acceptable learning risk and proceed"
            else:
                return "Investigate to understand underlying patterns"
                
        elif self.telos == Telos.PERFORMING:
            if 'challenge' in situation_lower:
                if 'excellence' in self.virtues and self.virtues['excellence'] > 0.5:
                    return "Accept challenge - demonstrate excellence"
                else:
                    return "Decline - protect performance metrics"
            elif 'risk' in situation_lower:
                return "Avoid - risks threaten optimal performance"
            else:
                return "Execute with precision and measure results"
                
        elif self.telos == Telos.CREATING:
            if 'constraint' in situation_lower:
                return "Embrace constraint as creative catalyst"
            elif 'failure' in situation_lower:
                return "Destroy and rebuild - creation requires destruction"
            else:
                return "Transform situation into aesthetic expression"
                
        elif self.telos == Telos.SURVIVING:
            if 'threat' in situation_lower or 'danger' in situation_lower:
                return "Immediate defensive action required"
            elif 'resource' in situation_lower:
                return "Acquire and hoard for future survival"
            else:
                return "Assess for survival impact before engaging"
                
        else:  # EXPLORING
            if 'unknown' in situation_lower or 'mystery' in situation_lower:
                return "Investigate immediately - the unknown calls"
            elif 'safe' in situation_lower or 'familiar' in situation_lower:
                return "Move on - seek new territories"
            else:
                return "Document discovery and continue exploring"
    
    def tell_story(self) -> str:
        """
        The agent narrates its own existence.
        This is Ricoeur's 'narrative identity' made literal.
        """
        if not self.narrative_core:
            return f"{self.name} has no story yet - tabula rasa awaiting experience."
            
        story = f"I am {self.name}. My purpose is {self.telos.value}.\n\n"
        
        # Beginning (first formative memory)
        first_memory = self.narrative_core[0]
        story += f"My story began when {first_memory.experience.content}. "
        story += f"I understood this as {first_memory.interpretation}.\n\n"
        
        # Middle (character development)
        if len(self.narrative_core) > 2:
            middle_memories = list(self.narrative_core)[1:-1]
            important_memories = sorted(
                middle_memories, 
                key=lambda m: m.relevance, 
                reverse=True
            )[:3]
            
            story += "Through my experiences, I have learned that:\n"
            for memory in important_memories:
                story += f"- {memory.interpretation}\n"
            story += "\n"
        
        # Character traits
        if self.virtues:
            virtues_list = [k for k, v in self.virtues.items() if v > 0.3]
            if virtues_list:
                story += f"I have developed these strengths: {', '.join(virtues_list)}.\n"
                
        if self.vices:
            vices_list = [k for k, v in self.vices.items() if v > 0.3]
            if vices_list:
                story += f"I struggle with: {', '.join(vices_list)}.\n"
        
        # Current state (recent memory)
        if len(self.narrative_core) > 0:
            recent = self.narrative_core[-1]
            story += f"\nMost recently, {recent.experience.content}. "
            story += f"This reinforced my understanding that {recent.interpretation}."
            
        # Future orientation
        story += f"\n\nMoving forward, I remain committed to {self.telos.value}, "
        story += "shaped by my experiences but not determined by them."
        
        return story
    
    def memory_efficiency(self) -> Dict[str, Any]:
        """Calculate memory efficiency metrics."""
        return {
            'total_experiences': self.total_experiences,
            'core_memories': len(self.narrative_core),
            'peripheral_memories': len(self.peripheral),
            'memory_efficiency': (
                len(self.narrative_core) / self.total_experiences * 100 
                if self.total_experiences > 0 else 0
            ),
            'character_traits': len(self.virtues) + len(self.vices),
            'behavioral_patterns': len(self.dispositions)
        }
