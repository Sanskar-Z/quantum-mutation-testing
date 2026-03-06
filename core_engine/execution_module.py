"""
Core Mutation Testing Engine - Execution Module
Manages execution of original and mutant circuits.
"""
import time
from typing import Dict, List, Tuple, Any
from qiskit import QuantumCircuit
from quantum_execution.simulator import QuantumSimulator
import json


class ExecutionModule:
    """
    Manages execution of original and mutant circuits.
    """
    
    def __init__(self, num_shots: int = 1000, seed: int = None):
        """
        Initialize ExecutionModule.
        
        Args:
            num_shots: Number of shots for circuit execution
            seed: Random seed for reproducibility
        """
        self.num_shots = num_shots
        self.simulator = QuantumSimulator(seed=seed)
        self.execution_results = {}
    
    def execute_original_circuit(self, circuit: QuantumCircuit) -> Dict[str, Any]:
        """
        Execute the original circuit.
        
        Args:
            circuit: Original QuantumCircuit
        
        Returns:
            Dict: Execution results
        """
        counts, exec_time = self.simulator.execute_circuit(circuit, self.num_shots)
        
        result = {
            'circuit_type': 'original',
            'counts': counts,
            'execution_time': exec_time,
            'timestamp': time.time()
        }
        
        self.execution_results['original'] = result
        return result
    
    def execute_mutant_circuit(self, mutant: QuantumCircuit, mutant_id: int) -> Dict[str, Any]:
        """
        Execute a mutant circuit.
        
        Args:
            mutant: Mutant QuantumCircuit
            mutant_id: Identifier for the mutant
        
        Returns:
            Dict: Execution results
        """
        counts, exec_time = self.simulator.execute_circuit(mutant, self.num_shots)
        
        result = {
            'mutant_id': mutant_id,
            'circuit_type': 'mutant',
            'counts': counts,
            'execution_time': exec_time,
            'timestamp': time.time()
        }
        
        self.execution_results[f'mutant_{mutant_id}'] = result
        return result
    
    def execute_mutant_batch(self, mutants: List[Tuple[QuantumCircuit, str, dict]]) -> List[Dict[str, Any]]:
        """
        Execute multiple mutant circuits.
        
        Args:
            mutants: List of (circuit, operator, details) tuples
        
        Returns:
            List[Dict]: Execution results for all mutants
        """
        results = []
        for i, (mutant_circuit, operator, details) in enumerate(mutants):
            result = self.execute_mutant_circuit(mutant_circuit, i)
            result['operator'] = operator
            result['mutation_details'] = details
            results.append(result)
        
        return results
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """
        Get summary of all executions.
        
        Returns:
            Dict: Summary statistics
        """
        if not self.execution_results:
            return {}
        
        total_time = sum(
            result['execution_time'] 
            for result in self.execution_results.values()
        )
        
        return {
            'total_executions': len(self.execution_results),
            'total_time': total_time,
            'average_time': total_time / len(self.execution_results),
            'num_shots': self.num_shots
        }
    
    def compare_circuits(self, circuit1: QuantumCircuit, circuit2: QuantumCircuit) -> Dict[str, Any]:
        """
        Execute and compare two circuits.
        
        Args:
            circuit1: First circuit
            circuit2: Second circuit
        
        Returns:
            Dict: Comparison results
        """
        return self.simulator.compare_circuits(circuit1, circuit2, self.num_shots)
    
    def get_circuit_results(self, circuit_id: str) -> Dict[str, Any]:
        """
        Get results for a specific circuit execution.
        
        Args:
            circuit_id: Circuit identifier
        
        Returns:
            Dict: Execution results or empty dict if not found
        """
        return self.execution_results.get(circuit_id, {})
    
    def export_results(self, filepath: str = None) -> str:
        """
        Export execution results to JSON.
        
        Args:
            filepath: File path to save results
        
        Returns:
            str: JSON string of results
        """
        # Convert counts dict to string format for JSON serialization
        export_data = {}
        for key, result in self.execution_results.items():
            export_data[key] = {
                **result,
                'counts': {str(k): v for k, v in result['counts'].items()}
            }
        
        json_str = json.dumps(export_data, indent=2)
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(json_str)
        
        return json_str
