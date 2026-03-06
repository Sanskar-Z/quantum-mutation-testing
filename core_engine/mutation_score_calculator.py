"""
Core Mutation Testing Engine - Mutation Score Calculator
Calculates mutation scores based on mutants killed vs survived.
"""
from typing import Dict, List, Any
import math


class MutationScoreCalculator:
    """
    Calculates mutation scores for quantum circuit testing.
    """
    
    @staticmethod
    def calculate_mutation_score(total_mutants: int, killed_mutants: int) -> float:
        """
        Calculate basic mutation score.
        
        Formula: mutation_score = (killed_mutants / total_mutants) * 100
        
        Args:
            total_mutants: Total number of mutants generated
            killed_mutants: Number of mutants that were killed (detected)
        
        Returns:
            float: Mutation score as percentage (0-100)
        """
        if total_mutants == 0:
            return 0.0
        
        score = (killed_mutants / total_mutants) * 100
        return round(score, 2)
    
    @staticmethod
    def calculate_survival_rate(total_mutants: int, killed_mutants: int) -> float:
        """
        Calculate mutation survival rate.
        
        Formula: survival_rate = (survived_mutants / total_mutants) * 100
        
        Args:
            total_mutants: Total number of mutants generated
            killed_mutants: Number of mutants that were killed
        
        Returns:
            float: Survival rate as percentage (0-100)
        """
        if total_mutants == 0:
            return 0.0
        
        survived = total_mutants - killed_mutants
        rate = (survived / total_mutants) * 100
        return round(rate, 2)
    
    @staticmethod
    def calculate_equivalent_mutants(kill_ratios: List[float], threshold: float = 0.95) -> int:
        """
        Estimate number of equivalent mutants (mutants that produce identical results).
        
        Args:
            kill_ratios: List of kill ratios for each mutant
            threshold: Similarity threshold (0-1)
        
        Returns:
            int: Estimated number of equivalent mutants
        """
        # Count kill ratios close to 1.0 (equivalent mutants)
        equivalent = sum(1 for ratio in kill_ratios if ratio > threshold)
        return equivalent
    
    @staticmethod
    def calculate_score_metrics(mutant_results: List[Dict[str, Any]],
                               original_counts: Dict[str, int],
                               comparison_module) -> Dict[str, Any]:
        """
        Calculate comprehensive mutation score metrics.
        
        Args:
            mutant_results: List of mutant execution results
            original_counts: Original circuit execution counts
            comparison_module: Statistical comparison module
        
        Returns:
            Dict: Comprehensive score metrics
        """
        total_mutants = len(mutant_results)
        killed_mutants = 0
        survivor_ratios = []
        
        for mutant in mutant_results:
            mutant_counts = mutant['counts']
            
            # Compare using multiple metrics
            comparison = comparison_module.compare_distributions(
                original_counts, mutant_counts
            )
            
            # Determine if mutant is killed (significantly different)
            is_killed = False
            
            # Check Chi-Square test
            if 'chi_square' in comparison:
                if comparison['chi_square']['is_significantly_different']:
                    is_killed = True
            
            # Check JS divergence (threshold)
            if 'js_divergence' in comparison:
                if comparison['js_divergence'] > 0.1:
                    is_killed = True
            
            if is_killed:
                killed_mutants += 1
            
            # Store kill ratio
            if 'js_divergence' in comparison:
                survivor_ratios.append(comparison['js_divergence'])
        
        survived_mutants = total_mutants - killed_mutants
        
        return {
            'total_mutants': total_mutants,
            'killed_mutants': killed_mutants,
            'survived_mutants': survived_mutants,
            'mutation_score': MutationScoreCalculator.calculate_mutation_score(
                total_mutants, killed_mutants
            ),
            'survival_rate': MutationScoreCalculator.calculate_survival_rate(
                total_mutants, killed_mutants
            ),
            'kill_ratio': killed_mutants / total_mutants if total_mutants > 0 else 0.0,
            'avg_survivor_ratio': sum(survivor_ratios) / len(survivor_ratios) if survivor_ratios else 0.0
        }
    
    @staticmethod
    def interpret_score(mutation_score: float) -> str:
        """
        Interpret mutation score quality.
        
        Args:
            mutation_score: Mutation score (0-100)
        
        Returns:
            str: Quality interpretation
        """
        if mutation_score >= 80:
            return "Excellent - Test suite is very effective"
        elif mutation_score >= 60:
            return "Good - Test suite is effective"
        elif mutation_score >= 40:
            return "Fair - Test suite needs improvement"
        elif mutation_score >= 20:
            return "Poor - Test suite is weak"
        else:
            return "Very Poor - Test suite is inadequate"
    
    @staticmethod
    def calculate_operator_effectiveness(mutant_results: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate effectiveness of each mutation operator.
        
        Args:
            mutant_results: List of mutant execution results with operators
        
        Returns:
            Dict: Effectiveness score for each operator
        """
        operator_stats = {}
        
        for mutant in mutant_results:
            operator = mutant.get('operator', 'unknown')
            
            if operator not in operator_stats:
                operator_stats[operator] = {'total': 0, 'killed': 0}
            
            operator_stats[operator]['total'] += 1
            
            # Assume is_killed is provided in mutant result
            if mutant.get('is_killed', False):
                operator_stats[operator]['killed'] += 1
        
        # Calculate effectiveness for each operator
        effectiveness = {}
        for operator, stats in operator_stats.items():
            if stats['total'] > 0:
                effectiveness[operator] = (stats['killed'] / stats['total']) * 100
        
        return effectiveness
