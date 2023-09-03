
# Reference: Vazirani, Vijay V. Approximation algorithms. Springer, 2001.
def greedy_mwds(vertices_w:dict, edges:list) -> (set, int):
    """Find the greedy minimum weighted dominating set.

    Args:
        vertices_w (dict): A dictionary mapping vertices to their weights.
        edges (list): A list of edges.

    Returns:
        A tuple containing the dominating set and the total weight of the vertices in the dominating set.

    Note:
        The dominating set is a set of vertices such that every vertex in the graph is either in the set
        or adjacent to a vertex in the set. The minimum weight dominating set is the dominating set with
        the minimum total weight.
    
    !!! note

    The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
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

        ---

        Calculate the cost-effectiveness of adding a vertex to the dominating set.

        Args:
            vertex_weight: The weight of the vertex.
            neighborhood_size: The size of the neighborhood that is not already covered by the dominating set.

        Returns:
            The cost-effectiveness of adding the vertex to the dominating set.
        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
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
        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
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
