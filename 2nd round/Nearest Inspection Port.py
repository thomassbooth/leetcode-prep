from collections import deque

# Problem 2: Nearest Inspection Port (medium)
#
# A facility map has:
#   'P' = inspection port (where a robot can be inserted)
#   '#' = wall
#   '.' = open floor
#
# The robot moves up/down/left/right, one cell per move, and can't pass through walls.
# For every cell, return how many moves it is from the NEAREST port.
#   - Ports are 0
#   - Walls are -1
#   - Open cells that no port can reach are -1
#
# Example 1:
#   grid = [
#     ['P', '.', '#'],
#     ['.', '#', '.'],
#     ['.', '.', 'P'],
#   ]
#   -> [
#     [0,  1, -1],
#     [1, -1,  1],
#     [2,  1,  0],
#   ]
#
# Example 2:
#   grid = [
#     ['.', '#', 'P'],
#     ['#', '.', '.'],
#   ]
#   -> [
#     [-1, -1,  0],
#     [-1,  2,  1],
#   ]
#   (top-left is walled in, so no port can reach it)
#
# Example 3:
#   grid = [['.', '.']]
#   -> [[-1, -1]]
#   (no ports at all)
#
# Constraints:
#   - up to 1000 x 1000 cells
#   - any number of ports, including zero
#


def port_distances(grid: list[list[str]]) -> list[list[int]]:

    rows = len(grid)
    cols = len(grid[0])
    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    q = deque()

    # find ports
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "P":
                q.append([row, col])

    # bfs
    dist = 0
    while q:

        for _ in range(len(q)):
            row, col = q.popleft()
            if grid[row][col] == "#":
                grid[row][col] = -1
                continue

            if grid[row][col] not in (".", "P"):
                continue

            grid[row][col] = dist
            for dr, dc in dirs:
                if dr+row < 0 or dr+row >= rows:
                    continue
                if dc + col < 0 or dc + col >= cols:
                    continue

                q.append([row + dr, col + dc])

        dist += 1

    return grid
