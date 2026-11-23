# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (Problem 2: Thickness Map)
# ─────────────────────────────────────────────────────────────
#
# "Our robot crawled over a 150 mm x 150 mm steel test plate taking
#  thickness readings. The inspectors don't want thousands of raw
#  points - they want the plate split into a grid of squares, and to
#  be able to ask for the average, minimum, maximum or median
#  thickness in any square."
#
# Readings come in as "x_mm,y_mm,thickness_mm".
#   - x is from the left edge of the plate, y from the top edge.
#   - The robot doesn't stop on a neat grid - positions are wherever
#     it happened to be when the probe fired.
#   - Readings arrive in no particular order.
#   - It's field data, so expect some bad lines.
#
# Build something the inspectors can load readings into and then
# query. Grid squares are BIN_SIZE mm on each side.
#
# Supported aggregations: "avg", "min", "max", "median".
#
# ~40 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────
import math
from collections import defaultdict

readings = [
    "12.5,8.0,9.8",
    "30.0,45.5,9.6",
    "49.9,10.0,9.9",
    "50.0,10.0,6.1",
    "75.2,20.1,5.8",
    "60.0,49.0,6.4",
    "99.0,0.0,6.0",
    "10.0,60.0,4.2",
    "20.0,70.0,4.4",
    "40.0,99.9,3.1",
    "120.0,130.0,8.8",
    "x,10,5.0",
    "10,10",
    "-5.0,20.0,9.0",
    "30.0,45.5,9.6",
    "55.0,15.0,0",
    "130,140,nan",
    "160.0,20.0,7.5",
]

PLATE_SIZE = 150
BIN_SIZE = 50


class ThicknessMap:
    def __init__(self, plate_size, bin_size):
        self.cells = plate_size // bin_size
        self.plate_size = plate_size
        self.bin_size = bin_size

        # each key is a (x, y) pos
        self.grid = defaultdict(lambda: {
            "readings": [],
            "min": float("inf"),
            "max": float("-inf"),
            "sum": 0,
            "length": 0,
            "sorted": False
        })

    def __parse_reading(self, line):

        try:
            x, y, thickness = line.split(",")
            x = float(x)
            y = float(y)
            thickness = float(thickness)

            if math.isnan(thickness) or thickness <= 0:

                return None, None, None

            if x >= self.plate_size or y >= self.plate_size:
                return None, None, None

            if x < 0 or y < 0:
                return None, None, None

            return x, y, thickness

        except Exception as e:

            return None, None, None

    def add_reading(self, line):

        x, y, thickness = self.__parse_reading(line)
        if not (x or y or thickness):
            return

        cell = (x // self.bin_size, y // self.bin_size)

        self.grid[cell]["readings"].append(
            {"x": x, "y": y, "thickness": thickness})

        if thickness < self.grid[cell]["min"]:
            self.grid[cell]["min"] = thickness

        if thickness > self.grid[cell]["max"]:
            self.grid[cell]["max"] = thickness

        self.grid[cell]["sorted"] = False
        self.grid[cell]["sum"] += thickness
        self.grid[cell]["length"] += 1

    def __check_cell(self, x, y):

        cell = self.grid[(x, y)]

        return cell

    def __average(self, x, y):

        cell = self.__check_cell(x, y)

        return (cell["sum"] / cell["length"])

    def __median(self, x, y):

        cell = self.__check_cell(x, y)

        if not cell["sorted"]:
            cell["readings"].sort(key=lambda r: r["thickness"])
            cell["sorted"] = True

        r = cell["readings"]
        n = len(r)
        mid = n // 2
        if n % 2:
            return r[mid]["thickness"]
        return (r[mid - 1]["thickness"] + r[mid]["thickness"]) / 2

    def __min(self, x, y):

        cell = self.__check_cell(x, y)

        return cell["min"]

    def __max(self, x, y):

        cell = self.__check_cell(x, y)

        return cell["max"]

    def query(self, bin_x, bin_y, agg):

        if self.grid[(bin_x, bin_y)]["length"] == 0:

            return "No data in this cell"

        queries = {
            "avg": self.__average,
            "min": self.__min,
            "max": self.__max,
            "median": self.__median,
        }

        if agg in queries:

            return queries[agg](bin_x, bin_y)
        else:
            return "Not a valid query"


if __name__ == "__main__":
    m = ThicknessMap(PLATE_SIZE, BIN_SIZE)
    for line in readings:
        m.add_reading(line)

    print(m.query(0, 0, "avg"))
    print(m.query(0, 0, "min"))
    print(m.query(1, 0, "median"))
    print(m.query(0, 1, "max"))
    print(m.query(2, 2, "median"))
    print(m.query(1, 1, "avg"))
    print(m.query(1, 0, "mode"))
