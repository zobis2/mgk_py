# Requires: unittest, httpx (for making HTTP requests in the example test)
import unittest
import subprocess
import httpx
import time
import asyncio
import websockets

class MyServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the Uvicorn server as a subprocess
        cls.server = subprocess.Popen(["uvicorn", "server.main:app", "--port", "8000"])
        time.sleep(3)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        # Terminate the Uvicorn server
        cls.server.terminate()
        cls.server.wait()
        # Function to start the AI client as a subprocess
    def test_server_is_up_serving_http(self):
        response = httpx.get("http://localhost:8000/")
        self.assertEqual(response.status_code, 200)

    def test_ai_client(self):

        uri='ws://localhost:8000/ws/AI'+  str(time.time())

        command = [
            "python", "client/ai.py",
            "--uri",uri ,
            "--mode", "seconds",
            "--n", "3"
        ]
        self.ai=subprocess.Popen(command)
        client_uri='ws://localhost:8000/ws/Client'

        # Run the WebSocket client to listen for messages
        message_count = asyncio.run(self.listen_for_messages(client_uri, 10))

        # Assert the expected number of messages
        # This expectation might need adjustment based on your AI client's behavior
        expected_messages = 2  # Example expectation
        self.assertTrue(message_count > expected_messages)
        self.ai.terminate();
        self.ai.wait();


    async def listen_for_messages(self, uri, listen_duration):
        """WebSocket client to listen for messages."""
        async with websockets.connect(uri) as websocket:
            start_time = asyncio.get_event_loop().time()
            received_messages = []

            while (asyncio.get_event_loop().time() - start_time) < listen_duration:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    received_messages.append(message)
                except asyncio.TimeoutError:
                    # No message received within timeout period
                    pass

            return len(received_messages)

