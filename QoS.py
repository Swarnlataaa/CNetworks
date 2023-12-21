import scapy.all as scapy
import time
from threading import Thread

class QoSMeasurementTool:
    def __init__(self, interface="eth0"):
        self.interface = interface

    def start_sniffing(self):
        scapy.sniff(iface=self.interface, store=False, prn=self.process_packet)

    def process_packet(self, packet):
        if packet.haslayer(scapy.IP):
            source_ip = packet[scapy.IP].src
            destination_ip = packet[scapy.IP].dst
            protocol = packet[scapy.IP].proto

            if protocol == 1:  # ICMP (ping)
                latency = self.calculate_latency(packet)
                print(f"ICMP Packet from {source_ip} to {destination_ip} - Latency: {latency} ms")

            # Add more conditions for different protocols or types of traffic

    def calculate_latency(self, packet):
        if packet.haslayer(scapy.ICMP) and packet[scapy.ICMP].type == 8:
            sent_time = packet[scapy.IP].time
            return (time.time() - sent_time) * 1000  # Convert to milliseconds
        return None

    def start_measurement(self):
        sniffer_thread = Thread(target=self.start_sniffing)
        sniffer_thread.start()

if __name__ == "__main__":
    qos_tool = QoSMeasurementTool()
    qos_tool.start_measurement()
