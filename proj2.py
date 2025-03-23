"""CSC111 Project 2 | Laptop Recommendation System"""

from __future__ import annotations

import csv
from typing import Any, Optional

from python_ta.contracts import check_contracts


class _Vertex:
    """A vertex in a laptop recommendation graph, used to represent the laptop's specs, including 'name', 'price',
    'processor', 'ram', 'os', 'storage', 'display (inches)', 'rating' represented by strings.

    Instance Attributes:
        - item: The data stored in this vertex.
        - kind: The type of this vertex, one of: 'name', 'price', 'processor', 'ram', 'os',
        'storage', 'display size', 'rating'
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'name', 'price', 'processor', 'ram', 'os',
        'storage', 'display size', 'rating'}
    """
    item: Any
    kind: str
    neighbours: set[_Vertex]

    def __init__(self, item: Any, name: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'book'}
        """
        self.item = item
        self.name = name
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    ############################################################################
    # Part 2, Q2a
    ############################################################################
    def similarity_score(self, other: _Vertex) -> float:
        """Return the similarity score between this vertex and other.
        If this vertex has the same item as another vertex, and they are both of the same kind,
        """

        if len(self.neighbours) == 0 or len(other.neighbours) == 0:
            return 0

        numerator = len(self.neighbours.intersection(other.neighbours))
        denominator = len(self.neighbours.union(other.neighbours))

        return numerator / denominator


class Graph:
    """A graph used to represent a book review network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, type: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'user', 'book'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, type)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False
