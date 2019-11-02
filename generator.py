import sys
import numpy as np
from itertools import product

def random_board(n):
    return np.floor(np.random.rand(n) * n + 1).astype(int)

def generate_random_boards(n):
    return (random_board(n), random_board(n), random_board(n), random_board(n))

def create_grid(n):
    return np.zeros([n, n]).astype(int)

def print_grid(grid, boards):
    for j in range(grid.shape[0] + 2):
        if (j == 0 or j == grid.shape[0] + 1):
            print("  ", end="")
        if (j > 0 and j < grid.shape[0] + 1):
            print("{} ".format(boards[3][j - 1]), end="")
        for i in range(grid.shape[0]):
            if (j == 0):
                print("{} ".format(boards[0][i]), end="")
            elif (j == grid.shape[0] + 1):
                print("{} ".format(boards[2][i]), end="")
            else:
                print("{} ".format(grid[j - 1][i]), end="")
        if (j == 0 or j == grid.shape[0] + 1):
            print("  ", end="")
        if (j > 0 and j < grid.shape[0] + 1):
            print("{} ".format(boards[1][j - 1]), end="")
        print("")

def check(grid, boards):
    for i in range(grid.shape[0]):
        if (not check_vect(boards[0][i], grid[:, i])):
            return False
        if (not check_vect(boards[2][i], np.flip(grid[:, i]))):
            return False
        if (not check_vect(boards[1][i], np.flip(grid[i, :]))):
            return False
        if (not check_vect(boards[3][i], grid[i, :])):
            return False
    return True

def check_vect(target, row):
    max = 0
    count = 0
    for i in row:
        if (i > max):
            max = i
            count += 1
    return target == count

def grid_full(grid):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[0]):
            if (grid[i][j] == 0):
                return False
    return True

def fill_evident(grid, boards):
    for i in range(grid.shape[0]):
        if (boards[0][i] == grid.shape[0]):
            grid[:, i] = np.array(range(1, grid.shape[0] + 1))
        if (boards[2][i] == grid.shape[0]):
            grid[:, i] = np.flip(np.array(range(1, grid.shape[0] + 1)))
        if (boards[1][i] == grid.shape[0]):
            grid[i, :] = np.flip(np.array(range(1, grid.shape[0] + 1)))
        if (boards[3][i] == grid.shape[0]):
            grid[i, :] = np.array(range(1, grid.shape[0] + 1))
    return grid

def solve_rec(grid, boards):
    if (grid_full(grid)):
        if (check(grid, boards)):
            return True
        return False
    grid = fill_evident(grid, boards)

def fill_random(grid):
    cords = None
    res = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[0]):
            if (grid[i][j] == 0):
                cords = (i, j)
    if (cords != None):
        for i in range(1, grid.shape[0] + 1):
            grid = array()
    return ()

def solve(boards):
    pass

def generation():
    if (len(sys.argv) != 2):
        print("Error: Number of arguments is not valid")
        exit()
    n = int(sys.argv[1])
    print("Generation of grids of {} dimensions".format(n))
    print_grid(create_grid(n), generate_random_boards(n))

g = np.array([[3, 4, 1, 2], [1, 3, 2, 4], [2, 1, 4, 3], [4, 2, 3, 1]])
b = (np.array([2, 1, 3, 2]),
np.array([2, 1, 2, 3]),
np.array([1, 3, 2, 3]),
np.array([2, 3, 2, 1]))

#generation()
#print_grid(g, b)
#print(check(g, b))
#solve(b)
ge = create_grid(3)
be = generate_random_boards(3)
print_grid(ge, be)
ge = fill_evident(ge, be)
print_grid(ge, be)