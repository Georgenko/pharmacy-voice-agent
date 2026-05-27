# pharmacy-voice-agent
An agent you can talk to who can help you with questions regarding medication


## Project structure
pharmacy-voice-agent/  
├── index.html        ← entire UI + voice logic  
├── server.py         ← tiny FastAPI app, one endpoint  
├── prompt.txt        ← your system prompt (versioned separately)  
└── README.md         ← explain your decisions, not just setup  

## Evaluate the prompt
```
pytest eval/ -v
```