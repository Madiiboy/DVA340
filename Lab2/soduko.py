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
    

def checkIfValid(puzzle, position, value):

    # print(type(value))
    # print(type(int(puzzle[0][0])))

    # Check the row for occurance
    for i in range(9):
        if int(puzzle[position[0]][i]) == value and position[1] != i:
            return False

    # Check column for occurance
    for i in range(9):
        if int(puzzle[i][position[1]]) == value and position[0] != i:
            return False

    # Check if value occurs within our box
    box_x = position[1] // 3
    box_y = position[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if puzzle[i][j] == value and (i,j) != position:
                return False

    return True


#recursive function to solve each soduko table
def solve(puzzle):

    spot = findEmptySlot(puzzle)
   
    # If we do not find any empty slots, we can assume that we have solved the puzzle
    if not spot:
        return True
    else:
        row, column = spot

    for i in range(1, 10):
        if checkIfValid(puzzle, (row, column), i):
            puzzle[row][column] = i

            # Recursivly call this function to be able to backtrack our solution
            if solve(puzzle):
                return True

            puzzle[row][column] = 0

    return False
                
    
def findEmptySlot(puzzle):
    # find an empty slot and returns tuple with position
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] == 0:
                return (i, j)


if __name__ == "__main__":
    puzzles = readFile()

    start = time.time()
    # solve for every puzzle
    for p in puzzles:
        solve(p)

    end = time.time()
    for p in puzzles:
        for i in range(9):
            print(p[i])
        print('------------------------')
    print(end-start)
