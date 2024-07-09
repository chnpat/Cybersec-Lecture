# Simple demonstration of hashing using SHA-256

from Crypto.Hash import SHA256

while True:
    message = input("Enter a message: ")
    if message == 'exit':
        break
    hash_object = SHA256.new()
    hash_object.update(message.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    print(hex_dig)