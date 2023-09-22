import random
import time
import logging


# Define the functions for calculating scores
def sum_of_white_successors(vertex):
    # EQ1: Calculate Ws(u)
    sum = 0
    for successor in vertex.successors:
        if successor.color == 0:
            sum += successor.weight
    return sum

def clr_vertex(vertex):
    # EQ2: Calculate CLR(u)
    if vertex.color == 0:
        return 1
    return 0

def wout_degree(vertex):
    # EQ4: Calculate WOUTdeg(u)
    sum = 0
    for successor in vertex.successors:
        if successor.color == 0:
            sum += 1
    return sum

def score(vertex):
    # EQ2: Calculate score(u)
    return sum_of_white_successors(vertex) + (vertex.weight * clr_vertex(vertex)) / vertex.weight

def score_tie(vertex):
    # EQ5: Calculate scoreTie(u)
    return wout_degree(vertex) + clr_vertex(vertex) / vertex.weight

def repair(graph, individual, initial=False):
    graph.reset_colors()

    # Step 1: Add all source vertices to the solution
    for source_vertex in graph.source_vertices:
        individual.chromosome[source_vertex.id - 1] = 1
        graph.color_vertex(source_vertex, 2)

    while len(graph.white_vertices) > 0:
        scores = []

        # Step 2: Compute score(u) for all vertices not in the solution
        for vertex in graph.white_vertices:
            scores.append((vertex, score(vertex)))

        # Step 3: Select vertex with the highest score
        max_score = max(scores, key=lambda x: x[1])[1]
        max_score_vertices = [v for v, s in scores if s == max_score]

        if initial:
            # In case of multiple vertices with the same score, select one by EQ6
            max_score_vertex = max(max_score_vertices, key=lambda x: score_tie(x))
        else:
            # In case of multiple vertices with the same score, select one randomly
            max_score_vertex = random.choice(max_score_vertices)

        # Update the individual and color the selected vertex
        individual.chromosome[max_score_vertex.id - 1] = 1
        graph.color_vertex(max_score_vertex, 2)

    return individual

def redundant_removal(graph, individual):
    # goal is to remove redundant vertices from the solution. node v is redundant if:
    # sd without v remains directed dominating set

    # we iteratively compute set of redundant nodes and remove all nodes belonging to this set from Sd

    # Step 1: Add all source vertices to the solution
    for source_vertex in graph.source_vertices:
        graph.color_vertex(source_vertex, 2)
    
    # Step 2: Compute set of redundant vertices
    redundant_vertices = []
    for vertex in graph.vertices:
        if vertex.color == 2:
            graph.color_vertex(vertex, 0)
            individual.chromosome[vertex.id - 1] = 0

            # if Sd is valid without v, then v is redundant
            if is_valid(graph, individual):
                redundant_vertices.append(vertex)

            graph.color_vertex(vertex, 2)
            individual.chromosome[vertex.id - 1] = 1
    
    # Step 3: Remove redundant vertices from the solution
    for vertex in redundant_vertices:
        graph.color_vertex(vertex, 0)
        individual.chromosome[vertex.id - 1] = 0

    
    individual = repair(graph, individual)

    return individual


def is_valid(graph, individual):
    graph.reset_colors()

    for i in range(len(individual.chromosome)):
        if individual.chromosome[i] == 1:
            graph.color_vertex(graph.vertices[i], 2)

    # Check if all white vertices are colored
    if len(graph.white_vertices) == 0:
        return True

    return False



class Individual:
    def __init__(self, init=None, chromosome_length=0):
        if init is None:
            self.chromosome = [0] * chromosome_length
            self.chromosome_length = 0
            self.fitness = 0
        else:
            self.chromosome = init
            self.chromosome_length = len(init)
            self.fitness = 0

    def mutate(self):
        for i in range(len(self.chromosome)):
            if random.random() < 0.5:
                self.chromosome[i] = 1 - self.chromosome[i]
                
        return self
    
    def get_uniqe_ids(self):
        idx1 = random.randint(0, len(self.chromosome) - 1)
        idx2 = random.randint(0, len(self.chromosome) - 1)

        while idx1 == idx2:
            idx2 = random.randint(0, len(self.chromosome) - 1)
        
        return idx1, idx2

    def __str__(self):
        return f"Chromosome: {self.chromosome}\nFitness: {self.fitness}"

    def __repr__(self):
        return self.__str__()
    
    def fitness_func(self, graph, initial=False):
        if is_valid(graph, self):
            self = redundant_removal(graph, self)
            self.fitness = sum([graph.vertices[i].weight for i, _ in enumerate(self.chromosome) if self.chromosome[i] == 1])
        else:
            self = repair(graph, self, initial)
            self.fitness = sum([graph.vertices[i].weight for i, _ in enumerate(self.chromosome) if self.chromosome[i] == 1])


class Population:    
    def __init__(self, graph, population_size):
        self.population_size = population_size
        self.normalized_proportions = None
        self.graph = graph
        self.source_vertices = [vertex.id - 1 for vertex in graph.source_vertices] # vertices with in-degree 0
        self.individuals = self._initialize_population()

    def get_sorted_individuals(self, first_n=0):
        if first_n > 0 and first_n < len(self.individuals):
            return sorted(self.individuals, key=lambda individual: individual.fitness)[:first_n]

        return sorted(self.individuals, key=lambda individual: individual.fitness)

    def _gen_by_source_vertices(self, max_number):
        chromosome_length = len(self.graph.vertices)
        population = []

        for _ in range(max_number):
            individual = [0] * chromosome_length

            for i in range(chromosome_length):
                if i in self.source_vertices:
                    individual[i] = 1
                else:
                    individual[i] = random.randint(0, 1)
            
            individual = Individual(init=individual)
            population.append(individual)
        
        return population
    
    def _gen_random(self, max_number):
        chromosome_length = len(self.graph.vertices)
        population = []

        for _ in range(max_number):
            individual = [0] * chromosome_length

            for i in range(chromosome_length):
                if i not in self.source_vertices:
                    individual[i] = random.randint(0, 1)
            
            individual = Individual(init=individual)
            population.append(individual)
        
        return population
    
    def _gen_by_highest_degree_vertices(self, max_number):
        chromosome_length = len(self.graph.vertices)
        population = []

        for _ in range(max_number):
            individual = [0] * chromosome_length

            for i in range(chromosome_length):
                if self.graph.vertices[i].in_degree > 2 and self.graph.vertices[i].out_degree > 2:
                    individual[i] = 1
                elif i not in self.source_vertices:
                    individual[i] = random.randint(0, 1)
            
            individual = Individual(init=individual)
            population.append(individual)
        
        return population

    def _initialize_population(self):
        chromosome_length = len(self.graph.vertices)
        population = []

        # generate individuals with source vertices
        max_source_individuals = int(self.population_size * 0.9)
        population += self._gen_by_source_vertices(max_source_individuals)

        # generate random individuals
        max_random_individuals = self.population_size - max_source_individuals
        population += self._gen_random(max_random_individuals)

        # generate individuals with highest degree vertices
        # max_highest_degree_individuals = self.population_size - max_source_individuals - max_random_individuals
        # population += self._gen_by_highest_degree_vertices(max_highest_degree_individuals)

        for individual in population:
            individual.fitness_func(self.graph, initial=True)
    
        return population

    def _calc_normalized_proportions(self):
        all_fitnesses = [individual.fitness for individual in self.individuals]
        sum_fitnesses = sum(all_fitnesses)

        # lower fitness -> higher probability of selection
        inverse_proportions = [sum_fitnesses / fitness for fitness in all_fitnesses]

        # Normalize the proportions
        proportions_sum = sum(inverse_proportions)
        normalized_proportions = [proportion / proportions_sum for proportion in inverse_proportions]
        
        self.normalized_proportions = normalized_proportions

    def selection(self, method='tournament', tournament_size=2):
        if method == 'roulette_wheel':
            total = 0.0
            best_individual = min(self.individuals, key=lambda individual: individual.fitness)
            cumulative_proportions = []

            for proportion in self.normalized_proportions:
                total += proportion
                cumulative_proportions.append(total)
                
            selected_value = random.uniform(0, 1)            
            for i, proportion in enumerate(cumulative_proportions):
                if proportion >= selected_value:
                    return self.individuals[i]
            
            # If we didn't find an individual, return the best one
            return best_individual
        elif method == 'tournament':
            # select random sample of individuals and return the best one
            tournament_individuals = random.sample(self.individuals, tournament_size)

            # ensure that selected individuals are different
            while len(set(tournament_individuals)) != len(tournament_individuals):
                tournament_individuals = random.sample(self.individuals, tournament_size)

            # Select the better of the k individuals
            return min(tournament_individuals, key=lambda individual: individual.fitness)

    def single_point_crossover(self, individual1, individual2, mutation_probability=0.05):
        crossover_point = random.randint(1, len(individual1.chromosome) - 1)

        child1 = Individual(chromosome_length=len(individual1.chromosome))
        child2 = Individual(chromosome_length=len(individual1.chromosome))

        child1.chromosome = individual1.chromosome[:crossover_point] + individual2.chromosome[crossover_point:]
        child2.chromosome = individual2.chromosome[:crossover_point] + individual1.chromosome[crossover_point:]

        # mutation of childrens
        child1, child2 = self.mutation(child1, child2, mutation_probability)

        # ensure that results are valid/feasible (source vertices are selected)
        for i in range(len(child1.chromosome)):
            if i in self.source_vertices:
                child1.chromosome[i] = 1
                child2.chromosome[i] = 1
            
        child1.fitness_func(self.graph)
        child2.fitness_func(self.graph)        
        
        return child1, child2
    
    def two_point_crossover(self, individual1, individual2, mutation_probability=0.05):
        crossover_point1 = random.randint(1, len(individual1.chromosome) // 2)
        crossover_point2 = random.randint(len(individual1.chromosome) // 2, len(individual1.chromosome) - 1)

        child1 = Individual(chromosome_length=len(individual1.chromosome))
        child2 = Individual(chromosome_length=len(individual1.chromosome))

        child1.chromosome = individual1.chromosome[:crossover_point1] + individual2.chromosome[crossover_point1:crossover_point2] + individual1.chromosome[crossover_point2:]
        child2.chromosome = individual2.chromosome[:crossover_point1] + individual1.chromosome[crossover_point1:crossover_point2] + individual2.chromosome[crossover_point2:]

        # mutation of childrens
        child1, child2 = self.mutation(child1, child2, mutation_probability)

        # ensure that results are valid/feasible (source vertices are selected)
        for i in range(len(child1.chromosome)):
            if i in self.source_vertices:
                child1.chromosome[i] = 1
                child2.chromosome[i] = 1

        child1.fitness_func(self.graph)
        child2.fitness_func(self.graph)

        return child1, child2        

    
    def mutation(self, child1, child2, mutation_probability):
        new_child1 = Individual(init=child1.chromosome)
        new_child2 = Individual(init=child2.chromosome)

        if random.uniform(0, 1) < mutation_probability:
            new_child1 = child1.mutate()
        
        if random.uniform(0, 1) < mutation_probability:
            new_child2 = child2.mutate()
        
        return new_child1, new_child2


class GeneticAlgorithm:
    def __init__(self, graph, max_time=600, max_no_improvement=None, **kwargs):
        self.graph = graph
        self.max_time = max_time
        self.fitness_over_time = []
        self.max_no_improvement = max_no_improvement
        self.gen_counter = 0
        self.no_improvement_counter = 0
        self.previous_best_fitness = graph.total_weight
        self.running_time = 0
        
        # Update class attributes with values from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

        if not hasattr(self, 'n_generations'):
            self.n_generations = 100
        if not hasattr(self, 'population_size'):
            self.population_size = 100
        if not hasattr(self, 'n_elite'):
            self.n_elite = 3
        if not hasattr(self, 'selection_method'):
            self.selection_method = 'tournament'
        if not hasattr(self, 'tournament_size'):
            self.tournament_size = 3
        if not hasattr(self, 'crossover_probability'):
            self.crossover_probability = 0.95 # NOTE was 0.8
        if not hasattr(self, 'two_point_crossover_prob'):
            self.two_point_crossover_prob = 0.8
        if not hasattr(self, 'mutation_probability'):
            self.mutation_probability = 0.05
        if not hasattr(self, 'mutation_increase_factor'):
            self.mutation_increase_factor = 1.1
        if not hasattr(self, 'inc_mutation'):
            self.inc_mutation = 10

        self.population = Population(self.graph, self.population_size)
    
    def get_fitness_over_time(self):
        return self.fitness_over_time

    def has_converged(self):
        if self.gen_counter >= self.n_generations or self.no_improvement_counter >= self.max_no_improvement:
            return True
        return False

    def get_running_time(self):
        return self.running_time

    def run(self):
        start = time.time()
        
        while (not self.has_converged()) and (self.running_time < self.max_time):
            new_population = []

            # get elite individuals
            elite_individuals = self.population.get_sorted_individuals(first_n=self.n_elite)
            new_population += elite_individuals

            # selection phase
            selected_individuals = []
            for _ in range(int(self.population_size)):
                selected_individuals.append(self.population.selection(self.selection_method, self.tournament_size))
            
            for i in range(0, len(selected_individuals), 2):
                individual1 = selected_individuals[i]
                individual2 = selected_individuals[i + 1]

                # crossover of selected individuals
                if random.uniform(0, 1) < self.crossover_probability:
                    if random.uniform(0, 1) < self.two_point_crossover_prob:
                        ch1, ch2 = self.population.two_point_crossover(individual1, individual2, self.mutation_probability)
                    else:
                        ch1, ch2 = self.population.single_point_crossover(individual1, individual2, self.mutation_probability)

                    new_population.append(ch1)
                    new_population.append(ch2)
                else:
                    new_population.append(individual1)
                    new_population.append(individual2)

            self.population.individuals = new_population                    
            
            best_fitness = self.population.get_sorted_individuals(first_n=1)[0].fitness
            self.fitness_over_time.append(best_fitness)

            if self.previous_best_fitness == best_fitness:
                self.no_improvement_counter += 1
                if self.no_improvement_counter >= self.inc_mutation:
                    self.mutation_probability *= self.mutation_increase_factor
                    self.mutation_probability = min(self.mutation_probability, 0.5) # max mutation probability is 0.5
            else:
                self.no_improvement_counter = 0
                self.previous_best_fitness = best_fitness

            self.gen_counter += 1
            self.running_time = time.time() - start
