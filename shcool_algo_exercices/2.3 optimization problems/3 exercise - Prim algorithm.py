class Graph():

    def __init__(self, vertices):
        self.V = vertices
        self.my_shortest_edge = [float("Inf")] * self.V
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]
        self.linked_to = [None] * self.V

    def printMST(self):
        print("Minimum spanning tree:")
        t_weight = 0
        path = []
        for i in range(1, self.V):
            if self.linked_to[i] is not None:
                print(f"Nodes {self.linked_to[i]} - {i} weight {self.graph[i][self.linked_to[i]]}")
                path.append((self.linked_to[i], i))
                t_weight += self.graph[i][self.linked_to[i]]
        print(f"MST total weight : {t_weight}")
        return path, t_weight

    def get_shortest_edge(self, visited):
        min_val = float("Inf")
        min_index = -1

        for v in range(self.V):
            if self.my_shortest_edge[v] < min_val and not visited[v]:
                min_val = self.my_shortest_edge[v]
                min_index = v

        return min_index

    def primMST(self):
        first_node = 0  
        self.my_shortest_edge[first_node] = 0
        self.linked_to[first_node] = -1
        visited = [False] * self.V

        for _ in range(self.V - 1):
            u = self.get_shortest_edge(visited)
            visited[u] = True

            for v in range(self.V):
                if self.graph[u][v] and not visited[v] and self.graph[u][v] < self.my_shortest_edge[v]:
                    self.my_shortest_edge[v] = self.graph[u][v]
                    self.linked_to[v] = u

        return self.printMST()

if __name__ == "__main__":
    i = float("Inf")

    g = Graph(5)

    g.graph = [[0, 6, 4, i, 5],
               [6, 0, 2, 1, 4],
               [4, 2, 0, 2, 2],
               [i, 1, 2, 0, 3],
               [5, 4, 2, 3, 0]]

    path, t_weight = g.primMST()
    print("\n")
    print("Path Found:", path)
    print("Total min weight:", t_weight)
