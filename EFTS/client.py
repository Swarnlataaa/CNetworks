import socket
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

def decrypt_file(ciphertext, tag, key):
    cipher = Cipher(algorithms.AES(key), modes.GCM(tag))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8888))

    # Key exchange using Diffie-Hellman
    client_private_key = 123  # Replace with secure key generation
    client_public_key = pow(5, client_private_key, 1001)
    client_socket.sendall(bytes(str(client_public_key), 'utf-8'))

    # Shared key derivation
    shared_key = pow(int(client_socket.recv(4096).decode()), client_private_key, 1001)

    print("Shared Key:", shared_key)

    # Key derivation
    key_derivation_key = generate_key_derivation_key()
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'file_encryption_key',
    ).derive(bytes(str(shared_key), 'utf-8'))

    # Receive encrypted file and tag from the server
    ciphertext = client_socket.recv(4096)
    tag = client_socket.recv(16)

    # File decryption
    decrypted_data = decrypt_file(ciphertext, tag, derived_key)

    print("Decrypted Data:", decrypted_data.decode('utf-8'))

if __name__ == "__main__":
    start_client()
