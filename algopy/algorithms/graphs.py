from typing import Generator, Any
import copy
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
    if start not in list(graph.nodes):
        print(f"Cannot use dijkstra: start node {start} is not a node in the input graph")
        return None
    
    # Dictionary for node, cost, and path tracking
    new_item = {"node": None, "cost": float('inf'), "parent": None}
    A = {}  # key=node, value=new_item
    
    # Process original dictionary
    for node in graph.nodes:
        item = copy.deepcopy(new_item)
        item["node"] = node
        A[node] = item
    
    A[start]['cost'] = 0

    # Min heap to process incoming edges
    pq = MinHeap()  # takes (item: tuple(u, v), value: w int)
    
    # Let set S be the explored nodes
    # Let set V_S be the unexplored nodes
    S = set([start])
    V_S = set(node for node in graph.nodes if node != start)

    graph_edges = [(u, v, d['weight']) for (u, v, d) in graph.edges(data=True)]
    yield (sorted(S), sorted(V_S), graph_edges, copy.deepcopy(A))

    # Seed the heap with edges from the start node
    for neighbor in graph.neighbors(start):
        w = graph[start][neighbor]['weight']
        pq.insert(item=(start, neighbor), value=A[start]['cost'] + w)

    while len(V_S) > 0:

        # Pop the lowest cost edge, skipping stale entries
        el = pq.pop()
        u, v = el.get("item")
        w = el.get("value")

        # Orient the edge so new_node is the unexplored end
        if u in S and v in S:
            continue  # Both already explored, stale entry
        new_node = v if v not in S else u
        parent = u if new_node == v else v

        # Update cost list A
        A[new_node]['parent'] = parent
        A[new_node]['cost'] = round(w, 3)

        # Move new_node from V_S to S
        V_S.discard(new_node)
        S.add(new_node)

        # Add edges from the newly explored node to the heap
        for neighbor in graph.neighbors(new_node):
            if neighbor not in S:
                edge_w = graph[new_node][neighbor]['weight']
                pq.insert(item=(new_node, neighbor), value=A[new_node]['cost'] + edge_w)

        yield (sorted(S), sorted(V_S), graph_edges, copy.deepcopy(A))
    

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
