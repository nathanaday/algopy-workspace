from collections import deque
from typing import Generator, Optional
import networkx as nx

from algopy.utilities import Edge, Snapshot
from algopy.data_structures import MinHeap


def dijkstra(graph: nx.Graph, start: int) -> Generator[Snapshot, None, None]:
    
    # Dictionary for node, cost, and path tracking
    new_item = {"node": None, "cost": float('inf'), "parent": None}
    A = {}  # Dictoinary of new_item types
    
    # Min heap to process incoming edges
    
    