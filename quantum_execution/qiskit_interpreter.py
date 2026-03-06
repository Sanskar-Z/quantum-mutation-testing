"""
Quantum Execution Layer - Qiskit Interpreter Module
Converts QASM strings into Qiskit QuantumCircuit objects.
"""
import re
from typing import Tuple, Dict, Any, Optional
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Instruction


class QiskitCircuitInterpreter:
    """
    Interprets and converts QASM and other formats into Qiskit QuantumCircuit objects.
    """
    
    @staticmethod
    def from_qasm_string(qasm_code: str) -> QuantumCircuit:
        """
        Create a Qiskit QuantumCircuit from QASM string.
        
        Args:
            qasm_code: QASM format quantum circuit code
        
        Returns:
            QuantumCircuit: Qiskit quantum circuit object
        
        Raises:
            ValueError: If QASM code is invalid
        """
        try:
            circuit = QuantumCircuit.from_qasm_str(qasm_code)
            return circuit
        except Exception as e:
            raise ValueError(f"Invalid QASM code: {str(e)}")
    
    @staticmethod
    def from_dict(circuit_dict: Dict[str, Any]) -> QuantumCircuit:
        """
        Create a QuantumCircuit from dictionary specification.
        
        Args:
            circuit_dict: Dictionary with circuit specification
                        Expected keys: 'num_qubits', 'gates' (list of gate dicts)
        
        Returns:
            QuantumCircuit: Qiskit quantum circuit object
        """
        num_qubits = circuit_dict.get('num_qubits', 2)
        circuit = QuantumCircuit(num_qubits)
        
        gates = circuit_dict.get('gates', [])
        for gate_spec in gates:
            gate_name = gate_spec.get('name')
            qubits = gate_spec.get('qubits', [])
            params = gate_spec.get('params', [])
            
            QiskitCircuitInterpreter._add_gate_to_circuit(
                circuit, gate_name, qubits, params
            )
        
        return circuit
    
    @staticmethod
    def _add_gate_to_circuit(circuit: QuantumCircuit, gate_name: str, 
                            qubits: list, params: list = None):
        """
        Add a gate to the circuit.
        
        Args:
            circuit: QuantumCircuit to modify
            gate_name: Name of the gate (h, x, y, z, rx, ry, rz, cx, etc.)
            qubits: List of qubit indices
            params: Optional parameters for parameterized gates
        """
        if not qubits:
            return
        
        gate_name = gate_name.lower()
        
        # Single-qubit gates
        if gate_name == 'h':
            circuit.h(qubits[0])
        elif gate_name == 'x':
            circuit.x(qubits[0])
        elif gate_name == 'y':
            circuit.y(qubits[0])
        elif gate_name == 'z':
            circuit.z(qubits[0])
        elif gate_name == 's':
            circuit.s(qubits[0])
        elif gate_name == 't':
            circuit.t(qubits[0])
        elif gate_name == 'sdg':
            circuit.sdg(qubits[0])
        elif gate_name == 'tdg':
            circuit.tdg(qubits[0])
        elif gate_name == 'rx' and params:
            circuit.rx(params[0], qubits[0])
        elif gate_name == 'ry' and params:
            circuit.ry(params[0], qubits[0])
        elif gate_name == 'rz' and params:
            circuit.rz(params[0], qubits[0])
        # Two-qubit gates
        elif gate_name == 'cx' or gate_name == 'cnot':
            if len(qubits) >= 2:
                circuit.cx(qubits[0], qubits[1])
        elif gate_name == 'cz':
            if len(qubits) >= 2:
                circuit.cz(qubits[0], qubits[1])
        elif gate_name == 'swap':
            if len(qubits) >= 2:
                circuit.swap(qubits[0], qubits[1])
        elif gate_name == 'ch':
            if len(qubits) >= 2:
                circuit.ch(qubits[0], qubits[1])
    
    @staticmethod
    def to_qasm_string(circuit: QuantumCircuit) -> str:
        """
        Convert Qiskit QuantumCircuit to QASM string.
        
        Args:
            circuit: QuantumCircuit to convert
        
        Returns:
            str: QASM format string
        """
        return circuit.qasm()
    
    @staticmethod
    def get_circuit_info(circuit: QuantumCircuit) -> Dict[str, Any]:
        """
        Get information about a circuit.
        
        Args:
            circuit: QuantumCircuit to analyze
        
        Returns:
            Dict with circuit information (num_qubits, num_gates, depth, etc.)
        """
        return {
            'num_qubits': circuit.num_qubits,
            'num_gates': circuit.size(),
            'depth': circuit.depth(),
            'operations': list(circuit.count_ops().elements()),
            'width': len(circuit.qregs) + len(circuit.cregs)
        }
    
    @staticmethod
    def validate_circuit(circuit: QuantumCircuit) -> Tuple[bool, str]:
        """
        Validate a Qiskit circuit.
        
        Args:
            circuit: QuantumCircuit to validate
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            if circuit.num_qubits == 0:
                return False, "Circuit has no qubits"
            if circuit.size() == 0:
                return False, "Circuit has no gates"
            return True, "Circuit is valid"
        except Exception as e:
            return False, f"Circuit validation failed: {str(e)}"
