import os
import google.generativeai as genai
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Personal AI Agent Workspace", page_icon="🤖", layout="wide"
)

# Custom CSS for Modern, Interactive UI
st.markdown(
    """
    <style>
    /* Main Background & Font Styling */
    .main {
        background-color: #f8fafc;
    }
    
    /* Custom Chat Bubble Styling */
    .stChatMessage {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    /* Header Card Styling */
    .hero-card {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Sidebar customization */
    [data-testid="stSidebar"] {
        background-color: #f1f5f9;
        border-right: 1px solid #e2e8f0;
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

# Interactive Hero Banner
st.markdown(
    """
    <div class="hero-card">
        <h1>🤖 Personal AI Agent Workspace</h1>
        <p style="font-size: 1.1rem; opacity: 0.9;">Your custom, unlimited-access intelligence hub powered by Google Gemini 2.5 Flash.</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Sidebar for Persona / Mode Selection with Icons
st.sidebar.markdown("## 🎛️ Control Panel")
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
      "🟢 Mode Active: **General Assistant**\n\nReady for writing, summaries,"
      " and daily tasks."
  )

elif persona == "AI Tutor":
  system_prompt = (
      "You are an expert, patient, and encouraging tutor. Break down concepts"
      " simply, use analogies, ask interactive questions, and guide the user"
      " step-by-step without just giving away answers right away."
  )
  st.sidebar.success(
      "🔵 Mode Active: **AI Tutor**\n\nAsk me to explain code, teach Python,"
      " data science, or math."
  )

elif persona == "Project Builder":
  system_prompt = (
      "You are a master software architect and coding mentor. Help design"
      " applications, write clean code snippets, structure projects, and solve"
      " technical roadblocks."
  )
  st.sidebar.success(
      "🟣 Mode Active: **Project Builder**\n\nReady to write code, design apps,"
      " and fix bugs."
  )

st.sidebar.markdown("---")
st.sidebar.markdown(
    "### ⚡ Quick Stats\n- **Model:** Gemini 2.5 Flash\n- **Status:** Online"
    " & Secure\n- **Cloud:** Streamlit Cloud"
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

# Display interactive welcome message if chat is empty
if not st.session_state.messages:
  with st.chat_message("assistant"):
    st.markdown(
        f"Hello! I am your **{persona}**. How can I help you excel today?"
    )

# Display chat history from session state
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# User Input Handling (Unified clean bar)
if user_input := st.chat_input("Type your message or ask for code..."):
  # Append user message to state and display
  st.session_state.messages.append({"role": "user", "content": user_input})
  with st.chat_message("user"):
    st.markdown(user_input)

  # Generate response from Gemini model
  with st.chat_message("assistant"):
    with st.spinner("✨ Crafting response..."):
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
            f"Agent error: {e}. (If this is a 503 high demand error, Google's"
            " servers are busy—please try sending your message again in a"
            " moment!)"
        )