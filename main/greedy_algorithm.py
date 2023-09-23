import numpy as np


def greedy_mwdds(vertices_w:dict, edges:list, alpha:float=0.001) -> (set, int):
    """Find a greedy minimum weighted directed dominating set.

    Args:
        vertices_w (dict): A dictionary mapping vertices to their weights.
        edges (list): A list of edges in the graph.
        alpha (float, optional): A parameter that affects the cost calculation. Defaults to 0.001.

    Returns:
        A tuple containing the dominating set (set of vertices) and the total weight of the dominating set.
    """
    def _get_successors(u, vertices, edges):
        """Get the successors of a vertex in a graph.

        Args:
            u: The vertex for which to find the successors.
            vertices: A set of vertices in the graph.
            edges: A set of edges in the graph.

        Returns:
            A set of vertices that are successors of the given vertex.

        Note:
            This function assumes that the graph is represented as a set of vertices and a set of edges. The edges are represented as tuples of the form (u, v), where u and v are vertices in the graph.
        """
        successors = set()

        for v in vertices:
            if (u, v) in edges:
                successors.add(v)

        return successors
    
    domination_set = set()
    remaining_vertices = set(vertices_w.keys())

    while remaining_vertices:
        min_weight = float('inf')
        min_vertex = None

        for v in remaining_vertices:
            # calculate the cost for each vertex based on its weight and the number of successors
            cost = vertices_w[v] / (1 + alpha * len(_get_successors(v, remaining_vertices, edges)))

            if cost < min_weight:
                min_weight = cost
                min_vertex = v

        domination_set.add(min_vertex)

        # remove the vertex and its successors from the remaining vertices
        vertices_and_successors = _get_successors(min_vertex, remaining_vertices, edges)
        vertices_and_successors.add(min_vertex)
        remaining_vertices -= vertices_and_successors

    weight = sum(vertices_w[v] for v in domination_set)
    return domination_set, weight


"""
######################################################
Greedy algorithms for MWDS problem (just for reference)
######################################################
"""
# Reference: Vazirani, Vijay V. Approximation algorithms. Springer, 2001.
def greedy_mwds(vertices_w:dict, edges:list) -> (set, int):
    """Find the greedy minimum weighted dominating set.

    Args:
        vertices_w (dict): A dictionary mapping vertices to their weights.
        edges (list): A list of edges.

    Returns:
        A tuple containing the dominating set and the total weight of the vertices in the dominating set.
    """
    domination_set = set()

    # helper function for getting neighbours of a vertex
    def _get_neighbours(v, edges):
        """Calculate the neighbors of a vertex.

        Args:
            v: The vertex for which neighbors need to be calculated.
            edges: The list of edges in the graph.

        Returns:
            A set of neighbors of the vertex.

        Note:
            This function assumes that the graph is represented as a list of edges, where each edge is a tuple of two vertices.
        """
        neighbours = set()

        for edge in edges:
            if v in edge:
                neighbours.add(edge[0] if edge[0] != v else edge[1])

        return neighbours
    
    # calculate cost-effectiveness of adding a vertex to the dominating set
    # this fn uses the vertex weight divided by the size of the neighborhood thats not already covered by the dominating set
    def _cost(vertex_and_neighborhood):
        """Calculate the cost of a vertex and its neighborhood.

        Args:
            vertex_and_neighborhood: A tuple containing a vertex and its neighborhood.

        Returns:
            The cost of the vertex and its neighborhood.

        Note:
            The cost is calculated by dividing the weight of the vertex by the size of the neighborhood minus the domination set.
        """
        v, neighborhood = vertex_and_neighborhood
        return vertices_w[v] / len(neighborhood - domination_set)
    
    vertices = set(vertices_w.keys())
    # dictionary mapping each vertex to its closed neighborhood (vertex itself and its neighbors)
    neighborhoods = {v: {v} | _get_neighbours(v, edges) for v in list(vertices_w.keys())}

    # while there are still vertices left to cover
    while vertices:
        # choose the node with the lowest cost
        dom_vertex, min_set = min(neighborhoods.items(), key=_cost) 
        # print(dom_vertex, min_set)

        domination_set.add(dom_vertex)
        # remove the vertex from the neighborhoods
        del neighborhoods[dom_vertex]
        # print(neighborhoods)

        # remove vertices that are already covered by the dominating set
        vertices -= min_set

    return domination_set, sum(w for v, w in vertices_w.items() if v in domination_set)



# Reference: Ant Colony Optimization Applied to Minimum Weighted Dominating Set Problem
def greedy_mwds_aco(vertices_w:dict, edges:list) -> (set, int):
    """
    Color: White: Uncovered, Black: Dominating, Gray: Covered
    Return MWDS set, Gray set, and the total weights of MWDS
    :param vertices_w: Dictionary where keys are vertex IDs and values are vertex weights
    :param edges: List of edges as tuples (source, target)
    :return: mwds, gray_set, total_wt
    """
    vertices = list(vertices_w.keys())
    mwds = set()
    gray_set = set(vertices)
    white_set = set(vertices)
    wts_0 = np.array([vertices_w[vertex] for vertex in vertices])
    wts_1 = wts_0.copy() + 1e-6
    degrees = np.array([len([e for e in edges if e[0] == v]) for v in vertices])
    
    while len(white_set) > 0:
        covers = np.zeros(len(vertices))
        for i, v in enumerate(vertices):
            covers[i] = sum([wts_1[vertices.index(u)] for u, _ in edges if v == u])
        
        weights = wts_0 / (1 + covers)
        weights[list(mwds)] = np.Inf
        weights[np.logical_and(covers == 0, degrees > 0)] = np.Inf
        i = np.argmin(weights)
        
        mwds.add(vertices[i])
        gray_set.remove(vertices[i])
        nb_set = set([v for u, v in edges if u == vertices[i]]).intersection(white_set)
        gray_set = gray_set.union(nb_set)
        nb_set.add(vertices[i])
        white_set = white_set - nb_set - mwds
        wts_1[list(map(vertices.index, list(nb_set)))] = 0
    
    total_ws = sum([vertices_w[vertex] for vertex in mwds])

    return mwds, total_ws
