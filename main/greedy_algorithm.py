
# Reference: Vazirani, Vijay V. Approximation algorithms. Springer, 2001.
def greedy_mwds(vertices_w:dict, edges:list) -> (set, int):
    domination_set = set()

    # helper function for getting neighbours of a vertex
    def _get_neighbours(v, edges):
        neighbours = set()

        for edge in edges:
            if v in edge:
                neighbours.add(edge[0] if edge[0] != v else edge[1])

        return neighbours
    
    # calculate cost-effectiveness of adding a vertex to the dominating set
    # this fn uses the vertex weight divided by the size of the neighborhood thats not already covered by the dominating set
    def _cost(vertex_and_neighborhood):
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
        #print(neighborhoods)

        # remove vertices that are already covered by the dominating set
        vertices -= min_set

    return domination_set, sum(w for v, w in vertices_w.items() if v in domination_set)
