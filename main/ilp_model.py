from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, lpSum, value, PULP_CBC_CMD
from math import ceil

def ilp_mwdds(vertices_w:dict, edges:list) -> (set, int):
    """Solve the Minimum Weighted Directed Domination Set problem using the ILP solver.

    Args:
        vertices_w: A dictionary of vertices and their weights.
        edges: A list of edges.

    Returns:
        A tuple of the domination set and the objective value.

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """
    vertices = list(vertices_w.keys())

    model = LpProblem("mwdds", LpMinimize)

    x = LpVariable.dicts("x", vertices, lowBound=0, upBound=1, cat=LpInteger)

    z = {}
    for vi in vertices:
        out_degree = sum(1 for (i, j) in edges if i == vi)
        z[vi] = 1 + out_degree

    Z = set(z.values())

    model += lpSum(vertices_w[vi] * x[vi] for vi in vertices)

    for vi in vertices:
        model += x[vi] + lpSum(x[vj] for vj in vertices if (vj, vi) in edges) >= 1

    for q in Z:
        model += lpSum(ceil(z[vi] / q) * x[vi] for vi in vertices) >= ceil(len(vertices) / q)
    
    time_limit_s = 600
    model.solve(PULP_CBC_CMD(msg=False, timeLimit=time_limit_s))

    domination_set = set()
    for i in vertices:
        if x[i].value() == 1:
            domination_set.add(i)

    objective_value = value(model.objective)
    return domination_set, int(objective_value)
