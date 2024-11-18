from pulp import LpProblem, LpMinimize, LpVariable, lpSum,  LpStatus, value

def main():
    # Using a dictionary as the input data of the problem:
    data = {
        "num_reqs": 3,
        "ing_node": [0, 1, 2],  # ingress_nodes
        "egr_node": [5, 4, 3],  # egress_nodes
        "flow": [6, 4, 2],  # commodity_flow

        "num_ndes": 6,
        "nde_to_nde": [[0, 1, 1, 0, 0, 0],
                       [0, 0, 0, 1, 1, 0],
                       [0, 0, 0, 1, 1, 0],
                       [0, 0, 0, 0, 1, 1],
                       [0, 0, 0, 0, 0, 1],
                       [0, 0, 0, 0, 0, 0]],
        "capacity": [[0, 8, 6, 0, 0, 0],
                     [0, 0, 0, 6, 1, 0],
                     [0, 0, 0, 3, 4, 0],
                     [0, 0, 0, 0, 6, 4],
                     [0, 0, 0, 0, 0, 6],
                     [0, 0, 0, 0, 0, 0]],
        "cost": [[0, 3, 3, 0, 0, 0],
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

    # 1. Define the problem
    prob = LpProblem("MCF_LP_Path_Variables", LpMinimize)

    # 2. Define variables
    path_vars = {}
    for req in REQs:
        for p, path in enumerate(paths[req]):
            path_vars[req, p] = LpVariable(f"flow_req{req}_path{p}", lowBound=0)

    # 3. Add the objective function
    prob += lpSum(
        path_vars[req, p] * sum(data["cost"][path[i]][path[i + 1]] for i in range(len(path) - 1))
        for req in REQs for p, path in enumerate(paths[req])
    )

    # 4. Add flow constraints
    for req in REQs:
        prob += lpSum(path_vars[req, p] for p in range(len(paths[req]))) == data["flow"][req], f"Flow_Req{req}"

    # 5. Add capacity constraints
    for u in NDEs:
        for v in NDEs:
            if data["nde_to_nde"][u][v]:
                prob += lpSum(
                    path_vars[req, p]
                    for req in REQs
                    for p, path in enumerate(paths[req])
                    if (u, v) in zip(path, path[1:])
                ) <= data["capacity"][u][v], f"Capacity_{u}_{v}"

    # 6. Solve the problem
    prob.solve()

    # 7. Output results
    print(f"Status: {LpStatus[prob.status]}")
    print(f"MCF min cost: {value(prob.objective)}")
    for req in REQs:
        for p, path in enumerate(paths[req]):
            flow = path_vars[req, p].varValue
            if flow > 0:
                print(f"req_{req}, path_{p} ({path}): flow {flow}")

if __name__ == "__main__":
    main()
