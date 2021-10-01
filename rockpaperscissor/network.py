import socket
import pickle


# Network Class
# an object of Network class is instantiated on the side of the client
# this object immediately attempts to connect to the server
# on successful connection, it is assigned an int (0 or 1) symbolizing whether the client will
# act as player 1 or player 1

class Network:

    def __init__(self):  # constructor
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # become a socket client
        self.server = "192.168.48.128"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()  # attempt to connect to the server and let the server assign whether am player 1 (
        # p=0) or player 2 (p=1)

    # getter function which returns if the client is player 1 for player 2 according to the server
    def getP(self):
        return self.p

    # function which tried to connect to the server and receives an int from the server regarding player id
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    # function to send some data to the server
    def send(self, data):
        try:
            self.client.send(str.encode(data))  # send the encoded data as string
            return pickle.loads(self.client.recv(2048 * 2))  # accept a pickled object back from the server and
            # unpickle it
        except socket.error as e:
            print(e)
