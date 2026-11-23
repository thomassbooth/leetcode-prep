# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (Problem 5: Corrosion Rate)
# ─────────────────────────────────────────────────────────────
#
# "We've scanned this plate three times now. I don't just want to
#  know what's thin today, I want to know what's GOING to be thin.
#  Tell me which squares will hit minimum thickness in the next
#  five years, soonest first, so I can plan the repairs."
#
# Readings: "inspection_date,x_mm,y_mm,thickness_mm"
# Plate is 200 x 200 mm. Grid squares are 50 mm.
#
# For each at-risk square report:
#   - the square (col, row)
#   - latest thickness
#   - corrosion rate in mm/year
#   - years remaining until it reaches MIN_THICKNESS
# Sorted soonest first.
#
# ~40 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────
from collections import defaultdict
from datetime import datetime

readings = [
    "2026-06-01,11,12,9.2",   "2022-06-01,10,10,10.0",  "2024-06-01,12,14,9.6",
    "2022-06-01,60,20,9.0",   "2026-06-01,70,30,7.0",   "2024-06-01,120,20,9.9",
    "2022-06-01,110,30,9.8",  "2026-06-01,130,10,10.0", "2026-06-01,160,10,8.0",
    "2024-06-01,30,80,7.0",   "2022-06-01,20,70,8.0",   "2026-06-01,25,75,6.4",
    "2022-06-01,70,80,7.5",   "2026-06-01,75,85,5.5",   "2024-06-01,80,90,6.5",
    "2024-06-01,120,60,9.0",  "2026-06-01,130,70,8.8",  "2022-06-01,170,170,9.0",
    "2022-06-01,180,180,8.6", "2026-06-01,175,175,7.4",
    "ERR", "2024-06-01,60,,8.0", "2026-06-01,210,10,9.0",
    "2026-06-01,25,75,6.4", "2025-13-01,10,10,9.0",
]

PLATE_SIZE = 200
BIN_SIZE = 50
MIN_THICKNESS = 6.0
HORIZON_YEARS = 5

# sol
# parse data
# bucket data into cells
# for each cell work out its decay rate -> there must be atleast a min of 2 readings to calcuate a decay rate
# if theres more than 1 then just take the min/max and calculate the time diference and the rate of change to work out the last. (min, max dates that is)


def parse_readings(readings):
    parsed = []
    dropped = 0

    for reading in readings:
        try:
            time, x, y, thickness = reading.split(',')

            time = datetime.fromisoformat(time)
            x = float(x)
            y = float(y)
            thickness = float(thickness)

            if thickness <= 0:
                dropped += 1
                continue

            if x < 0 or x > PLATE_SIZE or y < 0 or y > PLATE_SIZE:
                dropped += 1
                continue

            parsed.append({
                "x": x,
                "y": y,
                "thickness": thickness,
                "time": time
            })

        except Exception as e:
            print(e)

    return parsed, dropped


def get_cell(x, y):
    x = min(x // BIN_SIZE, (PLATE_SIZE // BIN_SIZE) - 1)
    y = min(y // BIN_SIZE, (PLATE_SIZE // BIN_SIZE) - 1)

    return (x, y)


def bin_readings(readings):

    bins = defaultdict(list)

    for reading in readings:
        x, y = reading["x"], reading["y"]

        cell = get_cell(x, y)

        bins[cell].append(reading)

    return bins


def parse_bins(bins):

    bin_data = []

    for bin, readings in bins.items():

        dates = {}

        for reading in readings:
            dates[reading["time"]] = reading

        if len(dates) < 2:
            continue

        min_date = min(dates.keys())
        max_date = max(dates.keys())
        first = dates[min_date]["thickness"]
        latest = dates[max_date]["thickness"]
        date_diff_years = (max_date - min_date).days / 365

        thickness_diff = first - latest

        rate_of_change = thickness_diff / date_diff_years

        time_to_min = (latest -
                       MIN_THICKNESS) / rate_of_change

        if time_to_min >= 5 or rate_of_change <= 0:
            continue

        bin_data.append({
            "rate_of_change": round(rate_of_change, 3),
            "latest_thickness": latest,
            "time_to_min": max(0, round(time_to_min, 3)),
            "bin": (int(bin[0]), int(bin[1]))
        })

    bin_data.sort(key=lambda b: b["time_to_min"])
    return bin_data


def at_risk_squares(readings):
    parsed, dropped = parse_readings(readings)

    bins = bin_readings(parsed)

    bin_data = parse_bins(bins)

    return bin_data


if __name__ == "__main__":
    for row in at_risk_squares(readings):
        print(row)
