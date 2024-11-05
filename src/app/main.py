import os
from fastapi import FastAPI
from app.routes import audio
from app.routes import webhook_notify
from app.routes import webhook_stt
from app.routes import lrrController 
from app.routes import tagsController
from app.routes import lrr_tagController
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Include STT router
app.include_router(audio.router)
app.include_router(webhook_notify.router)
app.include_router(webhook_stt.router)
app.include_router(webhook_stt.router)
app.include_router(lrrController.router)
app.include_router(tagsController.router)
app.include_router(lrr_tagController.router)

@app.get("/", response_class=HTMLResponse)
async def get_index():
    # Get the absolute path of the file based on the current file location
    file_path = os.path.join(os.path.dirname(__file__), "../frontend/public/index.html")
    with open(file_path, "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())
