import streamlit as st
import subprocess
import sys
import os
import json
import time
import threading
from datetime import datetime, timedelta
import tempfile
import signal
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
import uuid

# Hardcoded VAPI API Key
VAPI_API_KEY = "be55f3ed-dde7-4cc1-8ac4-be6d1efd30bc"  # Replace with your actual API key

# All AI Agents with their Assistant IDs
AI_AGENTS = {
    "Agent CEO": {
        "id": "bf161516-6d88-490c-972e-274098a6b51a",
        "category": "Leadership",
        "description": "Executive leadership and strategic decision-making assistant for C-level operations and corporate governance.",
        "capabilities": ["Strategic Planning", "Executive Decisions", "Corporate Governance", "Leadership Guidance"]
    },
    "Agent Social": {
        "id": "bf161516-6d88-490c-972e-274098a6b51a",
        "category": "Marketing",
        "description": "Social media management and digital marketing specialist for brand engagement and online presence.",
        "capabilities": ["Social Media Strategy", "Content Creation", "Brand Management", "Digital Marketing"]
    },
    "Agent Mindset": {
        "id": "4fe7083e-2f28-4502-b6bf-4ae6ea71a8f4",
        "category": "Personal Development",
        "description": "Personal development and mindset coaching for motivation, goal setting, and mental wellness.",
        "capabilities": ["Mindset Coaching", "Goal Setting", "Motivation", "Personal Growth"]
    },
    "Agent Blogger": {
        "id": "f8ef1ad5-5281-42f1-ae69-f94ff7acb453",
        "category": "Content Creation",
        "description": "Content creation and blogging specialist for article writing, SEO optimization, and content strategy.",
        "capabilities": ["Blog Writing", "SEO Optimization", "Content Strategy", "Editorial Planning"]
    },
    "Agent Grant": {
        "id": "7673e69d-170b-4319-bdf4-e74e5370e98a",
        "category": "Funding",
        "description": "Grant writing and funding acquisition specialist for non-profits, startups, and research projects.",
        "capabilities": ["Grant Writing", "Funding Research", "Proposal Development", "Application Support"]
    },
    "Agent Prayer AI": {
        "id": "339cdad6-9989-4bb6-98ed-bd15521707d1",
        "category": "Spiritual",
        "description": "Spiritual guidance and prayer support for faith-based counseling and religious assistance.",
        "capabilities": ["Spiritual Guidance", "Prayer Support", "Faith Counseling", "Religious Education"]
    },
    "Agent Metrics": {
        "id": "4820eab2-adaf-4f17-a8a0-30cab3e3f007",
        "category": "Analytics",
        "description": "Data analytics and metrics tracking specialist for KPI monitoring and performance analysis.",
        "capabilities": ["Data Analysis", "KPI Tracking", "Performance Metrics", "Reporting"]
    },
    "Agent Researcher": {
        "id": "f05c182f-d3d1-4a17-9c79-52442a9171b8",
        "category": "Research",
        "description": "Research and information gathering specialist for market research, academic studies, and data collection.",
        "capabilities": ["Market Research", "Academic Research", "Data Collection", "Information Analysis"]
    },
    "Agent Investor": {
        "id": "1008771d-86ca-472a-a125-7a7e10100297",
        "category": "Finance",
        "description": "Investment advisory and financial planning specialist for portfolio management and investment strategies.",
        "capabilities": ["Investment Analysis", "Portfolio Management", "Financial Planning", "Market Analysis"]
    },
    "Agent Newsroom": {
        "id": "76f1d6e5-cab4-45b8-9aeb-d3e6f3c0c019",
        "category": "Media",
        "description": "News reporting and journalism specialist for press releases, news articles, and media communications.",
        "capabilities": ["News Writing", "Press Releases", "Media Relations", "Journalism"]
    },
    "STREAMLIT Agent": {
        "id": "538258da-0dda-473d-8ef8-5427251f3ad5",
        "category": "Development",
        "description": "Streamlit application development specialist for data apps and interactive dashboards.",
        "capabilities": ["Streamlit Development", "Data Visualization", "Dashboard Creation", "Web Apps"]
    },
    "HTML/CSS Agent": {
        "id": "14b94e2f-299b-4e75-a445-a4f5feacc522",
        "category": "Development",
        "description": "Web development specialist for HTML, CSS, and frontend design implementation.",
        "capabilities": ["HTML Development", "CSS Styling", "Frontend Design", "Responsive Design"]
    },
    "Business Plan Agent": {
        "id": "bea627a6-3aaf-45d0-8753-94f98d80972c",
        "category": "Business",
        "description": "Business planning and strategy development specialist for comprehensive business plan creation.",
        "capabilities": ["Business Planning", "Strategy Development", "Market Analysis", "Financial Projections"]
    },
    "Ecom Agent": {
        "id": "04b80e02-9615-4c06-9424-93b4b1e2cdc9",
        "category": "E-commerce",
        "description": "E-commerce specialist for online store management, product optimization, and sales strategies.",
        "capabilities": ["E-commerce Strategy", "Product Management", "Sales Optimization", "Online Marketing"]
    },
    "Agent Health": {
        "id": "7b2b8b86-5caa-4f28-8c6b-e7d3d0404f06",
        "category": "Healthcare",
        "description": "Health and wellness specialist for medical information, fitness guidance, and wellness coaching.",
        "capabilities": ["Health Consultation", "Wellness Coaching", "Fitness Guidance", "Medical Information"]
    },
    "Cinch Closer": {
        "id": "232f3d9c-18b3-4963-bdd9-e7de3be156ae",
        "category": "Sales",
        "description": "Sales closing specialist for deal negotiation, customer conversion, and sales optimization.",
        "capabilities": ["Sales Closing", "Deal Negotiation", "Customer Conversion", "Sales Strategy"]
    },
    "DISC Agent": {
        "id": "41fe59e1-829f-4936-8ee5-eef2bb1287fe",
        "category": "Psychology",
        "description": "DISC personality assessment specialist for behavioral analysis and team development.",
        "capabilities": ["DISC Assessment", "Personality Analysis", "Team Building", "Behavioral Coaching"]
    },
    "Invoice Agent": {
        "id": "invoice-agent-id-placeholder",
        "category": "Finance",
        "description": "Invoice management and billing specialist for automated invoicing and payment processing.",
        "capabilities": ["Invoice Creation", "Billing Management", "Payment Processing", "Financial Tracking"]
    },
    "Agent Clone": {
        "id": "88862739-c227-4bfc-b90a-5f450a823e23",
        "category": "AI",
        "description": "AI cloning and replication specialist for creating personalized AI assistants and voice clones.",
        "capabilities": ["AI Cloning", "Voice Replication", "Personalization", "AI Training"]
    },
    "Agent Doctor": {
        "id": "9d1cccc6-3193-4694-a9f7-853198ee4082",
        "category": "Healthcare",
        "description": "Medical consultation specialist for health assessments, symptom analysis, and medical guidance.",
        "capabilities": ["Medical Consultation", "Symptom Analysis", "Health Assessment", "Medical Guidance"]
    },
    "Agent Multi-Lig": {
        "id": "8f045bce-08bc-4477-8d3d-05f233a44df3",
        "category": "Language",
        "description": "Multilingual communication specialist for translation, interpretation, and cross-cultural communication.",
        "capabilities": ["Translation", "Interpretation", "Multilingual Support", "Cultural Communication"]
    },
    "Agent Real Estate": {
        "id": "d982667e-d931-477c-9708-c183ba0aa964",
        "category": "Real Estate",
        "description": "Real estate specialist for property analysis, market evaluation, and real estate transactions.",
        "capabilities": ["Property Analysis", "Market Evaluation", "Real Estate Transactions", "Investment Analysis"]
    },
    "Business Launcher": {
        "id": "dffb2e5c-7d59-462b-a8aa-48746ea70cb1",
        "category": "Business",
        "description": "Business launch specialist for startup guidance, business setup, and entrepreneurial support.",
        "capabilities": ["Startup Guidance", "Business Setup", "Entrepreneurial Support", "Launch Strategy"]
    },
    "Agent Booking": {
        "id": "6de56812-68b9-4b13-8a5c-69f45e642af2",
        "category": "Scheduling",
        "description": "Booking and scheduling specialist for appointment management, calendar coordination, and reservation systems.",
        "capabilities": ["Appointment Scheduling", "Calendar Management", "Booking Systems", "Reservation Handling"]
    }
}

# Agent Categories
AGENT_CATEGORIES = {
    "Leadership": ["Agent CEO"],
    "Marketing": ["Agent Social"],
    "Personal Development": ["Agent Mindset"],
    "Content Creation": ["Agent Blogger"],
    "Funding": ["Agent Grant"],
    "Spiritual": ["Agent Prayer AI"],
    "Analytics": ["Agent Metrics"],
    "Research": ["Agent Researcher"],
    "Finance": ["Agent Investor", "Invoice Agent"],
    "Media": ["Agent Newsroom"],
    "Development": ["STREAMLIT Agent", "HTML/CSS Agent"],
    "Business": ["Business Plan Agent", "Business Launcher"],
    "E-commerce": ["Ecom Agent"],
    "Healthcare": ["Agent Health", "Agent Doctor"],
    "Sales": ["Cinch Closer"],
    "Psychology": ["DISC Agent"],
    "AI": ["Agent Clone"],
    "Language": ["Agent Multi-Lig"],
    "Real Estate": ["Agent Real Estate"],
    "Scheduling": ["Agent Booking"]
}

# Page configuration
st.set_page_config(
    page_title="AI Call Center - Professional Edition",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .call-status-active {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
    }
    .call-status-inactive {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    defaults = {
        "call_active": False,
        "call_history": [],
        "current_process": None,
        "selected_agent": None,
        "call_logs": [],
        "call_analytics": defaultdict(int),
        "user_preferences": {},
        "call_recordings": [],
        "agent_performance": defaultdict(list),
        "call_duration": 0,
        "call_start_time": None,
        "total_calls_today": 0,
        "successful_calls": 0,
        "failed_calls": 0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# Header
st.markdown("""
<div class="main-header">
    <h1>🏢 AI Call Center - Professional Edition</h1>
    <p>Advanced AI-Powered Communication Hub with 25+ Specialized Agents</p>
</div>
""", unsafe_allow_html=True)

# Create the isolated VAPI caller script
def create_vapi_caller_script():
    script_content = '''
import sys
import json
import time
from vapi_python import Vapi
import signal
import os
from datetime import datetime

def signal_handler(signum, frame):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Call interrupted by user")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

def main():
    try:
        if len(sys.argv) != 2:
            print("Usage: python vapi_caller.py <config_json>")
            sys.exit(1)
        
        config = json.loads(sys.argv[1])
        api_key = config["api_key"]
        assistant_id = config["assistant_id"]
        overrides = config.get("overrides", {})
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Initializing VAPI with assistant: {assistant_id}")
        
        vapi = Vapi(api_key=api_key)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting call...")
        call_response = vapi.start(
            assistant_id=assistant_id,
            assistant_overrides=overrides
        )
        
        call_id = getattr(call_response, 'id', 'unknown')
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Call started successfully. Call ID: {call_id}")
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Call is active. Monitoring connection...")
        
        try:
            start_time = time.time()
            while True:
                elapsed = int(time.time() - start_time)
                if elapsed % 30 == 0:  # Status update every 30 seconds
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Call active for {elapsed} seconds")
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Stopping call...")
            try:
                vapi.stop()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Call stopped successfully")
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Error stopping call: {e}")
        
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error in VAPI caller: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    script_path = os.path.join(tempfile.gettempdir(), "vapi_caller_enhanced.py")
    with open(script_path, "w") as f:
        f.write(script_content)
    
    return script_path

# Enhanced call functions
def start_call_isolated(agent_name, assistant_id, overrides=None):
    try:
        if st.session_state.current_process:
            try:
                st.session_state.current_process.terminate()
                st.session_state.current_process.wait(timeout=5)
            except:
                try:
                    st.session_state.current_process.kill()
                except:
                    pass
            st.session_state.current_process = None
        
        script_path = create_vapi_caller_script()
        
        config = {
            "api_key": VAPI_API_KEY,
            "assistant_id": assistant_id,
            "overrides": overrides or {}
        }
        
        config_json = json.dumps(config)
        
        process = subprocess.Popen(
            [sys.executable, script_path, config_json],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        st.session_state.current_process = process
        st.session_state.call_active = True
        st.session_state.selected_agent = agent_name
        st.session_state.call_start_time = datetime.now()
        st.session_state.call_logs = []
        
        # Update analytics
        st.session_state.call_analytics[agent_name] += 1
        st.session_state.total_calls_today += 1
        
        # Add to call history
        call_record = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'agent_name': agent_name,
            'assistant_id': assistant_id,
            'status': 'started',
            'process_id': process.pid,
            'duration': 0
        }
        st.session_state.call_history.append(call_record)
        
        return True, f"Call started with {agent_name} (PID: {process.pid})"
        
    except Exception as e:
        st.session_state.call_active = False
        st.session_state.failed_calls += 1
        return False, f"Failed to start call: {str(e)}"

def stop_call_isolated():
    try:
        if st.session_state.current_process:
            st.session_state.current_process.terminate()
            
            try:
                st.session_state.current_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                st.session_state.current_process.kill()
                st.session_state.current_process.wait()
            
            st.session_state.current_process = None
        
        # Calculate call duration
        if st.session_state.call_start_time:
            duration = (datetime.now() - st.session_state.call_start_time).total_seconds()
            st.session_state.call_duration = duration
            
            # Update call history with duration
            if st.session_state.call_history:
                st.session_state.call_history[-1]['status'] = 'completed'
                st.session_state.call_history[-1]['duration'] = duration
                
            # Update agent performance
            if st.session_state.selected_agent:
                st.session_state.agent_performance[st.session_state.selected_agent].append(duration)
        
        st.session_state.call_active = False
        st.session_state.successful_calls += 1
        
        return True, "Call stopped successfully"
        
    except Exception as e:
        st.session_state.call_active = False
        return False, f"Error stopping call: {str(e)}"

def check_call_status():
    if st.session_state.current_process:
        poll_result = st.session_state.current_process.poll()
        if poll_result is not None:
            st.session_state.call_active = False
            st.session_state.current_process = None
            
            if st.session_state.call_history:
                st.session_state.call_history[-1]['status'] = 'ended'
            
            return False, f"Call process ended with code: {poll_result}"
    
    return st.session_state.call_active, "Call is active"

# Sidebar
with st.sidebar:
    st.header("🎛️ Control Panel")
    
    # API Status
    st.subheader("🔐 API Status")
    if VAPI_API_KEY and VAPI_API_KEY != "your_vapi_api_key_here":
        st.success("✅ API Key Configured")
    else:
        st.error("❌ Please configure API key in code")
    
    # Call Status
    st.subheader("📊 Call Status")
    call_active, status_msg = check_call_status()
    
    if call_active:
        st.markdown('<div class="call-status-active">🟢 Call Active</div>', unsafe_allow_html=True)
        if st.session_state.call_start_time:
            duration = (datetime.now() - st.session_state.call_start_time).total_seconds()
            st.write(f"**Duration:** {int(duration//60)}m {int(duration%60)}s")
        st.write(f"**Agent:** {st.session_state.selected_agent}")
    else:
        st.markdown('<div class="call-status-inactive">🔴 No Active Call</div>', unsafe_allow_html=True)
    
    # Quick Stats
    st.subheader("📈 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Calls", st.session_state.total_calls_today)
        st.metric("Successful", st.session_state.successful_calls)
    with col2:
        st.metric("Available Agents", len(AI_AGENTS))
        st.metric("Failed", st.session_state.failed_calls)
    
    # Emergency Controls
    st.subheader("🚨 Emergency Controls")
    if st.button("🔄 Reset Session", use_container_width=True):
        if st.session_state.current_process:
            try:
                st.session_state.current_process.kill()
            except:
                pass
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        initialize_session_state()
        st.rerun()
    
    if st.button("💀 Force Kill Call", use_container_width=True):
        if st.session_state.current_process:
            try:
                st.session_state.current_process.kill()
                st.session_state.current_process = None
                st.session_state.call_active = False
                st.success("Process terminated")
            except Exception as e:
                st.error(f"Error: {e}")

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🤖 Agents", "📞 Call Center", "📊 Analytics", "📋 History", "⚙️ Settings"])

with tab1:
    st.header("🤖 AI Agent Directory")
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search Agents", placeholder="Search by name or capability...")
    with col2:
        category_filter = st.selectbox("📂 Filter by Category", ["All"] + list(AGENT_CATEGORIES.keys()))
    
    # Display agents
    if category_filter == "All":
        filtered_agents = AI_AGENTS
    else:
        filtered_agents = {name: details for name, details in AI_AGENTS.items() 
                          if name in AGENT_CATEGORIES.get(category_filter, [])}
    
    if search_term:
        filtered_agents = {name: details for name, details in filtered_agents.items()
                          if search_term.lower() in name.lower() or 
                          search_term.lower() in details['description'].lower() or
                          any(search_term.lower() in cap.lower() for cap in details['capabilities'])}
    
    # Display agents in cards
    for i, (agent_name, agent_info) in enumerate(filtered_agents.items()):
        if i % 2 == 0:
            col1, col2 = st.columns(2)
        
        with col1 if i % 2 == 0 else col2:
            with st.container():
                st.markdown(f"""
                <div class="agent-card">
                    <h3>🤖 {agent_name}</h3>
                    <p><strong>Category:</strong> {agent_info['category']}</p>
                    <p><strong>Description:</strong> {agent_info['description']}</p>
                    <p><strong>ID:</strong> <code>{agent_info['id']}</code></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Capabilities
                st.write("**Capabilities:**")
                caps_text = " • ".join(agent_info['capabilities'])
                st.write(f"• {caps_text}")
                
                # Quick call button
                if st.button(f"📞 Call {agent_name}", key=f"quick_call_{agent_name}"):
                    if not st.session_state.call_active:
                        success, message = start_call_isolated(agent_name, agent_info['id'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("Please stop the current call first")
                
                st.divider()

with tab2:
    st.header("📞 Call Center Operations")
    
    # Agent Selection
    st.subheader("🎯 Select Agent")
    
    # Category-based selection
    selected_category = st.selectbox(
        "Choose Category",
        list(AGENT_CATEGORIES.keys()),
        help="Select a category to see available agents"
    )
    
    agents_in_category = AGENT_CATEGORIES[selected_category]
    selected_agent_name = st.selectbox(
        "Choose Agent",
        agents_in_category,
        help="Select the specific agent you want to call"
    )
    
    if selected_agent_name:
        agent_info = AI_AGENTS[selected_agent_name]
        
        # Display selected agent info
        st.subheader("🤖 Selected Agent Details")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**Name:** {selected_agent_name}")
            st.write(f"**Category:** {agent_info['category']}")
            st.write(f"**Description:** {agent_info['description']}")
            st.write(f"**Assistant ID:** `{agent_info['id']}`")
        
        with col2:
            st.write("**Capabilities:**")
            for cap in agent_info['capabilities']:
                st.write(f"• {cap}")
    
    # User Information
    st.subheader("👤 Your Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        user_name = st.text_input("Your Name", placeholder="Enter your name")
    with col2:
        user_company = st.text_input("Company", placeholder="Your company")
    with col3:
        user_phone = st.text_input("Phone", placeholder="+1234567890")
    
    # Call Controls
    st.subheader("🎮 Call Controls")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("▶️ Start Call", disabled=st.session_state.call_active, use_container_width=True):
            overrides = {}
            if user_name:
                overrides["variableValues"] = {
                    "name": user_name,
                    "company": user_company,
                    "phone": user_phone
                }
            
            success, message = start_call_isolated(selected_agent_name, agent_info['id'], overrides)
            if success:
                st.success(message)
                st.balloons()
                st.rerun()
            else:
                st.error(message)
    
    with col2:
        if st.button("⛔ Stop Call", disabled=not st.session_state.call_active, use_container_width=True):
            success, message = stop_call_isolated()
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    
    with col3:
        if st.button("🔄 Check Status", use_container_width=True):
            active, msg = check_call_status()
            if active:
                st.success(f"✅ {msg}")
            else:
                st.info(f"ℹ️ {msg}")
    
    with col4:
        if st.button("📋 View Logs", use_container_width=True):
            st.session_state.show_logs = not getattr(st.session_state, 'show_logs', False)
    
    # Live Call Information
    if st.session_state.call_active:
        st.success("🟢 **Call is currently active**")
        
        # Real-time metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.session_state.call_start_time:
                duration = (datetime.now() - st.session_state.call_start_time).total_seconds()
                st.metric("Call Duration", f"{int(duration//60)}m {int(duration%60)}s")
        with col2:
            st.metric("Agent", st.session_state.selected_agent)
        with col3:
            st.metric("Process ID", st.session_state.current_process.pid if st.session_state.current_process else "N/A")
        
        # Live logs
        if getattr(st.session_state, 'show_logs', False):
            st.subheader("📝 Live Call Logs")
            log_container = st.container()
            
            # Try to read process output
            if st.session_state.current_process:
                try:
                    # Non-blocking read
                    import select
                    if hasattr(select, 'select'):
                        ready, _, _ = select.select([st.session_state.current_process.stdout], [], [], 0)
                        if ready:
                            output = st.session_state.current_process.stdout.readline()
                            if output:
                                st.session_state.call_logs.append(output.strip())
                except:
                    pass
            
            # Display logs
            with log_container:
                for log in st.session_state.call_logs[-10:]:
                    st.text(log)
    else:
        st.info("🔴 **No active call**")

with tab3:
    st.header("📊 Call Analytics & Performance")
    
    if st.session_state.call_history:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_calls = len(st.session_state.call_history)
        completed_calls = len([c for c in st.session_state.call_history if c['status'] == 'completed'])
        avg_duration = sum([c.get('duration', 0) for c in st.session_state.call_history if c.get('duration')]) / max(completed_calls, 1)
        
        with col1:
            st.metric("Total Calls", total_calls)
        with col2:
            st.metric("Completed Calls", completed_calls)
        with col3:
            st.metric("Success Rate", f"{(completed_calls/total_calls*100):.1f}%" if total_calls > 0 else "0%")
        with col4:
            st.metric("Avg Duration", f"{int(avg_duration//60)}m {int(avg_duration%60)}s")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Calls by agent
            agent_calls = defaultdict(int)
            for call in st.session_state.call_history:
                agent_calls[call['agent_name']] += 1
            
            if agent_calls:
                fig = px.bar(
                    x=list(agent_calls.keys()),
                    y=list(agent_calls.values()),
                    title="Calls by Agent",
                    labels={'x': 'Agent', 'y': 'Number of Calls'}
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Call status distribution
            status_counts = defaultdict(int)
            for call in st.session_state.call_history:
                status_counts[call['status']] += 1
            
            if status_counts:
                fig = px.pie(
                    values=list(status_counts.values()),
                    names=list(status_counts.keys()),
                    title="Call Status Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Call timeline
        if len(st.session_state.call_history) > 1:
            st.subheader("📈 Call Timeline")
            
            # Prepare timeline data
            timeline_data = []
            for call in st.session_state.call_history:
                timeline_data.append({
                    'timestamp': call['timestamp'],
                    'agent': call['agent_name'],
                    'duration': call.get('duration', 0),
                    'status': call['status']
                })
            
            df = pd.DataFrame(timeline_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            fig = px.scatter(
                df,
                x='timestamp',
                y='agent',
                size='duration',
                color='status',
                title="Call Timeline",
                hover_data=['duration']
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 No call data available yet. Make some calls to see analytics!")

with tab4:
    st.header("📋 Call History")
    
    if st.session_state.call_history:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "started", "completed", "ended"])
        with col2:
            agent_filter = st.selectbox("Filter by Agent", ["All"] + list(set([c['agent_name'] for c in st.session_state.call_history])))
        with col3:
            date_filter = st.date_input("Filter by Date", value=datetime.now().date())
        
        # Filter data
        filtered_history = st.session_state.call_history
        
        if status_filter != "All":
            filtered_history = [c for c in filtered_history if c['status'] == status_filter]
        
        if agent_filter != "All":
            filtered_history = [c for c in filtered_history if c['agent_name'] == agent_filter]
        
        # Display history
        st.subheader(f"📞 Call Records ({len(filtered_history)} records)")
        
        for call in reversed(filtered_history[-20:]):  # Show last 20 calls
            with st.expander(f"📞 {call['agent_name']} - {call['timestamp']} ({call['status']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Call ID:** {call['id']}")
                    st.write(f"**Agent:** {call['agent_name']}")
                    st.write(f"**Status:** {call['status']}")
                    st.write(f"**Timestamp:** {call['timestamp']}")
                
                with col2:
                    st.write(f"**Assistant ID:** {call['assistant_id']}")
                    st.write(f"**Process ID:** {call.get('process_id', 'N/A')}")
                    if call.get('duration'):
                        duration = call['duration']
                        st.write(f"**Duration:** {int(duration//60)}m {int(duration%60)}s")
                    else:
                        st.write("**Duration:** N/A")
                
                # Action buttons
                if call['status'] == 'started' and st.session_state.call_active:
                    if st.button(f"Stop Call {call['id'][:8]}", key=f"stop_{call['id']}"):
                        success, message = stop_call_isolated()
                        if success:
                            st.success(message)
                            st.rerun()
    else:
        st.info("📋 No call history available yet.")

with tab5:
    st.header("⚙️ Settings & Configuration")
    
    # API Configuration
    st.subheader("🔐 API Configuration")
    st.info("API Key is hardcoded in the application for security.")
    st.code(f"Current API Key: {'*' * (len(VAPI_API_KEY) - 4) + VAPI_API_KEY[-4:] if len(VAPI_API_KEY) > 4 else '****'}")
    
    # User Preferences
    st.subheader("👤 User Preferences")
    col1, col2 = st.columns(2)
    
    with col1:
        default_name = st.text_input("Default Name", value=st.session_state.user_preferences.get('name', ''))
        default_company = st.text_input("Default Company", value=st.session_state.user_preferences.get('company', ''))
    
    with col2:
        default_phone = st.text_input("Default Phone", value=st.session_state.user_preferences.get('phone', ''))
        auto_refresh = st.checkbox("Auto-refresh during calls", value=st.session_state.user_preferences.get('auto_refresh', True))
    
    if st.button("💾 Save Preferences"):
        st.session_state.user_preferences.update({
            'name': default_name,
            'company': default_company,
            'phone': default_phone,
            'auto_refresh': auto_refresh
        })
        st.success("Preferences saved!")
    
    # System Information
    st.subheader("ℹ️ System Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Total Agents:** {len(AI_AGENTS)}")
        st.write(f"**Categories:** {len(AGENT_CATEGORIES)}")
        st.write(f"**Session Start:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    with col2:
        st.write(f"**Python Version:** {sys.version.split()[0]}")
        st.write(f"**Streamlit Version:** {st.__version__}")
        st.write(f"**Platform:** {os.name}")
    
    # Export/Import
    st.subheader("📤 Data Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Export Call History"):
            if st.session_state.call_history:
                df = pd.DataFrame(st.session_state.call_history)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"call_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No data to export")
    
    with col2:
        if st.button("🗑️ Clear All Data"):
            st.session_state.call_history = []
            st.session_state.call_analytics = defaultdict(int)
            st.session_state.agent_performance = defaultdict(list)
            st.session_state.total_calls_today = 0
            st.session_state.successful_calls = 0
            st.session_state.failed_calls = 0
            st.success("All data cleared!")

# Auto-refresh for active calls
if st.session_state.call_active and st.session_state.user_preferences.get('auto_refresh', True):
    time.sleep(3)
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <h3>🏢 AI Call Center - Professional Edition</h3>
    <p>Powered by VAPI • 25+ Specialized AI Agents • Advanced Analytics</p>
    <p>Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
