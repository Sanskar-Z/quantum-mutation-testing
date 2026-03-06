"""
Storage Layer - Models Module
Defines data models for database operations with helper methods.
"""
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from storage.database import DatabaseManager


class DataModel:
    """Base class for all data models."""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize with database manager."""
        self.db = db_manager
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        raise NotImplementedError


class User(DataModel):
    """User model."""
    
    def __init__(self, db_manager: DatabaseManager, user_id: int = None, 
                 username: str = None, email: str = None):
        """
        Initialize User.
        
        Args:
            db_manager: Database manager instance
            user_id: User ID
            username: Username
            email: User email
        """
        super().__init__(db_manager)
        self.user_id = user_id
        self.username = username
        self.email = email
    
    def create(self) -> int:
        """
        Create user in database.
        
        Returns:
            User ID
        """
        query = '''
            INSERT INTO users (username, email) 
            VALUES (?, ?)
        '''
        self.user_id = self.db.execute_insert(query, (self.username, self.email))
        return self.user_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email
        }


class Circuit(DataModel):
    """Quantum Circuit model."""
    
    def __init__(self, db_manager: DatabaseManager, circuit_id: int = None,
                 user_id: int = None, circuit_name: str = None, 
                 qasm_code: str = None, num_qubits: int = 0, num_gates: int = 0):
        """Initialize Circuit."""
        super().__init__(db_manager)
        self.circuit_id = circuit_id
        self.user_id = user_id
        self.circuit_name = circuit_name
        self.qasm_code = qasm_code
        self.num_qubits = num_qubits
        self.num_gates = num_gates
    
    def create(self) -> int:
        """Create circuit in database."""
        query = '''
            INSERT INTO circuits (user_id, circuit_name, qasm_code, num_qubits, num_gates)
            VALUES (?, ?, ?, ?, ?)
        '''
        self.circuit_id = self.db.execute_insert(
            query, 
            (self.user_id, self.circuit_name, self.qasm_code, self.num_qubits, self.num_gates)
        )
        return self.circuit_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'circuit_id': self.circuit_id,
            'user_id': self.user_id,
            'circuit_name': self.circuit_name,
            'qasm_code': self.qasm_code,
            'num_qubits': self.num_qubits,
            'num_gates': self.num_gates
        }


class Mutant(DataModel):
    """Mutant circuit model."""
    
    def __init__(self, db_manager: DatabaseManager, mutant_id: int = None,
                 circuit_id: int = None, execution_id: int = None,
                 mutation_operator: str = None, mutant_qasm: str = None,
                 mutation_details: str = None):
        """Initialize Mutant."""
        super().__init__(db_manager)
        self.mutant_id = mutant_id
        self.circuit_id = circuit_id
        self.execution_id = execution_id
        self.mutation_operator = mutation_operator
        self.mutant_qasm = mutant_qasm
        self.mutation_details = mutation_details
    
    def create(self) -> int:
        """Create mutant in database."""
        query = '''
            INSERT INTO mutants (circuit_id, execution_id, mutation_operator, mutant_qasm, mutation_details)
            VALUES (?, ?, ?, ?, ?)
        '''
        self.mutant_id = self.db.execute_insert(
            query,
            (self.circuit_id, self.execution_id, self.mutation_operator, 
             self.mutant_qasm, self.mutation_details)
        )
        return self.mutant_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'mutant_id': self.mutant_id,
            'circuit_id': self.circuit_id,
            'execution_id': self.execution_id,
            'mutation_operator': self.mutation_operator,
            'mutant_qasm': self.mutant_qasm,
            'mutation_details': self.mutation_details
        }


class Execution(DataModel):
    """Execution model."""
    
    def __init__(self, db_manager: DatabaseManager, execution_id: int = None,
                 circuit_id: int = None, num_shots: int = 1000,
                 execution_time: float = None, status: str = 'pending'):
        """Initialize Execution."""
        super().__init__(db_manager)
        self.execution_id = execution_id
        self.circuit_id = circuit_id
        self.num_shots = num_shots
        self.execution_time = execution_time
        self.status = status
    
    def create(self) -> int:
        """Create execution in database."""
        query = '''
            INSERT INTO executions (circuit_id, num_shots, execution_time, status)
            VALUES (?, ?, ?, ?)
        '''
        self.execution_id = self.db.execute_insert(
            query,
            (self.circuit_id, self.num_shots, self.execution_time, self.status)
        )
        return self.execution_id
    
    def update_status(self, status: str):
        """Update execution status."""
        query = 'UPDATE executions SET status = ? WHERE execution_id = ?'
        self.db.execute_update(query, (status, self.execution_id))
        self.status = status
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'execution_id': self.execution_id,
            'circuit_id': self.circuit_id,
            'num_shots': self.num_shots,
            'execution_time': self.execution_time,
            'status': self.status
        }


class Result(DataModel):
    """Result model."""
    
    def __init__(self, db_manager: DatabaseManager, result_id: int = None,
                 execution_id: int = None, mutant_id: int = None,
                 output_counts: str = None):
        """Initialize Result."""
        super().__init__(db_manager)
        self.result_id = result_id
        self.execution_id = execution_id
        self.mutant_id = mutant_id
        self.output_counts = output_counts
    
    def create(self) -> int:
        """Create result in database."""
        query = '''
            INSERT INTO results (execution_id, mutant_id, output_counts)
            VALUES (?, ?, ?)
        '''
        self.result_id = self.db.execute_insert(
            query,
            (self.execution_id, self.mutant_id, self.output_counts)
        )
        return self.result_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'result_id': self.result_id,
            'execution_id': self.execution_id,
            'mutant_id': self.mutant_id,
            'output_counts': self.output_counts
        }


class Report(DataModel):
    """Report model."""
    
    def __init__(self, db_manager: DatabaseManager, report_id: int = None,
                 execution_id: int = None, total_mutants: int = 0,
                 killed_mutants: int = 0, survived_mutants: int = 0,
                 mutation_score: float = 0.0, statistical_metric: str = None,
                 metric_value: float = None, report_data: str = None):
        """Initialize Report."""
        super().__init__(db_manager)
        self.report_id = report_id
        self.execution_id = execution_id
        self.total_mutants = total_mutants
        self.killed_mutants = killed_mutants
        self.survived_mutants = survived_mutants
        self.mutation_score = mutation_score
        self.statistical_metric = statistical_metric
        self.metric_value = metric_value
        self.report_data = report_data
    
    def create(self) -> int:
        """Create report in database."""
        query = '''
            INSERT INTO reports 
            (execution_id, total_mutants, killed_mutants, survived_mutants, 
             mutation_score, statistical_metric, metric_value, report_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.report_id = self.db.execute_insert(
            query,
            (self.execution_id, self.total_mutants, self.killed_mutants,
             self.survived_mutants, self.mutation_score, self.statistical_metric,
             self.metric_value, self.report_data)
        )
        return self.report_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'report_id': self.report_id,
            'execution_id': self.execution_id,
            'total_mutants': self.total_mutants,
            'killed_mutants': self.killed_mutants,
            'survived_mutants': self.survived_mutants,
            'mutation_score': self.mutation_score,
            'statistical_metric': self.statistical_metric,
            'metric_value': self.metric_value,
            'report_data': self.report_data
        }
