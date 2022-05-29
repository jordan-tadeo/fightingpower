import socket

# Connect to server class
# Server = server connecting to, needs to be same as in server.py
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.93"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        # Returns string recieved from server: "Connected"
        try:
            self.client.connect(self.addr)
            print("Client connection succeeded")
            # Send client info to server
            return self.client.recv(2048).decode()
        except:
            print("Client connection failed")
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)