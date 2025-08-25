import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
import os

# --- Page Configuration ---
# Use a variable to set the layout, so we can change it dynamically
if 'layout' not in st.session_state:
    st.session_state.layout = 'wide'

st.set_page_config(
    page_title="Chrysalis PAT Simulator",
    page_icon="🦋",
    layout=st.session_state.layout,
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
    if not os.path.exists(path):
        st.warning(f"Video file not found at path: {path}")
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
    
    debrief_prompt = f"""
    As an expert in Psychedelic-Assisted Therapy (PAT) training, analyze the following transcript from the '{scenario_name}' scenario.
    Provide a concise, insightful "Debrief Report" in Markdown format with three sections:
    1.  **Key Moments**: Identify 2-3 pivotal moments.
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

    with st.expander("Full Transcript"):
        for msg in chat_history:
            role = "Facilitator" if msg['role'] == 'user' else "Client"
            st.write(f"**{role}**: {msg['parts'][0]}")

    if st.button("↩️ Return to Lobby"):
        st.session_state.scenario_active = False
        st.session_state.show_debrief = False
        st.session_state.messages = []
        st.session_state.scenario_name = ""
        st.session_state.layout = 'wide' # Reset layout for lobby
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
    else:
        st.info("No active session. Please select a scenario from the lobby.")

# --- Main Content Router ---
if st.session_state.show_debrief:
    generate_debrief_report(st.session_state.messages, st.session_state.scenario_name)

elif st.session_state.scenario_active:
    if st.session_state.layout != 'centered':
        st.session_state.layout = 'centered'
        st.rerun()

    st.success(f"**Active Scenario**: {st.session_state.scenario_name}")

    # Display chat messages from history
    for message in st.session_state.messages:
        role = "assistant" if message['role'] == 'model' else message['role']
        with st.chat_message(role):
            st.markdown(message['parts'][0])

    # The "End Session" button, now in the main view
    if st.button("End Session & Begin Debrief", type="primary"):
        st.session_state.show_debrief = True
        st.rerun()

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

else: # This is the LOBBY screen
    if st.session_state.layout != 'wide':
        st.session_state.layout = 'wide'
        st.rerun()
        
    st.info("Welcome! Please select a scenario to begin your training.")
    st.divider()

    scenarios = {
        "David": {"title": "Intense Experience", "desc": "David wants to stop a 'dark' session.", "video": "assets/scenario1-new-video.mp4", "prompt": "You are David..."},
        "Alex": {"title": "Integration Session", "desc": "Alex feels embarrassed about requesting a hug.", "video": "assets/scenario2a-new-video.mp4", "prompt": "You are Alex..."},
        "Bruce": {"title": "Managing Expectations", "desc": "Bruce expects psychedelics to instantly 'cure' him.", "video": "assets/scenario3c-new-video.mp4", "prompt": "You are Bruce..."}
    }

    cols = st.columns(len(scenarios))
    for i, (client, data) in enumerate(scenarios.items()):
        with cols[i]:
            with st.container(border=True):
                st.subheader(client)
                st.caption(data["title"])
                
                video_html = f"""<video autoplay loop muted playsinline width="100%"><source src="data:video/mp4;base64,{get_video_b64(data['video'])}" type="video/mp4"></video>"""
                st.markdown(video_html, unsafe_allow_html=True)
                
                st.write(data["desc"])
                if st.button(f"Begin with {client}", key=client, use_container_width=True):
                    st.session_state.scenario_active = True
                    st.session_state.scenario_name = f"{client}: {data['title']}"
                    st.session_state.chat = model.start_chat(history=[])
                    with st.spinner("Client is preparing..."):
                        response = st.session_state.chat.send_message(data["prompt"])
                        st.session_state.messages.append({"role": "model", "parts": [response.text]})
                    st.rerun()
