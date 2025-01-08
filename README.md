
# Client-Server Communication System

This repository contains a simple client-server communication system implemented in Python using the `socket` library. It demonstrates basic networking concepts and multithreading to handle real-time message exchange between a client and a server.

## Features

- **Client-Server Architecture**:
  - The server listens for incoming connections and manages communication with multiple clients.
  - The client connects to the server and exchanges messages.

- **Multithreading**:
  - The server uses threading to handle multiple clients concurrently.
  - The client employs threading to manage sending and receiving messages simultaneously.

- **Real-Time Communication**:
  - Messages are transmitted over a TCP connection in real-time.

## Files

### `client.py`
This script implements the client-side functionality, including:
- Connecting to the server via IP and port.
- Sending messages to the server.
- Receiving and displaying responses from the server.

### `server.py`
This script implements the server-side functionality, including:
- Listening for incoming client connections.
- Handling communication with each client in a separate thread.
- Echoing messages back to the respective client.

## Setup and Usage

### Prerequisites
- Python 3.x installed on your system.

### Running the Project
1. Start the server:
   ```bash
   python server.py
   ```
   The server will start on the host's IP address and port `50000` by default.

>[!NOTE]
>If port 50000 is not free, you'll need to change this in the server.py file.
>To check which ports are free, run cmd as administrator and run the command
>```bash
>netstat -an | find "LISTEN"
>```
>and any port that's ***NOT*** on this list should be free.

2. Run the client:
   ```bash
   python client.py
   ```
   When prompted, provide the server's IP address and port to connect.

### Interaction
- The client sends messages to the server.
- The server echoes back the received messages.

## Known Issues
- Ensure the specified port (`50000`) is free before starting the server.
- Limited error handling for network interruptions or invalid inputs.

## Future Enhancements
- Add features such as message logging or group communication.
- Implement a graphical user interface (GUI) for easier interaction.
- Enhance error handling and validation mechanisms.

## Contributing
Feel free to fork this repository, make improvements, and submit a pull request. Contributions are welcome!

## License
This project is licensed under the MIT License.
