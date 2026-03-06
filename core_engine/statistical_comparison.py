"""
Core Mutation Testing Engine - Statistical Comparison Module
Implements statistical tests to compare circuit execution results.
"""
import numpy as np
from typing import Dict, Tuple, Any
from scipy.stats import chi2_contingency
from scipy.spatial.distance import jensenshannon
import math


class StatisticalComparisonModule:
    """
    Performs statistical comparisons between original and mutant circuit results.
    """
    
    @staticmethod
    def chi_square_test(original_counts: Dict[str, int], 
                       mutant_counts: Dict[str, int]) -> Tuple[float, float, bool]:
        """
        Perform Chi-Square test to compare two distributions.
        
        Args:
            original_counts: Count distribution from original circuit
            mutant_counts: Count distribution from mutant circuit
        
        Returns:
            Tuple[chi2_stat, p_value, is_significantly_different]
            where is_significantly_different True if p_value < 0.05
        """
        # Get all possible states
        all_states = set(original_counts.keys()) | set(mutant_counts.keys())
        
        # Create contingency table
        observed = []
        for state in all_states:
            observed.append([
                original_counts.get(state, 0),
                mutant_counts.get(state, 0)
            ])
        
        observed = np.array(observed)
        
        # Perform Chi-Square test
        try:
            chi2_stat, p_value, dof, expected = chi2_contingency(observed)
            
            # Check if significantly different (p < 0.05)
            is_different = p_value < 0.05
            
            return chi2_stat, p_value, is_different
        except Exception as e:
            # Return default values if test fails
            return 0.0, 1.0, False
    
    @staticmethod
    def kl_divergence(original_counts: Dict[str, int],
                     mutant_counts: Dict[str, int]) -> float:
        """
        Calculate Kullback-Leibler (KL) Divergence between two distributions.
        
        Formula: KL(P||Q) = Σ P(x) * log(P(x) / Q(x))
        
        Args:
            original_counts: Count distribution from original circuit (P)
            mutant_counts: Count distribution from mutant circuit (Q)
        
        Returns:
            float: KL divergence value
        """
        # Normalize counts to probabilities
        total_orig = sum(original_counts.values())
        total_mut = sum(mutant_counts.values())
        
        if total_orig == 0 or total_mut == 0:
            return float('inf')
        
        # Get all possible states
        all_states = set(original_counts.keys()) | set(mutant_counts.keys())
        
        # Calculate probabilities
        p = np.array([original_counts.get(state, 0) / total_orig for state in all_states])
        q = np.array([mutant_counts.get(state, 0) / total_mut for state in all_states])
        
        # Add small epsilon to avoid log(0)
        epsilon = 1e-10
        p = np.where(p > 0, p, epsilon)
        q = np.where(q > 0, q, epsilon)
        
        # Calculate KL divergence
        kl_div = np.sum(p * np.log(p / q))
        
        return float(kl_div)
    
    @staticmethod
    def jensen_shannon_divergence(original_counts: Dict[str, int],
                                  mutant_counts: Dict[str, int]) -> float:
        """
        Calculate Jensen-Shannon divergence between two distributions.
        
        JS divergence is symmetric: JS(P||Q) = JS(Q||P)
        Unlike KL divergence, JS is always finite and symmetric.
        
        Args:
            original_counts: Count distribution from original circuit
            mutant_counts: Count distribution from mutant circuit
        
        Returns:
            float: Jensen-Shannon divergence value (0-1)
        """
        # Normalize counts to probabilities
        total_orig = sum(original_counts.values())
        total_mut = sum(mutant_counts.values())
        
        if total_orig == 0 or total_mut == 0:
            return 0.0
        
        # Get all possible states
        all_states = set(original_counts.keys()) | set(mutant_counts.keys())
        
        # Calculate probabilities
        p = np.array([original_counts.get(state, 0) / total_orig for state in all_states])
        q = np.array([mutant_counts.get(state, 0) / total_mut for state in all_states])
        
        # Calculate Jensen-Shannon divergence
        js_div = jensenshannon(p, q)
        
        return float(js_div)
    
    @staticmethod
    def hellinger_distance(original_counts: Dict[str, int],
                          mutant_counts: Dict[str, int]) -> float:
        """
        Calculate Hellinger distance between two distributions.
        
        Args:
            original_counts: Count distribution from original circuit
            mutant_counts: Count distribution from mutant circuit
        
        Returns:
            float: Hellinger distance (0-1)
        """
        # Normalize counts to probabilities
        total_orig = sum(original_counts.values())
        total_mut = sum(mutant_counts.values())
        
        if total_orig == 0 or total_mut == 0:
            return 1.0
        
        # Get all possible states
        all_states = set(original_counts.keys()) | set(mutant_counts.keys())
        
        # Calculate probabilities
        p = np.array([original_counts.get(state, 0) / total_orig for state in all_states])
        q = np.array([mutant_counts.get(state, 0) / total_mut for state in all_states])
        
        # Calculate Hellinger distance
        bc = np.sum(np.sqrt(p * q))  # Bhattacharyya coefficient
        hellinger = np.sqrt(1 - bc)
        
        return float(hellinger)
    
    @staticmethod
    def total_variation_distance(original_counts: Dict[str, int],
                                mutant_counts: Dict[str, int]) -> float:
        """
        Calculate Total Variation Distance between two distributions.
        
        Args:
            original_counts: Count distribution from original circuit
            mutant_counts: Count distribution from mutant circuit
        
        Returns:
            float: Total variation distance (0-1)
        """
        # Normalize counts to probabilities
        total_orig = sum(original_counts.values())
        total_mut = sum(mutant_counts.values())
        
        if total_orig == 0 or total_mut == 0:
            return 1.0
        
        # Get all possible states
        all_states = set(original_counts.keys()) | set(mutant_counts.keys())
        
        # Calculate total variation distance
        tvd = 0.0
        for state in all_states:
            p = original_counts.get(state, 0) / total_orig
            q = mutant_counts.get(state, 0) / total_mut
            tvd += abs(p - q)
        
        return tvd / 2.0
    
    @staticmethod
    def compare_distributions(original_counts: Dict[str, int],
                             mutant_counts: Dict[str, int],
                             metrics: list = None) -> Dict[str, Any]:
        """
        Compare two distributions using multiple metrics.
        
        Args:
            original_counts: Count distribution from original circuit
            mutant_counts: Count distribution from mutant circuit
            metrics: List of metrics to compute (None = all)
        
        Returns:
            Dict: Results for all requested metrics
        """
        if metrics is None:
            metrics = ['chi_square', 'kl_divergence', 'js_divergence', 
                      'hellinger', 'total_variation']
        
        results = {}
        
        for metric in metrics:
            if metric == 'chi_square':
                chi2, p_val, is_diff = StatisticalComparisonModule.chi_square_test(
                    original_counts, mutant_counts
                )
                results['chi_square'] = {
                    'statistic': chi2,
                    'p_value': p_val,
                    'is_significantly_different': is_diff
                }
            elif metric == 'kl_divergence':
                kl = StatisticalComparisonModule.kl_divergence(
                    original_counts, mutant_counts
                )
                results['kl_divergence'] = kl
            elif metric == 'js_divergence':
                js = StatisticalComparisonModule.jensen_shannon_divergence(
                    original_counts, mutant_counts
                )
                results['js_divergence'] = js
            elif metric == 'hellinger':
                hell = StatisticalComparisonModule.hellinger_distance(
                    original_counts, mutant_counts
                )
                results['hellinger_distance'] = hell
            elif metric == 'total_variation':
                tv = StatisticalComparisonModule.total_variation_distance(
                    original_counts, mutant_counts
                )
                results['total_variation_distance'] = tv
        
        return results
