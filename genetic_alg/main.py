from random import randint, shuffle

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def distance(self, city):
        return ((self.x - city.x)**2 + (self.y - city.y)**2)**0.5
    

class Individual:
    def __init__(self, chromosome, cities):
        self.chromosome = chromosome
        self.cities = cities
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        fitness = 0
        for i in range(len(self.chromosome)-1):
            fitness += self.cities[self.chromosome[i]].distance(self.cities[self.chromosome[i+1]])
        return fitness

class GeneticAlg:
    def __init__(self, n_generations, n_cities, n_population):
        self.n_generations = n_generations
        self.n_cities = n_cities
        self.n_population = n_population
        self.cities = self.generate_cities()
        self.population = self.generate_population()
        self.best_individual = None
    def generate_cities(self):
        cities = []
        for i in range(self.n_cities):
            cities.append(City(randint(0, 100), randint(0, 100)))
        return cities
    def generate_population(self):
        population = []
        for i in range(self.n_population):
            chromosome = [i for i in range(self.n_cities)]
            shuffle(chromosome)
            chromosome.append(chromosome[0])
            population.append(Individual(chromosome, self.cities))
        return population
    def simule_generation(self):
        self.population.sort(key=lambda x: x.fitness)
        self.best_individual = self.population[0]
        new_population = []
        for i in range(self.n_population//2):
            new_population.append(self.population[i])
        for i in range(self.n_population//2):
            new_population.append(self.crossover())
        self.population = new_population
        
    

if __name__ == "__main__":
    genetic_alg = GeneticAlg(100, 50, 50)
    print(genetic_alg.cities)
    for i in genetic_alg.population:
        print(i.chromosome)
        print(i.fitness)
        print()