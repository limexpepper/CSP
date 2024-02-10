import heapq

def dijkstra(graph, source, destination):
    pq = [(0, source, graph[source]['open'], [])]  # Priority queue (distance, node, arrival_time, path)
    distance = {node: float('inf') for node in graph}
    distance[source] = 0

    while pq:
        dist, current, arrival_time, path = heapq.heappop(pq)
        
        if current == destination:
            return distance[current], path
        
        if dist > distance[current]:  # Skip outdated nodes
            continue
        
        for neighbor, info in graph[current]['neighbors'].items():
            travel_time = info['travel_time']
            neighbor_open = info['open']
            neighbor_close = info['close']
            
            # Calculate arrival time at neighbor
            new_arrival_time = max(arrival_time + travel_time, neighbor_open)
            
            if new_arrival_time < neighbor_close - 60:  # Ensure at least 1 hour before closing
                if new_arrival_time < distance[neighbor]:
                    distance[neighbor] = new_arrival_time
                    heapq.heappush(pq, (new_arrival_time, neighbor, neighbor_open, path + [current]))
            else:  # If visiting the waypoint during opening hours is not possible
                while path:
                    print("Earlier waypoints in the path:")
                    for i, waypoint in enumerate(path):
                        print(f"{i + 1}. {waypoint}")
                    choice = input("Choose an earlier waypoint to pop off (enter its index) or press Enter to skip: ")
                    if choice == "":
                        break
                    try:
                        choice_index = int(choice) - 1
                        if 0 <= choice_index < len(path):
                            popped_node = path.pop(choice_index)
                            popped_node_travel_time = graph[popped_node]['neighbors'][current]['travel_time']
                            new_arrival_time -= popped_node_travel_time
                            if new_arrival_time >= neighbor_close - 60:
                                heapq.heappush(pq, (new_arrival_time, neighbor, neighbor_open, path))
                                break
                            else:
                                print("Not enough time to reach the current waypoint at least one hour before its closing time.")
                        else:
                            print("Invalid index.")
                    except ValueError:
                        print("Invalid input. Please enter a valid index.")
                        continue

    return float('inf'), None  # Destination is unreachable

def main():
    # Mock location data and opening hours data
    graph = {
        'A': {'open': 0, 'neighbors': {'B': {'travel_time': 5, 'open': 10, 'close': 18}}},
        'B': {'open': 10, 'neighbors': {'C': {'travel_time': 3, 'open': 12, 'close': 17}, 'D': {'travel_time': 4, 'open': 13, 'close': 19}}},
        'C': {'open': 12, 'neighbors': {'D': {'travel_time': 2, 'open': 13, 'close': 18}}},
        'D': {'open': 13, 'neighbors': {}}
    }
   
    source = 'A'
    destination = 'D'

    shortest_distance, shortest_path = dijkstra(graph, source, destination)
    if shortest_distance == float('inf'):
        print("Destination is unreachable.")
    else:
        print("Shortest distance:", shortest_distance)
        print("Shortest path:", shortest_path)

if __name__ == "__main__":
    main()
