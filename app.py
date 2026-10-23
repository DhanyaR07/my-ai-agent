import os
import google.generativeai as genai
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="AI Workspace", page_icon="✨", layout="wide"
)

# Custom CSS for 100% Pure Cohesive Light Theme
st.markdown(
    """
    <style>
    /* Force full light background across the entire app and sidebar */
    .stApp, .main, [data-testid="stSidebar"] {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }
    
    /* Hide Streamlit default top header */
    header {visibility: hidden;}

    /* Hero Header Card */
    .hero-header {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        padding: 2rem;
        border-radius: 16px;
        color: #0f172a;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    }
    
    /* Telemetry Stat Cards */
    .stat-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        flex: 1;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
    }
    
    /* Chat Message Bubbles for Light Mode */
    .stChatMessage {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        color: #0f172a !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }
    
    /* Bottom Chat Input Bar for Light Mode */
    [data-testid="stChatInput"] {
        background-color: #f8fafc !important;
        border-top: 1px solid #e2e8f0;
        padding-bottom: 1rem;
    }
    
    .stChatInputContainer {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
    }
    
    .stChatInputContainer textarea {
        color: #0f172a !important;
        background-color: transparent !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #f1f5f9 !important;
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

# Hero Header
st.markdown(
    """
    <div class="hero-header">
        <h2 style="margin: 0; font-weight: 700; color: #1e293b;">🚀 Personal AI Workspace</h2>
        <p style="margin: 5px 0 0 0; color: #64748b; font-size: 1rem;">Your custom intelligence hub • Powered by Google Gemini 2.5 Flash</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Stat Cards Row
col1, col2, col3, col4 = st.columns(4)
with col1:
  st.markdown(
      """
        <div class="stat-card">
            <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">System Status</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #16a34a; margin-top: 5px;">ONLINE</div>
        </div>
    """,
      unsafe_allow_html=True,
  )
with col2:
  st.markdown(
      """
        <div class="stat-card">
            <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">AI Model</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #2563eb; margin-top: 5px;">Gemini 2.5</div>
        </div>
    """,
      unsafe_allow_html=True,
  )
with col3:
  st.markdown(
      """
        <div class="stat-card">
            <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">Security</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #7c3aed; margin-top: 5px;">SECURE</div>
        </div>
    """,
      unsafe_allow_html=True,
  )
with col4:
  st.markdown(
      """
        <div class="stat-card">
            <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">Uptime</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #db2777; margin-top: 5px;">100%</div>
        </div>
    """,
      unsafe_allow_html=True,
  )

st.markdown("<br>", unsafe_allow_html=True)

# Sidebar for Persona / Mode Selection
st.sidebar.markdown(
    "## 🎛️ Control Panel", unsafe_allow_html=True
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
      "💡 **Mode:** General Assistant\n\nReady to help with summaries, writing,"
      " and tasks."
  )

elif persona == "AI Tutor":
  system_prompt = (
      "You are an expert, patient, and encouraging tutor. Break down concepts"
      " simply, use analogies, ask interactive questions, and guide the user"
      " step-by-step without just giving away answers right away."
  )
  st.sidebar.info(
      "📚 **Mode:** AI Tutor\n\nReady to explain code, teach Python, or math."
  )

elif persona == "Project Builder":
  system_prompt = (
      "You are a master software architect and coding mentor. Help design"
      " applications, write clean code snippets, structure projects, and solve"
      " technical roadblocks."
  )
  st.sidebar.info(
      "💻 **Mode:** Project Builder\n\nReady to write code and architect apps."
  )

st.sidebar.markdown("---")
st.sidebar.markdown(
    "### 📊 Dashboard Info\n- **Cloud Host:** Streamlit Cloud\n- **Access"
    " Level:** Unlimited\n- **Status:** Active"
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
        f"Hello! Your **{persona}** workspace is ready. How can I help you"
        " excel today?"
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
    with st.spinner("✨ Thinking..."):
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