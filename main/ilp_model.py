from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, lpSum, value, PULP_CBC_CMD
from math import ceil

"""
Reference: 
Nakkala, Mallikarjun Rao, Alok Singh, André Rossi. 
"Swarm intelligence, exact and matheuristic approaches for minimum weight directed dominating set problem."
Engineering Applications of Artificial Intelligence, Volume 109, 2022.
"""
def ilp_mwdds(vertices_w:dict, edges:list) -> (set, int):
    """Solve the Minimum Weighted Directed Domination Set problem using the ILP solver.

    Args:
        vertices_w: A dictionary of vertices and their weights.
        edges: A list of edges.

    Returns:
        A tuple of the domination set and the objective value.
    """
    vertices = list(vertices_w.keys())

    model = LpProblem("mwdds", LpMinimize)

    x = LpVariable.dicts("x", vertices, lowBound=0, upBound=1, cat=LpInteger)

    # z(vi) = 1 + out_degree(vi) -  max number of vertices that can be dominated by vertex vi
    z = {}
    for vi in vertices:
        out_degree = sum(1 for (i, j) in edges if i == vi)
        z[vi] = 1 + out_degree

    # Z = {z(vi) | vi in V} - set of all z(vi)
    Z = set(z.values())

    # objective function - minimize the total weight of the domination set
    model += lpSum(vertices_w[vi] * x[vi] for vi in vertices)

    # constraints - each vertex must be dominated by at least one vertex in the domination set 
    for vi in vertices:
        model += x[vi] + lpSum(x[vj] for vj in vertices if (vj, vi) in edges) >= 1

    # strengthen the constraints by adding the following constraints
    # upper bound on the number of vertices that can be dominated by vertex
    for q in Z:
        model += lpSum(ceil(z[vi] / q) * x[vi] for vi in vertices) >= ceil(len(vertices) / q)
    
    time_limit_s = 600
    model.solve(PULP_CBC_CMD(msg=False, timeLimit=time_limit_s))

    # get the domination set
    domination_set = set()
    for i in vertices:
        if x[i].value() == 1:
            domination_set.add(i)

    # get the objective value
    objective_value = value(model.objective)
    
    return domination_set, int(objective_value)
