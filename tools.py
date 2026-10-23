import datetime
import math
from pathlib import Path
from duckduckgo_search import DDGS


def search_web(query: str, max_results: int = 5) -> str:
    """Searches the web using DuckDuckGo and returns top results with titles, snippets, and URLs.

    Args:
        query: The search query string to look up on the web.
        max_results: Maximum number of results to return (default is 5).

    Returns:
        A formatted string containing the search results.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return f"No results found for query: '{query}'."

        formatted = []
        for idx, item in enumerate(results, start=1):
            title = item.get("title", "Untitled")
            body = item.get("body", "")
            href = item.get("href", "")
            formatted.append(f"{idx}. {title}\n   Snippet: {body}\n   URL: {href}")
        return "\n\n".join(formatted)
    except Exception as e:
        return f"Error performing web search: {e}"


def calculate(expression: str) -> str:
    """Evaluates a mathematical expression safely (e.g., '25 * 48 + sqrt(144)').

    Args:
        expression: A mathematical expression string to evaluate.

    Returns:
        The calculated result as a string.
    """
    allowed_names = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    allowed_names.update({"abs": abs, "round": round, "min": min, "max": max})
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"Result: {result}"
    except Exception as e:
        return f"Error evaluating math expression '{expression}': {e}"


def save_note(filename: str, content: str) -> str:
    """Saves text content to a local file inside the 'notes' folder.

    Args:
        filename: Name of the file to save (e.g., 'summary.txt' or 'ideas.md').
        content: The text content to write into the file.

    Returns:
        Confirmation message with the saved file path.
    """
    try:
        notes_dir = Path("notes")
        notes_dir.mkdir(exist_ok=True)
        safe_name = Path(filename).name
        file_path = notes_dir / safe_name
        file_path.write_text(content, encoding="utf-8")
        return f"Successfully saved note to {file_path.resolve()}"
    except Exception as e:
        return f"Error saving file '{filename}': {e}"


def get_current_datetime() -> str:
    """Returns the current local date and time.

    Returns:
        Current date and time formatted as YYYY-MM-DD HH:MM:SS.
    """
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S (%A)")


# List of all tools exposed to the Gemini agent
AGENT_TOOLS = [
    search_web,
    calculate,
    save_note,
    get_current_datetime,
]