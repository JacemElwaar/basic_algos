class Graph():

    def __init__(self, num_users, BS_cap):
        self.num_users = num_users
        self.num_BS = len(BS_cap)
        self.graph = [[0 for column in range(self.num_BS)] for row in range(num_users)]
        self.BS_cap = BS_cap

    def isSafe(self, user, BS, state):
        return self.graph[user][BS] == 1 and state[BS] < self.BS_cap[BS]

    def successor_function(self, user, assignment, state):
        if user >= self.num_users:
            return True

        for BS in range(self.num_BS):
            if self.isSafe(user, BS, state):
                assignment[user] = BS
                state[BS] += 1

                if self.successor_function(user + 1, assignment, state):
                    #print('state' , state)
                    return True

                assignment[user] = -1
                state[BS] -= 1
                #print("debug")
                #print(assignment[user] ,  state[BS] )

        return False

    def BS_assignment(self):
        load_state = [0] * len(self.BS_cap)
        assignment = [-1 for _ in range(self.num_users)]

        assignment_success = self.successor_function(user=0, assignment=assignment, state=load_state)

        if not assignment_success:
            print('no solution has been found')

        else:
            print("solution exists with assigned BS:")
            for i, BS in enumerate(assignment):
                print(f"User {i} assigned to BS {BS}")
            print("\nLoad of each BS: ", load_state)

if __name__ == "__main__":

    num_users = 10
    g = Graph(10, [4, 3, 4])
    g.graph = [[1, 1, 1],
               [1, 0, 1],
               [1, 1, 0],
               [1, 1, 0],
               [1, 1, 1],
               [1, 0, 1],
               [1, 0, 0],
               [0, 1, 1],
               [0, 1, 1],
               [0, 1, 0]]

    g.BS_assignment()
