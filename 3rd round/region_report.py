# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (Problem 3: Region Report)
# ─────────────────────────────────────────────────────────────
#
# "The inspector doesn't care about one square at a time. They draw
#  a box on the plate drawing and want the avg / min / max / median
#  thickness of everything inside it. They'll do this a LOT while
#  reviewing a plate, so it needs to feel instant."
#
# Readings: "x_mm,y_mm,thickness_mm"   (plate is 200 x 200 mm)
# Grid squares are 50 mm.
# A region query is "x1,y1,x2,y2,agg" in mm - the box the inspector drew.
#
# ~40 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────
from collections import defaultdict

readings = [
    "10,10,9.5", "40,30,9.7", "60,20,8.1", "90,40,7.9",
    "110,10,9.9", "160,30,10.0", "20,70,6.2", "70,80,5.1",
    "80,95,4.8", "130,60,9.1", "180,90,9.4", "30,130,9.8",
    "75,140,5.5", "120,120,9.0", "170,170,3.9", "190,199,4.1",
    "ERR", "60,20,8.1", "210,10,9.0",
]

PLATE_SIZE = 200
BIN_SIZE = 50

queries = [
    "0,0,100,100,avg",
    "50,50,100,150,min",
    "0,0,200,200,median",
    "150,150,200,200,max",
    "25,25,75,75,avg",
    "100,100,50,50,avg",
]


def parse_data(readings):

    parsed = []
    dropped = 0

    for reading in readings:
        try:
            x, y, thickness = reading.split(',')
            x = float(x)
            y = float(y)
            thickness = float(thickness)
            if x > PLATE_SIZE or y > PLATE_SIZE or x < 0 or y < 0:
                dropped += 1
                continue

            parsed.append({
                "x": x,
                "y": y,
                "thickness": thickness
            })
        except:
            continue

    return parsed, dropped


def find_cell(x, y):

    return (x // BIN_SIZE, y // BIN_SIZE)


def bin_results(readings):

    grid = defaultdict(lambda: {
        "readings": [],
        "min": float("inf"),
        "max": float("-inf"),
        "sum": 0,
        "length": 0,
        "sorted": False
    })

    for reading in readings:
        cell = find_cell(reading["x"], reading["y"])

        grid[cell]["readings"].append(reading)
        grid[cell]["min"] = min(grid[cell]["min"], reading["thickness"])
        grid[cell]["max"] = max(grid[cell]["max"], reading["thickness"])
        grid[cell]["length"] += 1
        grid[cell]["sum"] += reading["thickness"]

    return grid


def parse_query(query):
    x1, y1, x2, y2, agg = query.split(",")
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    x1, x2 = sorted((x1, x2))   # handles the inverted box "100,100,50,50"
    y1, y2 = sorted((y1, y2))
    return x1, y1, x2, y2, agg


def run_query(bins, x1, y1, x2, y2, agg):
    total, count = 0, 0
    lo, high = float("inf"), float("-inf")

    values = []

    for cx in range(int(x1 // BIN_SIZE), int(x2 // BIN_SIZE)+1):
        for cy in range(int(y1 // BIN_SIZE), int(y2 // BIN_SIZE) + 1):
            cell = bins.get((cx, cy))

            if not cell:
                continue

            fully_inside = (
                x1 <= cx * BIN_SIZE and (cx + 1) * BIN_SIZE <= x2 and
                y1 <= cy * BIN_SIZE and (cy + 1) * BIN_SIZE <= y2
            )

            if fully_inside and agg != "median":
                # set our values for else
                total += cell["sum"]
                count += cell["length"]
                lo = min(lo, cell["min"])
                high = max(high, cell["max"])
            else:
                # boundaries or if its median so we need to get all of the values
                for r in cell["readings"]:
                    # make sure its in range
                    if x1 <= r["x"] <= x2 and y1 <= r["y"] <= y2:
                        t = r["thickness"]
                        total += t
                        count += 1
                        lo = min(lo, t)
                        high = max(high, t)
                        values.append(t)

    if count == 0:
        return None

    if agg == "avg":
        return round(total / count, 2)

    if agg == "min":
        return lo

    if agg == "max":
        return high

    if agg == "median":
        values.sort()
        mid = len(values)//2
        # check if even number
        return values[mid] if len(values) % 2 else (values[mid-1] + values[mid]) / 2


def process_queries(queries, bins):
    return [run_query(bins, *parse_query(query)) for query in queries]


def region_report(readings, queries):

    parsed, dropped = parse_data(readings)

    bins = bin_results(parsed)

    res = process_queries(queries, bins)

    return res


if __name__ == "__main__":
    for q, ans in zip(queries, region_report(readings, queries)):
        print(q, "->", ans)
