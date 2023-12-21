import socket
import threading
import pickle
import zlib
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk

class RemoteDesktopClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        self.root = tk.Tk()
        self.root.title("Remote Desktop Client")

        self.label = tk.Label(self.root)
        self.label.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.is_running = True

    def on_close(self):
        self.is_running = False
        self.client_socket.close()
        self.root.destroy()

    def receive_screen(self):
        try:
            while self.is_running:
                compressed_data = self.client_socket.recv(4096)
                screenshot_data = zlib.decompress(compressed_data)
                screenshot = pickle.loads(screenshot_data)

                screenshot_image = ImageTk.PhotoImage(screenshot)
                self.label.config(image=screenshot_image)
                self.label.image = screenshot_image

                self.root.update()
        except Exception as e:
            print(f"Error receiving screen: {e}")
            self.client_socket.close()

    def send_input(self, event_type, event_data):
        try:
            input_data = {'event_type': event_type, 'event_data': event_data}
            serialized_data = pickle.dumps(input_data)
            self.client_socket.sendall(serialized_data)
        except Exception as e:
            print(f"Error sending input: {e}")
            self.client_socket.close()

    def handle_keyboard(self, event):
        key = event.char
        self.send_input('keyboard', key)

    def handle_mouse(self, event):
        x, y = event.x, event.y
        self.send_input('mouse', (x, y))

    def start(self):
        screen_thread = threading.Thread(target=self.receive_screen)
        screen_thread.start()

        self.root.bind("<Key>", self.handle_keyboard)
        self.root.bind("<B1-Motion>", self.handle_mouse)

        self.root.mainloop()

if __name__ == "__main__":
    client = RemoteDesktopClient('127.0.0.1', 5555)
    client.start()
