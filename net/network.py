import socket

# Connect to server class
# Server = server connecting to, needs to be same as in server.py
class Network:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.40.16.19"
        self.port = 63553
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.sock.connect(self.addr)
            print("Client socket connection succeeded")
            return self.sock.recv(2048).decode()
        except:
            print("Client socket connection failed")
            pass

    def send_and_recv(self, data):
        try:
            self.sock.send(str.encode(data))
            return self.sock.recv(2048).decode()
        except socket.error as e:
            print("ERROR IN NETWORK.PY")
            print(f" * * * Error with socket {socket}: {e}")