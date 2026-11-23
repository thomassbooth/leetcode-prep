# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (Problem 1: Corrosion Patches)
# ─────────────────────────────────────────────────────────────
#
# "Our crawler scanned a section of boiler wall. The plant manager
#  wants to know how many separate corroded areas there are, how
#  big each one is, and how thin the worst point in each one gets."
#
# The robot streams readings as "x_mm,y_mm,thickness_mm".
#   - x is distance from the left edge, y is distance down from the top.
#   - The probe takes a reading every 25 mm in both directions.
#   - Readings arrive in no particular order.
#   - Some spots were scanned more than once.
#   - Some spots have no reading at all.
#   - It's field data, so expect some bad lines.
#
# A reading below the threshold is corroded. Corroded readings
# that touch up/down/left/right are the same corroded area.
#
# For each area, report (size_in_cells, min_thickness), sorted
# biggest area first, then thinnest first.
#
# ~30 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────

from collections import deque
from pprint import pprint

readings = [
    "75,75,4.9",
    "50,0,4.2",
    "0,25,10.0",
    "25,50,10.2",
    "75,ERR,4.0",
    "0,75,4.5",
    "50,25,4.1",
    "75,0,4.0",
    "",
    "25,25,-1.0",
    "0,0,10.1",
    "75,50,9.7",
    "50,75,10.0",
    "100,0",
    "25,0,9.8",
    "0,50,3.9",
    "75,25,9.9",
    "50,50,10.0",
    "25,75,4.6",
    "50,25,4.3",
]

threshold = 5.0
CELL = 25


# solution ->
# 1. we want to parse our data make sure we only have valid rows
# 2. Remove duplicates by either taking the average of the two or just the thinnest reading - id go with thinnest reading probably
# 3. flag all of our readings that fall below our threshold
# 4. assign x, y grid positions into a map key: (x // 25, y // 25): thickness
# 5. bfs out from each position we find creating a 'patch', visisted set also
# 6. post processing with some sorting of each patch

def parse_readings(readings):
    parsed, garb = [], []

    for reading in readings:
        try:
            x, y, thickness = reading.split(',')
            x = float(x)
            y = float(y)
            thickness = float(thickness)

            if thickness <= 0:
                garb.append(reading)
                continue

            parsed.append({
                "x": x,
                "y": y,
                "thickness": thickness
            })

        except:
            garb.append(reading)

    return parsed, garb


def cell_location(x, y, cell_size=25):
    return (x // cell_size, y // cell_size)


def flag_data(readings, threshold):

    flagged = {}
    dropped = 0
    for reading in readings:
        thickness = reading["thickness"]

        if thickness >= threshold:
            dropped += 1
            continue

        cell = cell_location(reading["x"], reading["y"])

        # handles our deduplication
        if cell in flagged and flagged[cell] < thickness:
            continue

        flagged[cell] = thickness

    return flagged, dropped


def bfs(start_x, start_y, seen, flagged):
    q = deque()
    q.append((start_x, start_y))
    seen.add((start_x, start_y))
    area = 0
    patch = []
    smallest = float("inf")
    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    while q:

        for _ in range(len(q)):
            x, y = q.popleft()
            thickness = flagged[(x, y)]
            patch.append((x, y, thickness))
            smallest = min(thickness, smallest)
            area += 1
            for dx, dy in dirs:
                dc = (x + dx, y + dy)
                if dc not in seen and dc in flagged:
                    seen.add(dc)
                    q.append(dc)

    return patch, area, smallest


def find_patches(flagged):
    patches = []
    seen = set()

    for x, y in flagged.keys():

        if (x, y) not in seen:
            patch, area, smallest = bfs(x, y, seen, flagged)
            patches.append({
                "patches": patch,
                "thinnest": smallest,
                "area": area
            })

    return patches


def organise_result(patches: list):
    patches.sort(key=lambda p: (-p["area"], p["thinnest"]),)

    return [()]


def corroded_areas(readings, threshold):

    readings, garbage = parse_readings(readings)

    flagged, dropped = flag_data(readings, threshold)

    patches = find_patches(flagged)
    organise_result(patches)
    return patches


if __name__ == "__main__":
    pprint(corroded_areas(readings, threshold))
