import streamlit as st
import requests
import json
from datetime import datetime
import time
import pandas as pd

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
def list_assistants(limit=100):
    """Fetches the list of all assistants from the Vapi API."""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{VAPI_BASE_URL}/assistant"
    params = {"limit": limit}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
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
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            st.error(f"❌ Assistant not found (404). The ID '{assistant_id}' may be invalid or deleted.")
        else:
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
        response = requests.patch(url, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status()
        st.success(f"✅ Successfully updated agent {assistant_id[:12]}...")
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
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error creating assistant: {e.response.status_code} - {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating assistant: {e}")
        return None

def clone_assistant(assistant_id, new_name=None):
    """Clones an existing assistant with a new name."""
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
        response = requests.delete(url, headers=headers, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error deleting assistant: {e.response.status_code} - {e.response.text}")
        return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting assistant: {e}")
        return False

# --- Call Management ---
def list_calls(assistant_id=None, limit=50):
    """Fetches recent calls, optionally filtered by assistant."""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{VAPI_BASE_URL}/call"
    params = {"limit": limit}
    if assistant_id:
        params["assistantId"] = assistant_id
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
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
        response = requests.get(url, headers=headers, timeout=10)
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
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching phone numbers: {e}")
        return []

def update_phone_number(phone_id, payload):
    """Updates a phone number configuration."""
    headers = get_headers()
    if not headers:
        return False
    
    url = f"{VAPI_BASE_URL}/phone-number/{phone_id}"
    
    try:
        response = requests.patch(url, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating phone number: {e}")
        return False

# --- Squad Management ---
def list_squads():
    """Fetches all squads (assistant groups)."""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{VAPI_BASE_URL}/squad"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching squads: {e}")
        return []

def create_squad(payload):
    """Creates a new squad."""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{VAPI_BASE_URL}/squad"
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating squad: {e}")
        return None

# --- Tool/Function Management ---
def list_tools():
    """Fetches all custom tools/functions."""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{VAPI_BASE_URL}/tool"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching tools: {e}")
        return []

def create_tool(payload):
    """Creates a new tool."""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{VAPI_BASE_URL}/tool"
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating tool: {e}")
        return None

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

def get_agent_list():
    """Fetches only valid agents from the Vapi API, avoiding hardcoded invalid IDs."""
    fetched_agents = list_assistants(limit=200)
    
    if not fetched_agents:
        st.warning("Could not fetch any assistants. Please check your API key and network connection.")
        return {}
    
    combined_agents = {}
    for agent in fetched_agents:
        name = agent.get('name', 'Unnamed Agent')
        combined_agents[name] = {
            "id": agent['id'],
            "live": True,
            "createdAt": agent.get('createdAt', 'N/A')
        }
    
    return combined_agents

# --- Streamlit UI Functions ---
def main():
    st.set_page_config(
        page_title="Vapi Agent Configuration Editor",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Vapi Agent Configuration Editor")
    st.markdown("Use this comprehensive tool to manage your Vapi assistants, phone numbers, and calls.")
    
    # --- Sidebar Navigation ---
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Assistant Editor", "Phone Number Manager", "Call Logs", "Squads & Tools"])
    st.sidebar.divider()
    
    if page == "Assistant Editor":
        assistant_editor_page()
    elif page == "Phone Number Manager":
        phone_number_manager_page()
    elif page == "Call Logs":
        call_logs_page()
    elif page == "Squads & Tools":
        squads_tools_page()

def assistant_editor_page():
    st.header("Assistant Editor")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.subheader("Select an Assistant")
    with col2:
        if st.button("Refresh", key="refresh_agents"):
            st.session_state.clear()
            st.rerun()
    
    # --- Agent Selection ---
    combined_agents = get_agent_list()
    
    if not combined_agents:
        st.error("No assistants found. Please check your Vapi API credentials and try again.")
        return
    
    agent_names = list(combined_agents.keys())
    selected_agent_name = st.sidebar.selectbox("Select Agent to Edit", agent_names)
    
    if selected_agent_name:
        assistant_id = combined_agents[selected_agent_name]['id']
        
        st.sidebar.info(f"**Assistant ID:** `{assistant_id}`")
        
        # Clear config if a new agent is selected
        if 'selected_agent_id' not in st.session_state or st.session_state.selected_agent_id != assistant_id:
            st.session_state.current_config = None
            st.session_state.selected_agent_id = assistant_id
        
        if st.sidebar.button("Load Agent Configuration", use_container_width=True):
            with st.spinner(f"Fetching configuration for {selected_agent_name}..."):
                config = get_assistant_config(assistant_id)
                if config:
                    st.session_state.current_config = config
                    st.session_state.selected_agent_name = selected_agent_name
                    st.success("Configuration loaded successfully!")
                else:
                    st.session_state.current_config = None
        
        st.sidebar.divider()
        
        # --- Configuration Editor Main Content ---
        if 'current_config' in st.session_state and st.session_state.current_config:
            config = st.session_state.current_config
            
            st.subheader(f"Editing: {st.session_state.selected_agent_name}")
            
            # Extract fields for editing
            current_name = config.get('name', st.session_state.selected_agent_name)
            current_first_message = config.get('firstMessage', '')
            current_background_sound = config.get('backgroundSound', 'office')
            current_background_deniese = config.get('backgroundDenoisingEnabled', False)
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
            current_max_tokens = min(model_config.get('maxTokens', 1024), 4000)  # Cap at 4000
            
            voice_config = config.get('voice', {})
            current_voice_provider = voice_config.get('provider', 'playht')
            current_voice_id = voice_config.get('voiceId', 'andrew')
            
            transcriber_config = config.get('transcriber', {})
            current_transcriber_provider = transcriber_config.get('provider', 'deepgram')
            current_transcriber_model = transcriber_config.get('model', 'base')
            current_transcriber_language = transcriber_config.get('language', 'en')
            
            with st.form("agent_editor_form"):
                # --- General Settings ---
                st.subheader("General Settings")
                col1, col2 = st.columns(2)
                with col1:
                    new_name = st.text_input("Agent Name", value=current_name, max_chars=40)
                with col2:
                    new_server_url = st.text_input("Server URL", value=current_server_url,
                                                   help="Your backend server URL for webhooks")
                
                new_server_secret = st.text_input("Server Secret", value=current_server_secret,
                                                  type="password", help="Secret key for webhook authentication")
                
                # --- Call Experience ---
                st.subheader("Call Experience")
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_background_sound = st.text_input(
                        "Background Sound",
                        value=current_background_sound,
                        help="e.g., 'office', 'off', or a URL to an audio file."
                    )
                with col2:
                    new_silence_timeout = st.number_input(
                        "Silence Timeout (seconds)",
                        5, 300, current_silence_timeout, 5,
                        help="How long to wait before ending call due to silence"
                    )
                with col3:
                    new_background_denoise = st.checkbox("Background Denoising", value=current_background_deniese)
                
                st.divider()
                
                # --- Messages ---
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
                
                # --- Model Configuration ---
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
                    new_max_tokens = st.number_input("Max Tokens", 50, 4000, current_max_tokens, 50)
                
                st.divider()
                
                # --- Transcriber Configuration ---
                st.subheader("Transcriber Settings")
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_transcriber_provider = st.selectbox(
                        "Provider",
                        options=['deepgram', 'talkscriber'],
                        index=['deepgram', 'talkscriber'].index(current_transcriber_provider) if current_transcriber_provider in ['deepgram', 'talkscriber'] else 0
                    )
                with col2:
                    new_transcriber_model = st.text_input("Model", value=current_transcriber_model)
                with col3:
                    new_transcriber_language = st.text_input("Language", value=current_transcriber_language)
                
                st.divider()
                
                # --- Voice Configuration ---
                st.subheader("Voice Settings")
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_voice_provider = st.selectbox(
                        "Voice Provider",
                        options=['playht', 'elevenlabs', 'azure', 'rime-ai', 'deepgram'],
                        index=['playht', 'elevenlabs', 'azure', 'rime-ai', 'deepgram'].index(current_voice_provider) if current_voice_provider in ['playht', 'elevenlabs', 'azure', 'rime-ai', 'deepgram'] else 0
                    )
                with col2:
                    new_voice_id = st.text_input("Voice ID", value=current_voice_id, help="e.g., andrew, jennifer")
                with col3:
                    voice_speed = voice_config.get('speed', 1.0)
                    new_voice_speed = st.slider("Voice Speed", 0.5, 2.0, voice_speed, 0.1)
                
                st.divider()
                
                # --- Recording & Compliance ---
                st.subheader("Recording & Compliance")
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_record_enabled = st.checkbox("Enable Call Recording", value=current_record_enabled)
                with col2:
                    new_hipaa_enabled = st.checkbox("HIPAA Compliance Mode", value=current_hipaa_enabled)
                with col3:
                    st.caption("HIPAA mode affects data handling")
                
                # --- Timing Settings ---
                st.subheader("Timing & Duration")
                col1, col2 = st.columns(2)
                with col1:
                    new_max_duration = st.number_input(
                        "Max Call Duration (seconds)",
                        60, 3600, current_max_duration, 60,
                        help="Maximum duration for a call"
                    )
                
                # Submit buttons
                st.divider()
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    submitted = st.form_submit_button("Save All Changes", use_container_width=True, type="primary")
                with col2:
                    preview = st.form_submit_button("Preview", use_container_width=True)
                with col3:
                    export = st.form_submit_button("Export", use_container_width=True)
                with col4:
                    reset = st.form_submit_button("Reset", use_container_width=True)
                
                if submitted:
                    # 1. Build the payload
                    payload = {}
                    
                    # General
                    if new_name != current_name:
                        payload['name'] = new_name
                    if new_server_url != current_server_url:
                        payload['serverUrl'] = new_server_url
                    if new_server_secret != current_server_secret:
                        payload['serverSecret'] = new_server_secret
                    
                    # Call Experience
                    if new_background_sound != current_background_sound:
                        payload['backgroundSound'] = new_background_sound
                    if new_background_denoise != current_background_deniese:
                        payload['backgroundDenoisingEnabled'] = new_background_denoise
                    
                    # Messages
                    if new_first_message != current_first_message:
                        payload['firstMessage'] = new_first_message
                    if new_end_call_phrases != current_end_call_phrases:
                        payload['endCallPhrases'] = new_end_call_phrases
                    
                    # Model
                    model_payload = {}
                    if new_model != current_model:
                        model_payload['model'] = new_model
                    if new_temperature != current_temperature:
                        model_payload['temperature'] = new_temperature
                    if new_max_tokens != current_max_tokens:
                        model_payload['maxTokens'] = new_max_tokens
                    
                    # System Prompt Update
                    temp_config = json.loads(json.dumps(config))
                    set_system_prompt(temp_config, new_system_prompt)
                    if temp_config.get('model', {}).get('messages') != config.get('model', {}).get('messages'):
                        model_payload['messages'] = temp_config['model']['messages']
                    
                    if model_payload:
                        payload['model'] = model_payload
                    
                    # Transcriber
                    transcriber_payload = {}
                    if new_transcriber_provider != current_transcriber_provider:
                        transcriber_payload['provider'] = new_transcriber_provider
                    if new_transcriber_model != current_transcriber_model:
                        transcriber_payload['model'] = new_transcriber_model
                    if new_transcriber_language != current_transcriber_language:
                        transcriber_payload['language'] = new_transcriber_language
                    
                    if transcriber_payload:
                        payload['transcriber'] = transcriber_payload
                    
                    # Voice
                    voice_payload = {}
                    if new_voice_provider != current_voice_provider:
                        voice_payload['provider'] = new_voice_provider
                    if new_voice_id != current_voice_id:
                        voice_payload['voiceId'] = new_voice_id
                    if new_voice_speed != voice_config.get('speed', 1.0):
                        voice_payload['speed'] = new_voice_speed
                    
                    if voice_payload:
                        payload['voice'] = voice_payload
                    
                    # Recording & Compliance
                    if new_record_enabled != current_record_enabled:
                        payload['recordingEnabled'] = new_record_enabled
                    if new_hipaa_enabled != current_hipaa_enabled:
                        payload['hipaaEnabled'] = new_hipaa_enabled
                    
                    # Timing
                    if new_silence_timeout != current_silence_timeout:
                        payload['silenceTimeoutSeconds'] = new_silence_timeout
                    if new_max_duration != current_max_duration:
                        payload['maxDurationSeconds'] = new_max_duration
                    
                    if payload:
                        st.subheader("Payload to be sent:")
                        st.json(payload)
                        
                        # 2. Send the update
                        if update_assistant_config(st.session_state.selected_agent_id, payload):
                            # 3. Reload config to show latest changes
                            with st.spinner("Reloading configuration..."):
                                reloaded_config = get_assistant_config(st.session_state.selected_agent_id)
                                if reloaded_config:
                                    st.session_state.current_config = reloaded_config
                                    st.rerun()
                    else:
                        st.info("No changes detected. Nothing to save.")
                
                if preview:
                    st.subheader("Current Configuration Preview")
                    st.json(config)
                
                if export:
                    st.download_button(
                        label="Download Config JSON",
                        data=json.dumps(config, indent=2),
                        file_name=f"{assistant_id}_config.json",
                        mime="application/json"
                    )
                
                if reset:
                    st.session_state.current_config = None
                    st.rerun()
        else:
            st.info("Please select an agent and click 'Load Agent Configuration' to begin editing.")

def phone_number_manager_page():
    st.header("Phone Number Manager")
    
    phone_numbers = list_phone_numbers()
    if not phone_numbers:
        st.warning("No phone numbers found or API key is invalid.")
        return
    
    # Prepare data for display
    data = []
    for num in phone_numbers:
        data.append({
            "Number": num.get('number', 'N/A'),
            "ID": num.get('id', 'N/A'),
            "Assistant ID": num.get('assistantId', 'N/A'),
            "Provider": num.get('provider', 'N/A'),
            "Status": num.get('status', 'N/A')
        })
    
    st.dataframe(pd.DataFrame(data), use_container_width=True)
    
    st.subheader("Update Phone Number Assistant")
    phone_options = {f"{d['Number']} ({d['ID'][:8]}...)": d['ID'] for d in data}
    selected_phone_display = st.selectbox("Select Phone Number to Update", list(phone_options.keys()))
    
    if selected_phone_display:
        selected_phone_id = phone_options[selected_phone_display]
        
        combined_agents = get_agent_list()
        agent_options = {f"{name} ({details['id'][:8]}...)": details['id'] for name, details in combined_agents.items()}
        
        new_assistant_display = st.selectbox("Assign New Assistant", list(agent_options.keys()))
        
        if st.button("Assign Assistant to Phone Number", type="primary"):
            new_assistant_id = agent_options[new_assistant_display]
            payload = {"assistantId": new_assistant_id}
            
            if update_phone_number(selected_phone_id, payload):
                st.success(f"Successfully assigned {new_assistant_display} to {selected_phone_display}!")
                st.rerun()

def call_logs_page():
    st.header("Call Logs")
    
    combined_agents = get_agent_list()
    agent_options = {f"{name} ({details['id'][:8]}...)": details['id'] for name, details in combined_agents.items()}
    
    filter_agent_display = st.selectbox("Filter by Assistant", ["All Assistants"] + list(agent_options.keys()))
    filter_assistant_id = agent_options[filter_agent_display] if filter_agent_display != "All Assistants" else None
    
    if st.button("Fetch Call Logs", type="primary"):
        with st.spinner("Fetching call logs..."):
            calls = list_calls(assistant_id=filter_assistant_id, limit=100)
            
            if not calls:
                st.info("No calls found for the selected filter.")
                return
            
            # Prepare data for display
            data = []
            for call in calls:
                duration = call.get('duration', 0)
                duration_str = f"{duration // 60}m {duration % 60}s"
                
                data.append({
                    "ID": call.get('id', 'N/A'),
                    "Assistant": call.get('assistantId', 'N/A')[:8] + '...',
                    "From": call.get('customerNumber', 'N/A'),
                    "To": call.get('phoneNumber', 'N/A'),
                    "Duration": duration_str,
                    "Status": call.get('status', 'N/A'),
                    "Started At": datetime.fromisoformat(call['createdAt'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S') if 'createdAt' in call else 'N/A'
                })
            
            st.dataframe(pd.DataFrame(data), use_container_width=True)
            
            # Option to view full details of a call
            st.subheader("View Full Call Details")
            call_ids = [d['ID'] for d in data]
            selected_call_id = st.selectbox("Select Call ID", call_ids)
            
            if st.button("Get Full Details"):
                details = get_call_details(selected_call_id)
                if details:
                    st.json(details)

def squads_tools_page():
    st.header("Squads & Tools Manager")
    
    st.subheader("Squads (Assistant Groups)")
    squads = list_squads()
    if squads:
        squad_data = []
        for squad in squads:
            squad_data.append({
                "Name": squad.get('name', 'N/A'),
                "ID": squad.get('id', 'N/A'),
                "Assistant Count": len(squad.get('assistantIds', [])),
                "Routing Strategy": squad.get('routingStrategy', 'N/A')
            })
        st.dataframe(pd.DataFrame(squad_data), use_container_width=True)
    else:
        st.info("No squads found.")
    
    st.subheader("Custom Tools/Functions")
    tools = list_tools()
    if tools:
        tool_data = []
        for tool in tools:
            tool_data.append({
                "Name": tool.get('name', 'N/A'),
                "ID": tool.get('id', 'N/A'),
                "Type": tool.get('type', 'N/A'),
                "URL": tool.get('url', 'N/A')
            })
        st.dataframe(pd.DataFrame(tool_data), use_container_width=True)
    else:
        st.info("No custom tools found.")

if __name__ == "__main__":
    main()
