from random import shuffle
import copy
import math
from queue import PriorityQueue
import time

class City:
    def __init__(self, _id, x, y):
        self.id = _id
        self.x = x
        self.y = y

class Fitness:
    def __init__(self, _id, value):
        self.id = _id
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
    return [randomPopulation(c, i) for i in range(60)]

def randomPopulation(c, index):
    shuffled = c.copy()
    shuffle(shuffled)
    return (index, shuffled)

def calcDistance(a, b):

    distance = float(math.sqrt((((b.x - a.x)**2)+(b.y - a.y)**2)))
    return distance

# Sort the best solutions. Return priority queue sorted on the shortest distance 
def fitness(population):
    queue = PriorityQueue()
    for _, pop in enumerate(population):
        tot_distance = 0
        p_index = pop[0]
        p_data = pop[1]
        for i in range(len(pop[1])):
            if i == len(pop[1])-1: #If we are at the final index, add with the first
                tot_distance += calcDistance(p_data[i], p_data[0])
                queue.put((tot_distance, p_index))
                break
            tot_distance += calcDistance(p_data[i], p_data[i+1])
   
    # for _ in range(60):
    #     print(queue.get())
    
    return queue

def breed(queue, population):

    new_population = []

    # for _ in range(60):
    #     print(queue.get())
    #Index of our population
    # for p in population:
    #     print(p[0])

    for _ in range(1):
        p1, p2 = queue.get(), queue.get()
        p1_index, p2_index = p1[1], p2[1]
        # print(p1_index, p2_index)

        #This is the data to be copied into our new child
        parent_1 = population[p1_index][1]
        parent_2 = population[p2_index][1]

        #Do the breeding here!!!

        print(parent_1)
        





        

    
    #return the new population
    return

if __name__ == '__main__':
    cities, dim = readFromFile()
    start = time.time()
    init_population = createPopulation(cities, dim)

    fitness(init_population)
    end = time.time()
    # print(end-start)

    # print(init_population)

    

    population = init_population.copy()
    gen = 0

    # while True:
    gen += 1
    order = fitness(population)
    breed(order, population)

    
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