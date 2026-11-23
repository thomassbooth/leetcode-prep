# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (Repair Route)
# ─────────────────────────────────────────────────────────────
#
# "The scan of the ship's deck is done and we've flagged the spots
#  that need repair. The repair crew is starting from the gangway.
#  For each repair spot, they want to know how far they have to walk
#  to get there, so they can plan the day, nearest jobs first."
#
# The deck has been divided into 1 m squares:
#   'S'  the gangway, where the crew starts
#   '.'  open deck
#   '#'  can't walk through (hatch covers, vents, pipework)
#   'R'  a repair spot (you can walk onto it)
#
# The crew can walk forwards, backwards, left or right one square
# at a time - no diagonals, no climbing over obstacles.
#
# Return every repair spot with its walking distance in metres,
# nearest first.
#
# ~30 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────

from collections import deque

deck = [
    "S...#.....",
    ".##.#.##R.",
    ".#R...#...",
    ".#.####.#.",
    "...#R...#R",
    "##.#.##.##",
    "R..#....#R",
]


def find_repair_spots(deck):

    spots = set()

    for row in range(len(deck)):
        for col in range(len(deck[0])):
            if deck[row][col] == "R":
                spots.add((row, col))

            if deck[row][col] == "S":
                start = (row, col)

    return spots, start


def walk_deck(deck):

    seen = set()
    rows = len(deck)
    cols = len(deck[0])
    repair_spots, start = find_repair_spots(deck)
    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    # each result we see we add its time to it and yeah boom
    res = []
    q = deque()
    q.append(start)
    seen.add(start)
    dist = 0

    while q:

        for _ in range(len(q)):
            x, y = q.popleft()

            if deck[x][y] == "R":
                res.append(((x, y), dist))
                repair_spots.remove((x, y))

            for dx, dy in dirs:
                cx = dx + x
                cy = dy + y
                if cx < 0 or cy < 0 or cx >= rows or cy >= cols or (cx, cy) in seen or deck[cx][cy] == "#":
                    continue

                q.append((cx, cy))
                seen.add((cx, cy))
        dist += 1

    for x, y in repair_spots:
        res.append(((x, y), -1))
    return res


def repair_route(deck):
    return walk_deck(deck)


if __name__ == "__main__":
    for row in repair_route(deck):
        print(row)
