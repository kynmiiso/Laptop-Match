"""CSC111 Project 2 | Laptop Recommendation System"""

from __future__ import annotations

from typing import Any, Optional
from python_ta.contracts import check_contracts
from dataclasses import dataclass
import pandas as pd

from user_input_form import load_boxes


class _Vertex:
    """A vertex in a laptop recommendation graph, used to represent the laptop's specs, including 'name', 'price',
    'processor', 'ram', 'os', 'storage', 'display (inches)', 'rating' represented by strings.

    Instance Attributes:
        - item: The data stored in this vertex, holding both id and rating in id
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

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'book'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()

    def similarity_score(self, other: _Vertex) -> float:
        """Return the similarity score between this vertex and other.
        If this vertex has the same item as another vertex, and they are both of the same kind,
        """

        # TODO (Consideration) what if we mimic Ex 4 in terms of using weighted graphs

        if len(self.neighbours) == 0 or len(other.neighbours) == 0:
            return 0

        # temporary fix lol
        s_neighbor_no_price = self.neighbours.copy()
        s_price = [v for v in self.neighbours if v.kind == "price(in Rs.)"][0]
        s_neighbor_no_price.remove(s_price)

        o_neighbor_no_price = other.neighbours.copy()
        o_price = [v for v in other.neighbours if v.kind == "price(in Rs.)"][0]
        o_neighbor_no_price.remove(o_price)

        # Non price similarity score
        numerator = len(s_neighbor_no_price.intersection(o_neighbor_no_price))
        denominator = len(s_neighbor_no_price.union(o_neighbor_no_price))

        # Price similarity score
        price_tolerance = 100
        sim_score_price = abs(s_price.item - o_price.item)

        return numerator / denominator


class Graph:
    """A graph used to represent a book review network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]
    _ratings: dict[int, float]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}
        self._ratings = {}

    def add_vertex(self, item: Any, type_: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'user', 'book'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, type_)

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

    def add_rating(self, id_: int, rating: float) -> None:
        """Adds a rating to the graph"""
        self._ratings[id_] = rating

    def get_neighbours(self, item: Any) -> dict:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.kind: neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_similarity_score(self, item1: Any, item2: Any) -> float:
        """Return the similarity score between the two given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        >>> g = Graph()
        >>> for i in range(0, 6):
        ...     g.add_vertex(str(i), kind='user')
        >>> g.add_edge('0', '2')
        >>> g.add_edge('0', '3')
        >>> g.add_edge('0', '4')
        >>> g.add_edge('1', '3')
        >>> g.add_edge('1', '4')
        >>> g.add_edge('1', '5')
        >>> g.get_similarity_score('0', '1')
        0.5
        """

        if item1 not in self._vertices or item2 not in self._vertices:
            raise ValueError
        else:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]
            return v1.similarity_score(v2)

    def recommended_laptops(self, specs: int, limit: int):
        """Get recommended laptops"""
        recommended_dict = {}

        for vertex in self._vertices:
            vertex_obj = self._vertices[vertex]
            if vertex != specs and vertex_obj.kind == 'id':
                similarity_score = self.get_similarity_score(specs, vertex)
                if similarity_score > 0:
                    recommended_dict[vertex] = similarity_score + (self._ratings[vertex] / 5 * (1 / 7))  #

        recommended_list = [(recommended_dict[laptop_id], laptop_id) for laptop_id in recommended_dict]
        recommended_list.sort(reverse=True)
        recs = [i[1] for i in recommended_list[0:limit]]

        return recs


def _get_processor(processor: str) -> tuple[str, str]:
    """fiukhdsjkfhdsf"""
    processing_power_dict = {"low": ["i3"],
                             "medium": ["i5"],
                             "high": ["i7", "i9"]}

    if "amd" in processor.lower():
        brand = "amd"
    elif "apple" in processor.lower():
        brand = "apple"
    else:
        brand = "intel"

    proc_pwr = "medium"
    for k in processing_power_dict.keys():
        if any(i in processor.lower() for i in processing_power_dict[k]):
            proc_pwr = k
            break

    return brand, proc_pwr


def load_laptop_graph(laptop_data_file: str) -> Graph:
    """Return a book review graph corresponding to the given datasets.

    Preconditions:
        - reviews_file is the path to a CSV file corresponding to the book review data
          format described on the assignment handout
        - book_names_file is the path to a CSV file corresponding to the book data
          format described on the assignment handout
        - each book ID in reviews_file exists as a book ID in book_names_file

    """
    df = pd.read_csv(laptop_data_file)
    df = df.drop(columns=['id'])
    df = df.drop_duplicates()
    df = df.dropna()
    exchange_rate = 0.016  # INR to CAD
    df['price(in Rs.)'] = round(df['price(in Rs.)'] * exchange_rate)
    # print(df)

    graph = Graph()

    # with open(laptop_data_file, 'r') as file:
    #     reader = csv.reader(file)
    #     data = ['name', 'price', 'processor', 'ram', 'os', 'storage', 'display']
    #     for row in reader:
    #         id = row[0]
    #         # rating = row[9]
    #         # tmp = _Id(id, rating)
    #         graph.add_vertex(id, 'id')
    #         for i in range(len(data)):
    #             j = row[i + 2]
    #             graph.add_vertex(j, data[i])
    #             graph.add_edge(id, j)

    # data = ['name', 'price(in Rs.)', 'processor', 'ram', 'os', 'storage', 'display(in inch)']
    data_ = ['name', 'price(in Rs.)', 'processor', 'ram', 'os', 'storage', 'display(in inch)']
    for index, row in df.iterrows():
        # id = index
        # rating = row[9]
        # tmp = _Id(id, rating)
        graph.add_vertex(index, 'id')
        graph.add_rating(index, row['rating'])
        for i in range(len(data_)):
            j = row[data_[i]]

            if i == 2:  # (if currently assessing processor)
                brand, proc_pwr = _get_processor(j)
                graph.add_vertex(brand, "processor")
                graph.add_vertex(proc_pwr, "processing power")
                graph.add_edge(index, brand)
                graph.add_edge(index, proc_pwr)
            else:
                graph.add_vertex(j, data_[i])
                graph.add_edge(index, j)

    return graph


if __name__ == "__main__":
    g = load_laptop_graph("laptops.csv")
    data = ['', '', 'processor', 'processing power', 'ram', 'os', 'storage', 'display(in inch)']

    specs = load_boxes()

    g.add_vertex(-1, 'id')  # TODO: BE ABLE TO CHANGE THE ID MAYBE
    tot_price = 0
    diff = 0

    if specs is not None:
        for ques, ans in specs.items():
            print(f"{ques}: {ans}")

            val = None

            # create price vertex
            if ques == 0:
                tot_price += float(ans)
                continue
            elif ques == 1:
                tot_price += float(ans)
                val = tot_price/2
                diff = float(ans) - val
                g.add_vertex(val, 'price(in Rs.)')
                # for similarity score, we get range which is mean_price +- diff
            # other
            else:
                val = data[ques]
                g.add_vertex(ans, val)

            g.add_edge(-1, val)

    else:
        print("Form was closed without submission.")
