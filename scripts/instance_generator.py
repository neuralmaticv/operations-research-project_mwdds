import random

"""
Skripta za generisanje instanci.
Cvorovi se upisuju u fajl u formatu: vertex_id vertex_weight
Grane se u fajl upisuju u formatu: source_vertex target_vertex
"""


def generate_random_weighted_graph(num_vertices, num_instances):
    if num_vertices <= 100:
        dim = "0"
    elif 100 < num_vertices < 1000:
        dim = "1"
    else:
        dim = "2"

    for k in range(num_instances):
        # Generisi listu cvorova sa random tezinom
        vertices = [(i, random.randint(10, 100)) for i in range(num_vertices)]

        # Lista za cuvanje grana
        edges = []

        # Generisanje random grana izmedju cvorova
        # TODO: smanjiti vjerovatnocu za dodavanje grane?
        for i in range(num_vertices):
            for j in range(num_vertices):
                if i != j and random.random() < 0.5:
                    edges.append((i, j))

        # Upis informacija u fajl i cuvanje u odgovarajucem folderu u zavisnosti od dimenzije grafa
        with open('./instances/level' + dim + '/instance' + str(k) + '.txt', 'w') as f:
            for v in vertices:
                f.write(f"{v[0]} {v[1]}\n")

            for e in edges:
                f.write(f"{e[0]} {e[1]}\n")


if __name__ == '__main__':
    generate_random_weighted_graph(1000, 10)
    print("Generisanje je zavrseno.")
