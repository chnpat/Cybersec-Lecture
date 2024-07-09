import socket
import threading

SERVER_HOST = "192.168.1.1"   # Please change this to your ip address
SERVER_PORT = 25550


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"\nReceived: {message.decode()}") # This is not a decryption. It just decodes the byte message into a string.
        except OSError:
            break
        except Exception as e:
            print(f"Error: {e}")

    client_socket.close()

def send_messages(client_socket):
    while True:
        try:
            message = input("Enter your message to send: ")
            client_socket.send(message.encode()) # This is not an encryption. It just encodes a string into a byte format.
        except OSError:
            break
        except Exception as e:
            print(f"Error: {e}")

    client_socket.close()

if __name__ == "__main__":
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        send_thread = threading.Thread(target=send_messages, args=(client_socket,))
        send_thread.start()

        receive_thread.join()
        send_thread.join()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()