# Client-Server Communication System

This project demonstrates a client-server system that allows the client to send commands to the server for remote execution of predefined functions. The server can handle tasks such as listing files, deleting files, generating random numbers, taking screenshots, and more. The system uses a custom communication protocol for handling data exchange and file transfers between the client and server.

**Made by Ilan 1/1/2025**

---

## Project Structure

The project consists of four main scripts:

- `client.py` - The client-side logic.
- `server.py` - The server-side logic.
- `protocol.py` - Custom communication protocol for sending and receiving data.
- `functions.py` - Predefined functions that can be executed by the server (can be changed dynamically). 

---

## Scripts Description

### `client.py`

#### Description:
The `client.py` script defines the client-side logic of the application. The client connects to a server, sends commands to request actions, and handles responses, such as receiving files, executing server-side functions, and displaying the results. It uses a custom communication protocol defined in `protocol.py` for sending and receiving data. The client can execute a set of commands like listing functions available on the server, updating server functions, or performing file operations like sending files to the server.

- **Connecting to the Server:** The client establishes a connection to the server at the specified `HOST` and `PORT`.
- **Command Input:** The client listens for user input in the form of commands (`LIST`, `UPDATE`, `EXIT`, etc.) and sends these commands to the server.
- **Handling Server Responses:** After sending a command, the client waits for a response from the server, which could involve receiving data, receiving files, or executing server functions.
- **Reconnecting Logic:** If the server connection is lost, the client attempts to reconnect automatically.
- **File Transfers:** If the server sends a file (like a screenshot), the client receives and processes it using the custom protocol.

---

### `server.py`

#### Description:
The `server.py` script is the server-side component that listens for incoming client connections and processes the commands sent by the client. It allows dynamic interaction with the client, including the ability to list available functions, update server-side functions, and manage files (send and receive). The server continuously listens for new connections and executes commands based on client requests.

- **Listening for Client Connections:** The server listens for client connections on the specified `HOST` and `PORT`.
- **Function List (`list` Command):** The server can list the available functions by reflecting on the `func_tst` module, which contains predefined functions the client can invoke.
- **Updating Functions (`update` Command):** The server supports function updates by receiving a file containing updated code and dynamically reloading the functions from that file.
- **Handling Commands:** When the client sends a command, the server matches it to a predefined function in `func_tst` and executes it, sending back results or files as appropriate.
- **Error Handling:** The server handles cases where a command is unrecognized, and can also reconnect if a client disconnects.

---

### `protocol.py`

#### Description:
The `protocol.py` script contains the logic for the custom communication protocol that the client and server use to send and receive data. This protocol handles basic messaging (strings) as well as file transfers between the client and server.

- **Sending Data (`send_all`):** This function takes a socket and data (string), prepends a header with the length of the data, and sends the data to the recipient.
- **Receiving Data (`recv_all`):** This function reads the incoming data, first retrieving the header to determine the message length, and then receiving the actual data.
- **File Transfers (`send_file` and `recv_file`):** The `send_file` function sends a file to the recipient by breaking it into chunks, while the `recv_file` function receives a file and saves it to the designated folder.
- **General Send/Receive Logic:** The `send` and `recv` functions encapsulate the logic for sending both messages and files, abstracting the specifics of data type and handling.

---

### `functions.py`

#### Description:
The `functions.py` script contains a collection of server-side functions that the client can invoke remotely. These functions range from interacting with the file system to generating random numbers and taking screenshots.

- **`wdel`:** Deletes a specified file on the server's file system.
- **`wdir`:** Lists files in a directory on the server's file system, or the current working directory by default.
- **`wname`:** Returns the name of the server as a string.
- **`wrand`:** Generates and sends a random number, either within a specified range or a default range.
- **`wscreenshot`:** Takes a screenshot of the server's screen and sends the image back to the client.
- **`wtime`:** Sends the current system time to the client.
- **`wsend`:** Sends a file from the server to the client if it exists.

These functions are prefixed with `w` to signify they are remote callable functions, and the client can invoke them by sending corresponding commands.

---

## How to Use
Make sure the ports in each of the scripts are alike, and change the HOST variable in client to the IP you would like to connect to, which is the IP of where server is located.
1. **Start the Server:**
   To start the server, run the `server.py` script:
   ```bash
   python server.py

2. **Connect the Client:**
   To connect the client, run the `client.py` script:
   ```bash
   python client.py
