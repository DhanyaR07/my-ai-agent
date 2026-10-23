import os
import google.generativeai as genai
import streamlit as st

# Configure page settings with an ocean icon
st.set_page_config(
    page_title="Oceanic AI Workspace", page_icon="🌊", layout="wide"
)

# Custom CSS for Sea / Ocean Theme Styling
st.markdown(
    """
    <style>
    /* Main Background - Soft Ocean Mist */
    .main {
        background-color: #f0f9ff;
    }
    
    /* Hero Banner - Deep Sea Gradient */
    .hero-card {
        background: linear-gradient(135deg, #0284c7 0%, #0d9488 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.2);
    }
    
    /* Chat Bubble Styling */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    
    /* Sidebar Customization - Aquatic Tint */
    [data-testid="stSidebar"] {
        background-color: #e0f2fe;
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

# Interactive Ocean Hero Banner
st.markdown(
    """
    <div class="hero-card">
        <h1>🌊 Oceanic AI Workspace</h1>
        <p style="font-size: 1.1rem; opacity: 0.9;">Sail through tasks, coding, and learning with your deep-sea intelligence hub powered by Google Gemini 2.5 Flash.</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Sidebar for Persona / Mode Selection with Aquatic Icons
st.sidebar.markdown("## ⚓ Control Deck")
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
      "🌊 Mode Active: **General Assistant**\n\nReady for writing, summaries,"
      " and daily navigation."
  )

elif persona == "AI Tutor":
  system_prompt = (
      "You are an expert, patient, and encouraging tutor. Break down concepts"
      " simply, use analogies, ask interactive questions, and guide the user"
      " step-by-step without just giving away answers right away."
  )
  st.sidebar.success(
      "🐬 Mode Active: **AI Tutor**\n\nAsk me to explain code, teach Python,"
      " data science, or math."
  )

elif persona == "Project Builder":
  system_prompt = (
      "You are a master software architect and coding mentor. Help design"
      " applications, write clean code snippets, structure projects, and solve"
      " technical roadblocks."
  )
  st.sidebar.success(
      "⚓ Mode Active: **Project Builder**\n\nReady to write code, design apps,"
      " and anchor your projects."
  )

st.sidebar.markdown("---")
st.sidebar.markdown(
    "### 🧭 Voyage Stats\n- **Model:** Gemini 2.5 Flash\n- **Waters:** Calm &"
    " Secure\n- **Platform:** Streamlit Cloud"
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
        f"Ahoy! I am your **{persona}**. What shall we explore or build"
        " today?"
    )

# Display chat history from session state
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# User Input Handling (Unified single chat bar)
if user_input := st.chat_input("Type your message or ask for code..."):
  # Append user message to state and display
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
            f"Agent error: {e}. (If this is a 503 high demand error, Google's"
            " servers are busy—please try sending your message again in a"
            " moment!)"
        )