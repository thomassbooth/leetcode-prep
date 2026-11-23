# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (Problem 7: Where Was The Robot?)
# ─────────────────────────────────────────────────────────────
#
# "The robot doesn't give us x and y. It gives us a log: I turned to
#  this heading, I drove this far, I took a reading. Every so often
#  the tripod on the deck gets a clean look at it and tells us where
#  it REALLY is. I need the thin spots on the plate drawing, and I
#  need to know how far off the robot's own idea of its position was."
#
# Log lines, in order:
#   "MOVE,heading_deg,distance_mm"   heading 0 = +x, 90 = +y
#   "READ,thickness_mm"              taken at the robot's current position
#   "FIX,x_mm,y_mm"                  true position from the tripod
#
# The robot starts at START. The plate is 200 x 200 mm, squares are 50 mm.
#
# Report:
#   - each valid reading with its plate position (x, y) and square (col, row)
#   - the thin squares (below MIN_THICKNESS) with their minimum, worst first
#   - the drift at each FIX (distance between where the robot thought it
#     was and where it really was), and the largest drift seen
#
# ~40 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────
import math
from collections import defaultdict

log = [
    "READ,9.5",
    "MOVE,0,50",   "READ,8.1",
    "MOVE,0,50",   "READ,9.9",
    "MOVE,90,50",  "READ,9.1",
    "FIX,120,80",
    "MOVE,180,50", "READ,5.1",
    "ERR",
    "MOVE,180,50", "READ,6.2", "READ,",
    "MOVE,90,50",  "READ,9.8",
    "MOVE,abc,50",
    "FIX,30,128",
    "MOVE,0,50",   "READ,5.5",
    "JUMP,10,10",
    "MOVE,0,150",  "READ,9.0",
    "MOVE,180,60", "READ,4.8", "READ,-1.0",
]

START = (25.0, 25.0)
PLATE_SIZE = 200
BIN_SIZE = 50
MIN_THICKNESS = 6.0


def parse_log(logs):

    parsed_logs = []
    dropped = 0

    for log in logs:
        try:
            split_log = log.split(',')
            cmd = split_log[0]
            if cmd == "MOVE":
                heading = float(split_log[1])
                dist = float(split_log[2])

                parsed_logs.append({
                    "cmd": cmd,
                    "heading": heading,
                    "dist": dist
                })

            elif cmd == "FIX":
                x = int(split_log[1])
                y = int(split_log[2])
                parsed_logs.append({
                    "cmd": cmd,
                    "x": x,
                    "y": y
                })

            elif cmd == "READ":
                thickness = float(split_log[1])
                parsed_logs.append({
                    "cmd": cmd,
                    "thickness": thickness
                })
            else:
                dropped += 1
        except Exception as e:
            dropped += 1
    return parsed_logs, dropped


def cmd_fix(x, y, act_x, act_y):

    return round(math.hypot(x - act_x, y - act_y), 2)


def cmd_move(x_start, y_start, heading, dist):

    dx = dist * math.cos(math.radians(heading))
    dy = dist * math.sin(math.radians(heading))

    return x_start + dx, y_start + dy


def process_cmds(logs):

    x, y = START
    bins = defaultdict(list)
    drift = []
    off_plate = 0
    for log in logs:
        cmd = log["cmd"]

        if cmd == "MOVE":
            x, y = cmd_move(x, y, log["heading"], log["dist"])
        elif cmd == "FIX":
            dist = cmd_fix(log["x"], log["y"], x, y)
            x, y = log["x"], log["y"]
            drift.append({"drift": dist})
        elif cmd == "READ":
            thickness = log["thickness"]
            if thickness <= 0:
                continue
            if not (0 <= x <= PLATE_SIZE and 0 <= y <= PLATE_SIZE):
                off_plate += 1
                continue
            bins[get_cell(x, y)].append({
                "thickness": thickness,
                "x": round(x, 2), "y": round(y, 2),
            })
    return bins, drift, off_plate


def get_cell(x, y):
    last = PLATE_SIZE // BIN_SIZE - 1

    return (min(x // BIN_SIZE, last), min(y // BIN_SIZE, last))


def binned_results(bins, drift, off_plate):

    thin = []
    for cell, cell_readings in bins.items():
        lowest = min(r["thickness"] for r in cell_readings)

        if lowest < MIN_THICKNESS:
            thin.append({"cell": cell, "min_thickness": lowest})

    thin.sort(key=lambda t: t["min_thickness"])

    return {
        "drift": drift,
        "thin_squares": thin,
        "valid_readings": bins,
        "max drift": max(value["drift"] for value in drift),
        "res off plate": off_plate
    }


def robot_report(log):
    logs, dropped = parse_log(log)
    bins, drift, off_plate = process_cmds(logs)
    res = binned_results(bins, drift, off_plate)
    return res


if __name__ == "__main__":
    print(robot_report(log))
