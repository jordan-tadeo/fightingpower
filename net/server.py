import socket
from _thread import *
from pygame import time

def read_pos(str):
    str = str.split(",")
    return float(str[0]), float(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

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
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break
    
    print("Lost connection")
    conn.close()

# Starting the server and listening for connections
if __name__ == "__main__":
    # IPv4 Address of host
    server = "127.0.0.1"
    port = 63553

    # Initialize socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #bind server/port to socket
    try:
        s.bind((server,port))
        print(f'Successfully bound server to socket {s}')
    except socket.error as e:
        str(e)

    # Listen for client connection, allow 2 clients
    s.listen(2)
    print("Server started")
    print("Waiting for connection . . .")

    # Hold players positions on server [p1, p2]
    pos = [(0,0), (0,0)]
    # Continue to look for connections
    currentPlayer = 0
    while True:
        # conn - connection object
        # addr - IP
        conn, addr = s.accept()
        print(f"Connected to: {addr}")

        # Start threaded process
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1
        clock = time.Clock().tick(60)
