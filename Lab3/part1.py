from random import shuffle
import copy
import math

class City:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Fitness:
    def __init__(self, id, value):
        self.id = id
        self.value = value

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

def createPopulation(c,d):
    population = []

    # print(population)
    for _ in range(50):
        population.append(randomPopulation(c))

    return population
    # print(len(population))

    # for i in range(len(population)):
    #     for j in range(len(c)):
    #         print(population[i][j].id)
    #     print('--------------------------------')

    # print(len(population))

    # print(len(population))
    # for p in population:
    #     print(p)

def randomPopulation(c):
    shuffled = c.copy()
    shuffle(shuffled)
    return shuffled

def calcDistance(a, b):
    distance = math.sqrt((((b.x - a.x)**2)+(b.y - a.y)**2))
    return distance

def fitness(population):
    current_best = 100000 #setting high start values
    current_next_best = 100000
    current_best_index = 0
    current_next_best_index = 0

    for i, pop in enumerate(population):
        tot_distance = 0
        # print(len(pop))
        for i in range(len(pop)):
            if i == len(pop)-1: #If we are at the final index, add with the first
                tot_distance += calcDistance(pop[i], pop[0])
                break
            tot_distance += calcDistance(pop[i], pop[i+1])
    
    # Save current best index and value

    #     if tot_distance < current_best:
    #         current_next_best_index = current_best_index
    #         current_best_index = i
    #         current_next_best = current_best
    #         current_best = tot_distance

    # print('--------------------------------')
    # print('Index:', current_best_index, 'Value:', current_best)
    # print('Index:', current_next_best_index, 'Value:', current_next_best)
        # print(tot_distance)
        # print('------------------')


if __name__ == '__main__':
    cities, dim = readFromFile()
    init_population = createPopulation(cities, dim)
    fitness(init_population)
    # d = calcDistance(ci_sh[0], ci_sh[1]) #testing purpouses
    tot_distance = 0
    # print(ci_sh[0].id)
    # print(ci_sh[-1].id)

    # for i, c in enumerate(ci_sh):

    #     # If we are at the final element, we want to add with calculate with first index
    #     if i == dim-1:
    #         print(c.id)

    #for s in shuffled:
    #    print(s.id)
    #print(type(shuffled))