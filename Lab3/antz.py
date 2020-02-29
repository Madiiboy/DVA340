import math
import random

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

class Edge:
    def __init__(self, distance, pheronone):
        self.distance = distance
        self.pheronone = pheronone

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

    # print(len(ants))
    # return ants
    # return [ant for i, ant = Ant(i+1,cities[0],[]) in enumerate(amount)]

def initPopulation(amount, cities):
    ants = []
    for i in range(amount):
        ants.append(Ant(i+1,cities[0], cities[0]))

    return ants

if __name__ == "__main__":

    cities = readFromFile()

    #initiate ant colony
    ants = initPopulation(100, cities)

    # for a in ants:
    #     print(a.current.id)


    # !!! Skapa typ 100 myror   !!!!!!
    # !!! Alla myror startar i samma stad !!!!!

    # För alla andra städer, flytta mororna baserat på pheromon

    #Calculate the total cost of the ants and the best ant

    #Update the pheromone on the edges

    #If better, replace the best