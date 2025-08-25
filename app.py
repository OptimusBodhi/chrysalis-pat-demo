import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Chrysalis PAT Simulator",
    page_icon="🦋",
    layout="wide",
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
def get_video_html(path: str):
    if not os.path.exists(path):
        return f"<p>Video not found: {path}</p>"
    with open(path, "rb") as f:
        video_bytes = f.read()
    b64_video = base64.b64encode(video_bytes).decode()
    return f'<video autoplay loop muted playsinline width="100%"><source src="data:video/mp4;base64,{b64_video}" type="video/mp4"></video>'

# --- Session State Initialization ---
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'current_screen' not in st.session_state:
        st.session_state['current_screen'] = 'login'
    if 'chat' not in st.session_state:
        st.session_state.chat = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'scenario_name' not in st.session_state:
        st.session_state.scenario_name = ""

# --- Screen Functions ---
def show_login_screen():
    st.image(logo, width=200)
    st.title("Chrysalis PAT Simulator")
    with st.form("login_form"):
        st.text_input("Username")
        st.text_input("Password", type="password")
        if st.form_submit_button("Login", use_container_width=True):
            st.session_state['logged_in'] = True
            st.session_state['current_screen'] = 'lobby'
            st.rerun()

def show_lobby_screen():
    with st.sidebar:
        st.image(logo, use_container_width=True)
        st.header("Status")
        st.info("No active session. Please select a scenario.")
    
    st.title("Scenario Lobby")
    st.info("Welcome! Please select a scenario to begin your training.")
    st.divider()

    scenarios = {
        "David": {
            "title": "Intense Experience (Dosing)",
            "description": "David, a 50yo male, is 80min post-dose and wants to stop due to creepy/dark feelings.",
            "video_path": "assets/scenario1-new-video.mp4",
            "system_prompt": "You are David, a client in a PAT dosing session. You feel overwhelmed, scared, and want the experience to stop. Your tone is anxious and desperate. Your opening line is: 'I can't... I can't do this anymore. You have to make it stop. It's too dark.'"
        },
        "Alex": {
            "title": "Integration Session - Touch",
            "description": "Alex is in an integration session and feels embarrassed about requesting a hug yesterday.",
            "video_path": "assets/scenario2a-new-video.mp4",
            "system_prompt": "You are Alex, in a PAT integration session. You feel awkward and embarrassed about asking for a hug during yesterday's session. Your tone is shy and hesitant. Your opening line is: 'So... about yesterday. I feel really weird about that hug thing. Was that... okay?'"
        },
        "Bruce": {
            "title": "Preparation - Expectations",
            "description": "Bruce, a 55yo male, expects psychedelics to instantly 'cure' his lifelong depression.",
            "video_path": "assets/scenario3c-new-video.mp4",
            "system_prompt": "You are Bruce, in a PAT preparation session. You are extremely optimistic, almost naively so, that this one session will finally cure your lifelong depression. Your tone is excited and expectant. Your opening line is: 'Doc, I am so ready for this. I really think this is it—the magic bullet that's going to fix everything.'"
        }
    }

    cols = st.columns(len(scenarios))
    for i, (client_name, data) in enumerate(scenarios.items()):
        with cols[i]:
            with st.container(border=True):
                st.subheader(client_name)
                st.caption(data["title"])
                st.markdown(get_video_html(data["video_path"]), unsafe_allow_html=True)
                st.write(data["description"])
                if st.button(f"Begin with {client_name}", key=client_name, use_container_width=True):
                    st.session_state.scenario_name = f"{client_name}: {data['title']}"
                    st.session_state.chat = model.start_chat(history=[{'role': 'user', 'parts': [data['system_prompt']]}])
                    response = st.session_state.chat.send_message("Please give me your opening line based on your persona.")
                    st.session_state.messages = [{"role": "model", "parts": [response.text]}]
                    st.session_state.current_screen = 'dojo'
                    st.rerun()

def show_dojo_screen():
    with st.sidebar:
        st.image(logo, use_container_width=True)
        st.header("Session Status")
        st.info(f"**Active Scenario**:\n{st.session_state.scenario_name}")

    st.title("Training Dojo")
    
    # Display chat messages
    for message in st.session_state.messages:
        role = "assistant" if message['role'] == 'model' else message['role']
        with st.chat_message(role):
            st.markdown(message['parts'][0])

    # --- FIX: Input and Button Area ---
    # Use columns to place the button next to the input field
    input_col, button_col = st.columns([4, 1])

    with input_col:
        prompt = st.chat_input("Your response...", key="chat_input")

    with button_col:
        # A bit of vertical space to align the button
        st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True) 
        if st.button("End Session", use_container_width=True, type="primary"):
            st.session_state.current_screen = 'debrief'
            st.rerun()

    if prompt:
        st.session_state.messages.append({"role": "user", "parts": [prompt]})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Client is thinking..."):
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "parts": [response.text]})
        st.rerun()

def show_debrief_screen():
    with st.sidebar:
        st.image(logo, use_container_width=True)
        st.header("Status")
        st.info("Debrief complete.")

    st.header("Debrief Report", divider="rainbow")
    st.info(f"Analysis for: **{st.session_state.scenario_name}**")
    
    st.write("Debrief analysis will be displayed here.")

    with st.expander("Full Transcript"):
        for msg in st.session_state.messages:
            role = "Facilitator" if msg['role'] == 'user' else "Client"
            st.write(f"**{role}**: {msg['parts'][0]}")

    if st.button("↩️ Return to Lobby", use_container_width=True):
        st.session_state.current_screen = 'lobby'
        st.session_state.messages = []
        st.session_state.chat = None
        st.session_state.scenario_name = ""
        st.rerun()

# --- Main Application Router ---
init_session_state()

if not st.session_state.logged_in:
    show_login_screen()
else:
    if st.session_state.current_screen == 'lobby':
        show_lobby_screen()
    elif st.session_state.current_screen == 'dojo':
        show_dojo_screen()
    elif st.session_state.current_screen == 'debrief':
        show_debrief_screen()
