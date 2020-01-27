#  Mats Fridberg, mfg17006
#  Assignment 1, part 1
import time
from queue import Queue
from copy import copy

#Class for the items
class Item:
    def __init__(self, item_id, b, w):
        self.item_id = item_id
        self.benefit = b
        self.weight = w

# Class that will contain the current state and values of the current node
class Node:
    solution = []
    def __init__(self, item_id, s, b, w , cb, cw):
        self.item_id = item_id
        self.benefit = b
        self.weight = w
        self.solution = s #type: list
        self.cb = cb
        self.cw = cw

class Solution:
    solution = []
    benefit = 0
    weight = 0

    def __init__(self, s, b, w):
        self.solution = s
        self.benefit = b
        self.weight = w

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

    depth = len(items)
    solution_bfs = Solution([], 0, 0)

    print("Init Breadth-first search")
    # Create and init the tree 
    empty_tree = []
    # Append -1 to all nodes in the tree, will represent an empty spot
    while len(empty_tree) < len(items):
        empty_tree.append(-1)

    # inititate an empty node 
    init_node = Node(0, empty_tree, 0, 0, 0, 0)
    
    # Create a queue
    queue = Queue()
    queue.put(init_node)
    # Run while there is items in the queue
    while not queue.empty():
        node = queue.get()
        if check_if_solution(node):
            for i in range(0, len(node.solution)):
                #-1 means it is an empty spot in the tree
                if node.solution[i] == -1:
                    depth = i
                    break
            # Go here only if item will not exceed max weight
            if (node.cw+items[depth].weight) <= max_weight:
                if depth < len(items):
                    # We use copy so that we get a shallow copy of list
                    sol_1 = copy(node.solution)
                    sol_1[depth] = 0
                    child = Node(depth+1, sol_1, items[depth].benefit, items[depth].weight, node.cb, node.cw)
                    queue.put(child)
                    sol_2 = copy(node.solution)
                    sol_2[depth] = 1
                    child = Node( depth+1, sol_2, items[depth].benefit, items[depth].weight, node.cb+items[depth].benefit, node.cw+items[depth].weight)
                    queue.put(child)
                    
        # Set the new best solution
        if solution_bfs.benefit < node.cb:
            solution_bfs.solution = node.solution
            solution_bfs.benefit = node.cb
            solution_bfs.weight = node.cw
    return solution_bfs

def DFS():
    print("Init Depth-first search")

def check_if_solution(node):
    for i in range(len(node.solution)):
        if node.solution[i] == -1:
            return True
    return False

if __name__ == "__main__":
    time_start = time.time()
    items, max_weight = read_from_file()
    solution = BFS(items, max_weight)
    time_end = time.time()
    id_list = []
    a = 1
    for i in solution.solution:
        if(i != 0):
            id_list.append(a)
        a+=1

    print("Solution: \n", "Items:  ", id_list, "\n\tBenefit: ", solution.benefit,  "\n\tWeight: ", solution.weight)

    print("Duration: ", time_end-time_start)
