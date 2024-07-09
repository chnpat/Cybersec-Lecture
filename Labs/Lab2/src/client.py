import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break

            print(f"Other Client: {message.decode('utf-8')}")
            
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
        client_socket.send(message.encode('utf-8'))


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Change to your ip address
    # -------------------------
    # For Windows:  Type 'ipconfig' in the command prompt
    # For Unix:     Type 'ipconfig getifaddr en0' 
    host = "192.168.1.1"
    port = 25550
    client_socket.connect((host, port))

    print("Connected to the server.")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()


if __name__ == "__main__":
    start_client()