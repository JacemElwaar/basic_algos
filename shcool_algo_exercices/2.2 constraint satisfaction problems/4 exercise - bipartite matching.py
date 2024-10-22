class Graph():

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]

    def isSafe(self, a, t, state):
        return self.graph[a][t] == 1 and t not in state

    def successor_function(self, a, state):
        if a >= self.V:
            return True

        for t in range(self.V):
            if self.isSafe(a, t, state):
                state[a] = t

                if self.successor_function(a + 1, state):
                    return True

                state[a] = -1

        return False

    def getMatching(self):
        state = [-1] * self.V

        assignment_success = self.successor_function(a=0, state=state)

        if not assignment_success:
            print('No solution exists')
        else:
            print("Solution exists with assigned tasks:")
            for index in range(len(state)):
                print("Agent ", index, " to Task ", state[index])

if __name__ == "__main__":
    g = Graph(6)
    g.graph = [[0, 1, 1, 0, 0, 0],
               [1, 0, 0, 1, 0, 0],
               [0, 0, 1, 0, 0, 0],
               [0, 0, 1, 1, 0, 0],
               [0, 0, 0, 0, 1, 1],
               [0, 0, 0, 0, 1, 1]]

    g.getMatching()
