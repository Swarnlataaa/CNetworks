import heapq
import threading
import time

class RoutingTable:
    def __init__(self):
        self.table = {}

    def add_route(self, destination, next_hop, cost):
        self.table[destination] = {'next_hop': next_hop, 'cost': cost}

    def get_next_hop(self, destination):
        return self.table.get(destination, {}).get('next_hop', None)

class Router:
    def __init__(self, router_id):
        self.router_id = router_id
        self.routing_table = RoutingTable()
        self.neighbours = {}
        self.lock = threading.Lock()

    def add_neighbour(self, neighbour_id, cost):
        with self.lock:
            self.neighbours[neighbour_id] = cost

    def update_routing_table(self, new_table):
        with self.lock:
            self.routing_table.table.update(new_table)

    def send_routing_table(self, neighbour_id):
        neighbour_cost = self.neighbours.get(neighbour_id, float('inf'))
        with self.lock:
            return {self.router_id: {'next_hop': self.router_id, 'cost': neighbour_cost}}

class Network:
    def __init__(self):
        self.routers = {}

    def add_router(self, router_id):
        self.routers[router_id] = Router(router_id)

    def simulate(self):
        for router_id, router in self.routers.items():
            for neighbour_id, cost in router.neighbours.items():
                neighbour_routing_table = self.routers[neighbour_id].send_routing_table(router_id)
                router.update_routing_table(neighbour_routing_table)

        for router_id, router in self.routers.items():
            print(f"Router {router_id} Routing Table:")
            print(router.routing_table.table)
            print()

if __name__ == "__main__":
    network = Network()

    # Add routers to the network
    network.add_router('R1')
    network.add_router('R2')
    network.add_router('R3')

    # Set up neighbours and costs
    network.routers['R1'].add_neighbour('R2', 1)
    network.routers['R2'].add_neighbour('R1', 1)
    network.routers['R2'].add_neighbour('R3', 2)
    network.routers['R3'].add_neighbour('R2', 2)

    # Simulate the network
    for _ in range(5):
        network.simulate()
        time.sleep(2)
