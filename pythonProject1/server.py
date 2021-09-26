import socket
from _thread import *
import sys

server = "192.168.48.128" #IPv4 address of the machine where server script will run
port = 5555 # port number which we will bind to the server to accept connections

#The arguments passed to socket() specify the address family and socket type.
# AF_INET is the Internet address family for IPv4.
# SOCK_STREAM is the socket type for TCP, the protocol that will be used to transport our messages in the network.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #

try:
    # bind() is used to associate the socket with a specific network interface and port number:
    s.bind((server, port))
except socket.error as e:
    str(e)
# listen() enables a server to accept() connections.
s.listen(2)
print("Waiting for a connection, Server Started")


def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    # accept() blocks and waits for an incoming connection.
    # When a client connects, it returns a new socket object representing the connection and a tuple holding the address of the client.
    conn, addr = s.accept()
    print("Connected to:", addr)
    # dispatching a thread to handle clientsocket, create a new process to handle clientsocket and server goes back to listening
    start_new_thread(threaded_client, (conn,))