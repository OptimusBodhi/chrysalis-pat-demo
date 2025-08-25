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
DEBRIEF_PROMPT = """You are a Senior Clinical Assessment Specialist providing in-depth feedback based on MAPS protocols and evidence-based practices.

Analyze the session transcript and create a comprehensive After-Action Report meeting  training standards.

Transcript:
{transcript}

### After-Action Report
**Scenario:** Intense Experience - Dosing Session

#### Performance Assessment

**1. Crisis Response & Intervention Hierarchy**
- **What was done:** [Specific crisis interventions from transcript]
- **Why this matters:** The intervention hierarchy (empathy → grounding → environment → medical) is designed to support the participant's inner healing intelligence while ensuring safety. Premature medical intervention can interrupt crucial therapeutic processes, while delayed intervention risks genuine harm. This balance requires sophisticated clinical judgment (MAPS Manual, 2017).
- **Evidence from transcript:** [Direct quotes]

**2. Validation Without Amplification**
- **What was done:** [Specific validation techniques used]
- **Why this matters:** In expanded states, participants are highly suggestible. Language that amplifies fear ("That sounds terrifying") can escalate panic, while minimizing ("You're fine") can break trust. Skillful validation acknowledges the reality of their experience while maintaining calm presence (Johnson et al., 2008).
- **Evidence from transcript:** [Direct quotes]

**3. Clinical Judgment: Difficult Passage vs Emergency**
- **What was done:** [Assessment techniques employed]
- **Why this matters:** Distinguishing between challenging but therapeutic experiences and genuine medical emergencies is crucial. The "window of tolerance" concept helps assess whether the participant is in a growth zone or genuinely overwhelmed. Misreading this can either traumatize (pushing too hard) or waste therapeutic opportunity (intervening too soon).
- **Evidence from transcript:** [Direct quotes]

**4. Therapist Metaskills & Internal State**
- **Somatic self-regulation:** Did therapist maintain calm breathing and grounded presence?
- **Non-anxious presence:** Evidence of therapist remaining centered despite client distress?
- **Trust in the process:** Did therapist convey confidence in participant's capacity?
- **Why this matters:** In crisis moments, the therapist's nervous system becomes a co-regulatory tool. Participant's mirror therapist's internal state - anxiety breeds anxiety, calm facilitates navigation through difficulty (MAPS Manual, 2017).

#### Key Therapeutic Moments
[Quote 2-3 critical exchanges with analysis of micro-skills demonstrated]

#### Specific Recommendations for Enhancement

1. **Immediate improvement:** [E.g., "When David said 'make it stop,' respond first with somatic mirroring: 'I hear you want this to stop. I'm right here with you. Let's take one breath together.'"]

2. **Advanced technique:** [E.g., "Use the 'and' frame: 'Part of you wants this to stop AND another part brought you here for healing. Can we be with both?'"]

3. **Safety protocol refinement:** [E.g., "Establish numerical scaling: 'On a scale of 1-10, with 10 being medical emergency, where are you?'"]

#### Further Reading & Protocol Citations
- MAPS MDMA-AT Treatment Manual V8.1 (2017): Crisis intervention protocols
- Johnson et al. (2008): "Human hallucinogen research: Guidelines for safety"
- McGovern et al. (2024): "Deconstructing Psychedelic Phenomenology" - phases of experience
- Nicholas et al. (2018): "Escalating psilocybin doses" - understanding dose-response

#### Clinical Supervision Note
Consider bringing this session to supervision to explore: [Specific growth edge for therapist]
"""

DEBRIEF_PROMPT_2 = """You are a Senior Clinical Assessment Specialist providing in-depth feedback based on MAPS protocols and evidence-based practices.

Analyze the session transcript and create a comprehensive After-Action Report meeting  training standards.

Transcript:
{transcript}

### After-Action Report
**Scenario:** Integration Session - Therapeutic Touch

#### Performance Assessment

**1. Creating Safety & Non-Judgmental Space**
- **What was done:** [Specific actions from transcript]
- **Why this matters:** Creating psychological safety is foundational to integration work. When participants feel judged, they may withhold crucial material or re-experience shame, blocking the healing process. The therapist's ability to hold space without judgment directly impacts the participant's capacity to integrate difficult experiences (MAPS Manual, 2017).
- **Evidence from transcript:** [Direct quotes]

**2. Consent, Agency & Touch Dynamics**
- **What was done:** [Specific actions regarding consent discussion]
- **Why this matters:** MDMA can heighten receptivity to touch and intensify power dynamics. Normalizing consent fluidity helps participants understand that changing needs during non-ordinary states is expected, not a failure. This prevents additional shame layers from forming around natural vulnerability (Luoma et al., 2024).
- **Evidence from transcript:** [Direct quotes]
- **Therapeutic touch protocol adherence:** 
  - Was touch framed as nonsexual and participant-centered? 
  - Was the "inner healing intelligence" trusted?
  - Was withholding nurturing touch considered as potential "abuse by neglect"?

**3. Integration Skills & Somatic Awareness**
- **What was done:** [Specific integration techniques used]
- **Why this matters:** Integration requires bridging the somatic, emotional, and cognitive domains. Touch requests often carry deeper therapeutic themes - unmet developmental needs, attachment wounds, or corrective experiences. Skilled facilitators help participants make these connections without imposing interpretations (Bathje et al., 2022).
- **Evidence from transcript:** [Direct quotes]

**4. Therapist Metaskills & Internal State**
- **Presence & Regulation:** Did the therapist maintain grounded presence when discussing vulnerable topics?
- **Counter-transference awareness:** Any signs of therapist discomfort with touch discussion?
- **Embodied attunement:** Evidence of somatic resonance with client's experience?
- **Why this matters:** The therapist's internal state directly impacts the therapeutic container. Participants in expanded states are highly attuned to subtle cues of judgment or anxiety. The therapist's regulated nervous system serves as a co-regulatory resource (MAPS Manual, 2017).

#### Key Therapeutic Moments
[Quote 2-3 critical exchanges with analysis of micro-skills demonstrated]

#### Specific Recommendations for Enhancement

1. **Immediate improvement:** [Highly specific suggestion, e.g., "When the client expressed embarrassment, the therapist could have offered: 'I'm noticing you looking down as you share this. I wonder if we might pause and notice what's happening in your body right now?'"]

2. **Advanced technique:** [Suggestion for deepening the work, e.g., "To explore the attachment dimension, consider: 'The part of you that reached for comfort - what age does that part feel like? What did that younger part need?'"]

3. **Integration homework:** [Specific practice to suggest to client, e.g., "Journaling prompt: 'Write a letter from your dosing-session self to your everyday self about what comfort means'"]

#### Further Reading & Protocol Citations
- MAPS MDMA-AT Treatment Manual V8.1 (2017): Sections on therapeutic touch and consent
- Luoma et al. (2024): "Getting in touch with touch" - Touch Outcomes Measurement Inventory
- Bathje et al. (2022): "Psychedelic integration: An analysis of the concept and its practice"
- O'Donnell et al. (2024): "Conceptual framework for therapeutic approach in MDMA-AT"

#### Clinical Supervision Note
Consider bringing this session to supervision to explore: [Specific growth edge for therapist]
"""

DEBRIEF_PROMPT_3 = """You are a Senior Clinical Assessment Specialist providing in-depth feedback based on MAPS protocols and evidence-based practices.

Analyze the session transcript and create a comprehensive After-Action Report meeting  training standards.

Transcript:
{transcript}

### After-Action Report
**Scenario:** Preparation - Managing Expectations

#### Performance Assessment

**1. Expectation Management & Hope Calibration**
- **What was done:** [Specific techniques for addressing "cure" mindset]
- **Why this matters:** Unrealistic expectations can lead to devastating disappointment and treatment dropout. Yet hope is essential for engagement. The art lies in validating hope while introducing nuance. The concept of "healing" vs "curing" helps participants understand transformation without prometheaning overnight miracles (Breeksema et al., 2020).
- **Evidence from transcript:** [Direct quotes]

**2. Psychoeducation & Informed Consent**
- **What was done:** [Educational elements provided]
- **Why this matters:** True informed consent requires understanding both potential benefits and challenges. Participants need to know about "ontological shock," challenging experiences, and integration demands. This isn't fear-mongering but preparation that actually improves outcomes by reducing anxiety when difficulties arise (Argyri et al., 2025).
- **Evidence from transcript:** [Direct quotes]

**3. Collaborative Therapeutic Frame**
- **What was done:** [Partnership-building techniques]
- **Why this matters:** PAT's effectiveness partly stems from empowering participants as active agents in their healing. Moving from "doctor-patient" to "healing partnership" activates internal resources and responsibility. This shift begins in preparation through language and relational stance (O'Donnell et al., 2024).
- **Evidence from transcript:** [Direct quotes]

**4. Therapist Metaskills & Internal State**
- **Managing own attachment to outcomes:** Evidence of therapist remaining neutral about "success"?
- **Holding complexity:** Ability to sit with both hope and uncertainty?
- **Authentic presence:** Genuine rather than scripted responses?
- **Why this matters:** Participants can sense when therapists are over-invested in positive outcomes or following scripts. Authentic, grounded presence that can hold complexity models the very flexibility needed for psychedelic work (MAPS Manual, 2017).

#### Key Therapeutic Moments
[Quote 2-3 critical exchanges with analysis of micro-skills demonstrated]

#### Specific Recommendations for Enhancement

1. **Immediate improvement:** [E.g., "When Bruce used 'cure,' reflect with curiosity: 'I'm hearing that word cure is really important to you. Can you say more about what cure would look like in your life?'"]

2. **Advanced technique:** [E.g., "Introduce healing vs curing: 'Many people find these medicines help them relate differently to their depression rather than erasing it. What if healing meant changing your relationship with these feelings?'"]

3. **Preparation homework:** [E.g., "Suggest journaling: 'Between now and next session, notice moments when you feel even slightly different than usual - not better or worse, just different. These might be breadcrumbs.'"]

#### Further Reading & Protocol Citations
- MAPS MDMA-AT Treatment Manual V8.1 (2017): Preparation protocols
- Breeksema et al. (2020): "Patient experiences in qualitative studies" - expectation themes
- Argyri et al. (2025): "Navigating groundlessness" - ontological shock preparation
- Frymann et al. (2022): "Psychedelic Integration Scales" - measuring readiness

#### Clinical Supervision Note
Consider bringing this session to supervision to explore: [Specific growth edge for therapist]
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
        if st.button("◎ My Scenarios", use_container_width=True):
            st.session_state.current_screen = 'lobby'
            st.rerun()
        st.markdown("◈ Learning History")
        st.markdown("◇ Settings")
        st.markdown("◌ Logout")


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
    
    if st.session_state.current_scenario == 1:
        with st.expander("📋 Session Overview", expanded=True):
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
        with st.expander("📋 Session Overview", expanded=True):
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
        with st.expander("📋 Session Overview", expanded=True):
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
        st.markdown("### 📋 Generating Assessment Report...")
        
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
            debrief_model = genai.GenerativeModel('gemini-1.5-flash')
            debrief_response = debrief_model.generate_content(
                debrief_prompt.format(transcript=transcript)
            )
            
            st.markdown("### 📊 After-Action Report")
            st.markdown(debrief_response.text)
            
        except Exception as e:
            st.error(f"Error generating debrief: {str(e)}")
        
        # Return to lobby button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
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

if __name__ == "__main__":
    main()
