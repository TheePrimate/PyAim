"""
File for compiling information and sending it to the server.
"""


import socket
import pickle
from constants import SERVER_IP
from constants import PORT


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER_IP
        self.port = PORT
        self.address = (self.server, self.port)
        self.p = self.connect()

    def get_player_id(self):
        """Get the player's ID"""
        return self.p

    def connect(self):
        """
        Connect client to the address and
        send data to confirm connection.
        """
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode()
        # "End of File" Error occurs when there is
        # expected information, but nothing is received/sent.
        except EOFError:
            pass

    def send(self, data):
        """Function that compiles code and then sends it"""
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048 * 2))
        except socket.error as e:
            print(e)
