import socket
import threading

# Configuration to match the server
host = 'localhost'
port = 12345

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == '/login':
                client.send(f'/login {nickname} {input("Password: ")}'.encode('utf-8'))
            elif message.startswith('/login success'):
                print("Logged in successfully!")
            elif message.startswith('/login fail'):
                print("Login failed. Check your credentials.")
                client.close()
                break
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = f'{input("")}'
        if message.startswith('/pm'):
            client.send(message.encode('utf-8'))
        else:
            client.send(f'{nickname}: {message}'.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
