import json

class Graph:
    def __init__(self, json_data):
        self.nodes = list(json_data["nodes"].keys())  
        self.graph = json_data["nodes"] 
    
    def adjacency_matrix(self):
        n = len(self.nodes)
        matrix = [[0] * n for _ in range(n)] 
        for i, node in enumerate(self.nodes):
            for _ in self.graph[node]:
                j = self.nodes.index(_)  
                matrix[i][j] = 1
        return matrix
    
    def print_adjacency_matrix(self):
        matrix = self.adjacency_matrix()
        print("  ", " ".join(self.nodes))  
        for i, row in enumerate(matrix):
            print(f"{self.nodes[i]}: {' '.join(map(str, row))}")

json_string = '''
{
    "nodes": {
        "1": ["2"],
        "2": ["3", "4"],
        "3": ["5"],
        "4": [],
        "5": []
    }
}
'''

if __name__ == '__main__':
           
    json_data = json.loads(json_string)
    graph = Graph(json_data)
    graph.print_adjacency_matrix()
