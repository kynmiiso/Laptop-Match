"""
SOLELY FOR FUCKING DEBUGGING
"""

# from main import load_laptop_graph

import pandas as pd
from IPython.display import display
# import IPython

from notes.main_copy import load_laptop_graph


def abnormal_rows():
    """Abnormal rows"""
    graph = load_laptop_graph("../laptops.csv")
    ids_ = graph.get_vertices("id")

    # print(ids_)

    no_issue = ['os', 'processing power', 'processor', 'ram', 'storage']

    for id_ in ids_:
        # print(id_)
        n = graph.get_neighbours(id_, "id")
        n2 = sorted(list(n.keys()))
        # if n2 != ['display(in inch)', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram',
        # 'storage']:
        if n2 != ['display(in inch)', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']:
            # print(id_, n2)
            print(id_, n['id'], [i for i in n2 if i not in no_issue])
        # print(id_, sorted(list(n.keys())))


def setup():
    """setup df"""
    df = pd.read_csv("../laptops.csv")
    df = df.drop(columns=['id'])
    df = df.drop_duplicates()
    df = df.dropna()
    exchange_rate = 0.016  # INR to CAD
    df['price(in Rs.)'] = round(df['price(in Rs.)'] * exchange_rate)
    # print(df)
    df = df.reset_index()
    df = df.drop(columns=['index'])

    to_drop = ["img_link", "os", "ram", "storage", "processor"]
    for td in to_drop:
        df = df.drop(columns=[td])

    return df


def show_df():
    """show dataframe"""
    df = setup()

    with pd.option_context('display.max_rows', None,
                           'display.max_columns', None,
                           'display.precision', 3,
                           ):
        display(df)


def show_select_rows(lst: list):
    """show select rows"""
    df = setup()

    for i in lst:
        specific_row = df.loc[[i]]
        display(specific_row)


if __name__ == "__main__":
    # show_df()
    # show_select_rows([15, 16, 35, 62, 196, 220, 235, 249, 272, 285, 333, 347, 352, 397, 446, 450, 477, 508, 514])
    abnormal_rows()
