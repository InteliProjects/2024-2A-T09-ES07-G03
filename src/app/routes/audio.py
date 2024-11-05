from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
import asyncpg
import os
import uuid
import json
import logging
import assemblyai as aai
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Create a new APIRouter instance
router = APIRouter()

# Configurações do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")

# Configura a chave de API para o AssemblyAI usando uma variável de ambiente
aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')

async def save_audio_and_transcription_to_db(file_name: str, audio_bytes: bytes, transcription: str):
    """Função para salvar o áudio e a transcrição no banco de dados."""
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute("""
            INSERT INTO audio_data (file_name, audio_bytes, transcription)
            VALUES ($1, $2, $3)
        """, file_name, audio_bytes, transcription)
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=400, detail="Erro ao armazenar arquivo.")
    except Exception as e:
        logger.error(f"Erro ao salvar áudio e transcrição no banco de dados: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        await conn.close()

async def transcribe_audio(file_path: str):
    """Função para transcrever um arquivo de áudio usando AssemblyAI."""
    try:
        # Configura o AssemblyAI para detectar o idioma e transcrever o arquivo de áudio
        config = aai.TranscriptionConfig(language_detection=True)
        transcriber = aai.Transcriber(config=config)
        with open(file_path, "rb") as audio_file:
            transcript = transcriber.transcribe(audio_file)

        # Verifica se houve algum erro na transcrição
        if transcript.status == aai.TranscriptStatus.error:
            raise HTTPException(status_code=500, detail=transcript.error)

        # Retorna o texto da transcrição
        return transcript.text
    except Exception as e:
        logger.error(f"Erro ao transcrever o áudio: {e}")
        raise HTTPException(status_code=500, detail="Erro ao transcrever o áudio.")

@router.post("/record-and-transcribe-audio")
async def record_and_transcribe_audio(file: UploadFile = File(...)):
    """Endpoint para gravar o áudio, transcrever e salvar ambos no banco de dados."""
    
    try:
        # Obtém o tipo de conteúdo do arquivo enviado
        content_type = file.content_type

        # Valida o tipo de arquivo
        if content_type not in ["audio/mpeg", "audio/wav", "audio/x-wav"]:
            raise HTTPException(status_code=400, detail="Formato de arquivo inválido. Apenas arquivos .mp3 e .wav são suportados.")
        
        # Gera um nome de arquivo único
        file_name = f'{uuid.uuid4()}.wav'
        
        # Lê os bytes do arquivo enviado
        audio_bytes = await file.read()

        # Salva os bytes do áudio como um arquivo temporário
        temp_file_path = f"/tmp/{file_name}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(audio_bytes)

        # Transcreve o áudio usando AssemblyAI
        transcription = await transcribe_audio(temp_file_path)

        # Salva o áudio e a transcrição no banco de dados
        await save_audio_and_transcription_to_db(file_name, audio_bytes, transcription)

        # Cria o dicionário de resposta
        response_body = {
            "message": "Áudio gravado, transcrito e salvo com sucesso!",
            "file_name": file_name,
            "transcription": transcription
        }

        # Retorna a resposta
        return {
            'statusCode': 200,
            'body': json.dumps(response_body)
        }

    except HTTPException as e:
        # Retorna o erro HTTP com o status adequado
        logger.error(f"Erro HTTP: {e.detail}")
        raise e

    except Exception as e:
        # Retorna um erro HTTP com status 500 para erros internos do servidor
        logger.error(f"Erro interno do servidor: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
