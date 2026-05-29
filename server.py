import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from groq import Groq, BadRequestError
from pydantic import BaseModel

from constants import TEXT_MODEL

app = FastAPI()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    audio_bytes = await audio.read()
    if len(audio_bytes) < 5000:  # ignore tiny/empty recordings
        return {"text": ""}
    try:
        transcription = client.audio.transcriptions.create(
            file=(audio.filename, audio_bytes, audio.content_type),
            model="whisper-large-v3-turbo",
        )
        return {"text": transcription.text}
    except BadRequestError:
        return {"text": ""}

@app.post("/chat")
async def chat(req: ChatRequest):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += req.history
    messages.append({"role": "user", "content": req.message})

    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=messages,
        max_tokens=150,  # keep responses short for voice
    )
    reply = response.choices[0].message.content
    return {"reply": reply}

app.mount("/", StaticFiles(directory=".", html=True), name="static")
