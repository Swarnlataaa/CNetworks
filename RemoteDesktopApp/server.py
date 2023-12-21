import socket
import threading
from PIL import ImageGrab
import pickle
import zlib

def send_screen(conn):
    try:
        while True:
            screenshot = ImageGrab.grab()
            screenshot_data = pickle.dumps(screenshot)
            compressed_data = zlib.compress(screenshot_data)
            conn.sendall(compressed_data)
    except Exception as e:
        print(f"Error sending screen: {e}")
        conn.close()

def receive_input(conn):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            input_data = pickle.loads(data)
            handle_input(input_data)
    except Exception as e:
        print(f"Error receiving input: {e}")
        conn.close()

def handle_input(input_data):
    event_type = input_data['event_type']
    event_data = input_data['event_data']

    if event_type == 'mouse':
        x, y = event_data
        pyautogui.moveTo(x, y)

    elif event_type == 'keyboard':
        pyautogui.press(event_data)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen(1)

    print("Waiting for a connection...")
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    screen_thread = threading.Thread(target=send_screen, args=(conn,))
    input_thread = threading.Thread(target=receive_input, args=(conn,))

    screen_thread.start()
    input_thread.start()

    screen_thread.join()
    input_thread.join()

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
