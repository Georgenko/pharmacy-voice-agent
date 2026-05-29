# pharmacy-voice-agent

A voice assistant for a digital pharmacy platform. Talk to MediBot to get help with e-prescriptions, medication ordering, pharmacy pickup and delivery, finding pharmacies or doctors, and general medication information.

> Voice interface powered by a Whisper (STT) → LLaMA (LLM) → Browser SpeechSynthesis (TTS) pipeline via Groq.

---

## Project structure

```
pharmacy-voice-agent/
├── index.html            ← app shell
├── static/
│   └── app.js            ← voice recording + pipeline logic
├── server.py             ← FastAPI app (STT → LLM → TTS endpoint)
├── prompt.txt            ← system prompt, edit here to change MediBot's behavior
├── constants.py          ← model strings and shared config
├── eval/
│   ├── conftest.py       ← test setup and fixtures
│   └── test_text_bot.py  ← regression tests (LLM-as-judge)
└── README.md
```

## Prerequisites

This project uses [Groq](https://console.groq.com/) for free access to Whisper and LLaMA models. Create a free account and generate an API key.

> The server expects the key to be named `GROQ_API_KEY`. The model strings in `constants.py` are Groq-compatible — if you swap in a different provider, update both the key name and model strings there.

## Run locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
 
export GROQ_API_KEY=your_key_here

uvicorn server:app --reload
```

## Run regression suite

The eval suite uses LLM-as-judge to test MediBot's responses against expected behavior (scope boundaries, safety guardrails, clarification logic).

```bash
python -m pytest eval/ -v
```
