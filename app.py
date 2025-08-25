import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Chrysalis PAT Simulator",
    page_icon="🦋",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- API Configuration ---
# Use a single, clear check for the API key.
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🚨 **Error**: `GEMINI_API_KEY` is not set in Streamlit Secrets.", icon="🔑")
    st.info("Please add your Gemini API key to your Streamlit secrets file.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro-latest')


# --- Asset Loading ---
try:
    logo = Image.open("assets/chrysalis-logo.png")
except FileNotFoundError:
    logo = None

# --- Debrief Generation Function ---
def generate_debrief_report(chat_history, scenario_name):
    """Generates a debrief report from the chat history."""
    st.header("Debrief Report", divider="rainbow")
    st.info(f"This report analyzes your interaction for **{scenario_name}**.", icon="📝")

    with st.expander("**Full Session Transcript**", expanded=False):
        for message in chat_history:
            role_icon = "🧑‍💻" if message['role'] == 'user' else "🤖"
            role_name = "Facilitator" if message['role'] == 'user' else "Client"
            st.markdown(f"**{role_icon} {role_name}**: {message['parts'][0]}")

    debrief_prompt = f"""
    As an expert in Psychedelic-Assisted Therapy (PAT) training, analyze the following facilitator-client conversation transcript.
    The session context was: '{scenario_name}'.

    Provide a concise, insightful "Debrief Report" in Markdown format with three sections:
    1.  **Key Moments**: Identify 2-3 pivotal moments. What made them significant?
    2.  **Areas for Improvement**: Suggest 1-2 specific areas for improvement with alternative phrasing.
    3.  **Strengths**: Highlight 1-2 things the facilitator did well.

    Transcript:
    ---
    {chat_history}
    ---
    """
    with st.spinner("Analyzing session and generating your report..."):
        try:
            response = model.generate_content(debrief_prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"An error occurred while generating the debrief: {e}")

    if st.button("↩️ Start a New Session"):
        # Clear all session state keys to reset the app
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# --- Initialize Session State ---
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


# --- Sidebar ---
with st.sidebar:
    if logo:
        st.image(logo, use_column_width=True)
    st.title("Settings")

    # This selectbox will be disabled once a scenario is active.
    scenario_choice = st.selectbox(
        "Choose a Client Scenario:",
        ("Select a scenario...", "Scenario A: Pre-session Anxiety", "Scenario B: Post-session Integration"),
        disabled=st.session_state.scenario_active,
        key="scenario_selectbox" # Add a key for stability
    )

    if scenario_choice != "Select a scenario..." and not st.session_state.scenario_active:
        if st.button(f"Begin {scenario_choice.split(':')[0]}"):
            st.session_state.scenario_active = True
            st.session_state.scenario_name = scenario_choice # Store the scenario name
            st.session_state.chat = model.start_chat(history=[])
            
            # Create a more robust initial message for the AI
            initial_prompt = f"You are a client in a psychedelic-assisted therapy setting. The context for our session is '{st.session_state.scenario_name}'. Please begin the conversation naturally from your perspective as the client."
            
            with st.spinner("Client is readying themselves..."):
                response = st.session_state.chat.send_message(initial_prompt)
                st.session_state.messages.append({"role": "model", "parts": [response.text]})
            st.rerun()


# --- Main Application Logic ---

st.header("🦋 Chrysalis PAT Simulator")

# If show_debrief is true, show the report and stop.
if st.session_state.show_debrief:
    generate_debrief_report(st.session_state.messages, st.session_state.scenario_name)

# If a scenario is active, show the chat interface.
elif st.session_state.scenario_active:
    st.success(f"**Active Scenario**: {st.session_state.scenario_name}")

    # Display chat messages
    for message in st.session_state.messages:
        role = "assistant" if message['role'] == 'model' else message['role']
        with st.chat_message(role):
            st.markdown(message['parts'][0])

    # End session button
    if st.button("End Session & Begin Debrief", type="primary"):
        st.session_state.show_debrief = True
        st.rerun() # Rerun to switch to the debrief view

    # Chat input
    if prompt := st.chat_input("Your response..."):
        # Append and display user message
        st.session_state.messages.append({"role": "user", "parts": [prompt]})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display model response
        with st.chat_message("assistant"):
            with st.spinner("Client is thinking..."):
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "parts": [response.text]})
        
        # NOTE: The problematic st.rerun() that was here has been REMOVED.
        # Streamlit automatically reruns the script after chat_input is used.

# If nothing is active, show the welcome screen.
else:
    st.info("Welcome to the Chrysalis PAT Simulator. Please select a scenario from the sidebar to begin.")
