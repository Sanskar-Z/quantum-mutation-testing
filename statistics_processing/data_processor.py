"""
Statistics and Data Processing Layer - Data Processor Module
Processes and organizes execution results for analysis.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from collections import Counter


class DataProcessor:
    """
    Processes quantum circuit execution data for analysis.
    """
    
    @staticmethod
    def normalize_counts(counts: Dict[str, int]) -> Dict[str, float]:
        """
        Normalize count dictionary to probabilities.
        
        Args:
            counts: Count dictionary {bitstring: count}
        
        Returns:
            Dict: Probability dictionary {bitstring: probability}
        """
        total = sum(counts.values())
        if total == 0:
            return {}
        
        return {state: count / total for state, count in counts.items()}
    
    @staticmethod
    def counts_to_dataframe(results: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Convert execution results to pandas DataFrame.
        
        Args:
            results: List of execution result dictionaries
        
        Returns:
            pd.DataFrame: DataFrame with results
        """
        data = []
        
        for result in results:
            counts = result.get('counts', {})
            for bitstring, count in counts.items():
                data.append({
                    'result_id': result.get('mutant_id', 'original'),
                    'bitstring': bitstring,
                    'count': count,
                    'operator': result.get('operator', 'N/A'),
                    'probability': count / sum(counts.values()) if counts else 0
                })
        
        return pd.DataFrame(data)
    
    @staticmethod
    def calculate_statistics(counts: Dict[str, int]) -> Dict[str, Any]:
        """
        Calculate statistical measures for a count distribution.
        
        Args:
            counts: Count dictionary
        
        Returns:
            Dict: Statistical measures
        """
        if not counts:
            return {}
        
        probs = DataProcessor.normalize_counts(counts)
        values = list(probs.values())
        
        return {
            'mean': np.mean(values),
            'median': np.median(values),
            'std_dev': np.std(values),
            'min': np.min(values),
            'max': np.max(values),
            'entropy': DataProcessor._calculate_entropy(probs),
            'num_states': len(probs)
        }
    
    @staticmethod
    def _calculate_entropy(probs: Dict[str, float]) -> float:
        """
        Calculate Shannon entropy of a probability distribution.
        
        Args:
            probs: Probability dictionary
        
        Returns:
            float: Shannon entropy
        """
        entropy = 0.0
        for prob in probs.values():
            if prob > 0:
                entropy -= prob * np.log2(prob)
        return entropy
    
    @staticmethod
    def aggregate_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate results from multiple executions.
        
        Args:
            results: List of execution results
        
        Returns:
            Dict: Aggregated statistics
        """
        if not results:
            return {}
        
        df = DataProcessor.counts_to_dataframe(results)
        
        return {
            'total_executions': len(results),
            'total_samples': df['count'].sum(),
            'unique_states': df['bitstring'].nunique(),
            'operators_used': df['operator'].unique().tolist() if 'operator' in df.columns else [],
            'average_state_count': df.groupby('result_id')['count'].sum().mean()
        }
    
    @staticmethod
    def extract_top_states(counts: Dict[str, int], top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Extract top N most probable states.
        
        Args:
            counts: Count dictionary
            top_n: Number of top states to extract
        
        Returns:
            List: Top states as [(bitstring, count)] sorted by count
        """
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_counts[:top_n]
    
    @staticmethod
    def compare_count_distributions(original: Dict[str, int],
                                   mutant: Dict[str, int]) -> Dict[str, Any]:
        """
        Compare two count distributions and extract differences.
        
        Args:
            original: Original circuit counts
            mutant: Mutant circuit counts
        
        Returns:
            Dict: Comparison statistics
        """
        all_states = set(original.keys()) | set(mutant.keys())
        
        original_probs = DataProcessor.normalize_counts(original)
        mutant_probs = DataProcessor.normalize_counts(mutant)
        
        differences = {}
        for state in all_states:
            orig_prob = original_probs.get(state, 0)
            mut_prob = mutant_probs.get(state, 0)
            diff = abs(orig_prob - mut_prob)
            if diff > 0:
                differences[state] = diff
        
        sorted_diff = sorted(differences.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'total_different_states': len(differences),
            'max_probability_diff': sorted_diff[0][1] if sorted_diff else 0,
            'avg_probability_diff': np.mean(list(differences.values())) if differences else 0,
            'top_different_states': sorted_diff[:5]
        }
