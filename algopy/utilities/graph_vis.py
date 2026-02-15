import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from collections import deque

# Type aliases used across notebooks and algorithms.
Edge = tuple[int, int]
Snapshot = tuple[set[int], list[Edge]]


class GraphVis:
    """Reusable graph-drawing helper for algorithm walkthrough notebooks."""

    def __init__(self) -> None:
        self.pos: dict[int, tuple[float, float]] | None = None

    def display(self, graph: nx.Graph, title: str = "Graph") -> None:
        """Draw the graph with a spring layout and store positions for later use."""
        self.pos = nx.spring_layout(graph, seed=42)

        plt.figure(figsize=(7, 5))
        nx.draw(
            graph,
            self.pos,
            with_labels=True,
            node_color="lightgray",
            node_size=500,
            font_size=12,
            edge_color="gray",
            width=1.5,
        )
        plt.title(title)
        plt.show()

    def show_progress(
        self,
        graph: nx.Graph,
        snapshots: list[Snapshot],
        title_prefix: str = "Step",
    ) -> None:
        """Draw one figure per snapshot showing visited/unvisited nodes and tree edges."""
        total = len(snapshots)
        for idx, (visited, tree_edges) in enumerate(snapshots):
            plt.figure(figsize=(7, 5))

            node_colors = [
                "orange" if n in visited else "lightblue" for n in graph.nodes()
            ]

            nx.draw_networkx_edges(graph, self.pos, edge_color="lightgray", width=1.0)

            if tree_edges:
                nx.draw_networkx_edges(
                    graph,
                    self.pos,
                    edgelist=tree_edges,
                    edge_color="darkblue",
                    width=2.5,
                )

            nx.draw_networkx_nodes(
                graph, self.pos, node_color=node_colors, node_size=500
            )
            nx.draw_networkx_labels(graph, self.pos, font_size=12)

            legend_elements = [
                Line2D(
                    [0], [0],
                    marker="o",
                    color="w",
                    markerfacecolor="orange",
                    markersize=12,
                    label="Visited",
                ),
                Line2D(
                    [0], [0],
                    marker="o",
                    color="w",
                    markerfacecolor="lightblue",
                    markersize=12,
                    label="Unvisited",
                ),
                Line2D(
                    [0], [0], color="darkblue", linewidth=2.5, label="Tree edge"
                ),
            ]
            plt.legend(handles=legend_elements, loc="upper left")
            label = f"{title_prefix} {idx + 1}/{total}  --  visited {sorted(visited)}"
            plt.title(label)
            plt.show()

    def show_tree(
        self,
        graph: nx.Graph,
        tree_edges: list[Edge],
        root: int,
        title: str = "Search Tree",
    ) -> None:
        """Build a tree subgraph and draw it with a hierarchical layout."""
        T = nx.Graph()
        T.add_nodes_from(graph.nodes())
        T.add_edges_from(tree_edges)

        tree_pos = _hierarchy_pos(T, root)

        plt.figure(figsize=(8, 6))
        nx.draw(
            T,
            tree_pos,
            with_labels=True,
            node_color="orange",
            node_size=500,
            font_size=12,
            edge_color="darkblue",
            width=2.5,
        )
        plt.title(title)
        plt.show()


def _hierarchy_pos(
    tree: nx.Graph, root: int
) -> dict[int, tuple[float, float]]:
    """Position nodes in a top-down tree layout using BFS layers."""
    levels: dict[int, int] = {root: 0}
    queue: deque[int] = deque([root])
    children: dict[int, list[int]] = {root: []}

    while queue:
        node = queue.popleft()
        for nbr in tree.neighbors(node):
            if nbr not in levels:
                levels[nbr] = levels[node] + 1
                children.setdefault(node, []).append(nbr)
                children.setdefault(nbr, [])
                queue.append(nbr)

    max_depth = max(levels.values())
    pos: dict[int, tuple[float, float]] = {}

    def _assign_x(node: int, left: float, right: float) -> None:
        kids = children[node]
        if not kids:
            pos[node] = ((left + right) / 2, -levels[node])
            return
        width = (right - left) / len(kids)
        for i, child in enumerate(kids):
            _assign_x(child, left + i * width, left + (i + 1) * width)
        xs = [pos[c][0] for c in kids]
        pos[node] = (sum(xs) / len(xs), -levels[node])

    _assign_x(root, 0, max(max_depth, 1) * 3)
    return pos


def draw_heap(graph: nx.DiGraph, title: str = "Heap") -> None:
    """Draw a heap exported via Heap.to_networkx() as a top-down tree.

    Nodes are labelled with their stored values. The layout mirrors the
    implicit binary-tree structure of the underlying array.
    """
    if graph.number_of_nodes() == 0:
        plt.figure(figsize=(7, 5))
        plt.text(
            0.5, 0.5, "(empty heap)",
            ha="center", va="center", fontsize=14, color="gray",
        )
        plt.title(title)
        plt.axis("off")
        plt.show()
        return

    # _hierarchy_pos works on undirected graphs, so convert temporarily
    undirected = graph.to_undirected()
    pos = _hierarchy_pos(undirected, root=0)

    labels = nx.get_node_attributes(graph, "label")

    plt.figure(figsize=(7, 5))
    nx.draw(
        graph,
        pos,
        labels=labels,
        with_labels=True,
        node_color="lightyellow",
        edgecolors="black",
        node_size=600,
        font_size=13,
        font_weight="bold",
        edge_color="gray",
        width=1.5,
        arrows=False,
    )
    plt.title(title)
    plt.show()
