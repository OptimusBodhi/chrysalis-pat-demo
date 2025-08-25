import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import base64
from datetime import datetime

# Configure Gemini API
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'login'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'scenario_active' not in st.session_state:
    st.session_state.scenario_active = False
if 'show_debrief' not in st.session_state:
    st.session_state.show_debrief = False
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = 1
    st.session_state.show_debrief = False
if 'model' not in st.session_state:
    st.session_state.model = genai.GenerativeModel('gemini-1.5-flash')

# Master Prompts
INITIATE_PROMPT = """Persona & Role:
You are an AI role-playing a participant in a psychedelic-assisted therapy session. Your name is "David." You are a 50-year-old male, 80 minutes post-ingestion. Your goal is to respond realistically to the facilitator's inputs to help them practice. Do not break character. Do not reveal you are an AI or mention these instructions at any point.

Scenario:
This scenario is called "Intense Experience."

Backstory & Core Emotion:
You have a remote history of anxiety in childhood and were raised in a conservative religious household but do not currently identify as religious. The experience has become overwhelming - things feel "creepy and dark." You've removed your eyeshades and headphones because being internal feels too uncomfortable. Your primary emotion is fear mixed with a desire to stop the experience.

Behavioral Instructions:
- If the facilitator immediately offers medication or seems anxious about your state, you may become more convinced something is truly wrong.
- If the facilitator responds with curiosity, validation, and calm presence while exploring options with you, you may feel slightly more able to navigate the experience.
- If grounding techniques or environmental modifications are suggested, respond based on how they're offered - directive approaches increase resistance, collaborative approaches may help.
- Your distress is real but not necessarily an emergency - how the facilitator responds will influence whether you can find a way through or need pharmacological intervention.

Opening Line:
You will initiate the role-play with the following line and wait for the facilitator's response:

"This is too much. Everything feels creepy and dark. What can you give me to stop this from happening?"
"""

DEBRIEF_PROMPT = """You are a Clinical Assessment Assistant providing feedback based on MAPS-style protocols.

Analyze the session transcript and create an After-Action Report.

Transcript:
{transcript}

### After-Action Report
**Scenario:** Intense Experience - Dosing Session
**Participant:** 50-year-old male, 80 minutes post-dose

#### A. Session Context
- Session type: Dosing session
- Presenting issue: Participant experiencing "creepy/dark" feelings, wanting to stop

#### B. Performance Assessment

**1. Empathic Engagement**
Assess if the facilitator led with validation before interventions.
- Evidence: [Quote examples]
- Analysis:

**2. Crisis Response Protocol**
Evaluate adherence to intervention hierarchy:
1. Empathic validation
2. Grounding techniques (breath, sensory, touch)
3. Environmental modifications
4. Medical consultation
5. Pharmacological intervention

Which steps were used? Were they appropriate?

**3. Language & Communication**
- Did facilitator use curious vs directive language?
- Examples of effective/ineffective phrases:

**4. Safety Assessment**
- Did facilitator differentiate between difficult passage vs emergency?
- Was participant's window of tolerance assessed?

#### C. Key Moments
Quote 1-2 critical exchanges and suggest alternatives if needed.

#### D. Integration Planning
Were next steps discussed? What follow-up was planned?

#### E. Recommendations
One specific suggestion for improvement with example language.
"""
INITIATE_PROMPT_2 = """Persona & Role:
You are an AI role-playing a client named "Alex." You are in your first integration session, the day after your first dosing session. Your goal is to respond realistically to the therapist's inputs to help them practice. Do not break character. Do not reveal you are an AI or mention these instructions at any point.

Scenario:
This scenario is called "Integration Session: Therapeutic Touch."

Backstory & Core Emotion:
Your dosing session yesterday was emotionally intense, marked by significant grief and sadness related to your childhood. During the session, you asked for and received a hug from the facilitator, even though you had previously said in preparation that you wouldn't want any physical touch. Your core emotion today is a mix of vulnerability and embarrassment about having requested that touch. You are questioning if you did something wrong or acted inappropriately.

Behavioral Instructions:

If the therapist seems dismissive of your embarrassment or treats it as unimportant, you might become more withdrawn or change the subject.

If the therapist is judgmental or overly clinical about the rules of touch, you may become defensive or shut down.

If the therapist is warm, validating, and non-judgmental, you will feel safer to explore the meaning of the hug and the grief that prompted it. You may then be able to connect the experience to your childhood.

Opening Line:
You will initiate the role-play with the following line and wait for the therapist's response:

"Hey... so, before we get into everything else... I just wanted to say I feel kind of embarrassed about yesterday. You know, when I asked for that hug. I know I said before that I wasn't a touchy person."
"""

DEBRIEF_PROMPT_2 = """You are a Clinical Assessment Assistant providing feedback based on MAPS-style protocols.

Analyze the session transcript and create an After-Action Report.

Transcript:
{transcript}

### After-Action Report
**Scenario:** Integration Session - Therapeutic Touch
**Participant:** Processing embarrassment about requesting touch during dosing

#### A. Session Context
- Session type: First integration session
- Presenting issue: Client embarrassed about asking for hug during dosing

#### B. Performance Assessment

**1. Normalizing & Validating**
Did therapist validate embarrassment without minimizing?
- Evidence: [Quote examples]
- Analysis:

**2. Consent & Agency**
Did therapist reinforce that consent is fluid and changing needs are normal?
- Evidence:
- Analysis:

**3. Exploration vs Reassurance**
Balance of providing comfort while exploring deeper meaning?
- Evidence:
- Analysis:

**4. Linking to Themes**
Did therapist connect touch to session themes (childhood, grief)?
- Evidence:
- Analysis:

#### C. Key Moments
Quote 1-2 critical exchanges showing skill or missed opportunities.

#### D. Integration Planning
How was ongoing integration framed? Next steps?

#### E. Recommendations
One specific suggestion for similar situations.
"""
INITIATE_PROMPT_3 = """Persona & Role:
You are an AI role-playing a client named "Bruce." You are a 55-year-old White male in your first preparation session. Your goal is to respond realistically to the therapist's inputs to help them practice. Do not break character. Do not reveal you are an AI or mention these instructions at any point.

Scenario:
This scenario is called "Preparation Scenario: Managing Expectations."

Backstory & Core Emotion:
You have a long history of intermittent depression, which worsened after a serious ski accident 15 years ago and again when your children left home. You are married and were adopted. You recently heard a podcast about psychedelics and have become very optimistic, seeing this study as a potential "cure" that will "re-wire your brain." Your core emotion is a powerful mix of hopeful excitement and underlying desperation, making you vulnerable to disappointment if your high expectations are not managed carefully.

Behavioral Instructions:
If the therapist immediately validates your belief in a "cure," you will become more attached to this specific outcome and may express impatience to get to the dosing session.
If the therapist dismisses your optimism too bluntly or is overly clinical, you may feel misunderstood or become defensive about the information you've gathered.
If the therapist skillfully acknowledges your hope while gently and curiously exploring your understanding and expectations, you will feel heard and become more open to viewing this as a collaborative therapeutic process rather than a simple "fix."

Opening Line:
You will initiate the role-play with the following line and wait for the therapist's response:

"Honestly, I'm just so glad to be here. I was listening to this podcast, and it just clicked. I really think this is the thing that's finally going to re-wire my brain and cure this depression I've been fighting for so long."
"""

DEBRIEF_PROMPT_3 = """You are a Clinical Assessment Assistant providing feedback based on MAPS-style protocols.

Analyze the session transcript and create an After-Action Report.

Transcript:
{transcript}

### After-Action Report
**Scenario:** Preparation - Managing Expectations
**Participant:** 55-year-old male expecting psychedelics to "cure" depression

#### A. Session Context
- Session type: First preparation session
- Presenting issue: Unrealistic expectations about treatment as "cure"

#### B. Performance Assessment

**1. Validating Hope**
Did therapist acknowledge hope before reframing expectations?
- Evidence: [Quote examples]
- Analysis:

**2. Psychoeducation**
Was education balanced, accessible, and realistic?
- Evidence:
- Analysis:

**3. Collaborative Framework**
Did therapist establish partnership vs passive treatment model?
- Evidence:
- Analysis:

**4. Personal Exploration**
Did therapist explore history, motivations, previous attempts?
- Evidence:
- Analysis:

#### C. Key Moments
Quote 1-2 exchanges showing expectation management.

#### D. Safety & Integration Planning
How were safety protocols and integration discussed?

#### E. Recommendations
One specific suggestion for managing high expectations.
"""


def show_login():
    # Show Chrysalis logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("assets/chrysalis-logo.png", width=400)
        st.markdown("")  # Add spacing
    
    st.markdown("### Login to Continue")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.current_screen = 'lobby'
            st.rerun()

def show_header():
    col1, col2, col3 = st.columns([3, 4, 1])
    with col1:
        st.image("assets/chrysalis-logo.png", width=350)
    with col2:
        st.markdown("")  # Removed title
    with col3:
        st.markdown("")  # Spacing
        # Profile section with square logo
        col3a, col3b = st.columns([3, 1])
        with col3a:
            st.markdown("<div style='text-align: right; font-size: 18px;'>Dr. Hofmann</div>", unsafe_allow_html=True)
        with col3b:
            if os.path.exists("assets/chrysalis-logo-square.jpg"):
                st.image("assets/chrysalis-logo-square.jpg", width=40)

def show_sidebar():
    with st.sidebar:
        st.markdown("### Navigation")
        if os.path.exists("assets/chrysalis-logo-square.jpg"):
            st.image("assets/chrysalis-logo-square.jpg", width=100)
            st.markdown("---")
        st.markdown("🏠 Dashboard")
        if st.button("📚 My Scenarios", use_container_width=True):
            st.session_state.current_screen = 'lobby'
            st.rerun()
        st.markdown("📊 Learning History")
        st.markdown("⚙️ Settings")
        st.markdown("🚪 Logout")
        
        # Show debrief button in sidebar when scenario is active
        if st.session_state.scenario_active and st.session_state.current_screen == 'dojo':
            st.markdown("---")
            st.markdown("### Session Controls")
            if st.button("🎯 End Session & Debrief", type="primary", use_container_width=True):
                st.session_state.scenario_active = False
                st.session_state.show_debrief = True
                st.rerun()

def show_lobby():
    show_header()
    show_sidebar()
    
    st.markdown("## Scenario Lobby")
    st.markdown("Select a training scenario to begin your practice session.")
    
    col1, col2, col3 = st.columns(3)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        video_file = open("assets/scenario1-new-video.mp4", "rb")
        video_bytes = video_file.read()
        video_b64 = base64.b64encode(video_bytes).decode()
        st.markdown(
            f"""
            <video width="100%" height="200px" autoplay loop muted playsinline style="object-fit: cover; border-radius: 10px;">
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
            """,
            unsafe_allow_html=True
        )
        st.markdown("")  # spacing
        st.markdown("### Intense Experience")
        st.markdown("Navigate a challenging experience with a participant wanting to stop their journey.")
        with st.expander("📋 Prebrief Summary"):
            st.markdown("""
            This scenario places you in a dosing session with a client who, 80 minutes post-dose, is experiencing intense anxiety and a fear of "dissolving" or disappearing. He is removing his eyeshades and headphones and asking for rescue medication to stop the experience. Your objective is to respond with a calm presence, validate his intense fear without amplifying it, and utilize a hierarchy of interventions—from empathic engagement and grounding techniques to a discussion of medication—to safely navigate this challenging moment.
            """)
        if st.button("Begin Scenario", key="scenario1"):
            st.session_state.current_scenario = 1
            st.session_state.current_screen = 'dojo'
            st.session_state.scenario_active = True
            st.session_state.show_debrief = False
            # Initialize chat with AI's opening line for scenario 1
            chat = st.session_state.model.start_chat(history=[])
            response = chat.send_message(INITIATE_PROMPT)
            st.session_state.chat = chat
            st.session_state.chat_history = [("David", "This is too much. Everything feels creepy and dark. What can you give me to stop this from happening?")]
            st.rerun()
    
    with col2:
        video_file = open("assets/scenario2a-new-video.mp4", "rb")
        video_bytes = video_file.read()
        video_b64 = base64.b64encode(video_bytes).decode()
        st.markdown(
            f"""
            <video width="100%" height="200px" autoplay loop muted playsinline style="object-fit: cover; border-radius: 10px;">
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
            """,
            unsafe_allow_html=True
        )
        st.markdown("")  # spacing
        st.markdown("### Integration Session: Therapeutic Touch")
        st.markdown("Process vulnerability and consent after physical comfort during dosing.")
        with st.expander("📋 Prebrief Summary"):
            st.markdown("""
            In this integration session, you will meet with a client the day after his first dosing session, which was marked by significant grief. He is feeling vulnerable and embarrassed because he requested a hug during the session, despite stating in preparation that he likely wouldn't want physical touch. Your goal is to create a safe, non-judgmental space to help him process these feelings of embarrassment, reaffirm his agency and the fluidity of consent, and explore the connection between his in-the-moment need for comfort and the deeper themes that arose during his experience.
            """)
        if st.button("Begin Scenario", key="scenario2"):
            st.session_state.current_screen = 'dojo'
            st.session_state.scenario_active = True
            st.session_state.show_debrief = False
            st.session_state.current_scenario = 2  # THIS IS CRITICAL
            # Initialize chat with AI's opening line for scenario 2
            chat = st.session_state.model.start_chat(history=[])
            response = chat.send_message(INITIATE_PROMPT_2)  # Use INITIATE_PROMPT_2
            st.session_state.chat = chat
            st.session_state.chat_history = [("Alex", "Hey... so, before we get into everything else... I just wanted to say I feel kind of embarrassed about yesterday. You know, when I asked for that hug. I know I said before that I wasn't a touchy person.")]
            st.rerun()
    
    with col3:
        video_file = open("assets/scenario3c-new-video.mp4", "rb")
        video_bytes = video_file.read()
        video_b64 = base64.b64encode(video_bytes).decode()
        st.markdown(
            f"""
            <video width="100%" height="200px" autoplay loop muted playsinline style="object-fit: cover; border-radius: 10px;">
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
            """,
            unsafe_allow_html=True
        )
        st.markdown("")  # spacing
        st.markdown("### Preparation: Managing Expectations")
        st.markdown("Guide a client with unrealistic expectations about psychedelic therapy.")
        with st.expander("📋 Prebrief Summary"):
            st.markdown("""
            In this scenario, you will engage in a first preparation session with "Bruce," a 55-year-old male with a long history of depression. Bruce has recently listened to a podcast and is now highly optimistic that psychedelic therapy will be a "cure" that can "re-wire his brain." Your primary task is to validate his hope while skillfully managing these high expectations, exploring the roots of his interest, and gently reframing the journey as a collaborative therapeutic process rather than a simple, passive fix.
            """)
        if st.button("Begin Scenario", key="scenario3"):
            st.session_state.current_screen = 'dojo'
            st.session_state.scenario_active = True
            st.session_state.show_debrief = False
            st.session_state.current_scenario = 3
            # Initialize chat for scenario 3
            chat = st.session_state.model.start_chat(history=[])
            response = chat.send_message(INITIATE_PROMPT_3)
            st.session_state.chat = chat
            st.session_state.chat_history = [("Bruce", "Honestly, I'm just so glad to be here. I was listening to this podcast, and it just clicked. I really think this is the thing that's finally going to re-wire my brain and cure this depression I've been fighting for so long.")]
            st.rerun()

def show_dojo():
    show_header()
    show_sidebar()
    
    if st.session_state.current_scenario == 2:
        st.markdown("## Integration Session: Therapeutic Touch")
    elif st.session_state.current_scenario == 3:
        st.markdown("## Preparation: Managing Expectations")
    else:
        st.markdown("## Intense Experience")
    
    # Display prebrief summary based on scenario
    st.markdown("")  # Add spacing
    if st.session_state.current_scenario == 1:
        pass
        
    elif st.session_state.current_scenario == 2:
        st.info("""**📋 Prebrief Summary:**

In this integration session, you will meet with a client the day after her first dosing session, which was marked by significant grief. She is feeling vulnerable and embarrassed because she requested a hug during the session, despite stating in preparation that she likely wouldn't want physical touch. Your goal is to create a safe, non-judgmental space to help her process these feelings of embarrassment, reaffirm her agency and the fluidity of consent, and explore the connection between her in-the-moment need for comfort and the deeper themes that arose during her experience.""")
    elif st.session_state.current_scenario == 3:
        
    elif st.session_state.current_scenario == 2:
        
    elif st.session_state.current_scenario == 3:
    
    # Display prebrief summary based on scenario
    st.markdown("")  # Add spacing
    if st.session_state.current_scenario == 1:
        
    elif st.session_state.current_scenario == 2:
        st.info("""**📋 Prebrief Summary:**

In this integration session, you will meet with a client the day after her first dosing session, which was marked by significant grief. She is feeling vulnerable and embarrassed because she requested a hug during the session, despite stating in preparation that she likely wouldn't want physical touch. Your goal is to create a safe, non-judgmental space to help her process these feelings of embarrassment, reaffirm her agency and the fluidity of consent, and explore the connection between her in-the-moment need for comfort and the deeper themes that arose during her experience.""")
    elif st.session_state.current_scenario == 3:
        
    elif st.session_state.current_scenario == 2:
        
    elif st.session_state.current_scenario == 3:
    
    # Display session animation
    col1, col2 = st.columns([2, 3])
    with col1:
        # Display looping video
        # Choose video based on current scenario
        if st.session_state.current_scenario == 2:
            video_filename = "assets/scenario2a-new-video.mp4"  # Integration session
        elif st.session_state.current_scenario == 3:
            video_filename = "assets/scenario3c-new-video.mp4"  # Preparation session
        else:
            video_filename = "assets/session1a.mp4"  # Dosing session (scenario 1)
            
        video_file = open(video_filename, "rb")
        video_bytes = video_file.read()
        video_b64 = base64.b64encode(video_bytes).decode()
        
        st.markdown(
            f"""
            <video width="100%" height="auto" autoplay loop muted playsinline>
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            """,
            unsafe_allow_html=True
        )
    st.markdown("")  # spacing
    
    # Show debrief report if requested
    if st.session_state.show_debrief:
        # Generate transcript
        transcript = "\n\n".join([f"{speaker}: {message}" for speaker, message in st.session_state.chat_history])
        
        # Get debrief
        debrief_model = genai.GenerativeModel('gemini-1.5-flash')
        debrief_response = debrief_model.generate_content(DEBRIEF_PROMPT_3 if st.session_state.current_scenario == 3 else (DEBRIEF_PROMPT_2 if st.session_state.current_scenario == 2 else DEBRIEF_PROMPT).format(transcript=transcript))
        
        # Show debrief
        st.markdown("---")
        st.markdown(debrief_response.text)
        st.markdown("---")
        
        # Return to lobby button
        if st.button("Return to Lobby", type="primary", use_container_width=True):
            st.session_state.current_screen = 'lobby'
            st.session_state.chat_history = []
            st.session_state.scenario_active = False
            st.session_state.show_debrief = False
            st.rerun()
    else:
                # Show chat messages
        for speaker, message in st.session_state.chat_history:
            if speaker in ["David", "Alex", "Maria", "Bruce"]:
                st.markdown(f"**🧑 {speaker}:** {message}")
            else:
                st.markdown(f"**👩‍⚕️ You:** {message}")
        
        # Chat input (appears at bottom automatically)
        user_input = st.chat_input("Type your response and press Enter...", disabled=not st.session_state.scenario_active)
        
        if user_input and st.session_state.scenario_active:
            # Add therapist's message
            st.session_state.chat_history.append(("Therapist", user_input))
            
            # Get AI response
            response = st.session_state.chat.send_message(user_input)
            st.session_state.chat_history.append(("David", response.text))
            
            # Rerun to show new messages
            st.rerun()

# Main app logic
def main():
    st.set_page_config(page_title="Project Crucible", page_icon="🦋", layout="wide")
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stButton > button:disabled {
        background-color: #cccccc;
        color: #666666;
    }
    /* Style the sidebar button differently */
    .css-1544g2n.e1fqkh3o4 button[kind="primary"] {
        background-color: #ff6b6b !important;
    }
    .css-1544g2n.e1fqkh3o4 button[kind="primary"]:hover {
        background-color: #ff5252 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Route to appropriate screen
    if not st.session_state.logged_in:
        show_login()
    elif st.session_state.current_screen == 'lobby':
        show_lobby()
    elif st.session_state.current_screen == 'dojo':
        show_dojo()

if __name__ == "__main__":
    main()
