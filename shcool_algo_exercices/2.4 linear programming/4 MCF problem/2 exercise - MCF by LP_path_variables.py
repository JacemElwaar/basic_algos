#solved with variables = paths, instead of variables = links.

from pulp import *

def main():

    # using a dictionary as the input data of the problem:

    data = {
            "num_reqs": 3,
            "ing_node": [0, 1, 2],  # ingress_nodes
            "egr_node": [5, 4, 3],  # egress_nodes
            "flow":     [6, 4, 2],  # commodity_flow

            "num_ndes": 6,
            "nde_to_nde":
                [[0, 1, 1, 0, 0, 0],
                 [0, 0, 0, 1, 1, 0],
                 [0, 0, 0, 1, 1, 0],
                 [0, 0, 0, 0, 1, 1],
                 [0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 0]],
            "capacity":
                [[0, 8, 6, 0, 0, 0],
                 [0, 0, 0, 6, 1, 0],
                 [0, 0, 0, 3, 4, 0],
                 [0, 0, 0, 0, 6, 4],
                 [0, 0, 0, 0, 0, 6],
                 [0, 0, 0, 0, 0, 0]],
            "cost":
                [[0, 3, 3, 0, 0, 0],
                 [0, 0, 0, 3, 3, 0],
                 [0, 0, 0, 3, 3, 0],
                 [0, 0, 0, 0, 3, 3],
                 [0, 0, 0, 0, 0, 3],
                 [0, 0, 0, 0, 0, 0]],
            }

    # Sets of candidate paths for each request:
    paths = {
        0: [[0, 1, 3, 5], [0, 1, 3, 4, 5], [0, 1, 4, 5], [0, 2, 3, 5], [0, 2, 3, 4, 5], [0, 2, 4, 5]],
        1: [[1, 4], [1, 3, 4]],
        2: [[2, 3]]
    }

    REQs = range(data["num_reqs"])
    NDEs = range(data["num_ndes"])


    # to be completed


if __name__ == "__main__":
    main()

