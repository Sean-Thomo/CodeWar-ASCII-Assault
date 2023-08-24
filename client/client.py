import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)
nickname = input("Choose a nickname: ")

def receive():
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == "NICK":
                client.send(nickname.encode(FORMAT))
            else:
                print(message)
        except:
            print("An Error occured")
            client.close()
            break


def send():
    while True:
        message = f"{nickname} > {input()}"
        client.send(message.encode(FORMAT))
    # message = msg.encode(FORMAT)
    # msg_length = len(message)
    # send_length = str(msg_length).encode(FORMAT)
    # send_length += b' ' * (HEADER-len(send_length))
    # client.send(send_length)
    # client.send(message)
    
if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    
    send_thread = threading.Thread(target=send)
    send_thread.start()