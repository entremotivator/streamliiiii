import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import time
import pandas as pd
from functools import lru_cache

# --- Page Configuration ---
st.set_page_config(
    page_title="Vapi Agent Configuration Editor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Better Styling ---
st.markdown("""
    <style>
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .success-box {
            background-color: #d4edda;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #28a745;
        }
        .error-box {
            background-color: #f8d7da;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #dc3545;
        }
    </style>
""", unsafe_allow_html=True)

# --- Vapi API Client Functions ---
VAPI_BASE_URL = "https://api.vapi.ai"
REQUEST_TIMEOUT = 10

def get_headers():
    """Constructs authorization headers using the secret API key."""
    try:
        api_key = st.secrets["vapi_api_key"]
        if api_key == "YOUR_VAPI_API_KEY":
            st.error("❌ Please replace 'YOUR_VAPI_API_KEY' in .streamlit/secrets.toml with your actual Vapi API key.")
            return None
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    except KeyError:
        st.error("❌ Vapi API Key not found in Streamlit secrets. Please configure `vapi_api_key`.")
        return None

def handle_api_error(e, context="API Call"):
    """Centralized error handling for API requests."""
    if hasattr(e, 'response') and e.response is not None:
        try:
            error_detail = e.response.json()
            st.error(f"❌ {context} Error ({e.response.status_code}): {error_detail}")
        except:
            st.error(f"❌ {context} Error ({e.response.status_code}): {e.response.text}")
    else:
        st.error(f"❌ {context} Error: {str(e)}")

# --- Assistant Management ---
@st.cache_data(ttl=300)
def list_assistants(limit=100):
    """Fetches all assistants from Vapi API."""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{VAPI_BASE_URL}/assistant"
    params = {"limit": limit}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        handle_api_error(e, "Listing Assistants")
        return []

def get_assistant_config(assistant_id):
    """Fetches configuration for a specific assistant."""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{VAPI_BASE_URL}/assistant/{assistant_id}"
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        handle_api_error(e, "Fetching Assistant Config")
        return None

def update_assistant_config(assistant_id, payload):
    """Updates assistant configuration."""
    headers = get_headers()
    if not headers:
        return False
    
    url = f"{VAPI_BASE_URL}/assistant/{assistant_id}"
    try:
        response = requests.patch(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        st.success(f"✅ Successfully updated agent {assistant_id[:12]}...")
        return True
    except requests.exceptions.RequestException as e:
        handle_api_error(e, "Updating Assistant Config")
        return False

def create_assistant(payload):
    """Creates a new assistant."""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{VAPI_BASE_URL}/assistant"
    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        handle_api_error(e, "Creating Assistant")
        return None

def clone_assistant(assistant_id, new_name=None):
    """Clones an existing assistant."""
    config = get_assistant_config(assistant_id)
    if not config:
        return None
    
    # Remove system fields
    fields_to_remove = ['id', 'orgId', 'createdAt', 'updatedAt']
    for field in fields_to_remove:
        config.pop(field, None)
    
    # Update name
    if new_name:
        config['name'] = new_name
    else:
        config['name'] = f"{config.get('name', 'Assistant')} (Copy)"
    
    return create_assistant(config)

def delete_assistant(assistant_id):
    """Deletes an assistant."""
    headers = get_headers()
    if not headers:
        return False
    
    url = f"{VAPI_BASE_URL}/assistant/{assistant_id}"
    try:
        response = requests.delete(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        handle_api_error(e, "Deleting Assistant")
        return False

# --- Call Management ---
def list_calls(assistant_id=None, limit=100):
    """Fetches recent calls."""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{VAPI_BASE_URL}/call"
    params = {"limit": limit}
    if assistant_id:
        params["assistantId"] = assistant_id
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        handle_api_error(e, "Fetching Calls")
        return []

def get_call_details(call_id):
    """Fetches details for a specific call."""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{VAPI_BASE_URL}/call/{call_id}"
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        handle_api_error(e, "Fetching Call Details")
        return None

# --- Phone Number Management ---
def list_phone_numbers():
    """Fetches all phone numbers."""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{VAPI_BASE_URL}/phone-number"
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        handle_api_error(e, "Fetching Phone Numbers")
        return []

def update_phone_number(phone_id, payload):
    """Updates phone number configuration."""
    headers = get_headers()
    if not headers:
        return False
    
    url = f"{VAPI_BASE_URL}/phone-number/{phone_id}"
    try:
        response = requests.patch(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        handle_api_error(e, "Updating Phone Number")
        return False

# --- Squad Management ---
def list_squads():
    """Fetches all squads."""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{VAPI_BASE_URL}/squad"
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        handle_api_error(e, "Fetching Squads")
        return []

def create_squad(payload):
    """Creates a new squad."""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{VAPI_BASE_URL}/squad"
    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        handle_api_error(e, "Creating Squad")
        return None

# --- Tool/Function Management ---
def list_tools():
    """Fetches all custom tools."""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{VAPI_BASE_URL}/tool"
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        handle_api_error(e, "Fetching Tools")
        return []

def create_tool(payload):
    """Creates a new tool."""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{VAPI_BASE_URL}/tool"
    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        handle_api_error(e, "Creating Tool")
        return None

# --- Analytics & Logs ---
def get_analytics_summary():
    """Gets analytics summary."""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{VAPI_BASE_URL}/analytics"
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def list_logs(limit=100):
    """Fetches system logs."""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{VAPI_BASE_URL}/log"
    params = {"limit": limit}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []

# --- Helper Functions ---
def get_system_prompt(config):
    """Extracts system prompt from config."""
    if config and 'model' in config and 'messages' in config['model']:
        for message in config['model']['messages']:
            if message.get('role') == 'system':
                return message.get('content', '')
    return ""

def set_system_prompt(config, new_prompt):
    """Updates system prompt in config."""
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
        config['model']['messages'].insert(0, {"role": "system", "content": new_prompt})

def get_agent_list():
    """Gets combined hardcoded and live agent list."""
    AI_AGENTS = {
        "Agent CEO": {"id": "bf161516-6d88-490c-972e-274098a6b51a"},
        "Agent Social": {"id": "bf161516-6d88-490c-972e-274098a6b51a"},
        "Agent Mindset": {"id": "4fe7083e-2f28-4502-b6bf-4ae6ea71a8f4"},
        "Agent Blogger": {"id": "f8ef1ad5-5281-42f1-ae69-f94ff7acb453"},
        "Agent Grant": {"id": "7673e69d-170b-4319-bdf4-e74e5370e98a"},
        "Agent Prayer AI": {"id": "339cdad6-9989-4bb6-98ed-bd15521707d1"},
        "Agent Metrics": {"id": "4820eab2-adaf-4f17-a8a0-30cab3e3f007"},
        "Agent Researcher": {"id": "f05c182f-d3d1-4a17-9c79-52442a9171b8"},
        "Agent Investor": {"id": "1008771d-86ca-472a-a125-7a7e10100297"},
        "Agent Newsroom": {"id": "76f1d6e5-cab4-45b8-9aeb-d3e6f3c0c019"},
        "STREAMLIT Agent": {"id": "538258da-0dda-473d-8ef8-5427251f3ad5"},
        "HTML/CSS Agent": {"id": "14b94e2f-299b-4e75-a445-a4f5feacc522"},
        "Business Plan Agent": {"id": "bea627a6-3aaf-45d0-8753-94f98d80972c"},
        "Ecom Agent": {"id": "04b80e02-9615-4c06-9424-93b4b1e2cdc9"},
        "Agent Health": {"id": "7b2b8b86-5caa-4f28-8c6b-e7d3d0404f06"},
        "Cinch Closer": {"id": "232f3d9c-18b3-4963-bdd9-e7de3be156ae"},
        "DISC Agent": {"id": "41fe59e1-829f-4936-8ee5-eef2bb1287fe"},
        "Agent Clone": {"id": "88862739-c227-4bfc-b90a-5f450a823e23"},
        "Agent Doctor": {"id": "9d1cccc6-3193-4694-a9f7-853198ee4082"},
        "Agent Multi-Lig": {"id": "8f045bce-08bc-4477-8d3d-05f233a44df3"},
        "Agent Real Estate": {"id": "d982667e-d931-477c-9708-c183ba0aa964"},
        "Business Launcher": {"id": "dffb2e5c-7d59-462b-a8aa-48746ea70cb1"},
        "Agent Booking": {"id": "6de56812-68b9-4b13-8a5c-69f45e642af2"}
    }
    
    fetched_agents = list_assistants()
    combined_agents = {}
    
    for agent in fetched_agents:
        name = agent.get('name', 'Unnamed Agent')
        combined_agents[f"{name} (Live)"] = {"id": agent['id'], "live": True}
    
    for name, details in AI_AGENTS.items():
        if details['id'] not in [a['id'] for a in fetched_agents]:
            combined_agents[f"{name} (Hardcoded)"] = {"id": details['id'], "live": False}
    
    return combined_agents

# --- Streamlit UI Functions ---
def dashboard_page():
    """Main dashboard with analytics."""
    st.header("📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        agents = list_assistants()
        st.metric("Total Assistants", len(agents), delta=None)
    
    with col2:
        calls = list_calls(limit=1000)
        st.metric("Recent Calls", len(calls), delta=None)
    
    with col3:
        phone_nums = list_phone_numbers()
        st.metric("Phone Numbers", len(phone_nums), delta=None)
    
    with col4:
        squads = list_squads()
        st.metric("Squads", len(squads), delta=None)
    
    st.divider()
    
    # Call analytics
    if calls:
        st.subheader("📈 Call Analytics")
        
        # Duration analysis
        durations = [call.get('duration', 0) for call in calls if 'duration' in call]
        if durations:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Avg Call Duration", f"{sum(durations)//len(durations)}s", delta=None)
            with col2:
                st.metric("Total Call Time", f"{sum(durations)//60}m", delta=None)
            with col3:
                st.metric("Longest Call", f"{max(durations)}s", delta=None)
        
        # Recent calls table
        st.subheader("Recent Calls")
        recent_data = []
        for call in calls[:20]:
            recent_data.append({
                "ID": call.get('id', 'N/A')[:12] + '...',
                "Duration": f"{call.get('duration', 0)}s",
                "Status": call.get('status', 'N/A'),
                "From": call.get('customerNumber', 'N/A'),
                "Date": datetime.fromisoformat(call.get('createdAt', '').replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M') if 'createdAt' in call else 'N/A'
            })
        st.dataframe(pd.DataFrame(recent_data), use_container_width=True)

def assistant_editor_page():
    """Enhanced assistant editor."""
    st.header("✏️ Assistant Editor")
    
    combined_agents = get_agent_list()
    agent_names = sorted(list(combined_agents.keys()))
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_agent_name = st.selectbox("Select Agent to Edit", agent_names)
    
    with col2:
        if st.button("🔄 Refresh List", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    if selected_agent_name:
        assistant_id = combined_agents[selected_agent_name]['id']
        is_live = combined_agents[selected_agent_name]['live']
        
        st.sidebar.info(f"**Assistant ID:** `{assistant_id}`")
        st.sidebar.caption(f"Status: {'🟢 Live' if is_live else '🟡 Hardcoded (May be invalid)'}")
        
        if 'selected_agent_id' not in st.session_state or st.session_state.selected_agent_id != assistant_id:
            st.session_state.current_config = None
            st.session_state.selected_agent_id = assistant_id
        
        load_col1, load_col2, load_col3 = st.columns([2, 1, 1])
        
        with load_col1:
            if st.button("📥 Load Agent Configuration", use_container_width=True, type="primary"):
                with st.spinner(f"Fetching configuration for {selected_agent_name}..."):
                    config = get_assistant_config(assistant_id)
                    if config:
                        st.session_state.current_config = config
                        st.session_state.selected_agent_name = selected_agent_name
                        st.success("✅ Configuration loaded successfully!")
                    else:
                        st.session_state.current_config = None
        
        with load_col2:
            if st.button("🔄 Clone Agent", use_container_width=True):
                clone_name = f"{selected_agent_name} - Copy"
                with st.spinner(f"Cloning {selected_agent_name}..."):
                    result = clone_assistant(assistant_id, clone_name)
                    if result:
                        st.success(f"✅ Successfully cloned agent! New ID: {result.get('id')}")
                    else:
                        st.error("❌ Failed to clone agent")
        
        with load_col3:
            if st.button("🗑️ Delete Agent", use_container_width=True):
                with st.spinner("Deleting agent..."):
                    if delete_assistant(assistant_id):
                        st.success("✅ Agent deleted successfully!")
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete agent")
        
        st.divider()
        
        if 'current_config' in st.session_state and st.session_state.current_config:
            config = st.session_state.current_config
            st.subheader(f"Editing: {st.session_state.selected_agent_name}")
            
            # Extract current values
            current_name = config.get('name', selected_agent_name.split(' (')[0])
            current_first_message = config.get('firstMessage', '')
            current_background_sound = config.get('backgroundSound', 'office')
            current_background_denoise = config.get('backgroundDenoisingEnabled', False)
            current_end_call_phrases = config.get('endCallPhrases', [])
            current_silence_timeout = config.get('silenceTimeoutSeconds', 10)
            current_max_duration = config.get('maxDurationSeconds', 600)
            current_record_enabled = config.get('recordingEnabled', False)
            current_hipaa_enabled = config.get('hipaaEnabled', False)
            current_server_url = config.get('serverUrl', '')
            current_server_secret = config.get('serverSecret', '')
            
            model_config = config.get('model', {})
            current_system_prompt = get_system_prompt(config)
            current_model = model_config.get('model', 'gpt-4o')
            current_temperature = model_config.get('temperature', 0.7)
            # <CHANGE> Fixed max tokens - use min of current value and 4000 to avoid error
            current_max_tokens = min(model_config.get('maxTokens', 2000), 4000)
            
            voice_config = config.get('voice', {})
            current_voice_provider = voice_config.get('provider', 'playht')
            current_voice_id = voice_config.get('voiceId', 'andrew')
            current_voice_speed = voice_config.get('speed', 1.0)
            
            transcriber_config = config.get('transcriber', {})
            current_transcriber_provider = transcriber_config.get('provider', 'deepgram')
            current_transcriber_model = transcriber_config.get('model', 'base')
            current_transcriber_language = transcriber_config.get('language', 'en')
            
            with st.form("agent_editor_form"):
                tab1, tab2, tab3, tab4, tab5 = st.tabs(
                    ["⚙️ General", "💬 Conversation", "🤖 Model", "🎙️ Voice", "📹 Recording"]
                )
                
                with tab1:
                    st.subheader("General Settings")
                    col1, col2 = st.columns(2)
                    with col1:
                        new_name = st.text_input("Agent Name", value=current_name, max_chars=100)
                    with col2:
                        new_silence_timeout = st.number_input(
                            "Silence Timeout (seconds)",
                            min_value=5, max_value=300, value=current_silence_timeout, step=5,
                            help="How long to wait before ending call due to silence"
                        )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        new_server_url = st.text_input("Server URL", value=current_server_url,
                                                       help="Your backend server URL for webhooks")
                    with col2:
                        new_server_secret = st.text_input("Server Secret", value=current_server_secret,
                                                          type="password", help="Secret key for webhook authentication")
                    
                    new_max_duration = st.number_input(
                        "Max Call Duration (seconds)",
                        min_value=60, max_value=3600, value=current_max_duration, step=60,
                        help="Maximum duration for a call"
                    )
                
                with tab2:
                    st.subheader("Conversation Settings")
                    
                    new_first_message = st.text_area(
                        "First Message (Initial Greeting)",
                        value=current_first_message,
                        height=100,
                        help="The first message the agent speaks. Leave blank for user to speak first."
                    )
                    
                    new_system_prompt = st.text_area(
                        "System Prompt (Agent Personality & Instructions)",
                        value=current_system_prompt,
                        height=200,
                        help="Main instruction set for your AI agent."
                    )
                    
                    end_phrases_text = st.text_area(
                        "End Call Phrases (one per line)",
                        value="\n".join(current_end_call_phrases),
                        height=80,
                        help="Phrases that will trigger the call to end"
                    )
                    new_end_call_phrases = [p.strip() for p in end_phrases_text.split('\n') if p.strip()]
                
                with tab3:
                    st.subheader("AI Model Settings")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        model_options = ['gpt-4', 'gpt-4-turbo', 'gpt-4o', 'gpt-3.5-turbo',
                                        'claude-3-opus-20240229', 'claude-3-sonnet-20240229',
                                        'claude-3-haiku-20240307']
                        try:
                            model_index = model_options.index(current_model)
                        except ValueError:
                            model_index = 0
                        new_model = st.selectbox("LLM Model", options=model_options, index=model_index)
                    
                    with col2:
                        new_temperature = st.slider("Temperature", 0.0, 2.0, current_temperature, 0.1)
                    
                    with col3:
                        # <CHANGE> Max tokens now properly constrained to 4000
                        new_max_tokens = st.number_input("Max Tokens", min_value=50, max_value=4000, 
                                                         value=current_max_tokens, step=50)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        new_background_sound = st.text_input(
                            "Background Sound",
                            value=current_background_sound,
                            help="e.g., 'office', 'off', or a URL to an audio file."
                        )
                    with col2:
                        new_background_denoise = st.checkbox("Background Denoising", value=current_background_denoise)
                
                with tab4:
                    st.subheader("Voice Settings")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        voice_providers = ['playht', 'elevenlabs', 'azure', 'rime-ai', 'deepgram']
                        try:
                            voice_idx = voice_providers.index(current_voice_provider)
                        except ValueError:
                            voice_idx = 0
                        new_voice_provider = st.selectbox("Voice Provider", options=voice_providers, index=voice_idx)
                    
                    with col2:
                        new_voice_id = st.text_input("Voice ID", value=current_voice_id, help="e.g., andrew, jennifer")
                    
                    with col3:
                        new_voice_speed = st.slider("Voice Speed", 0.5, 2.0, current_voice_speed, 0.1)
                    
                    # Transcriber settings
                    st.subheader("Transcriber Settings")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        transcriber_providers = ['deepgram', 'talkscriber']
                        try:
                            trans_idx = transcriber_providers.index(current_transcriber_provider)
                        except ValueError:
                            trans_idx = 0
                        new_transcriber_provider = st.selectbox("Transcriber Provider", 
                                                               options=transcriber_providers, index=trans_idx)
                    with col2:
                        new_transcriber_model = st.text_input("Transcriber Model", value=current_transcriber_model)
                    with col3:
                        new_transcriber_language = st.text_input("Language", value=current_transcriber_language)
                
                with tab5:
                    st.subheader("Recording & Compliance")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        new_record_enabled = st.checkbox("Enable Call Recording", value=current_record_enabled)
                    with col2:
                        new_hipaa_enabled = st.checkbox("HIPAA Compliance Mode", value=current_hipaa_enabled)
                    
                    if new_hipaa_enabled:
                        st.warning("⚠️ HIPAA mode affects data handling and compliance requirements.")
                
                # Submit buttons
                st.divider()
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    submitted = st.form_submit_button("💾 Save All Changes", use_container_width=True, type="primary")
                with col2:
                    preview = st.form_submit_button("👁️ Preview", use_container_width=True)
                with col3:
                    export = st.form_submit_button("📥 Export", use_container_width=True)
                with col4:
                    reset = st.form_submit_button("🔄 Reset", use_container_width=True)
                
                if submitted:
                    payload = {}
                    
                    if new_name != current_name:
                        payload['name'] = new_name
                    if new_server_url != current_server_url:
                        payload['serverUrl'] = new_server_url
                    if new_server_secret != current_server_secret:
                        payload['serverSecret'] = new_server_secret
                    
                    if new_background_sound != current_background_sound:
                        payload['backgroundSound'] = new_background_sound
                    if new_background_denoise != current_background_denoise:
                        payload['backgroundDenoisingEnabled'] = new_background_denoise
                    
                    if new_first_message != current_first_message:
                        payload['firstMessage'] = new_first_message
                    if new_end_call_phrases != current_end_call_phrases:
                        payload['endCallPhrases'] = new_end_call_phrases
                    
                    if new_silence_timeout != current_silence_timeout:
                        payload['silenceTimeoutSeconds'] = new_silence_timeout
                    if new_max_duration != current_max_duration:
                        payload['maxDurationSeconds'] = new_max_duration
                    
                    model_payload = {}
                    if new_model != current_model:
                        model_payload['model'] = new_model
                    if new_temperature != current_temperature:
                        model_payload['temperature'] = new_temperature
                    if new_max_tokens != current_max_tokens:
                        model_payload['maxTokens'] = new_max_tokens
                    
                    temp_config = json.loads(json.dumps(config))
                    set_system_prompt(temp_config, new_system_prompt)
                    if temp_config.get('model', {}).get('messages') != config.get('model', {}).get('messages'):
                        model_payload['messages'] = temp_config['model']['messages']
                    
                    if model_payload:
                        payload['model'] = model_payload
                    
                    transcriber_payload = {}
                    if new_transcriber_provider != current_transcriber_provider:
                        transcriber_payload['provider'] = new_transcriber_provider
                    if new_transcriber_model != current_transcriber_model:
                        transcriber_payload['model'] = new_transcriber_model
                    if new_transcriber_language != current_transcriber_language:
                        transcriber_payload['language'] = new_transcriber_language
                    
                    if transcriber_payload:
                        payload['transcriber'] = transcriber_payload
                    
                    voice_payload = {}
                    if new_voice_provider != current_voice_provider:
                        voice_payload['provider'] = new_voice_provider
                    if new_voice_id != current_voice_id:
                        voice_payload['voiceId'] = new_voice_id
                    if new_voice_speed != current_voice_speed:
                        voice_payload['speed'] = new_voice_speed
                    
                    if voice_payload:
                        payload['voice'] = voice_payload
                    
                    if new_record_enabled != current_record_enabled:
                        payload['recordingEnabled'] = new_record_enabled
                    if new_hipaa_enabled != current_hipaa_enabled:
                        payload['hipaaEnabled'] = new_hipaa_enabled
                    
                    if payload:
                        st.info("📋 Payload to be sent:")
                        st.json(payload)
                        
                        if update_assistant_config(st.session_state.selected_agent_id, payload):
                            st.success("✅ Configuration updated successfully!")
                            st.session_state.current_config = None
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.info("ℹ️ No changes detected. Nothing to save.")
                
                if preview:
                    st.subheader("Configuration Preview")
                    st.json(config)
                
                if export:
                    st.download_button(
                        label="📥 Download Config JSON",
                        data=json.dumps(config, indent=2),
                        file_name=f"{assistant_id}_config.json",
                        mime="application/json"
                    )
                
                if reset:
                    st.session_state.current_config = None
                    st.rerun()
        else:
            st.info("📌 Please select an agent and click 'Load Agent Configuration' to begin editing.")

def phone_number_manager_page():
    """Phone number management."""
    st.header("📞 Phone Number Manager")
    
    phone_numbers = list_phone_numbers()
    if not phone_numbers:
        st.warning("No phone numbers found.")
        return
    
    data = []
    for num in phone_numbers:
        data.append({
            "Number": num.get('number', 'N/A'),
            "ID": num.get('id', 'N/A')[:12] + '...',
            "Assistant ID": num.get('assistantId', 'N/A')[:12] + '...',
            "Provider": num.get('provider', 'N/A'),
            "Status": num.get('status', 'N/A')
        })
    
    st.dataframe(pd.DataFrame(data), use_container_width=True)
    
    st.divider()
    st.subheader("Update Phone Number Assignment")
    
    phone_options = {f"{d['Number']}": num.get('id') for d, num in zip(data, phone_numbers)}
    selected_phone = st.selectbox("Select Phone Number", list(phone_options.keys()))
    
    if selected_phone:
        selected_phone_id = phone_options[selected_phone]
        
        combined_agents = get_agent_list()
        agent_options = {f"{name} ({details['id'][:8]}...)": details['id'] for name, details in combined_agents.items()}
        
        new_assistant = st.selectbox("Assign New Assistant", list(agent_options.keys()))
        
        if st.button("✅ Assign Assistant", type="primary", use_container_width=True):
            new_assistant_id = agent_options[new_assistant]
            payload = {"assistantId": new_assistant_id}
            
            if update_phone_number(selected_phone_id, payload):
                st.success(f"✅ Successfully assigned {new_assistant} to {selected_phone}!")
                st.cache_data.clear()
                time.sleep(1)
                st.rerun()

def call_logs_page():
    """Call logs and analytics."""
    st.header("📞 Call Logs & Analytics")
    
    combined_agents = get_agent_list()
    agent_options = {f"{name}": details['id'] for name, details in combined_agents.items()}
    
    col1, col2 = st.columns([3, 1])
    with col1:
        filter_agent = st.selectbox("Filter by Assistant", ["All Assistants"] + sorted(list(agent_options.keys())))
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
    
    filter_assistant_id = agent_options.get(filter_agent) if filter_agent != "All Assistants" else None
    
    with st.spinner("Fetching call logs..."):
        calls = list_calls(assistant_id=filter_assistant_id, limit=200)
    
    if not calls:
        st.info("No calls found for the selected filter.")
        return
    
    data = []
    for call in calls:
        duration = call.get('duration', 0)
        duration_str = f"{duration // 60}m {duration % 60}s" if duration else "N/A"
        
        data.append({
            "ID": call.get('id', 'N/A')[:12] + '...',
            "Duration": duration_str,
            "From": call.get('customerNumber', 'N/A'),
            "To": call.get('phoneNumber', 'N/A'),
            "Status": call.get('status', 'N/A'),
            "Date": datetime.fromisoformat(call['createdAt'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M') if 'createdAt' in call else 'N/A'
        })
    
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
    
    # Call details viewer
    st.divider()
    st.subheader("View Full Call Details")
    
    call_ids = [call.get('id') for call in calls]
    selected_call_id = st.selectbox("Select Call ID", call_ids, format_func=lambda x: x[:12] + '...')
    
    if st.button("📋 Get Full Details", use_container_width=True):
        details = get_call_details(selected_call_id)
        if details:
            st.json(details)

def squads_tools_page():
    """Squads and tools management."""
    st.header("👥 Squads & Tools Manager")
    
    tab1, tab2 = st.tabs(["👥 Squads", "🔧 Tools"])
    
    with tab1:
        st.subheader("Assistant Squads (Groups)")
        
        squads = list_squads()
        if squads:
            squad_data = []
            for squad in squads:
                squad_data.append({
                    "Name": squad.get('name', 'N/A'),
                    "ID": squad.get('id', 'N/A')[:12] + '...',
                    "Assistants": len(squad.get('assistantIds', [])),
                    "Routing": squad.get('routingStrategy', 'N/A')
                })
            st.dataframe(pd.DataFrame(squad_data), use_container_width=True)
        else:
            st.info("No squads found.")
        
        st.divider()
        st.subheader("Create New Squad")
        
        with st.form("create_squad_form"):
            squad_name = st.text_input("Squad Name")
            routing_strategy = st.selectbox("Routing Strategy", ["sequential", "round-robin", "random"])
            
            combined_agents = get_agent_list()
            agent_options = {f"{name}": details['id'] for name, details in combined_agents.items()}
            selected_agents = st.multiselect("Select Assistants", list(agent_options.keys()))
            
            if st.form_submit_button("✅ Create Squad", type="primary", use_container_width=True):
                if squad_name and selected_agents:
                    payload = {
                        "name": squad_name,
                        "routingStrategy": routing_strategy,
                        "assistantIds": [agent_options[agent] for agent in selected_agents]
                    }
                    
                    if create_squad(payload):
                        st.success(f"✅ Squad '{squad_name}' created successfully!")
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error("Please fill in all fields.")
    
    with tab2:
        st.subheader("Custom Tools/Functions")
        
        tools = list_tools()
        if tools:
            tool_data = []
            for tool in tools:
                tool_data.append({
                    "Name": tool.get('name', 'N/A'),
                    "ID": tool.get('id', 'N/A')[:12] + '...',
                    "Type": tool.get('type', 'N/A'),
                    "URL": tool.get('url', 'N/A')
                })
            st.dataframe(pd.DataFrame(tool_data), use_container_width=True)
        else:
            st.info("No custom tools found.")

def settings_page():
    """Settings and system info."""
    st.header("⚙️ Settings & System Info")
    
    st.subheader("API Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**API Base URL:** {VAPI_BASE_URL}")
    
    with col2:
        st.info(f"**Request Timeout:** {REQUEST_TIMEOUT}s")
    
    st.divider()
    st.subheader("System Logs")
    
    logs = list_logs(limit=50)
    if logs:
        log_data = []
        for log in logs:
            log_data.append({
                "Level": log.get('level', 'N/A'),
                "Message": log.get('message', 'N/A')[:50] + '...',
                "Timestamp": log.get('timestamp', 'N/A')
            })
        st.dataframe(pd.DataFrame(log_data), use_container_width=True)
    else:
        st.info("No system logs available.")

def main():
    """Main app entry point."""
    st.title("🤖 Vapi Agent Configuration Editor")
    st.markdown("Comprehensive tool to manage your Vapi assistants, phone numbers, calls, and more.")
    
    # Initialize session state
    if 'selected_agent_id' not in st.session_state:
        st.session_state.selected_agent_id = None
    if 'current_config' not in st.session_state:
        st.session_state.current_config = None
    
    # Sidebar navigation
    st.sidebar.title("🗂️ Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Assistant Editor", "Phone Number Manager", "Call Logs", "Squads & Tools", "Settings"],
        index=0
    )
    
    st.sidebar.divider()
    
    # Page routing
    if page == "Dashboard":
        dashboard_page()
    elif page == "Assistant Editor":
        assistant_editor_page()
    elif page == "Phone Number Manager":
        phone_number_manager_page()
    elif page == "Call Logs":
        call_logs_page()
    elif page == "Squads & Tools":
        squads_tools_page()
    elif page == "Settings":
        settings_page()

if __name__ == "__main__":
    main()
