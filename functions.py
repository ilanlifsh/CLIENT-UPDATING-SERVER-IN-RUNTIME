"""
Server-side functions for handling various client requests. Functions include deleting files, 
listing directories, sending random numbers, capturing screenshots, sending files, and providing 
server information such as its name and current time.
Made by Ilan 1/1/2025
"""
import time
import protocol as prot  # Custom protocol for sending and receiving data
import subprocess as sub
import random
import os
from PIL import ImageGrab  # For capturing screenshots

# Constant for server name
FINAL_NAME = "ILAN'S SERVER"

def wdel(args):
    """
    Deletes a specified file.
    
    Args:
        args: List containing the client socket and the path to the file to be deleted.
    """
    client_socket = args[0]
    pathToDel = args[1]
    try:
        os.remove(pathToDel)
        prot.send(socket=client_socket, data="DELETED SUCCESSFULLY")
    except:
        prot.send(socket=client_socket, data="ERROR DELETING FILE")

def wdir(args):
    """
    Lists the contents of a directory.
    
    Args:
        args: List containing the client socket and (optionally) the directory path.
    """
    client_socket = args[0]
    if len(args) == 2:
        directory = args[1]
        if os.path.exists(directory):
            files = os.listdir(directory)
            prot.send(socket=client_socket, data=files)
        else:
            prot.send(socket=client_socket, data="No such file or directory")
    else:
        cwd = os.getcwd()  # Current working directory
        files = os.listdir(cwd)
        prot.send(socket=client_socket, data=files)

def wname(args):
    """
    Sends the server name to the client.
    
    Args:
        args: List containing the client socket.
    """
    client_socket = args[0]
    prot.send(socket=client_socket, data=FINAL_NAME)

def wrand(args):
    """
    Sends a random integer to the client.
    
    Args:
        args: List containing the client socket and optional range parameters.
    """
    client_socket = args[0]
    if len(args) == 2:
        param1 = int(args[1])
        rand = random.randrange(param1, 1000)
        prot.send(socket=client_socket, data=rand)
    elif len(args) == 3:
        param1 = int(args[1])
        param2 = int(args[2])
        rand = random.randrange(param1, param2)
        prot.send(socket=client_socket, data=rand)
    else:
        rand = random.randrange(0, 1000)
        prot.send(socket=client_socket, data=rand)

def wscreenshot(args):
    """
    Captures a screenshot and sends it to the client.
    
    Args:
        args: List containing the client socket.
    """
    client_socket = args[0]

    # Capture the entire screen
    screenshot = ImageGrab.grab()

    # Save the screenshot to a file
    screenshot.save("screenshot.png")
    screenshot.close()

    # Notify the client and send the screenshot file
    prot.send(socket=client_socket, data='screenshot')
    prot.send(socket=client_socket, file='screenshot.png')

def wtime(args):
    """
    Sends the current time to the client.
    
    Args:
        args: List containing the client socket.
    """
    t = time.ctime()  # Get current time as a string
    client_socket = args[0]
    prot.send(data=t, socket=client_socket)

def wsend(args):
    """
    Sends a specified file to the client.
    
    Args:
        args: List containing the client socket and the file name.
    """
    client_socket = args[0]
    file_name = args[1]
    if os.path.exists(file_name):
        prot.send(socket=client_socket, data='send')  # Notify client about the file
        prot.send(socket=client_socket, file=file_name)
    else:
        error_message = f"There is no such file or directory named: \"{file_name}\". Try again!"
        prot.send(socket=client_socket, data=error_message)
