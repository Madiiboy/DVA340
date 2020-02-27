import random
import copy
import math

best = 0

class City:
    def __init__(self, _id, x, y):
        self.ide = _id
        self.x = x
        self.y = y

def readFromFile():
    file = open('tsp.txt', 'r')
    for _ in range(3):
        file.readline()

    dimension = int(file.readline().split(" ")[1])

    for _ in range(2):
        file.readline()

    cities = []
    for _ in range(dimension):
        data = file.readline().replace('\n', '').split(" ")
        cities.append(City(int(data[0]), float(data[1]), float(data[2])))

    return cities, dimension

#Create 50 individuals for the population
def createPopulation(c):
    return [randomPopulation(c) for i in range(50)]

#Shuffle the cities in the individual
def randomPopulation(c):
    shuffle_copy = copy.deepcopy(c)
    random.shuffle(shuffle_copy)
    return shuffle_copy

#Calculate distance between points
def calcDistance(a, b):
    return float(math.sqrt((((b.x - a.x) ** 2) + (b.y - a.y) ** 2)))

# Find the best and sort
def fitness(population):
    global best
    population_fitness = []
    for _, pop in enumerate(population):
        tot_distance = 0
        for i in range(len(pop)):
            if i == len(pop) - 1:  # If we are at the final index, add with the first
                tot_distance += calcDistance(pop[i], pop[0])
                population_fitness.append((tot_distance, pop))
                break
            tot_distance += calcDistance(pop[i], pop[i + 1])

    #Sort function
    population_fitness.sort(key = lambda t: t[0])
    # Set current best value to the global variable
    best = population_fitness[0][0]

    sorted_pop = []
    for p in population_fitness:
        sorted_pop.append(p[1])
    return sorted_pop

def crossover(best, rest):

    r1 = random.randint(0, len(population[0])-2)
    r2 = random.randint(r1, len(population[0])-1)

    section1_c1 = best[r1:r2]

    cities_in = []

    for c in section1_c1:
        cities_in.append(c.ide)

    section2_c1 = []
    for p in rest:
        if p.ide not in cities_in:
            section2_c1.append(p)

    c1 = section2_c1[:r1] + section1_c1 + section2_c1[r1:]

    r = random.randint(0,10)
    if r < 2:
        ri, ri2 = random.randint(0, len(population[0]) - 1), random.randint(0, len(population[0]) - 1)
        c1[ri], c1[ri2] = c1[ri2], c1[ri]

    return c1

def evolution(population):

    new_population = []

    alpha = population[0:5]
    #Randomize the best and the rest
    random.shuffle(best)
    random.shuffle(population)
    for i, citizen in enumerate(population[::-1]):
        new_population.append(crossover(best[i % len(best)-1], citizen))

    #Some elitism here
    new_population = new_population[0:40]
    new_population += population[0:10]

    return new_population

if __name__ == '__main__':
    cities, dim = readFromFile()
    population = createPopulation(cities)

    gen = 0
    while True:
        gen += 1
        population = fitness(population)
        population = evolution(population)
        print("Generation:", gen, "Best:", best)