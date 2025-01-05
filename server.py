"""
Server Script for handling client requests and executing commands locate such as listing files, updating functions, and sending filesn or executing commands that are located in "functions.py".
Made by Ilan 1/1/2025
"""

import socket
import os
import protocol as prot
import functions as func_tst
import importlib as imp
import shutil

# Server configuration
HOST = 'localhost'  # Server address
PORT = 9098         # Server port
ADDR = (HOST, PORT) # Address tuple
BUF_SIZE = 1024     # Buffer size for data transfer

# Create and configure the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen(5)  # Listen for up to 5 incoming connections

def ulist():
    """
    Generates a list of functions in the `functions.py` module
    that start with the letter 'w'.
    """
    ulist = dir(func_tst)  # Get all attributes in the module
    list_func = "Here is a list of the functions: \n"
    for x in ulist:
        if x.startswith("w"):  # Filter for functions starting with 'w'
            list_func += x + "\n"
    return list_func

def update():
    """
    Updates the server's functionality by receiving an updated `functions.py` file from the client.
    Dynamically reloads the module to reflect the changes.
    """
    prot.send(socket=client_socket, data="ACK")  # Acknowledge the update request
    file_name = prot.recv(socket=client_socket, type='file', type_send="update")  # Receive the updated file

    # Overwrite the existing `functions.py` file
    shutil.copy(file_name, "functions.py")

    # Remove all attributes in the module except essential ones
    for attr in dir(func_tst):
        if attr not in ('__name__', '__file__'):
            delattr(func_tst, attr)

    # Reload the module to apply updates
    imp.reload(func_tst)

def handle_client(client_socket):
    """
    Handles communication with a connected client.
    Processes commands sent by the client and sends appropriate responses.
    """
    try:
        while True:
            # Receive command from the client
            data = prot.recv(socket=client_socket, type='msg')
            if not data:
                # Reinitialize connection if client disconnects
                print(f"Server listening on {ADDR}")
                client_socket, client_addr = server_socket.accept()
                print(f"New client connected from {client_addr}")
                handle_client(client_socket)

            # Decode the command
            command = data.decode().split()[0]
            if command.lower() == "exit":
                # Handle client exit
                print(f"Server listening on {ADDR}")
                client_socket, client_addr = server_socket.accept()
                print(f"New client connected from {client_addr}")
                handle_client(client_socket)

            elif command.lower() == "list":
                # Respond with the list of available functions
                response = "Function list: " + ulist()
                prot.send(socket=client_socket, data=response)
                continue

            elif command.lower() == "update":
                # Handle the update request
                update()
                response = "Updating functions..."
                prot.send(socket=client_socket, data=response)
                continue

            elif command.lower() != "exit":
                # Handle custom commands
                parameters = []
                command = 'w' + command  # Prepend 'w' to match function names
                if not hasattr(func_tst, command):
                    prot.send(socket=client_socket, data="Unknown command")
                else:
                    parameters.append(client_socket)
                    param = data.decode().lower().split()[1:]
                    if str(command)[1:] not in param:
                        parameters = parameters + param
                    getattr(func_tst, command)(parameters)

    except Exception as e:
        print(f"Error handling client: {e}")
        client_socket.close()

if __name__ == "__main__":
    """
    Main server logic: Accepts incoming connections and delegates to the handler.
    """
    print(f"Server listening on {ADDR}")
    client_socket, client_addr = server_socket.accept()
    print(f"New client connected from {client_addr}")
    handle_client(client_socket)
