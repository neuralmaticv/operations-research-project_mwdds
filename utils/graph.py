import logging
logger = logging.getLogger("main")

class Vertex:
    def __init__(self, id, weight, color=0):
        self.id = id
        self.weight = weight
        self.successors = []
        self.predecessors = []
        self.in_degree = 0
        self.out_degree = 0
        self.color = color # 0 - white, 1 - gray, 2 - black

    def add_successor(self, successor):
        self.successors.append(successor)
        self.out_degree += 1

    def add_predecessor(self, predecessor):
        self.predecessors.append(predecessor)
        self.in_degree += 1

    def __repr__(self) -> str:
        return f"V(id={self.id}, w={self.weight}, in_d={self.in_degree}, out_d={self.out_degree}, color={self.color})"
    
    def __str__(self) -> str:
        return self.__repr__()
    

class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.source_vertices = []
        self.white_vertices = []
        self.gray_vertices = []
        self.black_vertices = []
        self.total_weight = 0

    def create_from_data(self, vertices_weights, edges):
        for vertex_id, weight in vertices_weights.items():
            v = Vertex(vertex_id, weight)
            self.vertices.append(v)
            self.white_vertices.append(v)
            self.total_weight += weight

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
                self.white_vertices.remove(vertex)
                vertex.color = 2 # source vertices are included - black
                self.black_vertices.append(vertex)
                for successor in vertex.successors:
                    if successor.color == 0:
                        self.white_vertices.remove(successor)
                        successor.color = 1
                        self.gray_vertices.append(successor)
                    
    def color_vertex(self, vertex, color):
        if vertex.color == 0:
            if color == 1:
                self.white_vertices.remove(vertex)
                vertex.color = color
                self.gray_vertices.append(vertex)
                # logger.info(f"vertex {vertex.id}: w -> g")
            elif color == 2:
                self.white_vertices.remove(vertex)
                vertex.color = color
                self.black_vertices.append(vertex)
                for successor in vertex.successors:
                    if successor.color == 0:
                        self.color_vertex(successor, 1)
                # logger.info(f"vertex {vertex.id}: w -> b")
        elif vertex.color == 1:
            if color == 2:
                self.gray_vertices.remove(vertex)
                vertex.color = color
                self.black_vertices.append(vertex)
                for successor in vertex.successors:
                    if successor.color == 0:
                        self.color_vertex(successor, 1)
                # logger.info(f"vertex {vertex.id}: g -> b")
        
        if len(self.vertices) != (len(self.black_vertices) + len(self.gray_vertices) + len(self.white_vertices)):
            logger.error("Number of vertices is not equal to the sum of colored vertices")
            raise Exception("Number of vertices is not equal to the sum of colored vertices")

                
    def get_vertex_by_id(self, vertex_id):
        for vertex in self.vertices:
            if vertex.id == vertex_id:
                return vertex
        return None
    
    def reset_colors(self):
        self.white_vertices = self.vertices.copy()
        self.gray_vertices = []
        self.black_vertices = []
        for vertex in self.vertices:
            vertex.color = 0
        
        # for vertex in self.source_vertices:
        #     self.color_vertex(vertex, 2)
    
    def __repr__(self) -> str:
        return f"Graph(vertices={self.vertices}, edges={self.edges})"
    
    def __str__(self) -> str:
        return self.__repr__()
