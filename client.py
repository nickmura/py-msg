import socket, random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
init()

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

client_color = random.choice(colors)


# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)

server_host = "127.0.0.1"
port = 8080
token = "<SEP>"

# initalize tcp socket
new_socket = socket.socket()
print(f"[*] Connecting to {server_host}:{port}")
# connect to the host
new_socket.connect((server_host, port))
print("[+] Connected.")

# prompt the client for a name
name = input("name: ")


def listen_for_messages():
    while True:
        message = new_socket.recv(1024).decode()
        print("\n" + message)

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()
while True:
    # input message we want to send to the server
    to_send =  input()
    # a way to exit the program
    if to_send.lower() == 'q':
        break
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{token}{to_send}{Fore.RESET}"
    # finally, send the message
    new_socket.send(to_send.encode())

# close the socket
new_socket.close()
