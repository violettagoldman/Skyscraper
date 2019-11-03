import json
import sys
import numpy as np
from itertools import product
from os import path

def random_board(n):
    return np.floor(np.random.rand(n) * n + 1).astype(int).tolist()

def generate_random_boards(n):
    top = random_board(n)
    right = random_board(n)
    bottom = random_board(n)
    left = random_board(n)
    valid = True
    for i in range(n):
        if (top[i] == bottom[i] and (top[i] == 1 or top[i] == n)):
            valid = False
        if (left[i] == right[i] and (left[i] == 1 or left[i] == n)):
            valid = False
    if (not valid):
        return generate_random_boards(n)
    return [top, right, bottom, left]

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

def check_grid_not_full(grid):
    for i in range(grid.shape[0]):
        if (not check_vect_not_full(grid[:, i])):
            return False
        if (not check_vect_not_full(grid[i, :])):
            return False
    return True


def check_vect_not_full(vect):
    for i in range(1, len(vect) + 1):
        count = 0
        for j in vect:
            if (j == i):
                count += 1
        if (count > 1):
            return False
    return True

def check_vect(target, row):
    max = 0
    count = 0
    s = set()
    for i in row:
        if (i > max):
            max = i
            count += 1
        s.add(i)
    if (len(s) != len(row)):
        return False
    return target == count

def grid_full(grid):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[0]):
            if (grid[i][j] == 0):
                return False
    return True

def fill_row(row):
    count_undefined = 0
    index = 0
    for i in range(len(row)):
        if (row[i] == 0):
            count_undefined += 1
            index = i
    if (count_undefined == 1):
        for i in range(1, len(row) + 1):
            if (not i in row):
                row[index] = i
    return row

def fill_evident(grid, boards):
    for i in range(grid.shape[0]):
        grid[:, i] = fill_row(grid[:, i])
        grid[i, :] = fill_row(grid[i, :])
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
    global grids
    if (grid_full(grid)):
        if (check(grid, boards)):
            print_grid(grid, boards)
            grids = load_arr(grid.shape[0])
            if (not boards in grids):
                print("A new grid added :)")
                grids.append(boards)
                save_arr(grid.shape[0], grids)
            else:
                print("Already exists :(")
            print("Length:{}".format(len(grids)))
            return True
        return False
    grid = fill_evident(grid, boards)
    for rec in fill_random(grid):
        if (check_grid_not_full(rec) and solve_rec(rec, boards)):
            return True
    return False

def fill_random(grid):
    cords = None
    res = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[0]):
            if (grid[i][j] == 0):
                cords = (i, j)
    if (cords != None):
        for i in range(1, grid.shape[0] + 1):
            temp = np.array(grid)
            temp[cords] = i
            res.append(temp)
    return res

def solve(boards):
    grid = create_grid(len(boards[0]))
    return solve_rec(grid, boards)

def generation():
    global grids
    if (len(sys.argv) != 2):
        print("Error: Number of arguments is not valid")
        exit()
    n = int(sys.argv[1])
    print("Generation of grids of {} dimensions".format(n))
    i = 0
    grids = load_arr(n)
    while True:
        i += 1
        boards = generate_random_boards(n)
        solve(boards)

def load_arr(n):
    if (not path.exists("./grids/grids_{}.json".format(n))):
        return []
    with open("./grids/grids_{}.json".format(n), "r") as file:
        content = file.read()
    return json.loads(content)

def save_arr(n, array):
    with open("./grids/grids_{}.json".format(n), "w+") as file:
        file.write(json.dumps(array))

generation()
