from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, lpSum, PULP_CBC_CMD, LpStatus

'''
3 types of SFCs:
 
        VNF1_1 -  VNF1_2  -  VNF1_3
                  
        VNF2_4 -  VNF2_5  -  VNF2_7
               \  VNF2_6  /
                     
                  VNF3_9  - VNF3_11
               /  
        VNF3_8
               \
                  VNF3_10 - VNF3_12

problem input:                        
- a given amount of requests of the 3 types of SFCs,
- the 3 SFC-graphs with their VNFs weights, 
- a set of servers of 2 types: edge-servers and core-servers.

'''

def main():
    
    
    data = {
        "num_reqs": 6,
        "sfc_type": [0, 0, 0, 1, 1, 2],

        "num_vnfs": 12,
        "vnf_weight": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "vnf_in_sfc": [
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],  
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],  
        ],

        "num_srvs": 3,
        "srv_type": [1, 1, 0],  
        "srv_cap": [10, 10, 10]  
    }

    REQs = range(data["num_reqs"])
    VNFs = range(data["num_vnfs"])
    SRVs = range(data["num_srvs"])

    
    problem = LpProblem("SFC_only_vnf_mapping_Problem", LpMinimize)

    
    var_vnf = LpVariable.dicts("vnf_fit", (REQs, VNFs, SRVs), 0, 1, LpInteger)

    
    
    problem += lpSum(
        var_vnf[req][vnf][srv] * data["srv_type"][srv]
        for req in REQs
        for vnf in VNFs
        for srv in SRVs
        if data["vnf_in_sfc"][data["sfc_type"][req]][vnf] == 1
    )

    

    
    for srv in SRVs:
        problem += lpSum(
            var_vnf[req][vnf][srv] * data["vnf_weight"][vnf]
            for req in REQs
            for vnf in VNFs
            if data["vnf_in_sfc"][data["sfc_type"][req]][vnf] == 1
        ) <= data["srv_cap"][srv], f"Capacity_constraint_srv_{srv}"

    
    for req in REQs:
        for vnf in VNFs:
            if data["vnf_in_sfc"][data["sfc_type"][req]][vnf] == 1:
                problem += lpSum(
                    var_vnf[req][vnf][srv] for srv in SRVs
                ) == 1, f"Single_allocation_req_{req}_vnf_{vnf}"

    
    problem.solve(PULP_CBC_CMD(msg=False))

    
    print(f"Status: {LpStatus[problem.status]}\n")

    
    total_vnfs = 0
    total_weight = 0
    for srv in SRVs:
        print(f"Content of srv {srv}:")
        srv_weight = 0
        for req in REQs:
            for vnf in VNFs:
                if var_vnf[req][vnf][srv].value() == 1.0:
                    print(f"req {req} vnf {vnf}")
                    srv_weight += data["vnf_weight"][vnf]
                    total_vnfs += 1

        print(f"Weight of srv {srv} = {srv_weight}\n")
        total_weight += srv_weight

    print(f"Total accepted VNFs = {total_vnfs}")
    print(f"Total weight of REQs = {total_weight}")


if __name__ == "__main__":
    main()
