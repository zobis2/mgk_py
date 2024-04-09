import asyncio
import websockets
import uuid
from pynput import keyboard

class ChatClient:
    def __init__(self):
        self.client_id = str(uuid.uuid4())
        self.websocket = None
        self.current_input = []
        self.listener = keyboard.Listener(on_press=self.on_press)

    def on_press(self, key):
        try:
            if key == keyboard.Key.enter:
                asyncio.run_coroutine_threadsafe(self.send_message(), asyncio.get_event_loop())
                self.current_input.clear()
            elif key == keyboard.Key.backspace:
                if self.current_input:
                    self.current_input.pop()
            elif hasattr(key, 'char') and key.char:
                self.current_input.append(key.char)
        except Exception as e:
            print(f"Error handling key press: {e}")

    async def send_message(self):
        try:
            message = ''.join(self.current_input)
            if self.websocket:
                await self.websocket.send(message)
                print(f"\nYou: {message}", end='', flush=True)
        except Exception as e:
            print(f"Error sending message: {e}")

    async def receive_messages(self):
        try:
            async for message in self.websocket:
                print(f"\nReceived message: {message}\nYou: {''.join(self.current_input)}", end='', flush=True)
        except websockets.exceptions.ConnectionClosed:
            print("\nConnection closed, exiting...")
        except Exception as e:
            print(f"Error receiving message: {e}")

    async def run(self):
        uri = f"ws://localhost:8000/ws/{self.client_id}"
        try:
            async with websockets.connect(uri) as websocket:
                self.websocket = websocket
                print(f"You are now connected to the chat server with ID: {self.client_id}")
                self.listener.start()

                receive_task = asyncio.create_task(self.receive_messages())
                await asyncio.gather(receive_task)
        except Exception as e:
            print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    client = ChatClient()
    asyncio.run(client.run())
