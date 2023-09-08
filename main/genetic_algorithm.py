import random
import time
import logging

logger = logging.getLogger("main")
def fitness_func(graph, individual):
    # Convert the binary string to a set of selected vertices
    selected_vertices = set(i for i, bit in enumerate(individual.chromosome) if bit == 1)
    
    return sum(graph.vertices[v].weight for v in selected_vertices), len(selected_vertices)

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

    def mutate(self, graph):
        if random.uniform(0, 1) > 0.5:
            # swap
            logger.info("Swapping")
            logger.info(f"Before: {self.chromosome}")
            idx1, idx2 = self.get_uniqe_ids()
            
            self.chromosome[idx1], self.chromosome[idx2] = self.chromosome[idx2], self.chromosome[idx1]
            logger.info(f"After: {self.chromosome}")
        else:
            logger.info("Rotating")
            logger.info(f"Before: {self.chromosome}")
            idx1, idx2 = self.get_uniqe_ids()
            
            fst = idx1 if graph.vertices[idx1].weight < graph.vertices[idx2].weight else idx2
            snd = idx2 if graph.vertices[idx1].weight < graph.vertices[idx2].weight else idx1

            self.chromosome = self.chromosome[:fst] + self.chromosome[fst:snd][::-1] + self.chromosome[snd:]
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
        self.individuals = [self._create_individual(graph) for _ in range(population_size - 1)]
        

    def _create_individual(self, graph):
        chromosome_length = len(graph.vertices)

        # Initialize an individual with all bits set to 0
        individual = [0] * chromosome_length

        # Ensure that all vertices with in-degree 0 are selected
        for i in range(chromosome_length):
            if i in self.source_vertices:
                individual[i] = 1
            else:
                # Set the rest of the bits randomly
                individual[i] = random.randint(0, 1)

        
        # Create an Individual object if needed
        initial = Individual(individual)
        initial.fitness, _ = fitness_func(graph, initial)

        return initial

    def _calc_normalized_proportions(self):
        all_fitnesses = [individual.fitness for individual in self.individuals]
        sum_fitnesses = sum(all_fitnesses)

        # lower fitness -> higher probability of selection
        inverse_proportions = [sum_fitnesses / fitness for fitness in all_fitnesses]

        # Normalize the proportions
        proportions_sum = sum(inverse_proportions)
        normalized_proportions = [proportion / proportions_sum for proportion in inverse_proportions]
        
        self.normalized_proportions = normalized_proportions

    def calculate_fitness(self, vertices_w, edges):
        for individual in self.individuals:
            individual.fitness_func(vertices_w, edges)

    def selection(self, method='roulette_wheel'):
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
            
        child1.fitness,_ = fitness_func(self.graph, child1)
        child2.fitness,_ = fitness_func(self.graph, child2)        
        
        return child1, child2
    
    def mutation(self, child1, child2, mutation_probability):
        new_child1 = Individual(init=child1.chromosome)
        new_child2 = Individual(init=child2.chromosome)

        if random.uniform(0, 1) < mutation_probability:
            new_child1 = child1.mutate(self.graph)
        
        if random.uniform(0, 1) < mutation_probability:
            new_child2 = child2.mutate(self.graph)
        
        return new_child1, new_child2
    
class GeneticAlgorithm:
    def __init__(self, graph, fitness_fn, max_time=None, **kwargs):
        self.graph = graph
        self.fitness_fn = fitness_fn
        self.max_time = max_time
        
        # Update class attributes with values from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

        if not hasattr(self, 'n_generations'):
            self.n_generations = 100
        if not hasattr(self, 'population_size'):
            self.population_size = 100
        if not hasattr(self, 'selection_method'):
            self.selection_method = 'roulette_wheel'
        if not hasattr(self, 'crossover_probability'):
            self.crossover_probability = 0.8
        if not hasattr(self, 'mutation_probability'):
            self.mutation_probability = 0.05
        
        self.population = Population(self.graph, self.population_size)


    def run(self):
        logger.info("Initial population:")
        for individual in self.population.individuals:
            logger.info(f"chromosome: {individual.chromosome}, fitness: {individual.fitness}")
        self.population._calc_normalized_proportions()

        logger.info("Starting the algorithm...")
        start = time.time()
        while self.n_generations > 0:
            logger.info(f"Generation {self.n_generations}")

            logger.info("Selection...")
            individual1 = self.population.selection(self.selection_method)
            individual2 = self.population.selection(self.selection_method)
            
            # make sure that we dont select the same individuals
            while (individual1 == individual2):
                individual2 = self.population.selection(self.selection_method)

            logger.info(f"individual1: {individual1.chromosome}, fitness: {individual1.fitness}")
            logger.info(f"individual2: {individual2.chromosome}, fitness: {individual2.fitness}")
            
            logger.info("Crossover...")
            ch1, ch2 = self.population.single_point_crossover(individual1, individual2)
            logger.info(f"ch1: {ch1.chromosome}, fitness: {ch1.fitness}")
            logger.info(f"ch2: {ch2.chromosome}, fitness: {ch2.fitness}")

            # add children to the population and remove the worst individuals
            self.population.individuals.append(ch1)
            self.population.individuals.append(ch2)
            self.population.individuals = sorted(self.population.individuals, key=lambda individual: individual.fitness)[:self.population_size]
            logger.info(f"Population size: {len(self.population.individuals)}")
            for individual in self.population.individuals:
                logger.info(f"chromosome: {individual.chromosome}, fitness: {individual.fitness}")

            self.n_generations -= 1
            
            if time.time() - start > self.max_time:
                logger.info("Time limit reached.")
                break
        
        logger.info("Algorithm finished.")
