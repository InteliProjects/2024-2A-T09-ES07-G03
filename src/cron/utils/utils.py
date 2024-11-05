from infra.db import DatabaseManager
import json
from fastapi import HTTPException
import logging
import os 
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

# Função para adicionar uma nova lei usando um JSON
async def add_lrr(json_str: str):
    db_manager = DatabaseManager(DATABASE_URL)    

    try:
        # Converte a string JSON para um objeto Python (dicionário)
        json_obj = json.loads(json_str)

        # Extrair os dados do JSON e converter quando necessário
        regulator = str(json_obj.get("regulator", "")).strip()  # Garantir que seja string e não seja None
        publication_date = datetime.strptime(json_obj.get("publication_date"), "%Y-%m-%d").date()  # Converter string para date
        effective_date = datetime.strptime(json_obj.get("effective_date"), "%Y-%m-%d").date()  # Converter string para date

        lrr_type = json_obj.get("lrr_type")  # Valor opcional, pode ser None
        if lrr_type is not None:
            lrr_type = str(lrr_type).strip()  # Garantir que seja string caso exista

        repealed_lrr = json_obj.get("repealed_lrr", None)  # Pode ser None
        if isinstance(repealed_lrr, str):
            # Converter string 'true' ou 'false' para booleano, se necessário
            repealed_lrr = repealed_lrr.lower() == 'true'
        elif repealed_lrr is None:
            repealed_lrr = False  # Definir um valor padrão para o campo booleano
        
        # Convertendo booleano para inteiro (1 ou 0) para o banco de dados
        repealed_lrr = bool(repealed_lrr)

        lrr_explanation = str(json_obj.get("lrr_explanation", "")).strip()  # Garantir que seja string e não seja None

        # Verificação simples para garantir que os dados obrigatórios existem
        if not regulator or not publication_date or not effective_date or not lrr_type or not lrr_explanation:
            raise HTTPException(status_code=400, detail="Dados incompletos no JSON")

        # Query para inserir a nova lei na tabela 'lrr', incluindo a coluna pdf
        query = """
        INSERT INTO lrr (regulator, publication_date, effective_date, lrr_type, repealed_lrr, lrr_explanation)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id
        """

        # Executa o comando SQL usando a função 'execute', passando pdf_bytes como último parâmetro
        lrr_id = await db_manager.execute_result(query, regulator, publication_date, effective_date, lrr_type, repealed_lrr, lrr_explanation)
        print("Lei adicionada com sucesso!", lrr_id)

        return lrr_id 

    except json.JSONDecodeError as e:
        logging.error(f"Erro ao decodificar o JSON: {e}")
        raise HTTPException(status_code=400, detail="Formato de JSON inválido")
    
    except HTTPException as e:
        logging.error(f"Erro ao adicionar a lei: {e.detail}")
        raise e