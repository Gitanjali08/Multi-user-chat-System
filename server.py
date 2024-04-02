import socket
import threading
import json

# Server Configuration
host = 'localhost'
port = 12345

# Store clients and their addresses
clients = []
nicknames = []

# User credentials for authentication
user_credentials = {"user1": "password1", "user2": "password2"}


def broadcast(message, _sender=None):
    for client in clients:
        if client != _sender:
            client.send(message)


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('utf-8').startswith('/login'):
                _, username, password = message.decode('utf-8').split()
                if username in user_credentials and user_credentials[username] == password:
                    client.send('/login success'.encode('utf-8'))
                    broadcast(f"{username} has joined the chat!".encode('utf-8'), client)
                    nicknames.append(username)
                    print(f"{username} has logged in")
                else:
                    client.send('/login fail'.encode('utf-8'))
            elif message.decode('utf-8').startswith('/pm'):
                _, recipient, *content = message.decode('utf-8').split()
                content = ' '.join(content)
                if recipient in nicknames:
                    target = clients[nicknames.index(recipient)]
                    target.send(f"PM from {nicknames[clients.index(client)]}: {content}".encode('utf-8'))
            else:
                broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"Server running on {host}:{port}")

    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        clients.append(client)

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
