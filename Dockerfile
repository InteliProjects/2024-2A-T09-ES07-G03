FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /src

# Copy requirements early to leverage caching of pip installs
COPY requirements.txt ./requirements.txt

COPY start.sh ./start.sh

# Install dependencies from requirements.txt
RUN pip install -r ./requirements.txt

# Download the spaCy model to the default location
RUN python -m spacy download pt_core_news_sm

# Copy the rest of the application code
COPY src/ ./

# Set PYTHONPATH to include the /src directory
ENV PYTHONPATH=/src

# Command to run the start script using bash
CMD ["bash", "./start.sh"]
