ICS460 - Assignment 3
Chat Room Program

Files:
chatclient.py
 - Runs the chat room server. Waits for incoming connections and dispatches threads to handle each. 
 - takes arguments <server_name><server_port><username> 

chat_server.py 
 - Runs the chat room client program. Attempts to connect to the server specified as username. 
 - takes arguemnt <server_port>

SimpleAuth.py
 - Handles user authentication and storing data

users.json
 - stored credentials of users


Operation:
Private Message: 'PM messagetext'
Direct Message:  'DM <username> messagetext'
Show User List:  'SU'
Exit Server:     'EX'

Sent messages will appear in the chat serving as confirmation of receipt