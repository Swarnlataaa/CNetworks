import socket
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def generate_key_derivation_key():
    # Generate a key derivation key using a fixed, shared key
    shared_key = b'SharedSecretKey'
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'key_derivation_key',
    ).derive(shared_key)

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        plaintext = file.read()

    cipher = Cipher(algorithms.AES(key), modes.GCM())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return ciphertext, encryptor.tag

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8888))
    server_socket.listen(1)

    print("Server is listening for connections...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection established with {address}")

        # Key exchange using Diffie-Hellman
        client_public_key = int(client_socket.recv(4096).decode())
        server_private_key = 567  # Replace with secure key generation
        shared_key = pow(client_public_key, server_private_key, 1001)

        print("Shared Key:", shared_key)

        # Key derivation
        key_derivation_key = generate_key_derivation_key()
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'file_encryption_key',
        ).derive(bytes(str(shared_key), 'utf-8'))

        # File encryption
        file_path = 'example.txt'  # Replace with the path to your file
        ciphertext, tag = encrypt_file(file_path, derived_key)

        # Send encrypted file and tag to the client
        client_socket.sendall(ciphertext)
        client_socket.sendall(tag)

        client_socket.close()

if __name__ == "__main__":
    start_server()
