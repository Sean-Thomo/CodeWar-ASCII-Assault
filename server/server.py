import socket
import threading


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) #127.0.1.1
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Handle individual connections concurrently
def handle_client(conn, addr):
    print(f"Server > [NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) #blocking line
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False
        
        print(f"{addr} > {msg}")
        
    conn.close()


# Handle new connection
def start():
    server.listen()
    
    print(f"Server > listening on {SERVER}")
    while True:
        # conn - socket allows us to communucate back connected client
        # addr - info about the connection
        conn, addr = server.accept() # bloacking line
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Server > [ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        

print("Server > Sever is starting...")
start()