# Visualization Implementation Plan
*Quick win: 2-3 hours of work*

---

## Goal

Transform `memory_efficiency.py` from text output to publication-ready visualizations.

---

## What We'll Create

### 1. Memory Efficiency Bar Chart
**Shows**: Storage percentage for each agent type
**Visual**: Horizontal bar chart with color coding
- Narrative agents: Blue
- Traditional agents: Gray
**Labels**: Percentages + character trait counts
**Title**: "Memory Storage: Narrative vs Traditional Agents"

### 2. Character Development Over Time
**Shows**: How virtues/vices develop with experience count
**Visual**: Line graph, one line per agent
**X-axis**: Number of experiences (0-100)
**Y-axis**: Number of character traits developed
**Title**: "Character Emergence Through Experience"

### 3. Behavioral Coherence Comparison
**Shows**: Coherence score vs memory efficiency
**Visual**: Scatter plot with agent labels
**X-axis**: Memory efficiency (%)
**Y-axis**: Behavioral coherence score (%)
**Highlight**: Narrative agents cluster high on both
**Title**: "Coherence Despite Forgetting"

### 4. Decision Pattern Heatmap
**Shows**: How each agent responds to different situations
**Visual**: Color-coded matrix
**Rows**: Agent types
**Columns**: Situation types (challenge, risk, routine, etc.)
**Colors**: Green (engage), Yellow (cautious), Red (avoid)
**Title**: "Identity-Based Decision Patterns"

---

## Implementation Approach

### Step 1: Modify `memory_efficiency.py` to collect visualization data

Add data collection during the benchmark:
```python
# After processing experiences
viz_data = {
    'agent_names': list(agents.keys()),
    'storage_pct': [...],
    'trait_counts': [...],
    'coherence_scores': [...],
    'trait_development_over_time': {
        'Narrative-Learner': [(exp_count, trait_count), ...],
        ...
    }
}
```

### Step 2: Create visualization function

```python
def create_visualizations(viz_data, output_dir='./outputs'):
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Set style for academic publications
    plt.style.use('seaborn-v0_8-paper')
    
    # Create 2x2 subplot figure
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Chart 1: Memory efficiency bar chart
    # Chart 2: Character development lines
    # Chart 3: Coherence scatter plot  
    # Chart 4: Decision pattern heatmap
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/narrative_agents_benchmark.png', dpi=300)
    plt.show()
```

### Step 3: Add to requirements.txt

```
matplotlib>=3.7.0
seaborn>=0.12.0  # Optional, for better styling
```

### Step 4: Update README with visualization screenshots

Add a section:
```markdown
## Empirical Results

[Benchmark visualization screenshot]

Our experiments demonstrate:
- **70% memory reduction**: Narrative agents store only 22-30% of experiences
- **Character emergence**: 1-3 behavioral traits develop automatically  
- **Behavioral coherence**: High consistency despite selective forgetting
```

---

## Code Structure

### New file: `examples/visualizations.py`

```python
"""
Visualization utilities for narrative agent benchmarks.
Creates publication-quality charts and graphs.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Any


def plot_memory_efficiency(agent_data: Dict[str, Any], save_path: str = None):
    """Bar chart comparing memory storage across agent types."""
    # Implementation here
    pass


def plot_character_development(timeline_data: Dict[str, List], save_path: str = None):
    """Line graph showing trait emergence over time."""
    # Implementation here
    pass


def plot_coherence_scatter(efficiency: List[float], coherence: List[float], 
                           labels: List[str], save_path: str = None):
    """Scatter plot of efficiency vs coherence."""
    # Implementation here
    pass


def plot_decision_heatmap(decision_matrix: np.ndarray, agent_names: List[str],
                          situations: List[str], save_path: str = None):
    """Heatmap of decision patterns by agent type."""
    # Implementation here
    pass


def create_full_benchmark_figure(viz_data: Dict[str, Any], output_path: str):
    """Create the complete 2x2 benchmark visualization."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    plot_memory_efficiency(viz_data['memory'], ax=axes[0,0])
    plot_character_development(viz_data['traits'], ax=axes[0,1])
    plot_coherence_scatter(viz_data['efficiency'], viz_data['coherence'], 
                          viz_data['labels'], ax=axes[1,0])
    plot_decision_heatmap(viz_data['decisions'], viz_data['agents'],
                         viz_data['situations'], ax=axes[1,1])
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    return fig
```

### Modified: `examples/memory_efficiency.py`

Add at the end:
```python
if __name__ == "__main__":
    results = compare_memory_efficiency()
    
    # Create visualizations
    from visualizations import create_full_benchmark_figure
    
    print("\n📊 Creating visualizations...")
    fig = create_full_benchmark_figure(
        viz_data=results,
        output_path='../../outputs/benchmark_results.png'
    )
    print("✅ Saved: outputs/benchmark_results.png")
```

---

## Visual Design Principles

1. **Academic Style**: Clean, professional, suitable for papers
2. **Color Coding**: 
   - Narrative agents: Blue spectrum (#2E86AB, #06A77D)
   - Traditional agents: Gray spectrum (#6C757D, #ADB5BD)
3. **Fonts**: 
   - Title: 14pt, bold
   - Labels: 11pt
   - Annotations: 9pt
4. **Grid**: Subtle, light gray
5. **Legend**: Top-right, transparent background

---

## Testing Checklist

- [ ] Run memory_efficiency.py with visualization flag
- [ ] Verify all 4 charts render correctly
- [ ] Check PNG output at 300 DPI
- [ ] Ensure labels are readable
- [ ] Test with different agent counts
- [ ] Verify colors are colorblind-friendly
- [ ] Check file size (should be < 2MB)

---

## Output Files

After implementation:
```
narrative-agents/
  examples/
    memory_efficiency.py (modified)
    visualizations.py (new)
  outputs/
    benchmark_results.png (2x2 grid)
    memory_efficiency.png (individual chart)
    character_development.png (individual chart)
    coherence_scatter.png (individual chart)
    decision_heatmap.png (individual chart)
```

---

## Estimated Time

- Chart 1 (bar chart): 30 min
- Chart 2 (line graph): 30 min  
- Chart 3 (scatter plot): 20 min
- Chart 4 (heatmap): 40 min
- Integration + testing: 30 min
- **Total**: ~2.5 hours

---

## Why This Matters

These visualizations transform the narrative-agents repo from "interesting code" to "publication-ready research."

They enable:
1. **LinkedIn posts** with eye-catching graphics
2. **Medium article** with embedded charts
3. **Academic paper** with proper figures
4. **GitHub stars** (visual projects get 3-5x more engagement)
5. **Conference talks** with ready-made slides

**ROI**: 2.5 hours of work → dramatically increased shareability

---

## Next Step

Reply with:
- "A: Create the visualization code" → I'll write the complete implementation
- "B: Show me a mockup first" → I'll sketch what each chart will look like
- "C: Let's focus on Medium article instead" → I'll draft that

Your call.
