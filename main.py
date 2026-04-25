from graph import Graph
from dijkstra import dijkstra, get_path
from utils import save_graph, load_graph

def menu():
    print("\n===== Campus Navigator =====")
    print("1. Add Building")
    print("2. Add Path")
    print("3. Display Map")
    print("4. Find Shortest Path")
    print("5. Save & Exit")


def main():
    g = Graph()
    load_graph(g)

    while True:
        menu()
        choice = input("Enter choice: ")

        if choice == '1':
            name = input("Enter building name: ")
            g.add_building(name)

        elif choice == '2':
            src = input("Source building: ")
            dest = input("Destination building: ")
            distance = int(input("Distance: "))
            g.add_path(src, dest, distance)

        elif choice == '3':
            g.display()

        elif choice == '4':
            start = input("Start: ")
            end = input("End: ")

            if start not in g.graph or end not in g.graph:
                print("Invalid buildings.")
                continue

            distances, parent = dijkstra(g.graph, start)
            path = get_path(parent, end)

            print("\nShortest Path:")
            print(" -> ".join(path))
            print(f"Total Distance: {distances[end]}")

        elif choice == '5':
            save_graph(g.graph)
            print("Data saved. Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()