import time
import numpy as np

def splitting(line):
    return [char for char in line]

def readFile():
    path = './puzzle.txt'

    file = open(path, 'r')
    # skip the first four lines
    for _ in range(4):
        file.readline()

    puzzle_amount = 10
    # puzzles will be a list of 2d arrays
    puzzles = []

    for _ in range(puzzle_amount):
        puzzle = []
        # for every row in puzzle
        for _ in range(9):
            temp = file.readline()
            split = splitting(temp)
            del split[-1]
            int_split = []
            for s in split:
                int_split.append(int(s))

            puzzle.append(int_split)

        puzzles.append(puzzle)
        for _ in range(2):
            file.readline()

    return puzzles


if __name__ == "__main__":
    puzzles = readFile()
    # print(puzzles[0])
    pz = np.array(puzzles[0])
    y = pz.view(dtype=np.int16, type=np.matrix)
    print(y)
    # pz = puzzles[0].view(dtype=np.int16, type=np.matrix)
