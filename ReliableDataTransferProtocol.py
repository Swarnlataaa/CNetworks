import time
import random

class ReliableDataTransfer:
    def __init__(self, packet_loss_probability=0.1):
        self.packet_loss_probability = packet_loss_probability

    def simulate_packet_loss(self):
        return random.random() < self.packet_loss_probability

    def send_data(self, data):
        if self.simulate_packet_loss():
            print("Packet lost! Retransmitting...")
            return None
        else:
            return data

    def receive_data(self, data):
        return data

def sender(data, rdt):
    for packet in data:
        while True:
            ack = rdt.send_data(packet)
            if ack is not None:
                print(f"Sender: Acknowledgment received: {ack}")
                break

def receiver(rdt):
    received_data = []
    while True:
        data = rdt.receive_data("Received data")
        if data is not None:
            received_data.append(data)
            print(f"Receiver: Data received: {data}")
            rdt.send_data("ACK")

            # Simulate processing delay
            time.sleep(1)

            # Simulate end of transmission
            if random.random() < 0.1:
                break

    return received_data

if __name__ == "__main__":
    data_to_send = ["Packet 1", "Packet 2", "Packet 3", "Packet 4", "Packet 5"]

    # Simulate packet loss probability of 10%
    rdt = ReliableDataTransfer(packet_loss_probability=0.1)

    print("Starting communication:")
    sender(data_to_send, rdt)

    # Simulate network delay
    time.sleep(3)

    received_data = receiver(rdt)
    print("\nReceived Data:")
    for packet in received_data:
        print(packet)
