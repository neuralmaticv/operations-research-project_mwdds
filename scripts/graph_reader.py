""""
Funkcija koja se koristi za citanje/generisanje grafa
"""
from main.greedy_algorithm import get_successors
import networkx as nx
import random


def read_graph(instance_path, gen_by_instance):
    edges = []
    with open(instance_path, 'r') as f:
        for line in f:
            fields = line.strip().split()
            source, target = fields
            edges.append((int(source), int(target)))

    for i in range(len(edges)):
        edges[i] = (edges[i][0] - 1, edges[i][1] - 1)

    graph = nx.Graph(edges)

    if gen_by_instance:
        if instance_path.__contains__(500) or instance_path.__contains__(400):
            weights = [random.randint(1, (1 + len(get_successors(i, graph.nodes, edges))) ** 2) for i in
                       range(len(graph.nodes))]
        else:
            weights = [random.randint(20, 70) for _ in range(len(graph.nodes))]
    else:
        weights = [random.randint(20, 70) for _ in range(len(graph.nodes))]

    vertices_w = dict(zip(graph.nodes, weights))

    return vertices_w, edges
