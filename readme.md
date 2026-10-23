# Personal AI Agent (Python & Google Gemini API)

A lightweight, modular, tool-calling AI agent built in Python using the official [Google GenAI SDK](https://ai.google.dev/gemini-api/docs/api-key) (`google-genai`) and the `gemini-2.5-flash` model. Instead of only generating text, this agent autonomously decides when to invoke custom Python functions to search the live web, evaluate mathematical expressions, check the local date and time, and save research notes to disk while maintaining multi-turn conversational memory.

## Key Capabilities

| Tool Function | Capability | Underlying Library |
| :--- | :--- | :--- |
| `search_web(query, max_results)` | Searches the live web and returns top titles, snippets, and URLs | `duckduckgo-search` |
| `calculate(expression)` | Evaluates arithmetic and scientific math expressions safely | Python `math` |
| `save_note(filename, content)` | Saves generated notes, summaries, or markdown files to `notes/` | Python `pathlib` |
| `get_current_datetime()` | Retrieves the exact local date, time, and day of the week | Python `datetime` |

## Project Architecture

| File | Role in the Project |
| :--- | :--- |
| `main.py` | Interactive command-line interface (CLI) loop for chatting with the agent |
| `agent.py` | Core `PersonalAgent` class managing Gemini API configuration, tool registration, and chat memory |
| `tools.py` | Custom Python tool functions with type annotations and docstrings for automatic function calling |
| `requirements.txt` | Python package dependencies (`google-genai`, `python-dotenv`, `duckduckgo-search`) |
| `.env` | Local environment variable file storing `GEMINI_API_KEY` (excluded from Git via `.gitignore`) |

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/my-ai-agent.git
cd my-ai-agent
```

### 2. Install Dependencies

Ensure Python 3.10+ is installed, then install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Configure Your Free Gemini API Key

1. Generate a free API key from [Google AI Studio API Keys](https://aistudio.google.com/app/apikey).
2. Create a `.env` file in the root directory of the project:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 4. Run the Agent

```bash
python main.py
```

## Example Prompts to Try

* **Live Web Search & Note Saving**: *"Search the web for the top 3 features in Python 3.12 and save a short summary to python_features.md"*
* **Math Calculation**: *"Calculate sqrt(2025) * 18 + 340"*
* **Date & Time Awareness**: *"What is the current local date and time, and how many days are left in this month?"*

## Adding Your Own Custom Tools

To give the agent a new skill:

1. Write a new Python function inside `tools.py` with clear type hints (such as `str` or `int`) and a descriptive docstring explaining its arguments and return value.
2. Add the function name to the `AGENT_TOOLS` list at the bottom of `tools.py`.
3. Restart `python main.py`—the Gemini SDK automatically inspects your function signature and makes it available to the agent.
