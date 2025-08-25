import streamlit as st
import google.generativeai as genai
import os
import base64
from PIL import Image
from datetime import datetime

# Configure Gemini API
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))


# Scenario 1 - Intense Experience
INITIATE_PROMPT = """You are an AI role-playing a participant named "David." You are a 50-year-old male, 80 minutes post-ingestion. The experience has become overwhelming - things feel "creepy and dark." You've removed your eyeshades and headphones. Your primary emotion is fear mixed with a desire to stop the experience.

Opening Line: "This is too much. Everything feels creepy and dark. What can you give me to stop this from happening?"
"""

# Scenario 2 - Integration Touch
INITIATE_PROMPT_2 = """You are an AI role-playing a client named "Alex." You are in your first integration session, the day after your first dosing session which was marked by significant grief. You feel embarrassed because you requested a hug during the session, despite saying you wouldn't want touch.

Opening Line: "Hey... so, before we get into everything else... I just wanted to say I feel kind of embarrassed about yesterday. You know, when I asked for that hug. I know I said before that I wasn't a touchy person."
"""

# Scenario 3 - Managing Expectations
INITIATE_PROMPT_3 = """You are an AI role-playing a client named "Bruce." You are a 55-year-old male in your first preparation session. You recently heard a podcast and are optimistic that psychedelic therapy will be a "cure" that can "re-wire your brain."

Opening Line: "Honestly, I'm just so glad to be here. I was listening to this podcast, and it just clicked. I really think this is the thing that's finally going to re-wire my brain and cure this depression I've been fighting for so long."
"""

# Debrief prompts
DEBRIEF_PROMPT = """You are a Senior Clinical Assessment Specialist providing feedback based on MAPS protocols.

Analyze the session transcript and create an Adherence Feedback report.

Transcript:
{transcript}

### Adherence Feedback
**Scenario:** Intense Experience - Dosing Session

#### Performance Assessment

**[Rate with 🟢/🟡/🔴] 1. Crisis Response & Intervention Hierarchy**
- What was done: [Specific actions from transcript]
- Why this matters: The intervention hierarchy (empathy → grounding → environment → medical) supports the participant's inner healing intelligence while ensuring safety.
- Evidence from transcript: [Direct quotes]

**[Rate with 🟢/🟡/🔴] 2. Validation Without Amplification**
- What was done: [Specific validation techniques]
- Why this matters: In expanded states, participants are highly suggestible. Skillful validation acknowledges their experience while maintaining calm presence.
- Evidence from transcript: [Direct quotes]

**[Rate with 🟢/🟡/🔴] 3. Clinical Judgment**
- Assessment of difficult passage vs emergency
- Window of tolerance evaluation
- Evidence from transcript: [Direct quotes]

**[Rate with 🟢/🟡/🔴] 4. Therapist Metaskills**
- Somatic self-regulation and grounded presence
- Trust in the process
- Evidence of calm nervous system

#### Key Therapeutic Moments
[Quote 2-3 critical exchanges]

#### Specific Recommendations
1. [Immediate improvement with example phrase]
2. [Advanced technique suggestion]

#### Further Reading & Protocol Citations
- MAPS MDMA-AT Treatment Manual V8.1 (2017)
- Johnson et al. (2008): Guidelines for safety

Remember to replace [Rate with 🟢/🟡/🔴] with appropriate emoji based on performance.
"""

DEBRIEF_PROMPT_2 = """You are a Senior Clinical Assessment Specialist providing feedback based on MAPS protocols.

Analyze the session transcript and create an Adherence Feedback report.

Transcript:
{transcript}

### Adherence Feedback
**Scenario:** Integration Session - Therapeutic Touch

#### Performance Assessment

**[Rate with 🟢/🟡/🔴] 1. Creating Safety & Non-Judgmental Space**
- What was done: [Specific actions]
- Why this matters: Creating psychological safety is foundational to integration work.
- Evidence from transcript: [Direct quotes]

**[Rate with 🟢/🟡/🔴] 2. Consent, Agency & Touch Dynamics**
- Normalizing consent fluidity
- Therapeutic touch protocol adherence
- Evidence from transcript: [Direct quotes]

**[Rate with 🟢/🟡/🔴] 3. Integration Skills**
- Connecting to deeper therapeutic themes
- Balance of support vs exploration
- Evidence from transcript: [Direct quotes]

**[Rate with 🟢/🟡/🔴] 4. Therapeutic Touch Considerations**
Per MAPS protocols, therapeutic touch must be:
- Nonsexual and participant-centered
- Explicitly consented to
- Driven by participant needs

#### Key Therapeutic Moments
[Quote 2-3 critical exchanges]

#### Specific Recommendations
1. [Immediate improvement with example phrase]
2. [Advanced technique suggestion]

#### Further Reading & Protocol Citations
- Luoma et al. (2024): Getting in touch with touch
- MAPS Manual: Therapeutic touch guidelines

Remember to replace [Rate with 🟢/🟡/🔴] with appropriate emoji based on performance.
"""

DEBRIEF_PROMPT_3 = """You are a Senior Clinical Assessment Specialist providing feedback based on MAPS protocols.

Analyze the session transcript and create an Adherence Feedback report.

Transcript:
{transcript}

### Adherence Feedback
**Scenario:** Preparation - Managing Expectations

#### Performance Assessment

**[Rate with 🟢/🟡/🔴] 1. Expectation Management**
- Validating hope while introducing nuance
- "Healing" vs "curing" distinction
- Evidence from transcript: [Direct quotes]

**[Rate with 🟢/🟡/🔴] 2. Psychoeducation**
- Balanced information delivery
- Informed consent elements
- Evidence from transcript: [Direct quotes]

**[Rate with 🟢/🟡/🔴] 3. Collaborative Framework**
- Partnership building
- Empowering participant agency
- Evidence from transcript: [Direct quotes]

**[Rate with 🟢/🟡/🔴] 4. Therapist Metaskills**
- Managing attachment to outcomes
- Authentic presence
- Evidence from transcript: [Direct quotes]

#### Key Therapeutic Moments
[Quote 2-3 critical exchanges]

#### Specific Recommendations
1. [Immediate improvement with example phrase]
2. [Advanced technique suggestion]

#### Further Reading & Protocol Citations
- Breeksema et al. (2020): Patient experiences
- MAPS Manual: Preparation protocols

Remember to replace [Rate with 🟢/🟡/🔴] with appropriate emoji based on performance.
"""


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
if 'model' not in st.session_state:
    st.session_state.model = genai.GenerativeModel('gemini-1.5-flash')


def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("assets/chrysalis-logo.png"):
            st.image("assets/chrysalis-logo.png", width=400)
        st.markdown("### Login to Continue")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.current_screen = 'lobby'
            st.rerun()

def show_header():
    col1, col2, col3 = st.columns([2, 5, 1])
    with col1:
        if os.path.exists("assets/chrysalis-logo.png"):
            st.image("assets/chrysalis-logo.png", width=250)
    with col2:
        st.markdown("")
    with col3:
        st.markdown("<div style='text-align: right; font-size: 18px;'>👨‍⚕️ Dr. Hofmann</div>", unsafe_allow_html=True)

def show_sidebar():
    with st.sidebar:
        # Add logo at top of sidebar if square version exists
        if os.path.exists("assets/chrysalis-logo-square.jpg"):
            st.image("assets/chrysalis-logo-square.jpg", width=120)
            st.markdown("---")
        
        st.markdown("### Navigation")
        st.markdown("◉ Dashboard")
        if st.button("◎ Scenario Lobby", use_container_width=True):
            st.session_state.current_screen = 'lobby'
            st.rerun()
        if st.button("📚 Learning History", use_container_width=True):
            st.session_state.current_screen = 'history'
            st.rerun()
        st.markdown("◇ Settings")
        st.markdown("◌ Logout")


def show_history():
    """Display learning history"""
    show_header()
    show_sidebar()
    
    st.markdown("# 📚 Learning History")
    st.markdown("Review your completed training sessions.")
    
    from datetime import datetime, timedelta
    import random
    
    sessions = []
    base_date = datetime.now()
    scenario_names = {
        1: "Intense Experience - Dosing Session",
        2: "Integration Session - Therapeutic Touch", 
        3: "Preparation Session - Managing Expectations"
    }
    
    summaries = {
        1: ["Strong crisis response", "Good validation techniques", "Excellent clinical judgment"],
        2: ["Created safety container", "Good integration skills", "Strong therapeutic presence"],
        3: ["Managed expectations well", "Good psychoeducation", "Excellent collaborative stance"]
    }
    
    for i in range(15):
        scenario = (i % 3) + 1
        sessions.append({
            'id': 15-i,
            'scenario': scenario,
            'title': scenario_names[scenario],
            'date': base_date - timedelta(days=random.randint(1,30)),
            'summary': random.choice(summaries[scenario]),
            'duration': random.randint(15,35),
            'rating': random.choice(['🟢', '🟢', '🟡'])
        })
    
    sessions.sort(key=lambda x: x['date'], reverse=True)
    
    # Progress Summary
    st.markdown("### 📊 Your Progress Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sessions", 15)
    with col2:
        excellent = len([s for s in sessions if s['rating'] == '🟢'])
        st.metric("Excellent Sessions", f"{excellent} ({excellent/15*100:.0f}%)")
    with col3:
        st.metric("Total Practice Time", "375 min")
    with col4:
        st.metric("Avg Session Length", "25 min")
    
    st.markdown("---")
    st.markdown("### Recent Sessions")
    
    for session in sessions:
        col1, col2, col3, col4, col5 = st.columns([0.5, 2.5, 1.5, 2.5, 1])
        with col1:
            st.markdown(session['rating'])
        with col2:
            st.markdown(f"**{session['title']}**")
            st.caption(f"{session['duration']} min")
        with col3:
            st.markdown(session['date'].strftime('%b %d, %Y'))
        with col4:
            st.caption(session['summary'])
        with col5:
            st.button("View", key=f"v{session['id']}")
        st.markdown("---")


def show_dojo():
    show_header()
    show_sidebar()
    
    # Show scenario title
    if st.session_state.current_scenario == 1:
        st.markdown("## Intense Experience")
    elif st.session_state.current_scenario == 2:
        st.markdown("## Integration Session: Therapeutic Touch")
    else:
        st.markdown("## Preparation: Managing Expectations")
    
    # Show video for the scenario
    if st.session_state.current_scenario == 1:
        video_file = "assets/session1a.mp4"
    elif st.session_state.current_scenario == 2:
        video_file = "assets/scenario2a-new-video.mp4"
    else:
        video_file = "assets/scenario3c-new-video.mp4"
    
    if os.path.exists(video_file):
        with open(video_file, "rb") as f:
            video_bytes = f.read()
            video_b64 = base64.b64encode(video_bytes).decode()
            st.markdown(
                f"""
                <video width="25%" height="auto" style="margin: 0; display: block;" autoplay loop muted playsinline>
                    <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                </video>
                """,
                unsafe_allow_html=True
            )
    
    # Display prebrief summary
    st.markdown("")  # spacing
    
    # Close overview if showing debrief
    overview_expanded = not st.session_state.get('show_debrief', False)
    
    if st.session_state.current_scenario == 1:
        with st.expander("📋 Session Overview", expanded=overview_expanded):
            st.info("""
            **Dosing Session: Intense Experience**
            
            This scenario places you in a dosing session with a client who, 80 minutes post-dose, is experiencing intense anxiety and a fear of dissolving or disappearing. He is removing his eyeshades and headphones and asking for rescue medication to stop the experience.
            
            **Your objectives:**
            • Respond with a calm, grounded presence
            • Validate his fear without amplifying it
            • Use the intervention hierarchy (empathy → grounding → environment → medical)
            • Differentiate between difficult passage and genuine emergency
            """)
    
    elif st.session_state.current_scenario == 2:
        with st.expander("📋 Session Overview", expanded=overview_expanded):
            st.info("""
            **Integration Session: Therapeutic Touch**
            
            In this integration session, you will meet with a client the day after her first dosing session, which was marked by significant grief. She is feeling vulnerable and embarrassed because she requested a hug during the session, despite stating in preparation that she likely would not want physical touch.
            
            **Your objectives:**
            • Create a safe, non-judgmental space
            • Normalize the fluidity of consent
            • Explore the meaning behind the request for touch
            • Connect the experience to deeper therapeutic themes
            """)
    
    elif st.session_state.current_scenario == 3:
        with st.expander("📋 Session Overview", expanded=overview_expanded):
            st.info("""
            **Preparation Session: Managing Expectations**
            
            In this scenario, you will engage in a first preparation session with Bruce, a 55-year-old male with a long history of depression. Bruce has recently listened to a podcast and is now highly optimistic that psychedelic therapy will be a cure that can re-wire his brain.
            
            **Your objectives:**
            • Validate his hope while managing expectations
            • Provide balanced psychoeducation
            • Establish a collaborative therapeutic framework
            • Explore his history and motivations
            """)
    
    # Show debrief if requested
    if st.session_state.get('show_debrief', False):
        st.markdown("---")
        
        # Generate transcript
        transcript = "\n\n".join([f"{speaker}: {message}" for speaker, message in st.session_state.chat_history])
        
        # Select appropriate debrief prompt
        if st.session_state.current_scenario == 1:
            debrief_prompt = DEBRIEF_PROMPT
        elif st.session_state.current_scenario == 2:
            debrief_prompt = DEBRIEF_PROMPT_2
        else:
            debrief_prompt = DEBRIEF_PROMPT_3
        
        # Generate debrief
        try:
            with st.spinner("📋 Generating Adherence Feedback..."):
                debrief_model = genai.GenerativeModel('gemini-1.5-flash')
                debrief_response = debrief_model.generate_content(
                    debrief_prompt.format(transcript=transcript)
                )
            
            # Display the feedback
            st.markdown(debrief_response.text)
            
        except Exception as e:
            st.error(f"Error generating debrief: {str(e)}")
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("📤 Submit for Instructor Review", use_container_width=True, disabled=True):
                pass
            st.caption("Coming soon")
        
        with col2:
            if st.button("⬇️ Download Session Report", use_container_width=True, disabled=True):
                pass
            st.caption("Coming soon")
        
        # Navigation buttons
        st.markdown("")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🔄 Restart Session", type="secondary", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.show_debrief = False
                st.session_state.scenario_active = False
                if 'chat' in st.session_state:
                    del st.session_state.chat
                st.rerun()
        
        with col3:
            if st.button("Return to Lobby", type="primary", use_container_width=True):
                st.session_state.current_screen = 'lobby'
                st.session_state.chat_history = []
                st.session_state.show_debrief = False
                st.rerun()
        
        # Don't show chat input during debrief
        return
    
    
    # Chat display
    st.markdown("")
    for speaker, message in st.session_state.chat_history:
        if speaker == "Therapist":
            st.markdown(f"**› You:** {message}")
        else:
            st.markdown(f"**‹ {speaker}:** {message}")
    
    # Chat input
    if st.session_state.scenario_active:
        user_input = st.chat_input("Type your response and press Enter...")
        
        if user_input:
            # Add therapist message
            st.session_state.chat_history.append(("Therapist", user_input))
            
            # Get AI response
            response = st.session_state.chat.send_message(user_input)
            speaker_name = "David" if st.session_state.current_scenario == 1 else ("Alex" if st.session_state.current_scenario == 2 else "Bruce")
            st.session_state.chat_history.append((speaker_name, response.text))
            
            st.rerun()
    
    # End session button in sidebar
    with st.sidebar:
        st.markdown("---")
        if st.button("◉ End Session & Debrief", type="primary", use_container_width=True):
            st.session_state.scenario_active = False
            st.session_state.show_debrief = True
            st.rerun()

# Main app
def main():
    # Set favicon
    favicon = "🦋"  # Default
    if os.path.exists("assets/chrysalis-logo-square.jpg"):
        favicon = Image.open("assets/chrysalis-logo-square.jpg")
    
    st.set_page_config(page_title="Chrysalis Therapist Training", page_icon=favicon, layout="wide")
    # Custom CSS for visual theme
    st.markdown("""
    <style>
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #2b2b3e;
    }
    
    /* Button styling with Chrysalis theme colors */
    .stButton > button {
        background-color: #2d4a5c;
        color: white;
        border-radius: 8px;
        border: 1px solid #4a7c8c;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #3a5a6c;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(74, 124, 140, 0.2);
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background-color: #4a7c8c;
        border: 1px solid #5a8c9c;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #5a8c9c;
    }
    
    /* Chat message styling */
    .stMarkdown {
        line-height: 1.6;
    }
    
    /* Video container styling */
    video {
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    
    if not st.session_state.logged_in:
        show_login()
    elif st.session_state.current_screen == 'dojo':
        show_dojo()
    elif st.session_state.current_screen == 'history':
        show_history()
    else:
        show_header()
        show_sidebar()
        
        st.markdown("## Scenario Lobby")
        st.markdown("Select a training scenario to begin your practice session.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Video for scenario 1
            if os.path.exists("assets/scenario1-new-video.mp4"):
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
            if st.button("Begin Scenario", key="scenario1"):
                st.session_state.current_screen = 'dojo'
                st.session_state.current_scenario = 1
                st.session_state.scenario_active = True
                chat = st.session_state.model.start_chat(history=[])
                response = chat.send_message(INITIATE_PROMPT)
                st.session_state.chat = chat
                st.session_state.chat_history = [("David", "This is too much. Everything feels creepy and dark. What can you give me to stop this from happening?")]
                st.rerun()
                
        with col2:
            # Video for scenario 2
            if os.path.exists("assets/scenario2a-new-video.mp4"):
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
            if st.button("Begin Scenario", key="scenario2"):
                st.session_state.current_screen = 'dojo'
                st.session_state.current_scenario = 2
                st.session_state.scenario_active = True
                chat = st.session_state.model.start_chat(history=[])
                response = chat.send_message(INITIATE_PROMPT_2)
                st.session_state.chat = chat
                st.session_state.chat_history = [("Alex", "Hey... so, before we get into everything else... I just wanted to say I feel kind of embarrassed about yesterday. You know, when I asked for that hug. I know I said before that I wasn't a touchy person.")]
                st.rerun()
                
        with col3:
            # Video for scenario 3
            if os.path.exists("assets/scenario3c-new-video.mp4"):
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
            if st.button("Begin Scenario", key="scenario3"):
                st.session_state.current_screen = 'dojo'
                st.session_state.current_scenario = 3
                st.session_state.scenario_active = True
                chat = st.session_state.model.start_chat(history=[])
                response = chat.send_message(INITIATE_PROMPT_3)
                st.session_state.chat = chat
                st.session_state.chat_history = [("Bruce", "Honestly, I'm just so glad to be here. I was listening to this podcast, and it just clicked. I really think this is the thing that's finally going to re-wire my brain and cure this depression I've been fighting for so long.")]
                st.rerun()
        
        # Available Scenarios
        st.markdown("---")
        st.markdown("### Available Scenarios")
        st.markdown("Expand your training with these scenarios:")
        
        scenarios = [
            ("Crisis Intervention", "Handle panic during peak", "🔴 Advanced", "30m"),
            ("Spiritual Emergency", "Navigate mystical experiences", "🔴 Advanced", "35m"),
            ("Somatic Release", "Guide trauma processing", "🟡 Intermediate", "25m"),
            ("First Timer Anxiety", "Support anxious participants", "🟢 Beginner", "20m"),
            ("Integration Resistance", "Help struggling clients", "🟡 Intermediate", "30m"),
            ("Childhood Trauma", "Support regression to early memories", "🔴 Advanced", "35m"),
            ("End of Life", "Terminal diagnosis exploration", "🔴 Advanced", "40m"),
            ("Veteran PTSD", "Military trauma processing", "🔴 Advanced", "35m"),
            ("Group Facilitation", "Managing multiple participants", "🔴 Advanced", "45m"),
            ("Music Medicine", "Therapeutic playlist curation", "🟢 Beginner", "20m"),
            ("Silent Session", "Non-verbal therapeutic presence", "🟡 Intermediate", "30m"),
            ("Harm Reduction", "Substance use history clients", "🟡 Intermediate", "25m"),
            ("Cultural Bridging", "Indigenous wisdom integration", "🟡 Intermediate", "30m"),
            ("Microdosing Consult", "Sub-perceptual protocols", "🟢 Beginner", "20m"),
            ("Boundary Testing", "Managing difficult dynamics", "🔴 Advanced", "35m")
        ]
        
        for i, (name, desc, level, time) in enumerate(scenarios):
            c1, c2, c3, c4, c5 = st.columns([2.5, 3.5, 1.5, 1, 1.5])
            with c1:
                st.markdown(f"**{name}**")
            with c2:
                st.caption(desc)
            with c3:
                st.markdown(level)
            with c4:
                st.caption(time)
            with c5:
                st.button("Begin →", key=f"begin_s{i}", disabled=True, use_container_width=True, help="Coming soon")
            st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("🔓 Unlock Additional Scenarios", disabled=True, use_container_width=True)
            st.caption("Coming soon")

if __name__ == "__main__":
    main()
