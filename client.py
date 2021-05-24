import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
import socket
import os
import tqdm

init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
          Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
          Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, 
          Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.YELLOW
          ]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine,

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002  # server's port
separator_token = "<SEP>" 

# initialize TCP socket
s = socket.socket()

print(f"[*] Connecting to server...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

name = input("Enter your name: ")
# send name of client to server
s.send(name.encode())

# choose a peer
peer = str(
    input('Who do you want to connect with? (Enter username of a connected peer): '))
while(peer == name):
    print('You cannot choose yourself as a peer. ')
    peer = str(
        input('Who do you want to connect with? (Enter username of a connected peer): '))
s.send(peer.encode())

directory = os.getcwd()
path = os.path.join(directory, name)

if not os.path.exists(path):
    os.makedirs(path)

def listen_for_messages():
    while True:
        try:
            message = s.recv(256).decode()
            message = message.replace(separator_token, ": ")
        except Exception as e:
            print(e)
            message = s.recv(256)

        if message[-17:] == 'has left the chat':
            print(
                'Press q to close connection. Please rejoin to connect with another peer.')
            break
        elif "//file" in message:

            file = message.split('//file ')[1]
            files = (file.split(' '))
            filename = files[0]
            file_data = files[1].split('<=>')
            filesize = int(file_data[0])

            junkvar = filesize
            filename = os.path.join(filename)
            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=256)
            with open(filename, "wb") as f:
                while True:
                    if junkvar <= 0:
                        # nothing is received
                        # file transmitting is done
                        break
                    # read 256 bytes from the socket (receive)
                    junkvar -= 256
                    bytes_read = s.recv(256)
                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))
                f.close()
        elif message != 'q':
            print('\n',message,'\n')


# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()
junk_value = 0
while True:
    # input message we want to send to the server
    print('\n')
    to_send = input()
    # a way to exit the program
    if to_send.lower() == 'q':
        s.send(to_send.encode())
        break
    elif to_send[:6] == '//send':
        filename = to_send[6:]
        filesize = os.path.getsize(name + '/'+filename)
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        to_send = f"//file {peer + '/' +filename} {filesize}<=>"
        s.send(to_send.encode())

        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=256)
        junk_value = filesize
        with open(name + '/'+filename, "rb") as f:
            while True:
                # read the bytes from the file
                if junk_value <= 0:
                    s.send(bytes('', encoding='utf-8'))
                    break
                junk_value -= 256
                bytes_read = f.read(256)

                s.send(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        f.close()
    else:
        # add the datetime, name & the color of the sender
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
        # finally, send the message
        s.send(to_send.encode())

# close the socket
s.close()
