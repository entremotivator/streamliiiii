import streamlit as st
import requests
import json

# --- Vapi API Client Functions ---

VAPI_BASE_URL = "https://api.vapi.ai/assistant"

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

@st.cache_data(ttl=3600) # Cache the list for 1 hour
def list_assistants():
    """Fetches the list of all assistants from the Vapi API."""
    headers = get_headers()
    if not headers:
        return []
    
    url = VAPI_BASE_URL
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        # The API returns a list of assistant objects
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error listing assistants: {e.response.status_code} - {e.response.text}")
        st.warning("This usually means your API key is invalid or has insufficient permissions.")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error listing assistants: {e}")
        return []

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
        st.warning("The selected Assistant ID might be invalid or deleted.")
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
        # System prompt is the first message with role 'system'
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
    
    # 1. Fetch the list of assistants from the Vapi API
    assistants = list_assistants()
    
    if not assistants:
        st.error("Could not load any Vapi assistants. Please check your API key and network connection.")
        return

    # Create a dictionary for easy lookup: {name: id}
    assistant_map = {f"{a.get('name', 'Unnamed Agent')} ({a['id'][:8]}...)": a['id'] for a in assistants}
    agent_names = list(assistant_map.keys())
    
    selected_agent_name = st.sidebar.selectbox("Select Agent to Edit", agent_names)
    
    if selected_agent_name:
        assistant_id = assistant_map[selected_agent_name]
        st.sidebar.info(f"**Assistant ID:** `{assistant_id}`")
        
        # Clear config if a new agent is selected
        if 'selected_agent_id' in st.session_state and st.session_state.selected_agent_id != assistant_id:
            st.session_state.current_config = None
            st.session_state.selected_agent_id = assistant_id
        elif 'selected_agent_id' not in st.session_state:
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

    # --- Configuration Editor ---
    if 'current_config' in st.session_state and st.session_state.current_config:
        config = st.session_state.current_config
        
        st.header(f"Editing: {st.session_state.selected_agent_name}")
        st.subheader("Core Settings")
        
        # Extract fields for editing
        current_name = config.get('name', st.session_state.selected_agent_name.split(' (')[0])
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
                    if update_assistant_config(st.session_state.selected_agent_id, payload):
                        # 3. Reload config to show latest changes
                        with st.spinner("Reloading configuration..."):
                            # Clear cache to force a fresh list load if the name changed
                            list_assistants.clear()
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

