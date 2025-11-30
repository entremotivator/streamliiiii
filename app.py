import streamlit as st
import requests
import json
from datetime import datetime
import time

# --- Vapi API Client Functions ---

VAPI_BASE_URL = "https://api.vapi.ai"

def get_headers():
    """Constructs the authorization headers using the secret API key."""
    try:
        api_key = st.secrets["vapi_api_key"]
        if api_key == "YOUR_VAPI_API_KEY":
            st.error("Please replace 'YOUR_VAPI_API_KEY' in .streamlit/secrets.toml with your actual Vapi API key.")
            return None
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    except KeyError:
        st.error("Vapi API Key not found in Streamlit secrets. Please configure `vapi_api_key`.")
        return None

# --- Assistant Management ---

@st.cache_data(ttl=300)
def list_assistants():
    """Fetches the list of all assistants from the Vapi API."""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{VAPI_BASE_URL}/assistant"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error listing assistants: {e.response.status_code} - {e.response.text}")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error listing assistants: {e}")
        return []

def get_assistant_config(assistant_id):
    """Fetches the current configuration for a given assistant ID."""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{VAPI_BASE_URL}/assistant/{assistant_id}"
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
    
    url = f"{VAPI_BASE_URL}/assistant/{assistant_id}"
    try:
        response = requests.patch(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        st.success(f"✅ Successfully updated agent {assistant_id}!")
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error updating config: {e.response.status_code} - {e.response.text}")
        return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating config: {e}")
        return False

def create_assistant(payload):
    """Creates a new assistant."""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{VAPI_BASE_URL}/assistant"
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error creating assistant: {e.response.status_code} - {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating assistant: {e}")
        return None

def delete_assistant(assistant_id):
    """Deletes an assistant."""
    headers = get_headers()
    if not headers:
        return False
    
    url = f"{VAPI_BASE_URL}/assistant/{assistant_id}"
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error deleting assistant: {e.response.status_code} - {e.response.text}")
        return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting assistant: {e}")
        return False

# --- Call Management ---

def list_calls(assistant_id=None, limit=10):
    """Fetches recent calls, optionally filtered by assistant."""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{VAPI_BASE_URL}/call"
    params = {"limit": limit}
    if assistant_id:
        params["assistantId"] = assistant_id
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching calls: {e}")
        return []

def get_call_details(call_id):
    """Fetches details for a specific call."""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{VAPI_BASE_URL}/call/{call_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching call details: {e}")
        return None

# --- Phone Number Management ---

def list_phone_numbers():
    """Fetches all phone numbers."""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{VAPI_BASE_URL}/phone-number"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching phone numbers: {e}")
        return []

# --- Helper Functions ---

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
        config['model']['messages'].insert(0, {"role": "system", "content": new_prompt})

def format_timestamp(timestamp):
    """Formats ISO timestamp to readable format."""
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return timestamp

# --- UI Components ---

def render_assistant_editor(config, assistant_id):
    """Renders the main assistant editor form."""
    
    # Extract current values
    current_name = config.get('name', 'Unnamed Agent')
    current_first_message = config.get('firstMessage', '')
    current_system_prompt = get_system_prompt(config)
    
    # Voice settings
    voice_config = config.get('voice', {})
    current_voice_id = voice_config.get('voiceId', 'andrew')
    current_voice_provider = voice_config.get('provider', 'playht')
    
    # Model settings
    model_config = config.get('model', {})
    current_model = model_config.get('model', 'gpt-4')
    current_temperature = model_config.get('temperature', 0.7)
    current_max_tokens = model_config.get('maxTokens', 250)
    
    # Advanced settings
    current_end_call_phrases = config.get('endCallPhrases', [])
    current_silence_timeout = config.get('silenceTimeoutSeconds', 30)
    current_max_duration = config.get('maxDurationSeconds', 600)
    current_background_sound = config.get('backgroundSound', 'off')
    
    with st.form("agent_editor_form"):
        
        # Basic Info
        st.subheader("🔹 Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Agent Name", value=current_name, max_chars=100)
        with col2:
            new_background_sound = st.selectbox(
                "Background Sound",
                options=['off', 'office'],
                index=['off', 'office'].index(current_background_sound) if current_background_sound in ['off', 'office'] else 0
            )
        
        st.divider()
        
        # Messages
        st.subheader("💬 Conversation Settings")
        new_first_message = st.text_area(
            "First Message (Initial Greeting)", 
            value=current_first_message, 
            height=100,
            help="The first message the agent speaks. Leave blank for user to speak first."
        )
        
        new_system_prompt = st.text_area(
            "System Prompt (Agent Personality & Instructions)", 
            value=current_system_prompt, 
            height=300,
            help="Main instruction set for your AI agent."
        )
        
        # End call phrases
        end_phrases_text = st.text_area(
            "End Call Phrases (one per line)",
            value="\n".join(current_end_call_phrases),
            height=80,
            help="Phrases that will trigger the call to end"
        )
        new_end_call_phrases = [p.strip() for p in end_phrases_text.split('\n') if p.strip()]
        
        st.divider()
        
        # Model Configuration
        st.subheader("🤖 AI Model Settings")
        col1, col2, col3 = st.columns(3)
        with col1:
            new_model = st.selectbox(
                "LLM Model",
                options=['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo', 'claude-3-opus-20240229', 'claude-3-sonnet-20240229'],
                index=['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo', 'claude-3-opus-20240229', 'claude-3-sonnet-20240229'].index(current_model) if current_model in ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo', 'claude-3-opus-20240229', 'claude-3-sonnet-20240229'] else 0
            )
        with col2:
            new_temperature = st.slider("Temperature", 0.0, 2.0, current_temperature, 0.1)
        with col3:
            new_max_tokens = st.number_input("Max Tokens", 50, 4000, current_max_tokens, 50)
        
        st.divider()
        
        # Voice Configuration
        st.subheader("🎙️ Voice Settings")
        col1, col2 = st.columns(2)
        with col1:
            new_voice_provider = st.selectbox(
                "Voice Provider",
                options=['playht', 'elevenlabs', 'azure'],
                index=['playht', 'elevenlabs', 'azure'].index(current_voice_provider) if current_voice_provider in ['playht', 'elevenlabs', 'azure'] else 0
            )
        with col2:
            new_voice_id = st.text_input("Voice ID", value=current_voice_id, help="e.g., andrew, jennifer")
        
        st.divider()
        
        # Timing Settings
        st.subheader("⏱️ Timing & Duration")
        col1, col2 = st.columns(2)
        with col1:
            new_silence_timeout = st.number_input(
                "Silence Timeout (seconds)", 
                5, 300, current_silence_timeout, 5,
                help="How long to wait before ending call due to silence"
            )
        with col2:
            new_max_duration = st.number_input(
                "Max Call Duration (seconds)", 
                60, 3600, current_max_duration, 60,
                help="Maximum duration for a call"
            )
        
        # Submit buttons
        st.divider()
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            submitted = st.form_submit_button("💾 Save All Changes", use_container_width=True, type="primary")
        with col2:
            preview = st.form_submit_button("👁️ Preview Changes", use_container_width=True)
        with col3:
            reset = st.form_submit_button("🔄 Reset Form", use_container_width=True)
        
        if submitted:
            # Build payload
            payload = {}
            
            if new_name != current_name:
                payload['name'] = new_name
            
            if new_first_message != current_first_message:
                payload['firstMessage'] = new_first_message
            
            if new_background_sound != current_background_sound:
                payload['backgroundSound'] = new_background_sound
            
            if new_end_call_phrases != current_end_call_phrases:
                payload['endCallPhrases'] = new_end_call_phrases
            
            if new_silence_timeout != current_silence_timeout:
                payload['silenceTimeoutSeconds'] = new_silence_timeout
            
            if new_max_duration != current_max_duration:
                payload['maxDurationSeconds'] = new_max_duration
            
            # System prompt
            temp_config = json.loads(json.dumps(config))
            set_system_prompt(temp_config, new_system_prompt)
            if temp_config['model']['messages'] != config['model']['messages']:
                if 'model' not in payload:
                    payload['model'] = {}
                payload['model']['messages'] = temp_config['model']['messages']
            
            # Model settings
            if new_model != current_model or new_temperature != current_temperature or new_max_tokens != current_max_tokens:
                if 'model' not in payload:
                    payload['model'] = {}
                if new_model != current_model:
                    payload['model']['model'] = new_model
                if new_temperature != current_temperature:
                    payload['model']['temperature'] = new_temperature
                if new_max_tokens != current_max_tokens:
                    payload['model']['maxTokens'] = new_max_tokens
            
            # Voice settings
            if new_voice_id != current_voice_id or new_voice_provider != current_voice_provider:
                payload['voice'] = {
                    'provider': new_voice_provider,
                    'voiceId': new_voice_id
                }
            
            if payload:
                with st.spinner("Saving changes..."):
                    if update_assistant_config(assistant_id, payload):
                        list_assistants.clear()
                        time.sleep(0.5)
                        reloaded_config = get_assistant_config(assistant_id)
                        if reloaded_config:
                            st.session_state.current_config = reloaded_config
                            st.rerun()
            else:
                st.info("No changes detected.")
        
        elif preview:
            st.subheader("Preview of Changes")
            payload = {
                'name': new_name,
                'firstMessage': new_first_message,
                'model': {
                    'model': new_model,
                    'temperature': new_temperature,
                    'maxTokens': new_max_tokens
                },
                'voice': {
                    'provider': new_voice_provider,
                    'voiceId': new_voice_id
                },
                'silenceTimeoutSeconds': new_silence_timeout,
                'maxDurationSeconds': new_max_duration,
                'backgroundSound': new_background_sound,
                'endCallPhrases': new_end_call_phrases
            }
            st.json(payload)
        
        elif reset:
            st.rerun()

def render_call_analytics(assistant_id):
    """Renders call analytics for an assistant."""
    st.subheader("📞 Recent Calls")
    
    calls = list_calls(assistant_id=assistant_id, limit=20)
    
    if not calls:
        st.info("No calls found for this assistant.")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Calls", len(calls))
    with col2:
        completed = sum(1 for c in calls if c.get('status') == 'ended')
        st.metric("Completed", completed)
    with col3:
        avg_duration = sum(c.get('duration', 0) for c in calls) / len(calls) if calls else 0
        st.metric("Avg Duration", f"{avg_duration:.1f}s")
    with col4:
        total_cost = sum(c.get('cost', 0) for c in calls)
        st.metric("Total Cost", f"${total_cost:.2f}")
    
    # Call list
    st.divider()
    for call in calls[:10]:
        with st.expander(f"Call {call.get('id', 'Unknown')[:8]}... - {format_timestamp(call.get('createdAt', ''))}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Status:** {call.get('status', 'Unknown')}")
                st.write(f"**Duration:** {call.get('duration', 0)} seconds")
                st.write(f"**Cost:** ${call.get('cost', 0):.4f}")
            with col2:
                st.write(f"**Type:** {call.get('type', 'Unknown')}")
                st.write(f"**Started:** {format_timestamp(call.get('startedAt', 'N/A'))}")
                st.write(f"**Ended:** {format_timestamp(call.get('endedAt', 'N/A'))}")

def render_create_assistant():
    """Renders form to create a new assistant."""
    st.subheader("➕ Create New Assistant")
    
    with st.form("create_assistant_form"):
        name = st.text_input("Assistant Name", placeholder="My New Agent")
        
        model = st.selectbox("Model", ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'])
        
        system_prompt = st.text_area(
            "System Prompt",
            placeholder="You are a helpful AI assistant...",
            height=200
        )
        
        voice_provider = st.selectbox("Voice Provider", ['playht', 'elevenlabs'])
        voice_id = st.text_input("Voice ID", value="andrew")
        
        first_message = st.text_input("First Message", placeholder="Hello! How can I help you today?")
        
        submitted = st.form_submit_button("Create Assistant", type="primary")
        
        if submitted:
            if not name or not system_prompt:
                st.error("Please provide at least a name and system prompt.")
                return
            
            payload = {
                'name': name,
                'model': {
                    'model': model,
                    'messages': [
                        {'role': 'system', 'content': system_prompt}
                    ]
                },
                'voice': {
                    'provider': voice_provider,
                    'voiceId': voice_id
                }
            }
            
            if first_message:
                payload['firstMessage'] = first_message
            
            with st.spinner("Creating assistant..."):
                result = create_assistant(payload)
                if result:
                    st.success(f"✅ Created assistant: {result.get('id')}")
                    list_assistants.clear()
                    time.sleep(1)
                    st.rerun()

# --- Main App ---

def main():
    st.set_page_config(
        page_title="Vapi Agent Control Center",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .stButton button {
        width: 100%;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🎯 Vapi Agent Control Center")
    st.markdown("Advanced configuration and management for your Vapi AI assistants")

    # Sidebar Navigation
    with st.sidebar:
        st.header("Navigation")
        
        page = st.radio(
            "Select View",
            ["📝 Edit Assistant", "➕ Create Assistant", "📊 Analytics", "📞 Phone Numbers", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Agent Selection
        if page in ["📝 Edit Assistant", "📊 Analytics"]:
            assistants = list_assistants()
            
            if assistants:
                assistant_map = {f"{a.get('name', 'Unnamed')} ({a['id'][:8]}...)": a['id'] for a in assistants}
                agent_names = list(assistant_map.keys())
                
                selected_agent_name = st.selectbox("Select Agent", agent_names)
                
                if selected_agent_name:
                    assistant_id = assistant_map[selected_agent_name]
                    st.info(f"**ID:** `{assistant_id[:16]}...`")
                    
                    if 'selected_agent_id' not in st.session_state or st.session_state.selected_agent_id != assistant_id:
                        st.session_state.selected_agent_id = assistant_id
                        st.session_state.current_config = None

                    if st.button("🔄 Load Configuration", use_container_width=True):
                        with st.spinner("Loading..."):
                            config = get_assistant_config(assistant_id)
                            if config:
                                st.session_state.current_config = config
                                st.session_state.selected_agent_name = selected_agent_name
                                st.rerun()
                    
                    if st.button("🗑️ Delete Assistant", use_container_width=True):
                        if st.session_state.get('confirm_delete'):
                            if delete_assistant(assistant_id):
                                st.success("Deleted!")
                                list_assistants.clear()
                                st.session_state.current_config = None
                                time.sleep(1)
                                st.rerun()
                            st.session_state.confirm_delete = False
                        else:
                            st.session_state.confirm_delete = True
                            st.warning("Click again to confirm deletion")
        
        st.divider()
        st.caption("Vapi Agent Control Center v2.0")

    # Main Content Area
    if page == "📝 Edit Assistant":
        if 'current_config' in st.session_state and st.session_state.current_config:
            config = st.session_state.current_config
            
            # Header with metadata
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.header(f"Editing: {config.get('name', 'Unnamed Agent')}")
            with col2:
                st.metric("Created", format_timestamp(config.get('createdAt', 'N/A')))
            with col3:
                st.metric("Updated", format_timestamp(config.get('updatedAt', 'N/A')))
            
            st.divider()
            
            # Tabs for different sections
            tab1, tab2, tab3 = st.tabs(["⚙️ Configuration", "📊 Analytics", "🔍 Raw JSON"])
            
            with tab1:
                render_assistant_editor(config, st.session_state.selected_agent_id)
            
            with tab2:
                render_call_analytics(st.session_state.selected_agent_id)
            
            with tab3:
                st.subheader("Full Configuration (Read-Only)")
                st.json(config)
                
                if st.button("📋 Copy to Clipboard"):
                    st.code(json.dumps(config, indent=2), language='json')
        else:
            st.info("👈 Select an agent from the sidebar and click 'Load Configuration'")
    
    elif page == "➕ Create Assistant":
        render_create_assistant()
    
    elif page == "📊 Analytics":
        st.header("📊 Analytics Dashboard")
        
        if 'selected_agent_id' in st.session_state:
            render_call_analytics(st.session_state.selected_agent_id)
        else:
            st.info("Select an agent from the sidebar to view analytics")
    
    elif page == "📞 Phone Numbers":
        st.header("📞 Phone Number Management")
        
        phone_numbers = list_phone_numbers()
        
        if phone_numbers:
            for phone in phone_numbers:
                with st.expander(f"{phone.get('number', 'Unknown')} - {phone.get('provider', 'N/A')}"):
                    st.json(phone)
        else:
            st.info("No phone numbers configured")
    
    elif page == "⚙️ Settings":
        st.header("⚙️ Settings")
        
        st.subheader("API Configuration")
        st.info("API key is configured in Streamlit secrets")
        
        st.subheader("Cache Management")
        if st.button("Clear Assistant Cache"):
            list_assistants.clear()
            st.success("Cache cleared!")
        
        st.subheader("About")
        st.markdown("""
        **Vapi Agent Control Center** provides advanced management capabilities for your Vapi assistants:
        
        - ✏️ Full assistant configuration editing
        - 📊 Real-time call analytics
        - ➕ Create new assistants
        - 🗑️ Delete assistants
        - 📞 Phone number management
        - 🔍 Raw JSON inspection
        
        Version: 2.0.0
        """)

if __name__ == "__main__":
    main()

