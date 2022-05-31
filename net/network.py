import socket

# Connect to server class
# Server = server connecting to, needs to be same as in server.py
class Network:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 63553
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def connect(self):
        try:
            self.sock.connect(self.addr)
            print("Client socket connection succeeded")
            return self.sock.recv(2048).decode()
        except:
            print("Client socket connection failed")
            pass
    
    # Send our info, and receive (return) other player position info
    def send_and_recv(self, data):
        try:
            self.sock.send(str.encode(data))
            return self.sock.recv(2048).decode()
        except socket.error as e:
            print(f"* Network.py > error with socket {socket} >> {e}")

    def getPos(self):
        return self.pos