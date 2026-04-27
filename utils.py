def save_graph(graph, filename="data.txt"):
    """Save graph to file without duplicates"""
    if not graph:
        print("⚠ Nothing to save. Graph is empty.")
        return False
    
    edges = set()  # Use set to avoid duplicate edges
    
    for node in graph:
        for neighbor, weight in graph[node]:
            # Store edge in normalized form (alphabetical order)
            edge = tuple(sorted([node, neighbor]) + [weight])
            edges.add(edge)
    
    try:
        with open(filename, "w") as f:
            # Write header comment
            f.write("# Campus Navigator Data File\n")
            f.write("# Format: Source,Destination,Distance(meters)\n")
            f.write("# " + "="*50 + "\n\n")
            
            for node1, node2, weight in sorted(edges):
                f.write(f"{node1},{node2},{weight}\n")
        
        print(f"✓ Saved {len(edges)} paths to {filename}")
        return True
    except Exception as e:
        print(f"✗ Error saving: {e}")
        return False


def load_graph(graph_obj, filename="data.txt"):
    """Load graph from file with comment skipping"""
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
            
        if not lines:
            print("ℹ No data found. Starting with empty campus.")
            return False
        
        edges_loaded = 0
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
                
            try:
                parts = line.split(",")
                if len(parts) != 3:
                    print(f"⚠ Line {line_num}: Invalid format (skipped)")
                    continue
                
                src, dest, weight_str = parts
                src = src.strip()
                dest = dest.strip()
                weight = int(weight_str.strip())
                
                if weight <= 0:
                    print(f"⚠ Line {line_num}: Invalid weight {weight} (skipped)")
                    continue
                
                # Add buildings if they don't exist
                if src not in graph_obj.graph:
                    graph_obj.add_building(src)
                if dest not in graph_obj.graph:
                    graph_obj.add_building(dest)
                
                # Add path (checking for duplicates)
                if src in graph_obj.graph and dest in graph_obj.graph:
                    path_exists = False
                    for neighbor, _ in graph_obj.graph[src]:
                        if neighbor == dest:
                            path_exists = True
                            break
                    
                    if not path_exists:
                        graph_obj.graph[src].append((dest, weight))
                        graph_obj.graph[dest].append((src, weight))
                        edges_loaded += 1
                        
            except ValueError:
                print(f"⚠ Line {line_num}: Invalid number format (skipped)")
            except Exception as e:
                print(f"⚠ Line {line_num}: Error - {e} (skipped)")
        
        print(f"✓ Loaded {edges_loaded} paths from {filename}")
        return True
        
    except FileNotFoundError:
        print("ℹ No saved data found. Starting with empty campus.")
        return False