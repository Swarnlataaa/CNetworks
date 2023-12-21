import socket
import zlib
import pickle

def optimize_data(data):
    # Compression at the presentation layer
    compressed_data = zlib.compress(pickle.dumps(data))
    return compressed_data

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8888))

    # Receive data from the server
    received_data = client_socket.recv(4096)

    # Decompression at the presentation layer
    decompressed_data = pickle.loads(zlib.decompress(received_data))

    print(f"Received data from server: {decompressed_data}")

if __name__ == "__main__":
    start_client()
