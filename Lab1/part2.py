
class Distance():
    def __init__(self, o, d, v):
        self.origin = o
        self.destination = d
        self.val = v

# Straigh line distance is usually called "fågelvägen" in swedish, therefore name bird
class Bird():
    def __init__(self, o, v):
        self.origin = o
        self.val = v

class City():
    def __init__(self, city, adjecents):
        self.city = city
        self.adjecents = adjecents


def readFile():
    file = open("spain_map.txt", "r")
    # Skip first four lines
    for _ in range(5):
        file.readline()
    
    distance = []
    while True:
        temp = file.readline().split()
        if len(temp) < 3:
            break
        distance.append(Distance(temp[0], temp[1], temp[2]))
        # print(temp)

    for _ in range(2):
        file.readline()

    birdie = []
    while True:
        temp = file.readline().split()

        if len(temp) < 2:
            break
        birdie.append(Bird(temp[0], temp[1]))

    # print(file.readline())
    return distance, birdie

def GBFS(distance, bird, source, dest):

    # for b in bird:
    #     print(b.origin)

    tree = []
    unique_cities = []

    for d in distance:
        if d.origin not in unique_cities:
            unique_cities.append(d.origin)
        if d.destination not in unique_cities:
            unique_cities.append(d.destination)
    # print(len(unique_cities))
    # print(type(distance[0].origin))
    dictionary = {}

    for u in unique_cities:
        dictionary[u] = {}

    for d in distance:
        dictionary[d.origin][d.destination] = int(d.val)
        dictionary[d.destination][d.origin] = int(d.val)


    current = "Malaga"

    while True:

        # Check adjecent cities starting at Malaga
        # Pick the neighbor with the smallest bird distance
        # Repeat until we have reached Valladolid
        tree = []
        for d in distance:
            if d.origin == current:
                tree.append(d.destination)
            
        for b in bird:
            if b.origin in tree:
                


            


    # print(l)








if __name__ == "__main__":
    src = "Malaga"
    dest = "VValladolid"
    distance, bird = readFile()
    GBFS(distance, bird, src, dest)