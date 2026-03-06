"""
Statistics and Data Processing Layer - Visualization Module
Generates charts and visualizations for mutation testing results.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import Dict, List, Tuple, Any
import io
import base64


class VisualizationModule:
    """
    Generates visualizations for mutation testing data.
    """
    
    @staticmethod
    def plot_mutation_score_gauge(mutation_score: float, 
                                 filepath: str = None) -> str:
        """
        Create a gauge chart for mutation score.
        
        Args:
            mutation_score: Mutation score (0-100)
            filepath: Optional file path to save
        
        Returns:
            str: Base64 encoded image or file path
        """
        fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(projection='polar'))
        
        # Create gauge
        theta = np.linspace(0, np.pi, 100)
        r = np.ones(100)
        
        # Color regions
        theta_score = (mutation_score / 100) * np.pi
        
        # Poor region (red)
        ax.fill_between(np.linspace(0, np.pi * 0.2, 50), 0, 1, alpha=0.3, color='red', label='Poor')
        # Fair region (yellow)
        ax.fill_between(np.linspace(np.pi * 0.2, np.pi * 0.4, 50), 0, 1, alpha=0.3, color='yellow', label='Fair')
        # Good region (light green)
        ax.fill_between(np.linspace(np.pi * 0.4, np.pi * 0.6, 50), 0, 1, alpha=0.3, color='lightgreen', label='Good')
        # Excellent region (green)
        ax.fill_between(np.linspace(np.pi * 0.6, np.pi, 50), 0, 1, alpha=0.3, color='green', label='Excellent')
        
        # Needle
        ax.plot([theta_score, theta_score], [0, 1], 'k-', linewidth=3)
        ax.plot(theta_score, 1, 'ko', markersize=10)
        
        ax.set_ylim(0, 1)
        ax.set_theta_offset(np.pi)
        ax.set_theta_direction(-1)
        ax.set_xticks([np.pi, np.pi * 0.75, np.pi * 0.5, np.pi * 0.25, 0])
        ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])
        ax.set_yticks([])
        
        plt.title(f'Mutation Score: {mutation_score:.1f}%', fontsize=14, fontweight='bold', pad=20)
        
        return VisualizationModule._save_figure(fig, filepath)
    
    @staticmethod
    def plot_mutation_stats(total_mutants: int, killed_mutants: int,
                           survived_mutants: int, filepath: str = None) -> str:
        """
        Create a bar chart showing mutation statistics.
        
        Args:
            total_mutants: Total mutants generated
            killed_mutants: Mutants that were killed
            survived_mutants: Mutants that survived
            filepath: Optional file path to save
        
        Returns:
            str: Base64 encoded image or file path
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Bar chart
        categories = ['Killed', 'Survived']
        values = [killed_mutants, survived_mutants]
        colors = ['#00c853', '#d32f2f']
        
        bars = ax1.bar(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        ax1.set_ylabel('Number of Mutants', fontsize=12)
        ax1.set_title('Mutation Statistics', fontsize=14, fontweight='bold')
        ax1.set_ylim(0, max(values) * 1.2)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(value)}\n({value/total_mutants*100:.1f}%)',
                    ha='center', va='bottom', fontweight='bold')
        
        # Pie chart
        ax2.pie(values, labels=categories, colors=colors, autopct='%1.1f%%',
               startangle=90, wedgeprops={'edgecolor': 'black', 'linewidth': 2})
        ax2.set_title('Mutation Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return VisualizationModule._save_figure(fig, filepath)
    
    @staticmethod
    def plot_count_distribution(counts: Dict[str, int], title: str = 'State Distribution',
                               filepath: str = None) -> str:
        """
        Create a bar chart for quantum state distribution.
        
        Args:
            counts: Count dictionary {bitstring: count}
            title: Chart title
            filepath: Optional file path to save
        
        Returns:
            str: Base64 encoded image or file path
        """
        # Get top 10 states
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
        states = [item[0] for item in sorted_counts]
        values = [item[1] for item in sorted_counts]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(range(len(states)), values, color='steelblue', alpha=0.7, edgecolor='black')
        
        ax.set_xlabel('Quantum States (Top 10)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(states)))
        ax.set_xticklabels(states, rotation=45, ha='right')
        
        # Add value labels
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(value)}',
                   ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        return VisualizationModule._save_figure(fig, filepath)
    
    @staticmethod
    def plot_comparison(original_counts: Dict[str, int],
                       mutant_counts: Dict[str, int],
                       filepath: str = None) -> str:
        """
        Create a comparison chart between original and mutant distributions.
        
        Args:
            original_counts: Original circuit counts
            mutant_counts: Mutant circuit counts
            filepath: Optional file path to save
        
        Returns:
            str: Base64 encoded image or file path
        """
        # Get all states
        all_states = set(original_counts.keys()) | set(mutant_counts.keys())
        states = sorted(list(all_states))[:10]  # Top 10 states
        
        original_vals = [original_counts.get(s, 0) for s in states]
        mutant_vals = [mutant_counts.get(s, 0) for s in states]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(states))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, original_vals, width, label='Original',
                      color='blue', alpha=0.7, edgecolor='black')
        bars2 = ax.bar(x + width/2, mutant_vals, width, label='Mutant',
                      color='red', alpha=0.7, edgecolor='black')
        
        ax.set_xlabel('Quantum States', fontsize=12, fontweight='bold')
        ax.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax.set_title('Original vs Mutant Circuit Results', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(states, rotation=45, ha='right')
        ax.legend()
        
        plt.tight_layout()
        return VisualizationModule._save_figure(fig, filepath)
    
    @staticmethod
    def plot_operator_effectiveness(operator_effectiveness: Dict[str, float],
                                   filepath: str = None) -> str:
        """
        Create a bar chart showing effectiveness of mutation operators.
        
        Args:
            operator_effectiveness: Dict of {operator: effectiveness_score}
            filepath: Optional file path to save
        
        Returns:
            str: Base64 encoded image or file path
        """
        operators = list(operator_effectiveness.keys())
        effectiveness = list(operator_effectiveness.values())
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#00c853' if eff > 60 else '#ffa726' for eff in effectiveness]
        bars = ax.barh(operators, effectiveness, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        
        ax.set_xlabel('Effectiveness Score (%)', fontsize=12, fontweight='bold')
        ax.set_title('Mutation Operator Effectiveness', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)
        
        # Add value labels
        for bar, eff in zip(bars, effectiveness):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{eff:.1f}%',
                   ha='left', va='center', fontweight='bold', fontsize=10)
        
        plt.tight_layout()
        return VisualizationModule._save_figure(fig, filepath)
    
    @staticmethod
    def _save_figure(fig, filepath: str = None) -> str:
        """
        Save figure and return path or base64 string.
        
        Args:
            fig: Matplotlib figure object
            filepath: Optional file path
        
        Returns:
            str: File path or base64 encoded image
        """
        if filepath:
            fig.savefig(filepath, dpi=100, bbox_inches='tight')
            plt.close(fig)
            return filepath
        else:
            # Convert to base64
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode()
            plt.close(fig)
            return f"data:image/png;base64,{image_base64}"
