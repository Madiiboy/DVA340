import math
import random
import numpy as np
from matplotlib import pyplot as plt

best = float('inf')

class City:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Ant:
    path = []
    def __init__(self, name, current, visited):
        self.name = name
        self.current = current
        self.visited = visited

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

def initAnts(amount, cities):
    ants = []
    for i in range(amount):
        ants.append(Ant(i,cities[0], cities[0]))

    return ants

# Returns a matrix with distances between all the different cities
def initCities(cities):

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

    return matrix

#def reducePheromone():

#Here we randomly select path taking probabilities into consideration
def selectPath(ant, cx, ph):
    print("What we wanna do here?!")

if __name__ == "__main__":

    cities = readFromFile()

    #initiate ant colony
    ants = initAnts(100, cities)
    cx = initCities(cities)
    ph = initPheromone()
    selectPath(ants[0], cx, ph)
    # for a in ants:
    #     print(a.current.id)

    # !!! Skapa typ 100 myror   !!!!!!
    # !!! Alla myror startar i samma stad !!!!!

    # För alla andra städer, flytta mororna baserat på pheromon

    #Calculate the total cost of the ants and the best ant

    #Update the pheromone on the edges

    #If better, replace the best