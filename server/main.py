from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .connection_manager import ConnectionManager
import os

app = FastAPI()
manager = ConnectionManager()
# Construct an absolute path to the 'static' directory
current_file_path = os.path.dirname(__file__)
static_files_path = os.path.join(current_file_path, 'static')
app.mount("/static", StaticFiles(directory=static_files_path), name="/")
@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        path_to_file = os.path.join(static_files_path, "chat_interface.html")
        with open(path_to_file, "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

# Add other routes and logic as needed
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    try:
        while True:
            # Receive the data as bytes instead of text
            data_bytes = await websocket.receive_bytes()

            # The first 4 bytes are the header indicating the message length
            message_length = int.from_bytes(data_bytes[:4], byteorder='little')

            # Extract the message using the length provided by the header
            message = data_bytes[4:4+message_length]

            # Assuming the message is UTF-8 encoded, decode it to a string
            message_text = message.decode('utf-8')

            print(f"{client_id} :  message to server: {message_text}")
            await manager.broadcast(message_text, client_id)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        manager.disconnect(client_id)
        await manager.broadcast(f"Client {client_id} left the chat", "Server")