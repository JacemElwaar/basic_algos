class Graph():

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[float("Inf") for _ in range(vertices)] for _ in range(vertices)]
        self.dist = [-float("Inf")] * self.V  
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
        return stack[::-1]  

    def longest_path(self, src):
        stack = self.topological_sort()
        self.dist[src] = 0  

        while stack:
            u = stack.pop(0)

            
            if self.dist[u] != -float("Inf"):
                for v in range(self.V):
                    
                    if self.graph[u][v] != float("Inf"):
                        if self.dist[v] < self.dist[u] + self.graph[u][v]:
                            self.dist[v] = self.dist[u] + self.graph[u][v]
                            self.predecessor[v] = u

        self.print_distances()

    def print_distances(self):
        print("\nLongest distances from source:")
        for node in range(self.V):
            distance = self.dist[node] if self.dist[node] != -float("Inf") else "np path"
            print(f"node {node} : {distance}")

        print("\nprede essors : ", self.predecessor)

    def path(self, src, dst):
        if dst not in self.predecessor:
            return "no path "

        path = [dst]
        node = dst
        while node != src:
            path.append(self.predecessor[node])
            node = self.predecessor[node]
        path.reverse()
        return path

    def print_detailed_path(self, src, dst):
        
        path_nodes = self.path(src, dst)
        if path_nodes == "no path":
            return path_nodes

        detailed_path = []
        total_duration = 0
        for i in range(len(path_nodes) - 1):
            u = path_nodes[i]
            v = path_nodes[i + 1]
            weight = self.graph[u][v]
            total_duration += weight
            detailed_path.append(f"{u}->{v} : {weight}")

        path_description = f"path found: {{{', '.join(detailed_path)}}} => duration: {total_duration}"
        return path_description

if __name__ == "__main__":
    i = float("Inf")
    g = Graph(22)
    jobs = {
        0: {'duration': 41.0, 'dependencies': [1, 7, 9]},
        1: {'duration': 51.0, 'dependencies': [2]},
        2: {'duration': 50.0, 'dependencies': []},
        3: {'duration': 36.0, 'dependencies': []},
        4: {'duration': 38.0, 'dependencies': []},
        5: {'duration': 45.0, 'dependencies': []},
        6: {'duration': 21.0, 'dependencies': [3, 8]},
        7: {'duration': 32.0, 'dependencies': [3, 8]},
        8: {'duration': 32.0, 'dependencies': [2]},
        9: {'duration': 29.0, 'dependencies': [4, 6]}
    }

    
    source = 20
    sink = 21

    
    for job_id, attrs in jobs.items():
        begin = job_id * 2  
        end = job_id * 2 + 1  
        
        
        g.graph[begin][end] = attrs['duration']
        g.graph[source][begin] = 0
        g.graph[end][sink] = 0

        for dep in attrs['dependencies']:
            dep_end = dep * 2 + 1  
            g.graph[dep_end][begin] = 0  

    g.longest_path(source)

    longest_path_str = g.print_detailed_path(source, sink)
    print("\nLongest path:", longest_path_str)
