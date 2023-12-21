import paho.mqtt.client as mqtt
import threading
import time

class IoTDevice:
    def __init__(self, device_id, broker_address, port=1883):
        self.device_id = device_id
        self.broker_address = broker_address
        self.port = port
        self.client = mqtt.Client(self.device_id)
        self.client.on_message = self.on_message
        self.client.connect(self.broker_address, self.port, 60)
        self.client.subscribe(f"devices/{self.device_id}/commands")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        print(f"Received command '{payload}' from the server.")

    def send_data(self, data):
        topic = f"devices/{self.device_id}/data"
        self.client.publish(topic, data)
        print(f"Sent data '{data}' to the server.")

def server_thread():
    server = mqtt.Client("Server")
    server.connect("localhost", 1883, 60)

    while True:
        command = input("Enter a command to send to devices: ")
        server.publish("devices/+/commands", command)

if __name__ == "__main__":
    # Start the server thread
    server_thread = threading.Thread(target=server_thread)
    server_thread.daemon = True
    server_thread.start()

    # Create IoT devices
    device1 = IoTDevice("Device1", "localhost")
    device2 = IoTDevice("Device2", "localhost")

    # Send data from devices
    device1.send_data("Temperature: 25°C")
    device2.send_data("Humidity: 50%")

    # Keep the program running
    while True:
        time.sleep(1)
