import asyncio
import websockets
import struct
import random
import argparse

class AIChatClient:
    def __init__(self, uri, mode, n):
        self.uri = uri
        self.mode = mode  # 'seconds' or 'lines'
        self.n = n
        self.counter = 0
        self.message_queue = asyncio.Queue()
        print(self.mode)
    def generate_gibberish(self):
        vowels = "aeiou"
        consonants = "".join(set("abcdefghijklmnopqrstuvwxyz") - set(vowels))

        def generate_word(length):
            return ''.join(random.choice(consonants + vowels) for _ in range(length))

        sentence_length = random.randint(5, 10)  # Number of words in the sentence
        word_lengths = [random.randint(3, 7) for _ in range(sentence_length)]  # Length of each word

        return ' '.join(generate_word(length) for length in word_lengths) + '.'
    async def send_message(self, websocket, message):
        encoded_message = message.encode('utf-8')
        header = struct.pack("I", len(encoded_message))
        await websocket.send(header + encoded_message)
        print(f"Sent: {message}")

    async def listener(self, websocket):
        retry_count = 0
        max_retries = 3  # Maximum number of retries
        retry_delay = 5  # Delay in seconds between retries
        """Continuously listen for messages and increment the counter."""
        try:
            while True:
                data = await websocket.recv()  # Corrected to use recv() here
                if isinstance(data, bytes):
                    await self.message_queue.put(data)
                else:
                    print("Received non-binary message, which is unexpected.")
        except Exception as e:
            print(f"Error in listener: {e}")
            retry_count += 1
            if retry_count > max_retries:
                print("Max retries exceeded. Exiting listener.")

            else:
                print(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                try:
                    await self.run()
                    # THATS WHERE I DO RETIRES - i didnt had much time to do otherwise
                except Exception as e:
                        print(f"Reconnection failed: {e}")

    async def responder(self, websocket):
        """Check the counter and respond accordingly."""
        try:
            while True:
                await asyncio.sleep(0.3)  # Short sleep to yield control
                if self.mode == 'lines' and not self.message_queue.empty():
                    data = await self.message_queue.get()
                    message_length = struct.unpack("I", data[:4])[0]
                    message = data[4:4+message_length].decode('utf-8')
                    print(f"Received: {message}")
                    self.counter += 1
                    if  self.counter >= self.n:
                        await self.send_message(websocket, "response based on N lines.")
                        self.counter = 0

                elif self.mode == 'seconds':
                    await asyncio.sleep(self.n)  # Adjusted to sleep for N seconds for 'seconds' mode
                    await self.send_message(websocket,"my wierd message is :"+self.generate_gibberish())
        except Exception as e:
            print(f"Error in responder: {e}")

    async def run(self):
        while True:
            try:
                async with websockets.connect(self.uri) as websocket:
                    print("Connected to the server.")
                    listener_task = asyncio.create_task(self.listener(websocket))
                    responder_task = asyncio.create_task(self.responder(websocket))

                    await asyncio.gather(listener_task, responder_task)
            except Exception as e:
                print(f"Connection error or disconnection occurred: {e}")
                await asyncio.sleep(5)  # Reconnect after a delay
                self.run(self)

def get_args():
    parser = argparse.ArgumentParser(description="Run AI Chat Client")
    parser.add_argument("--uri", type=str, help="WebSocket URI to connect to", required=False)
    parser.add_argument("--mode", type=str, choices=["seconds", "lines"], help="Mode of operation: seconds or lines")
    parser.add_argument("--n", type=int, help="Frequency of responses (in seconds or lines, based on mode)")

    args = parser.parse_args()
    if args.mode is None or args.n is None:
        # If mode or n is not provided, ask for them
        args.uri= "ws://localhost:8000/ws/AI"

        mode_input = input("Choose mode (1 for seconds, 2 for lines): ")
        args.mode = "seconds" if mode_input == "1" else "lines"
        args.n = int(input(f"Enter N (frequency of responses in {args.mode}): "))

    return args

async def main():
    print("start ai")
    args = get_args()
    ai_client = AIChatClient(args.uri, args.mode, args.n)
    # ai_client = AIChatClient("ws://localhost:8000/ws/AI","seconds",2)

    await ai_client.run()
if __name__ == "__main__":
    asyncio.run(main())


