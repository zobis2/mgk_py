
# MGK LABS - home test in the base:) 

This project utilizes FastAPI and Uvicorn to leverage 
asynchronous behavior, ensuring optimal server performance and 
handling complex asynchronous operations seamlessly. 
A retry mechanism is implemented in both the `client/ai.py` 
and the HTML client to enhance connectivity resilience, automatically 
handling retries in case of connection issues. The project also features 
a custom protocol for message handling, where the first 4 bytes denote
the message length, followed by the message content, ensuring consistent
and reliable communication between the server, AI client, and HTML client.

## Getting Started

### Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn
- HTTPX (for HTTP client functionality)

### Installation

1. Clone the repository to your local machine.
2. Install the required Python packages:

bash
pip install fastapi uvicorn httpx
or
pip install -r requirements.txt


### Running the Server
To run the Uvicorn server:

Configure your IDE (VS Code, IntelliJ, PyCharm, etc.) 
to recognize the Uvicorn server script.
Script Path: Locate the uvicorn executable within your 
Python environment's site-packages. 
This is typically found in ${PYTHONLOCATION}/site-packages/uvicorn/__main__.py.
Script Parameters: Set to "server.main:app --reload" to run the main app with auto-reload enabled. The default port is 8000.
Alternatively, you can run the server directly from the command line:

bash

uvicorn server.main:app --reload

### Accessing the HTML Client
After starting the server, visit http://localhost:8000/ to access the HTML client. This client allows users to enter a user ID to connect. A unique ID mechanism is implemented for user identification, enhancing the chat service's reliability and user experience. The client displays messages with their timestamps, ensuring a dynamic and real-time chat experience.

### Running the AI Client
To run the AI client, execute the client/ai.py
script as a standard Python script. 
The script prompts for 
input regarding the operation mode (1 for seconds, 2 for lines) 
and the sequence number (n). This setup allows for customized
interaction with the server based on user input.

## Tests
Testing is facilitated through a tests.py script,
utilizing unittest and subprocesses to accommodate 
the asynchronous nature of
the application and the external 
dependencies on Uvicorn and FastAPI. Although initially considered, 
pytest was set aside due to time constraints. 
The provided tests ensure that the server operates
correctly and that the AI client interacts with it as expected.

### Running Tests
To run the tests, use the following command:

# bash
python -m unittest tests.py
This command executes the test suite, verifying the server's functionality and the AI client's integration.

### Notes
Some parts of the code were generated with the assistance of OpenAI, complementing manual development efforts to adhere to the project's time constraints.
The project aims to demonstrate a practical implementation of asynchronous web technologies and custom communication protocols, underlined by a robust testing strategy to ensure reliability and performance.
Conclusion
This README provides a 
comprehensive guide to setting up, running, 
and testing the project, ive written it and then re-wrote it openai.
