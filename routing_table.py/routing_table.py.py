import heapq

def load_network(input_file):
    net = {}
    with open(input_file, 'r') as file:
        _ = file.readline()  # Skip the first line
        for line in file:
            if line.strip():
                n1, n2, cost = line.split()
                n1, n2, cost = int(n1), int(n2), float(cost)

                if n1 not in net:
                    net[n1] = {}
                if n2 not in net:
                    net[n2] = {}

                net[n1][n2] = cost
                net[n2][n1] = cost
    return net

def algo(net, start_n):
    shortest_p = {n: float('inf') for n in net}
    prev_n = {n: None for n in net}
    shortest_p[start_n] = 0
    pq = [(0, start_n)]

    while pq:
        current_d, current_n = heapq.heappop(pq)
        if current_d > shortest_p[current_n]:
            continue

        for neighbor, weight in net[current_n].items():
            updated_d = current_d + weight
            if updated_d < shortest_p[neighbor]:
                shortest_p[neighbor] = updated_d
                prev_n[neighbor] = current_n
                heapq.heappush(pq, (updated_d, neighbor))

    return shortest_p, prev_n

def generate_routing_data(net):
    routing_data = {}

    for start_n in net:
        shortest_p, prev_n = algo(net, start_n)

        routing_table = {}
        for target_n in net:
            route = []
            current_n = target_n

            while current_n is not None:
                route.insert(0, current_n)
                current_n = prev_n[current_n]

            next_hop = route[1] if len(route) > 1 else None
            routing_table[target_n] = {
                'cost': shortest_p[target_n],
                'route': route,
                'next_hop': next_hop
            }

        routing_data[start_n] = routing_table

    return routing_data

def display_routing_data(routing_data):
    for n, table in routing_data.items():
        print(f"\nRouting Data for Node {n}:")
        print("Destination  Cost    Next Hop  Route                                  ")
        print("---------------------------------------------------------------")
        for dest_n, info in table.items():
            cost = f"{info['cost']:.2f}"
            route = " -> ".join(map(str, info["route"]))
            next_hop = info["next_hop"]
            next_hop_str = str(next_hop) if next_hop is not None else "None"

            current_n_marker = "   <---     (currently on this node)" if dest_n == n else ""

            print(f"{dest_n:<12} {cost:<8} {next_hop_str:<9} {route:<40}{current_n_marker}")

def main():
    input_file = "net.txt"
    net = load_network(input_file)
    routing_data = generate_routing_data(net)
    display_routing_data(routing_data)

if __name__ == "__main__":
    main()
