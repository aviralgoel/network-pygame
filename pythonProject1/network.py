import socket
import pickle


# cretes a network socket connection associated with the client machine and server
class Network:
    def __init__(self): #constructor
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.48.128" #IPv4 address of the machine where server script will run
        self.port = 5555 # port number which we will bind to the server to accept connections
        self.addr = (self.server, self.port)
        self.p = self.connect() # when first time connected to the server, receive a string with player co-ordinates (spawn location)

    def getP(self): #getter function
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr) #connect here
            return pickle.loads(self.client.recv(2048)) #receive encoded string from server (with player coordinates)
        except socket.error as e: # if unsuccessful connection
            print("Cannot connect to server")
            print(e)

    # send server an encoded string and recieve back an encoded string
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)