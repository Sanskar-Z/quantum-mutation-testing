"""
Application Control Layer - Configuration Manager
Manages experiment settings and parameters.
"""
from typing import Dict, Any, List, Tuple
import json
import os


class ConfigurationManager:
    """
    Manages experiment configuration and settings.
    """
    
    # Default configuration
    DEFAULT_CONFIG = {
        'num_shots': 1000,
        'num_mutants': 20,
        'seed': None,
        'mutation_operators': [
            'gate_replacement',
            'gate_removal',
            'rotation_angle_change',
            'qubit_swap',
            'gate_duplication'
        ],
        'statistical_metrics': ['chi_square', 'kl_divergence', 'js_divergence'],
        'max_circuit_qubits': 20,
        'random_seed': None
    }
    
    def __init__(self, config_path: str = None):
        """
        Initialize ConfigurationManager.
        
        Args:
            config_path: Path to configuration file (JSON)
        """
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
    
    def load_config(self, filepath: str):
        """
        Load configuration from JSON file.
        
        Args:
            filepath: Path to configuration file
        """
        try:
            with open(filepath, 'r') as f:
                loaded_config = json.load(f)
                self.config.update(loaded_config)
        except Exception as e:
            raise ValueError(f"Failed to load configuration: {str(e)}")
    
    def save_config(self, filepath: str = None):
        """
        Save configuration to JSON file.
        
        Args:
            filepath: Path to save configuration (uses config_path if not provided)
        """
        filepath = filepath or self.config_path
        if not filepath:
            raise ValueError("No filepath provided for saving configuration")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def set_parameter(self, key: str, value: Any):
        """
        Set a configuration parameter.
        
        Args:
            key: Parameter name
            value: Parameter value
        """
        self.config[key] = value
    
    def get_parameter(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration parameter.
        
        Args:
            key: Parameter name
            default: Default value if not found
        
        Returns:
            Parameter value or default
        """
        return self.config.get(key, default)
    
    def get_all_parameters(self) -> Dict[str, Any]:
        """
        Get all configuration parameters.
        
        Returns:
            Dict: All configuration parameters
        """
        return self.config.copy()
    
    def validate_config(self) -> Tuple[bool, List[str]]:
        """
        Validate current configuration.
        
        Returns:
            Tuple[bool, List[str]]: (is_valid, error_messages)
        """
        errors = []
        
        # Validate num_shots
        if self.config.get('num_shots', 0) < 100:
            errors.append("num_shots must be at least 100")
        
        # Validate num_mutants
        if self.config.get('num_mutants', 0) < 1:
            errors.append("num_mutants must be at least 1")
        
        # Validate mutation operators
        valid_operators = {
            'gate_replacement', 'gate_removal', 'rotation_angle_change',
            'qubit_swap', 'gate_duplication'
        }
        operators = self.config.get('mutation_operators', [])
        invalid_ops = set(operators) - valid_operators
        if invalid_ops:
            errors.append(f"Invalid mutation operators: {invalid_ops}")
        
        # Validate statistical metrics
        valid_metrics = {'chi_square', 'kl_divergence', 'js_divergence', 'hellinger', 'total_variation'}
        metrics = self.config.get('statistical_metrics', [])
        invalid_metrics = set(metrics) - valid_metrics
        if invalid_metrics:
            errors.append(f"Invalid statistical metrics: {invalid_metrics}")
        
        return len(errors) == 0, errors
    
    def reset_to_defaults(self):
        """Reset configuration to default values."""
        self.config = self.DEFAULT_CONFIG.copy()
    
    def __str__(self) -> str:
        """Get string representation of configuration."""
        return json.dumps(self.config, indent=2)
