import requests
import json
import os

base_path = os.path.dirname(__file__)  # Diretorio dos scripts de teste

# Teste com áudio funcional (.mp3)
def test_stt_1():
    url = "http://localhost:8000/transcribe"
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

    # Extrai o campo 'transcript' do 'body' após o parsing
    transcript = body_dict.get("transcript")
    assert transcript is not None

    # Verifica se o texto do transcript é igual ao esperado (No momento testando apenas com ingles, para proxima sprint vamos implementar com portugues)
    expected_transcript = (
        "The bee and the gardener's daughter. Once a little bee there flew busily about and drew sweets from every blooming flower. "
        "Little bee. The maiden cried, who was busy there at work, oft therein doth poison lurk, and thou Sipp'st from every flower. "
        "Yes, said the bee, the sweets I sup, but leave the poison in the cup. This recording is in the public domain."
    )
    assert transcript == expected_transcript


# Teste com áudio funcional (.wav)
def test_stt_2():
    url = "http://localhost:8000/transcribe"
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

    # Extrai o campo 'transcript' do 'body' após o parsing
    transcript = body_dict.get("transcript")
    assert transcript is not None

    # Verifica se o texto do transcript é igual ao esperado (No momento testando apenas com ingles, para proxima sprint vamos implementar com portugues)
    expected_transcript = (
        "The bee and the gardener's daughter. Once a little bee there flew busily about and drew sweets from every blooming flower. "
        "Little bee. The maiden cried, who was busy there at work, oft therein doth poison lurk, and thou Sipp'st from every flower. "
        "Yes, said the bee, the sweets I sup, but leave the poison in the cup. This recording is in the public domain."
    )
    assert transcript == expected_transcript


# Teste com arquivo de formato inválido
def test_stt_3():
    url = "http://localhost:8000/transcribe"
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
def test_stt_4():
    url = "http://localhost:8000/transcribe"

    files = {
        'file': None # Passando um arquivo inexistente
    }

    # Envia uma requisição POST sem arquivo
    response = requests.post(url, files=files)

    # Verifica o código de status HTTP
    assert response.status_code == 400
