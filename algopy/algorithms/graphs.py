from typing import Generator, Any
import json

import networkx as nx
from algopy.data_structures import MinHeap

# tuple (explored nodes, unexplored nodes, edges, cost dictionary)
DijkstraSnapshot = tuple[list[Any], list[Any], list[tuple[int, int, float]], dict[Any]]

def dijkstra(graph: nx.Graph, start: Any) -> Generator[DijkstraSnapshot, None, None]:
    """
    Docstring for dijkstra
    
    :param graph: Description
    :type graph: nx.Graph
    :param start: Description
    :type start: int
    :return: Description
    :rtype: Generator[DijkstraSnapshot, None, None]
    """
    
    # Precondition checks
    if start not in graph.nodes:
        print(f"Cannot use dijkstra: start node {start} is not a node in the input graph")
        return None

    dist = {}
    prev = {}
    Q = MinHeap()

    # Initialization
    dist[start] = 0
    prev[start] = None
    Q.insert(start, 0)

    for v in graph.nodes:
        if v != start:
            prev[v] = None
            dist[v] = float('inf')
            Q.insert(v, float('inf'))

    graph_edges = [(u, v, d['weight']) for (u, v, d) in graph.edges(data=True)]
    explored = set()
    yield (_snapshot(dist, prev, explored, graph_edges))

    # The main loop
    while Q.size() > 0:
        el = Q.pop()
        u = el.get("item")

        explored.add(u)

        for v in graph.neighbors(u):
            alt = dist[u] + graph[u][v]['weight']
            if alt < dist[v]:
                prev[v] = u
                dist[v] = round(alt, 3)
                Q.decrease_priority(v, dist[v])

        yield (_snapshot(dist, prev, explored, graph_edges))


def _snapshot(dist, prev, explored, graph_edges):
    """Build a DijkstraSnapshot tuple from current algorithm state."""
    all_nodes = list(dist.keys())
    S = sorted(n for n in all_nodes if n in explored)
    V_S = sorted(n for n in all_nodes if n not in explored)
    A = {}
    for node in all_nodes:
        cost = dist[node]
        A[node] = {"node": node, "cost": cost, "parent": prev[node]}
    return (S, V_S, graph_edges, A)
    

if __name__ == '__main__':

    G = nx.Graph()

    G.add_edge("a", "b", weight=0.6)
    G.add_edge("a", "c", weight=0.2)
    G.add_edge("c", "d", weight=0.1)
    G.add_edge("c", "e", weight=0.7)
    G.add_edge("c", "f", weight=0.1)
    G.add_edge("a", "d", weight=0.3)
    G.add_edge("a", "f", weight=0.2)

    title = "----------- Input Graph -----------"
    print(title)
    print(list(G.nodes))
    print(list(G.edges(data=True)))
    print("-" * len(title), "\n")
    
    snapshots = list(dijkstra(G, 'a'))
    
    for i, snap in enumerate(snapshots):
        V, V_S, graph_edges, A = snap
        
        print(f"\n--------------------  Dijkstra Iteration {i} --------------------")
        print(f"V: {V}")
        print(f"V_S: {V_S}")
        print(f"{json.dumps(A, indent=4)}")
        print("-----------------------------------------------------------------\n")
