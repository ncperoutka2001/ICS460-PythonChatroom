
#Authentication Handler Class
#Program handles the authentication and data storage

# imports
import os
import json
import hashlib
import threading

class SimpleAuth:
    # contructor either loads or create the users file. set empty_file=true to reset the records
    def __init__(self, storage_file='users.json', empty_file=False):
        self.storage_file = storage_file
        self.lock = threading.Lock()
        if empty_file or not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as file:
                file.write('{}')
    # returns true if the requested username exits
    def user_exists(self, username):
        with open(self.storage_file, 'r') as file:
            data = json.load(file)
        return (username in data)
    # attempts to register new user, returns true if successful
    def register_user(self, username, password):
        if not self.user_exists(username):
            salt = os.urandom(16)
            hashed_password = hashlib.sha256(password.encode() + salt).hexdigest()
            user_data = {'hashed_password': hashed_password, 'salt': salt.hex()}
            with self.lock:
                with open(self.storage_file, 'r+') as file:
                    data = json.load(file)
                    data[username] = user_data
                    file.seek(0)
                    json.dump(data, file, indent=None)
            return True
        else:
            return False
    # checks if password matches user records. returns true if successful
    def verify_identity(self, username, password):
        with open(self.storage_file, 'r') as file:
            data = json.load(file)
        record = data.get(username)
        if record:
            salt = bytes.fromhex(record['salt'])
            hashed_password = hashlib.sha256(password.encode() + salt).hexdigest()

            return (hashed_password == record['hashed_password'])
        return False
