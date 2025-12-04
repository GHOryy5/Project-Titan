from collections import deque

class GraphEngine:
    def __init__(self):
        self.adj_list = {}
        
    def add_connection(self, u, v, weight=1.0):
        if u not in self.adj_list: self.adj_list[u] = []
        if v not in self.adj_list: self.adj_list[v] = []
        self.adj_list[u].append((v, weight))
        self.adj_list[v].append((u, weight)) # Undirected
        
    def find_path(self, start, end):
        # BFS Shortest Path
        queue = deque([(start, [start])])
        visited = set()
        while queue:
            node, path = queue.popleft()
            if node == end: return path
            visited.add(node)
            for neighbor, _ in self.adj_list.get(node, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        return None
