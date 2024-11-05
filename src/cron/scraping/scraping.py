import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import pika
from dotenv import load_dotenv


load_dotenv()

QUEUE_NAME = "normas"
QUEUE_URL = os.getenv("RABBIT_URL")

# Retira o conteúdo da pagina
def get_page(url):
    # Fazer a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)
    response.raise_for_status()

    # Criar o objeto BeautifulSoup para parsear o HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup

# Retorna a string do dia anterior
def get_yesterday_str():
    # Identificar a data do dia anterior
    yesterday = datetime.now() - timedelta(1)
    yesterday_str = yesterday.strftime('%d/%m/%Y')

    yesterday_str = yesterday.strftime('%d/%m/%Y').split(" ")[0]

    return yesterday_str

# Baixa o pdf, dada uma url e o nome do pdf
def download_pdf(pdf_url, pdf_name):
    pdf_response = requests.get(pdf_url)
    with open(pdf_name, 'wb') as pdf_file:
        pdf_file.write(pdf_response.content)

# Função para publicar a mensagem na fila
def publish_message(message):
    params = pika.URLParameters(QUEUE_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # transforma a mensagem em bytes
    message = str(message).encode()

    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # torna a mensagem persistente
        )
    )

    print(f" [x] Sent {message}")

    connection.close()

# Itera pelos conteúdos e seleciona pela data de ontem
def get_pdfs(download_links):
    yesterday_str = get_yesterday_str()
    # Loop através dos links para verificar se o documento é do dia anterior
    for link in download_links:
        # Verificar a data associada ao documento
        # Encontra o elemento de data associado
        date_element = link.find_previous('div', class_='least-content')
        if date_element:
            document_date = date_element.text.strip()

            # Separar dia, mês e ano
            day, month, year = document_date.split("/")

            # Ajustar o ano para 4 dígitos
            if len(year) == 2:
                year = '20' + year

            # Recriar a data com o ano ajustado
            document_date = f"{day}/{month}/{year}"

            # Verificar se a data do documento corresponde à data de ontem
            if document_date == yesterday_str:
                li_parent = link.find_parent(
                    'li', class_='accordion-navigation')
                if li_parent:
                    primary_text_element = li_parent.find(
                        'p', class_='primary-text')
                    if primary_text_element:
                        full_text = primary_text_element.text.strip()
                        # Extrair a parte após o último hífen
                        if '-' in full_text:
                            pdf_type = full_text.split('-')[-1].strip()
                        else:
                            pdf_type = full_text
                    else:
                        pdf_type = ""
                        print(
                            f"Elemento 'primary-text' não encontrado para link: {link}")
                else:
                    pdf_type = ""
                    print(f"Elemento 'li' pai não encontrado para link: {link}")
                    
                pdf_title = link['title']
                # Remove espaços em branco ao redor do href
                pdf_href = link['href'].strip()

                # Verificar se o href começa com '/' e então construir a URL completa
                if pdf_href.startswith('/'):
                    pdf_url = f'https://www.b3.com.br{pdf_href}'
                else:
                    pdf_url = pdf_href  # Caso o href já seja uma URL completa

                # Nome do arquivo com base na URL
                pdf_name = pdf_href.split('/')[-1]

                # Fazer o download do PDF
                try:
                    download_pdf(pdf_url, pdf_name)
                    print(f'PDF {pdf_name} baixado com sucesso!')
                    print(pdf_url)
                    publish_message({
                        "title": pdf_title,
                        "url": pdf_url.replace(" ", "%20"),
                        "date": document_date,
                        "type": pdf_type
                    })
                except requests.exceptions.RequestException as e:
                    print(f'Erro ao baixar {pdf_name}: {e}')
            else:
                print("Documento desconsiderado: ", link)

# Aplica a extração de duas páginas (30 PDFs!!)
def process_page(page):
    url = f'https://www.b3.com.br/pt_br/regulacao/oficios-e-comunicados/?pagination={page}'

    soup = get_page(url)

    # Procurar por todos os <a> que têm o atributo title e href
    download_links = soup.find_all('a', title=True, href=True)

    get_pdfs(download_links)


def main():
    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    print(f'Iniciando scraping de dados em {data_atual}')
    for i in range(1, 4):
        process_page(i)


if __name__ == '__main':
    main()
