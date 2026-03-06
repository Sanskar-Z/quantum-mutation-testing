"""
Quantum Execution Layer - Simulator Module
Executes quantum circuits using Qiskit Aer simulator.
"""
import time
from typing import Dict, List, Any, Tuple
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.result import Result
import numpy as np


class QuantumSimulator:
    """
    Executes quantum circuits using Qiskit Aer simulator.
    """
    
    def __init__(self, backend_name: str = 'aer_simulator', seed: int = None):
        """
        Initialize QuantumSimulator.
        
        Args:
            backend_name: Name of the simulator backend (default: aer_simulator)
            seed: Random seed for reproducible results
        """
        self.backend_name = backend_name
        self.seed = seed
        self.simulator = AerSimulator()
    
    def execute_circuit(self, circuit: QuantumCircuit, shots: int = 1000) -> Dict[str, int]:
        """
        Execute a quantum circuit.
        
        Args:
            circuit: QuantumCircuit to execute
            shots: Number of iterations to run the circuit
        
        Returns:
            Dict: Output counts {bitstring: count}
        """
        try:
            # Add measurement if not present
            measured_circuit = self._add_measurements(circuit)
            
            # Execute the circuit
            start_time = time.time()
            job = self.simulator.run(measured_circuit, shots=shots, seed_simulator=self.seed)
            result = job.result()
            execution_time = time.time() - start_time
            
            # Get counts
            counts = result.get_counts(0)
            
            return counts, execution_time
        except Exception as e:
            raise RuntimeError(f"Circuit execution failed: {str(e)}")
    
    def execute_multiple_circuits(self, circuits: List[QuantumCircuit], 
                                 shots: int = 1000) -> List[Tuple[Dict[str, int], float]]:
        """
        Execute multiple quantum circuits.
        
        Args:
            circuits: List of QuantumCircuits to execute
            shots: Number of shots for each circuit
        
        Returns:
            List[Tuple]: List of (counts_dict, execution_time) tuples
        """
        results = []
        for circuit in circuits:
            counts, exec_time = self.execute_circuit(circuit, shots)
            results.append((counts, exec_time))
        return results
    
    def _add_measurements(self, circuit: QuantumCircuit) -> QuantumCircuit:
        """
        Add measurements to all qubits if not present.
        
        Args:
            circuit: QuantumCircuit to measure
        
        Returns:
            QuantumCircuit: Circuit with measurements
        """
        circuit_copy = circuit.copy()
        
        # Check if circuit already has measurements
        if len(circuit_copy.clbits) == 0:
            circuit_copy.measure_all()
        
        return circuit_copy
    
    def get_statevector(self, circuit: QuantumCircuit) -> np.ndarray:
        """
        Get statevector of a circuit (without measurements).
        
        Args:
            circuit: QuantumCircuit
        
        Returns:
            np.ndarray: The statevector
        """
        try:
            # Create a statevector simulator
            statevector_simulator = AerSimulator(method='statevector')
            job = statevector_simulator.run(circuit)
            result = job.result()
            statevector = result.get_statevector(0)
            return statevector
        except Exception as e:
            raise RuntimeError(f"Statevector calculation failed: {str(e)}")
    
    def get_unitary(self, circuit: QuantumCircuit) -> np.ndarray:
        """
        Get unitary matrix of a circuit.
        
        Args:
            circuit: QuantumCircuit (must be unitary)
        
        Returns:
            np.ndarray: The unitary matrix
        """
        try:
            unitary_simulator = AerSimulator(method='unitary')
            job = unitary_simulator.run(circuit)
            result = job.result()
            unitary = result.get_unitary(0)
            return unitary
        except Exception as e:
            raise RuntimeError(f"Unitary calculation failed: {str(e)}")
    
    def calculate_expectation_value(self, circuit: QuantumCircuit, 
                                   observable: str = 'Z', qubit: int = 0,
                                   shots: int = 1000) -> float:
        """
        Calculate expectation value for a given observable.
        
        Args:
            circuit: QuantumCircuit
            observable: Observable operator ('X', 'Y', or 'Z')
            qubit: Qubit index
            shots: Number of shots
        
        Returns:
            float: Expectation value
        """
        measured_circuit = self._add_measurements(circuit)
        counts, _ = self.execute_circuit(measured_circuit, shots)
        
        expectation = 0.0
        for bitstring, count in counts.items():
            # Get the bit of interest
            bit_value = int(bitstring[-(qubit + 1)])  # Reverse indexing
            eigenvalue = 1 if bit_value == 0 else -1
            expectation += eigenvalue * count
        
        return expectation / shots
    
    def compare_circuits(self, circuit1: QuantumCircuit, circuit2: QuantumCircuit,
                        shots: int = 1000) -> Dict[str, Any]:
        """
        Compare execution results of two circuits.
        
        Args:
            circuit1: First QuantumCircuit
            circuit2: Second QuantumCircuit
            shots: Number of shots for each circuit
        
        Returns:
            Dict: Comparison results including counts for both circuits
        """
        counts1, time1 = self.execute_circuit(circuit1, shots)
        counts2, time2 = self.execute_circuit(circuit2, shots)
        
        return {
            'circuit1_counts': counts1,
            'circuit2_counts': counts2,
            'circuit1_time': time1,
            'circuit2_time': time2,
            'counts_match': self._counts_match(counts1, counts2),
            'total_time': time1 + time2
        }
    
    @staticmethod
    def _counts_match(counts1: Dict[str, int], counts2: Dict[str, int], 
                     threshold: float = 0.95) -> bool:
        """
        Check if two count distributions are similar.
        
        Args:
            counts1: Count dictionary 1
            counts2: Count dictionary 2
            threshold: Similarity threshold (0-1)
        
        Returns:
            bool: True if counts are similar
        """
        # Normalize counts to probabilities
        total1 = sum(counts1.values())
        total2 = sum(counts2.values())
        
        prob1 = {k: v/total1 for k, v in counts1.items()}
        prob2 = {k: v/total2 for k, v in counts2.items()}
        
        # Get all possible bitstrings
        all_states = set(prob1.keys()) | set(prob2.keys())
        
        # Calculate similarity (overlap of probabilities)
        similarity = 0.0
        for state in all_states:
            similarity += min(prob1.get(state, 0), prob2.get(state, 0))
        
        return similarity >= threshold
