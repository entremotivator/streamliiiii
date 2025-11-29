import streamlit as st
import requests
import json

# --- Configuration from User's Provided Data ---
# The actual API key will be loaded from st.secrets
# VAPI_API_KEY = st.secrets["vapi_api_key"] 

# All AI Agents with their Assistant IDs (from user's pasted_content.txt)
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

# --- Vapi API Client Functions ---

VAPI_BASE_URL = "https://api.vapi.ai/assistant"

def get_headers():
    """Constructs the authorization headers using the secret API key."""
    try:
        api_key = st.secrets["vapi_api_key"]
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    except KeyError:
        st.error("Vapi API Key not found in Streamlit secrets. Please configure `vapi_api_key`.")
        return None

def get_assistant_config(assistant_id):
    """Fetches the current configuration for a given assistant ID."""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{VAPI_BASE_URL}/{assistant_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error fetching config: {e.response.status_code} - {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching config: {e}")
        return None

def update_assistant_config(assistant_id, payload):
    """Updates the configuration for a given assistant ID."""
    headers = get_headers()
    if not headers:
        return False
    
    url = f"{VAPI_BASE_URL}/{assistant_id}"
    try:
        # Vapi uses PATCH, so we only send the fields we want to update
        response = requests.patch(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        st.success(f"Successfully updated agent {assistant_id}!")
        st.json(response.json())
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error updating config: {e.response.status_code} - {e.response.text}")
        return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating config: {e}")
        return False

# --- Streamlit UI Functions ---

def get_system_prompt(config):
    """Extracts the system prompt from the assistant config."""
    if config and 'model' in config and 'messages' in config['model']:
        for message in config['model']['messages']:
            if message.get('role') == 'system':
                return message.get('content', '')
    return ""

def set_system_prompt(config, new_prompt):
    """Updates or adds the system prompt in the assistant config."""
    if 'model' not in config:
        config['model'] = {}
    if 'messages' not in config['model']:
        config['model']['messages'] = []
        
    found = False
    for message in config['model']['messages']:
        if message.get('role') == 'system':
            message['content'] = new_prompt
            found = True
            break
    
    if not found and new_prompt:
        # Prepend the system message to ensure it's the first one
        config['model']['messages'].insert(0, {"role": "system", "content": new_prompt})

def main():
    st.set_page_config(
        page_title="Vapi Agent Editor",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Vapi Agent Configuration Editor")
    st.markdown("Use this tool to fetch and update the configuration of your Vapi assistants.")

    # --- Agent Selection ---
    agent_names = list(AI_AGENTS.keys())
    selected_agent_name = st.sidebar.selectbox("Select Agent to Edit", agent_names)
    
    if selected_agent_name:
        assistant_id = AI_AGENTS[selected_agent_name]['id']
        st.sidebar.info(f"**Assistant ID:** `{assistant_id}`")
        
        if st.sidebar.button("Load Agent Configuration", use_container_width=True):
            with st.spinner(f"Fetching configuration for {selected_agent_name}..."):
                config = get_assistant_config(assistant_id)
                if config:
                    st.session_state.current_config = config
                    st.session_state.selected_agent_id = assistant_id
                    st.session_state.selected_agent_name = selected_agent_name
                    st.success("Configuration loaded successfully!")
                else:
                    st.session_state.current_config = None
        
        st.sidebar.divider()

    # --- Configuration Editor ---
    if 'current_config' in st.session_state and st.session_state.current_config:
        config = st.session_state.current_config
        
        st.header(f"Editing: {st.session_state.selected_agent_name}")
        st.subheader("Core Settings")
        
        # Extract fields for editing
        current_name = config.get('name', st.session_state.selected_agent_name)
        current_first_message = config.get('firstMessage', '')
        current_system_prompt = get_system_prompt(config)
        current_voice_id = config.get('voice', {}).get('voiceId', 'N/A')
        current_model = config.get('model', {}).get('model', 'N/A')
        
        with st.form("agent_editor_form"):
            
            # General Info
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Agent Name", value=current_name, max_chars=40)
            with col2:
                new_model = st.text_input("LLM Model", value=current_model, help="e.g., gpt-4o, claude-3-opus-20240229")
            
            new_voice_id = st.text_input("Voice ID", value=current_voice_id, help="e.g., andrew, jennifer")
            
            st.subheader("System Prompt (Agent Personality/Instructions)")
            new_system_prompt = st.text_area(
                "System Prompt", 
                value=current_system_prompt, 
                height=300,
                help="This is the main instruction set for your AI agent. It is sent as a 'system' message to the LLM."
            )
            
            st.subheader("First Message (Initial Greeting)")
            new_first_message = st.text_area(
                "First Message", 
                value=current_first_message, 
                height=150,
                help="This is the first message the agent speaks to the user. Leave blank if you want the agent to wait for the user to speak first."
            )
            
            # Submit button
            submitted = st.form_submit_button("💾 Save Changes to Vapi")
            
            if submitted:
                # 1. Build the payload
                payload = {}
                
                # Update name
                if new_name != current_name:
                    payload['name'] = new_name
                
                # Update firstMessage
                if new_first_message != current_first_message:
                    payload['firstMessage'] = new_first_message
                
                # Update system prompt (requires modifying the model.messages array)
                temp_config = json.loads(json.dumps(config)) # Deep copy
                set_system_prompt(temp_config, new_system_prompt)
                
                # Check if messages array changed
                if temp_config['model']['messages'] != config['model']['messages']:
                    if 'model' not in payload:
                        payload['model'] = {}
                    payload['model']['messages'] = temp_config['model']['messages']
                
                # Update model and voice
                if new_model != current_model:
                    if 'model' not in payload:
                        payload['model'] = {}
                    payload['model']['model'] = new_model
                
                if new_voice_id != current_voice_id:
                    payload['voice'] = {'voiceId': new_voice_id}
                
                
                if payload:
                    st.subheader("Payload to be sent:")
                    st.json(payload)
                    
                    # 2. Send the update
                    update_assistant_config(st.session_state.selected_agent_id, payload)
                    
                    # 3. Reload config to show latest changes
                    with st.spinner("Reloading configuration..."):
                        reloaded_config = get_assistant_config(st.session_state.selected_agent_id)
                        if reloaded_config:
                            st.session_state.current_config = reloaded_config
                            st.rerun()
                else:
                    st.info("No changes detected. Nothing to save.")

        st.subheader("Full Current Configuration (Read-Only)")
        st.json(config)
        
    else:
        st.info("Please select an agent and click 'Load Agent Configuration' to begin editing.")

if __name__ == "__main__":
    main()
