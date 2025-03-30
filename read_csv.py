"""Function to read csv"""

import csv


def read_csv(filename):
    """
    Read CSV file
    :param filename:
    :return:
    """
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            pass


# def img_link_from_csv(filename, id: str) -> str:
#     """Returns the image link associated with the id for the csv for the final laptop output.
#
#     Preconditions:
#     - ids are in the first column of the csv file
#     - img_links are located in the second column of the csv file
#
#     """
#     dict = {}
#
#     with open(filename, 'r') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             dict[row[0]] = row[1]
#
#     if id not in dict:
#         raise KeyError
#     else:
#         return dict[id]
