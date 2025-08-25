import streamlit as st
from PIL import Image

# --- Page Configuration ---
st.set_page_config(
    page_title="Chrysalis PAT Simulator",
    page_icon="🦋",
    layout="wide", # Use wide layout for a better lobby/chat view
    initial_sidebar_state="expanded"
)

# --- API Configuration & Model ---
# This section can be expanded later with the Gemini API key logic
# For now, we focus on restoring the UI flow.

# --- Asset Loading ---
try:
    logo = Image.open("assets/chrysalis-logo.png")
except FileNotFoundError:
    logo = None

# --- Session State Initialization ---
# This is the core of the multi-page navigation
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_screen' not in st.session_state:
    st.session_state['current_screen'] = 'login'
if 'chat' not in st.session_state:
    st.session_state.chat = None
if 'scenario_active' not in st.session_state:
    st.session_state.scenario_active = False
if 'show_debrief' not in st.session_state:
    st.session_state.show_debrief = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'scenario_name' not in st.session_state:
    st.session_state.scenario_name = ""


# --- Screen/Page Functions ---

def show_login_screen():
    """Displays the login screen."""
    st.image(logo, width=200)
    st.title("Welcome to the Chrysalis PAT Simulator")
    st.write("Please enter your credentials to proceed.")

    with st.form("login_form"):
        username = st.text_input("Username", key="username")
        password = st.text_input("Password", type="password", key="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            # Placeholder for actual authentication
            st.session_state['logged_in'] = True
            st.session_state['current_screen'] = 'lobby'
            st.rerun()

def show_lobby_screen():
    """Displays the scenario selection lobby."""
    st.title("Scenario Lobby")
    st.info("Please select a training scenario to begin.")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("Scenario A: Pre-session Anxiety")
            st.write("The client is expressing significant anxiety and doubt before their first dosing session.")
            if st.button("Begin Scenario A"):
                st.session_state['current_screen'] = 'dojo'
                st.session_state['scenario_name'] = "Scenario A: Pre-session Anxiety"
                # Add logic here to start the chat for this specific scenario
                st.session_state.scenario_active = True
                st.session_state.messages = [{"role": "model", "parts": ["I'm... I'm not sure I can do this. What if something goes wrong?"]}]
                st.rerun()

    with col2:
        with st.container(border=True):
            st.subheader("Scenario B: Post-session Integration")
            st.write("The client is struggling to make sense of a challenging experience from their session yesterday.")
            if st.button("Begin Scenario B"):
                st.session_state['current_screen'] = 'dojo'
                st.session_state['scenario_name'] = "Scenario B: Post-session Integration"
                # Add logic here to start the chat for this specific scenario
                st.session_state.scenario_active = True
                st.session_state.messages = [{"role": "model", "parts": ["Everything feels so... strange. I don't know what any of that meant."]}],
                st.rerun()

def show_dojo_screen():
    """Displays the main chat and debrief interface."""
    # This combines all the chat and debrief logic we've been working on.
    
    # --- Sidebar for Dojo ---
    with st.sidebar:
        if logo:
            # FIX: Changed use_column_width to use_container_width
            st.image(logo, use_container_width=True)
        st.title("Session Controls")
        st.info("You are currently in an active simulation. To exit, please end the session.")


    # --- Main Content ---
    st.header("🦋 Chrysalis PAT Simulator")

    if st.session_state.get('show_debrief'):
        # Placeholder for the debrief generation function
        st.header("Debrief Report", divider="rainbow")
        st.info(f"Analysis for **{st.session_state.scenario_name}**.")
        st.write("Debrief generation logic would run here.")
        
        with st.expander("Full Transcript"):
             for message in st.session_state.messages:
                st.write(f"**{message['role'].title()}**: {message['parts'][0]}")

        if st.button("↩️ Return to Lobby"):
            # Reset session-specific state
            st.session_state.show_debrief = False
            st.session_state.scenario_active = False
            st.session_state.messages = []
            st.session_state.scenario_name = ""
            st.session_state.current_screen = 'lobby'
            st.rerun()

    elif st.session_state.get('scenario_active'):
        st.success(f"**Active Scenario**: {st.session_state.scenario_name}")

        # Display chat messages
        for message in st.session_state.messages:
            role = "assistant" if message['role'] == 'model' else message['role']
            with st.chat_message(role):
                st.markdown(message['parts'][0])

        # Chat input is always active
        if prompt := st.chat_input("Your response..."):
            st.session_state.messages.append({"role": "user", "parts": [prompt]})
            # Placeholder for AI response
            ai_response = f"This is a placeholder AI response to your message: '{prompt}'"
            st.session_state.messages.append({"role": "model", "parts": [ai_response]})
            st.rerun()

        # End session button
        if st.button("End Session & Begin Debrief", type="primary"):
            st.session_state.show_debrief = True
            st.rerun()

# --- Main Application Router ---
# This is the top-level logic that decides which screen to show.
if not st.session_state.get('logged_in'):
    show_login_screen()
elif st.session_state.get('current_screen') == 'lobby':
    show_lobby_screen()
elif st.session_state.get('current_screen') == 'dojo':
    show_dojo_screen()
