# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (Problem 11: Tank Wall)
# ─────────────────────────────────────────────────────────────
#
# "This time the robot is on the wall of a storage tank, not a flat
#  plate. The wall is made of horizontal rings, and the lower rings
#  hold more pressure, so each ring has its own minimum thickness.
#  I need the squares that are below THEIR ring's limit, worst first,
#  and I want to draw boxes on the wall and get numbers back."
#
# Readings: "x_mm,y_mm,thickness_mm"
#   x runs around the tank, 0 to WALL_WIDTH. The wall is a cylinder,
#     so x = WALL_WIDTH is the same place as x = 0.
#   y runs up the wall, 0 to WALL_HEIGHT.
# Grid squares are 50 mm. Each row of squares is one ring.
# RING_MIN[row] is the minimum allowed thickness for that ring.
#
# Report:
#   - failing squares: any square whose lowest reading is below its
#     ring's minimum, as (col, row, lowest, limit, shortfall),
#     largest shortfall first
#   - one result per query, in order
#
# Queries: "x1,y1,x2,y2,agg"   agg is one of: min, max, avg, count
#   Because the wall wraps around, a box with x1 > x2 goes from x1
#   past WALL_WIDTH and round to x2. That is NOT an inverted box.
#
# ~40 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────
from collections import defaultdict

readings = [
    "10,10,13.0", "60,20,11.5", "120,30,12.4", "390,40,11.0",
    "20,70,10.5", "380,80,9.2", "400,60,9.8",
    "150,120,8.4", "210,110,7.1", "250,130,8.0",
    "300,170,5.5", "350,190,6.2", "40,199,6.0",
    "ERR", "450,10,9.0", "100,250,9.0", "100,100,-2", "60,20,11.5",
]

queries = [
    "0,0,100,50,min",
    "350,0,50,100,min",
    "350,0,50,100,count",
    "100,100,300,200,max",
    "0,100,400,100,count",
    "0,150,400,50,avg",
    "0,0,100,100,mean",
]

WALL_WIDTH = 400
WALL_HEIGHT = 200
BIN_SIZE = 50
RING_MIN = [12.0, 10.0, 8.0, 6.0]


def parse_readings(readings):

    parsed = []
    dropped = 0

    for reading in readings:
        try:
            x, y, thickness = reading.split(',')
            x = float(x)
            y = float(y)
            thickness = float(thickness)

            if thickness <= 0:
                dropped += 1
                continue

            if x > WALL_WIDTH or y >= WALL_HEIGHT or x < 0 or y < 0:
                dropped += 1
                continue

            parsed.append({
                "x": x,
                "y": y,
                "thickness": thickness,
            })

        except ValueError as e:
            print(e)
            dropped += 1

    return parsed, dropped


def get_cell(x, y):
    # x wraps 400 to 0
    # y just wraps 400 to the last index
    x = 0 if x == 400 else x // BIN_SIZE
    y = min(y // BIN_SIZE, (WALL_HEIGHT // BIN_SIZE) - 1)

    return (x, y)


def bin_data(readings):

    bins = defaultdict(lambda: {
        "readings": [],
        "min": float("inf"),
        "max": float("-inf"),
        "total": 0,
        "count": 0,
    })

    for reading in readings:
        cell = get_cell(reading["x"], reading["y"])
        bin = bins[cell]

        bin["readings"].append(reading)
        bin["min"] = min(reading["thickness"], bin["min"])
        bin["max"] = max(reading["thickness"], bin["max"])
        bin["total"] += reading["thickness"]
        bin["count"] += 1

    return bins


def get_x_range(x1, x2):
    nb = WALL_WIDTH // BIN_SIZE
    if x1 <= x2:
        return list(range(x1 // BIN_SIZE, min(x2 // BIN_SIZE, nb - 1) + 1))
    return list(range(x1 // BIN_SIZE, nb)) + list(range(0, x2 // BIN_SIZE + 1))


def query(x1, y1, x2, y2, agg, bins):
    if agg not in ("min", "max", "avg", "count"):
        return None
    if y1 > y2:
        y1, y2 = y2, y1

    def in_x(x):
        if x1 <= x2:
            return x1 <= x <= x2
        return (x >= x1 or x <= x2)

    max_row = WALL_HEIGHT // BIN_SIZE - 1
    rows = range(y1 // BIN_SIZE, min(y2 // BIN_SIZE, max_row) + 1)

    vals = []
    for cx in get_x_range(x1, x2):
        for cy in rows:
            for r in bins.get((cx, cy), {"readings": []})["readings"]:
                if in_x(r["x"]) and y1 <= r["y"] <= y2:
                    vals.append(r["thickness"])

    if agg == "count":
        return len(vals)
    if not vals:
        return None
    if agg == "min":
        return min(vals)
    if agg == "max":
        return max(vals)
    return sum(vals) / len(vals)


def parse_query(queries, bins):
    res = []
    for query_str in queries:
        x1, y1, x2, y2, agg = query_str.split(',')
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        result = query(x1, y1, x2, y2, agg, bins)

        res.append(result)

    return res


def tank_report(readings, queries):
    data, dropped = parse_readings(readings)

    bins = bin_data(data)
    results = parse_query(queries, bins)

    return results


if __name__ == "__main__":
    print(tank_report(readings, queries))
