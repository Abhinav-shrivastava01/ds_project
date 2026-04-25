def save_graph(graph, filename="data.txt"):
    with open(filename, "w") as f:
        for node in graph:
            for neighbor, weight in graph[node]:
                f.write(f"{node},{neighbor},{weight}\n")


def load_graph(graph_obj, filename="data.txt"):
    try:
        with open(filename, "r") as f:
            for line in f:
                src, dest, weight = line.strip().split(",")

                if src not in graph_obj.graph:
                    graph_obj.add_building(src)
                if dest not in graph_obj.graph:
                    graph_obj.add_building(dest)

                if (dest, int(weight)) not in graph_obj.graph[src]:
                    graph_obj.add_path(src, dest, int(weight))
    except FileNotFoundError:
        print("No saved data found.")