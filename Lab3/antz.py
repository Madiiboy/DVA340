import math
import random
import numpy as np
from matplotlib import pyplot as plt
import copy

alpha = 30
beta = 20
global_best = float('inf')
global_best_ant = None
best = float('inf')
best_ant = None
ph = None


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

# Returns a matrix with distances between all the different cities
def initCitiesNormalized(cities):

    matrix = np.zeros(shape=(52,52))
    for i in range(len(cities)):
        for j in range(len(cities)):
            if i != j:
                matrix[i][j] = 1 / float(calcDistance(cities[i], cities[j]))
            #Distance to same city should be 0
            else:
                matrix[i][j] = 0

    # plt.imshow(matrix, interpolation='nearest')
    # plt.show()

    return matrix

# Returns a matrix of starting values of pheromone
def initPheromone():
    global ph
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
    ph = matrix

#def pheromoneEvaporation():
def initCities(cities):

    matrix = np.zeros(shape=(52,52))
    for i in range(len(cities)):
        for j in range(len(cities)):
            if i != j:
                matrix[i][j] = float(calcDistance(cities[i], cities[j]))
            #Distance to same city should be 0
            else:
                matrix[i][j] = 0

    # plt.imshow(matrix, interpolation='nearest')
    # plt.show()

    return matrix
#Here we randomly select path taking probabilities into consideration
def selectPath(ant, cx_n):

    for _ in range(52):

        possible = []

        sum = 0
        for loc in range(cx_n.shape[0]):
            if loc not in ant.visited:
                possible.append(loc)
                sum += math.pow(ph[ant.current][loc], alpha) * math.pow(cx_n[ant.current][loc] ,beta)

        probabilities = []
        for loc in possible:
            part = math.pow(ph[ant.current][loc], alpha) * math.pow(cx_n[ant.current][loc] ,beta)
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

def addPheromone(ants):
    #The ants are sorted
    global ph
    paths = []
    for a in ants:
        paths.append(a[1])

    for i,p in enumerate(paths):
        x = 1 / ants[i][0]
        if i == 51:
            ph[p[i]][p[0]] += x
        else:
            ph[p[i]][p[i+1]] += x


def eachAnt(ants, cx, cx_n):
    global best
    global global_best
    # selectPath(ants, cx, ph)
    paths = []
    for ant in ants:
        paths.append(selectPath(ant, cx_n))

    # z = []
    # for p in paths:
    #     z.append(sorted(p))


    total = []
    for p in paths:
        total.append(calculateBest(p, cx))

    x = sorted(total)
    addPheromone(x)
    evaporatePheromone()
    # print(x[0][0], x[0][1])

    if x[0][0] < global_best:
        global_best = x[0][0]
        global_best_ant = x[0][1]
    
    best = x[0][0]
    best_ant = x[0][1]

def calculateBest(path, cx):

    tot = 0
    for i,p in enumerate(path):
        if i == len(path)-1:
            tot += cx[51][0]
        tot += cx[path[i-1]][path[i]]

    return (tot, path)

def evaporatePheromone():
    global ph
    for i in range(52):
        for j in range(52):
            ph[i][j] *= 1-0.7

if __name__ == "__main__":

    cities = readFromFile()

    cx_n = initCitiesNormalized(cities)
    cx = initCities(cities)
    initPheromone()

    gen = 0
    while best > 9000:
        gen += 1
        ants = initAnts(50)
        eachAnt(ants ,cx, cx_n)
        print('Gen:',gen, 'Best:', "{0:.2f}".format(best), 'Global:', "{0:.2f}".format(global_best))
        #plt.imshow(ph, interpolation='nearest')
        #plt.show()
        # updatePheromone(ph)
    print('Gen:', gen, 'Best:', "{0:.2f}".format(best), 'Global:', "{0:.2f}".format(global_best))
