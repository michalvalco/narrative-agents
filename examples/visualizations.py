"""
Visualization utilities for narrative agent benchmarks.
Creates publication-quality charts demonstrating memory efficiency and behavioral coherence.

Ported 2026-08-26 from _Archive/2025-10_AI_Tools_working_folder/
narrative-agents-repo/examples/visualizations.py (October 2025), unchanged
except the style guard in setup_publication_style. Offline tests:
tests/test_visualizations.py.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Any, Tuple
import matplotlib.patches as mpatches


def setup_publication_style():
    """Configure matplotlib for academic publication quality."""
    try:
        plt.style.use('seaborn-v0_8-paper')
    except OSError:  # style retired in newer matplotlib
        plt.style.use('default')
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['legend.fontsize'] = 9
    plt.rcParams['figure.titlesize'] = 14


def plot_memory_efficiency(
    agent_names: List[str],
    storage_pct: List[float],
    trait_counts: List[int],
    ax: plt.Axes
) -> None:
    """
    Bar chart comparing memory storage across agent types.
    
    Args:
        agent_names: Names of agents
        storage_pct: Storage percentage for each agent
        trait_counts: Number of character traits developed
        ax: Matplotlib axes to plot on
    """
    # Color coding: Blue for narrative, gray for traditional
    colors = []
    for name in agent_names:
        if 'Narrative' in name:
            colors.append('#2E86AB')  # Blue
        else:
            colors.append('#6C757D')  # Gray
    
    # Create horizontal bar chart
    y_pos = np.arange(len(agent_names))
    bars = ax.barh(y_pos, storage_pct, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # Add trait count annotations
    for i, (pct, traits) in enumerate(zip(storage_pct, trait_counts)):
        ax.text(pct + 2, i, f'{pct:.1f}% | {traits} traits', 
                va='center', fontsize=9, fontweight='bold')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(agent_names)
    ax.set_xlabel('Memory Storage (%)', fontweight='bold')
    ax.set_title('Memory Efficiency: Narrative vs Traditional Agents', fontweight='bold', pad=10)
    ax.set_xlim(0, 120)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.axvline(x=50, color='red', linestyle='--', linewidth=1, alpha=0.5, label='50% threshold')
    

def plot_character_development(
    timeline_data: Dict[str, List[Tuple[int, int]]],
    ax: plt.Axes
) -> None:
    """
    Line graph showing trait emergence over time.
    
    Args:
        timeline_data: Dict mapping agent names to [(experience_count, trait_count), ...]
        ax: Matplotlib axes to plot on
    """
    colors = {
        'Narrative-Learner': '#2E86AB',
        'Narrative-Performer': '#06A77D',
        'Traditional-All': '#6C757D',
        'Traditional-Limited': '#ADB5BD'
    }
    
    for agent_name, data in timeline_data.items():
        if data:
            exp_counts, trait_counts = zip(*data)
            color = colors.get(agent_name, '#000000')
            linewidth = 2.5 if 'Narrative' in agent_name else 1.5
            linestyle = '-' if 'Narrative' in agent_name else '--'
            
            ax.plot(exp_counts, trait_counts, 
                   label=agent_name, 
                   color=color, 
                   linewidth=linewidth,
                   linestyle=linestyle,
                   marker='o' if 'Narrative' in agent_name else 's',
                   markersize=4,
                   markevery=10)
    
    ax.set_xlabel('Number of Experiences', fontweight='bold')
    ax.set_ylabel('Character Traits Developed', fontweight='bold')
    ax.set_title('Character Emergence Through Experience', fontweight='bold', pad=10)
    ax.legend(loc='upper left', framealpha=0.9)
    ax.grid(alpha=0.3, linestyle='--')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, max([max([t[1] for t in data]) for data in timeline_data.values() if data]) + 1)


def plot_coherence_scatter(
    agent_names: List[str],
    efficiency: List[float],
    coherence: List[float],
    ax: plt.Axes
) -> None:
    """
    Scatter plot of memory efficiency vs behavioral coherence.
    
    Args:
        agent_names: Names of agents
        efficiency: Memory efficiency scores
        coherence: Behavioral coherence scores
        ax: Matplotlib axes to plot on
    """
    # Color and size coding
    colors = []
    sizes = []
    for name in agent_names:
        if 'Narrative' in name:
            colors.append('#2E86AB')
            sizes.append(200)
        else:
            colors.append('#6C757D')
            sizes.append(120)
    
    # Create scatter plot
    scatter = ax.scatter(efficiency, coherence, 
                        c=colors, 
                        s=sizes, 
                        alpha=0.7,
                        edgecolors='black',
                        linewidth=1.5)
    
    # Add labels for each point
    for i, name in enumerate(agent_names):
        ax.annotate(name.replace('-', '\n'), 
                   (efficiency[i], coherence[i]),
                   xytext=(5, 5), 
                   textcoords='offset points',
                   fontsize=8,
                   fontweight='bold' if 'Narrative' in name else 'normal',
                   bbox=dict(boxstyle='round,pad=0.3', 
                           facecolor='white', 
                           edgecolor='gray',
                           alpha=0.8))
    
    # Highlight the ideal quadrant (high efficiency, high coherence)
    ax.axhline(y=50, color='red', linestyle='--', linewidth=1, alpha=0.3)
    ax.axvline(x=50, color='red', linestyle='--', linewidth=1, alpha=0.3)
    ax.fill_between([50, 100], 50, 100, alpha=0.1, color='green', label='Optimal Zone')
    
    ax.set_xlabel('Memory Efficiency (%)', fontweight='bold')
    ax.set_ylabel('Behavioral Coherence (%)', fontweight='bold')
    ax.set_title('Coherence Despite Selective Forgetting', fontweight='bold', pad=10)
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 110)
    ax.grid(alpha=0.3, linestyle='--')
    

def plot_decision_heatmap(
    decision_matrix: np.ndarray,
    agent_names: List[str],
    situations: List[str],
    ax: plt.Axes
) -> None:
    """
    Heatmap of decision patterns by agent type.
    
    Args:
        decision_matrix: 2D array where rows=agents, cols=situations, values=decision type
        agent_names: List of agent names
        situations: List of situation types
        ax: Matplotlib axes to plot on
    """
    # Color map: Green (engage), Yellow (cautious), Red (avoid)
    # Values: 1 = engage, 0.5 = cautious, 0 = avoid
    cmap = plt.cm.RdYlGn
    
    im = ax.imshow(decision_matrix, cmap=cmap, aspect='auto', vmin=0, vmax=1)
    
    # Set ticks and labels
    ax.set_xticks(np.arange(len(situations)))
    ax.set_yticks(np.arange(len(agent_names)))
    ax.set_xticklabels(situations, rotation=45, ha='right')
    ax.set_yticklabels(agent_names)
    
    # Add text annotations
    for i in range(len(agent_names)):
        for j in range(len(situations)):
            value = decision_matrix[i, j]
            if value > 0.7:
                text = "Engage"
                color = 'darkgreen'
            elif value > 0.3:
                text = "Cautious"
                color = 'darkgoldenrod'
            else:
                text = "Avoid"
                color = 'darkred'
            
            ax.text(j, i, text, ha='center', va='center', 
                   fontsize=7, fontweight='bold', color=color)
    
    ax.set_title('Identity-Based Decision Patterns', fontweight='bold', pad=10)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, orientation='horizontal', pad=0.1, aspect=30)
    cbar.set_label('Engagement Level', fontweight='bold')


def create_full_benchmark_figure(
    viz_data: Dict[str, Any],
    output_path: str = 'narrative_agents_benchmark.png'
) -> plt.Figure:
    """
    Create the complete 2x2 benchmark visualization.
    
    Args:
        viz_data: Dictionary containing all visualization data:
            - agent_names: List[str]
            - storage_pct: List[float]
            - trait_counts: List[int]
            - timeline_data: Dict[str, List[Tuple[int, int]]]
            - efficiency: List[float]
            - coherence: List[float]
            - decision_matrix: np.ndarray
            - situations: List[str]
        output_path: Path to save the figure
    
    Returns:
        The matplotlib figure object
    """
    # Setup publication style
    setup_publication_style()
    
    # Create 2x2 subplot grid
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Narrative Agents: Empirical Benchmark Results', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Plot each chart
    plot_memory_efficiency(
        viz_data['agent_names'],
        viz_data['storage_pct'],
        viz_data['trait_counts'],
        ax=axes[0, 0]
    )
    
    plot_character_development(
        viz_data['timeline_data'],
        ax=axes[0, 1]
    )
    
    plot_coherence_scatter(
        viz_data['agent_names'],
        viz_data['efficiency'],
        viz_data['coherence'],
        ax=axes[1, 0]
    )
    
    plot_decision_heatmap(
        viz_data['decision_matrix'],
        viz_data['agent_names'],
        viz_data['situations'],
        ax=axes[1, 1]
    )
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    
    # Save figure
    print(f"\n📊 Saving visualization to: {output_path}")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Visualization saved successfully!")
    
    return fig


if __name__ == "__main__":
    # Example usage with dummy data
    print("Visualization module loaded successfully!")
    print("Import this module from memory_efficiency.py to create benchmark visualizations.")
