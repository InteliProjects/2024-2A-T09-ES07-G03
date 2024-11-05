from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/webhook/stt")
async def webhook_stt(request: Request):
    try:
        # Recebendo o payload com a transcricao apos o stt
        request_json = await request.json()
        transcricao = request_json['transcript']
        
        # Verificando se a transcricao esta presente
        if not transcricao:
            # Caso nenhuma transcricao recebida, retornar erro
            return JSONResponse(content={"message": "Transcricao não recebida"}, status_code=400)
        
        # Retorno de sucesso com a transcricao
        return JSONResponse(content={"message": "Documentos recebidos com sucesso!", "transcricao": transcricao}, status_code=200)
    
    except Exception as e:
        # Em caso de erro, retornar uma mensagem adequada com erro 500s
        return JSONResponse(content={"error": f"Erro ao processar transcricao: {str(e)}"}, status_code=500)