import asyncio
import os
import random
import time
from dataclasses import asdict, dataclass

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

TICK_SECONDS = float(os.getenv("TICK_SECONDS", "2"))
MAX_BOTS = int(os.getenv("MAX_BOTS", "100"))

@dataclass
class Bot:
    id: int
    name: str
    state: str = "waiting"
    x: float = 0.0
    y: float = 0.0
    actions: int = 0
    last_action: float = 0.0

bots = {}
running = False
worker_task = None

async def bot_loop():
    global running
    while running:
        for bot in list(bots.values()):
            if bot.state == "waiting":
                bot.state = "playing"
            bot.x += random.uniform(-3, 3)
            bot.y += random.uniform(-3, 3)
            bot.actions += 1
            bot.last_action = time.time()
        await asyncio.sleep(TICK_SECONDS)

app = FastAPI(title="Bot Simulator", version="1.0.0")

class StartRequest(BaseModel):
    amount: int = 10

@app.get("/")
async def home():
    return {
        "service": "bot-simulador",
        "running": running,
        "bots": len(bots),
        "endpoints": ["/start", "/stop", "/status", "/bots", "/health"]
    }

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/start")
async def start(req: StartRequest):
    global running, worker_task
    if req.amount < 1 or req.amount > MAX_BOTS:
        raise HTTPException(400, f"amount deve estar entre 1 e {MAX_BOTS}")

    bots.clear()
    for i in range(1, req.amount + 1):
        bots[i] = Bot(id=i, name=f"Bot-{i:03d}")

    if not running:
        running = True
        worker_task = asyncio.create_task(bot_loop())

    return {"ok": True, "running": running, "bots": len(bots)}

@app.post("/stop")
async def stop():
    global running, worker_task
    running = False
    if worker_task:
        worker_task.cancel()
        worker_task = None

    for bot in bots.values():
        bot.state = "stopped"

    return {"ok": True, "running": False}

@app.get("/status")
async def status():
    return {
        "running": running,
        "bot_count": len(bots),
        "tick_seconds": TICK_SECONDS,
        "bots": [asdict(bot) for bot in bots.values()]
    }

@app.get("/bots")
async def list_bots():
    return [asdict(bot) for bot in bots.values()]
