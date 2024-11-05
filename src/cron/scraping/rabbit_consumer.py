import pika
import psycopg2
import os
import json
import ast

AQMP_URL = os.getenv("RABBIT_URL")
QUEUE_NAME = "normas"

# Conexão com o banco de dados usando a string do .env
DATABASE_URL = os.getenv("DATABASE_URL")

MAPPING = {
    "Ofício Circular": "oficio",
    "Comunicado Externo": "comunicado",
    "Instrução Normativa": "instrucao_normativa",
}

def save_message_to_db(message):
    """Função para salvar a mensagem no banco de dados"""
    try:
        # Conectando ao banco de dados PostgreSQL
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Extrair os dados da mensagem JSON
        title = message.get('title')
        url = message.get('url')
        date = message.get('date')
        type = message.get('type')

        type = MAPPING.get(type, type)

        date = date.split("/")
        date = f"{date[2]}-{date[1]}-{date[0]}"

        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Date: {date}")

        # Inserir os dados na tabela lrr
        cursor.execute("""
            INSERT INTO lrr (regulator, publication_date, effective_date, lrr_type, repealed_lrr, file_url, lrr_explanation)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (title, date, date, type, False, url, ""))

        # Commit da transação
        conn.commit()

        # Fechar cursor e conexão
        cursor.close()
        conn.close()

        print(f" [x] Message saved to DB: {message}")
    except Exception as e:
        print(f"Error saving message to DB: {e}")


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    message_str = body.decode(
        "utf-8"
    )

    try:
        message = ast.literal_eval(message_str)
        save_message_to_db(message)
    except (ValueError, SyntaxError) as e:
        print(f"Failed to decode message: {e}")


def main():
    # Conexão com o servidor RabbitMQ
    params = pika.URLParameters(AQMP_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Criando a fila
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Consumindo as mensagens
    channel.basic_consume(
        queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

    print(f" [*] Waiting for messages in {QUEUE_NAME}. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()
