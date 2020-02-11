import time

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

    for i in range(puzzle_amount):
        puzzle = []
        # for every row in puzzle
        for _ in range(9):
            temp = file.readline()
            split = splitting(temp)
            del split[-1]
            puzzle.append(split)

        puzzles.append(puzzle)
        for _ in range(2):
            file.readline()

    return puzzles
    

def checkIfValid(puzzle, pos, val):

    # for x in range(9):

    # # Check row and column if value is within that row
    # for x in range(9):
    #     for y in range(9):
    #         if puzzle[x][y] is val:
    #             print("nono")
    #             return False
    #         if puzzle[y][x] is val:
    #             print("nono")
    #             return False


def solve(puzzle):
    
    # Make this function recursive

                

# find an empty slot
def findEmptySlot(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] is '0':
                return (i, j)
    return False


if __name__ == "__main__":
    puzzles = readFile()


    start = time.time()
    # solve for every puzzle
    solve(puzzles[0])
    # for p in puzzles:
    #     # print(p)
    #     solve(p)

    end = time.time()
    print(end-start)