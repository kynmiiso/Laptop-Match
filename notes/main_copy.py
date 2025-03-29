"""practically a copy"""
import json
from pprint import pprint
from typing import Any

import pandas as pd


class _Vertex:
    """A vertex in a laptop recommendation graph, used to represent the laptop's specs, including 'name', 'price',
    'processor', 'ram', 'os', 'storage', 'display (inches)', 'rating' represented by strings.
    """
    item: Any
    kind: str
    neighbours: set

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()

    def similarity_score(self, other, price_tolerance: float = 100.0) -> float:
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

        sim_score_price = int(abs(s_price.item - o_price.item) <= price_tolerance)
        # check whether the price falls between the range min_range to max_range

        return numerator / denominator + (sim_score_price * (1 / 8))  # weight for the price is 1/8


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

    def add_vertex(self, item: Any, type_: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'user', 'book'}
        """
        if item not in self._vertices:
            self._vertices[(item, type_)] = _Vertex(item, type_)

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

    def get_vertices(self, kind: str):
        """Return a set of all vertice items of some kind"""
        return {v.item for v in self._vertices.values() if v.kind == kind}

    def get_neighbours(self, item: Any, kind: str):
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
                             price_tolerance: float = 100.0) -> float:
        """Return the similarity score between the two given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.
        """

        if item1 not in self._vertices or item2 not in self._vertices:
            raise ValueError
        else:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]
            print(v1.item, v2.item)
            sim_score = v1.similarity_score(v2, price_tolerance)
            print(v1.item, v2.item, sim_score)
            return sim_score
            # return v1.similarity_score(v2, price_tolerance)

    def recommended_laptops(self, specs_: int, limit: int, price_tolerance: float) -> list:
        """Get recommended laptops"""
        recommended_dict = {}

        for vertex in self._vertices:
            vertex_obj = self._vertices[vertex]
            if vertex != specs_ and vertex_obj.kind == 'id':
                similarity_score = self.get_similarity_score((specs_, "id"), vertex, price_tolerance)
                if similarity_score > 0:
                    recommended_dict[vertex] = similarity_score + (self._ratings[vertex] / 5 * (1 / 8))

        recommended_list = [(recommended_dict[laptop_id], laptop_id) for laptop_id in recommended_dict]
        recommended_list.sort(reverse=True)
        recs = [i[1] for i in recommended_list[0:limit]]

        return recs


def _convert_split(s: str, mapping: dict):
    """
    s: string data
    mapping: conditions thing; maps from broad category to specifics (e.g. {"Intel": {"low": ["i3"], "medium": ["i5"]}}
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


def _convert_val(s: str, mapping: dict):
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


def load_laptop_graph(laptop_data_file: str) -> Graph:
    """Return a book review graph corresponding to the given datasets.

    Preconditions:
        - reviews_file is the path to a CSV file corresponding to the book review data
          format described on the assignment handout
        - book_names_file is the path to a CSV file corresponding to the book data
          format described on the assignment handout
        - each book ID in reviews_file exists as a book ID in book_names_file

    """
    # TODO
    spotlight = [15, 16, 35, 62, 196, 220, 235, 249, 272, 285, 333, 347, 352, 397, 446, 450, 477, 508, 514]

    df = pd.read_csv(laptop_data_file)
    df = df.drop(columns=['id'])
    df = df.drop_duplicates()
    df = df.dropna()
    exchange_rate = 0.016  # INR to CAD
    df['price(in Rs.)'] = round(df['price(in Rs.)'] * exchange_rate)
    # print(df)
    df = df.reset_index()
    df = df.drop(columns=['index'])
    df = df.drop(columns=['img_link'])

    graph = Graph()

    data_ = _load_data('../parameters_data.json')

    # todo
    # pprint(data_)
    print(data_.keys())

    for index, row in df.iterrows():
        # todo
        if index in spotlight:
            print(index, row['name'])

        graph.add_vertex(index, 'id')
        graph.add_rating(index, row['rating'])

        for k in data_:
            j = row[k]
            if k == "processor":
                brand, proc_pwr = _convert_split(j, data_[k])
                graph.add_vertex(brand, "processor")
                graph.add_vertex(proc_pwr, "processing power")

                # todo
                # if index in spotlight:
                #     print(f'{index} Processor: {brand}, Processing power: {proc_pwr}')

                graph.add_edge((index, "id"), (brand, "processor"))
                graph.add_edge((index, "id"), (proc_pwr, "processing power"))
            elif k in ["ram", "os", "storage"]:
                val_ = _convert_val(j, data_[k])
                graph.add_vertex(val_, k)

                # todo
                # if index in spotlight:
                #     print(f'{index} {k.upper()}: {val_}')

                graph.add_edge((index, "id"), (val_, k))
            elif k in ['name', 'display(in inch)', 'price(in Rs.)']:  # todo: issue is here
                graph.add_vertex(j, k)

                # todo
                if index in spotlight:
                    # print(f'{index} {k}: {j}')
                    print(f'graph.add_vertex(item="{j}", type_="{k}")')

                graph.add_edge((index, "id"), (j, k))

                # todo sflhdslkhfdslkfsfdlk
                if index in spotlight:
                    print(f'graph.add_edge(item1="{index}", item2="{j}")')

        if index in spotlight:  # todo
            print(f'---')

    return graph
