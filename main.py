from graph import Graph
from dijkstra import get_path_details, find_all_paths, calculate_path_distance, format_time, calculate_time
from utils import save_graph, load_graph

def display_menu():
    print("\n" + "="*50)
    print("   CAMPUS NAVIGATOR SYSTEM ")
    print("="*50)
    print("1.  Add Building")
    print("2.  Remove Building")
    print("3.  Add Path")
    print("4.  Remove Path")
    print("5.  Display Map")
    print("6.  Find Shortest Path")
    print("7.  Find All Possible Paths")
    print("8.  List All Buildings")
    print("9.  Check Building Connections")
    print("10.  Save & Exit")
    print("="*50)

def list_buildings(graph):
    buildings = graph.get_all_buildings()
    if not buildings:
        print("\n No buildings in the campus yet.")
        return []
    
    print("\n BUILDINGS IN CAMPUS:")
    for i, building in enumerate(buildings, 1):
        conn_count = len(graph.graph.get(building, []))
        print(f"   {i}. {building:<20} ({conn_count} connection{'s' if conn_count != 1 else ''})")
    return buildings

def find_shortest_path_interface(graph):
    buildings = list_buildings(graph)
    if len(buildings) < 2:
        print("\n Need at least 2 buildings to find a path.")
        return
    
    print("\n FIND SHORTEST PATH")
    print("-" * 30)
    
    start = input("Enter start building: ").strip().title()
    end = input("Enter destination: ").strip().title()
    
    if start not in graph.graph:
        print(f" Building '{start}' not found!")
        return
    if end not in graph.graph:
        print(f" Building '{end}' not found!")
        return
    
    path, distance, minutes, seconds = get_path_details(graph.graph, start, end)
    
    if not path or distance == float('inf'):
        print(f"\n No path exists from '{start}' to '{end}'!")
        return
    
    print("\n" + "="*50)
    print(" SHORTEST PATH FOUND")
    print("="*50)
    print(f" Route: {' → '.join(path)}")
    print(f" Total Distance: {distance} meters")
    print(f" Estimated Walking Time: {format_time(minutes, seconds)}")
    print(f" (Based on average walking speed: 80 m/min or 4.8 km/h)")
    print("="*50)

def find_all_paths_interface(graph):
    """Find and display all possible paths"""
    buildings = list_buildings(graph)
    if len(buildings) < 2:
        print("\n⚠ Need at least 2 buildings to find paths.")
        return
    
    print("\n🔄 FIND ALL POSSIBLE PATHS")
    print("-" * 30)
    
    start = input("Enter start building: ").strip().title()
    end = input("Enter destination: ").strip().title()
    
    if start not in graph.graph or end not in graph.graph:
        print("✗ Invalid building name!")
        return
    
    all_paths = find_all_paths(graph.graph, start, end, max_depth=10)
    
    if not all_paths:
        print(f"\n✗ No paths found from '{start}' to '{end}'!")
        return
    
    print(f"\n✅ Found {len(all_paths)} path(s):")
    print("="*50)
    
    for i, path in enumerate(all_paths, 1):
        total_dist = calculate_path_distance(graph.graph, path)
        minutes, seconds = calculate_time(total_dist)
        
        print(f"{i}. {' → '.join(path)}")
        print(f"   📏 Distance: {total_dist} meters")
        print(f"   ⏱ Time: {format_time(minutes, seconds)}")
        print()
    print("="*50)

def check_connections_interface(graph):
    """Show detailed connections for a building"""
    buildings = list_buildings(graph)
    if not buildings:
        return
    
    print("\n🔍 CHECK BUILDING CONNECTIONS")
    building = input("Enter building name: ").strip().title()
    
    if building not in graph.graph:
        print(f"✗ Building '{building}' not found!")
        return
    
    connections = graph.get_building_connections(building)
    
    if not connections:
        print(f"\n📍 {building} has no connections yet.")
        return
    
    print(f"\n📍 CONNECTIONS FROM {building}:")
    print("-" * 40)
    for neighbor, dist in sorted(connections, key=lambda x: x[1]):
        minutes, seconds = calculate_time(dist)
        print(f"   → {neighbor:<15} ({dist} meters, ~{format_time(minutes, seconds)} walk)")
    print("-" * 40)

def main():
    """Main program loop"""
    g = Graph()
    load_graph(g)
    
    while True:
        display_menu()
        choice = input("\n👉 Enter your choice: ").strip()
        
        if choice == '1':
            name = input("Enter building name: ").strip()
            if name:
                g.add_building(name)
            else:
                print("✗ Building name cannot be empty!")
        
        elif choice == '2':
            buildings = list_buildings(g)
            if buildings:
                name = input("Enter building name to remove: ").strip()
                if name:
                    g.remove_building(name)
        
        elif choice == '3':
            buildings = list_buildings(g)
            if len(buildings) < 2:
                print("\n⚠ Need at least 2 buildings to add a path.")
                continue
            
            print("\n🛤 ADD NEW PATH")
            src = input("Source building: ").strip().title()
            dest = input("Destination building: ").strip().title()
            
            try:
                distance = int(input("Distance (meters): ").strip())
                if distance <= 0:
                    print("✗ Distance must be positive!")
                    continue
                g.add_path(src, dest, distance)
            except ValueError:
                print("✗ Invalid distance! Please enter a number.")
        
        elif choice == '4':
            src = input("Source building: ").strip().title()
            dest = input("Destination building: ").strip().title()
            g.remove_path(src, dest)
        
        elif choice == '5':
            g.display()
        
        elif choice == '6':
            find_shortest_path_interface(g)
        
        elif choice == '7':
            find_all_paths_interface(g)
        
        elif choice == '8':
            list_buildings(g)
        
        elif choice == '9':
            check_connections_interface(g)
        
        elif choice == '10':
            if save_graph(g.graph):
                print("\n👋 Thank you for using Campus Navigator!")
                break
            else:
                confirm = input("\nSave failed. Exit anyway? (y/n): ").lower()
                if confirm == 'y':
                    break
        
        else:
            print("\n✗ Invalid choice! Please enter 1-10.")

if __name__ == "__main__":
    main()