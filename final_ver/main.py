"""Main file to run"""
import doctest

import python_ta
from python_ta import contracts

# from graph_class import load_laptop_graph
from final_ver.user_input_form import load_boxes

if __name__ == "__main__":
    specs = load_boxes()

    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['final_ver.user_input_form'],
        'allowed-io': [],
        'max-line-length': 120
    })

    contracts.check_all_contracts("user_input_form.py")
