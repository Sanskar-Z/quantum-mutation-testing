"""
Core Mutation Testing Engine - Circuit Validation Module
Validates quantum circuits for correctness and compatibility.
"""
import re
from typing import Tuple, List
from qiskit import QuantumCircuit


class CircuitValidationModule:
    """
    Validates quantum circuits for correctness and mutation testing compatibility.
    """
    
    # Valid gate names in QASM
    VALID_SINGLE_QUBIT_GATES = {
        'h', 'x', 'y', 'z', 's', 't', 'sdg', 'tdg', 'id',
        'rx', 'ry', 'rz', 'u1', 'u2', 'u3', 'p'
    }
    
    VALID_TWO_QUBIT_GATES = {
        'cx', 'cnot', 'cz', 'cy', 'ch', 'csx', 'swap',
        'iswap', 'ecr', 'rxx', 'ryy', 'rzz'
    }
    
    VALID_THREE_QUBIT_GATES = {
        'ccx', 'toffoli', 'cswap', 'fredkin', 'ccz'
    }
    
    @staticmethod
    def validate_qasm(qasm_code: str) -> Tuple[bool, List[str]]:
        """
        Validate QASM code syntax.
        
        Args:
            qasm_code: QASM format circuit code
        
        Returns:
            Tuple[bool, List[str]]: (is_valid, error_messages)
        """
        errors = []
        
        if not qasm_code or not qasm_code.strip():
            errors.append("QASM code is empty")
            return False, errors
        
        lines = qasm_code.strip().split('\n')
        
        # Check for OPENQASM declaration
        has_openqasm = any('OPENQASM' in line for line in lines)
        if not has_openqasm:
            errors.append("Missing OPENQASM declaration")
        
        # Check for quantum register
        has_qreg = any('qreg' in line for line in lines)
        if not has_qreg:
            errors.append("Missing quantum register declaration")
        
        # Basic validation of gate lines
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('//'):
                continue
            
            # Skip declarations
            if line.startswith('OPENQASM') or line.startswith('include') or \
               'qreg' in line or 'creg' in line or line.endswith(';'):
                continue
            
            # Validate gate syntax (basic check)
            if not line.endswith(';'):
                errors.append(f"Line {i}: Gate statement must end with semicolon")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_circuit(circuit: QuantumCircuit) -> Tuple[bool, List[str]]:
        """
        Validate a Qiskit QuantumCircuit.
        
        Args:
            circuit: QuantumCircuit to validate
        
        Returns:
            Tuple[bool, List[str]]: (is_valid, error_messages)
        """
        errors = []
        
        # Check number of qubits
        if circuit.num_qubits == 0:
            errors.append("Circuit has no qubits")
        
        # Check circuit size
        if circuit.size() == 0:
            errors.append("Circuit has no gates")
        
        # Check circuit depth
        if circuit.depth() == 0 and circuit.size() > 0:
            errors.append("Circuit has invalid depth")
        
        # Check for valid operations
        try:
            ops = circuit.count_ops()
            for op_name in ops.keys():
                if not CircuitValidationModule._is_valid_operation(op_name):
                    errors.append(f"Unknown operation: {op_name}")
        except Exception as e:
            errors.append(f"Error checking operations: {str(e)}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def _is_valid_operation(op_name: str) -> bool:
        """Check if operation is valid."""
        op_name_lower = op_name.lower()
        return (op_name_lower in CircuitValidationModule.VALID_SINGLE_QUBIT_GATES or
                op_name_lower in CircuitValidationModule.VALID_TWO_QUBIT_GATES or
                op_name_lower in CircuitValidationModule.VALID_THREE_QUBIT_GATES or
                op_name_lower == 'measure' or op_name_lower == 'barrier')
    
    @staticmethod
    def validate_circuit_compatibility(circuit: QuantumCircuit, 
                                       max_qubits: int = 20) -> Tuple[bool, List[str]]:
        """
        Validate circuit compatibility with system constraints.
        
        Args:
            circuit: QuantumCircuit to validate
            max_qubits: Maximum number of qubits allowed
        
        Returns:
            Tuple[bool, List[str]]: (is_compatible, error_messages)
        """
        errors = []
        
        if circuit.num_qubits > max_qubits:
            errors.append(f"Circuit has {circuit.num_qubits} qubits, max allowed: {max_qubits}")
        
        # Check circuit complexity
        if circuit.depth() > 1000:
            errors.append(f"Circuit depth {circuit.depth()} exceeds recommended limit of 1000")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def get_circuit_stats(circuit: QuantumCircuit) -> dict:
        """
        Get detailed statistics about a circuit.
        
        Args:
            circuit: QuantumCircuit to analyze
        
        Returns:
            dict: Statistics including num_qubits, num_gates, depth, etc.
        """
        ops = circuit.count_ops()
        
        return {
            'num_qubits': circuit.num_qubits,
            'num_gates': circuit.size(),
            'depth': circuit.depth(),
            'operations': dict(ops),
            'num_operations': len(ops),
            'num_classical_bits': circuit.num_clbits,
            'parameters': [str(p) for p in circuit.parameters]
        }
    
    @staticmethod
    def identify_mutation_points(circuit: QuantumCircuit) -> List[dict]:
        """
        Identify all potential mutation points in a circuit.
        
        Args:
            circuit: QuantumCircuit to analyze
        
        Returns:
            List[dict]: List of mutation points with metadata
        """
        mutation_points = []
        
        for i, instruction in enumerate(circuit.data):
            gate = instruction.operation
            qubits = instruction.qubits
            
            mutation_points.append({
                'index': i,
                'gate_name': gate.name,
                'num_qubits_involved': len(qubits),
                'qubits': [q.index for q in qubits],
                'parameters': gate.params if hasattr(gate, 'params') else [],
                'is_parametric': len(gate.params) > 0 if hasattr(gate, 'params') else False
            })
        
        return mutation_points
