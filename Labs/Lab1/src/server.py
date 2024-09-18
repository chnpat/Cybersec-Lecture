import socket
import threading
from cryptography.fernet import Fernet

SERVER_HOST = "192.168.20.229"   # Please change this to your ip address
SERVER_PORT = 25550

clients = []
key = Fernet.generate_key()
print(f"Generated key: {key.decode()}") 

def handle_client(client_socket, addr):
    client_socket.send(key) 
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break

            # This command will print out the message clients sent to the server
            print(f"Message received from {addr}: {message}")

            for client in clients:
                if client != client_socket:
                    client.send(message)
        except OSError:
            break

    client_socket.close()
    clients.remove(client_socket)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(2)
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while len(clients) < 2:  
        client_socket, addr = server.accept()
        print(f"New connection from {addr}")
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

    print("Both clients are connected. Ready to relay messages.")

if __name__ == "__main__":
    start_server()