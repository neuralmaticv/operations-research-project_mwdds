import matplotlib.pyplot as plt
import networkx as nx


def plot_graph(vertices_w: dict, edges: list, dominating_set: set=None, instance_info: str = "", digraph: bool = False):
    """Plot a graph

    Args:
        vertices_w: A dictionary of vertices weights
        edges: A list of edges
        dominating_set: A list of vertices in the dominating set
        instance_info: A string with the instance information
    """
    plt.rcParams["figure.figsize"] = [10, 8]
    plt.rcParams["figure.autolayout"] = True

    if digraph:
        graph = nx.DiGraph(edges)
        edges_options = {"arrows": True, "arrowstyle": "->", "arrowsize": 15, "node_size": 1500}
    else:
        graph = nx.Graph(edges)
        edges_options = {"arrows": True, "node_size": 1500}

    pos = nx.nx_pydot.graphviz_layout(graph, prog="neato")
    color_map = []

    for node in graph.nodes:
        if not dominating_set:
            color_map.append('blue')
        else:
            if node in dominating_set:
                color_map.append('red')
            else:
                color_map.append('blue')

        graph.nodes[node]["weight"] = vertices_w[node]

    nodes_options = {"edgecolors": "tab:gray", "node_size": 1500, "alpha": 0.8}
    nx.draw_networkx_nodes(graph, pos, node_color=color_map, **nodes_options)
    nx.draw_networkx_edges(graph, pos, edgelist=edges, width=2, **edges_options)

    labels = {
        n: str(n) + '\nw' + str(graph.nodes[n]['weight'])
        for n in graph.nodes
    }
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=14, font_color='white')

    if instance_info != "":
        plt.savefig("../instances/imgs/new_" + instance_info + ".png", format="PNG")
        
    plt.show()
