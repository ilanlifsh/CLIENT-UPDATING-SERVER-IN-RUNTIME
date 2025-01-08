"""
Client Script for communicating with a server using a custom protocol.
Features include sending commands, receiving responses, and transferring files.
Made by Ilan 1/1/2025
"""

import socket
import protocol as prot
import functions as func_tst

# Configuration for server connection
HOST = 'localhost'  # Server address
PORT = 9098         # Server port
ADDR = (HOST, PORT) # Address tuple
BUF_SIZE = 2        # Buffer size for receiving data

# Create the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server():
    """
    Establishes a connection to the server.
    If the server is unavailable, it keeps retrying until a connection is made.
    """
    connected = False
    print(f"[CONNECTING] Connecting to server at {HOST}:{PORT} ...")
    print("Server not found, waiting for server connection...")
    while not connected:
        try:
            client_socket.connect(ADDR)
            connected = True
            print("[CONNECTED]")
        except:
            # Retry if connection fails
            continue

def send_command(command):
    """
    Sends a command to the server and processes the server's response.
    Commands include file transfers, screenshots, or basic messages.
    """
    try:
        # Send command to the server
        prot.send(socket=client_socket, data=command)
        # Receive server response
        msg = (prot.recv(socket=client_socket, type='msg')).decode()
        
        # Handle specific server responses
        if msg == "send" or msg == "screenshot":
            prot.recv(socket=client_socket, type='file', type_send=msg)
            print(f"received {msg}")
        else:
            print(f"Server Response: {msg}")

    except ConnectionRefusedError:
        # Reconnect if the server connection is lost
        connect_to_server()

# Connect to the server initially
connect_to_server()

# Main loop for handling user commands
while True:
    try:
        while True:
            # Prompt the user for a command
            command = input("Enter command (LIST, UPDATE, EXIT): ")
            if not command:
                continue
            if command.lower() == "exit":
                # Exit the client
                send_command(command)
                client_socket.close()
                break
            elif command.lower() == "list":
                # Request a list of functions from the server
                send_command(command)
            elif command.lower() == "update":
                # Request to update the server's functionality
                prot.send(socket=client_socket, data=command)
                msg1 = prot.recv(socket=client_socket, type='msg')
                print(f"Server Response: {msg1.decode()}")
                prot.send(socket=client_socket, file='functions.py')
                msg2 = prot.recv(socket=client_socket, type='msg')
                print(f"Server Response: {msg2.decode()}")
            else:
                # Handle other commands
                send_command(command)

    except ConnectionResetError:
        # Handle unexpected connection resets
        client_socket.close()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect_to_server()
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        print("Client exiting...")
        client_socket.close()
