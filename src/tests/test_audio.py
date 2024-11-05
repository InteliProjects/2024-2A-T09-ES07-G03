import requests
import json
import os

base_path = os.path.dirname(__file__)  # Diretorio dos scripts de teste

# Teste com áudio funcional (.mp3)
def test_record_audio_1():
    url = "http://localhost:8000/record-audio"
    audio_path = os.path.join(base_path, "files", "audio_test_file_1.mp3")

    # Abre o arquivo em modo binário
    with open(audio_path, 'rb') as audio_file:
        # Envia o arquivo usando o parâmetro 'files'
        files = {
            'file': audio_file
        }

        # Envia uma requisição POST com o arquivo
        response = requests.post(url, files=files)

    # Verifica o código de status HTTP
    assert response.status_code == 200
    
    # Verifica o conteúdo da resposta
    response_data = response.json()
    assert response_data.get("statusCode") == 200
    
    # Extrai o campo 'body' da resposta
    body = response_data.get("body")
    assert body is not None

    # Faz o parsing da string JSON 'body' para um dicionário
    body_dict = json.loads(body)

    # Extrai o campo 'message' do 'body' após o parsing
    message = body_dict.get("message")
    assert message == "Áudio gravado e salvo com sucesso!"

    # Verifica se o 'file_name' foi retornado corretamente
    file_name = body_dict.get("file_name")
    assert file_name is not None


# Teste com áudio funcional (.wav)
def test_record_audio_2():
    url = "http://localhost:8000/record-audio"
    audio_path = os.path.join(base_path, "files", "audio_test_file_2.wav")

    # Abre o arquivo em modo binário
    with open(audio_path, 'rb') as audio_file:
        # Envia o arquivo usando o parâmetro 'files'
        files = {
            'file': audio_file
        }

        # Envia uma requisição POST com o arquivo
        response = requests.post(url, files=files)

    # Verifica o código de status HTTP
    assert response.status_code == 200
    
    # Verifica o conteúdo da resposta
    response_data = response.json()
    assert response_data.get("statusCode") == 200
    
    # Extrai o campo 'body' da resposta
    body = response_data.get("body")
    assert body is not None

    # Faz o parsing da string JSON 'body' para um dicionário
    body_dict = json.loads(body)

    # Extrai o campo 'message' do 'body' após o parsing
    message = body_dict.get("message")
    assert message == "Áudio gravado e salvo com sucesso!"

    # Verifica se o 'file_name' foi retornado corretamente
    file_name = body_dict.get("file_name")
    assert file_name is not None


# Teste com arquivo de formato inválido
def test_record_audio_3():
    url = "http://localhost:8000/record-audio"
    audio_path = os.path.join(base_path, "files", "audio_test_file_3.txt") # Passando um arquivo .txt, não aceito pela API

    # Abre o arquivo em modo binário
    with open(audio_path, 'rb') as audio_file:
        # Envia o arquivo usando o parâmetro 'files'
        files = {
            'file': audio_file
        }

        # Envia uma requisição POST com o arquivo
        response = requests.post(url, files=files)

    # Verifica o código de status HTTP
    assert response.status_code == 400

    response_data = response.json()
    assert response_data.get("detail") == "Formato de arquivo inválido. Apenas arquivos .mp3 e .wav são suportados."


# Teste com arquivo inexistente
def test_record_audio_4():
    url = "http://localhost:8000/record-audio"

    files = {
        'file': None  # Passando um arquivo inexistente
    }

    # Envia uma requisição POST sem arquivo
    response = requests.post(url, files=files)

    # Verifica o código de status HTTP
    assert response.status_code == 400

