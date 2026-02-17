from fastapi import WebSocket
from typing import Dict, List
import asyncio
import json

from .redis_client import redis_client


class ConnectionManager:

    def __init__(self):

        # document_id -> list of websocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

        # start redis listener safely
        self.listener_task = None


    async def start_listener(self):
        """
        Start Redis listener (call once on app startup)
        """
        if self.listener_task is None:
            self.listener_task = asyncio.create_task(self.redis_listener())


    async def connect(self, document_id: str, websocket: WebSocket):

        await websocket.accept()

        if document_id not in self.active_connections:
            self.active_connections[document_id] = []

        self.active_connections[document_id].append(websocket)

        print(f"Client connected to document {document_id}")


    def disconnect(self, document_id: str, websocket: WebSocket):

        if document_id in self.active_connections:

            if websocket in self.active_connections[document_id]:
                self.active_connections[document_id].remove(websocket)

            if not self.active_connections[document_id]:
                del self.active_connections[document_id]

        print(f"Client disconnected from document {document_id}")


    async def send_local(self, document_id: str, message: str):
        """
        Send message to local clients only
        """

        if document_id in self.active_connections:

            disconnected = []

            for connection in self.active_connections[document_id]:

                try:
                    await connection.send_text(message)

                except Exception:
                    disconnected.append(connection)

            # cleanup dead connections
            for conn in disconnected:
                self.active_connections[document_id].remove(conn)


    async def broadcast_json(self, document_id: str, data: dict):
        """
        Broadcast structured JSON message locally and via Redis
        """

        message = json.dumps(data)

        # send locally first (fast)
        await self.send_local(document_id, message)

        # publish to redis (other servers)
        await redis_client.publish(document_id, message)


    async def redis_listener(self):
        """
        Listen for Redis Pub/Sub messages and forward locally
        """

        pubsub = redis_client.pubsub()

        await pubsub.psubscribe("*")

        print("Redis listener started")

        async for message in pubsub.listen():

            try:

                if message["type"] != "pmessage":
                    continue

                document_id = message["channel"]

                data = message["data"]

                # send to local clients only
                if document_id in self.active_connections:

                    await self.send_local(document_id, data)

            except Exception as e:

                print("Redis listener error:", e)


# global manager instance
manager = ConnectionManager()
