import streamlit as st
import networkx as nx
import plotly.graph_objects as go

from graph import Graph
from dijkstra import (
    get_path_details,
    find_all_paths,
    calculate_path_distance,
    calculate_time,
    format_time,
)
from utils import load_graph, save_graph

st.set_page_config(page_title="Campus Navigator Pro", layout="wide")

# ---------------- INIT ----------------
if "graph" not in st.session_state:
    g = Graph()
    load_graph(g)
    st.session_state.graph = g

g = st.session_state.graph

# ---------------- HEADER ----------------
st.title("🏫 Campus Navigator Pro")
st.markdown("### 🚀 Smart Navigation • Interactive Map • Analytics")

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "🏢 Buildings",
        "🛤 Paths",
        "🚀 Shortest Path",
        "🔄 All Paths",
        "🗺 Interactive Map",
    ],
)

# ---------------- DASHBOARD ----------------
if menu == "📊 Dashboard":
    st.subheader("📊 System Overview")

    total_buildings = len(g.graph)
    total_paths = sum(len(v) for v in g.graph.values()) // 2

    col1, col2 = st.columns(2)
    col1.metric("🏢 Buildings", total_buildings)
    col2.metric("🛤 Paths", total_paths)

    st.divider()

    # Most connected building
    if g.graph:
        most_connected = max(g.graph, key=lambda x: len(g.graph[x]))
        st.success(f"🏆 Most Connected Building: **{most_connected}**")

    st.subheader("📍 Buildings")
    st.write(list(g.graph.keys()))

# ---------------- BUILDINGS ----------------
elif menu == "🏢 Buildings":
    st.subheader("Manage Buildings")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Add Building")
        if st.button("Add Building"):
            if name:
                g.add_building(name.title())
                st.success("Added!")

    with col2:
        if g.graph:
            remove = st.selectbox("Remove Building", list(g.graph.keys()))
            if st.button("Remove Building"):
                g.remove_building(remove)
                st.warning("Removed")

# ---------------- PATHS ----------------
elif menu == "🛤 Paths":
    st.subheader("Manage Paths")

    buildings = list(g.graph.keys())

    if len(buildings) < 2:
        st.warning("Need at least 2 buildings")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Add Path")
            b1 = st.selectbox("Source", buildings)
            b2 = st.selectbox("Destination", buildings)
            dist = st.number_input("Distance", min_value=1)

            if st.button("Add Path"):
                g.add_path(b1, b2, int(dist))
                st.success("Path added!")

        with col2:
            st.markdown("### Remove Path")
            r1 = st.selectbox("From", buildings, key="r1")
            r2 = st.selectbox("To", buildings, key="r2")

            if st.button("Remove Path"):
                g.remove_path(r1, r2)
                st.warning("Removed")

# ---------------- SHORTEST PATH ----------------
elif menu == "🚀 Shortest Path":
    st.subheader("Find Shortest Path")

    buildings = list(g.graph.keys())

    if len(buildings) < 2:
        st.warning("Not enough buildings")
    else:
        start = st.selectbox("Start", buildings)
        end = st.selectbox("End", buildings)

        if st.button("Find"):
            path, dist, m, s = get_path_details(g.graph, start, end)

            if path:
                st.success(" → ".join(path))

                c1, c2 = st.columns(2)
                c1.metric("Distance", f"{dist} m")
                c2.metric("Time", format_time(m, s))

                st.session_state.highlight_path = path
            else:
                st.error("No path found")

# ---------------- ALL PATHS ----------------
elif menu == "🔄 All Paths":
    st.subheader("All Paths")

    buildings = list(g.graph.keys())

    if len(buildings) < 2:
        st.warning("Not enough buildings")
    else:
        start = st.selectbox("Start", buildings, key="a1")
        end = st.selectbox("End", buildings, key="a2")

        if st.button("Find All"):
            paths = find_all_paths(g.graph, start, end)

            if paths:
                st.success(f"{len(paths)} paths found")

                for p in paths:
                    d = calculate_path_distance(g.graph, p)
                    m, s = calculate_time(d)

                    st.info(f"{' → '.join(p)} | {d}m | {format_time(m, s)}")
            else:
                st.error("No paths")

# ---------------- INTERACTIVE GRAPH ----------------
elif menu == "🗺 Interactive Map":
    st.subheader("Interactive Campus Map")

    if not g.graph:
        st.warning("No data available")
    else:
        G = nx.Graph()

        for node in g.graph:
            for neighbor, dist in g.graph[node]:
                G.add_edge(node, neighbor, weight=dist)

        pos = nx.spring_layout(G)

        edge_x = []
        edge_y = []

        highlight = st.session_state.get("highlight_path", [])

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]

            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=2),
            hoverinfo="none",
            mode="lines",
        )

        node_x = []
        node_y = []
        text = []

        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            text.append(node)

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=text,
            textposition="top center",
            marker=dict(size=20),
        )

        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(showlegend=False)

        st.plotly_chart(fig, use_container_width=True)

# ---------------- SAVE ----------------
st.sidebar.divider()
if st.sidebar.button("💾 Save Data"):
    save_graph(g.graph)
    st.sidebar.success("Saved!")