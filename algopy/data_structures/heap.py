# pylint: disable=trailing-whitespace
# pylint: disable=missing-function-docstring
# pylint: disable=unused-argument

import networkx as nx

class Heap:
    """Basic heap superclass"""
    
    def __init__(self):
        self.elements = []
        
    def size(self) -> int:
        return len(self.elements)
        
    def peek(self):
        if self.elements:
            return self.elements[0]

    def pop(self):

        if len(self.elements) < 1:
            return None

        # Copy the element to return
        el = self.elements[0]

        # Specify case, single element empties the collection
        if len(self.elements) == 1:
            self.elements = []
            return el

        # Swap the last index with the root
        self.elements[0] = self.elements.pop()
        self._heapify_down(0)
        return el

    def change_key(self, index: int, new_val: int):
        """ Override """
        return

    def insert(self, item, value: int):
        """ Override """
        return
    
    def _heapify_up(self, index: int):
        """ Override """
        return
    
    def _heapify_down(self, index: int):
        """ Override """
        return
    
    def _get_parent_index(self, index: int) -> int:
        if not self.elements:
            return None
        
        # No parent at root node
        if index == 0:
            return None
        
        return (index - 1) // 2
        
    def _get_left_index(self, index: int) -> int:
        if not self.elements:
            return
        
        l = 2 * index + 1
        if l >= len(self.elements):
            return None
        
        return l
    
    def _get_right_index(self, index: int) -> int:
        if not self.elements:
            return
        
        r = 2 * index + 2
        if r >= len(self.elements):
            return None

        return r

    def to_networkx(self) -> nx.DiGraph:
        """Export the current heap state as a directed NetworkX graph.

        Each node stores its array index as the node id and its value as
        the 'label' attribute.  Edges point from parent to child.
        """
        G = nx.DiGraph()
        for i, el in enumerate(self.elements):
            G.add_node(i, label=str(el["value"]))
        for i in range(len(self.elements)):
            left = self._get_left_index(i)
            right = self._get_right_index(i)
            if left is not None:
                G.add_edge(i, left)
            if right is not None:
                G.add_edge(i, right)
        return G

class MaxHeap(Heap):
    """Max Heap"""

    def change_key(self, index: int, new_val: int):
        """ Override """

        if (not self.elements or index >= len(self.elements)):
            return None

        current_val = self.elements[index]["value"]
        self.elements[index]["value"] = new_val

        # We will have to swap upwards
        if new_val > current_val:
            return self._heapify_up(index)
        else:
            return self._heapify_down(index)

    def insert(self, item, value: int):
        """ Add new element and heapify up """

        self.elements.append({"item": item, "value": value})
        self._heapify_up(len(self.elements) -1)

    def _heapify_up(self, index: int):
        """ Swap keys upwards until heap property is set """

        parent_index = self._get_parent_index(index)

        if parent_index is None:
            # already at the top! nowhere to go
            return

        if self.elements[parent_index]["value"] >= self.elements[index]["value"]:
            # base case, this is what we want
            return

        # Swap with parent if needed
        if self.elements[parent_index]["value"] < self.elements[index]["value"]:

            self.elements[parent_index], self.elements[index] = \
            self.elements[index], self.elements[parent_index]

            # recursively handle the parent, which may require more heap-up ops
            return self._heapify_up(parent_index)

    def _heapify_down(self, index: int):
        """ Swap keys downwards until heap property is set """

        if not self._get_left_index(index) and not self._get_right_index(index):
            # no children left, we are at the leaf nodes
            return

        # We checked for the absence of *both* children, but it's possible there is one child
        left_index = self._get_left_index(index)
        right_index = self._get_right_index(index)

        largest = index
        if left_index and self.elements[left_index]["value"] > self.elements[largest]["value"]:
            largest = left_index
        if right_index and self.elements[right_index]["value"] > self.elements[largest]["value"]:
            largest = right_index

        if largest != index:
            self.elements[index], self.elements[largest] = self.elements[largest], self.elements[index]
            return self._heapify_down(largest)
      
                
class MinHeap(Heap):
    """Min Heap"""

    def change_key(self, index: int, new_val: int):

        if (not self.elements or index >= len(self.elements)):
            return None

        current_val = self.elements[index]["value"]
        self.elements[index]["value"] = new_val

        # We will have to swap upwards
        if new_val < current_val:
            return self._heapify_up(index)
        else:
            return self._heapify_down(index)

    def insert(self, item, value: int):
        """ Add new element and heapify up """

        self.elements.append({"item": item, "value": value})
        self._heapify_up(len(self.elements) -1)

    def _heapify_up(self, index: int):
        """ Swap keys upwards until heap property is set """

        parent_index = self._get_parent_index(index)

        if parent_index is None:
            # already at the top! nowhere to go
            return

        if self.elements[parent_index]["value"] <= self.elements[index]["value"]:
            # base case, this is what we want
            return

        # Swap with parent if needed
        if self.elements[parent_index]["value"] > self.elements[index]["value"]:

            self.elements[parent_index], self.elements[index] = \
            self.elements[index], self.elements[parent_index]

            # recursively handle the parent, which may require more heap-up ops
            return self._heapify_up(parent_index)

    def _heapify_down(self, index: int):
        """ Swap keys downwards until heap property is set """

        if not self._get_left_index(index) and not self._get_right_index(index):
            # no children left, we are at the leaf nodes
            return

        # We checked for the absence of *both* children, but it's possible there is one child
        left_index = self._get_left_index(index)
        right_index = self._get_right_index(index)

        smallest = index
        if left_index and self.elements[left_index]["value"] < self.elements[smallest]["value"]:
            smallest = left_index
        if right_index and self.elements[right_index]["value"] < self.elements[smallest]["value"]:
            smallest = right_index

        if smallest != index:
            self.elements[index], self.elements[smallest] = self.elements[smallest], self.elements[index]
            return self._heapify_down(smallest)
                
        
