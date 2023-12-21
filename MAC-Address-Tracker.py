from scapy.all import ARP, Ether, srp

def get_mac(ip):
    # Create ARP request packet
    arp_request = ARP(pdst=ip)

    # Create Ethernet frame
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    # Combine Ethernet frame and ARP request packet
    packet = ether / arp_request

    # Send and receive ARP packets
    result = srp(packet, timeout=3, verbose=0)[0]

    # Return the MAC address from the response
    return result[0][1].hwsrc if result else None

def mac_address_tracker(ip_range):
    print("Scanning for devices...\n")
    print("IP Address\t\tMAC Address\n-----------------------------------------")

    for ip in ip_range:
        mac_address = get_mac(ip)
        if mac_address:
            print(f"{ip}\t\t{mac_address}")

if __name__ == "__main__":
    # Specify the IP range to scan (modify as needed)
    ip_range = ["192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4"]

    mac_address_tracker(ip_range)
