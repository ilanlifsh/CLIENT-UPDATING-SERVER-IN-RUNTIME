"""
Protocol Module for handling communication and file transfers between client and server.
Made by Ilan 1/1/2025
"""

import os

# Constants for protocol handling
HEADER_SIZE = 10         # Size of the header containing the length of the message
BUF_SIZE = 1024          # Buffer size for data transfer
FILE_HEADER = 20         # Header size for file metadata (file name)

def send_all(**kwargs):
    """
    Sends a string message with a prefixed header indicating the message length.
    
    Args:
        socket: The socket through which data is sent.
        data: The message string to be sent.
    """
    socket = kwargs.get("socket")
    data = str(kwargs.get("data"))
    header = str(len(data))  # Calculate the length of the message as a header

    # Pad the header and concatenate it with the data
    msg = header.rjust(HEADER_SIZE, '0') + data
    socket.sendall(msg.encode())  # Send the complete message

def recv_all(**kwargs):
    """
    Receives a string message, reading the header first to determine its length.
    
    Args:
        socket: The socket from which data is received.
    
    Returns:
        The received message as bytes, or an empty byte string if an error occurs.
    """
    try:
        socket = kwargs.get("socket")
        # Read the header to determine message length
        msg_len = int(socket.recv(HEADER_SIZE).decode().strip())

        msg_data = b''
        while len(msg_data) < msg_len:
            chunk = socket.recv(BUF_SIZE)
            if chunk == b'':  # Handle socket disconnection
                raise Exception
            msg_data += chunk

        return msg_data
    except:
        return b''

def send_file(**kwargs):
    """
    Sends a file to the client, including its size and name as headers.
    
    Args:
        socket: The socket through which the file is sent.
        file_name: The path to the file being sent.
    """
    client_socket = kwargs.get('socket')
    file_name = kwargs.get('file_name')
    file = open(file_name, 'rb')  # Open the file in binary read mode
    file_size = str(os.path.getsize(file_name)).rjust(HEADER_SIZE, '0')
    file_name_padded = os.path.basename(file_name).rjust(FILE_HEADER, ' ')

    # Send file size and name
    client_socket.sendall(file_size.encode())
    client_socket.sendall(file_name_padded.encode())

    # Send the file data in chunks
    data_sent = 0
    file_size = int(file_size)
    while data_sent < file_size:
        chunk = file.read(BUF_SIZE)
        client_socket.sendall(chunk)
        data_sent += len(chunk)

    file.close()  # Close the file after sending

def recv_file(**kwargs):
    """
    Receives a file from the client, including its size and name, and saves it locally.
    
    Args:
        socket: The socket from which the file is received.
        folder: The folder where the file will be saved.

    Returns:
        The path to the saved file, or None if an error occurs.
    """
    try:
        client_socket = kwargs.get('socket')
        # Receive file size and name
        file_size = int(client_socket.recv(HEADER_SIZE).decode())
        file_name = client_socket.recv(FILE_HEADER).decode().strip()
        folder = kwargs.get("folder")

        if file_name == "" or not file_size:
            return None

        # Ensure the destination folder exists
        folder_path = os.path.join(os.getcwd(), folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder)

        # Save the received file in the specified folder
        file_name = os.path.join(folder_path, file_name)
        with open(file_name, 'wb') as file:
            data_recv = 0
            while data_recv < file_size:
                chunk = client_socket.recv(BUF_SIZE)
                file.write(chunk)
                data_recv += len(chunk)

        return file_name

    except:
        return None

def send(**kwargs):
    """
    General-purpose function for sending either a message or a file.

    Args:
        socket: The socket through which data is sent.
        data: The message string to be sent (optional).
        file: The file path to be sent (optional).
    """
    try:
        socket = kwargs.get("socket")
        data = kwargs.get("data")
        file = kwargs.get("file")

        if file:
            # Send a file if specified
            send_file(socket=socket, file_name=file)
        elif data:
            # Send a string message if specified
            send_all(socket=socket, data=data)
    except Exception as e:
        raise

def recv(**kwargs):
    """
    General-purpose function for receiving either a message or a file.
    
    Args:
        socket: The socket from which data is received.
        type: The type of data expected ('msg' or 'file').
        type_send: The folder where received files will be stored ('screenshot', 'send', or 'update').
    
    Returns:
        The received message (bytes) or the file path (string), or None if an error occurs.
    """
    try:
        socket = kwargs.get("socket")
        msg_type = kwargs.get("type")
        type_send = kwargs.get("type_send")

        if socket is None:
            raise Exception

        if msg_type == 'msg':
            # Receive a string message
            return recv_all(socket=socket)
        elif msg_type == 'file':
            # Receive a file and store it in the appropriate folder
            if type_send in ("screenshot", "send"):
                filename = recv_file(socket=socket, folder=type_send)
            else:
                filename = recv_file(socket=socket, folder="update")
            return filename
    except:
        return None
