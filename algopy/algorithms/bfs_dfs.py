from collections import deque
from typing import Generator, Optional
import networkx as nx

from algopy.utilities import Edge, Snapshot


def dfs(graph: nx.Graph, start: int) -> Generator[Snapshot, None, None]:
    """
    Iterative DFS that yields a snapshot after each new node visit.
    """
    
    visited: set[int] = set()
    tree_edges: list[Edge] = []
    stack: list[tuple[int, Optional[int]]] = [(start, None)]

    while stack:
        node, parent = stack.pop()
        if node in visited:
            continue
        visited.add(node)

        if parent is not None:
            tree_edges.append((parent, node))

        yield set(visited), list(tree_edges)

        for neighbor in sorted(graph.neighbors(node), reverse=True):
            if neighbor not in visited:
                stack.append((neighbor, node))


def bfs(graph: nx.Graph, start: int) -> Generator[Snapshot, None, None]:
    """
    Iterative BFS that yields a snapshot after each new node visit.
    """
    
    visited: set[int] = set()
    tree_edges: list[Edge] = []
    fifo: deque[tuple[int, Optional[int]]] = deque()
    fifo.append((start, None))

    while fifo:
        node, parent = fifo.popleft()
        if node in visited:
            continue
        visited.add(node)

        if parent is not None:
            tree_edges.append((parent, node))

        yield set(visited), list(tree_edges)

        for neighbor in sorted(graph.neighbors(node), reverse=True):
            if neighbor not in visited:
                fifo.append((neighbor, node))

