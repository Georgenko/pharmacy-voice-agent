import os

TEXT_MODEL = os.environ.get("GROQ_TEXT_MODEL", "openai/gpt-oss-120b")
STT_MODEL = os.environ.get("GROQ_STT_MODEL", "whisper-large-v3-turbo")