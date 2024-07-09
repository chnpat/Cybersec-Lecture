# Open Lab Session II

## Overview

In the 4th lecture, we've learned about how we can ensure data integrity during the transmission. It is important that client applications can authenticate and check for data tampering. In this open lab session, we will enhance our chat application from the previous open lab session to generate a signature of each message and send it along with the message to another client.

## Instruction
### A. Simple Hash function.

1. Download and extract the source code folder into your directory.

> https://drive.google.com/file/d/1y7ptIkxny5PMNwYP77_828SNIJvmhUBX/view?usp=sharing 

2. Open a terminal (in the Visual Studio Code) and change the directory to the location you saved the lab source code.

```console
~$ cd labs/lab2/
```

3. Create a Python virtual environment for install dependencies.

```console
/labs/lab1$ pwd

/labs/lab1/

/labs/lab1$ python3 -m venv /labs/lab2/
```

4. After the virtual environment is created, you can activate and use it with the following command:


```console
~$ source bin/activate
```

5. We can now install a library used for data integrity as follows:

```console
~$  pip3 install pycryptodome
```


6. Then, we can now try running the simple hash program:

```console
labs/lab2$ python3 simple_hash.py
```

### B. Data Integrity Checking with Signatures

1. Now, we will start improving our chat application. Initiate a dependency to the `Hash` package from pycryptodome after other imports in the `client.py` file.

```python
import socket
import threading

# Add the line below:
from Crypto.Hash import SHA256                                          
```
2. Then, we must find and change it to the IP address to your one in the `client.py` file:

```console
~$ ipconfig getifaddr en0
192.168.1.108
```

```python
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Change the IP address herer.
host = "192.168.1.105"
port = 25550
```

3. Add the following code fragment to the `receive_messages(client_socket)` function of the `client.py` file.

```python
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
```

4. Add the following code fragment to the `send_messages(client_socket)` function of the `client.py` file.

```python
while True:
    message = input(">> ")
    if message.lower() == 'exit':
        client_socket.close()
        break
    hash_value = SHA256.new()
    hash_value.update(message.encode('utf-8'))
    message = message + "|" + hash_value.hexdigest()
    client_socket.send(message.encode('utf-8'))
```

5. Try to run the program files.