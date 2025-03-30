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
