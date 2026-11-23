# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (mock #7)
# ─────────────────────────────────────────────────────────────
#
# "We've got thickness readings from a scan of a pipe section.
#  Each reading says where on the pipe it was taken and how thick
#  the wall was. The team wants to know how many separate damaged
#  areas there are, and how big the worst one is."
#
# Pipe: length 500 mm. Minimum allowed thickness: 8.0 mm.
# Angles are measured from the top of the pipe, clockwise, in degrees.
# z is the distance along the pipe from the start end, in mm.
#
# Each reading is "angle_deg,z_mm,thickness_mm"
#
# ~45 minutes. Ask clarifying questions first.
# Target: something running end to end by the 25-minute mark.
# ─────────────────────────────────────────────────────────────

readings = [
    "340,150,7.2",
    "10,120,7.5",
    "5,250,7.9",
    "160,330,9.0",
    "165,360,7.8",
    "190,310,7.4",
    "abc",
    "250,40,6.9",
    "225,180,7.7",
    "70,450,8.0",
    "120,300",
    "100,220,9.5",
    "280,500,9.1",
    "200,600,9.0",
    "-20,100,9.4",
    "90,90,0",
]

# first we need to convert to their equivalent sections - how do we wanna choose the sections?


def parse(readings, length_mm):
    parsed = []
    garb = []

    for log in readings:

        try:
            ang, z_mm, thickness = log.split(",")

            angle = int(ang) % 360
            z_mm = int(z_mm)
            thickness = float(thickness)

            if z_mm < 0 or thickness <= 0 or z_mm > length_mm:
                garb.append(log)
            else:
                parsed.append({
                    "angle": angle,
                    "z_mm": z_mm,
                    "thickness": thickness
                })
        except:
            garb.append(log)

    return parsed, garb


def migrate_to_grid_cells(readings, len_mm):

    rows = len_mm // 100
    cols = 360 // 30
    for reading in readings:
        reading["row"] = min(reading["z_mm"] // 100, rows - 1)
        reading["col"] = (reading["angle"] // 30) % cols

    return readings


def dedupe_get_lowest(grid, min_thickness_mm):

    cell_min = {}

    for r in grid:
        cell = (r["col"], r["row"])
        cell_min[cell] = min(cell_min.get(cell, float("inf")), r["thickness"])

    return {cell for cell, t in cell_min.items() if t < min_thickness_mm}


def find_largest_area(grid):

    largest = 0
    areas = []
    seen = set()
    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    def dfs(r, c, area):

        if r > 12 or r < 0:
            return 0

        if (r, c) not in grid:
            return 0

        if (r, c) in seen:
            return 0

        seen.add((r, c))
        area.append((r, c))

        res = 1
        for dr, dc in dirs:
            row, col = dr + r, dc + c

            if row >= 12:
                row = 0
            elif row < 0:
                row = 11

            res += dfs(row, col, area)

        return res

    for row, col in grid:

        if (row, col) in seen:
            continue
        area = []
        largest = max(largest, dfs(row, col, area))
        areas.append(area)
    return largest, areas


def damaged_areas(readings, length_mm, min_thickness_mm):

    parsed, garbage = parse(readings, length_mm)
    grid = migrate_to_grid_cells(parsed, length_mm)

    deduped_grid = dedupe_get_lowest(grid, min_thickness_mm)

    largest, areas = find_largest_area(deduped_grid)

    print(largest, areas)


if __name__ == "__main__":
    damaged_areas(readings, 500, 8.0)
