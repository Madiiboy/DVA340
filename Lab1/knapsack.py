#  Mats Fridberg, mfg17006
#  Assignment 1, part 1
import time
from queue import Queue

#Class for the items
class Item:
    def __init__(self, item_id, b, w):
        self.item_id = item_id
        self.benefit = b
        self.weight = w

# Class that will contain the current state and values of the current node
class Node:
    def __init__(self, item_id, s, b, w , cb, cw):
        self.item_id = item_id
        self.solution = s #type: list
        self.benefit = b
        self.weight = w
        self.current_benefit = cb
        self.current_weight = cw

#Read the input data
def read_from_file():
    file = open('./knapsack.txt', 'r')
    #ignore the first three lines
    for _ in range(2):
        file.readline()

    #Get amount of items, dimension and max weight
    item_amount = int(file.readline().split()[1])
    dimension = int(file.readline().split()[1])
    max_weight = int(file.readline().split()[2])
    
    print('Items: ', item_amount, '\nDimension: ', dimension, '\nMax Weight: ', max_weight)
    # Skip two lines
    for _ in range(2):
        file.readline()

    # List of all the items in the document
    items = []
    for _ in range(item_amount):
        data = file.readline().split()
        item_id = int(data[0].replace('.', ''))
        item_b = int(data[1])
        item_w = int(data[2])
        items.append(Item(item_id, item_b, item_w))

    # Return relevant data
    return items, max_weight

def BFS(items, max_weight):

    # Create and init the tree 
    empty_tree = []
    while len(empty_tree) < len(items):
        empty_tree.append(False)

    
    print("Init Breadth-first search")
    return solution

def DFS():
    print("Init Depth-first search")

if __name__ == "__main__":
    time_start = time.time()
    items, max_weight = read_from_file()

    solution = BFS(items, max_weight)

    time_end = time.time()
    print(time_end-time_start)
