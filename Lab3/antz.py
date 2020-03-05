import math
import random
import numpy as np
from matplotlib import pyplot as plt
import copy

alpha = 1.5
beta = 0.95
global_best = float('inf')
global_best_ant = None
best = float('inf')
best_ant = None
pheromone_matrix = None
city_matrix = None

class City:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Ant:
    path = []
    visited = []
    def __init__(self, name, current):
        self.name = name
        self.current = current
        self.visited = [current]

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

    return cities

#Calculate distance between points
def calcDistance(a, b):
    return float(math.sqrt((((b.x - a.x) ** 2) + (b.y - a.y) ** 2)))

def initAnts(amount):
    ants = []
    for i in range(amount):
        ants.append(Ant(i, 0))

    return ants

def initCities(cities):
    global city_matrix
    matrix = np.zeros(shape=(52,52))
    for i in range(len(cities)):
        for j in range(len(cities)):
            if i != j:
                matrix[i][j] = float(calcDistance(cities[i], cities[j]))
            #Distance to same city should be 0
            else:
                matrix[i][j] = 0

    city_matrix = matrix
    # plt.imshow(matrix, interpolation='nearest')
    # plt.show()

def initPheromone():
    global pheromone_matrix
    matrix = np.zeros(shape=(52,52))
    #Fill the new matrix with the start value
    for i in range(52):
        for j in range(52):
            if i != j:
                matrix[i][j] = 10
            #Distance to same city should be 0
            else:
                matrix[i][j] = 0
    #plt.imshow(matrix, interpolation='nearest')
    #plt.show()
    pheromone_matrix = matrix

def buildSolution(ants):
    global best

    paths = []
    #For each ant we want to walk around the path
    for ant in ants:
        paths.append(selectPath(ant))

    calculated_dist = []
    for path in paths:
        calculated_dist.append(calDistance(path))

    #Evaporate all edges
    evaporate()
    sort = sorted(calculated_dist)
    best = sort[0][0]
    addPheromone(sort)


def selectPath(ant):
    #For every city
    for i in range(52):
        possible = []
        sum = 0
        for i in range(52):
            if i not in ant.visited:
                #Add it to the path
                possible.append(i)
                sum += math.pow(pheromone_matrix[ant.current][i], alpha) * math.pow(1 / city_matrix[ant.current][i], beta)

        probabilities = []
        for i in possible:
            part = math.pow(pheromone_matrix[ant.current][i], alpha) * math.pow( 1 / city_matrix[ant.current][i], beta)
            d = part / sum
            probabilities.append(d)

        # Roulette selection
        selected = 0
        r = random.random()
        for i, p in enumerate(probabilities):
            r -= p
            if r <= 0:
                selected = i
                break
        if not len(possible):
            return ant.visited
        ant.current = possible[selected]
        ant.visited.append(possible[selected])

def calDistance(path):

    #Distance matrix yes pls
    val = 0
    for i in range(len(path)):
        #final index
        if i is len(path) - 1:
            val += city_matrix[path[i]][0]
        else:
            val += city_matrix[path[i]][path[i+1]]

    return (val, path)

def evaporate():
    global pheromone_matrix
    evap_rate = 0.3
    for i in range(52):
        for j in range(52):
            pheromone_matrix[i][j] = (1-evap_rate) * pheromone_matrix[i][j]

def addPheromone(sorted_ants):
    global pheromone_matrix
    vals = []
    paths = []
    for val in sorted_ants:
        vals.append(val[0])
        paths.append(val[1])

    for i,ant in enumerate(paths):
        x = vals[i]
        for i in range(1, 52):
            pheromone_matrix[ant[i-1]][ant[i]] += x
            pheromone_matrix[ant[i]][ant[i-1]] += x


if __name__ == "__main__":

    cities = readFromFile()
    initCities(cities)
    initPheromone()

    gen = 1
    while best > 9000:
        ants = initAnts(50)
        buildSolution(ants)
        print('Gen:',gen, 'Best:', "{0:.2f}".format(best))
        gen += 1
    #plt.imshow(city_matrix, interpolation='nearest')
    #plt.show()
        # updatePheromone(ph)
    #print('Gen:', gen, 'Best:', "{0:.2f}".format(best), 'Global:', "{0:.2f}".format(global_best))


