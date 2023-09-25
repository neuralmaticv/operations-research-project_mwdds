import random
import time


def is_feasible(graph, partial_solution):
    graph.reset_colors()

    for i in range(len(partial_solution)):
        if partial_solution[i] == 1:
            graph.color_vertex(graph.vertices[i], 2)

    # check if all white vertices are colored
    if len(graph.white_vertices) == 0:
        return True

    return False

def is_white(vertex):
    # EQ2: Calculate CLR(u)
    if vertex.color == 0:
        return 1
    return 0

def weighted_sum_of_white_successors(vertex):
    # Ws(u)
    sum = 0
    for successor in vertex.successors:
        if successor.color == 0:
            sum += successor.weight
    return sum

def number_of_white_successors(vertex):
    # WOUTdeg(u)
    count = 0
    for successor in vertex.successors:
        count += is_white(successor)
    
    return count

def number_of_predecessors(vertex):
    return vertex.in_degree

def p_score(vertex):
    # score(u)
    score = (weighted_sum_of_white_successors(vertex) + is_white(vertex) * vertex.weight) / vertex.weight
    return score

def t_score(vertex):
    # score_tie(u)
    score = (number_of_white_successors(vertex) + is_white(vertex)) / vertex.weight
    return score

def heuristic12(non_black_vertices):
    '''
    H1 and H2: in every iteration it tries to select non-black vertex with the highest p-score
    if two or more vertices have the same p-score, it selects the one with the highest t-score
    if two or more vertices have the same p-score and t-score, it selects the one randomly
    '''

    non_black_vertices.sort(key=p_score, reverse=True)

    max_p_score = p_score(non_black_vertices[0])
    max_p_score_vertices = [non_black_vertices[0]]

    for i in range(1, len(non_black_vertices)):
        if p_score(non_black_vertices[i]) == max_p_score:
            max_p_score_vertices.append(non_black_vertices[i])
        else:
            break
    
    if len(max_p_score_vertices) == 1:
        return max_p_score_vertices[0]
    else:
        max_p_score_vertices.sort(key=t_score, reverse=True)
        return max_p_score_vertices[random.randint(0, len(max_p_score_vertices) - 1)]

    
def heuristic3(non_black_vertices):
    '''
    H3: begins by making all source vertices black
    if there is tie per p-score, it selects the white vertex with minimum number of predecessors
    if still tie, it selects the first one
    if there is no white vertex, it selects the gray vertex with the highest p-score
    if there is tie per p-score for gray vertices, it selects randomly
    '''

    non_black_vertices.sort(key=p_score, reverse=True)

    max_p_score = p_score(non_black_vertices[0])
    max_p_score_vertices = [non_black_vertices[0]]

    for i in range(1, len(non_black_vertices)):
        if p_score(non_black_vertices[i]) == max_p_score:
            max_p_score_vertices.append(non_black_vertices[i])
        else:
            break

    if len(max_p_score_vertices) == 1:
        return max_p_score_vertices[0]
    else:
        white_vertices = [v for v in max_p_score_vertices if is_white(v)]
        
        if len(white_vertices) > 0:
            white_vertices.sort(key=number_of_predecessors)

            min_predecessors = number_of_predecessors(white_vertices[0])
            min_predecessors_vertices = [white_vertices[0]]

            for i in range(1, len(white_vertices)):
                if number_of_predecessors(white_vertices[i]) == min_predecessors:
                    min_predecessors_vertices.append(white_vertices[i])
                else:
                    break

            if len(min_predecessors_vertices) == 1:
                return min_predecessors_vertices[0]
            else:
                return min_predecessors_vertices[random.randint(0, len(min_predecessors_vertices) - 1)]
        else:        
            gray_vertices = [v for v in max_p_score_vertices if v.color == 1]
            gray_vertices.sort(key=p_score, reverse=True)

            max_p_score = p_score(gray_vertices[0])
            max_p_score_vertices = [gray_vertices[0]]

            for i in range(1, len(gray_vertices)):
                if p_score(gray_vertices[i]) == max_p_score:
                    max_p_score_vertices.append(gray_vertices[i])
                else:
                    break
            
            if len(max_p_score_vertices) == 1:
                return max_p_score_vertices[0]
            else:
                return max_p_score_vertices[random.randint(0, len(max_p_score_vertices) - 1)]

def greedy_heuristics(graph, partial_solution, heuristic_fn):
    graph.reset_colors()
    for i in range(len(partial_solution)):
        if partial_solution[i] == 1:
            graph.color_vertex(graph.vertices[i], 2)

    while not is_feasible(graph, partial_solution):
        non_black_vertices = [v for v in graph.vertices if partial_solution[v.id] == 0]
        v = heuristic_fn(non_black_vertices)
        partial_solution[v.id] = 1

    return partial_solution

def repair_operator(graph, individual):
    graph.reset_colors()

    # add all source vertices to the solution
    for source_vertex in graph.source_vertices:
        individual[source_vertex.id] = 1
        graph.color_vertex(source_vertex, 2)

    while len(graph.white_vertices) > 0:
        scores = []

        # compute p_score(u) for all vertices that are not in the Sd
        for vertex in graph.white_vertices:
            scores.append((vertex, p_score(vertex)))

        # select vertex with the highest score
        max_score = max(scores, key=lambda x: x[1])[1]
        max_score_vertices = [v for v, s in scores if s == max_score]

        # if there is tie select randomly
        if len(max_score_vertices) == 1:
            max_score_vertex = max_score_vertices[0]
        else:
            max_score_vertex = random.choice(max_score_vertices)

        # update the individual and color the selected vertex
        individual[max_score_vertex.id] = 1
        graph.color_vertex(max_score_vertex, 2)

    return individual

def redundant_removal(graph, individual):
    # step 1: add all source vertices to the solution
    for source_vertex in graph.source_vertices:
        graph.color_vertex(source_vertex, 2)
    
    # step 2: compute set of redundant vertices
    redundant_vertices = []
    for vertex in graph.vertices:
        if vertex.color == 2:
            graph.color_vertex(vertex, 0)
            individual[vertex.id] = 0

            # if Sd is valid without v, then v is redundant
            if is_feasible(graph, individual):
                redundant_vertices.append(vertex)
            else:
                graph.color_vertex(vertex, 2)
                individual[vertex.id] = 1
    
    # step 3: remove redundant vertices from the solution
    for vertex in redundant_vertices:
        graph.color_vertex(vertex, 0)
        individual[vertex.id] = 0
    
    return individual


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
    
    def fitness_fn(self, graph):
        if is_feasible(graph, self.chromosome):            
            if random.random() < 0.2:
                self.chromosome = redundant_removal(graph, self.chromosome)

            self.fitness = sum([graph.vertices[i].weight for i, _ in enumerate(self.chromosome) if self.chromosome[i] == 1])
        else:
            if random.random() < 0.2:
                self.chromosome = repair_operator(graph, self.chromosome)
                self.fitness = sum([graph.vertices[i].weight for i, _ in enumerate(self.chromosome) if self.chromosome[i] == 1])
            else:
                self.fitness = graph.total_weight


class Population:    
    def __init__(self, graph, population_size):
        self.population_size = population_size
        self.normalized_proportions = None
        self.graph = graph
        self.source_vertices = [vertex.id for vertex in graph.source_vertices] # vertices with in-degree 0
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
        
            if random.random() < 0.3:
                individual = greedy_heuristics(self.graph, individual, heuristic3)
            elif random.random() < 0.5:
                individual = greedy_heuristics(self.graph, individual, heuristic12)

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
            
            if random.random() < 0.3:
                individual = greedy_heuristics(self.graph, individual, heuristic12)

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
        max_source_individuals = int(self.population_size * 0.01)
        population += self._gen_by_source_vertices(max_source_individuals)

        # generate random individuals
        max_random_individuals = self.population_size - max_source_individuals
        population += self._gen_random(max_random_individuals)

        for individual in population:
            individual.fitness_fn(self.graph)
    
        return population

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
            
            return best_individual
        elif method == 'tournament':
            tournament_individuals = random.sample(self.individuals, tournament_size)

            while len(set(tournament_individuals)) != len(tournament_individuals):
                tournament_individuals = random.sample(self.individuals, tournament_size)

            return min(tournament_individuals, key=lambda individual: individual.fitness)

    def single_point_crossover(self, individual1, individual2, mutation_probability=0.05):
        crossover_point = random.randint(1, len(individual1.chromosome) - 1)

        child1 = Individual(chromosome_length=len(individual1.chromosome))
        child2 = Individual(chromosome_length=len(individual1.chromosome))

        child1.chromosome = individual1.chromosome[:crossover_point] + individual2.chromosome[crossover_point:]
        child2.chromosome = individual2.chromosome[:crossover_point] + individual1.chromosome[crossover_point:]

        child1, child2 = self.mutation(child1, child2, mutation_probability)
            
        child1.fitness_fn(self.graph)
        child2.fitness_fn(self.graph)        
        
        return child1, child2
    
    def two_point_crossover(self, individual1, individual2, mutation_probability=0.05):
        crossover_point1 = random.randint(1, len(individual1.chromosome) // 2)
        crossover_point2 = random.randint(len(individual1.chromosome) // 2, len(individual1.chromosome) - 1)

        child1 = Individual(chromosome_length=len(individual1.chromosome))
        child2 = Individual(chromosome_length=len(individual1.chromosome))

        child1.chromosome = individual1.chromosome[:crossover_point1] + individual2.chromosome[crossover_point1:crossover_point2] + individual1.chromosome[crossover_point2:]
        child2.chromosome = individual2.chromosome[:crossover_point1] + individual1.chromosome[crossover_point1:crossover_point2] + individual2.chromosome[crossover_point2:]

        child1, child2 = self.mutation(child1, child2, mutation_probability)

        child1.fitness_fn(self.graph)
        child2.fitness_fn(self.graph)

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
            self.crossover_probability = 0.95
        if not hasattr(self, 'two_point_crossover_prob'):
            self.two_point_crossover_prob = 0.8
        if not hasattr(self, 'mutation_probability'):
            self.mutation_probability = 0.05
        if not hasattr(self, 'mutation_increase_factor'):
            self.mutation_increase_factor = 2
        if not hasattr(self, 'inc_mutation'):
            self.inc_mutation = self.n_generations // 10

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

            # elitism phase
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
