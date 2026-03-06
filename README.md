# Quantum Circuit Mutation Testing System

Automated Test Generation and Bug Detection for Quantum Circuits using Mutation Testing

## Overview

This project implements a comprehensive mutation testing framework for quantum circuits. It allows users to:

- **Upload** quantum circuits in QASM format
- **Configure** mutation parameters and testing settings
- **Generate** multiple mutant circuits using various mutation operators
- **Execute** circuits on quantum simulators
- **Compare** results using statistical methods
- **Calculate** mutation scores to assess test suite quality
- **Generate** detailed reports and visualizations

## Architecture

The system follows a strict 6-layer architecture:

```
┌─────────────────────────────────────────────┐
│    1. User Interface Layer (Streamlit)      │
├─────────────────────────────────────────────┤
│   2. Application Control Layer              │
│   (ExperimentController, ConfigurationMgr)  │
├─────────────────────────────────────────────┤
│   3. Core Mutation Testing Engine           │
│   (Validation, Generation, Comparison)      │
├─────────────────────────────────────────────┤
│   4. Quantum Execution Layer                │
│   (Qiskit Interpreter, Simulator)           │
├─────────────────────────────────────────────┤
│   5. Statistics & Data Processing           │
│   (Data Processor, Visualization)           │
├─────────────────────────────────────────────┤
│   6. Storage Layer (SQLite)                 │
│   (Database, Models)                        │
└─────────────────────────────────────────────┘
```

## Project Structure

```
quantum-mutation-testing/
│
├── frontend/
│   └── app.py                          # Streamlit web interface
│
├── backend/
│   ├── experiment_controller.py         # Main experiment orchestrator
│   ├── configuration_manager.py         # Configuration management
│   └── workflow_manager.py              # Workflow pipeline
│
├── core_engine/
│   ├── circuit_validation.py            # Circuit validation module
│   ├── mutation_generator.py            # Mutation operators (5+)
│   ├── execution_module.py              # Circuit execution manager
│   ├── statistical_comparison.py        # Statistical tests
│   ├── mutation_score_calculator.py     # Score calculation
│   └── report_generator.py              # Report generation
│
├── quantum_execution/
│   ├── qiskit_interpreter.py            # QASM parser/interpreter
│   └── simulator.py                     # Quantum simulator wrapper
│
├── statistics_processing/
│   ├── data_processor.py                # Data analysis utilities
│   └── visualization.py                 # Chart generation
│
├── storage/
│   ├── database.py                      # SQLite database manager
│   └── models.py                        # Data models
│
├── utils/
│   └── helpers.py                       # Utility functions
│
├── tests/
│   └── test_system.py                   # Unit tests
│
├── requirements.txt                     # Python dependencies
└── README.md                            # This file
```

## Requirements

- Python 3.10+
- Qiskit 0.43+
- Streamlit 1.28+
- NumPy, SciPy, Pandas
- SQLite (included with Python)

## Installation

### 1. Clone or Navigate to Project Directory

```bash
cd quantum-mutation-testing
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Launch the Web Interface

```bash
streamlit run frontend/app.py
```
or
```bash
python -m streamlit run frontend/app.py
```


The application will open in your browser at `http://localhost:8501`

### 2. Upload a Quantum Circuit

- Navigate to "Upload Circuit" tab
- Choose input method:
  - Paste QASM code directly
  - Upload a QASM file
  - Load example circuits
- Example QASM:
  ```qasm
  OPENQASM 2.0;
  include "qelib1.inc";
  qreg q[2];
  creg c[2];
  h q[0];
  cx q[0],q[1];
  measure q -> c;
  ```

### 3. Configure Parameters

- Navigate to "Configure Parameters"
- Set:
  - Number of shots (100-10000)
  - Number of mutants to generate (1-500)
  - Mutation operators to use
  - Statistical metrics

### 4. Execute Testing

- Navigate to "Execute Testing"
- Click "START MUTATION TESTING"
- System will:
  1. Validate the circuit
  2. Generate mutants
  3. Execute original and mutant circuits
  4. Compare results statistically
  5. Calculate mutation score
  6. Generate visualizations

### 5. View Results

- Navigate to "View Results"
- See:
  - Mutation score gauge
  - Statistics charts
  - State distributions
  - Detailed mutant information

### 6. Download Reports

- Navigate to "Download Reports"
- Export reports in:
  - JSON format (structured data)
  - Text format (human-readable)
  - HTML format (interactive visualization)

## Mutation Operators

The system implements 5+ mutation operators:

### 1. **Gate Replacement**
Replaces a gate with a different gate of the same type.
- Single-qubit: H, X, Y, Z, S, T
- Example: Replace Hadamard (H) with Pauli-X

### 2. **Gate Removal**
Removes a randomly selected gate from the circuit.
- Tests if circuit is resilient to missing operations
- Example: Remove CNOT gate

### 3. **Rotation Angle Change**
Modifies rotation parameters of parameterized gates (RX, RY, RZ).
- Changes angle by random amount in range [-π, π]
- Example: Change RZ(θ) rotation angle

### 4. **Qubit Swap**
Swaps qubits in two-qubit gates.
- Tests gate direction sensitivity
- Example: Change CNOT(q0, q1) to CNOT(q1, q0)

### 5. **Gate Duplication**
Duplicates a gate immediately after its original position.
- Tests redundancy detection
- Example: Duplicate an Hadamard gate

## Statistical Comparison Methods

### 1. **Chi-Square Test**
Tests if distributions are significantly different.
- H₀: Distributions are identical
- p < 0.05: Reject null hypothesis (mutant killed)

### 2. **Kullback-Leibler (KL) Divergence**
Measures asymmetric divergence between distributions.
- KL(P||Q) = Σ P(x) log(P(x)/Q(x))
- Higher value = more different

### 3. **Jensen-Shannon Divergence**
Symmetric divergence measure.
- Range: [0, 1]
- More stable than KL divergence

### 4. **Hellinger Distance**
Geometric distance between distributions.
- Range: [0, 1]
- Always finite

### 5. **Total Variation Distance**
Maximum difference in probabilities.
- TVD = 0.5 * Σ |P(x) - Q(x)|
- Range: [0, 1]

## Mutation Score Interpretation

The mutation score indicates test quality:

| Score Range | Interpretation |
|------------|-----------------|
| 80-100%    | Excellent - Test suite is very effective |
| 60-79%     | Good - Test suite is effective |
| 40-59%     | Fair - Test suite needs improvement |
| 20-39%     | Poor - Test suite is weak |
| 0-19%      | Very Poor - Test suite is inadequate |

## Example Circuits

Included example circuits:

1. **Bell State** - 2-qubit maximally entangled state
2. **GHZ State** - 3-qubit entanglement
3. **Superposition** - Equal superposition of all states
4. **Deutsch Algorithm** - Simple oracle implementation
5. **Grover (2Q)** - 2-qubit Grover's search algorithm
6. **QAOA** - Simplified QAOA circuit

## Running Tests

Run the system test suite:

```bash
python tests/test_system.py
```

Tests included:
- Database operations
- Circuit parsing and validation
- Quantum circuit execution
- Mutation generation
- Statistical comparison
- Configuration management
- Experiment execution

## Database Schema

The system uses SQLite with 6 tables:

### users
- user_id (PK)
- username (UNIQUE)
- email
- created_at (TIMESTAMP)

### circuits
- circuit_id (PK)
- user_id (FK)
- circuit_name
- qasm_code
- num_qubits
- num_gates
- created_at (TIMESTAMP)

### executions
- execution_id (PK)
- circuit_id (FK)
- num_shots
- execution_time
- status
- created_at (TIMESTAMP)

### mutants
- mutant_id (PK)
- circuit_id (FK)
- execution_id (FK)
- mutation_operator
- mutant_qasm
- mutation_details
- created_at (TIMESTAMP)

### results
- result_id (PK)
- execution_id (FK)
- mutant_id (FK)
- output_counts (JSON)
- created_at (TIMESTAMP)

### reports
- report_id (PK)
- execution_id (FK)
- total_mutants
- killed_mutants
- survived_mutants
- mutation_score
- statistical_metric
- metric_value
- report_data (JSON)
- created_at (TIMESTAMP)

## API Usage (Python)

### Using the System Programmatically

```python
from backend.experiment_controller import ExperimentController

# Create controller
controller = ExperimentController()

# Configure parameters
controller.configure_experiment({
    'num_shots': 1000,
    'num_mutants': 20,
    'mutation_operators': ['gate_replacement', 'gate_removal']
})

# Execute experiment
qasm = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0],q[1];
measure q -> c;"""

results = controller.create_experiment(
    circuit_input=qasm,
    circuit_name='my_circuit',
    input_format='qasm'
)

# Access results
print(f"Mutation Score: {results['mutation_score']}%")
print(f"Killed Mutants: {results['killed_mutants']}")

# Export report
controller.export_experiment_report(
    experiment_id=results['execution_id'],
    filepath='report.json',
    format='json'
)
```

## Configuration File

Create `config.json` in the project root:

```json
{
  "num_shots": 1000,
  "num_mutants": 20,
  "mutation_operators": [
    "gate_replacement",
    "gate_removal",
    "rotation_angle_change",
    "qubit_swap",
    "gate_duplication"
  ],
  "statistical_metrics": [
    "chi_square",
    "kl_divergence",
    "js_divergence"
  ],
  "max_circuit_qubits": 20,
  "random_seed": null
}
```

## Performance Considerations

- Each circuit execution uses a simulator (no real quantum hardware)
- Execution time scales with:
  - Number of qubits (exponential in worst case)
  - Number of gates
  - Number of shots
  - Number of mutants

- Typical performance:
  - 2-qubit circuit: ~1-2 seconds per execution
  - 10 mutants × 1000 shots: ~10-20 seconds

## Troubleshooting

### Issue: ImportError for qiskit modules

**Solution:** Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Streamlit app doesn't load

**Solution:** Run from project root and ensure port 8501 is available:
```bash
streamlit run frontend/app.py --server.port 8500
```

### Issue: Circuit parsing error

**Solution:** Ensure QASM syntax is correct:
- Must start with `OPENQASM 2.0;`
- Must include `include "qelib1.inc";`
- Must declare quantum/classical registers
- All statements must end with `;`

### Issue: Memory error with large circuits

**Solution:** Reduce number of qubits or number of shots:
```python
controller.configure_experiment({
    'num_shots': 512,
    'num_mutants': 10
})
```

## Future Enhancements

Potential future features:
- Real quantum hardware backend (IBM Quantum)
- Advanced mutation operators (parameterized circuits)
- Machine learning for mutant prioritization
- Parallel execution of mutants
- Custom mutation operator definitions
- Integration with Jupyter notebooks
- REST API endpoint

## References

### Mutation Testing Concepts
- Offutt & Untch: "Mutation 2000" research paper
- Quantum mutation testing framework extensions

### Quantum Computing Resources
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [IBM Quantum Composer](https://quantum-computing.ibm.com/)

### Statistical Methods
- [SciPy Statistics](https://docs.scipy.org/doc/scipy/reference/stats.html)

## License

This project is provided for educational purposes.

## Authors

- Development Team (2025-26)
- Supervised and verified for SEPM course

## Contact

For questions or issues, please contact the development team.

## Changelog

### Version 1.0.0 (Initial Release)
- Complete mutation testing framework
- 5 mutation operators implemented
- 5 statistical comparison methods
- Full Streamlit UI
- SQLite database
- Report generation
- Comprehensive documentation

---

**Last Updated:** March 2026
**Status:** Production Ready
