import heapq

# Average human walking speed: 80 meters per minute = 4.8 km/h
WALKING_SPEED = 80  # meters per minute

def calculate_time(distance_meters):
    """Calculate estimated walking time in minutes and seconds"""
    total_minutes = distance_meters / WALKING_SPEED
    minutes = int(total_minutes)
    seconds = int((total_minutes - minutes) * 60)
    return minutes, seconds

def format_time(minutes, seconds):
    """Format time nicely for display"""
    if minutes == 0:
        return f"{seconds} seconds"
    elif seconds == 0:
        return f"{minutes} minute{'s' if minutes > 1 else ''}"
    else:
        return f"{minutes} minute{'s' if minutes > 1 else ''} and {seconds} second{'s' if seconds > 1 else ''}"

def dijkstra(graph, start):
    """Find shortest paths from start to all buildings"""
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parent = {node: None for node in graph}
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_node in visited:
            continue
        visited.add(current_node)
        
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parent[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    return distances, parent

def get_path(parent, destination):
    """Reconstruct path from start to destination"""
    if parent.get(destination) is None and destination not in parent:
        return []
    
    path = []
    current = destination
    
    while current is not None:
        path.append(current)
        current = parent.get(current)
    
    path.reverse()
    return path

def get_path_details(graph, start, end):
    """Get path with distance and walking time"""
    if start not in graph or end not in graph:
        return [], 0, 0, 0
    
    distances, parent = dijkstra(graph, start)
    path = get_path(parent, end)
    
    if not path or distances[end] == float('inf'):
        return [], 0, 0, 0
    
    distance = distances[end]
    minutes, seconds = calculate_time(distance)
    
    return path, distance, minutes, seconds

def find_all_paths(graph, start, end, path=None, max_depth=10):
    """Find all possible paths between start and end"""
    if path is None:
        path = [start]
    
    if len(path) > max_depth:
        return []
    
    if start == end:
        return [path]
    
    if start not in graph:
        return []
    
    all_paths = []
    for neighbor, weight in graph[start]:
        if neighbor not in path:
            new_paths = find_all_paths(graph, neighbor, end, path + [neighbor], max_depth)
            all_paths.extend(new_paths)
    
    return all_paths

def calculate_path_distance(graph, path):
    """Calculate total distance of a given path"""
    total = 0
    for i in range(len(path) - 1):
        for neighbor, dist in graph[path[i]]:
            if neighbor == path[i + 1]:
                total += dist
                break
    return total