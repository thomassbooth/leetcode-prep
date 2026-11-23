# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (Remaining Life)
# ─────────────────────────────────────────────────────────────
#
# "We've inspected this tank floor three times now. The plant
#  manager has to plan the next shutdown and needs to know which
#  areas of the floor will hit minimum allowed thickness first,
#  and roughly when."
#
# Readings: "inspection_date,x_mm,y_mm,thickness_mm"
#   - Dates are ISO format, e.g. "2025-09-01".
#   - The floor is 150 x 150 mm (it's a test section), split into
#     50 mm squares.
#   - The robot doesn't revisit the exact same points each
#     inspection - positions differ every time.
#   - Inspections were NOT evenly spaced.
#   - Steel thinner than MIN_ALLOWED must be repaired.
#   - It's field data, so expect some bad lines.
#
# For each square, report:i
#   (square, current_thickness, corrosion_rate_mm_per_year, years_left)
# ordered so the plant manager sees the most urgent first.
#
# ~40 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────

# sol
# parse readings -> drop any not on overall width outside of range
# drop thickness 0 or below
#
# we can bin the readings into their cells -> end readings get bucketed -1 below so we go from 0 -> end
#

from datetime import date
from collections import defaultdict

readings = [
    "2024-03-01,10,10,10.0",
    "2024-03-01,40,30,10.2",
    "2024-03-01,60,20,8.0",
    "2024-03-01,120,40,9.9",
    "2024-03-01,20,70,6.0",
    "2024-03-01,30,120,9.0",
    "2024-03-01,130,140,5.5",
    "2025-09-01,15,20,9.4",
    "2025-09-01,70,10,7.0",
    "2025-09-01,90,45,7.3",
    "2025-09-01,110,10,10.1",
    "2025-09-01,40,140,8.9",
    "2025-09-01,140,120,5.0",
    "2026-03-01,30,30,9.0",
    "2026-03-01,80,30,6.1",
    "2026-03-01,140,20,10.0",
    "2026-03-01,10,90,5.4",
    "2026-03-01,70,70,7.5",
    "2026-03-01,20,110,8.95",
    "2026-03-01,120,130,4.6",
    "2025-13-01,50,50,7.0",
    "ERR",
    "2026-03-01,60,60",
    "2026-03-01,160,10,9.0",
    "2025-09-01,10,10,-1",
    "2024-03-01,60,20,8.0",
]

PLATE_SIZE = 150
BIN_SIZE = 50
MIN_ALLOWED = 5.0


def parse_data(readings):

    parsed = []
    dropped = 0

    for reading in readings:
        try:
            ts, x, y, thickness = reading.split(',')

            ts = date.fromisoformat(ts)

            x = int(x)
            y = int(y)
            thickness = float(thickness)

            if x < 0 or y < 0 or x > PLATE_SIZE or y > PLATE_SIZE:
                dropped += 1
                continue

            if thickness <= 0:
                dropped += 1
                continue

            parsed.append({
                "time": ts,
                "x": x,
                "y": y,
                "thickness": thickness
            })
        except Exception as e:
            print(e)
            dropped += 1

    return parsed, dropped


def get_cell(x, y):

    last = (PLATE_SIZE // BIN_SIZE) - 1

    return (min(x//BIN_SIZE, last), min(y//BIN_SIZE, last))


def bin_data(readings):
    import math

    bins = defaultdict(lambda: defaultdict(lambda: math.inf))

    for r in readings:
        cell = get_cell(r["x"], r["y"])
        d = r["time"]
        bins[cell][d] = min(bins[cell][d], r["thickness"])

    return bins


def years_between(d1, d2):

    return abs(d1 - d2).days / 364


def rate_of_change(min_d, max_d, min_t, max_t):

    return (max_t - min_t) / years_between(min_d, max_d)  # thickness/year


def results(bins: dict):

    res = []
    for cell, dates in bins.items():

        if len(bins[cell]) < 2:
            continue

        first_date = min(dates)
        last_date = max(dates)
        first_t = bins[cell][first_date]
        last_t = bins[cell][last_date]

        roc = rate_of_change(first_date, last_date, first_t, last_t)

        if last_t < MIN_ALLOWED:
            years_left = 0
        elif roc >= 0:
            years_left = float("inf")
        else:
            years_left = (last_t - MIN_ALLOWED) / -roc

        res.append({
            "years_left": years_left,
            "square": cell,
            "corrosion_rate": roc,
            "current_thickness": last_t
        })

    return res


def remaining_life(readings):
    parsed, dropped = parse_data(readings)
    bins = bin_data(parsed)
    res = results(bins)

    res.sort(key=lambda i: i["years_left"])
    return res


if __name__ == "__main__":
    for row in remaining_life(readings):
        print(row)
