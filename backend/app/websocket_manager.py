from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, job_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[job_id] = websocket

    def disconnect(self, job_id: str):
        if job_id in self.active_connections:
            del self.active_connections[job_id]

    async def send_log(self, job_id: str, message: dict):
        websocket = self.active_connections.get(job_id)

        if websocket:
            await websocket.send_json(message)


manager = ConnectionManager()