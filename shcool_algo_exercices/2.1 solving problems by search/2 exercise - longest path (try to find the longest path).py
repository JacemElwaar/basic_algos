class Graph():

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[float("Inf") for column in range(vertices)] for row in range(vertices)]
        self.dist = [-float("Inf")] * self.V  # Initialize distances to -infinity
        self.predecessor = {}

    def topological_sort_util(self, v, visited, stack):
        visited[v] = True
        for i in range(self.V):
            if self.graph[v][i] != float("Inf") and not visited[i]:
                self.topological_sort_util(i, visited, stack)
        stack.append(v)

    def topological_sort(self):
        visited = [False] * self.V
        stack = []
        for i in range(self.V):
            if not visited[i]:
                self.topological_sort_util(i, visited, stack)
        return stack[::-1]  # Return in reverse order for topological order

    def longest_path(self, src):
        stack = self.topological_sort()
        self.dist[src] = 0  # Set the source node distance to 0

        while stack:
            u = stack.pop(0)

            # If there's a valid distance for node u, update its adjacent nodes
            if self.dist[u] != -float("Inf"):
                for v in range(self.V):
                    # Update distance only if there is a valid edge and it's not infinity
                    if self.graph[u][v] != float("Inf"):
                        if self.dist[v] < self.dist[u] + self.graph[u][v]:
                            self.dist[v] = self.dist[u] + self.graph[u][v]
                            self.predecessor[v] = u

        self.printDistances()

    def printDistances(self):
        print("\nLongest distances from source:")
        for node in range(self.V):
            distance = self.dist[node] if self.dist[node] != -float("Inf") else "No path"
            print(f"Node {node} : {distance}")

        print("\nPredecessors: ", self.predecessor)

    def path(self, src, dst):
        if dst not in self.predecessor:
            return "No path exists"

        path = [dst]
        node = dst
        while node != src:
            path.append(self.predecessor[node])
            node = self.predecessor[node]
        path.reverse()
        return path


if __name__ == "__main__":

    i = float("Inf")

    g = Graph(6)
    g.graph = [[0, 4, 3, i, i, i],
               [i, 0, i, 2, 2, i],
               [i, i, 0, 8, 2, i],
               [i, i, i, 0, i, 2],
               [i, i, i, i, 0, 2],
               [i, i, i, i, i, 0]]

    g.longest_path(0)

    print("\nLongest path from 0 to 5:", g.path(0, 5))
