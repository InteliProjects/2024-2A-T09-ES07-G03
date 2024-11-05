import schedule
import time
from cron.utils.text_utils import TextUtils
from cron.scraping.llm import Llm
import requests
from infra.db import DatabaseManager
import os
from cron.utils.utils import add_lrr
import asyncio
from cron.scraping.scraping import main as scraping_main
from app.routes.lrr_tagController import add_tag_to_lrr
from app.routes.tagsController import get_tags

text_utils = TextUtils()
llm = Llm()
DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)
db_manager = DatabaseManager(
    'postgres://user-m7:password-m7@db:5432/database-m7')


async def data_scraping_routine():
    try:
        print("Iniciando scraping")

        scraping_main()

        print("Scraping finalizado")

        # Obtém o diretório atual
        root = './'

        # Obtém todos os arquivos .pdf na raiz do diretório
        pdf_files = [f for f in os.listdir(root) if f.endswith('.pdf')]

        tags = await get_tags()

        # Itera sobre cada arquivo PDF encontrado
        for pdf in pdf_files:
            text = text_utils.extract_text_from_pdf(pdf)
            json_str = llm.interpret_lrr(text)
            # recebe os tags e os tags selecionados
            selected_tags = llm.tagging(text, tags)
            lrr_id = await add_lrr(json_str)
            print('lrr ID: ', lrr_id)

            data = {
                "lrr_id": lrr_id,
                "tag_ids": selected_tags
            }

            print('data: ', data)

            try:
                await add_tag_to_lrr(data)
            except Exception as e:
                print('Erro ao adicionar tags à LRR:', e)

    except Exception as e:
        print('Erro:', e)


def run_data_scraping_routine():
    asyncio.run(data_scraping_routine())


schedule.every().day.at("07:00").do(run_data_scraping_routine)
# schedule.every(5).seconds.do(run_data_scraping_routine)


def main():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
