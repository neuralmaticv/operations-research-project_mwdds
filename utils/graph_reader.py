import re


def read_graph(instance_path):
    """Reads a graph from a file and returns vertices weights and edges.

    Args:
        instance_path (str): The path to the file containing the graph.

    Returns:
        A tuple containing a dictionary of vertices weights and a list of edges.
    """
    vertices_weights = {}
    edges = []

    match = re.search(r'instance_(\d+)_(\d+)', instance_path)
    
    if match:
        num_vertices = int(match.group(1))
        num_edges = int(match.group(2))
    else:
        raise ValueError("Path to instance file is not valid.")

    with open(instance_path, 'r') as f:
        lines = f.readlines()

    # Read and store vertices' weights
    for line in lines[:num_vertices]:
        weight = int(line.strip())
        vertices_weights[len(vertices_weights) + 1] = weight

    # Read and store edges
    for line in lines[num_vertices:num_vertices + num_edges]:
        source, target = map(int, line.strip().split())
        edges.append((source, target))

    return vertices_weights, edges

def read_graph_from_file(file_path):
    vertices_weight = {}
    edges = []
    vertice_index = 0

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            if line.isdigit():
                vertices_weight[vertice_index] = int(line)
                vertice_index += 1
            else:
                u, v = map(int, line.split())
                edges.append((u-1, v-1))

    return vertices_weight, edges

def read_graph_from_rakaj(file_path):
    vertices_weight = {}
    edges = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

        num_of_nodes = int(lines[1].strip())
        weights_line_index = lines.index("******************WEIGHTS*****************************\n")
        connections_line_index = lines.index("*****************CONNECTIONS****************\n")

        # Read vertex weights
        for i in range(weights_line_index + 1, weights_line_index + 1 + num_of_nodes):
            weight = int(lines[i].strip())
            vertices_weight[i - weights_line_index - 1] = weight

        # Read edge connections
        for i in range(connections_line_index + 1, connections_line_index + 1 + num_of_nodes):
            row = list(map(int, lines[i].split()))
            for v in range(len(row)):
                if row[v] == 1 and (i-connections_line_index -1 != v):
                    edge = (i - connections_line_index - 1, v)
                    edge_r = (v, i - connections_line_index - 1)
                    if edge not in edges and edge_r not in edges:
                        edges.append(edge)

    return vertices_weight, edges
