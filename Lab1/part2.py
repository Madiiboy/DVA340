from queue import PriorityQueue
import time

class Distance():
    def __init__(self, o, d, v):
        self.origin = o
        self.destination = d
        self.val = v


def readFile():
    file = open("spain_map.txt", "r")
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

    # Create a dictionary for the straight line distance
    straight_line = {}
    while True:
        temp = file.readline().split()

        if len(temp) < 2:
            break
        straight_line[temp[0]] = int(temp[1])

    return distance, straight_line

def GBFS(distance, bird, source, dest):

    target = "Valladolid"
    unique_cities = []

    # Fills a list of the unique cities
    for d in distance:
        if d.origin not in unique_cities:
            unique_cities.append(d.origin)
        if d.destination not in unique_cities:
            unique_cities.append(d.destination)
  
    dictionary = {}
    # Add all cities to the dictionary
    for u in unique_cities:
        dictionary[u] = {}

    # Add all the neighbors to each city
    for d in distance:
        dictionary[d.origin][d.destination] = int(d.val)
        dictionary[d.destination][d.origin] = int(d.val)

    # Create a queue that sorts depending on the shortest straight distance
    queue = PriorityQueue()
    queue.put((bird['Malaga'], 'Malaga')) #Putting the start value in the queue
    visited = []
    examined = []

    while queue:
        node = queue.get() 
        # print(node)
        if node[1] == target:
            examined.append(node[1])
            print("We found our way!")
            break
        else:
            for s in dictionary[node[1]]:
                if not s in visited:
                    visited.append(s)
                    queue.put((bird[s], s))
            examined.append(node[1])
    print(examined)
                  
if __name__ == "__main__":
    src = "Malaga"
    dest = "VValladolid"
    distance, bird = readFile()

    start = time.time()
    GBFS(distance, bird, src, dest)
    end = time.time()
    print(end-start)