from pulp import *

def ilp_solver(vertices_w, edges):
    vertices = list(vertices_w.keys())

    model = LpProblem("Minimum Weighted Directed Domination Set", LpMinimize)

    # definisemo varijable za cvorove u grafu
    x = LpVariable.dicts("x", vertices, lowBound=0, upBound=1, cat=LpInteger)

    # dodajemo funkciju cilja
    model += lpSum([vertices_w[i] * x[i] for i in vertices])

    # dodajemo ogranicenja
    # Svaki cvor mora biti u podskupu ili imati vezu sa nekim cvorom iz tog podskupa
    for v in vertices:
        constraint = x[v]
        for e in edges:
            if e[1] == v:
                constraint += x[e[0]]
        model += constraint >= 1


    # pokrecemo model, sa ogranicenjem na 10 minuta
    time_limit_s = 600
    model.solve(PULP_CBC_CMD(msg=0, maxSeconds=time_limit_s))

    # kreiramo dominirajuci skup
    domination_set = []
    for i in vertices:
      if x[i].value() == 1:
        domination_set.append(i)

    objective_value = value(model.objective)

    # vracamo dominirajuci skup i tezinu
    return domination_set, objective_value
