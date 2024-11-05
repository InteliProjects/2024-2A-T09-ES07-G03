from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/webhook/new_documents")
async def new_documents_webhook(request: Request):
    try:
        # Recebendo o payload de documentos
        documentos = await request.json()
        
        # Verificando se algum documento foi enviado
        if not documentos:
            # Notificação de ausência de documentos
            return JSONResponse(content={"message": "Nenhum documento foi lançado"}, status_code=200)
        
        # Processando os documentos recebidos (ex: enviar para o frontend)
        print(f"Novos documentos recebidos: {documentos}")
        
        # Retorno de sucesso com a lista de documentos
        return JSONResponse(content={"message": "Documentos recebidos com sucesso!", "documentos": documentos}, status_code=200)
    
    except Exception as e:
        # Em caso de erro, retornar uma mensagem adequada
        return JSONResponse(content={"error": f"Erro ao processar documentos: {str(e)}"}, status_code=500)
    


@router.get("/webhook/")
async def new_documents_webhook():
    return 'botafogo!!!'