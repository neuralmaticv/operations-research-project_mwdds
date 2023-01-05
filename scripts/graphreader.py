""""
Funkcija koja se koristi za citanje grafa iz fajla
"""


def read_graph(instance_path, num_vertices):
    with open(instance_path, 'r') as f:
        # Citaj cvorove i tezine
        vertices = {}
        counter = 0

        for line in f:
            counter += 1
            vertex_id, vertex_weight = line.strip().split()
            vertices[int(vertex_id)] = int(vertex_weight)
            if counter == num_vertices:
                break

        # Citaj grane
        edges = []
        for line in f:
            fields = line.strip().split()
            source, target = fields
            edges.append((int(source), int(target)))

    return vertices, edges
