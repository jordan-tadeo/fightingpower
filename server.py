import socket
from _thread import *
import sys

#IPv4 Address of host
server = "192.168.1.93"
port = 5555

#Initialize socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind server/port to socket
try:
    s.bind((server,port))
except socket.error as e:
    str(e)

#listen for client connection, 2 clients allowed to server
s.listen(2)
print("Server started")
print("Waiting for connection . . .")

#threaded client function
def threaded_client(conn):

    reply = ""
    while True:
        try:
            # 2048 = accepted bits from client
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print(f"Recieved : {reply}")
                print(f"Sending : {reply}")

            conn.sendall(str.encode(reply))

        except:
            break

#Continue to look for connections
while True:
    #conn - connection object
    #addr - IP
    conn, addr = s.accept()
    print(f"Connected to: {addr}")

    #start threaded process
    start_new_thread(threaded_client, (conn,))
