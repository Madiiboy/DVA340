from queue import PriorityQueue
import time

class Distance():
    def __init__(self, o, d, v):
        self.origin = o
        self.destination = d
        self.val = v

def readFile():
    file = open('spain_map.txt', 'r')
    # Skip first four lines
    for _ in range(5):
        file.readline()
    
    distance = []
    # Read all lines and append to distance list
    while True:
        temp = file.readline().split()
        if len(temp) < 3:
            break
        distance.append(Distance(temp[0], temp[1], temp[2]))

    # Skip two lines
    for _ in range(2):
        file.readline()

    # Create a cities for the straight line distance
    straight_line = {}
    while True:
        temp = file.readline().split()

        if len(temp) < 2:
            break
        straight_line[temp[0]] = int(temp[1])

    return distance, straight_line

def GBFS(distance, straight_line, dest):

    unique_cities = []

    # Fills a list of the unique cities
    for d in distance:
        if d.origin not in unique_cities:
            unique_cities.append(d.origin)
        if d.destination not in unique_cities:
            unique_cities.append(d.destination)
  
    cities = {}
    # Add all cities to the cities
    for u in unique_cities:
        cities[u] = {}

    # Add all the neighbors to each city
    for d in distance:
        cities[d.origin][d.destination] = int(d.val)
        cities[d.destination][d.origin] = int(d.val)

    # Create a queue that sorts depending on the shortest straight distance
    queue = PriorityQueue()
    queue.put((straight_line['Malaga'], 'Malaga')) #Putting the start value in the queue
    visited = []
    examined = []

    while queue:
        node = queue.get() 
        # print(node)
        if node[1] == dest:
            examined.append(node[1])
            print('We found our way!')
            break
        else:
            for s in cities[node[1]]:
                if not s in visited:
                    print(s)
                    queue.put((straight_line[s], s))
            examined.append(node[1])
    print(examined)

def AStar(distance, straight_line, dest):
    # Check straight_line but save the lenght of the current path

    unique_cities = []

    # Fills a list of the unique cities
    for d in distance:
        if d.origin not in unique_cities:
            unique_cities.append(d.origin)
        if d.destination not in unique_cities:
            unique_cities.append(d.destination)

    cities = {}
    # Add all cities to the cities
    for u in unique_cities:
        cities[u] = {}

    # Add all the neighbors to each city
    for d in distance:
        cities[d.origin][d.destination] = int(d.val)
        cities[d.destination][d.origin] = int(d.val)

    print(cities['Almeria']['Granada'])

if __name__ == '__main__':
    dest = 'Valladolid'
    distance, straight_line = readFile()

    start = time.time()
    # GBFS(distance, straight_line, dest)
    AStar(distance, straight_line, dest)
    end = time.time()
    print('Time elapsed:', end-start)