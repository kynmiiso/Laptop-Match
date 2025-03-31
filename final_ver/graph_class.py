"""CSC111 Project 2 | Laptop Recommendation System"""

from __future__ import annotations

import json
from typing import Any, Optional

# from python_ta.contracts import check_contracts
import pandas as pd

FACTORS_EXCL_LIMIT = 7  # price range, specs, etc


class _Vertex:
    """A vertex in a laptop recommendation graph, used to represent the laptop's specs, including 'name', 'price',
    'processor', 'ram', 'os', 'storage', 'display (inches)', 'rating' represented by strings.
    """
    item: Any
    kind: str
    neighbours: set[_Vertex]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()

    def _remove_certain_vertices(self,
                                 empty_vertice_kinds: Optional[list[str]] = None) -> tuple[set, _Vertex]:
        s_neighbor_no_price = self.neighbours.copy()

        # GET PRICE FROM NEIGHBOURS
        s_price = [v_neighbor for v_neighbor in self.neighbours if v_neighbor.kind == "price(in Rs.)"][0]

        s_to_remove = [s_price]

        # EXCLUDE EMPTY VERTICES FOR COUNT
        s_to_remove.extend([v_neighbor for v_neighbor in self.neighbours
                            if v_neighbor.kind in empty_vertice_kinds + ["name"]])

        # REMOVE VERTICES
        for v in s_to_remove:
            s_neighbor_no_price.remove(v)

        # FINALISE SET TO ONLY CONTAIN ITEMS
        s_neighbor_no_price = {v_neighbor.item for v_neighbor in s_neighbor_no_price}

        return s_neighbor_no_price, s_price

    def similarity_score(self, other: _Vertex, price_tolerance: float = 100.0,
                         empty_vertice_kinds: Optional[list[str]] = None) -> float:
        """Return the similarity score between this vertex and other.
        If this vertex has the same item as another vertex, and they are both of the same kind,

        Note that this is coded to only be applicable to vertex of kind 'id'

        Preconditions:
        - self.kind == 'id'
        """
        if empty_vertice_kinds is None:
            empty_vertice_kinds = []
        if len(self.neighbours) == 0 or len(other.neighbours) == 0:
            return 0

        s_neighbor_no_price, s_price = self._remove_certain_vertices(empty_vertice_kinds)
        o_neighbor_no_price, o_price = other._remove_certain_vertices(empty_vertice_kinds)

        # print(f'{s_neighbor_no_price}, {s_price.item}, {o_neighbor_no_price}, {o_price.item}')

        # Non price similarity score
        numerator = len(s_neighbor_no_price.intersection(o_neighbor_no_price))
        denominator = len(s_neighbor_no_price.union(o_neighbor_no_price))

        sim_score_price = int(abs(float(s_price.item) - float(o_price.item)) <= price_tolerance)
        # check whether the price falls between the range min_range to max_range

        if empty_vertice_kinds:
            factors = FACTORS_EXCL_LIMIT - len(empty_vertice_kinds)
        else:
            factors = FACTORS_EXCL_LIMIT

        if denominator == 0:
            return sim_score_price / factors
        else:
            return (numerator / denominator) + (sim_score_price * (1 / factors))
            # weight for the price depends on number of factors considered


class Graph:
    """A graph used to represent a book review network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    # _vertices: dict[Any, _Vertex]
    _vertices: dict[tuple[Any, str], _Vertex]
    _ratings: dict[Any, float]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}
        self._ratings = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'name', 'price', 'processor', 'ram', 'os',
        'storage', 'display size', 'rating'}
        """
        if item not in self._vertices:
            self._vertices[(item, kind)] = _Vertex(item, kind)

    def add_edge(self, item1: tuple[Any, str], item2: tuple[Any, str]) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]  # send in item name and kind
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def add_rating(self, id_: Any, rating: float) -> None:
        """Adds a rating to the graph"""
        self._ratings[id_] = rating

    def get_vertices(self, kind: str) -> set[Any]:
        """Return a set of all vertice items of some kind"""
        return {v.item for v in self._vertices.values() if v.kind == kind}

    def get_neighbours(self, item: Any, kind: str) -> dict:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if (item, kind) in self._vertices:
            v = self._vertices[(item, kind)]
            return {neighbour.kind: neighbour.item for neighbour in v.neighbours}
            # return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_similarity_score(self, item1: tuple[Any, str], item2: tuple[Any, str],
                             price_tolerance: float = 100.0,
                             empty_vertices_kind: Optional[list] = None) -> float:
        """Return the similarity score between the two given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.
        """

        if item1 not in self._vertices or item2 not in self._vertices:
            raise ValueError
        else:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]
            sim_score = v1.similarity_score(v2, price_tolerance, empty_vertices_kind)  # allow partial matching

            return sim_score

    def recommended_laptops(self, specs_: int, limit: int, price_tolerance: float,
                            empty_vertices_kind: Optional[list] = None) -> list:
        """Get recommended laptops"""
        recommended_dict = {}

        if not empty_vertices_kind:
            factors = FACTORS_EXCL_LIMIT
        else:
            factors = FACTORS_EXCL_LIMIT - len(empty_vertices_kind)

        for vertex in self._vertices:
            vertex_obj = self._vertices[vertex]
            if vertex != specs_ and vertex_obj.kind == 'id' and vertex[0] >= 0:
                similarity_score = self.get_similarity_score((specs_, "id"), vertex, price_tolerance,
                                                             empty_vertices_kind)  # allow partial matching
                if similarity_score > 0:  # has some degree of similarity
                    recommended_dict[vertex] = similarity_score + (self._ratings[vertex[0]] / 5 * (1 / factors))

        recommended_list = [(recommended_dict[laptop_id], laptop_id) for laptop_id in recommended_dict]
        recommended_list.sort(reverse=True)

        recs = [i[1][0] for i in recommended_list[0:limit]]

        return recs

    def id_to_rec(self, recs_ids: list, limit: int, img_links: dict) -> dict:
        """Converts id list to recommendation data with image links."""
        recommendations = {}

        for i, laptop_id in enumerate(recs_ids[:limit]):
            neighbors = self.get_neighbours(laptop_id, "id")

            name = neighbors.get("name")

            data = ["price(in Rs.)", "processor", "ram", "storage", "display(in inch)"]

            recommendations[i] = {
                'Name': name,
                'Price': neighbors.get(data[0]),
                'Processor': neighbors.get(data[1]),
                'RAM': neighbors.get(data[2]),
                'Storage': neighbors.get(data[3]),
                'Display': neighbors.get(data[4]),
                'Rating': self._ratings.get(laptop_id),
                'Image': img_links.get(laptop_id)
            }

        return recommendations


def add_dummy(g: Graph, specs_dict: dict, dummy_id: int = -1) -> None:
    """Inject dummy laptop into graph"""
    # based on information in the csv as well as the vertex kinds we are looking for
    data = ['', '', 'processor', 'processing power', 'ram', 'os', 'storage', 'display(in inch)']

    g.add_vertex(dummy_id, 'id')
    tot_price = 0

    if specs_dict is not None:
        for ques, ans in specs_dict.items():
            # create price vertex
            if ques == 0:
                tot_price += float(ans)
                continue
            elif ques == 1:
                tot_price += float(ans)
                val = tot_price / 2
                g.add_vertex(val, 'price(in Rs.)')
                g.add_edge((dummy_id, "id"), (val, 'price(in Rs.)'))
                # for similarity score, we get range which is mean_price +- diff
            elif 2 <= ques < len(data):
                val = data[ques].lower().strip()
                g.add_vertex(ans, val)
                g.add_edge((dummy_id, "id"), (ans, val))
            else:
                continue


def _convert_split(s: str, mapping: dict) -> tuple[str, str]:
    """Split string s to appropriate pieces of information, e.g. from "Intel
    s: string data
    mapping: maps from broad category to specifics (e.g. {"Intel": {"low": ["i3"], "medium": ["i5"], ...}
    """
    broad = None
    for general_k in mapping.keys():
        broad = general_k
        if general_k.lower() in s.lower():
            break

    specific = None
    for specific_k in mapping[broad]:
        specific = specific_k
        if any(i.lower() in s.lower() for i in mapping[broad][specific_k]):
            break

    return broad, specific


def _convert_val(s: str, mapping: dict) -> str:
    """
    s: string data
    mapping: mapping from output key to string in data or blank
    """
    itm = None
    for k in mapping:
        itm = k
        # if k.lower() in s.lower():
        if k.lower() in s.lower() or any(i.lower() in s.lower() for i in mapping[k]):
            # safety net if specific keyword is not found in s but s is still under category k
            return k

    return itm


def _load_data(filename: str) -> dict:
    """Load minigames from a JSON file with the given filename."""
    with open(filename, 'r') as f:
        grouped_data = json.load(f)

    return grouped_data


def load_laptop_graph(laptop_data_file: str, parameters_file: str) -> tuple[Graph, dict]:
    """Return a book review graph corresponding to the given datasets and a dictionary mapping laptop to image link.

    Preconditions:
        - laptop_data_file is the path to a CSV file corresponding to the laptop data
        - parameters_file is the path to a JSON file containing parameters to convert to kind
        - csv file rows contain headings in parameters_file in that order
        - parameters_file should contain ["processor", "ram", "os", "storage",
          'display(in inch)', 'name', 'price(in Rs.)']
    """
    # data cleaning
    df = pd.read_csv(laptop_data_file)
    df = df.drop(columns=['id'])
    df = df.drop_duplicates()
    df = df.dropna()
    exchange_rate = 0.016  # INR to CAD
    df['price(in Rs.)'] = round(df['price(in Rs.)'] * exchange_rate)
    # print(df)
    df = df.reset_index()
    df = df.drop(columns=['index'])

    img_links = {img_index: img_row['img_link'] for img_index, img_row in df.reset_index().iterrows()}

    df = df.drop(columns=['img_link'])

    # create graph
    graph = Graph()
    data_ = _load_data(parameters_file)

    for index, row in df.iterrows():

        graph.add_vertex(index, 'id')
        graph.add_rating(index, row['rating'])

        for k in data_:
            # print(type(row[k]), row[k])
            j = str(row[k]).lower().strip()
            if k == "processor":
                brand, proc_pwr = _convert_split(j, data_[k])
                graph.add_vertex(brand, "processor")
                graph.add_vertex(proc_pwr, "processing power")
                graph.add_edge((index, "id"), (brand, "processor"))
                graph.add_edge((index, "id"), (proc_pwr, "processing power"))
            elif k in ["ram", "os", "storage"]:
                j = _convert_val(j, data_[k])
                graph.add_vertex(j, k)
                graph.add_edge((index, "id"), (j, k))
            elif k == 'display(in inch)':
                j = str(int(round(float(j), 0)))
                graph.add_vertex(j, k)
                graph.add_edge((index, "id"), (j, k))
            elif k in ['name', 'price(in Rs.)']:
                graph.add_vertex(j, k)
                graph.add_edge((index, "id"), (j, k))

    return graph, img_links


if __name__ == "__main__":
    import doctest
    import python_ta

    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': [
            'json',
            'typing',
            'pandas'
        ],
        'allowed-io': ['_load_data'],
        'max-line-length': 120
    })

    python_ta.contracts.check_all_contracts("graph_class.py")
