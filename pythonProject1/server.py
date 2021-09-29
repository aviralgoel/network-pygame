import socket
from _thread import *
import sys

server = "192.168.48.128"  # IPv4 address of the machine where server script will run
port = 5555  # port number which we will bind to the server to accept connections

# The arguments passed to socket() specify the address family and socket type.
# AF_INET is the Internet address family for IPv4.
# SOCK_STREAM is the socket type for TCP, the protocol that will be used to transport our messages in the network.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # bind() is used to associate the socket with a specific network interface and port number:
    s.bind((server, port))
except socket.error as e:
    str(e)

# listen() enables a server to accept() connections. (in our case, only two clients can be connected to the server)
s.listen(2)
print("Waiting for a connection, Server Started")


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


pos = [(0, 0), (100, 100)]  # spawn/starting locations for the game


def threaded_client(conn, player):
    # once the connection is established send the player location tuple
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    # a loop to continuously receive player's position and send the position of opponent
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0

while True:
    # accept() blocks and waits for an incoming connection. When a client connects, it returns a new socket object
    # representing the connection and a tuple holding the address of the client.
    conn, addr = s.accept()
    print("Connected to:", addr)

    # dispatching a thread to handle clientsocket, create a new process to handle clientsocket and server goes back
    # to listening
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1  # count of number of players connected
