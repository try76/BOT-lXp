# Bot Simulator — app.py

Simulador de bots em Python usando FastAPI.
Os bots são simulados e não acessam nem controlam jogos ou serviços externos.

## Rodar
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000

Documentação: http://127.0.0.1:8000/docs

## API

Iniciar 20 bots:
curl -X POST http://127.0.0.1:8000/start -H "Content-Type: application/json" -d '{"amount":20}'

Status:
curl http://127.0.0.1:8000/status

Parar:
curl -X POST http://127.0.0.1:8000/stop

## Render

Build Command:
pip install -r requirements.txt

Start Command:
uvicorn app:app --host 0.0.0.0 --port $PORT
