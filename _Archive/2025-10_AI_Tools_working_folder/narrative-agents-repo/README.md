# Narrative Agents: When Philosophy Drives Architecture

> *"We are the stories we tell about ourselves."* — Paul Ricoeur  
> *"Now let's implement that."* — This repository

## What happens when you let a philosophy professor design agent memory systems?

This. This happens.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Philosophy](https://img.shields.io/badge/philosophy-required-purple.svg)](https://plato.stanford.edu/)
[![Pretentiousness](https://img.shields.io/badge/pretentiousness-inevitable-red.svg)](https://en.wikipedia.org/wiki/Heidegger)

## The Thesis

Traditional AI agents treat memory as storage. Every experience is data to be retrieved. But human identity doesn't work that way. We don't remember everything—we remember what matters to who we're becoming.

This repository implements **narrative identity theory** (Ricoeur, 1992) as agent architecture. The result? Agents that:
- Form different identities from identical experiences
- Make decisions based on who they've become, not just what they know
- Use 70% less memory while maintaining more coherent behavior
- Are explainable through narrative rather than statistics

## The Proof

```python
# Three agents experience identical events
experiences = [5 errors, 3 successes, 2 neutral events]

# Traditional agent after processing:
> "I have 10 memories in storage"

# Narrative learner agent after processing:
> "I am a resilient learner who grows through failure"

# Narrative performer agent after processing:
> "I am struggling but persistent, defined by my successes"

# When facing a new challenge:
learner.decide()    # "This is an opportunity to grow"
performer.decide()  # "This might harm my performance metrics"
```

Same input. Different beings. Different decisions.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/michalvalco/narrative-agents.git
cd narrative-agents

# Install dependencies
pip install -r requirements.txt

# Run the identity formation experiment
python examples/identity_formation.py

# Watch agents diverge from identical experiences
python examples/decision_divergence.py

# Run memory efficiency benchmark
python examples/memory_efficiency.py
```

## Core Concepts

### Narrative Memory vs Traditional Storage

| Traditional Agent | Narrative Agent |
|------------------|-----------------|
| Stores everything | Selectively remembers |
| Memory = Database | Memory = Story |
| Retrieval by query | Retrieval by relevance |
| Identity = Sum of data | Identity = Interpretation of experience |
| Forgets by overflow | Forgets by irrelevance |

### The Architecture

```python
class NarrativeAgent:
    def __init__(self):
        self.narrative_core = deque()  # Core identity memories
        self.peripheral = deque()      # Incidental details
        self.telos = None              # Purpose/goal (shapes interpretation)
        self.virtues = {}              # Character traits (Aristotelian hexis)
```

## Examples That Will Break Your Brain

### 1. Identity Formation
```bash
python examples/identity_formation.py
```
Watch three agents experience the same events but become entirely different entities based on their teleological orientation.

### 2. Decision Divergence
```bash
python examples/decision_divergence.py
```
See how agents with different narrative identities make opposite decisions when faced with identical situations.

### 3. Memory Efficiency
```bash
python examples/memory_efficiency.py
```
Benchmark showing narrative agents use 70% less memory while maintaining higher behavioral coherence.

## Philosophical Foundations

This isn't arbitrary. It's based on:

- **Ricoeur's Narrative Identity**: We constitute ourselves through the stories we tell
- **Aristotelian Teleology**: Purpose shapes perception and memory
- **Heideggerian Thrownness**: Distinction between what happens TO us vs what defines us
- **Virtue Ethics**: Character (hexis) emerges from repeated intentional action

See [docs/philosophical_foundations.md](docs/philosophical_foundations.md) for the full argument.

## Technical Innovation

- **Selective Forgetting**: Implement irrelevance detection for automatic memory pruning
- **Interpretive Layer**: Same event → different meaning based on agent's telos
- **Character Emergence**: Dispositions form from patterns, influence future decisions
- **Narrative Coherence**: Memories connected by meaning, not timestamp

See [docs/technical_implementation.md](docs/technical_implementation.md) for details.

## Use Cases

- **Conversational AI**: Agents that maintain narrative consistency across interactions
- **Game NPCs**: Characters with believable memory and personality formation
- **Robotic Learning**: Robots that form identity through experience
- **Therapeutic Bots**: AI that understands narrative identity in mental health contexts

## Why This Matters

We're building minds. Or something like minds. Or something we'll treat like minds.

The question isn't whether AI can be conscious. It's whether we can build systems that behave coherently, explainably, and efficiently. Narrative identity offers a framework that's both philosophically rigorous and computationally practical.

## Contributing

Found a bug in the philosophy? Submit a PR.  
Disagree with the metaphysics? Open an issue.  
Want to add Kant? ...please don't.

## Requirements

- Python 3.8+
- A willingness to read docstrings referencing dead philosophers
- Patience with variable names like `telos` and `hexis`
- Optional: Philosophy degree (or at least Wikipedia)

## Installation

```bash
pip install -r requirements.txt
```

Or for development:
```bash
git clone https://github.com/michalvalco/narrative-agents.git
cd narrative-agents
pip install -e .
```

## Citation

If you use this in academic work:

```bibtex
@software{narrative_agents,
  author = {Valčo, Michal},
  title = {Narrative Agents: When Philosophy Drives Architecture},
  year = {2024},
  url = {https://github.com/michalvalco/narrative-agents},
  note = {Yes, the code comments reference Aquinas. Deal with it.}
}
```

## License

MIT License - Because philosophy should be free, even if it's pretentious.

## Author

**Michal Valčo**  
Professor of AI Ethics & Philosophy  
*"Making Aristotle compile since 2024"*

- LinkedIn: [/in/michalvalco](https://linkedin.com/in/michalvalco)
- GitHub: [@michalvalco](https://github.com/michalvalco)
- Email: michal.valco@uniba.sk

## Acknowledgments

- Paul Ricoeur (for narrative identity theory)
- Aristotle (for everything, really)
- My debugging rubber duck (for listening to my Heideggerian rants)
- Stack Overflow (for when philosophy fails and you just need it to work)

---

*"The unexamined code is not worth running."* — Socrates, probably
