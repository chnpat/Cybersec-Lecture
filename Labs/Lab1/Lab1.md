# Open Lab Session I

## Overview 
We explored some basic and classical cryptography schemes from the previous lecture. You may get the concept of how data are protected by encryption algorithms. Typically, those classical cryptography schemes are broken and are no longer secure for current information systems. However, it is good to know how mathematicians and engineers think about encryption and decryption from the beginning.  In this open lab session, you will be asked to explore on how an information system (a chat application, to be exact) can leverage the encryption algorithm to protect user messages during the transmissions.

## Instruction
Please follow the steps below to install the environment for the target chat application. The given chat application is implemented in Python and consists of two main components, i.e., client.py and server.py. The client.py is a source code for a simple Command Line Interface (CLI) application that users can connect to the server (i.e., server.py) and send a message to another client.

1.	Download and extract the source code zip file from the Google Drive link provided into your file directory.

    - https://drive.google.com/file/d/19Sr1o373AQfZ-q5fwao99LapOqtomuF0/view?usp=sharing 

2.	Install the latest version of Python into your environment

    1. https://www.python.org/ 
    2. Make sure that the Python is working properly by running the “python3 --version” and it should print out the current version of Python installed.
3.	Install Visual Studio Code into your environment.
    1. Go to https://code.visualstudio.com/download and download the one that matches with your operating system.
4.	Open the source code directory downloaded in the first step (1) in the Visual Studio Code and try to look through the provided source code. There are two files as mentioned earlier. We use the “`socket`” library to establish internet connection and use the “`threading`” library to establish thread processing.
5.	Open the terminal console in the Visual Studio Code and try to create a virtual environment.
    1. Check the present working directory path by typing in the “`pwd`” command in the terminal. If it turns out that the present working directory is not the directory we download the source code, you have to change the directory by using the “`cd`” command.
    2. Copy the output of the “`pwd`” command for the further step.
    3. Create a Python virtual environment by typing the command below. There will be possible to have an error if the present working directory path consists of a whitespace ( ). It can be fixed by adding a backslash before the whitespace ( ) -> (\ ).
    ```
    python3 -m venv [the path you copied from the step 5.1]
    ``` 
    
    4. Active the created virtual environment by using the “source bin/activate” command.
6.	Check your current IP address from the terminal:
    1. https://www.avg.com/en/signal/find-ip-address 
    2. Copy the IPv4 address for configuring the chat application source code.
7.	Open the “`server.py`” and “`client.py`” source code files in the Visual Studio Code.
8.	Configure the IP address on line 4 of the “`server.py`” file to your IP address from step 6.
9.	Configure the IP address on line 4 of the “`client.py`” file to your IP address from step 6.
10.	In the terminal, try to run the “`server.py`” file by using the following command. Check whether it can run properly or not. It is expected that the terminal prints out the “`Server started on [your IP address]:25550`”.
```
python3 server.py
``` 
11.	Open a new terminal console in the Visual Studio Code by clicking the “+” button on the top right corner of the current terminal. It will show another terminal with the navigation pane on the righthand side.
12.	In the second terminal, try to run the “`client.py`” file by using the following command. Check whether it can run properly or not.
```
python3 client.py
```

13.	Repeat the 11th and 12th steps to instantiate another client. At the end of this step, you must have one terminal for the “`server.py`” file, and two terminals for the “`client.py`” file. After you run all the files correctly, the terminal for the “`server.py`” file should print out a message “`Both clients are connected. Ready to relay messages.`”
14.	You can type in a message to one of the “`client.py`” terminals and see whether it deliver the message properly.
15.	In the “`server.py`” terminal, check whether the server can read the message properly or not.
16.	**Try to implement an encryption algorithm to the client side. The goal of this implementation is to ensure that the server instance cannot read the plain text message. Only two client instances can read the plain text message. You can implement any classic cryptography schemes from the lecture.**
17.	Try to install import the “`cryptography`” library in Python to use the Fernet Token encryption algorithm.
a.	In the terminal, install the “`cryptography`” library in Python by typing: 
```
pip3 install cryptography
```
18.	Add the encryption features to the chat application to ensure its data confidentiality.
19. After the line of “`clients = []`” in the “`server.py`” file, add the following code segment:
```Python
# This will generate a secret key that will be shared among clients. This is used the symmetric key cryptography scheme.
key = Fernet.generate_key() 

# This will print out the generated secret key for the debugging purpose.
print(f"Generated key: {key.decode()}") 
```

20. After the “`def handle_client(client_socket):`” line in the “`server.py`” file, add the following code segment:
```Python	
# This will send the secret key to all clients when they initiate the first connection with the server.
client_socket.send(key) 
```
21. After the “`import threading`” line in the “`client.py`” file, add the following command.
```Python
from cryptography.fernet import Fernet
```
22. Change the “`receive_messages`” method in the “`client.py`” file from “`receive_messages(client_socket):`” into:
```Python 
def receive_messages(client_socket, fernet):
```

23.	Before the “`print(f"\nReceived: {message.decode()}")`” line in the “`client.py`” file, add the following code segment:
```Python
# This will use the cryptography.fernet library to decrypt the encrypted message when it arrives the recipient client.
message = fernet.decrypt(message).decode() 
```
24. Change the “`send_messages`” method in the “`client.py`” file from 
“`def send_messages(client_socket):`” into 
```Python
def send_messages(client_socket, fernet):
```
25.	Before the “`client_socket.send(message.encode())`” line in the “`client.py`” file, add the following code segment:
```Python
# This will use the cryptography.fernet library to encrypt the plain text message before sending to the server.
encrypted_message = fernet.encrypt(message.encode()) 
```
26.	After the “`client_socket.connect((SERVER_HOST, SERVER_PORT))`” line in the “`client.py`” file, add the following code segments:

```Python
# This line makes the client receives the key when the connection to the server is established.
key = client_socket.recv(1024)
# This will print out the received key (for debugging only) 
print(f"Received key: {key.decode()}") 
# Create an encryption algorimthm object.
fernet = Fernet(key)
```
27.	Change the “`receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))`” line in the “`client.py`” file into:
```Python
# Ask the thread for receiving messages to use the decryption
receive_thread = threading.Thread(target=receive_messages, args=(client_socket, fernet))
```
28.	Change the “`send_thread = threading.Thread(target=send_messages, args=(client_socket,))`” line in the “`client.py`” file into: 
```Python
# Ask the thread for sending messages to use the encryption
send_thread = threading.Thread(target=send_messages, args=(client_socket, fernet))
```
29.	Try to run the chat application again and see the result.
