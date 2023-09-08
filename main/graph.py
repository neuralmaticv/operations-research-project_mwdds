class Vertex:
    def __init__(self, id, weight):
        self.id = id
        self.weight = weight
        self.successors = []
        self.predecessors = []
        self.in_degree = 0
        self.out_degree = 0

    def add_successor(self, successor):
        self.successors.append(successor)
        self.out_degree += 1

    def add_predecessor(self, predecessor):
        self.predecessors.append(predecessor)
        self.in_degree += 1

    def __repr__(self) -> str:
        return f"Vertex(id={self.id}, weight={self.weight}, in_degree={self.in_degree}, out_degree={self.out_degree})"
    
    def __str__(self) -> str:
        return self.__repr__()
    

class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.source_vertices = []

    def create_from_data(self, vertices_weights, edges):
        for vertex_id, weight in vertices_weights.items():
            self.vertices.append(Vertex(vertex_id, weight))

        for edge in edges:
            source, target = edge
            source_vertex = self.get_vertex_by_id(source)
            target_vertex = self.get_vertex_by_id(target)

            if source_vertex and target_vertex:
                source_vertex.add_successor(target_vertex)
                target_vertex.add_predecessor(source_vertex)
                self.edges.append(edge)

        for vertex in self.vertices:
            if vertex.in_degree == 0:
                self.source_vertices.append(vertex)

    def get_vertex_by_id(self, vertex_id):
        for vertex in self.vertices:
            if vertex.id == vertex_id:
                return vertex
        return None
    
    def __repr__(self) -> str:
        return f"Graph(vertices={self.vertices}, edges={self.edges})"
    
    def __str__(self) -> str:
        return self.__repr__()
    