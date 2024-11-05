from http.client import HTTPException
import asyncpg
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url

    async def connect(self):
        """Conecta ao banco de dados e retorna a conexão."""
        return await asyncpg.connect(self.database_url)

    async def execute(self, query: str, *args) -> None:
        """Executa um comando SQL que não retorna resultados (e.g., INSERT, UPDATE)."""
        conn = await self.connect()
        try:
            await conn.execute(query, *args)
        except asyncpg.UniqueViolationError as e:
            logger.error(f"Erro de violação de unicidade: {e}")
            raise HTTPException(status_code=400, detail="Erro ao armazenar registro no banco de dados.")
        except Exception as e:
            logger.error(f"Erro ao executar comando no banco de dados: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            await conn.close()

    async def execute_result(self, query: str, *args) -> Optional[Any]:
        """Executa um comando SQL que pode retornar resultados (e.g., INSERT com RETURNING)."""
        conn = await self.connect()
        try:
            # Usa fetchrow para obter o resultado da consulta com RETURNING
            result = await conn.fetchrow(query, *args)
            if result:
                # Retorna o primeiro valor do resultado, que deve ser o ID retornado
                return result[0]
            else:
                return None
        except asyncpg.UniqueViolationError as e:
            logger.error(f"Erro de violação de unicidade: {e}")
            raise HTTPException(status_code=400, detail="Erro ao armazenar registro no banco de dados.")
        except Exception as e:
            logger.error(f"Erro ao executar comando no banco de dados: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            await conn.close()

    async def execute_query(self, query, params=None):
        conn = await asyncpg.connect(self.database_url)
        try:
            if params:
                result = await conn.fetch(query, *params.values())
            else:
                result = await conn.fetch(query)
            return result
        finally:
            await conn.close()

    async def fetch_one(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Executa uma consulta SQL e retorna um único registro como dicionário."""
        conn = await self.connect()
        try:
            result = await conn.fetchrow(query, *args)
            return dict(result) if result else None
        except Exception as e:
            logger.error(f"Erro ao buscar registro no banco de dados: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            await conn.close()

    async def fetch_all(self, query: str, *args) -> List[Dict[str, Any]]:
        """Executa uma consulta SQL e retorna todos os resultados como uma lista de dicionários."""
        conn = await self.connect()
        try:
            results = await conn.fetch(query, *args)
            return [dict(record) for record in results]
        except Exception as e:
            logger.error(f"Erro ao buscar registros no banco de dados: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            await conn.close()

    async def fetch_with_filters(self, filters: Dict[str, Any] = None, order_by: str = 'publication_date', order: str = 'DESC', has_repealed: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Executa uma consulta na tabela 'lrr' com possibilidade de filtros, incluindo se revoga alguma lei."""
        conn = await self.connect()
        try:
            # Base da consulta SQL
            query = "SELECT * FROM lrr WHERE 1=1"

            # Lista de argumentos para a consulta
            args = []

            # Construção dinâmica dos filtros
            if filters:
                for key, value in filters.items():
                    if isinstance(value, str):
                        # Converte campo enum para texto para usar ILIKE
                        if key == 'lrr_type':  # Supondo que lrr_type é o campo enum
                            query += f" AND {key}::text ILIKE $%d" % (len(args) + 1)
                        else:
                            query += f" AND {key} ILIKE $%d" % (len(args) + 1)
                    else:
                        query += f" AND {key} = $%d" % (len(args) + 1)
                    args.append(value)

            # Filtro para revogação de leis
            if has_repealed is not None:
                if has_repealed:
                    query += " AND repealed_lrr IS NOT NULL AND repealed_lrr != ''"
                else:
                    query += " AND (repealed_lrr IS NULL OR repealed_lrr = '')"

            # Adiciona ordenação
            query += f" ORDER BY {order_by} {order}"

            # Executa a consulta
            results = await conn.fetch(query, *args)
            return [dict(record) for record in results]
        except Exception as e:
            logger.error(f"Erro ao buscar registros no banco de dados: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            await conn.close()

    async def fetch_yestarday_lrr(self) -> List[Dict[str, Any]]:
        """Busca todas as leis inseridas no dia de ontem."""
        conn = await self.connect()
        try:
            # Obtem a data de ontem
            yesterday = (datetime.utcnow() - timedelta(days=1)).date()

            # Base da consulta SQL
            query = """
            SELECT * FROM lrr
            WHERE publication_date >= $1 AND publication_date < $2
            ORDER BY publication_date DESC
            """

            # Define o intervalo de data para o dia de ontem
            start_of_yesterday = datetime.combine(yesterday, datetime.min.time())
            start_of_today = datetime.combine(datetime.utcnow().date(), datetime.min.time())

            # Executa a consulta com os parâmetros
            results = await conn.fetch(query, start_of_yesterday, start_of_today)

            # Retorna os resultados como uma lista de dicionários
            return [dict(record) for record in results]
        except Exception as e:
            logger.error(f"Erro ao buscar registros do dia de ontem no banco de dados: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            await conn.close()
