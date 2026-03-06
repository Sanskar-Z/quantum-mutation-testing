"""
Application Control Layer - Experiment Controller
Orchestrates mutation testing experiments.
"""
from typing import Dict, List, Any, Optional, Tuple
from qiskit import QuantumCircuit
import time

from backend.configuration_manager import ConfigurationManager
from backend.workflow_manager import WorkflowManager
from storage.database import DatabaseManager
from quantum_execution.qiskit_interpreter import QiskitCircuitInterpreter


class ExperimentController:
    """
    Controls and orchestrates mutation testing experiments.
    """
    
    def __init__(self, db_manager: DatabaseManager = None):
        """
        Initialize ExperimentController.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager or DatabaseManager()
        self.config_manager = ConfigurationManager()
        self.workflow_manager = WorkflowManager(self.db)
        self.circuit_interpreter = QiskitCircuitInterpreter()
        
        self.experiments = {}
        self.current_experiment_id = 0
    
    def create_experiment(self, circuit_input: str, circuit_name: str,
                         input_format: str = 'qasm', num_mutants: int = None,
                         num_shots: int = None, mutation_operators: List[str] = None,
                         user_id: int = 1) -> Dict[str, Any]:
        """
        Create and execute a new experiment.
        
        Args:
            circuit_input: Quantum circuit code (QASM or dict)
            circuit_name: Name of the circuit
            input_format: Input format ('qasm', 'dict')
            num_mutants: Number of mutants (uses config default if None)
            num_shots: Number of shots (uses config default if None)
            mutation_operators: Mutation operators (uses config default if None)
            user_id: User ID
        
        Returns:
            Dict: Experiment results
        """
        try:
            # Parse circuit input
            if input_format == 'qasm':
                circuit = self.circuit_interpreter.from_qasm_string(circuit_input)
            elif input_format == 'dict':
                circuit = self.circuit_interpreter.from_dict(circuit_input)
            else:
                return {
                    'success': False,
                    'error': f"Unsupported input format: {input_format}"
                }
            
            # Get configuration parameters
            num_mutants = num_mutants or self.config_manager.get_parameter('num_mutants', 20)
            num_shots = num_shots or self.config_manager.get_parameter('num_shots', 1000)
            mutation_operators = mutation_operators or self.config_manager.get_parameter('mutation_operators')
            seed = self.config_manager.get_parameter('random_seed')
            
            # Execute workflow
            results = self.workflow_manager.execute_workflow(
                circuit=circuit,
                circuit_name=circuit_name,
                num_mutants=num_mutants,
                num_shots=num_shots,
                mutation_operators=mutation_operators,
                seed=seed,
                user_id=user_id
            )
            
            if results['success']:
                # Store experiment
                self.current_experiment_id += 1
                self.experiments[self.current_experiment_id] = {
                    'id': self.current_experiment_id,
                    'circuit_name': circuit_name,
                    'timestamp': time.time(),
                    'user_id': user_id,
                    'results': results
                }
            
            return results
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_experiment_results(self, experiment_id: int) -> Optional[Dict[str, Any]]:
        """
        Get results of a specific experiment.
        
        Args:
            experiment_id: Experiment ID
        
        Returns:
            Dict: Experiment results or None
        """
        if experiment_id in self.experiments:
            return self.experiments[experiment_id]['results']
        return None
    
    def list_experiments(self) -> List[Dict[str, Any]]:
        """
        Get list of all experiments.
        
        Returns:
            List: List of experiment metadata
        """
        experiments_list = []
        for exp_id, exp_data in self.experiments.items():
            experiments_list.append({
                'id': exp_id,
                'circuit_name': exp_data['circuit_name'],
                'timestamp': exp_data['timestamp'],
                'user_id': exp_data['user_id'],
                'mutation_score': exp_data['results'].get('mutation_score', 0)
            })
        return experiments_list
    
    def configure_experiment(self, config_dict: Dict[str, Any]):
        """
        Configure experiment parameters.
        
        Args:
            config_dict: Configuration dictionary
        """
        for key, value in config_dict.items():
            self.config_manager.set_parameter(key, value)
    
    def get_configuration(self) -> Dict[str, Any]:
        """
        Get current configuration.
        
        Returns:
            Dict: Current configuration
        """
        return self.config_manager.get_all_parameters()
    
    def validate_configuration(self) -> Tuple[bool, List[str]]:
        """
        Validate current configuration.
        
        Returns:
            Tuple[bool, List[str]]: (is_valid, error_messages)
        """
        return self.config_manager.validate_config()
    
    def create_example_circuit(self) -> str:
        """
        Create an example quantum circuit in QASM format.
        
        Returns:
            str: Example circuit QASM
        """
        return """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q -> c;"""
    
    def import_circuit(self, filepath: str) -> str:
        """
        Import circuit from file.
        
        Args:
            filepath: Path to circuit file
        
        Returns:
            str: Circuit content
        """
        with open(filepath, 'r') as f:
            return f.read()
    
    def export_experiment_report(self, experiment_id: int, filepath: str,
                                format: str = 'json'):
        """
        Export experiment report to file.
        
        Args:
            experiment_id: Experiment ID
            filepath: File path to save
            format: Report format (json, txt, html)
        """
        results = self.get_experiment_results(experiment_id)
        if not results:
            raise ValueError(f"Experiment {experiment_id} not found")
        
        if format == 'json':
            report = results['json_report']
        elif format == 'txt':
            report = self.workflow_manager.report_generator.generate_text_report(
                results['circuit_name'],
                results['total_mutants'],
                results['killed_mutants'],
                results['survived_mutants'],
                results['mutation_score'],
                {},
                results['mutant_details']
            )
        elif format == 'html':
            report = self.workflow_manager.report_generator.generate_html_report(
                results['circuit_name'],
                results['total_mutants'],
                results['killed_mutants'],
                results['survived_mutants'],
                results['mutation_score'],
                {}
            )
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        self.workflow_manager.report_generator.save_report(report, filepath, format)
