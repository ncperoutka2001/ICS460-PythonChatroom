
#Chat Server Program
#Program handles the server side operation of a client-server chat program
#py chatserver.py <port_number>

# import
from socket import *
import threading
import SimpleAuth
import sys
import re
import time

# Create a SimpleAuth and a dic to store active users
auth = SimpleAuth.SimpleAuth()
username_socket = {}

# Thread Functions ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Thread handles individual client connection
def handle_client(client_socket, client_address):
    try:
        print(f"Validating connection from {client_address}")
        username = handle_login(client_socket)
        print(f"Accepted: {client_address} as {username}")
        username_socket[username] = client_socket
        send_message_all("Joined the server",username)
        # running loop
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            text = data.decode()
            com = text[:2]
            msg = text[3:]

            if com == 'PM':
                send_message_all(msg,username)
            if com == 'DM':
                receiver = re.search(r'<(.*?)>', msg).group(1)
                msg = re.search(r'<.*?>\s*(.*)', msg).group(1)
                send_message(msg,username,receiver,receiver)
                send_message(msg,username,receiver,username)
            if com == 'SU':
                send_user_list(username)
            if com == 'EX':
                username_socket[username].send("EX".encode())
                break
    except Exception as e:
        print(f"Terminated 'handle_client' - {e}")
    finally:
        send_message_all("Left the server",username)
        username_socket.pop(username)
        client_socket.close()
# Thread handles waiting for incoming connections and dispatches them to 'handle_client'
def accept_client():
    try:
        server_address = ("localhost", int(sys.argv[1]))
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(server_address)
        server_socket.listen(8)
        print(f"Listening for Connections @ localhost:{server_address[1]}")
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True
            client_thread.start()
    except Exception as e:
        print(f"Terminated 'accept_client' - {e}")
    finally:
        server_socket.close()

# Utility Functions -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Fuction handles the server side of the login/register communication
def handle_login(client_socket):
    username = client_socket.recv(1024).decode()
    if auth.user_exists(username):
        client_socket.send("L".encode())
        while True:
            password = client_socket.recv(1024).decode()
            if auth.verify_identity(username,password):
                client_socket.send("S".encode())
                return username
            else:
                client_socket.send("F".encode())
    else:
        client_socket.send("R".encode())
        password = client_socket.recv(1024).decode()
        auth.register_user(username,password)
        return username
# Function return a HH:MM string timestamp
def get_timestamp():
    current_time = time.localtime()
    return f"{current_time.tm_hour}:{current_time.tm_min}"

# Messaging functions ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Takes message and sender name. send a message to all active users on the server
def send_message_all(msg,sender):
    for to in username_socket:
        username_socket[to].send(f"{get_timestamp()} <{sender}> {msg}".encode())
# Takes message,sender name,receiver name (display), and recipient name (address)
def send_message(msg,sender,receiver,to):
    if to in username_socket:
        username_socket[to].send(f"{get_timestamp()} <{sender}> -> <{receiver}> {msg}".encode())
# Formats a list of active users and sends to specific recipient
def send_user_list(to):
    users = ""
    for user in username_socket.keys():
        users += "<" + str(user) + "> "
    username_socket[to].send(users.encode())

# Main thread runs accept client to await incoming connections
accept_client()
