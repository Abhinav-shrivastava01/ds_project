# 🏫 Campus Navigator System

A graph-based navigation system that finds the shortest path between buildings on a university campus using **Dijkstra's algorithm**. The system calculates both distance (in meters) and estimated walking time based on average human walking speed.

## 📋 Table of Contents
- [Features](#features)
- [Data Structures Used](#data-structures-used)
- [Algorithm Used](#algorithm-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Sample Data](#sample-data)
- [Time Complexity](#time-complexity)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Author](#author)

## ✨ Features

- ✅ **Add Buildings** - Add new buildings to the campus map
- ✅ **Remove Buildings** - Remove buildings and all associated paths
- ✅ **Add Paths** - Create bidirectional paths between buildings with distances
- ✅ **Remove Paths** - Delete existing paths
- ✅ **Display Map** - View entire campus layout with all connections
- ✅ **Find Shortest Path** - Get optimal route between any two buildings
- ✅ **Find All Paths** - Discover all possible routes (DFS exploration)
- ✅ **Check Connections** - View direct connections from any building
- ✅ **Walking Time Estimation** - Automatic time calculation (80 m/min average speed)
- ✅ **Persistent Storage** - Save/load data from file

## 🗂️ Data Structures Used

| Data Structure | Purpose | Location |
|----------------|---------|----------|
| **Graph (Adjacency List)** | Models campus layout (nodes = buildings, edges = paths) | `graph.py` |
| **Dictionary / Hash Map** | O(1) lookups for distances, parents, and graph storage | `dijkstra.py`, `graph.py` |
| **Min-Heap (Priority Queue)** | Efficient vertex extraction in Dijkstra's algorithm | `dijkstra.py` |
| **List** | Stores neighbors, path reconstruction | `graph.py`, `dijkstra.py` |
| **Tuple** | Immutable (neighbor, distance) pairs | `graph.py` |
| **Set** | Avoids duplicate edges during save | `utils.py` |

## 🧮 Algorithm Used

### Dijkstra's Algorithm (Shortest Path)
- **Type:** Greedy Algorithm
- **Time Complexity:** O(E log V) with Min-Heap
- **Space Complexity:** O(V + E)

**Why Dijkstra?**
- Handles weighted graphs (realistic distances in meters)
- Guarantees shortest path when weights are positive
- Efficient for sparse campus maps

### DFS (All Paths Finding)
- **Type:** Backtracking / Recursive DFS
- **Time Complexity:** O(V!) in worst case (bounded by max_depth)
- **Space Complexity:** O(V)

