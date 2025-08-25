import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- Page Configuration ---
st.set_page_config(
    page_title="Chrysalis PAT Simulator",
    page_icon="🦋",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- API Configuration ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🚨 Error: `GEMINI_API_KEY` is not set in Streamlit Secrets.", icon="🔑")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# --- Asset Loading ---
try:
    logo = Image.open("assets/chrysalis-logo.png")
except FileNotFoundError:
    logo = None

# --- Session State Initialization ---
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


# --- Debrief Function ---
def generate_debrief_report(chat_history, scenario_name):
    st.header("Debrief Report", divider="rainbow")
    st.info(f"Analysis for: **{scenario_name}**")
    
    # This is a placeholder for the full debrief logic.
    st.write("Debrief generation would occur here.")
    with st.expander("Full Transcript"):
        for msg in chat_history:
            st.write(f"**{msg['role'].replace('model', 'Client').title()}**: {msg['parts'][0]}")

    if st.button("↩️ Start a New Session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# --- Main Application ---

st.title("🦋 Chrysalis PAT Simulator")

# --- Sidebar ---
with st.sidebar:
    if logo:
        st.image(logo, use_container_width=True) # Fix for deprecation warning
    st.header("Settings")

    if not st.session_state.scenario_active:
        scenario_choice = st.selectbox(
            "Choose a Client Scenario:",
            ("Select...", "Pre-session Anxiety", "Post-session Integration"),
            key="scenario_selector"
        )
        if scenario_choice != "Select..." and st.button(f"Begin Scenario"):
            st.session_state.scenario_active = True
            st.session_state.scenario_name = scenario_choice
            st.session_state.chat = model.start_chat(history=[])
            
            initial_prompt = f"Begin the conversation for a '{scenario_choice}' scenario."
            with st.spinner("Client is preparing..."):
                response = st.session_state.chat.send_message(initial_prompt)
                st.session_state.messages.append({"role": "model", "parts": [response.text]})
            st.rerun()
    else: # If a scenario IS active
        st.info(f"Scenario in progress:\n**{st.session_state.scenario_name}**")
        if st.button("End Session & Begin Debrief", type="primary"):
            st.session_state.show_debrief = True
            st.rerun()


# --- Main Content ---
if st.session_state.show_debrief:
    generate_debrief_report(st.session_state.messages, st.session_state.scenario_name)

elif st.session_state.scenario_active:
    # Display chat messages from history
    for message in st.session_state.messages:
        role = "assistant" if message['role'] == 'model' else message['role']
        with st.chat_message(role):
            st.markdown(message['parts'][0])

    # Chat input for user
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
    st.info("Welcome! Please select a scenario from the sidebar to begin.")
