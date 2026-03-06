"""
Utilities Module
Helper functions and utilities for the mutation testing system.
"""
import json
import os
from typing import Dict, List, Any, Tuple
from datetime import datetime


class CircuitExamples:
    """Provides example quantum circuits."""
    
    @staticmethod
    def get_bell_state() -> str:
        """Get Bell state circuit (maximally entangled)."""
        return """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q -> c;"""
    
    @staticmethod
    def get_ghz_state() -> str:
        """Get GHZ state circuit (3-qubit entanglement)."""
        return """OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[3];
h q[0];
cx q[0],q[1];
cx q[0],q[2];
measure q -> c;"""
    
    @staticmethod
    def get_superposition() -> str:
        """Get superposition circuit."""
        return """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
h q[1];
measure q -> c;"""
    
    @staticmethod
    def get_deutsch_algorithm() -> str:
        """Get Deutsch algorithm circuit."""
        return """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
x q[1];
h q[1];
cx q[0],q[1];
h q[0];
measure q[0] -> c[0];
measure q[1] -> c[1];"""
    
    @staticmethod
    def get_grover_2qubits() -> str:
        """Get Grover's algorithm circuit (2 qubits)."""
        return """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
h q[1];
z q[0];
cz q[0],q[1];
z q[1];
h q[0];
h q[1];
measure q -> c;"""
    
    @staticmethod
    def get_qaoa_example() -> str:
        """Get simple QAOA-like circuit."""
        return """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
rx(1.57) q[0];
rx(1.57) q[1];
cz q[0],q[1];
rx(0.785) q[0];
rx(0.785) q[1];
measure q -> c;"""


class FileUtils:
    """File handling utilities."""
    
    @staticmethod
    def ensure_directory(dirpath: str):
        """Ensure directory exists."""
        os.makedirs(dirpath, exist_ok=True)
    
    @staticmethod
    def save_json(data: Dict[str, Any], filepath: str):
        """Save data to JSON file."""
        FileUtils.ensure_directory(os.path.dirname(filepath))
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        """Load data from JSON file."""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_text(content: str, filepath: str):
        """Save text to file."""
        FileUtils.ensure_directory(os.path.dirname(filepath))
        with open(filepath, 'w') as f:
            f.write(content)
    
    @staticmethod
    def load_text(filepath: str) -> str:
        """Load text from file."""
        with open(filepath, 'r') as f:
            return f.read()


class Logger:
    """Simple logging utility."""
    
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    
    LOG_LEVEL = INFO
    
    @staticmethod
    def debug(message: str):
        """Log debug message."""
        if Logger.LOG_LEVEL <= Logger.DEBUG:
            print(f"[DEBUG] {datetime.now().isoformat()} - {message}")
    
    @staticmethod
    def info(message: str):
        """Log info message."""
        if Logger.LOG_LEVEL <= Logger.INFO:
            print(f"[INFO] {datetime.now().isoformat()} - {message}")
    
    @staticmethod
    def warning(message: str):
        """Log warning message."""
        if Logger.LOG_LEVEL <= Logger.WARNING:
            print(f"[WARNING] {datetime.now().isoformat()} - {message}")
    
    @staticmethod
    def error(message: str):
        """Log error message."""
        if Logger.LOG_LEVEL <= Logger.ERROR:
            print(f"[ERROR] {datetime.now().isoformat()} - {message}")
    
    @staticmethod
    def set_level(level: int):
        """Set logging level."""
        Logger.LOG_LEVEL = level


class ValidationUtils:
    """Validation utilities."""
    
    @staticmethod
    def validate_positive_integer(value: Any, name: str = "value") -> Tuple[bool, str]:
        """Validate positive integer."""
        try:
            val = int(value)
            if val > 0:
                return True, ""
            else:
                return False, f"{name} must be positive"
        except:
            return False, f"{name} must be an integer"
    
    @staticmethod
    def validate_range(value: Any, min_val: int, max_val: int, 
                      name: str = "value") -> Tuple[bool, str]:
        """Validate value in range."""
        try:
            val = int(value)
            if min_val <= val <= max_val:
                return True, ""
            else:
                return False, f"{name} must be between {min_val} and {max_val}"
        except:
            return False, f"{name} must be a number"
    
    @staticmethod
    def validate_non_empty_string(value: Any, name: str = "value") -> Tuple[bool, str]:
        """Validate non-empty string."""
        if isinstance(value, str) and value.strip():
            return True, ""
        else:
            return False, f"{name} must be a non-empty string"
