# Usa a imagem oficial do Python como base
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo requirements.txt
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do consumidor para o container
COPY . .

# Comando para rodar o consumer
CMD ["python", "-u", "rabbit_consumer.py"]
