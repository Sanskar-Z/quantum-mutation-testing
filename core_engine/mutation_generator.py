"""
Core Mutation Testing Engine - Mutation Generation Module
Generates mutant circuits using various mutation operators.
"""
import random
import copy
import math
from typing import List, Dict, Tuple
from qiskit import QuantumCircuit
import numpy as np


class MutationGenerationModule:
    """
    Generates mutant circuits by applying mutation operators.
    Implements 5+ mutation operators for comprehensive testing.
    """
    
    # Single-qubit gates that can replace each other
    SINGLE_QUBIT_GATES = ['h', 'x', 'y', 'z', 's', 't']
    
    # Two-qubit gates that can replace each other
    TWO_QUBIT_GATES = ['cx', 'cz', 'swap']
    
    def __init__(self, seed: int = None):
        """
        Initialize MutationGenerationModule.
        
        Args:
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        self.mutation_count = 0
    
    def generate_mutants(self, circuit: QuantumCircuit, num_mutants: int = 10,
                        mutation_operators: List[str] = None) -> List[Tuple[QuantumCircuit, str, dict]]:
        """
        Generate multiple mutant circuits.
        
        Args:
            circuit: Original QuantumCircuit
            num_mutants: Number of mutants to generate
            mutation_operators: List of operators to use (None = use all)
        
        Returns:
            List[Tuple]: List of (mutant_circuit, operator_name, mutation_details)
        """
        if mutation_operators is None:
            mutation_operators = [
                'gate_replacement',
                'gate_removal',
                'rotation_angle_change',
                'qubit_swap',
                'gate_duplication'
            ]
        
        mutants = []
        for _ in range(num_mutants):
            operator = random.choice(mutation_operators)
            mutant, details = self.apply_mutation(circuit, operator)
            if mutant is not None:
                mutants.append((mutant, operator, details))
        
        return mutants
    
    def apply_mutation(self, circuit: QuantumCircuit, operator: str) -> Tuple[QuantumCircuit, dict]:
        """
        Apply a specific mutation operator to a circuit.
        
        Args:
            circuit: Original QuantumCircuit
            operator: Mutation operator name
        
        Returns:
            Tuple: (mutant_circuit, mutation_details)
        """
        if operator == 'gate_replacement':
            return self._gate_replacement(circuit)
        elif operator == 'gate_removal':
            return self._gate_removal(circuit)
        elif operator == 'rotation_angle_change':
            return self._rotation_angle_change(circuit)
        elif operator == 'qubit_swap':
            return self._qubit_swap(circuit)
        elif operator == 'gate_duplication':
            return self._gate_duplication(circuit)
        else:
            raise ValueError(f"Unknown mutation operator: {operator}")
    
    def _create_circuit_with_registers(self, original_circuit: QuantumCircuit) -> QuantumCircuit:
        """
        Create a new circuit with the same quantum and classical registers as the original.
        
        Args:
            original_circuit: Circuit to copy registers from
        
        Returns:
            QuantumCircuit: New circuit with preserved registers
        """
        qargs = []
        cargs = []
        
        # Add quantum registers
        for qreg in original_circuit.qregs:
            qargs.append(qreg)
        
        # Add classical registers
        for creg in original_circuit.cregs:
            cargs.append(creg)
        
        if qargs and cargs:
            return QuantumCircuit(*qargs, *cargs)
        elif qargs:
            return QuantumCircuit(*qargs)
        else:
            return QuantumCircuit(original_circuit.num_qubits)
    
    def _gate_replacement(self, circuit: QuantumCircuit) -> Tuple[QuantumCircuit, dict]:
        """
        Mutation Operator 1: Gate Replacement
        Replace a gate with a different gate of the same type.
        Example: H gate → X gate
        
        Args:
            circuit: Original circuit
        
        Returns:
            Tuple: (mutant_circuit, details)
        """
        mutant = circuit.copy()
        
        if mutant.size() == 0:
            return None, {}
        
        # Find all single-qubit and two-qubit gates
        gate_positions = []
        for i, instruction in enumerate(mutant.data):
            gate = instruction.operation
            if gate.num_qubits in [1, 2]:
                gate_positions.append(i)
        
        if not gate_positions:
            return None, {}
        
        # Select random gate to replace
        pos = random.choice(gate_positions)
        old_instruction = mutant.data[pos]
        old_gate = old_instruction.operation
        qubits = old_instruction.qubits
        
        # Choose replacement gate
        if old_gate.num_qubits == 1:
            replacement_gate = random.choice(self.SINGLE_QUBIT_GATES)
        elif old_gate.num_qubits == 2:
            replacement_gate = random.choice(self.TWO_QUBIT_GATES)
        else:
            return None, {}
        
        # Create new circuit with replaced gate
        mutant_new = self._create_circuit_with_registers(mutant)
        
        for i, instruction in enumerate(mutant.data):
            if i == pos:
                # Replace gate
                if old_gate.num_qubits == 1:
                    getattr(mutant_new, replacement_gate)(qubits[0])
                elif old_gate.num_qubits == 2:
                    getattr(mutant_new, replacement_gate)(qubits[0], qubits[1])
            else:
                mutant_new.append(instruction)
        
        self.mutation_count += 1
        return mutant_new, {
            'operator': 'gate_replacement',
            'position': pos,
            'old_gate': old_gate.name,
            'new_gate': replacement_gate,
            'mutation_id': self.mutation_count
        }
    
    def _gate_removal(self, circuit: QuantumCircuit) -> Tuple[QuantumCircuit, dict]:
        """
        Mutation Operator 2: Gate Removal
        Remove a randomly selected gate from the circuit.
        
        Args:
            circuit: Original circuit
        
        Returns:
            Tuple: (mutant_circuit, details)
        """
        mutant = circuit.copy()
        
        if mutant.size() == 0:
            return None, {}
        
        # Select random gate to remove
        pos = random.randint(0, mutant.size() - 1)
        removed_instruction = mutant.data[pos]
        removed_gate = removed_instruction.operation
        
        # Create new circuit without the gate
        mutant_new = self._create_circuit_with_registers(mutant)
        
        for i, instruction in enumerate(mutant.data):
            if i != pos:
                mutant_new.append(instruction)
        
        self.mutation_count += 1
        return mutant_new, {
            'operator': 'gate_removal',
            'position': pos,
            'removed_gate': removed_gate.name,
            'mutation_id': self.mutation_count
        }
    
    def _rotation_angle_change(self, circuit: QuantumCircuit) -> Tuple[QuantumCircuit, dict]:
        """
        Mutation Operator 3: Rotation Angle Change
        Modify rotation parameters of rotation gates (RX, RY, RZ).
        
        Args:
            circuit: Original circuit
        
        Returns:
            Tuple: (mutant_circuit, details)
        """
        mutant = circuit.copy()
        
        # Find rotation gates
        rotation_positions = []
        for i, instruction in enumerate(mutant.data):
            gate = instruction.operation
            if gate.name in ['rx', 'ry', 'rz', 'u1', 'u2', 'u3']:
                if hasattr(gate, 'params') and len(gate.params) > 0:
                    rotation_positions.append(i)
        
        if not rotation_positions:
            return None, {}
        
        # Select random rotation gate
        pos = random.choice(rotation_positions)
        old_instruction = mutant.data[pos]
        old_gate = old_instruction.operation
        qubits = old_instruction.qubits
        
        # Modify the angle
        old_angle = old_gate.params[0] if len(old_gate.params) > 0 else 0
        # Add a small random change to the angle
        angle_change = random.uniform(-math.pi, math.pi)
        new_angle = old_angle + angle_change
        new_angle = new_angle % (2 * math.pi)  # Keep in range [0, 2π]
        
        # Create new circuit with modified rotation
        mutant_new = self._create_circuit_with_registers(mutant)
        
        for i, instruction in enumerate(mutant.data):
            if i == pos:
                # Add modified rotation gate
                gate_name = old_gate.name.lower()
                if gate_name in ['rx', 'ry', 'rz']:
                    getattr(mutant_new, gate_name)(new_angle, qubits[0])
            else:
                mutant_new.append(instruction)
        
        self.mutation_count += 1
        return mutant_new, {
            'operator': 'rotation_angle_change',
            'position': pos,
            'gate': old_gate.name,
            'old_angle': float(old_angle),
            'new_angle': float(new_angle),
            'angle_change': float(angle_change),
            'mutation_id': self.mutation_count
        }
    
    def _qubit_swap(self, circuit: QuantumCircuit) -> Tuple[QuantumCircuit, dict]:
        """
        Mutation Operator 4: Qubit Swap
        Swap qubits in two-qubit gates.
        Example: CX(q0, q1) → CX(q1, q0)
        
        Args:
            circuit: Original circuit
        
        Returns:
            Tuple: (mutant_circuit, details)
        """
        mutant = circuit.copy()
        
        # Find two-qubit gates
        two_qubit_positions = []
        for i, instruction in enumerate(mutant.data):
            gate = instruction.operation
            if gate.num_qubits == 2:
                two_qubit_positions.append(i)
        
        if not two_qubit_positions:
            return None, {}
        
        # Select random two-qubit gate
        pos = random.choice(two_qubit_positions)
        old_instruction = mutant.data[pos]
        old_gate = old_instruction.operation
        qubits = old_instruction.qubits
        
        # Get swapped qubits - qubits are Qubit objects, use them directly
        q1, q2 = qubits[0], qubits[1]
        q1_idx = mutant.qubits.index(q1)
        q2_idx = mutant.qubits.index(q2)
        
        # Create new circuit with swapped qubits
        mutant_new = self._create_circuit_with_registers(mutant)
        
        for i, instruction in enumerate(mutant.data):
            if i == pos:
                # Add gate with swapped qubits
                gate_name = old_gate.name.lower()
                if gate_name in self.TWO_QUBIT_GATES:
                    getattr(mutant_new, gate_name)(q2, q1)
            else:
                mutant_new.append(instruction)
        
        self.mutation_count += 1
        return mutant_new, {
            'operator': 'qubit_swap',
            'position': pos,
            'gate': old_gate.name,
            'old_qubits': [q1_idx, q2_idx],
            'new_qubits': [q2_idx, q1_idx],
            'mutation_id': self.mutation_count
        }
    
    def _gate_duplication(self, circuit: QuantumCircuit) -> Tuple[QuantumCircuit, dict]:
        """
        Mutation Operator 5: Gate Duplication
        Duplicate a randomly selected gate.
        
        Args:
            circuit: Original circuit
        
        Returns:
            Tuple: (mutant_circuit, details)
        """
        mutant = circuit.copy()
        
        if mutant.size() == 0:
            return None, {}
        
        # Select random gate to duplicate
        pos = random.randint(0, mutant.size() - 1)
        duplicated_instruction = mutant.data[pos]
        duplicated_gate = duplicated_instruction.operation
        
        # Create new circuit with duplicated gate
        mutant_new = self._create_circuit_with_registers(mutant)
        
        for i, instruction in enumerate(mutant.data):
            mutant_new.append(instruction)
            if i == pos:
                # Duplicate the gate right after
                mutant_new.append(duplicated_instruction)
        
        self.mutation_count += 1
        return mutant_new, {
            'operator': 'gate_duplication',
            'position': pos,
            'duplicated_gate': duplicated_gate.name,
            'new_position': pos + 1,
            'mutation_id': self.mutation_count
        }
