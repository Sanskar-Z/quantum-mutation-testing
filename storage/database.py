"""
Storage Layer - Database Module
Handles all database operations and connection management.
"""
import sqlite3
import os
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
import json
from datetime import datetime


class DatabaseManager:
    """Manages SQLite database operations."""
    
    def __init__(self, db_path: str = "quantum_mutation_testing.db"):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database with required tables if they don't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Circuits table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS circuits (
                    circuit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    circuit_name TEXT NOT NULL,
                    qasm_code TEXT NOT NULL,
                    num_qubits INTEGER NOT NULL,
                    num_gates INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Mutants table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mutants (
                    mutant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    circuit_id INTEGER NOT NULL,
                    execution_id INTEGER,
                    mutation_operator TEXT NOT NULL,
                    mutant_qasm TEXT NOT NULL,
                    mutation_details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (circuit_id) REFERENCES circuits (circuit_id),
                    FOREIGN KEY (execution_id) REFERENCES executions (execution_id)
                )
            ''')
            
            # Executions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS executions (
                    execution_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    circuit_id INTEGER NOT NULL,
                    num_shots INTEGER NOT NULL,
                    execution_time REAL,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (circuit_id) REFERENCES circuits (circuit_id)
                )
            ''')
            
            # Results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id INTEGER NOT NULL,
                    mutant_id INTEGER NOT NULL,
                    output_counts TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (execution_id) REFERENCES executions (execution_id),
                    FOREIGN KEY (mutant_id) REFERENCES mutants (mutant_id)
                )
            ''')
            
            # Reports table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reports (
                    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id INTEGER NOT NULL,
                    total_mutants INTEGER,
                    killed_mutants INTEGER,
                    survived_mutants INTEGER,
                    mutation_score REAL,
                    statistical_metric TEXT,
                    metric_value REAL,
                    report_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (execution_id) REFERENCES executions (execution_id)
                )
            ''')
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        
        Yields:
            sqlite3.Connection: Database connection
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = (), fetch_one: bool = False) -> Any:
        """
        Execute a SELECT query.
        
        Args:
            query: SQL query string
            params: Query parameters
            fetch_one: If True, fetch one row; otherwise fetch all
        
        Returns:
            Query results
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall()
    
    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """
        Execute an INSERT query.
        
        Args:
            query: SQL INSERT query string
            params: Query parameters
        
        Returns:
            Last inserted row ID
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Execute an UPDATE query.
        
        Args:
            query: SQL UPDATE query string
            params: Query parameters
        
        Returns:
            Number of affected rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    def execute_delete(self, query: str, params: tuple = ()) -> int:
        """
        Execute a DELETE query.
        
        Args:
            query: SQL DELETE query string
            params: Query parameters
        
        Returns:
            Number of deleted rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    def clear_database(self):
        """Clear all tables in the database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM results')
            cursor.execute('DELETE FROM reports')
            cursor.execute('DELETE FROM mutants')
            cursor.execute('DELETE FROM executions')
            cursor.execute('DELETE FROM circuits')
            cursor.execute('DELETE FROM users')
            conn.commit()
