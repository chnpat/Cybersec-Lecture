import socket
import threading
from cryptography.fernet import Fernet

SERVER_HOST = "192.168.20.229"   # Please change this to your ip address
SERVER_PORT = 25550


def receive_messages(client_socket, fernet):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            decrypted_message = fernet.decrypt(message.decode())
            print(f"\nReceived: {decrypted_message}") # This is not a decryption. It just decodes the byte message into a string.
        except OSError:
            break
        except Exception as e:
            print(f"Error: {e}")

    client_socket.close()

def send_messages(client_socket, fernet):
    while True:
        try:
            message = input("Enter your message to send: ")
            # This will use the cryptography.fernet library to encrypt the plain text message before sending to the server.
            encrypted_message = fernet.encrypt(message) 
            client_socket.send(encrypted_message.encode()) # This is not an encryption. It just encodes a string into a byte format.
        except OSError:
            break
        except Exception as e:
            print(f"Error: {e}")

    client_socket.close()

if __name__ == "__main__":
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        # This line makes the client receives the key when the connection to the server is established.
        key = client_socket.recv(1024)
        # This will print out the received key (for debugging only) 
        print(f"Received key: {key.decode()}") 
        # Create an encryption algorimthm object.
        fernet = Fernet(key)

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,fernet))
        receive_thread.start()

        send_thread = threading.Thread(target=send_messages, args=(client_socket,fernet))
        send_thread.start()

        receive_thread.join()
        send_thread.join()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()