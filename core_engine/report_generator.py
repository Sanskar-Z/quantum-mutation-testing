"""
Core Mutation Testing Engine - Report Generation Module
Generates comprehensive mutation testing reports.
"""
import json
from typing import Dict, List, Any
from datetime import datetime
import os


class ReportGenerationModule:
    """
    Generates comprehensive mutation testing reports.
    """
    
    @staticmethod
    def generate_json_report(execution_id: int, circuit_name: str,
                            total_mutants: int, killed_mutants: int,
                            survived_mutants: int, mutation_score: float,
                            statistical_metric: str, metric_value: float,
                            mutant_details: List[Dict[str, Any]],
                            execution_summary: Dict[str, Any]) -> str:
        """
        Generate a JSON format report.
        
        Args:
            execution_id: Execution ID
            circuit_name: Name of the circuit
            total_mutants: Total mutants generated
            killed_mutants: Mutants that were killed
            survived_mutants: Mutants that survived
            mutation_score: Overall mutation score
            statistical_metric: Primary statistical metric used
            metric_value: Value of the metric
            mutant_details: Details of each mutant
            execution_summary: Execution time and performance summary
        
        Returns:
            str: JSON report string
        """
        report = {
            'metadata': {
                'execution_id': execution_id,
                'circuit_name': circuit_name,
                'timestamp': datetime.now().isoformat(),
                'report_type': 'JSON'
            },
            'summary': {
                'total_mutants': total_mutants,
                'killed_mutants': killed_mutants,
                'survived_mutants': survived_mutants,
                'mutation_score': mutation_score,
                'survival_rate': (survived_mutants / total_mutants * 100) if total_mutants > 0 else 0,
                'primary_metric': statistical_metric,
                'metric_value': metric_value
            },
            'execution': execution_summary,
            'mutant_details': mutant_details
        }
        
        return json.dumps(report, indent=2, default=str)
    
    @staticmethod
    def generate_text_report(circuit_name: str, total_mutants: int,
                            killed_mutants: int, survived_mutants: int,
                            mutation_score: float, statistical_results: Dict[str, Any],
                            mutant_details: List[Dict[str, Any]]) -> str:
        """
        Generate a human-readable text report.
        
        Args:
            circuit_name: Name of the circuit
            total_mutants: Total mutants generated
            killed_mutants: Mutants that were killed
            survived_mutants: Mutants that survived
            mutation_score: Overall mutation score
            statistical_results: Statistical comparison results
            mutant_details: Details of each mutant
        
        Returns:
            str: Text report
        """
        report = []
        report.append("=" * 80)
        report.append("QUANTUM CIRCUIT MUTATION TESTING REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Header
        report.append(f"Circuit Name: {circuit_name}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        report.append("-" * 80)
        report.append("MUTATION TESTING SUMMARY")
        report.append("-" * 80)
        report.append(f"Total Mutants Generated:  {total_mutants}")
        report.append(f"Mutants Killed:           {killed_mutants}")
        report.append(f"Mutants Survived:         {survived_mutants}")
        report.append(f"Mutation Score:           {mutation_score:.2f}%")
        report.append(f"Survival Rate:            {(survived_mutants/total_mutants*100) if total_mutants > 0 else 0:.2f}%")
        report.append("")
        
        # Statistical Analysis
        report.append("-" * 80)
        report.append("STATISTICAL ANALYSIS")
        report.append("-" * 80)
        for metric_name, metric_value in statistical_results.items():
            if isinstance(metric_value, dict):
                report.append(f"\n{metric_name}:")
                for k, v in metric_value.items():
                    if isinstance(v, float):
                        report.append(f"  {k}: {v:.6f}")
                    else:
                        report.append(f"  {k}: {v}")
            else:
                if isinstance(metric_value, float):
                    report.append(f"{metric_name}: {metric_value:.6f}")
                else:
                    report.append(f"{metric_name}: {metric_value}")
        report.append("")
        
        # Score Interpretation
        report.append("-" * 80)
        report.append("SCORE INTERPRETATION")
        report.append("-" * 80)
        interpretation = ReportGenerationModule._interpret_score(mutation_score)
        report.append(interpretation)
        report.append("")
        
        # Detailed Mutant Information
        report.append("-" * 80)
        report.append("DETAILED MUTANT INFORMATION")
        report.append("-" * 80)
        
        for i, detail in enumerate(mutant_details, 1):
            report.append(f"\nMutant #{i}")
            report.append(f"  Operator: {detail.get('operator', 'N/A')}")
            report.append(f"  Details: {detail.get('details', 'N/A')}")
        
        report.append("\n" + "=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    @staticmethod
    def generate_html_report(circuit_name: str, total_mutants: int,
                            killed_mutants: int, survived_mutants: int,
                            mutation_score: float, chart_data: Dict[str, Any]) -> str:
        """
        Generate an HTML format report.
        
        Args:
            circuit_name: Name of the circuit
            total_mutants: Total mutants generated
            killed_mutants: Mutants that were killed
            survived_mutants: Mutants that survived
            mutation_score: Overall mutation score
            chart_data: Data for charts and visualizations
        
        Returns:
            str: HTML report
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Mutation Testing Report - {circuit_name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    background-color: white;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #333;
                    text-align: center;
                    border-bottom: 3px solid #007bff;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #007bff;
                    margin-top: 20px;
                }}
                .summary-box {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .metric {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 5px;
                    text-align: center;
                }}
                .metric.good {{
                    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                }}
                .metric.warning {{
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                }}
                .metric-value {{
                    font-size: 32px;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .metric-label {{
                    font-size: 14px;
                    opacity: 0.9;
                }}
                .score-gauge {{
                    width: 100px;
                    height: 100px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 20px auto;
                    font-size: 24px;
                    font-weight: bold;
                    color: white;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #007bff;
                    color: white;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Mutation Testing Report</h1>
                <p><strong>Circuit:</strong> {circuit_name}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <h2>Summary</h2>
                <div class="summary-box">
                    <div class="metric good">
                        <div class="metric-label">Mutation Score</div>
                        <div class="metric-value">{mutation_score:.1f}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Total Mutants</div>
                        <div class="metric-value">{total_mutants}</div>
                    </div>
                    <div class="metric good">
                        <div class="metric-label">Killed Mutants</div>
                        <div class="metric-value">{killed_mutants}</div>
                    </div>
                    <div class="metric warning">
                        <div class="metric-label">Survived Mutants</div>
                        <div class="metric-value">{survived_mutants}</div>
                    </div>
                </div>
                
                <h2>Score Assessment</h2>
                <div class="score-gauge\" style=\"background: {'#11998e' if mutation_score >= 80 else '#f5576c'}\">
                    {mutation_score:.1f}%
                </div>
                <p style="text-align: center;">
                    <strong>{ReportGenerationModule._interpret_score(mutation_score)}</strong>
                </p>
                
            </div>
        </body>
        </html>
        """
        return html
    
    @staticmethod
    def save_report(report_content: str, filepath: str, report_format: str = 'json'):
        """
        Save report to file.
        
        Args:
            report_content: Report content string
            filepath: File path to save
            report_format: Report format (json, txt, html)
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write(report_content)
    
    @staticmethod
    def _interpret_score(mutation_score: float) -> str:
        """Interpret mutation score quality."""
        if mutation_score >= 80:
            return "Excellent ✓ - Test suite is very effective"
        elif mutation_score >= 60:
            return "Good ✓ - Test suite is effective"
        elif mutation_score >= 40:
            return "Fair ⚠ - Test suite needs improvement"
        elif mutation_score >= 20:
            return "Poor ✗ - Test suite is weak"
        else:
            return "Very Poor ✗ - Test suite is inadequate"
