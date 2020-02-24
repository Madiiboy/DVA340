from random import shuffle
import random
import copy
import math
from queue import PriorityQueue
import time

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


def createPopulation(c):
    return [randomPopulation(c) for i in range(60)]


def randomPopulation(c):
    shuffled = c.copy()
    shuffle(shuffled)
    return (shuffled)


def calcDistance(a, b):
    distance = float(math.sqrt((((b.x - a.x) ** 2) + (b.y - a.y) ** 2)))
    return distance


# Sort the best solutions. Return priority queue sorted on the shortest distance
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

    sorted_pop = []
    sort = sorted(population_fitness)
    best = sort[0][0]
    for p in sort:
        sorted_pop.append(p[1])

    return sorted_pop

def breed2(population):

    new_population = []
    # Byt ut 2 mot 30

    for i in range(0, 30, 2):
        p1 = population[i]
        p2 = population[i + 1]

        r1 = random.randint(0, len(population[0]) / 2)
        r2 = random.randint(len(population[0]) / 2, len(population[0]))

        c1 = [None] * len(population[0])
        c2 = [None] * len(population[0])

        c1[r1:r2] = p1[r1:r2].copy()
        c2[r1:r2] = p2[r1:r2].copy()

        cities_in = []
        cities_in_2 = []

        for c in c1:
            if not c is None:
                cities_in.append(c.ide)
        for c in c2:
            if not c is None:
                cities_in_2.append(c.ide)

        for i, c in enumerate(c1):
            if c is None:
                for p in p2:
                    if not p.ide in cities_in:
                        cities_in.append(p.ide)
                        c1[i] = p
                        break

        for i, c in enumerate(c2):
            if c is None:
                for p in p1:
                    if not p.ide in cities_in_2:
                        cities_in.append(p.ide)
                        c2[i] = p
                        break

        rand = random.randint(0,100)
        if rand > 50:
            ri, ri2 = random.randint(0, len(population[0]) - 1), random.randint(0, len(population[0]) - 1)
            c1[ri], c1[ri2] = c1[ri2], c1[ri]
            c2[ri], c2[ri2] = c2[ri2], c2[ri]

        new_population.append(p1)
        new_population.append(p2)
        new_population.append(c1)
        new_population.append(c1)

    return new_population

def breed(population):

        new_population = []
        #Byt ut 2 mot 30

        for i in range(0, 30, 2):
            p1 = population[i]
            p2 = population[i+1]

            r1 = random.randint(0, len(population[0])/2)
            r2 = random.randint(len(population[0])/2, len(population[0]))

            c1 = [None] * len(population[0])
            c2 = [None] * len(population[0])

            c1[r1:r2] = p1[r1:r2].copy()
            c2[r1:r2] = p2[r1:r2].copy()

            cities_in = []
            cities_in_2 = []

            for c in c1:
                if not c is None:
                    cities_in.append(c.ide)
            for c in c2:
                if not c is None:
                    cities_in_2.append(c.ide)

            for i,c in enumerate(c1):
                if c is None:
                    for p in p2:
                        if not p.ide in cities_in:
                            cities_in.append(p.ide)
                            c1[i] = p
                            break

            for i,c in enumerate(c2):
                if c is None:
                    for p in p1:
                        if not p.ide in cities_in_2:
                            cities_in.append(p.ide)
                            c2[i] = p
                            break

            ri, ri2 = random.randint(0, len(population[0])-1), random.randint(0, len(population[0])-1)
            c1[ri], c1[ri2] = c1[ri2], c1[ri]
            c2[ri], c2[ri2] = c2[ri2], c2[ri]

            new_population.append(p1)
            new_population.append(p2)
            new_population.append(c1)
            new_population.append(c1)

        return new_population


if __name__ == '__main__':
    cities, dim = readFromFile()
    start = time.time()
    init_population = createPopulation(cities)


    population = init_population.copy()
    gen = 0
    while True:
        gen += 1
        population = fitness(population)
        population = breed2(population)
        print("Generation:", gen, "Best:", best)
