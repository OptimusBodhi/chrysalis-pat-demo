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
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
except Exception as e:
    st.error("🚨 **Error**: Could not configure the Gemini API. Please ensure your `GEMINI_API_KEY` is set correctly in Streamlit Secrets.", icon="🔑")
    st.stop()


# --- Asset Loading ---
try:
    # Using the hyphenated filename 'chrysalis-logo.png'
    logo = Image.open("assets/chrysalis-logo.png")
except FileNotFoundError:
    st.warning("Warning: `assets/chrysalis-logo.png` not found. The logo will not be displayed.")
    logo = None

# --- Debrief Generation Function ---
def generate_debrief_report(chat_history):
    """Generates a debrief report from the chat history."""
    st.header("Debrief Report", divider="rainbow")
    st.info("This report analyzes your interaction with the simulated client.", icon="📝")

    with st.expander("**Full Session Transcript**", expanded=False):
        for message in chat_history:
            role_icon = "🧑‍💻" if message['role'] == 'user' else "🤖"
            st.markdown(f"**{role_icon} {message['role'].replace('model', 'Client').replace('user', 'Facilitator').title()}**: {message['parts'][0]}")

    debrief_prompt = f"""
    As an expert in Psychedelic-Assisted Therapy (PAT) training, analyze the following facilitator-client conversation transcript.
    Provide a concise, insightful "Debrief Report" in Markdown format.

    The report should have three sections:
    1.  **Key Moments**: Identify 2-3 pivotal moments in the conversation. What made them significant?
    2.  **Areas for Improvement**: Suggest 1-2 specific areas where the facilitator could have approached the situation differently. Provide alternative phrasing.
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
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()


# --- Main Application ---

# Initialize session state variables
if 'chat' not in st.session_state:
    st.session_state.chat = None
if 'scenario_active' not in st.session_state:
    st.session_state.scenario_active = False
if 'show_debrief' not in st.session_state:
    st.session_state.show_debrief = False
if 'messages' not in st.session_state:
    st.session_state.messages = []


# --- Sidebar ---
with st.sidebar:
    if logo:
        st.image(logo, use_column_width=True)
    st.title("Settings")
    st.info("Select a client scenario to begin the simulation.")

    scenario = st.selectbox(
        "Choose a Client Scenario:",
        ("Select a scenario...", "Scenario A: Pre-session Anxiety", "Scenario B: Post-session Integration"),
        disabled=st.session_state.scenario_active
    )

    if scenario != "Select a scenario..." and not st.session_state.scenario_active:
        if st.button(f"Begin {scenario.split(':')[0]}"):
            st.session_state.scenario_active = True
            st.session_state.chat = model.start_chat(history=[])
            initial_message = f"You are a client in a psychedelic-assisted therapy setting. You are currently in '{scenario}'. Start the conversation naturally based on this context."
            response = st.session_state.chat.send_message(initial_message)
            st.session_state.messages.append({"role": "model", "parts": [response.text]})
            st.rerun()


# --- Main Content Area ---

st.header("🦋 Chrysalis PAT Simulator")

if st.session_state.get('show_debrief'):
    generate_debrief_report(st.session_state.messages)
else:
    if st.session_state.scenario_active:
        st.success(f"**Active Scenario**: {scenario}")

        # --- Chat History Container ---
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                role = "user" if message['role'] == 'user' else "assistant"
                with st.chat_message(role):
                    st.markdown(message['parts'][0])

        # --- Button and Input Area ---
        st.markdown("---") # Visual separator
        if st.button("End Session & Begin Debrief", type="primary"):
            st.session_state['show_debrief'] = True
            st.session_state['scenario_active'] = False
            st.rerun()

        if prompt := st.chat_input("Your response..."):
            st.session_state.messages.append({"role": "user", "parts": [prompt]})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Client is thinking..."):
                    response = st.session_state.chat.send_message(prompt)
                    st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "parts": [response.text]})
            st.rerun()

    else:
        st.info("Welcome to the Chrysalis PAT Simulator. Please select a scenario from the sidebar to begin.")
