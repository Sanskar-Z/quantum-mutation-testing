"""
User Interface Layer - Streamlit Frontend Application
Main dashboard for Quantum Circuit Mutation Testing System.
"""
import streamlit as st
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.experiment_controller import ExperimentController
from backend.configuration_manager import ConfigurationManager
from utils.helpers import CircuitExamples, FileUtils, Logger, ValidationUtils
from quantum_execution.qiskit_interpreter import QiskitCircuitInterpreter


# Page configuration
st.set_page_config(
    page_title="Quantum Mutation Testing System",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if 'controller' not in st.session_state:
    st.session_state.controller = ExperimentController()

if 'config_manager' not in st.session_state:
    st.session_state.config_manager = ConfigurationManager()

if 'circuit_interpreter' not in st.session_state:
    st.session_state.circuit_interpreter = QiskitCircuitInterpreter()

if 'current_results' not in st.session_state:
    st.session_state.current_results = None


# Main header
st.title("⚛️ Quantum Circuit Mutation Testing System")
st.markdown("**Automated Test Generation and Bug Detection for Quantum Circuits**")
st.divider()


# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Home", "Upload Circuit", "Configure Parameters", "Execute Testing", 
     "View Results", "Download Reports", "Settings"]
)

st.sidebar.divider()
st.sidebar.markdown("### Project Info")
st.sidebar.markdown("""
- **Framework**: Qiskit + Streamlit
- **Database**: SQLite
- **Statistics**: SciPy, NumPy, Pandas
- **Visualization**: Matplotlib
""")


# Page: Home
if page == "Home":
    st.header("Welcome to Quantum Circuit Mutation Testing System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### About This System
        
        This system provides automated mutation testing for quantum circuits:
        
        ✓ **Upload** quantum circuits in QASM format
        ✓ **Configure** mutation parameters and settings
        ✓ **Generate** mutant circuits automatically
        ✓ **Execute** on quantum simulators
        ✓ **Compare** results statistically
        ✓ **Calculate** mutation scores
        ✓ **Generate** detailed reports and visualizations
        
        ### Key Features
        
        - 5+ mutation operators
        - Statistical comparison (Chi-Square, KL Divergence)
        - Mutation scoring and analysis
        - Interactive visualizations
        - Report generation (JSON, HTML, TXT)
        """)
    
    with col2:
        st.markdown("""
        ### How It Works
        
        1. **Validation**: Validates circuit syntax and structure
        2. **Mutation**: Generates mutant circuits using various operators
        3. **Execution**: Executes both original and mutant circuits
        4. **Comparison**: Compares results using statistical tests
        5. **Scoring**: Calculates mutation score
        6. **Reporting**: Generates comprehensive reports
        
        ### Example Circuits
        """)
        
        if st.button("Load Bell State Example"):
            st.session_state.circuit_input = CircuitExamples.get_bell_state()
            st.success("Bell state circuit loaded!")
    
    st.divider()
    st.markdown("### Quick Start")
    st.markdown("""
    1. Go to **Upload Circuit** to enter your quantum circuit
    2. Configure mutation parameters in **Configure Parameters**
    3. Execute testing in **Execute Testing**
    4. View results in **View Results**
    5. Download reports in **Download Reports**
    """)


# Page: Upload Circuit
elif page == "Upload Circuit":
    st.header("📤 Upload or Input Quantum Circuit")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        input_method = st.radio("Choose Input Method", ["Paste QASM Code", "Upload File", "Load Example"])
        
        if input_method == "Paste QASM Code":
            circuit_input = st.text_area(
                "Enter QASM Code",
                value=st.session_state.get('circuit_input', ''),
                height=300,
                placeholder="OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[2];\ncreg c[2];\nh q[0];\ncx q[0],q[1];\nmeasure q -> c;"
            )
            st.session_state.circuit_input = circuit_input
        
        elif input_method == "Upload File":
            uploaded_file = st.file_uploader("Choose QASM file", type=['qasm', 'txt'])
            if uploaded_file is not None:
                circuit_input = uploaded_file.read().decode('utf-8')
                st.session_state.circuit_input = circuit_input
                st.success("File uploaded successfully!")
        
        else:  # Load Example
            example = st.selectbox(
                "Select Example Circuit",
                ["Bell State", "GHZ State", "Superposition", "Deutsch Algorithm", 
                 "Grover (2Q)", "QAOA"]
            )
            
            examples = {
                "Bell State": CircuitExamples.get_bell_state,
                "GHZ State": CircuitExamples.get_ghz_state,
                "Superposition": CircuitExamples.get_superposition,
                "Deutsch Algorithm": CircuitExamples.get_deutsch_algorithm,
                "Grover (2Q)": CircuitExamples.get_grover_2qubits,
                "QAOA": CircuitExamples.get_qaoa_example
            }
            
            circuit_input = examples[example]()
            st.session_state.circuit_input = circuit_input
            
            if st.button(f"Load {example}"):
                st.success(f"{example} circuit loaded!")
    
    with col2:
        st.markdown("### Circuit Info")
        if st.session_state.get('circuit_input'):
            try:
                circuit = st.session_state.circuit_interpreter.from_qasm_string(
                    st.session_state.circuit_input
                )
                info = st.session_state.circuit_interpreter.get_circuit_info(circuit)
                
                st.metric("Qubits", info['num_qubits'])
                st.metric("Gates", info['num_gates'])
                st.metric("Depth", info['depth'])
                
                # Validation
                is_valid, msg = st.session_state.circuit_interpreter.validate_circuit(circuit)
                if is_valid:
                    st.success("✓ Valid Circuit")
                else:
                    st.error(f"✗ Invalid: {msg}")
            
            except Exception as e:
                st.error(f"Error parsing circuit: {str(e)}")
    
    st.divider()
    
    # Circuit naming
    circuit_name = st.text_input("Circuit Name", value="my_circuit")
    
    if st.button("✓ Confirm Circuit", key="confirm_circuit"):
        if st.session_state.get('circuit_input'):
            st.session_state.circuit_name = circuit_name
            st.success(f"Circuit '{circuit_name}' confirmed and ready for testing!")
        else:
            st.error("Please enter a circuit first!")


# Page: Configure Parameters
elif page == "Configure Parameters":
    st.header("⚙️ Configure Mutation Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Execution Settings")
        
        num_shots = st.number_input(
            "Number of Shots",
            min_value=100,
            max_value=10000,
            value=st.session_state.config_manager.get_parameter('num_shots', 1000),
            step=100,
            help="Number of times to execute each circuit"
        )
        st.session_state.config_manager.set_parameter('num_shots', num_shots)
        
        num_mutants = st.number_input(
            "Number of Mutants to Generate",
            min_value=1,
            max_value=500,
            value=st.session_state.config_manager.get_parameter('num_mutants', 20),
            step=5,
            help="How many mutant circuits to generate"
        )
        st.session_state.config_manager.set_parameter('num_mutants', num_mutants)
        
        use_seed = st.checkbox("Use Random Seed")
        if use_seed:
            seed = st.number_input("Random Seed", value=42)
            st.session_state.config_manager.set_parameter('random_seed', seed)
        else:
            st.session_state.config_manager.set_parameter('random_seed', None)
    
    with col2:
        st.markdown("### Mutation Operators")
        
        available_operators = [
            'gate_replacement',
            'gate_removal',
            'rotation_angle_change',
            'qubit_swap',
            'gate_duplication'
        ]
        
        selected_operators = st.multiselect(
            "Select Mutation Operators",
            available_operators,
            default=st.session_state.config_manager.get_parameter('mutation_operators'),
            help="Choose which mutation operators to apply"
        )
        st.session_state.config_manager.set_parameter('mutation_operators', selected_operators)
        
        st.markdown("**Operator Descriptions:**")
        st.markdown("""
        - **Gate Replacement**: Replace gates with different gates
        - **Gate Removal**: Remove gates from circuit
        - **Rotation Angle Change**: Modify rotation parameters
        - **Qubit Swap**: Swap qubits in two-qubit gates
        - **Gate Duplication**: Duplicate gates
        """)
    
    st.divider()
    st.markdown("### Statistical Metrics")
    
    available_metrics = [
        'chi_square',
        'kl_divergence',
        'js_divergence',
        'hellinger',
        'total_variation'
    ]
    
    selected_metrics = st.multiselect(
        "Select Statistical Metrics",
        available_metrics,
        default=st.session_state.config_manager.get_parameter('statistical_metrics', ['chi_square', 'kl_divergence']),
        help="Choose metrics for comparing distributions"
    )
    st.session_state.config_manager.set_parameter('statistical_metrics', selected_metrics)
    
    st.divider()
    
    # Configuration validation and display
    is_valid, errors = st.session_state.config_manager.validate_config()
    
    if is_valid:
        st.success("✓ Configuration is valid!")
    else:
        st.warning("⚠️ Configuration issues:")
        for error in errors:
            st.warning(f"- {error}")
    
    # Current configuration display
    with st.expander("View Current Configuration"):
        st.json(st.session_state.config_manager.get_all_parameters())


# Page: Execute Testing
elif page == "Execute Testing":
    st.header("🚀 Execute Mutation Testing")
    
    if not st.session_state.get('circuit_input'):
        st.error("⚠️ Please upload a circuit first!")
        st.stop()
    
    st.markdown(f"### Testing Circuit: {st.session_state.get('circuit_name', 'Unnamed')}")
    
    # Test parameters recap
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Shots", st.session_state.config_manager.get_parameter('num_shots'))
    with col2:
        st.metric("Mutants", st.session_state.config_manager.get_parameter('num_mutants'))
    with col3:
        operators = st.session_state.config_manager.get_parameter('mutation_operators')
        st.metric("Operators", len(operators))
    with col4:
        metrics = st.session_state.config_manager.get_parameter('statistical_metrics')
        st.metric("Metrics", len(metrics))
    
    st.divider()
    
    if st.button("▶️ START MUTATION TESTING", key="start_testing"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("Step 1/6: Validating circuit...")
            progress_bar.progress(15)
            
            status_text.text("Step 2/6: Generating mutants...")
            progress_bar.progress(30)
            
            status_text.text("Step 3/6: Executing circuits...")
            progress_bar.progress(50)
            
            status_text.text("Step 4/6: Comparing results...")
            progress_bar.progress(65)
            
            status_text.text("Step 5/6: Calculating scores...")
            progress_bar.progress(80)
            
            status_text.text("Step 6/6: Generating report...")
            
            # Execute the actual testing
            results = st.session_state.controller.create_experiment(
                circuit_input=st.session_state.circuit_input,
                circuit_name=st.session_state.get('circuit_name', 'test_circuit'),
                input_format='qasm',
                num_mutants=st.session_state.config_manager.get_parameter('num_mutants'),
                num_shots=st.session_state.config_manager.get_parameter('num_shots'),
                mutation_operators=st.session_state.config_manager.get_parameter('mutation_operators'),
                user_id=1
            )
            
            progress_bar.progress(100)
            status_text.text("✓ Testing Complete!")
            
            if results['success']:
                st.session_state.current_results = results
                st.success("✓ Mutation testing completed successfully!")
                
                # Display key metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Mutants", results['total_mutants'])
                with col2:
                    st.metric("Killed Mutants", results['killed_mutants'], delta=f"+{results['killed_mutants']}")
                with col3:
                    st.metric("Mutation Score", f"{results['mutation_score']:.2f}%")
                with col4:
                    st.metric("Execution Time", f"{results['total_workflow_time']:.2f}s")
            else:
                st.error(f"Testing failed: {results.get('error', 'Unknown error')}")
        
        except Exception as e:
            progress_bar.progress(0)
            status_text.empty()
            st.error(f"Error during testing: {str(e)}")


# Page: View Results
elif page == "View Results":
    st.header("📊 View Mutation Testing Results")
    
    if not st.session_state.get('current_results'):
        st.info("ℹ️ No results available. Please execute testing first!")
        st.stop()
    
    results = st.session_state.current_results
    
    # Results summary
    st.markdown("### Mutation Testing Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Mutants", results['total_mutants'])
    with col2:
        st.metric("Killed Mutants", results['killed_mutants'])
    with col3:
        st.metric("Survived Mutants", results['survived_mutants'])
    with col4:
        score_color = "🟢" if results['mutation_score'] >= 80 else "🟡" if results['mutation_score'] >= 60 else "🔴"
        st.metric("Mutation Score", f"{result['mutation_score']:.2f}%", f" {score_color}")
    
    st.divider()
    
    # Visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Score", "Statistics", "Distribution", "Details"])
    
    with tab1:
        st.markdown("### Mutation Score Gauge")
        try:
            if results.get('gauge_chart'):
                from PIL import Image
                import io
                import base64
                
                img = Image.open(io.BytesIO(base64.b64decode(results['gauge_chart'].split(',')[1])))
                st.image(img)
        except:
            st.info("Gauge chart not available")
    
    with tab2:
        st.markdown("### Mutation Statistics")
        try:
            if results.get('stats_chart'):
                from PIL import Image
                import io
                import base64
                
                img = Image.open(io.BytesIO(base64.b64decode(results['stats_chart'].split(',')[1])))
                st.image(img)
        except:
            st.info("Statistics chart not available")
    
    with tab3:
        st.markdown("### State Distribution")
        try:
            if results.get('original_dist_chart'):
                from PIL import Image
                import io
                import base64
                
                img = Image.open(io.BytesIO(base64.b64decode(results['original_dist_chart'].split(',')[1])))
                st.image(img)
        except:
            st.info("Distribution chart not available")
    
    with tab4:
        st.markdown("### Mutant Details")
        if results.get('mutant_details'):
            df_data = []
            for detail in results['mutant_details']:
                df_data.append({
                    'Index': detail['index'],
                    'Operator': detail['operator'],
                    'Killed': '✓' if detail.get('is_killed') else '✗'
                })
            
            st.dataframe(df_data, use_container_width=True)


# Page: Download Reports
elif page == "Download Reports":
    st.header("📥 Download Reports")
    
    if not st.session_state.get('current_results'):
        st.info("ℹ️ No results available. Please execute testing first!")
        st.stop()
    
    results = st.session_state.current_results
    
    st.markdown("### Download Mutation Testing Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 JSON Report"):
            json_report = results['json_report']
            st.download_button(
                label="Download JSON",
                data=json_report,
                file_name=f"mutation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📋 Text Report"):
            try:
                text_report = st.session_state.controller.workflow_manager.report_generator.\
                    generate_text_report(
                        results['circuit_name'],
                        results['total_mutants'],
                        results['killed_mutants'],
                        results['survived_mutants'],
                        results['mutation_score'],
                        {},
                        results['mutant_details']
                    )
                st.download_button(
                    label="Download TXT",
                    data=text_report,
                    file_name=f"mutation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error generating text report: {str(e)}")
    
    with col3:
        if st.button("🌐 HTML Report"):
            try:
                html_report = st.session_state.controller.workflow_manager.report_generator.\
                    generate_html_report(
                        results['circuit_name'],
                        results['total_mutants'],
                        results['killed_mutants'],
                        results['survived_mutants'],
                        results['mutation_score'],
                        {}
                    )
                st.download_button(
                    label="Download HTML",
                    data=html_report,
                    file_name=f"mutation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html"
                )
            except Exception as e:
                st.error(f"Error generating HTML report: {str(e)}")
    
    st.divider()
    st.markdown("### Report Preview")
    
    with st.expander("View JSON Report"):
        st.json(results['json_report'])


# Page: Settings
elif page == "Settings":
    st.header("⚙️ System Settings")
    
    st.markdown("### Application Settings")
    
    debug_mode = st.checkbox("Enable Debug Mode")
    if debug_mode:
        Logger.set_level(Logger.DEBUG)
        st.info("Debug mode enabled")
    
    st.divider()
    st.markdown("### Configuration Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Reset to Defaults"):
            st.session_state.config_manager.reset_to_defaults()
            st.success("Configuration reset to defaults!")
            st.rerun()
    
    with col2:
        if st.button("Clear Results"):
            st.session_state.current_results = None
            st.success("Results cleared!")
    
    st.divider()
    st.markdown("### System Information")
    
    st.json({
        'app_name': 'Quantum Circuit Mutation Testing System',
        'version': '1.0.0',
        'python_version': sys.version.split()[0],
        'streamlit_version': st.__version__,
        'database': 'SQLite',
        'simulator': 'Qiskit Aer'
    })


# Footer
st.divider()
st.markdown("""
---
**Quantum Circuit Mutation Testing System** | Built with Streamlit, Qiskit, and PyQt5  
For bug reports and feature requests, contact the development team.
""")
