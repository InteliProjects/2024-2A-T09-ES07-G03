from infra.db import DatabaseManager
from fastapi import FastAPI, Depends, HTTPException, APIRouter 
from dotenv import load_dotenv
import os
import logging
from typing import Optional, List 

load_dotenv()
router = APIRouter()

DATABASE_URL = os.getenv("DATABASE_URL")
db_manager = DatabaseManager(DATABASE_URL)

@router.get("/lrr")
async def get_lrr(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    tags: Optional[List[str]] = None,
    order_by: str = 'publication_date',
    order: str = 'DESC',
):
    filters = []

    if start_date:
        filters.append(f"r.effective_date >= '{start_date}'")
    if end_date:
        filters.append(f"r.effective_date <= '{end_date}'")

    if tags:
        filters.append("t.tag_name IN ({})".format(','.join(f"'{tag}'" for tag in tags)))

    try:
        base_query = """
        SELECT 
            r.id, 
            r.effective_date, 
            r.file_url, 
            r.lrr_explanation, 
            r.lrr_type, 
            r.publication_date, 
            r.regulator, 
            STRING_AGG(t.tag_name, ', ') AS tag_names
        FROM 
            lrr r
        LEFT JOIN 
            lrr_tag rt ON r.id = rt.lrr_id
        LEFT JOIN 
            tag t ON rt.tag_id = t.id
        """

        if filters:
            base_query += " WHERE " + " AND ".join(filters)

        base_query += f" GROUP BY r.id ORDER BY {order_by} {order}"

        result = await db_manager.execute_query(base_query)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Erro na rota get_lrr: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/lrr_yesterday")
async def fetch_yestarday_lrr():
    try:
        result = await db_manager.fetch_yestarday_lrr()
        return result
    except HTTPException as e:
        raise e
