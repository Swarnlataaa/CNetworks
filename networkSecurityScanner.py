import nmap

class NetworkScanner:
    def __init__(self, target):
        self.target = target
        self.nm = nmap.PortScanner()

    def scan_ports(self, ports="1-1024"):
        print(f"Scanning ports on {self.target}...")
        self.nm.scan(hosts=self.target, arguments=f"-p {ports}")

    def print_open_ports(self):
        open_ports = []

        for host in self.nm.all_hosts():
            for proto in self.nm[host].all_protocols():
                lport = self.nm[host][proto].keys()
                for port in lport:
                    if self.nm[host][proto][port]['state'] == 'open':
                        open_ports.append(port)

        print(f"Open ports on {self.target}: {', '.join(map(str, open_ports))}")

    def service_identification(self):
        print("Identifying services on open ports...")
        for host in self.nm.all_hosts():
            for proto in self.nm[host].all_protocols():
                lport = self.nm[host][proto].keys()
                for port in lport:
                    service = self.nm[host][proto][port]['name']
                    print(f"Port {port}/{proto} is open, Service: {service}")

if __name__ == "__main__":
    target_ip = "127.0.0.1"  # Change this to the target IP address or hostname

    scanner = NetworkScanner(target_ip)

    # Perform port scanning
    scanner.scan_ports()

    # Print open ports
    scanner.print_open_ports()

    # Identify services on open ports
    scanner.service_identification()
