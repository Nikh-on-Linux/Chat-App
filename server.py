import socket
import threading

# Server setup
HOST = '127.0.0.1'  # Localhost
PORT = 12345         # Port to bind

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Broadcast message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle individual client
def handle_client(client):
    while True:
        try:
            # Receive message from a client
            message = client.recv(1024)
            broadcast(message)
        except:
            # Remove disconnected client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode('utf-8'))
            nicknames.remove(nickname)
            break

# Accept connections from clients
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        # Get nickname
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send("Connected to the server!".encode('utf-8'))

        # Start handling thread for the client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Server is running...")
receive()
