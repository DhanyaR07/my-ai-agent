import os
import google.generativeai as genai
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Oceanic AI Workspace", page_icon="🌊", layout="wide"
)

# Custom CSS for Light Sea / Ocean Theme
st.markdown(
    """
    <style>
    /* Force soft ocean mist background across the entire app and sidebar */
    .stApp, .main, [data-testid="stSidebar"] {
        background-color: #f0f9ff !important;
        color: #0c4a6e !important;
    }
    
    /* Hide Streamlit default top header */
    header {visibility: hidden;}

    /* Ocean Hero Header Card */
    .hero-header {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        border: 1px solid #7dd3fc;
        padding: 2rem;
        border-radius: 16px;
        color: #0369a1;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(2, 132, 199, 0.05);
    }
    
    /* Chat Message Bubbles for Sea Theme */
    .stChatMessage {
        background-color: #ffffff !important;
        border: 1px solid #bae6fd;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        color: #0c4a6e !important;
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.03);
    }
    
    /* Bottom Chat Input Bar for Sea Theme */
    [data-testid="stChatInput"] {
        background-color: #f0f9ff !important;
        border-top: 1px solid #bae6fd;
        padding-bottom: 1rem;
    }
    
    .stChatInputContainer {
        background-color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.05);
    }
    
    .stChatInputContainer textarea {
        color: #0c4a6e !important;
        background-color: transparent !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #e0f2fe !important;
        border-right: 1px solid #bae6fd;
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

# Ocean Hero Header
st.markdown(
    """
    <div class="hero-header">
        <h2 style="margin: 0; font-weight: 700; color: #0369a1;">🌊 Oceanic AI Workspace</h2>
        <p style="margin: 5px 0 0 0; color: #0284c7; font-size: 1rem;">Sail through tasks, coding, and learning • Powered by Google Gemini 2.5 Flash</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Sidebar for Persona / Mode Selection
st.sidebar.markdown(
    "## ⚓ Control Deck", unsafe_allow_html=True
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
  st.sidebar.success(
      "🌊 Mode Active: **General Assistant**\n\nReady for summaries, writing,"
      " and tasks."
  )

elif persona == "AI Tutor":
  system_prompt = (
      "You are an expert, patient, and encouraging tutor. Break down concepts"
      " simply, use analogies, ask interactive questions, and guide the user"
      " step-by-step without just giving away answers right away."
  )
  st.sidebar.success(
      "🐬 Mode Active: **AI Tutor**\n\nReady to explain code, teach Python, or"
      " math."
  )

elif persona == "Project Builder":
  system_prompt = (
      "You are a master software architect and coding mentor. Help design"
      " applications, write clean code snippets, structure projects, and solve"
      " technical roadblocks."
  )
  st.sidebar.success(
      "⚓ Mode Active: **Project Builder**\n\nReady to write code and architect"
      " apps."
  )

st.sidebar.markdown("---")
st.sidebar.markdown(
    "### 🧭 Voyage Stats\n- **Cloud Host:** Streamlit Cloud\n- **Waters:**"
    " Calm & Secure\n- **Status:** Active"
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
        f"Ahoy! Your **{persona}** oceanic workspace is ready. What shall we"
        " explore or build today?"
    )

# Display chat history from session state
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# User Input Handling
if user_input := st.chat_input("Type your message or ask for code..."):
  st.session_state.messages.append({"role": "user", "content": user_input})
  with st.chat_message("user"):
    st.markdown(user_input)

  # Generate response from Gemini model
  with st.chat_message("assistant"):
    with st.spinner("🌊 Navigating thoughts..."):
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
            f"Agent error: {e}. (If this is a 503 high demand error, please try"
            " again in a moment!)"
        )