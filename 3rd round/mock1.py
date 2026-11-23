"""
Wall thickness inspection - starter.

A sensor was moved over a steel wall. At many spots it recorded:
    x_mm, y_mm, thickness_mm

The wall was 12.7 mm thick when new.

Question: where are the dangerously thin areas, how big are they,
and which is the worst?

Run:  python3 starter.py readings.csv
"""

import pprint
from collections import deque
import math

NOMINAL_MM = 12.7
CELL_M = 0.1
THIN_MM = 10.0

# (x_m, y_m, thickness_mm)
READINGS = [
    (0.587, 0.451, 12.69), (0.832, 0.385,
                            12.42), (0.575, 0.162, 9.23), (0.719, 0.355, 12.1),
    (0.56, 0.772, 12.35), (0.366, 0.414,
                           None), (0.554, 0.03, 12.11), (0.471, 0.539, 12.5),
    (0.02, 0.71, 12.47), (0.926, 0.334, 12.61), (0.373,
                                                 0.519, 12.48), (0.378, 0.634, 12.19),
    (0.283, 0.737, 12.47), (0.273, 0.263, 0.0), (0.556,
                                                 0.763, 12.57), (0.759, 0.238, 12.68),
    (0.342, 0.229, 9.52), (0.635, 0.325, 12.18), (0.954,
                                                  0.65, 12.39), (0.833, 0.459, 12.69),
    (0.486, 0.762, 12.28), (0.11, 0.464, 12.46), (0.728,
                                                  0.533, 6.06), (0.074, 0.085, 12.55),
    (0.877, 0.128, ''), (0.323, 0.114, 9.8), (0.054,
                                              0.356, 12.25), (0.181, 0.234, 9.78),
    (0.422, 0.14, 12.34), (0.642, 0.532, 12.1), (0.313,
                                                 0.449, 12.65), (0.562, 0.269, 12.31),
    (0.788, 0.75, 12.26), (0.889, 0.049, 12.29), (0.378,
                                                  0.788, 12.7), (0.787, 0.683, 12.33),
    (0.82, 0.16, 12.39), (0.082, 0.219, 12.49), (0.432,
                                                 0.373, 12.15), (0.928, 0.776, 12.14),
    (0.286, 0.617, 12.12), (0.862, 0.458,
                            12.38), (0.834, 0.652, 12.3), (0.912, 0.768, 0.0),
    (0.322, 0.165, 9.25), (0.32, 0.469, 12.6), (0.562,
                                                0.586, 'n/a'), (0.648, 0.228, 9.02),
    (0.688, 0.69, 13.1), (0.468, 0.048, 12.39), (0.27,
                                                 0.384, 12.22), (0.972, 0.583, 12.27),
    (0.657, 0.429, 12.47), (0.067, 0.021, float("nan")
                            ), (0.618, 0.754, 12.47), (0.032, 0.483, 12.23),
    (0.239, 0.256, 9.67), (0.266, 0.015,
                           12.39), (0.466, 0.632, 9.9), (0.775, 0.061, 12.35),
    (0.983, 0.241, 12.39), (0.656, 0.787,
                            12.3), (0.677, 0.64, 12.17), (0.76, 0.481, 12.18),
    (0.45, 0.33), (0.473, 0.472, 12.32), (0.871,
                                          0.534, 5.87), (0.956, 0.167, 12.36),
    (0.577, 0.585, 12.2), (0.577, 0.38, 12.31), (0.922,
                                                 0.657, 12.3), (0.758, 0.155, 12.19),
    (0.449, 0.672, 10.1), (0.122, 0.315, 12.2), (0.613,
                                                 0.347, 12.22), (0.012, 0.147, 12.65),
    (0.214, 0.224, 9.21), (0.612, 0.023, 12.53), (0.27,
                                                  0.178, 9.21), (0.954, 0.011, 12.63),
    (0.83, 0.331, 12.57), (0.027, 0.727,
                           12.62), (0.46, 0.25, 12.68), (0.126, 0.185, 9.61),
    (0.568, 0.668, 12.51), (0.977, 0.466, 12.14), (0.175,
                                                   0.748, 12.29), (0.873, 0.276, 12.28),
    (0.023, 0.474, 12.56), (0.346, 0.344, 12.6), (0.946,
                                                  0.083, 12.25), (0.133, 0.087, 12.62),
    (0.27, 0.574, 8.26), (0.628, 0.165, 12.49), (0.733,
                                                 0.383, -1.5), (0.87, 0.757, 12.32),
    (0.335, 0.035, 12.43), (0.238, 0.452, 12.31),
]


def parse_data(readings, thickness):

    parsed = []
    garb = []

    for reading in readings:

        try:
            x, y, t = reading
            x = float(x)
            y = float(y)
            t = float(t)
            if t > thickness or t <= 0:
                garb.append(reading)
                continue

            if t is math.isnan:
                garb.append(reading)
                continue

            parsed.append((x, y, t))
        except:
            garb.append(reading)

    return parsed, garb


def cell_loc(x, y, cell_size=CELL_M):

    x, y = math.floor(x / cell_size), math.floor(y/cell_size)

    return x, y


def collect_mins(readings):

    mins = {}

    for x, y, t in readings:

        cell = cell_loc(x, y)
        if cell not in mins or mins[cell] > t:
            mins[cell] = t

    return mins


def flag_data(mins, nominal=NOMINAL_MM, loss=0.2):
    limit = nominal * (1-loss)
    flagged = sorted(((k, t) for k, t in mins.items() if t <=
                     limit), key=lambda kv: (kv[1], kv[0]))

    return dict(flagged)


def bfs(start_x, start_y, flagged, seen):
    q = deque()
    q.append((start_x, start_y))
    patch = []
    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    smallest = flagged[(start_x, start_y)]
    seen.add((start_x, start_y))
    while q:

        for _ in range(len(q)):
            x, y = q.popleft()
            patch.append((x, y))

            for dx, dy in dirs:
                nb = (x + dx, y + dy)
                if nb in flagged and nb not in seen:
                    smallest = min(smallest, flagged[nb])
                    seen.add(nb)
                    q.append(nb)

    return patch, smallest


def find_patches(flagged, cell=CELL_M):
    seen = set()
    patches = []

    for x, y in flagged:

        if (x, y) in seen:
            continue

        patch, smallest = bfs(x, y, flagged, seen)
        patches.append({
            "n_cells": len(patch),
            "area_m2": len(patch) * cell * cell,
            "min_thickness": smallest,
            "cells": patch
        }
        )

    patches.sort(key=lambda p: (p["min_thickness"], p["n_cells"]))
    pprint.pprint(patches)


def main():
    parsed, garb = parse_data(READINGS, NOMINAL_MM)
    mins = collect_mins(parsed)
    flagged = flag_data(mins)
    patches = find_patches(flagged)


if __name__ == "__main__":
    main()
