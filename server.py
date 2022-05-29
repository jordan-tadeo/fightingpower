import socket
from _thread import *
import sys

# IPv4 Address of host
server = "192.168.1.93"
port = 5555

# Hold players positions on server [p1, p2]
pos = [(0,0), (100,100)]

###########################################################################
# Helper functions to send and recieve Client positions between server    #
# and client as tuple                                                     #
###########################################################################

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

############################################################################

# Initialize socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind server/port to socket
try:
    s.bind((server,port))
except socket.error as e:
    str(e)

# Listen for client connection, allow 2 clients
s.listen(2)
print("Server started")
print("Waiting for connection . . .")

# Threaded client function
def threaded_client(conn, player):

    # Send position to respective connected client
    conn.send(str.encode(make_pos(pos[player])))

    reply = ""
    while True:
        try:
            # 2048 = accepted bits from client
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                # Send players eachothers positions
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                    
                print(f"Recieved : {data}")
                print(f"Sending : {reply}")

            conn.sendall(str.encode(make_pos(reply)))

        except:
            break

    print("Lost connection")
    conn.close()



currentPlayer = 0
# Continue to look for connections
while True:
    # conn - connection object
    # addr - IP
    conn, addr = s.accept()
    print(f"Connected to: {addr}")

    # Start threaded process
    start_new_thread(threaded_client, (conn,currentPlayer))
    currentPlayer += 1
