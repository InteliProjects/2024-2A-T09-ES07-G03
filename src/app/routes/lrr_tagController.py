from infra.db import DatabaseManager
from fastapi import HTTPException, APIRouter, Body
from dotenv import load_dotenv
import os
import logging
from typing import Dict, Optional, List
import json

load_dotenv()
router = APIRouter()

DATABASE_URL = os.getenv("DATABASE_URL")
db_manager = DatabaseManager(DATABASE_URL)

@router.post("/lrr_tags")
async def add_tag_to_lrr(data: Dict[str, List[int]] = Body(...)):
    try:
        # Extraindo os dados do JSON
        lrr_id = data.get("lrr_id")
        tags_names = data.get("tag_ids")

        if isinstance(tags_names, str):
            tags_names = json.loads(tags_names)

        print(lrr_id)
        print(tags_names)

        tag_ids = []

        for tag_name in tags_names:
            print(tag_name)
            query = "SELECT id FROM tag WHERE tag_name = $1"
            tag_id = await db_manager.fetch_all(query, tag_name)
            tag_ids.append(tag_id[0]['id'])
        
        print("IDs das tags:", tag_ids)

        if not lrr_id or not tag_ids:
            raise HTTPException(status_code=400, detail="lrr_id ou tag_ids ausentes.")

        # Para cada tag_id fornecido, inserimos na tabela lrr_tag
        for tag_id in tag_ids:
            query_insert = """
            INSERT INTO lrr_tag (lrr_id, tag_id)
            VALUES ($1, $2)
            """
            await db_manager.execute(query_insert, lrr_id, tag_id)

        return {"message": "Tags adicionadas à LRR com sucesso!"}
    except Exception as e:
        logging.error(f"Erro ao adicionar tags à LRR: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/lrr/{lrr_id}/tags")
async def remove_tag_from_lrr(lrr_id: int, tag_ids: List[int]):
    try:
        # Para cada tag_id fornecido, removemos da tabela lrr_tag
        for tag_id in tag_ids:
            query_delete = """
            DELETE FROM lrr_tag
            WHERE lrr_id = $1 AND tag_id = $2
            """
            await db_manager.execute_query(query_delete, (lrr_id, tag_id))

        return {"message": "Tags removidas da LRR com sucesso!"}
    except Exception as e:
        logging.error(f"Erro ao remover tags da LRR: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
