import os
import google.generativeai as genai
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="AI Command Center", page_icon="🚀", layout="wide"
)

# Custom CSS for 100% Pure Cohesive Dark Theme
st.markdown(
    """
    <style>
    /* Force full dark background across the entire app and sidebar */
    .stApp, .main, [data-testid="stSidebar"] {
        background-color: #08090d !important;
        color: #e2e8f0 !important;
    }
    
    /* Hide Streamlit default top header */
    header {visibility: hidden;}

    /* Command Center Hero Header */
    .command-header {
        background: linear-gradient(135deg, #12141c 0%, #1a1d2d 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
    }
    
    /* Mission Telemetry Stat Cards */
    .stat-card {
        background: rgba(18, 20, 28, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        flex: 1;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Chat Message Bubbles for Dark Mode */
    .stChatMessage {
        background-color: #12141c !important;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        color: #e2e8f0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    
    /* COMPLETELY FIX THE BOTTOM CHAT INPUT BAR TO DARK THEME */
    [data-testid="stChatInput"] {
        background-color: #08090d !important;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 1rem;
    }
    
    .stChatInputContainer {
        background-color: #12141c !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 12px !important;
    }
    
    .stChatInputContainer textarea {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0d0f17 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Gemini API configuration
api_key = None
try:
  if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
  pass

if not api_key:
  api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
  st.error(
      "⚠️ API Key not found! Please set GEMINI_API_KEY in Streamlit Secrets or"
      " your local environment."
  )
else:
  genai.configure(api_key=api_key)

# Command Center Hero Header
st.markdown(
    """
    <div class="command-header">
        <h2 style="margin: 0; font-weight: 700; letter-spacing: 0.5px; color: #ffffff;">⚡ Command Center</h2>
        <p style="margin: 5px 0 0 0; color: #94a3b8; font-size: 1rem;">Welcome back, Commander • Powered by Google Gemini 2.5 Flash</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Mission Telemetry / Stat Cards Row
col1, col2, col3, col4 = st.columns(4)
with col1:
  st.markdown(
      """
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">System Status</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: #34d399; margin-top: 5px;">ONLINE</div>
        </div>
    """,
      unsafe_allow_html=True,
  )
with col2:
  st.markdown(
      """
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">AI Model</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #60a5fa; margin-top: 5px;">Gemini 2.5</div>
        </div>
    """,
      unsafe_allow_html=True,
  )
with col3:
  st.markdown(
      """
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">Security</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: #a78bfa; margin-top: 5px;">SECURE</div>
        </div>
    """,
      unsafe_allow_html=True,
  )
with col4:
  st.markdown(
      """
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">Uptime</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: #f472b6; margin-top: 5px;">100%</div>
        </div>
    """,
      unsafe_allow_html=True,
  )

st.markdown("<br>", unsafe_allow_html=True)

# Sidebar for Persona / Mode Selection
st.sidebar.markdown(
    "## 🌌 Navigation Hub", unsafe_allow_html=True
)
persona = st.sidebar.selectbox(
    "Choose AI Persona/Mode",
    ["General Assistant", "AI Tutor", "Project Builder"],
)

# Define system prompts based on selected persona
if persona == "General Assistant":
  system_prompt = (
      "You are a helpful, smart, and versatile personal AI assistant. Help"
      " the user with general tasks, brainstorming, summarizing, and writing."
  )
  st.sidebar.info(
      "🛰️ **Mode:** General Assistant\n\nReady for operations, logs, and"
      " writing tasks."
  )

elif persona == "AI Tutor":
  system_prompt = (
      "You are an expert, patient, and encouraging tutor. Break down concepts"
      " simply, use analogies, ask interactive questions, and guide the user"
      " step-by-step without just giving away answers right away."
  )
  st.sidebar.info(
      "🪐 **Mode:** AI Tutor\n\nReady to decode programming, science, and math"
      " modules."
  )

elif persona == "Project Builder":
  system_prompt = (
      "You are a master software architect and coding mentor. Help design"
      " applications, write clean code snippets, structure projects, and solve"
      " technical roadblocks."
  )
  st.sidebar.info(
      "🚀 **Mode:** Project Builder\n\nReady to architect apps and build"
      " systems."
  )

st.sidebar.markdown("---")
st.sidebar.markdown(
    "### 📡 Telemetry Logs\n- **Cloud Host:** Streamlit Cloud\n- **Access Level:"
    "** Unlimited\n- **Connection:** Encrypted"
)

# Initialize Gemini Model
try:
  model = genai.GenerativeModel(
      model_name="gemini-2.5-flash", system_instruction=system_prompt
  )
except Exception:
  model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# Session State Management for Chat History
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display welcome message if empty
if not st.session_state.messages:
  with st.chat_message("assistant"):
    st.markdown(
        f"Commander, your **{persona}** module is active and synced. What"
        " mission shall we execute today?"
    )

# Display chat history from session state
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# User Input Handling (Unified single chat bar)
if user_input := st.chat_input("Enter command or query..."):
  st.session_state.messages.append({"role": "user", "content": user_input})
  with st.chat_message("user"):
    st.markdown(user_input)

  # Generate response from Gemini model
  with st.chat_message("assistant"):
    with st.spinner("⚡ Processing transmission..."):
      try:
        full_prompt = f"{system_prompt}\n\nUser Query: {user_input}"
        response = model.generate_content(full_prompt)
        ai_response = response.text

        st.markdown(ai_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": ai_response}
        )
      except Exception as e:
        st.error(
            f"Command error: {e}. (If this is a 503 high demand error,"
            " re-initiating transmission in a moment will resolve it!)"
        )