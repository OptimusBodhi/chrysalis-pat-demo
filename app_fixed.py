import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Chrysalis PAT Simulator",
    page_icon="🦋",
    layout="wide", # Use wide layout for the lobby
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

# --- Helper Function for Videos ---
def get_video_b64(path: str):
    """Reads a video file and returns its base64 encoded string."""
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        video_bytes = f.read()
    return base64.b64encode(video_bytes).decode()

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

    st.write("Debrief generation would occur here.")
    with st.expander("Full Transcript"):
        for msg in chat_history:
            st.write(f"**{msg['role'].replace('model', 'Client').title()}**: {msg['parts'][0]}")

    if st.button("↩️ Return to Lobby"):
        # Reset only session-specific state
        st.session_state.scenario_active = False
        st.session_state.show_debrief = False
        st.session_state.messages = []
        st.session_state.scenario_name = ""
        st.rerun()

# --- Main Application ---

st.title("🦋 Chrysalis PAT Simulator")

# --- Sidebar ---
with st.sidebar:
    if logo:
        st.image(logo, use_container_width=True)
    st.header("Session Status")

    if st.session_state.scenario_active:
        st.info(f"Scenario in progress:\n**{st.session_state.scenario_name}**")
        if st.button("End Session & Begin Debrief", type="primary"):
            st.session_state.show_debrief = True
            st.rerun()
    else:
        st.info("No active session. Please select a scenario from the lobby.")


# --- Main Content Router ---
if st.session_state.show_debrief:
    generate_debrief_report(st.session_state.messages, st.session_state.scenario_name)

elif st.session_state.scenario_active:
    st.set_page_config(layout="centered") # Switch to centered layout for chat
    st.success(f"**Active Scenario**: {st.session_state.scenario_name}")

    # Display chat messages
    for message in st.session_state.messages:
        role = "assistant" if message['role'] == 'model' else message['role']
        with st.chat_message(role):
            st.markdown(message['parts'][0])

    # Chat input
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

else: # This is the LOBBY screen
    st.info("Welcome! Please select a scenario to begin your training.")
    st.divider()

    scenarios = {
        "David": {
            "title": "Intense Experience (Dosing)",
            "description": "David, a 50yo male, is 80min post-dose and wants to stop due to creepy/dark feelings.",
            "video_path": "assets/scenario1-new-video.mp4",
            "initial_prompt": "You are David, a client in a PAT dosing session. Begin by expressing that you feel overwhelmed and want the experience to stop."
        },
        "Alex": {
            "title": "Integration Session - Touch",
            "description": "Alex is in an integration session and feels embarrassed about requesting a hug yesterday.",
            "video_path": "assets/scenario2a-new-video.mp4",
            "initial_prompt": "You are Alex, in a PAT integration session. Begin by awkwardly mentioning you feel embarrassed about asking for a hug during yesterday's session."
        },
        "Bruce": {
            "title": "Preparation - Expectations",
            "description": "Bruce, a 55yo male, expects psychedelics to instantly 'cure' his lifelong depression.",
            "video_path": "assets/scenario3c-new-video.mp4",
            "initial_prompt": "You are Bruce, in a PAT preparation session. Begin by expressing extreme optimism that this one session will finally cure your depression."
        }
    }

    cols = st.columns(len(scenarios))

    for i, (client_name, data) in enumerate(scenarios.items()):
        with cols[i]:
            with st.container(border=True):
                st.subheader(client_name)
                st.caption(data["title"])

                video_b64 = get_video_b64(data["video_path"])
                if video_b64:
                    # Streamlit's st.video expects a file path, URL, or bytes, not base64 string directly
                    # We need to write the bytes to a temporary file or pass bytes directly if possible
                    # For simplicity, we will just use the path
                    st.video(data["video_path"])
                else:
                    st.warning(f"Video not found: {data['video_path']}")

                st.write(data["description"])

                if st.button(f"Begin Scenario with {client_name}", key=f"begin_{client_name}", use_container_width=True):
                    st.session_state.scenario_active = True
                    st.session_state.scenario_name = f"{client_name}: {data['title']}"
                    st.session_state.chat = model.start_chat(history=[])

                    with st.spinner("Client is preparing..."):
                        response = st.session_state.chat.send_message(data["initial_prompt"])
                        st.session_state.messages.append({"role": "model", "parts": [response.text]})
                    st.rerun()
