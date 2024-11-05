#!/bin/bash
export PYTHONPATH=/src

# Inicia o servidor FastAPI com hot reload
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &

# Inicia o cron job
python -m cron.cron 