from collections import deque

# Problem 3: Crawler Battery (medium-hard)
#
# A crawler starts at 'S' with a full battery of B moves and must reach 'E'.
#   'S' = start
#   'E' = end
#   'C' = charging station
#   '.' = open floor
#   '#' = wall
#
# Rules:
#   - The crawler moves up/down/left/right, one cell per move.
#   - Each move uses 1 charge. It can't move with 0 charge left.
#   - Arriving on a 'C' instantly refills the battery to B.
#   - Arriving on 'E' with 0 charge is fine.
#
# Return the fewest moves to reach 'E', or -1 if it can't be reached.
#
# Example 1:
#   grid = ["S..C..E"], B = 3
#   -> 6
#   (3 moves to the charger with 0 left, refill to 3, 3 more moves to E)
#
# Example 2:
#   grid = ["S..C..E"], B = 2
#   -> -1
#   (the battery runs out 1 cell before the charger)
#
# Example 3:
#   grid = [
#     "S.....E",
#     ".#####.",
#     "...C...",
#   ]
#   B = 6  -> 6    (straight along the top row)
#   B = 5  -> 10   (the top row needs 6; detour down to the charger: 5 moves, refill, 5 more to E)
#   B = 4  -> -1   (can't even reach the charger)
#
# Constraints:
#   - up to 100 x 100 cells
#   - 1 <= B <= 100
#   - exactly one 'S' and one 'E', any number of 'C'
#
# Think about: in plain BFS you never visit a cell twice. Is that still safe here?
# Could arriving at the same cell later, but with MORE battery, ever be useful?


def min_moves(grid: list[str], B: int) -> int:
    # bfs solution
    # as we go out we can push onto our queue the location of the next node and the battery %
    # we cant traverse walls
    # lets mark the erm path as we go with moves to get to it

    rows = len(grid)
    cols = len(grid[0])
    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    q = deque()

    # fewest moves will be as soon as we reach the end
    start = [0, 0]
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "S":
                start = [row, col]
                break

    # on our queue we start will full battery at the start
    q.append([*start, B])
    moves = 0
    visited = set()

    while q:
        for _ in range(len(q)):
            row, col, battery = q.popleft()

            if row < 0 or row >= rows:
                continue

            if col < 0 or col >= cols:
                continue

            if grid[row][col] == "E":
                return moves

            if grid[row][col] == "C":
                battery = B

            if battery <= 0:
                continue

            if grid[row][col] == "#":
                continue

            if (row, col, battery) in visited:
                continue

            for dr, dc in dirs:
                q.append([row+dr, col+dc, battery-1])

            visited.add((row, col, battery))
        moves += 1

    return -1
