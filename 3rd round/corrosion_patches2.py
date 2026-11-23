# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (Problem 4: Corrosion Patches)
# ─────────────────────────────────────────────────────────────
#
# "Averages are nice but what I actually sign off on is patches.
#  If thin spots are next to each other, that's one repair job, not
#  three. Give me a list of the patches on this plate, worst first,
#  with how big each one is and where it is so I can mark it up."
#
# Readings: "x_mm,y_mm,thickness_mm"   (plate is 300 x 200 mm)
# Grid squares are 50 mm.
# A square is "thin" if it is below MIN_THICKNESS.
#
# For each patch report:
#   - number of squares and area in mm^2
#   - worst (minimum) thickness in the patch
#   - bounding box in mm: (x1, y1, x2, y2)
# Sorted worst patch first.
#
# ~40 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────

# each cell we can keep a min, max y and x value
# this way to can make our bounding box at query time easy in o(n)
from collections import defaultdict, deque

readings = [
    "10,10,9.5", "60,20,9.1", "110,30,9.8", "160,10,9.9",
    "210,40,10.0", "260,20,9.7", "20,70,5.8", "30,90,9.2",
    "70,80,5.1", "120,60,9.0", "170,90,9.4", "220,70,9.3",
    "280,60,9.6", "30,130,9.8", "75,140,4.4", "130,120,8.9",
    "180,110,9.1", "230,140,6.0", "270,130,9.2", "20,180,9.5",
    "80,170,9.0", "140,190,5.5", "210,160,3.9", "290,199,4.1",
    "ERR", "70,80,5.1", "310,10,9.0", "150,,8.8", "-5,20,9.0",
]

PLATE_W = 300
PLATE_H = 200
BIN_SIZE = 50
MIN_THICKNESS = 6.0

# sol
# parse data - only keep thicknesses under 6.0 (inclusive)
# dedup
# our range of x and y values are from 0 -> w/h
# as we parse we can work out the cell it lands in -> we know our 'bin' size it 50/50 grid squares
# after our parsed results we can then group up our bins while doing this working out min, max x, y values
# bfs on each patch we find when looping over the results collecting all the patches it touches to form a 'patch'
# while adding new results to what we see work out the bounding box using the min/max x y values


def parse_data(readings):

    parsed = []
    dropped = 0

    for reading in readings:
        try:
            x, y, thickness = reading.split(',')

            x = float(x)
            y = float(y)
            thickness = float(thickness)

            if thickness <= 0 or thickness >= MIN_THICKNESS:
                dropped += 1
                continue

            if x < 0 or y < 0 or x > PLATE_W or y > PLATE_H:
                dropped += 1
                continue

            parsed.append({
                "x": x,
                "y": y,
                "thickness": thickness
            })
        except Exception as e:
            dropped += 1

    return parsed, dropped


def grid_cell(x, y):
    col = min(int(x // BIN_SIZE), PLATE_W // BIN_SIZE - 1)
    row = min(int(y // BIN_SIZE), PLATE_H // BIN_SIZE - 1)
    return (col, row)


def bin_data(readings):

    # bin structure is (x, y) = thickness
    bins = {}

    for reading in readings:

        x, y, thickness = reading.values()

        x, y = grid_cell(x, y)

        if (x, y) in bins:
            bins[(x, y)] = min(bins[(x, y)], thickness)
            continue

        bins[(x, y)] = thickness

    return bins


def no_cells():
    return (PLATE_W // BIN_SIZE, PLATE_H // BIN_SIZE)


def bfs(x, y, bins, seen):
    q = deque()
    q.append((x, y))
    seen.add((x, y))
    patch = []
    min_x = x
    min_y = y
    max_x = x
    max_y = y
    length = 0
    thinnest = float("inf")
    rows, cols = no_cells()
    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    while q:

        for _ in range(len(q)):
            x, y = q.popleft()

            for dx, dy in dirs:
                cx, cy = x+dx, y+dy

                if cx < 0 or cy < 0 or cx >= rows or cy >= cols or (cx, cy) in seen or (cx, cy) not in bins:
                    continue

                q.append((cx, cy))
                seen.add((cx, cy))

            patch.append([x, y, bins[(x, y)]])
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            length += 1
            thinnest = min(thinnest, bins[(x, y)])

    return patch, min_x, max_x, min_y, max_y, thinnest, length


def find_all_patches(bins):
    rows, cols = no_cells()
    patches = []
    seen = set()
    for i in range(rows):
        for j in range(cols):
            if (i, j) in bins and (i, j) not in seen:
                patch, min_x, max_x, min_y, max_y, thinnest, length = bfs(
                    i, j, bins, seen)

                patches.append({
                    "patch": patch,
                    "min_x": min_x * BIN_SIZE,
                    # this is our upper bound for it
                    "max_x": (max_x + 1) * BIN_SIZE,
                    "min_y": min_y * BIN_SIZE,
                    # this is our upper bound for it
                    "max_y": (max_y + 1) * BIN_SIZE,
                    "thinnest": thinnest,
                    "size": length,
                    "area": length * (BIN_SIZE) * (BIN_SIZE)
                })

    return patches


def format_patches(patches):

    patches.sort(key=lambda p: (p["thinnest"], -p["area"]))

    return patches


def find_patches(readings):
    readings, dropped = parse_data(readings)

    bins = bin_data(readings)
    print(bins)
    patches = find_all_patches(bins)
    sorted_patches = format_patches(patches)
    return sorted_patches


if __name__ == "__main__":
    for patch in find_patches(readings):
        print(patch)
