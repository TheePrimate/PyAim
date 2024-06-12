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
        return self.p

    # Connect client to the address and
    # send data to confirm connection.
    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode()
        except EOFError:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048 * 2))
        except socket.error as e:
            print(e)
