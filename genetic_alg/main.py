from random import randint, shuffle
import pygame
import matplotlib.pyplot as plt

pygame.init()
#Clear statistic file
open("statistic.csv", "w").close()
font = pygame.font.Font('freesansbold.ttf', 32)

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
    def __init__(self, n_cities, n_population):
        self.n_cities = n_cities
        self.n_population = n_population
        self.cities = self.generate_cities()
        self.population = self.generate_population()
        self.best_individual = None
        self.generation = 0
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
    def next_generation(self):
        self.generation += 1
        self.population.sort(key=lambda x: x.fitness)
        self.best_individual = self.population[0]
        new_population = []
        fifty_percent = self.n_population//2
        ten_percent = self.n_population//10
        forty_percent = self.n_population - fifty_percent - ten_percent
        for i in range(forty_percent):
            new_population.append(self.population[i])
        for i in range(fifty_percent):
            new_population.append(self.crossover())
        for i in range(ten_percent):
            new_population.append(self.mutation())
        self.population = new_population
    
    def crossover(self):
        parent1 = self.population[randint(0, self.n_population//2)]
        parent2 = self.population[randint(0, self.n_population//2)]
        child = []
        rand_index = randint(0, self.n_cities-1)
        for i in range(rand_index):
            child.append(parent1.chromosome[i])
        for i in range(self.n_cities):
            if parent2.chromosome[i] not in child:
                child.append(parent2.chromosome[i])
        child.append(child[0])
        return Individual(child, self.cities)
    
    def mutation(self):
        rand_index1 = randint(0, self.n_cities-1)
        rand_index2 = randint(0, self.n_cities-1)
        while rand_index1 == rand_index2:
            rand_index2 = randint(0, self.n_cities-1)
        mutant= self.best_individual.chromosome.copy()
        mutant[rand_index1], mutant[rand_index2] = mutant[rand_index2], mutant[rand_index1]
        mutant.append(mutant[0])
        return Individual(mutant, self.cities)
    def statistic(self):
        average = 0
        for i in range(self.n_population):
            average += self.population[i].fitness
        average /= self.n_population
        return f"{self.generation},{average},{self.best_individual.fitness}\n"
        
class Draw:
    def __init__(self, genetic_alg: GeneticAlg):
        self.screen = pygame.display.set_mode((1000, 1000))
        self.genetic_alg = genetic_alg

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.genetic_alg.next_generation()
        save_statistic(self.genetic_alg.statistic())
        # Imprimir el numero de generacion
        text = font.render(str(self.genetic_alg.generation), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (50, 50)
        self.screen.blit(text, textRect)
        for i in range(len(self.genetic_alg.best_individual.chromosome)-1):
            pygame.draw.circle(self.screen, (255, 0, 0), (self.genetic_alg.cities[self.genetic_alg.best_individual.chromosome[i]].x*10, self.genetic_alg.cities[self.genetic_alg.best_individual.chromosome[i]].y*10), 5)
            pygame.draw.line(self.screen, (255, 255, 255), (self.genetic_alg.cities[self.genetic_alg.best_individual.chromosome[i]].x*10, self.genetic_alg.cities[self.genetic_alg.best_individual.chromosome[i]].y*10), (self.genetic_alg.cities[self.genetic_alg.best_individual.chromosome[i+1]].x*10, self.genetic_alg.cities[self.genetic_alg.best_individual.chromosome[i+1]].y*10))
        pygame.display.flip()
    
    def run(self, n_generations=100):
        for i in range(n_generations):
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            pygame.time.wait(100)
        pygame.quit()

#Save the statistic of average of fitness for each generation and the fitness of the best individual in a file
#Don't substitute the file, add the new statistic to the file
def save_statistic(string):
    file= open("statistic.csv", "a")
    file.write(string)
    file.close()
class DrawStatistic:
    #Draw the statistic of the genetic algorithm with matplotlib
    def __init__(self):
        self.load_statistic()
        self.draw()
    def load_statistic(self):
        self.generation= []
        self.average= []
        self.best= []
        file= open("statistic.csv", "r")
        for line in file:
            line= line.split(",")
            self.generation.append(int(line[0]))
            self.average.append(float(line[1]))
            self.best.append(float(line[2]))
        file.close()

    def draw(self):
        plt.plot(self.generation, self.average, label="Promedio")
        plt.plot(self.generation, self.best, label="Mejor individuo")
        plt.xlabel("Generación")
        plt.ylabel("Distancia")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    generations = 100
    genetic_alg = GeneticAlg(n_cities=20, n_population=300)
    draw= Draw(genetic_alg)
    draw.run(generations)
    statistic= DrawStatistic()