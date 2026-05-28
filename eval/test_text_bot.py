from conftest import ask_text_bot, evaluate_response

def test_no_filler_phrases():
    response = ask_text_bot("How do I check my order status?")
    forbidden = ["certainly", "great question", "absolutely", "of course", "sure!"]
    lowered = response.lower()
    for phrase in forbidden:
        assert phrase not in lowered, f"Response contains filler phrase '{phrase}': {response}"

def test_response_is_short():
    response = ask_text_bot("What is paracetamol?")
    word_count = len(response.split())
    assert word_count < 50, f"Response too long ({word_count} words): {response}"

def test_no_hallucinated_ui():
    response = ask_text_bot("How do I check my order status?")
    assert_judge(
        response,
        "The response must NOT mention specific UI elements like button names, "
        "menu items, or navigation steps such as 'Order History', 'My Orders', "
        "or 'click here'. Telling the user to check the app directly is acceptable."
    )

def test_out_of_scope_weather():
    response = ask_text_bot("What's the weather like in Berlin today?")
    assert_judge(
        response,
        "The response must decline to answer and redirect to pharmacy-related topics."
    )

# ── Helpers ───────────────────────────────────────────────────────────────────
def assert_judge(response: str, rubric: str):
    passed, reasoning = evaluate_response(response, rubric)
    assert passed, f"FAILED rubric: '{rubric}'\nReasoning: {reasoning}\nResponse was: {response}"