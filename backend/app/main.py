import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers.jobs import router
from .websocket_manager import manager


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):

    await manager.connect(job_id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except:
         manager.disconnect(job_id)