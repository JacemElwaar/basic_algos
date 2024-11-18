from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, PULP_CBC_CMD


def main():
    # using a dictionary as the input data of the problem:
    data = {
        "num_reqs": 3,
        "ing_node": [0, 1, 2],  # ingress_nodes
        "egr_node": [5, 4, 3],  # egress_nodes
        "flow": [6, 4, 2],  # commodity_flow

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

    REQs = range(data["num_reqs"])
    NDEs = range(data["num_ndes"])

    # min problem:
    problem = LpProblem("MCF_problem", LpMinimize)

    # variables of the LP problem: flow to be injected from each req through each link(u,v)
    var_lnk_flow = LpVariable.dicts("flow_fit", (REQs, NDEs, NDEs), lowBound=0)

    # Utility function: minimize the cost of transmitting all flows through all links:
    problem += lpSum(
        var_lnk_flow[req][node_u][node_v] * data["cost"][node_u][node_v]
        for req in REQs
        for node_u in NDEs
        for node_v in NDEs
        if data["nde_to_nde"][node_u][node_v]
    )

    # Constraints:

    # Capacity constraints: For each link(u,v), all allocated flows must not exceed the link capacity:
    for node_u in NDEs:
        for node_v in NDEs:
            if data["nde_to_nde"][node_u][node_v]:
                problem += lpSum(var_lnk_flow[req][node_u][node_v] for req in REQs) <= data["capacity"][node_u][node_v]

    # Flow conservation constraints:
    for req in REQs:
        for node_u in NDEs:
            if node_u == data["ing_node"][req]:  # Source node
                problem += lpSum(
                    var_lnk_flow[req][node_u][node_v] for node_v in NDEs if data["nde_to_nde"][node_u][node_v]
                ) - lpSum(
                    var_lnk_flow[req][node_v][node_u] for node_v in NDEs if data["nde_to_nde"][node_v][node_u]
                ) == data["flow"][req]
            elif node_u == data["egr_node"][req]:  # Sink node
                problem += lpSum(
                    var_lnk_flow[req][node_v][node_u] for node_v in NDEs if data["nde_to_nde"][node_v][node_u]
                ) - lpSum(
                    var_lnk_flow[req][node_u][node_v] for node_v in NDEs if data["nde_to_nde"][node_u][node_v]
                ) == data["flow"][req]
            else:  # Intermediate nodes
                problem += lpSum(
                    var_lnk_flow[req][node_u][node_v] for node_v in NDEs if data["nde_to_nde"][node_u][node_v]
                ) - lpSum(
                    var_lnk_flow[req][node_v][node_u] for node_v in NDEs if data["nde_to_nde"][node_v][node_u]
                ) == 0

    
    problem.solve(PULP_CBC_CMD(msg=False))


    # The status of the solution is printed to the screen
    print(f"Status: {LpStatus[problem.status]}\n")

    # print out the flow sent by each link(u,v) of all requests
    if problem.objective:
        print(f"MCF min cost: {problem.objective.value()}")
    else:
        print(f"Problem status: {LpStatus[problem.status]} - No solution found.")

    for req in REQs:
        print(f"\nreq_{req}: ")
        for node_u in NDEs:
            for node_v in NDEs:
                if data["nde_to_nde"][node_u][node_v] and var_lnk_flow[req][node_u][node_v].value() > 0:
                    print(f"link_{node_u}{node_v}: flow {var_lnk_flow[req][node_u][node_v].value()}, ")


if __name__ == "__main__":
    main()
