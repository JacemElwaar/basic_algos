
"""Solve a Multi-dim Multi_Knapsack_Problem using an ILP solver"""

from pulp import *


if __name__ == "__main__":
    
    # using a dictionary as the input data of the problem:
    
    data = {
            "req_res": [[36, 24, 48], [30, 30, 30], [24, 42, 12], [36, 42, 0], [36, 36, 36], [12, 24, 36], [36, 12, 24], [42, 42, 42], [16, 0, 24], [24, 24, 24], [6, 8, 0], [18, 24, 12]],
            "req_val": [10, 30, 25, 50, 35, 30, 15, 40, 30, 35, 45, 10],
            "bin_res": [[50, 50, 50], [100, 100, 100], [150, 150, 150]]
            }
    
    assert len(data["req_res"]) == len(data["req_val"])
 
    REQs = range(len(data["req_res"]))
    BINs = range(len(data["bin_res"]))

    # max problem:
    problem = LpProblem("mul-dim-req_multi_knapsack_problem", LpMaximize)

    # binary variables:
    var = LpVariable.dicts("req_fit", (REQs, BINs), 0, 1, LpInteger)

    # utility function: maximise the accumulated value of accepted REQs:
    # to be completed

    # constraints:
    
    # for each bin, all allocated reqs must not exceed the bin capacity:
    # to be completed

    # for each req, it must be allocated in a single bin or left out of service:
    # to be completed
        
    problem.solve(PULP_CBC_CMD(msg=False))

    ##########################
    # print out the result
    ##########################

    # The status of the solution is printed to the screen:
    print(f"Status: {LpStatus[problem.status]}\n")

    print(f"maximum profit = {problem.objective.value()}\n")

    # print out the REQs accommodated at each bin:
    total_reqs = 0
    consumed_resources = [0, 0, 0]
    for bin in BINs:
        print(f"Content of bin_{bin}:")
        bin_consumed_resources = [0, 0, 0]
        for req in REQs:
            if var[req][bin].value() == 1.0:
                print(f"req_{req}")
                bin_consumed_resources[0] += data["req_res"][req][0]
                bin_consumed_resources[1] += data["req_res"][req][1]
                bin_consumed_resources[2] += data["req_res"][req][2]
                total_reqs += 1
        print(f"consumed resources of bin_{bin} = {bin_consumed_resources}\n")
        consumed_resources[0] += bin_consumed_resources[0]
        consumed_resources[1] += bin_consumed_resources[1]
        consumed_resources[2] += bin_consumed_resources[2]
    print(f"total accepted REQs = {total_reqs} of {len(data['req_val'])}")
    print(f"consumed resources REQs = {consumed_resources}")


