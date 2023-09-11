import random
import time
import logging

logger = logging.getLogger("main")

def is_valid(graph, individual, initial=False):
    graph.reset_colors()

    logger.info(f"Individual: {individual}")

    for i in range(len(individual)):
        if individual[i] == 1:
            graph.color_vertex(graph.vertices[i], 2)
    
    logger.info(graph.white_vertices)
    logger.info(graph.gray_vertices)
    logger.info(graph.black_vertices)
    logger.info(sum([vertex.weight for vertex in graph.black_vertices]))
    logger.info("")
    logger.info("")
            
    if len(graph.white_vertices) == 0:
        return True
    
    if initial:
        if len(graph.white_vertices) > 0:
            for i in range(len(individual)):
                if random.random() < 0.8 and individual[i] == 0 and graph.vertices[i].color == 0:
                    individual[i] = 1
                    graph.color_vertex(graph.vertices[i], 2)
                    
            if len(graph.white_vertices) == 0:
                return True
    
    return False

def fitness_func(graph, individual, initial=False):
    if is_valid(graph, individual.chromosome, initial):
        return sum([graph.vertices[i].weight for i, _ in enumerate(individual.chromosome) if individual.chromosome[i] == 1])
    else:
        return graph.total_weight


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
        # swap
        # logger.info("Swapping")
        # logger.info(f"Before: {self.chromosome}")
        # idx1, idx2 = self.get_uniqe_ids()
        
        # self.chromosome[idx1], self.chromosome[idx2] = self.chromosome[idx2], self.chromosome[idx1]
        # logger.info(f"After: {self.chromosome}")
            
        # return self
        logger.info("Mutating")
        logger.info(f"Before: {self.chromosome}")
        for i in range(len(self.chromosome)):
            if random.random() < 0.5:
                self.chromosome[i] = 1 - self.chromosome[i]
        logger.info(f"After: {self.chromosome}")
                
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


class Population:    
    def __init__(self, graph, population_size):
        self.population_size = population_size
        self.normalized_proportions = None
        self.graph = graph
        self.source_vertices = [vertex.id - 1 for vertex in graph.source_vertices] # vertices with in-degree 0
        self.individuals = self._initialize_population()

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
        max_source_individuals = int(self.population_size * 0.3)
        population += self._gen_by_source_vertices(max_source_individuals)

        # generate random individuals
        max_random_individuals = self.population_size - max_source_individuals
        population += self._gen_random(max_random_individuals)

        # generate individuals with highest degree vertices
        # max_highest_degree_individuals = self.population_size - max_source_individuals - max_random_individuals
        # population += self._gen_by_highest_degree_vertices(max_highest_degree_individuals)

        for individual in population:
            individual.fitness = fitness_func(self.graph, individual, initial=True)
    
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

    def selection(self, method='tournament'):
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
            # Select two random individuals
            individual1 = random.choice(self.individuals)
            individual2 = random.choice(self.individuals)
            
            # Ensure that the two selected individuals are different
            while individual1 == individual2:
                individual2 = random.choice(self.individuals)
            
            # Select the better of the two individuals
            return min(individual1, individual2, key=lambda individual: individual.fitness)

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
            
        child1.fitness = fitness_func(self.graph, child1)
        child2.fitness= fitness_func(self.graph, child2)        
        
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
    def __init__(self, graph, fitness_fn, max_time=None, max_no_improvement=None, **kwargs):
        self.graph = graph
        self.fitness_fn = fitness_fn
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
        if not hasattr(self, 'selection_method'):
            self.selection_method = 'tournament'
        if not hasattr(self, 'crossover_probability'):
            self.crossover_probability = 0.8
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
        logger.info("Initial population:")
        for individual in self.population.individuals:
            logger.info(f"chromosome: {individual.chromosome}, fitness: {individual.fitness}")
        self.population._calc_normalized_proportions()
        
        
        logger.info("Starting the algorithm...")
        start = time.time()
        while (not self.has_converged()) and (self.running_time < self.max_time):
            logger.info(f"Generation {self.gen_counter}")

            logger.info("Selection...")
            # select 1/2 of the initial population
            selected_individuals = []
            for _ in range(int(self.population_size / 2)):
                selected_individuals.append(self.population.selection(self.selection_method))
            
            for i in range(0, len(selected_individuals), 2):
                individual1 = selected_individuals[i]
                individual2 = selected_individuals[i + 1]

                # crossover of selected individuals
                if random.uniform(0, 1) < self.crossover_probability:
                    logger.info("Crossover...")
                    ch1, ch2 = self.population.single_point_crossover(individual1, individual2, self.mutation_probability)
                    self.population.individuals.append(ch1)
                    self.population.individuals.append(ch2)                 

            logger.info(f"population size: {len(self.population.individuals)}")
            self.population.individuals = sorted(self.population.individuals, key=lambda individual: individual.fitness)[:self.population_size]
            logger.info(f"population size: {len(self.population.individuals)}")
            
            best_fitness = self.population.individuals[0].fitness
            self.fitness_over_time.append(best_fitness)
            logger.info(f"Best fitness: {best_fitness}")

            if self.previous_best_fitness == best_fitness:
                self.no_improvement_counter += 1
                if self.no_improvement_counter >= self.inc_mutation:
                    self.mutation_probability *= self.mutation_increase_factor
                    self.mutation_probability = min(self.mutation_probability, 0.5) # max mutation probability is 0.5
                    logger.info(f"Mutation probability increased to {self.mutation_probability}")
            else:
                self.no_improvement_counter = 0
                self.previous_best_fitness = best_fitness

            self.gen_counter += 1
            self.running_time = time.time() - start

        logger.info(f"Best solution: {self.population.individuals[0].chromosome}")
        logger.info(f"Best fitness: {self.population.individuals[0].fitness}")
        if self.gen_counter == self.n_generations:
            logger.info("Algorithm finished due to reaching the maximum number of generations.")
        elif self.no_improvement_counter == self.max_no_improvement:
            logger.info("Algorithm finished due to reaching the maximum number of generations without improvement.")
        else:
            logger.info("Algorithm finished due to reaching the maximum time.")
        
        logger.info("Algorithm finished.")
