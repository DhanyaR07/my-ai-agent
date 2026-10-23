import os
<<<<<<< HEAD
import streamlit as st
from agent import PersonalAgent

st.set_page_config(
    page_title="Personal AI Agent",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Personal AI Agent")
st.caption("Powered by Google Gemini 2.5 Flash • Web Search • Math • Notes • Live Date/Time")

# Load GEMINI_API_KEY from Streamlit Cloud Secrets if deployed online
if "GEMINI_API_KEY" in st.secrets and not os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

# Initialize the agent and chat history once per user session
if "agent" not in st.session_state:
    try:
        st.session_state.agent = PersonalAgent()
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hi! I'm your AI Agent. Ask me to search the web, calculate math, check the date/time, or save a note.",
            }
        ]
    except Exception as e:
        st.error(f"Configuration Error: {e}")
        st.stop()

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle new user input
if prompt := st.chat_input("Ask your agent anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking and running tools..."):
            reply = st.session_state.agent.ask(prompt)
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
=======
import google.generativeai as genai
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="My Unlimited Personal AI", page_icon="💡", layout="wide"
)

# Sidebar Navigation for Modes
st.sidebar.title("🛠️ Control Panel")
app_mode = st.sidebar.selectbox(
    "Choose AI Persona/Mode",
    [
        "💬 General Assistant",
        "🎓 AI Tutor (Learn Anything)",
        "🚀 Project Builder & Architect",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Tip:** This app runs locally on your machine with unlimited flexibility"
    " using your Gemini API connection!"
)

# 1. Load API Key Safely
gemini_api_key = None
try:
  gemini_api_key = st.secrets.get("GEMINI_API_KEY")
except Exception:
  pass

if not gemini_api_key:
  gemini_api_key = os.getenv("GEMINI_API_KEY")

# Main Interface Header
st.title("💡 Personal AI Workspace")

if not gemini_api_key:
  st.error(
      "❌ GEMINI_API_KEY is missing. Please add it to your"
      " `.streamlit/secrets.toml` file."
  )
else:
  try:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Define system instructions or prompt prefixes based on mode
    system_prompt = ""
    if app_mode == "🎓 AI Tutor (Learn Anything)":
      system_prompt = (
          "You are an expert, patient, and encouraging tutor. Break down"
          " concepts simply, use analogies, ask interactive questions, and"
          " guide the user step-by-step without just giving away answers right"
          " away."
      )
      st.subheader("🎓 AI Tutor Mode")
      st.write(
          "Ask me to explain code, teach you Python, data science, math, or"
          " any subject!"
      )

    elif app_mode == "🚀 Project Builder & Architect":
      system_prompt = (
          "You are a master software architect and project planner. Help the"
          " user design applications, structure directories, write code snippets,"
          " and solve engineering blockers."
      )
      st.subheader("🚀 Project Builder Mode")
      st.write(
          "Let's build projects together! Tell me what you want to create."
      )

    else:
      system_prompt = (
          "You are a helpful, multi-talented personal assistant capable of"
          " handling math, notes, and general inquiries."
      )
      st.subheader("💬 General Assistant Mode")

    # Session State Management for Chat History
    if "messages" not in st.session_state:
      st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
      with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # User Input Handling
    if user_input := st.chat_input("Type your message here..."):
      st.session_state.messages.append({"role": "user", "content": user_input})
      with st.chat_message("user"):
        st.markdown(user_input)

      # Generate response with the selected persona context
      with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
          try:
            # Combine system prompt context with user query
            full_prompt = f"{system_prompt}\n\nUser Query: {user_input}"
            response = model.generate_content(full_prompt)
            ai_response = response.text
            st.markdown(ai_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_response}
            )
          except Exception as e:
            st.error(f"Error generating response: {e}")

  except Exception as e:
    st.error(f"Failed to configure AI model: {e}")
>>>>>>> 157167f (Initial commit: Personal AI Agent with Gemini API and custom tools)
