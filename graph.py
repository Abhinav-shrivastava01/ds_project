class Graph:
    def __init__(self):  # FIXED: Correct init method name
        self.graph = {}
    
    def add_building(self, name):
        """Add a building to the campus"""
        name = name.strip().title()  # Clean input
        if not name:
            print("Building name cannot be empty.")
            return False
            
        if name not in self.graph:
            self.graph[name] = []
            print(f"✓ {name} added successfully.")
            return True
        else:
            print(f"✗ {name} already exists.")
            return False
    
    def remove_building(self, name):
        """Remove a building and all its connections"""
        name = name.strip().title()
        
        if name not in self.graph:
            print(f"✗ {name} does not exist.")
            return False
        
        # Remove all paths to this building from other buildings
        for building in self.graph:
            self.graph[building] = [edge for edge in self.graph[building] if edge[0] != name]
        
        # Remove the building itself
        del self.graph[name]
        print(f"✓ {name} and all its paths removed successfully.")
        return True
    
    def add_path(self, src, dest, distance):
        """Add a bidirectional path between two buildings"""
        src = src.strip().title()
        dest = dest.strip().title()
        
        # Validation 1: Check if buildings exist
        if src not in self.graph:
            print(f"✗ Building '{src}' does not exist.")
            return False
        if dest not in self.graph:
            print(f"✗ Building '{dest}' does not exist.")
            return False
        
        # Validation 2: Check for self-loop
        if src == dest:
            print("✗ Cannot connect a building to itself.")
            return False
        
        # Validation 3: Check for negative distance
        if distance <= 0:
            print("✗ Distance must be positive.")
            return False
        
        # Validation 4: Check if path already exists
        for neighbor, dist in self.graph[src]:
            if neighbor == dest:
                print(f"✗ Path between {src} and {dest} already exists (distance: {dist}).")
                return False
        
        # Add the path (bidirectional)
        self.graph[src].append((dest, distance))
        self.graph[dest].append((src, distance))
        print(f"✓ Path added between {src} and {dest} (distance: {distance}).")
        return True
    
    def remove_path(self, src, dest):
        """Remove a path between two buildings"""
        src = src.strip().title()
        dest = dest.strip().title()
        
        if src not in self.graph or dest not in self.graph:
            print("✗ One or both buildings don't exist.")
            return False
        
        # Check if path exists
        path_exists = False
        original_len = len(self.graph[src])
        
        # Remove from src to dest
        self.graph[src] = [edge for edge in self.graph[src] if edge[0] != dest]
        # Remove from dest to src
        self.graph[dest] = [edge for edge in self.graph[dest] if edge[0] != src]
        
        if len(self.graph[src]) < original_len:
            print(f"✓ Path between {src} and {dest} removed.")
            return True
        else:
            print(f"✗ No path exists between {src} and {dest}.")
            return False
    
    def get_all_buildings(self):
        """Return sorted list of all buildings"""
        return sorted(self.graph.keys())
    
    def display(self):
        """Display the campus map"""
        if not self.graph:
            print("\n⚠ No buildings in the campus yet.")
            return
        
        print("\n" + "="*50)
        print("CAMPUS MAP")
        print("="*50)
        for node in sorted(self.graph.keys()):
            if self.graph[node]:
                connections = []
                for neighbor, dist in self.graph[node]:
                    connections.append(f"{neighbor}({dist}m)")
                print(f"📍 {node:15} → {', '.join(connections)}")
            else:
                print(f"📍 {node:15} → (No connections)")
        print("="*50)
    
    def get_building_connections(self, building):
        """Get all connections from a specific building"""
        building = building.strip().title()
        if building in self.graph:
            return self.graph[building].copy()
        return []