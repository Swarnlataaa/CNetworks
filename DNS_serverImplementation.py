import socket
import threading

class DNSRecord:
    def __init__(self, domain, record_type, data):
        self.domain = domain
        self.record_type = record_type
        self.data = data

class DNSServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.records = [
            DNSRecord("example.com", "A", "192.168.1.1"),
            DNSRecord("www.example.com", "CNAME", "example.com"),
            # Add more DNS records as needed
        ]
        self.cache = {}

    def resolve_domain(self, domain, record_type):
        for record in self.records:
            if record.domain == domain and record.record_type == record_type:
                return record.data
        return None

    def handle_dns_query(self, query):
        domain = query.decode("utf-8").strip()

        if domain in self.cache:
            response = self.cache[domain]
        else:
            ip_address = self.resolve_domain(domain, "A")
            cname = self.resolve_domain(domain, "CNAME")

            if ip_address:
                response = f"{domain} IN A {ip_address}"
            elif cname:
                response = f"{domain} IN CNAME {cname}"
            else:
                response = f"{domain} not found"

            # Cache the response for future use
            self.cache[domain] = response

        return response.encode("utf-8")

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((self.host, self.port))
            print(f"DNS Server listening on {self.host}:{self.port}")

            while True:
                data, client_address = server_socket.recvfrom(1024)
                response_data = self.handle_dns_query(data)
                server_socket.sendto(response_data, client_address)

if __name__ == "__main__":
    dns_server = DNSServer("127.0.0.1", 53)  # Change the IP and port as needed
    dns_server.start_server()
