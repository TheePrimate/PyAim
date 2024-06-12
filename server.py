import socket
from _thread import *
import pickle
from game import Game
from constants import SERVER_IP
from constants import PORT

# Create a new socket using the given address family and socket type.
# SOCK_STREAM is the default type.
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try to bind the server address to the
# computer port to form an address.
try:
    socket.bind((SERVER_IP, PORT))
except socket.error as e:
    str(e)

# Tells the TCP stack to start accept incoming
# TCP connections on the port the socket is bound
# to, only accept two connections to each other.
socket.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(connection, player, game_id):
    global idCount
    connection.send(str.encode(str(player)))

    while True:
        try:
            data = connection.recv(2048 * 2).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset_submits()
                    elif data != "get":
                        game.submitted(player, data)

                    connection.sendall(pickle.dumps(game))
            else:
                break
        except EOFError:
            break

    print("Lost connection")
    try:
        del games[game_id]
        print("Closing Game", game_id)
    except EOFError:
        pass
    idCount -= 1
    connection.close()


while True:
    conn, addr = socket.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    ID = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[ID] = Game(ID)
        print("Creating a new game...")
    else:
        games[ID].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, ID))
