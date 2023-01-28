# prikazivanje grafa i dominirajuceg skupa
import matplotlib.pyplot as plt
import networkx as nx


def plot_graph(vertices_w, edges, dominating_set, instance_info):
    graph = nx.DiGraph(edges)
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

    labels = {
        n: str(n) + '\nw=' + str(graph.nodes[n]['weight'])
        for n in graph.nodes
    }
    options = {"edgecolors": "tab:gray", "node_size": 1500, "alpha": 0.8}
    nx.draw(graph, node_color=color_map, labels=labels, with_labels=True, **options)

    if instance_info != "":
        plt.savefig("../instances/imgs/new_" + instance_info + ".png", format="PNG")
    plt.show()
