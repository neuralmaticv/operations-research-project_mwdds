"""
Inicijalizujemo prazan skup za dominirajuce cvorove
Sortiramo sve cvorove u opadajucem poretku na osnovu tezine
Prolazimo kroz sve cvorove:
    Ako je svaki cvor, koji je dostizan iz i, dostizan iz cvora koji je u dominirajucem skupu, preskoci taj cvor.
    U suprotnom, dodaj cvor i u dominirajuci skup
Vrati informacije o dominirajucem skupu i tezini cvorova
"""


def greedy_solver(vertices, edges):
    # dominirajuci skup
    domination_set = []

    # sortiranje cvorova po tezini, u neopadajucem poretku
    nodes = sorted(vertices, key=lambda x: vertices[x])

    # "pomocni skup" za pracenje preostalih cvorova
    remaining_vertices = set(nodes)

    while remaining_vertices:
        min_weight = float('inf')
        min_vertex = None

        # Biramo cvor sa minimalnom tezinom
        for v in remaining_vertices:
            if vertices[v] < min_weight:
                min_weight = vertices[v]
                min_vertex = v

        # Dodajemo odabrani cvor u dominirajuci skup
        domination_set.append(min_vertex)

        # Uklanjamo odabrani cvor i njegove susjede iz preostalih cvorova
        remaining_vertices = remove_vertices(min_vertex, remaining_vertices, get_successors(min_vertex, remaining_vertices, edges))

    weight = sum(value for key, value in vertices.items() if key in domination_set)
    return domination_set, weight


# Funkcija koja vraca susjede cvoa u
def get_successors(u, vertices, edges):
    successors = []

    for v in vertices:
        if (u, v) in edges:
            successors.append(v)

    return successors


# Funkcija koja uklanja susjedne cvorove cvora u
# Implementirana su dva nacina zbog razlicitih ulaznih podataka
def remove_vertices(u, vertices, successors):
    if isinstance(vertices, dict):
        for v in successors:
            vertices.pop(v)
        vertices.pop(u)
    else:
        for v in successors:
            vertices.remove(v)
        vertices.remove(u)

    return vertices
