import random
from time import *

class Individual:
    def __init__(self, chromosome_length):
        self.chromosome = [random.randint(0, 1) for _ in range(chromosome_length)]
        self.chromosome[random.randint(0, chromosome_length - 1)] = 1
        self.fitness = 0

    def calculate_fitness(self, vertices_w, edges):
        total_weight = 0
        max_weight = 0

        for i, vertex in enumerate(self.chromosome):
            max_weight += vertices_w[i]

            if vertex == 1:
                total_weight += vertices_w[i]

        for i, vertex in enumerate(self.chromosome):
            if vertex == 0:
                outgoing_edges = [edge for edge in edges if edge[0] == i]
                for edge in outgoing_edges:
                    if self.chromosome[1] == 1:
                        break
                else:
                    total_weight = max_weight
                    break

        if total_weight == max_weight:
            self.fitness = max_weight, -1
        else:
            self.fitness = total_weight, self.chromosome.count(1)

        return self.fitness

    def single_pooint_crossover(self, other):
        crossover_point = random.randint(1, len(self.chromosome) - 1)

        child1 = Individual(len(self.chromosome))
        child2 = Individual(len(self.chromosome))

        child1.chromosome = self.chromosome[:crossover_point] + other.chromosome[crossover_point:]
        child2.chromosome = other.chromosome[:crossover_point] + self.chromosome[crossover_point:]

        return child1, child2

    def mutation(self, mutation_rate):
         for i in range(len(self.chromosome)):
            if random.uniform(0, 1) < mutation_rate:
                #print("Mutation: ", self.chromosome)
                # Flip the value of the i-th gene
                self.chromosome[i] = int(not self.chromosome[i])
                #print("--------> ", self.chromosome)

         return self

    def __str__(self):
        return f'[Chromosome: {self.chromosome}, Fitness: W={self.fitness[0]}, Ds={self.fitness[1]}]\n'

    def __repr__(self):
        return self.__str__()



class Population:
    def __init__(self, population_size, chromosome_length):
        self.individuals = [Individual(chromosome_length) for _ in range(population_size)]

    def calculate_fitness(self, vertices_w, edges):
        for individual in self.individuals:
            individual.calculate_fitness(vertices_w, edges)

    def selection(self, method, n_selected):
        if method == 'roulette_wheel':
            total_fitness = sum(individual.fitness[0] for individual in self.individuals)
            pick = random.uniform(0, total_fitness)
            current = 0

            for individual in self.individuals:
                current += individual.fitness[0]
                if current > pick:
                    return individual
        elif method == 'tournament':
            selected = random.sample(self.individuals, n_selected)
            return min(selected, key=lambda x: (x.fitness[0], -x.fitness[1]))



class GeneticAlgorithm:
    def __init__(self, vertices_w, edges, population_size, chromosome_length, selection_method, crossover_rate, mutation_rate, n_generations, max_time, logger=None):
        self.vertices_w = vertices_w
        self.edges = edges
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.selection_method = selection_method
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.n_generations = n_generations
        self.population = Population(self.population_size, self.chromosome_length)
        self.max_time = max_time
        if logger == None:
            self.logger = False
        else:
            self.logger = logger

    def filter_result(self, new_population):
        filtered_individuals = []

        for individual in new_population.individuals:
            is_valid = True

            if individual.fitness[0] <= 0:
                is_valid = False

            for i in range(len(self.vertices_w)):
                if individual.fitness[0] == self.vertices_w[i]:
                    is_valid = False

            if is_valid:
                filtered_individuals.append(individual)

        return filtered_individuals

    def run(self):
        for individual in self.population.individuals:
            individual.calculate_fitness(self.vertices_w, self.edges)

        if self.logger:
            print("INITIAL:")
            print(self.population.individuals)

        # run
        start_time = time()
        while self.n_generations > 0:
            # selection
            if self.selection_method == "roulette_wheel":
                selected = [self.population.selection(self.selection_method, 0) for _ in range(self.population_size)]
            else:
                selected = [self.population.selection(self.selection_method, 3) for _ in range(self.population_size)]

            if self.logger:
                print("selected:", selected)

            new_population = Population(self.population_size, self.chromosome_length)
            new_population.individuals = []

            if self.logger:
                print("New population -> ", len(new_population.individuals))
                print(new_population.individuals)

            # crossover
            for i in range(0, self.population_size, 2):
                if  random.uniform(0, 1) < self.crossover_rate:
                    child1, child2 = selected[i].single_pooint_crossover(selected[i+1])
                else:
                    child1, child2 = selected[i], selected[i+1]

                new_population.individuals.append(child1)
                new_population.individuals.append(child2)

            # mutation
            new_population.individuals = [individual.mutation(self.mutation_rate) for individual in new_population.individuals]

            # za svaku jedinku izracunaj fitness f
            for individual in new_population.individuals:
                individual.calculate_fitness(self.vertices_w, self.edges)

            if self.logger:
                print(new_population.individuals)


            # provjeri da li je isteklo definisano vrijeme za izvrsavanje
            elapsed_time = time() - start_time
            if elapsed_time > self.max_time:
                filtered_individuals = self.filter_result(new_population)
                return min(filtered_individuals, key=lambda x: (x.fitness[0], -x.fitness[1]))

            self.n_generations -= 1


        filtered_individuals = self.filter_result(new_population)
        return min(filtered_individuals, key=lambda x: (x.fitness[0], -x.fitness[1]))
