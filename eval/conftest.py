import os
import pytest
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])


def load_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompt.txt")
    with open(prompt_path) as f:
        return f.read()


def ask_text_bot(user_message: str) -> str:
    """Send a message to the text bot and return its response."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": load_prompt()},
            {"role": "user", "content": user_message},
        ],
        temperature=0,  # deterministic outputs for testing
    )
    return response.choices[0].message.content


def ask_text_bot_with_history(conversation: list[dict]) -> str:
    """Send a conversation history to the text bot and return its response."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": load_prompt()},
            *conversation,
        ],
        temperature=0,
    )
    return response.choices[0].message.content


def evaluate_response(response: str, rubric: str) -> tuple[bool, str]:
    """
    Ask an LLM to evaluate a response against a rubric.
    Returns (passed: bool, reasoning: str)
    """
    judge_prompt = f"""You are evaluating an AI assistant response against a rubric.

Response to evaluate:
{response}

Rubric (what the response MUST do):
{rubric}

Reply with exactly two lines:
PASS or FAIL
One sentence explaining why."""

    result = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": judge_prompt}],
        temperature=0,
    )
    text = result.choices[0].message.content.strip()
    lines = text.splitlines()
    passed = lines[0].strip().upper() == "PASS"
    reasoning = lines[1].strip() if len(lines) > 1 else text
    return passed, reasoning


@pytest.fixture
def text_bot():
    return ask_text_bot
