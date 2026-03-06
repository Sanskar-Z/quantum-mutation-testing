"""
Basic System Tests
Tests for the mutation testing system.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from storage.database import DatabaseManager
from storage.models import Circuit, User
from quantum_execution.qiskit_interpreter import QiskitCircuitInterpreter
from quantum_execution.simulator import QuantumSimulator
from core_engine.circuit_validation import CircuitValidationModule
from core_engine.mutation_generator import MutationGenerationModule
from core_engine.execution_module import ExecutionModule
from core_engine.statistical_comparison import StatisticalComparisonModule
from backend.configuration_manager import ConfigurationManager
from backend.experiment_controller import ExperimentController


def test_database():
    """Test database operations."""
    print("Testing Database...")
    db = DatabaseManager(":memory:")
    
    # Test user creation
    user = User(db, username="test_user", email="test@example.com")
    user_id = user.create()
    assert user_id > 0, "User creation failed"
    print("✓ Database test passed")


def test_circuit_parsing():
    """Test circuit parsing from QASM."""
    print("Testing Circuit Parsing...")
    
    qasm = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q -> c;"""
    
    interpreter = QiskitCircuitInterpreter()
    circuit = interpreter.from_qasm_string(qasm)
    
    assert circuit.num_qubits == 2, "Circuit has wrong number of qubits"
    assert circuit.size() > 0, "Circuit has no gates"
    
    info = interpreter.get_circuit_info(circuit)
    print(f"  Circuit Info: {info}")
    print("✓ Circuit parsing test passed")


def test_circuit_validation():
    """Test circuit validation."""
    print("Testing Circuit Validation...")
    
    qasm = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q -> c;"""
    
    interpreter = QiskitCircuitInterpreter()
    circuit = interpreter.from_qasm_string(qasm)
    
    validator = CircuitValidationModule()
    is_valid, errors = validator.validate_circuit(circuit)
    
    assert is_valid, f"Circuit validation failed: {errors}"
    print("✓ Circuit validation test passed")


def test_quantum_simulator():
    """Test quantum circuit execution."""
    print("Testing Quantum Simulator...")
    
    qasm = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q -> c;"""
    
    interpreter = QiskitCircuitInterpreter()
    circuit = interpreter.from_qasm_string(qasm)
    
    simulator = QuantumSimulator()
    counts, exec_time = simulator.execute_circuit(circuit, shots=1000)
    
    assert len(counts) > 0, "No results from execution"
    assert exec_time > 0, "Execution time is invalid"
    
    print(f"  Results: {dict(list(counts.items())[:3])}")
    print(f"  Execution Time: {exec_time:.3f}s")
    print("✓ Quantum simulator test passed")


def test_mutation_generation():
    """Test mutation generation."""
    print("Testing Mutation Generation...")
    
    qasm = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q -> c;"""
    
    interpreter = QiskitCircuitInterpreter()
    circuit = interpreter.from_qasm_string(qasm)
    
    generator = MutationGenerationModule(seed=42)
    mutants = generator.generate_mutants(circuit, num_mutants=5)
    
    assert len(mutants) == 5, f"Expected 5 mutants, got {len(mutants)}"
    
    for i, (mutant, operator, details) in enumerate(mutants):
        print(f"  Mutant {i+1}: {operator}")
    
    print("✓ Mutation generation test passed")


def test_statistical_comparison():
    """Test statistical comparison."""
    print("Testing Statistical Comparison...")
    
    original_counts = {'00': 500, '11': 500}
    mutant_counts = {'00': 600, '11': 400}
    
    comp = StatisticalComparisonModule()
    
    # Test Chi-Square
    chi2, p_val, is_diff = comp.chi_square_test(original_counts, mutant_counts)
    print(f"  Chi-Square: χ²={chi2:.4f}, p={p_val:.4f}, different={is_diff}")
    
    # Test KL Divergence
    kl = comp.kl_divergence(original_counts, mutant_counts)
    print(f"  KL Divergence: {kl:.4f}")
    
    print("✓ Statistical comparison test passed")


def test_configuration():
    """Test configuration manager."""
    print("Testing Configuration Manager...")
    
    config = ConfigurationManager()
    
    config.set_parameter('num_shots', 2000)
    assert config.get_parameter('num_shots') == 2000, "Configuration set failed"
    
    is_valid, errors = config.validate_config()
    assert is_valid, f"Configuration validation failed: {errors}"
    
    print(f"  Config Parameters: {len(config.get_all_parameters())} items")
    print("✓ Configuration test passed")


def test_experiment_controller():
    """Test experiment controller."""
    print("Testing Experiment Controller...")
    
    controller = ExperimentController()
    
    qasm = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q -> c;"""
    
    # Configure
    controller.configure_experiment({
        'num_shots': 500,
        'num_mutants': 5,
        'mutation_operators': ['gate_replacement', 'gate_removal']
    })
    
    # Create experiment
    results = controller.create_experiment(
        circuit_input=qasm,
        circuit_name='test_circuit',
        input_format='qasm'
    )
    
    assert results['success'], f"Experiment failed: {results.get('error')}"
    assert 'mutation_score' in results, "Mutation score not in results"
    
    print(f"  Mutation Score: {results['mutation_score']:.2f}%")
    print(f"  Total Mutants: {results['total_mutants']}")
    print("✓ Experiment controller test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Quantum Mutation Testing System - Unit Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_database,
        test_circuit_parsing,
        test_circuit_validation,
        test_quantum_simulator,
        test_mutation_generation,
        test_statistical_comparison,
        test_configuration,
        test_experiment_controller
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ Test failed: {str(e)}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
