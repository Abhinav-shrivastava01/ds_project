class Graph:
    def __init__(self):
        self.graph = {}

    def add_building(self, name):
        if name not in self.graph:
            self.graph[name] = []
            print(f"{name} added successfully.")
        else:
            print("Building already exists.")

    def add_path(self, src, dest, distance):
        if src not in self.graph or dest not in self.graph:
            print("One or both buildings do not exist.")
            return

        self.graph[src].append((dest, distance))
        self.graph[dest].append((src, distance))
        print(f"Path added between {src} and {dest} with distance {distance}.")

    def display(self):
        print("\nCampus Map:")
        for node in self.graph:
            print(f"{node} -> {self.graph[node]}")