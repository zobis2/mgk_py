# server/connection_manager.py
from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        if client_id in self.active_connections:
                # Optionally, send an error message to the client before closing the connection
            # await websocket.send_text("Error: Client ID already in use.")
            await websocket.close(reason="Client ID already in use.")
            print(f"Rejected connection attempt for duplicate Client ID {client_id}")
            return;
        await websocket.accept()
        self.active_connections[client_id] = websocket
        await self.broadcast(f"Client {client_id} joined the chat", "Server",client_id)
        print(f"Client {client_id} connected")

    def disconnect(self, client_id: str):
        del self.active_connections[client_id]
        print(f"Client {client_id} disconnected")

    async def broadcast(self, message: str, sender_id: str,client_joined = None):
        for client_id, connection in self.active_connections.items():
            if client_id != sender_id and client_joined != client_id:
                message_for_client=sender_id+": "+message;# Avoid sending the message back to the sender
                encoded_message = message_for_client.encode('utf-8')
                header = len(encoded_message).to_bytes(4, byteorder='little')
                await connection.send_bytes(header + encoded_message)


    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
