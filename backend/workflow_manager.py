"""
Application Control Layer - Workflow Manager
Manages the complete mutation testing workflow pipeline.
"""
import time
from typing import Dict, List, Tuple, Any
from qiskit import QuantumCircuit

from core_engine.circuit_validation import CircuitValidationModule
from core_engine.mutation_generator import MutationGenerationModule
from core_engine.execution_module import ExecutionModule
from core_engine.statistical_comparison import StatisticalComparisonModule
from core_engine.mutation_score_calculator import MutationScoreCalculator
from core_engine.report_generator import ReportGenerationModule
from storage.database import DatabaseManager
from storage.models import Execution, Mutant, Result, Report
from statistics_processing.data_processor import DataProcessor
from statistics_processing.visualization import VisualizationModule


class WorkflowManager:
    """
    Manages the complete mutation testing workflow pipeline:
    validate → mutate → execute → compare → score → report
    """
    
    def __init__(self, db_manager: DatabaseManager = None):
        """
        Initialize WorkflowManager.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager or DatabaseManager()
        self.validation_module = CircuitValidationModule()
        self.mutation_generator = None
        self.execution_module = None
        self.comparison_module = StatisticalComparisonModule()
        self.score_calculator = MutationScoreCalculator()
        self.report_generator = ReportGenerationModule()
        self.data_processor = DataProcessor()
        self.visualization_module = VisualizationModule()
        
        self.workflow_state = {}
    
    def execute_workflow(self, circuit: QuantumCircuit, circuit_name: str,
                        num_mutants: int = 20, num_shots: int = 1000,
                        mutation_operators: List[str] = None,
                        seed: int = None, user_id: int = 1) -> Dict[str, Any]:
        """
        Execute complete mutation testing workflow.
        
        Args:
            circuit: QuantumCircuit to test
            circuit_name: Name of the circuit
            num_mutants: Number of mutants to generate
            num_shots: Number of quantum shots
            mutation_operators: List of mutation operators to use
            seed: Random seed
            user_id: User ID for database storage
        
        Returns:
            Dict: Complete workflow results
        """
        workflow_start_time = time.time()
        
        try:
            # Step 1: Validate
            print("Step 1: Validating circuit...")
            is_valid, validation_errors = self.validation_module.validate_circuit(circuit)
            if not is_valid:
                return {
                    'success': False,
                    'error': f"Circuit validation failed: {validation_errors}",
                    'step': 'validation'
                }
            
            self.workflow_state['validation_passed'] = True
            
            # Step 2: Mutate
            print("Step 2: Generating mutants...")
            self.mutation_generator = MutationGenerationModule(seed=seed)
            mutants = self.mutation_generator.generate_mutants(
                circuit, num_mutants, mutation_operators
            )
            
            self.workflow_state['num_mutants_generated'] = len(mutants)
            
            # Step 3: Execute
            print("Step 3: Executing circuits...")
            self.execution_module = ExecutionModule(num_shots=num_shots, seed=seed)
            
            # Execute original circuit
            original_result = self.execution_module.execute_original_circuit(circuit)
            original_counts = original_result['counts']
            
            # Execute mutants
            mutant_results = self.execution_module.execute_mutant_batch(mutants)
            
            # Step 4: Compare
            print("Step 4: Comparing results...")
            comparison_results = []
            for mutant_result in mutant_results:
                mutant_counts = mutant_result['counts']
                comp = self.comparison_module.compare_distributions(
                    original_counts, mutant_counts
                )
                mutant_result['comparison'] = comp
                comparison_results.append(comp)
            
            # Step 5: Score
            print("Step 5: Calculating mutation score...")
            # Determine killed mutants based on statistical significance
            killed_mutants = 0
            for mutant_result in mutant_results:
                comp = mutant_result['comparison']
                if 'chi_square' in comp and comp['chi_square']['is_significantly_different']:
                    killed_mutants += 1
                    mutant_result['is_killed'] = True
                else:
                    mutant_result['is_killed'] = False
            
            survived_mutants = len(mutants) - killed_mutants
            mutation_score = self.score_calculator.calculate_mutation_score(
                len(mutants), killed_mutants
            )
            
            # Get primary metric value
            primary_metric = 'js_divergence'
            if comparison_results:
                primary_metric_value = comparison_results[0].get(primary_metric, 0)
            else:
                primary_metric_value = 0
            
            # Step 6: Report
            print("Step 6: Generating report...")
            
            # Prepare mutant details for report
            mutant_details = []
            for i, (mutant, operator, details) in enumerate(mutants):
                mutant_details.append({
                    'index': i,
                    'operator': operator,
                    'details': str(details),
                    'is_killed': mutant_results[i].get('is_killed', False)
                })
            
            # Generate reports
            execution_summary = self.execution_module.get_execution_summary()
            
            json_report = self.report_generator.generate_json_report(
                execution_id=1,
                circuit_name=circuit_name,
                total_mutants=len(mutants),
                killed_mutants=killed_mutants,
                survived_mutants=survived_mutants,
                mutation_score=mutation_score,
                statistical_metric=primary_metric,
                metric_value=primary_metric_value,
                mutant_details=mutant_details,
                execution_summary=execution_summary
            )
            
            # Generate visualizations
            print("Step 7: Generating visualizations...")
            gauge_chart = self.visualization_module.plot_mutation_score_gauge(mutation_score)
            stats_chart = self.visualization_module.plot_mutation_stats(
                len(mutants), killed_mutants, survived_mutants
            )
            original_dist_chart = self.visualization_module.plot_count_distribution(
                original_counts, title='Original Circuit State Distribution'
            )
            
            workflow_end_time = time.time()
            total_workflow_time = workflow_end_time - workflow_start_time
            
            # Compile final results
            return {
                'success': True,
                'circuit_name': circuit_name,
                'total_mutants': len(mutants),
                'killed_mutants': killed_mutants,
                'survived_mutants': survived_mutants,
                'mutation_score': mutation_score,
                'survival_rate': self.score_calculator.calculate_survival_rate(
                    len(mutants), killed_mutants
                ),
                'primary_metric': primary_metric,
                'metric_value': primary_metric_value,
                'execution_summary': execution_summary,
                'total_workflow_time': total_workflow_time,
                'json_report': json_report,
                'gauge_chart': gauge_chart,
                'stats_chart': stats_chart,
                'original_dist_chart': original_dist_chart,
                'mutant_details': mutant_details,
                'original_counts': original_counts
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'step': 'execution'
            }
    
    def get_workflow_state(self) -> Dict[str, Any]:
        """
        Get current workflow state.
        
        Returns:
            Dict: Current workflow state
        """
        return self.workflow_state.copy()
    
    def save_workflow_results(self, results: Dict[str, Any], filepath: str):
        """
        Save workflow results to database and files.
        
        Args:
            results: Workflow results
            filepath: Base filepath for saving reports
        """
        if not results.get('success', False):
            return
        
        # Save JSON report
        if filepath:
            json_path = f"{filepath}_report.json"
            self.report_generator.save_report(
                results['json_report'], json_path, 'json'
            )
