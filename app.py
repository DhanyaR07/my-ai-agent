import os
import google.generativeai as genai
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Personal AI Workspace", page_icon="✨", layout="wide"
)

# Top Theme Selector Bar
col_title, col_theme = st.columns([3, 1])
with col_theme:
  selected_theme = st.selectbox(
      "🎨 Choose Theme", ["Sea Theme 🌊", "Light Theme ☀️", "Dark Theme 🌙"]
  )

# Define Theme Styles
if selected_theme == "Sea Theme 🌊":
  bg_color = "#f0f9ff"
  text_color = "#0c4a6e"
  sidebar_bg = "#e0f2fe"
  hero_bg = "linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%)"
  hero_border = "#7dd3fc"
  hero_text = "#0369a1"
  chat_bg = "#ffffff"
  chat_border = "#bae6fd"
  input_bg = "#ffffff"
  input_border = "#38bdf8"
  fish_display = "block"
elif selected_theme == "Light Theme ☀️":
  bg_color = "#f8fafc"
  text_color = "#0f172a"
  sidebar_bg = "#f1f5f9"
  hero_bg = "linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%)"
  hero_border = "#e2e8f0"
  hero_text = "#1e293b"
  chat_bg = "#ffffff"
  chat_border = "#e2e8f0"
  input_bg = "#ffffff"
  input_border = "#cbd5e1"
  fish_display = "none"
else:  # Dark Theme 🌙
  bg_color = "#08090d"
  text_color = "#e2e8f0"
  sidebar_bg = "#0d0f17"
  hero_bg = "linear-gradient(135deg, #12141c 0%, #1a1d2d 100%)"
  hero_border = "rgba(139, 92, 246, 0.2)"
  hero_text = "#ffffff"
  chat_bg = "#12141c"
  chat_border = "rgba(255, 255, 255, 0.08)"
  input_bg = "#12141c"
  input_border = "rgba(139, 92, 246, 0.3)"
  fish_display = "none"

# Apply Dynamic CSS with Floating Bottom Chat Bar
st.markdown(
    """
    <style>
    .stApp, .main, [data-testid="stSidebar"] {
        background-color: """
    + bg_color
    + """ !important;
        color: """
    + text_color
    + """ !important;
    }
    
    header {visibility: hidden;}

    .hero-header {
        background: """
    + hero_bg
    + """;
        border: 1px solid """
    + hero_border
    + """;
        padding: 2rem;
        border-radius: 16px;
        color: """
    + hero_text
    + """;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        position: relative;
        z-index: 2;
    }
    
    .stChatMessage {
        background-color: """
    + chat_bg
    + """ !important;
        border: 1px solid """
    + chat_border
    + """;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        color: """
    + text_color
    + """ !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        position: relative;
        z-index: 2;
    }
    
    /* Floating Bottom Chat Input Bar */
    [data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: linear-gradient(180deg, transparent 0%, """
    + bg_color
    + """ 60%) !important;
        padding: 1rem 2rem 1.5rem 2rem !important;
        z-index: 99999 !important;
    }
    
    .stChatInputContainer {
        background-color: """
    + input_bg
    + """ !important;
        border: 1px solid """
    + input_border
    + """ !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .stChatInputContainer textarea {
        color: """
    + text_color
    + """ !important;
        background-color: transparent !important;
    }

    /* Add bottom padding so chat messages don't get hidden behind the floating input */
    .block-container {
        padding-bottom: 7rem !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: """
    + sidebar_bg
    + """ !important;
        border-right: 1px solid """
    + chat_border
    + """;
    }

    .fish-tank {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        overflow: hidden;
        z-index: 1;
        display: """
    + fish_display
    + """;
    }

    .fish {
        position: absolute;
        font-size: 24px;
        animation: swim linear infinite;
        opacity: 0.7;
    }

    @keyframes swim {
        0% { transform: translateX(-100px) translateY(0px) scaleX(1); }
        50% { transform: translateX(calc(50vw)) translateY(-30px) scaleX(1); }
        100% { transform: translateX(calc(100vw + 100px)) translateY(20px) scaleX(1); }
    }

    .fish-1 { top: 15%; animation-duration: 18s; animation-delay: 0s; }
    .fish-2 { top: 35%; animation-duration: 24s; animation-delay: 4s; font-size: 20px; }
    .fish-3 { top: 60%; animation-duration: 20s; animation-delay: 2s; font-size: 28px; }
    .fish-4 { top: 80%; animation-duration: 22s; animation-delay: 6s; }
    </style>

    <div class="fish-tank">
        <div class="fish fish-1">🐠</div>
        <div class="fish fish-2">🐟</div>
        <div class="fish fish-3">🐬</div>
        <div class="fish fish-4">🐠</div>
    </div>
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
        <h2 style="margin: 0; font-weight: 700;">🚀 Personal AI Workspace</h2>
        <p style="margin: 5px 0 0 0; font-size: 1rem; opacity: 0.85;">Your custom intelligence hub • Powered by Google Gemini 2.5 Flash</p>
    </div>
""",
    unsafe_allow_html=True,
)

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
    with st.spinner("✨ Processing..."):
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