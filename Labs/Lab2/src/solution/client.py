import socket
import threading
from Crypto.Hash import SHA256


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break

            print(f"Other Client: {message.decode('utf-8')}")
            
            msg_arr = message.decode('utf-8').split("|")
            hash_value = SHA256.new()
            hash_value.update(msg_arr[0].encode('utf-8'))
            
            if(hash_value.hexdigest() == msg_arr[1]):
                print(f"Message is authenticated: {hash_value.hexdigest()} is identical to {msg_arr[1]}")
            else:
                print(f"The received message is tampered!")
        except:
            print("Error receiving message.")
            client_socket.close()
            break


def send_messages(client_socket):
    while True:
        message = input(">> ")
        if message.lower() == 'exit':
            client_socket.close()
            break
        hash_value = SHA256.new()
        hash_value.update(message.encode('utf-8'))
        message = message + "|" + hash_value.hexdigest()
        client_socket.send(message.encode('utf-8'))


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.1.105"
    port = 25550
    client_socket.connect((host, port))

    print("Connected to the server.")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()


if __name__ == "__main__":
    start_client()