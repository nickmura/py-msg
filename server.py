import socket, sys, time
from threading import Thread

# server IP address
server_host = "0.0.0.0"
port = 8080
token = "<SEP>" #seperates client name & message

# init list/set of connected client sockets
client_sockets = set()

# create a TCP socket
new_socket = socket.socket()

# make the port as reusable port
new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind socket
new_socket.bind((server_host, port))

# listen for upcoming connections
new_socket.listen(5)
print(f"[*] success, listening as, {server_host}:{port}")

# new_socket.listen(1)
# conn, add =  new_socket.accept()
# print("Recieved conection from", add[0])

def listen_for_client(cs):
    """
    function listens for a message from 'cs' socket
    whenever a message is recieved, broadcast to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from 'c'
            msg = cs.recv(1024).decode()
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # if we have received a message, replace the token
            # with ": " for nice printing
            msg = msg.replace(token, ": ")
        # iterate over all connected sockets
        for client_socket in client_sockets:
            # sending message
            client_socket.send(msg.encode())
while True:
    # we keep listening for new connections all the time
    client_socket, client_address = new_socket.accept()
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()

# closing sockets
for cs in client_sockets:    
    cs.close()
# close server socket
new_socket.close()

