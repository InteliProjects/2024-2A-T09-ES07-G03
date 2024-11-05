from infra.db import DatabaseManager
from fastapi import HTTPException, APIRouter
from dotenv import load_dotenv
import os
import logging
from typing import Dict, Optional, List

load_dotenv()
router = APIRouter()

DATABASE_URL = os.getenv("DATABASE_URL")
db_manager = DatabaseManager(DATABASE_URL)

@router.get("/tags")
async def get_tags():   
    try:
        query = "SELECT tag_name FROM tag"
        result = await db_manager.fetch_all(query)
        return result
    except Exception as e:
        logging.error(f"Erro ao buscar tags: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/tags")
async def add_tag(tag_data: Dict[str, str]):
    try:
        # Extraindo os dados do JSON
        tag_name = tag_data.get("tag_name")
        tag_explanation = tag_data.get("tag_explanation")

        if not tag_name or not tag_explanation:
            raise HTTPException(status_code=400, detail="tag_name ou tag_explanation ausentes.")
        
        # Inserção da nova tag usando placeholders do PostgreSQL
        query_insert = """
        INSERT INTO tag (tag_name, tag_explanation)
        VALUES ($1, $2)
        """
        
        # Execução da query com os valores desestruturados
        await db_manager.execute_query(query_insert, (tag_name, tag_explanation))

        return {"message": "Tag adicionada com sucesso!"}
    except Exception as e:
        logging.error(f"Erro ao adicionar tag: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# Rota para excluir uma tag pelo ID
@router.delete("/tags/{tag_id}")
async def delete_tag(tag_id: int):
    try:
        # Excluir a tag
        query_delete = "DELETE FROM tag WHERE id = $1"
        await db_manager.execute_query(query_delete, (tag_id,))
        return {"message": "Tag excluída com sucesso!"}
    except Exception as e:
        logging.error(f"Erro ao excluir tag: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
