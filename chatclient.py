
#Chat Client Program
#Program handles the client side operation of a client-server chat program
#py chatclient.py <server_address> <server_port> <requested_username>

# imports
from socket import *
import threading
import sys
import re

# Thread functions ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Thread listens for incoming messages and puts them in message_queue
def receive_messages(client_socket):
    try:
        # wait on messages, if 'EX' close, else pretty print
        while True:
            msg = client_socket.recv(1024).decode()
            if msg == 'EX':
                break
            print("\x1b[s\x1b[1A\x1b[999D\x1b[1S\x1b[L"+msg+"\x1b[u", end="",flush=True)
    except Exception as e:
        print(f"Terminated 'receive_messages' - {e}")
# Thread handles communication with the server
def start_client():
    try:
        # Initialize the tcp connection
        server_address = (sys.argv[1],int(sys.argv[2]))
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(server_address)
        print(f"Connecting to the server @ {server_address[0]}:{server_address[1]}")
        username = sys.argv[3]
        # handle the login/register communication
        handle_login(client_socket, username)
        # print welcome text
        print_welcome_text()
        # dispatch thread to handle incoming messages
        recv_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        recv_thread.daemon = True
        recv_thread.start()
        # running input loop
        while True:
            # take input, erase the input for prettiness and send. if 'EX' wait for the receiver to terminate and then clean up
            message = input("> ")
            erase_console_line()
            client_socket.sendall(message.encode())
            if message == 'EX':
                recv_thread.join()
                break
    except Exception as e:
        print(f"Terminated 'start_client' - {e}")
    finally:
        client_socket.close()

# Utility Functions -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Fuction handles the client side of the login/register communication
def handle_login(client_socket, username):
    # send the requested username and track the response
    client_socket.send(username.encode())
    response = client_socket.recv(1024).decode()
    if response == "L":
        # if username is logging in take passwords until accepted
        print(f"Welcome Back {username}!")
        while True:
            password = input("Password> ")
            client_socket.send(password.encode())
            response = client_socket.recv(1024).decode()
            if response == "S":
                break
    else:
        # if user is new accept a password
        print(f"Welcome {username}!")
        password = input("Set Password> ")
        client_socket.send(password.encode())
# Function erases a line in the console count times for pretty printing
def erase_console_line(count=1):
    for i in range(count):
        sys.stdout.write('\033[F')
        sys.stdout.write('\033[K')
        sys.stdout.flush()
# function prints commands and sets adjusts console on login
def print_welcome_text():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("Private Message: 'PM messagetext'")
    print("Direct Message:  'DM <username> messagetext'")
    print("Show User List:  'SU'")
    print("Exit Server:     'EX'\n")

# start client communication thread
start_client()
