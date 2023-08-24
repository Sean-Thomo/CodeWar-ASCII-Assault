import socket
import threading


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) #127.0.1.1
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

# Handle individual connections concurrently
def handle_client(client, address):
    conn_message = f"Server > [NEW CONNECTION] {address} joined the world."
    print(conn_message)
    
    connected = True
    while connected:
        try:
            msg_length = client.recv(HEADER).decode(FORMAT) #blocking line
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                
                print(f"{address} > {msg}")
                client.send("Msg received".encode(FORMAT))
        except:
            index = clients.index(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"Server > {nickname} left the world.".encode(FORMAT))
            nicknames.remove(nickname)
            break
        
    client.close()


# Handle new connection
def start():
    server.listen()
    print(f"Server > listening on {SERVER}")
    while True:
        # conn - socket allows us to communucate back connected client
        # address - info about the connection
        client, address = server.accept() # bloacking line
        
        client.send("NICK".encode())
        nickname = client.recv(1024).decode(FORMAT)
        nicknames.append(nickname)
        clients.append(client)
        
        print(f"Nickname of the client is {nickname}!")
        broadcast(f"Server > {nickname} joined the world".encode())

        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()
        # print(f"Server > [ACTIVE CONNECTIONS] {threading.active_count()-1}")



if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    print("Server > Sever is starting...")
    start()