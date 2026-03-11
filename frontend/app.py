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
    /* Main background and layout */
    .main {
        padding-top: 1.5rem;
    }
    
    body {
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    h1 {
        color: #1f77b4;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #2e86de;
        border-bottom: 3px solid #2e86de;
        padding-bottom: 0.5rem;
        font-weight: 600;
    }
    
    h3 {
        color: #0a3161;
        font-weight: 600;
    }
    
    /* Metric cards */
    .stMetric {
        background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%);
        padding: 1.2rem;
        border-radius: 0.8rem;
        border-left: 5px solid #2e86de;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 2px solid #2e86de;
        margin: 1.5rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2e86de 0%, #1f77b4 100%);
        color: white;
        border: none;
        border-radius: 0.6rem;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(46,134,222,0.3);
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 12px rgba(46,134,222,0.5);
        transform: translateY(-2px);
    }
    
    /* Text input and select */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border: 2px solid #e0e0e0 !important;
        border-radius: 0.6rem !important;
        padding: 0.8rem !important;
        transition: all 0.3s ease;
        color: #333 !important;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #2e86de !important;
        box-shadow: 0 0 0 3px rgba(46,134,222,0.1) !important;
    }
    
    /* Info box */
    .stInformation {
        background-color: #e3f2fd;
        border-left: 5px solid #2e86de;
        border-radius: 0.6rem;
        padding: 1rem;
        color: #1565c0;
        font-weight: 500;
    }
    
    /* Success message */
    .stSuccess {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        border-radius: 0.6rem;
        color: #2e7d32;
    }
    
    /* Warning message */
    .stWarning {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        border-radius: 0.6rem;
        color: #e65100;
    }
    
    /* Error message */
    .stError {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        border-radius: 0.6rem;
        color: #c62828;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f0f0;
        border-radius: 0.6rem 0.6rem 0 0;
        padding: 0.8rem 1.2rem;
        color: #333;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2e86de;
        color: white;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: linear-gradient(90deg, #2e86de, #1f77b4);
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 2px solid #2e86de !important;
        border-radius: 0.6rem !important;
        overflow: hidden;
    }
    
    [data-testid="stDataFrame"] {
        font-weight: 500;
        color: #333 !important;
    }
    
    [data-testid="stDataFrame"] th {
        background-color: #2e86de !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 1rem !important;
    }
    
    [data-testid="stDataFrame"] td {
        padding: 0.8rem !important;
        color: #333 !important;
        font-weight: 500;
    }
    
    /* Slider */
    .stSlider [data-baseweb="slider"] {
        padding: 1rem 0;
    }
    
    /* Checkbox and Radio */
    .stCheckbox, .stRadio {
        padding: 0.5rem;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div > div {
        background-color: white;
        border: 2px solid #e0e0e0;
        border-radius: 0.6rem;
        color: #333;
        font-weight: 500;
    }
    
    /* Markdown text contrast */
    .stMarkdown {
        color: #333;
    }
    
    .stMarkdown strong {
        color: #1f77b4;
        font-weight: 700;
    }
    
    /* Code blocks */
    pre {
        background-color: #f5f5f5 !important;
        border: 1px solid #ddd !important;
        border-radius: 0.6rem !important;
        padding: 1rem !important;
        color: #333 !important;
    }
    
    code {
        color: #d73a49;
        background-color: #f6f8fa;
        padding: 0.2rem 0.4rem;
        border-radius: 0.3rem;
        font-weight: 500;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #e3f2fd !important;
        color: #1565c0 !important;
        font-weight: 600 !important;
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
    st.markdown("**Automated Test Generation and Bug Detection for Quantum Circuits**")
    st.divider()
    
    # Overview section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 About This System
        
        This system provides **automated mutation testing** for quantum circuits:
        
        ✓ **Upload** quantum circuits in QASM format  
        ✓ **Configure** mutation parameters and settings  
        ✓ **Generate** mutant circuits automatically  
        ✓ **Execute** on quantum simulators  
        ✓ **Compare** results statistically  
        ✓ **Calculate** mutation scores  
        ✓ **Generate** detailed reports with visualizations  
        
        ### ⚡ Key Features
        
        - **5+ Mutation Operators**: Comprehensive mutation strategies
        - **Statistical Methods**: Chi-Square, KL Divergence, JS Divergence, Hellinger Distance, Total Variation
        - **Mutation Scoring**: Quantitative test quality assessment
        - **Interactive Visualizations**: Gauges, charts, and distribution plots
        - **Multi-Format Reports**: JSON, HTML, and TXT exports
        - **SQLite Database**: Persistent storage of experiments
        """)
    
    with col2:
        st.markdown("""
        ### 🔄 How It Works (6-Step Pipeline)
        
        **Step 1: Validation**  
        Validates circuit syntax and structure
        
        **Step 2: Mutation**  
        Generates mutant circuits using various operators
        
        **Step 3: Execution**  
        Executes both original and mutant circuits on simulator
        
        **Step 4: Comparison**  
        Compares results using statistical tests
        
        **Step 5: Scoring**  
        Calculates mutation score (killed/total × 100)
        
        **Step 6: Reporting**  
        Generates comprehensive analysis reports
        """)
    
    st.divider()
    
    # Quick start cards
    st.markdown("### 🚀 Quick Start Guide")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 1rem; color: white; text-align: center;">
            <h3 style="margin: 0; color: white;">1️⃣ Upload</h3>
            <p>Go to <b>Upload Circuit</b> page and upload or paste your QASM circuit</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 1rem; color: white; text-align: center;">
            <h3 style="margin: 0; color: white;">2️⃣ Configure</h3>
            <p>Set mutation parameters in <b>Configure Parameters</b> page</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 1rem; color: white; text-align: center;">
            <h3 style="margin: 0; color: white;">3️⃣ Execute</h3>
            <p>Click <b>Execute Testing</b> to run the full pipeline</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Example circuits
    st.markdown("### 📚 Load Example Circuit")
    
    example_col1, example_col2, example_col3, example_col4 = st.columns(4)
    
    with example_col1:
        if st.button("🔔 Bell State", use_container_width=True):
            st.session_state.circuit_input = CircuitExamples.get_bell_state()
            st.session_state.circuit_name = "Bell State"
            st.success("✓ Bell state circuit loaded!")
    
    with example_col2:
        if st.button("👻 GHZ State", use_container_width=True):
            st.session_state.circuit_input = CircuitExamples.get_ghz_state()
            st.session_state.circuit_name = "GHZ State"
            st.success("✓ GHZ state circuit loaded!")
    
    with example_col3:
        if st.button("↔️ Superposition", use_container_width=True):
            st.session_state.circuit_input = CircuitExamples.get_superposition()
            st.session_state.circuit_name = "Superposition"
            st.success("✓ Superposition circuit loaded!")
    
    with example_col4:
        if st.button("🔍 Deutsch Algo", use_container_width=True):
            st.session_state.circuit_input = CircuitExamples.get_deutsch_algorithm()
            st.session_state.circuit_name = "Deutsch Algorithm"
            st.success("✓ Deutsch algorithm circuit loaded!")
    
    st.divider()
    
    # Information boxes
    st.markdown("### ℹ️ System Information")
    
    info_col1, info_col2, info_col3, info_col4 = st.columns(4)
    
    with info_col1:
        st.metric("Mutation Operators", "5+", "Gate ops")
    
    with info_col2:
        st.metric("Statistical Methods", "5+", "Comparison")
    
    with info_col3:
        st.metric("Example Circuits", "16+", "Available")
    
    with info_col4:
        st.metric("Architecture Layers", "6", "Layers")



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
        
        st.markdown("**Operator Descriptions:**", unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #f0f7ff; border-left: 4px solid #2e86de; padding: 1rem; border-radius: 0.5rem;">
            <p style="margin: 0.5rem 0; color: #1f77b4; font-weight: 600;">🔄 <b>Gate Replacement</b></p>
            <p style="margin: 0.5rem 0; color: #333;">Replace gates with different compatible gates</p>
            
            <p style="margin: 1rem 0 0.5rem 0; color: #1f77b4; font-weight: 600;">❌ <b>Gate Removal</b></p>
            <p style="margin: 0.5rem 0; color: #333;">Remove random gates from the circuit</p>
            
            <p style="margin: 1rem 0 0.5rem 0; color: #1f77b4; font-weight: 600;">📐 <b>Rotation Angle Change</b></p>
            <p style="margin: 0.5rem 0; color: #333;">Modify rotation parameters (RX, RY, RZ gates)</p>
            
            <p style="margin: 1rem 0 0.5rem 0; color: #1f77b4; font-weight: 600;">↔️ <b>Qubit Swap</b></p>
            <p style="margin: 0.5rem 0; color: #333;">Swap qubits in two-qubit gates</p>
            
            <p style="margin: 1rem 0 0.5rem 0; color: #1f77b4; font-weight: 600;">🔁 <b>Gate Duplication</b></p>
            <p style="margin: 0.5rem 0; color: #333;">Duplicate random gates immediately after the original</p>
        </div>
        """, unsafe_allow_html=True)
    
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
        st.metric("Mutation Score", f"{results['mutation_score']:.2f}%", f" {score_color}")
    
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
        st.markdown("### 📋 Mutant Details")
        if results.get('mutant_details'):
            df_data = []
            for detail in results['mutant_details']:
                df_data.append({
                    'Index': detail['index'],
                    'Operator': detail['operator'].replace('_', ' ').title(),
                    'Killed': '✅ Killed' if detail.get('is_killed') else '❌ Survived'
                })
            
            st.dataframe(df_data, use_container_width=True, height=400)
        else:
            st.info("No mutant details available")


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
