import scapy.all as scapy

class SimpleIDS:
    def __init__(self):
        self.signature_patterns = ["malicious_pattern1", "malicious_pattern2"]
        self.anomaly_threshold = 100  # Adjust the threshold based on network behavior

    def packet_callback(self, packet):
        if packet.haslayer(scapy.IP):
            ip_src = packet[scapy.IP].src
            ip_dst = packet[scapy.IP].dst

            # Signature-based detection
            for pattern in self.signature_patterns:
                if pattern in str(packet):
                    print(f"Signature-based detection: Suspicious pattern {pattern} detected in {ip_src} to {ip_dst}")

            # Anomaly-based detection
            if len(packet) > self.anomaly_threshold:
                print(f"Anomaly-based detection: Unusually large packet detected from {ip_src} to {ip_dst}")

    def start_sniffing(self):
        scapy.sniff(prn=self.packet_callback, store=False)

if __name__ == "__main__":
    ids = SimpleIDS()
    ids.start_sniffing()
