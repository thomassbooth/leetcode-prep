# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (Problem 9: Live Plate)
# ─────────────────────────────────────────────────────────────
#
# "The robot is on the plate right now and the inspector is watching
#  the screen. Readings keep coming in, and every so often the
#  inspector draws a box and wants a number for it straight away.
#  The answer has to reflect everything received up to that moment."
#
# Stream lines, in order:
#   "ADD,x_mm,y_mm,thickness_mm"
#   "QUERY,x1,y1,x2,y2,agg"        agg is one of: avg, min, max, median, count
#
# Plate is 200 x 200 mm. Grid squares are 50 mm.
#
# Produce one result per QUERY line, in order.
# Queries should stay fast as the number of readings grows.
#
# ~40 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────
from collections import defaultdict

stream = [
    "ADD,10,10,9.5", "ADD,40,30,9.7", "ADD,60,20,8.1",
    "QUERY,0,0,100,100,avg",
    "ADD,90,40,7.9", "ADD,20,70,6.2", "ADD,70,80,5.1",
    "QUERY,0,0,100,100,avg",
    "QUERY,0,0,100,100,min",
    "QUERY,25,25,75,75,max",
    "ADD,80,95,4.8", "ADD,130,60,9.1", "ADD,ERR", "ADD,210,10,9.0",
    "QUERY,0,0,200,200,median",
    "QUERY,150,150,200,200,avg",
    "QUERY,100,100,50,50,count",
    "ADD,200,200,3.3",
    "QUERY,150,150,200,200,min",
    "QUERY,0,0,200,200,sum",
    "QUERY,0,0,50",
    "ADD,60,20,8.1",
    "QUERY,0,0,200,200,count",
]

PLATE_SIZE = 200
BIN_SIZE = 50


class LivePlate:

    def __init__(self):
        self._grid = defaultdict(lambda: {
            "readings": [],
            "count": 0,
            "min": float('inf'),
            "max": float("-inf"),
            "total": 0,
            "sorted": False
        })

    def _get_cell(self, x, y):
        last = PLATE_SIZE // BIN_SIZE - 1
        # if it lands on the boundry itll go into a new cell so we need to prevent taht
        return (min(x // BIN_SIZE, last), min(y // BIN_SIZE, last))

    def add(self, x, y, thickness):

        cell = self._get_cell(x, y)

        self._grid[cell]["readings"].append({
            "x": x,
            "y": y,
            "t": thickness
        })
        self._grid[cell]["count"] += 1
        self._grid[cell]["min"] = min(self._grid[cell]["min"], thickness)
        self._grid[cell]["max"] = max(self._grid[cell]["max"], thickness)
        self._grid[cell]["total"] += thickness

    def query(self, x1, y1, x2, y2, agg):

        total, count = 0, 0
        low, high = float("inf"), float("-inf")

        values = []
        last = PLATE_SIZE // BIN_SIZE - 1
        for cx in range(int(x1 // BIN_SIZE), min(int(x2 // BIN_SIZE), last) + 1):
            for cy in range(int(y1 // BIN_SIZE), min(int(y2 // BIN_SIZE), last) + 1):

                cell = self._grid[(cx, cy)]

                if not cell:
                    continue

                fully_inside = (
                    x1 <= cx * BIN_SIZE and (cx + 1) * BIN_SIZE <= x2 and
                    y1 <= cy * BIN_SIZE and (cy + 1) * BIN_SIZE <= y2
                )

                if fully_inside and agg != "median":
                    total += cell["total"]
                    count += cell["count"]
                    low = min(low, cell["min"])
                    high = max(high, cell["max"])
                else:
                    for r in cell["readings"]:
                        x = r["x"]
                        y = r["y"]
                        thickness = r["t"]

                        if x1 <= x <= x2 and y1 <= y <= y2:
                            total += thickness
                            count += 1
                            low = min(low, thickness)
                            high = max(high, thickness)
                            values.append(thickness)

        if count == 0:
            return None

        if agg == "min":
            return low

        if agg == "max":
            return high

        if agg == "count":
            return count

        if agg == "avg":
            return round(total / count, 3)

        if agg == "median":
            l, r = 0, len(values)
            values.sort()
            mid = (l + r) // 2

            if mid % 2:
                return values[mid]
            else:
                return (values[mid-1] + values[mid]) / 2


def parse_query(item):

    try:
        x1, y1, x2, y2, agg = item

        x1 = float(x1)
        y1 = float(y1)
        x2 = float(x2)
        y2 = float(y2)

        if agg not in ("min", "max", "avg", "median", "count"):
            return None

    except Exception as e:
        print(e)

    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1

    x1 = max(0, x1)
    x2 = min(PLATE_SIZE, x2)
    y1 = max(0, y1)
    y2 = min(PLATE_SIZE, y2)
    return x1, y1, x2, y2, agg


def parse_add(item):

    try:
        x, y, thickness = item
        x = float(x)
        y = float(y)
        thickness = float(thickness)

        if thickness < 0:
            return

        if not (0 <= x <= PLATE_SIZE and 0 <= y <= PLATE_SIZE):
            return None

    except Exception as e:
        print(e)

    return x, y, thickness


def run(stream):
    plate = LivePlate()
    res = []
    for query in stream:

        query = query.split(',')

        if query[0] == "QUERY":
            if len(query) != 6:
                continue

            parsed = parse_query(query[1:])
            if parsed is None:
                res.append("error: invalid query")
                continue

            x1, y1, x2, y2, agg = parsed
            result = plate.query(x1, y1, x2, y2, agg)

            if result:
                res.append(result)
            else:
                res.append("error: invalid query")

        elif query[0] == "ADD":
            if len(query) != 4:
                continue

            parsed = parse_add(query[1:])

            if not parsed:
                continue

            x, y, thickness = parse_add(query[1:])

            plate.add(x, y, thickness)

    return res


if __name__ == "__main__":
    for result in run(stream):
        print(result)
