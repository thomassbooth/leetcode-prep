# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (Problem 2: Sensor Fusion)
# ─────────────────────────────────────────────────────────────
#
# "The thickness readings from yesterday's crawler run are no use
#  to us without knowing WHERE on the wall each one was taken.
#  Can you give us a position for every thickness reading?"
#
# The robot has two sensors that log to the same file:
#   - "ut"  : ultrasonic wall thickness, in mm
#   - "pos" : the robot's position along the wall, in cm
#
# Each line is "time_s,sensor,value".
#   - The two sensors are NOT synchronised: they fire at different
#     times and at different rates.
#   - Lines were written by different threads, so they're out of order.
#   - Some lines were logged twice.
#   - It's field data, so expect some bad lines.
#
# The robot moves smoothly between position readings, so you can
# estimate where it was at any moment between two of them.
#
# If the position sensor went quiet for more than MAX_GAP seconds,
# the customer does NOT want a guessed position for readings in
# that gap.
#
# Return (time_s, thickness_mm, position_cm) for every thickness
# reading you can place, in time order, position to 2 dp.
#
# ~30 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────


# sol
# parse data into two lists
# sort the position times
# loop through the sensor readings and for each reading we need to find its two closest position readings, left and right of it.
# we can do this using binary search.

log = [
    "1.0,pos,10.0",
    "0.0,pos,0.0",
    "0.5,ut,9.8",
    "0.5,ut,9.8",
    "",
    "garbage",
    "1.0,ut,9.5",
    "1.5,ut,9.1",
    "2.0,pos,20.0",
    "2.5,ut,8.0",
    "9.0,pos,90.0",
    "6.0,ut,7.0",
    "-1,ut,9.9",
    "3.0,ut,abc",
]

MAX_GAP = 3.0


def parse_logs(logs):

    pos_logs = []
    ut_logs = []
    times_seen = set()

    dropped = 0

    for log in logs:

        try:
            time, type, res = log.split(",")

            time = float(time)

            # we can just skip as in our data it has the same value
            if (time, type) in times_seen:
                continue

            if type not in ("ut", "pos"):
                dropped += 1
                continue

            res = float(res)

            if type == "ut":
                ut_logs.append({
                    "time": time,
                    "val": res
                })
            else:
                pos_logs.append({
                    "time": time,
                    "val": res
                })

            times_seen.add((time, type))
        except:
            dropped += 1

    pos_logs.sort(key=lambda u: u["time"])

    return ut_logs, pos_logs, dropped


def binary_search(time, pos_logs):

    l = 0
    r = len(pos_logs) - 1

    while l <= r:

        mid = l + ((r-l)//2)

        if pos_logs[mid]["time"] > time:
            r = mid - 1
        elif pos_logs[mid]["time"] < time:
            l = mid + 1
        else:
            return mid, mid

    return r, l


def pair_pos_ut(ut_logs, pos_logs, max_gap):

    final_readings = []
    paired_readings = []
    dropped = 0
    for ut_log in ut_logs:
        time = ut_log["time"]

        l, r = binary_search(time, pos_logs)

        # out of bounds
        if l < 0 or r >= len(pos_logs):
            dropped += 1
            continue

        # position is found, no need to interpolate
        if l == r:
            final_readings.append({
                "time": time,
                "pos": pos_logs[l]["val"],
                "thickness": ut_log["val"]
            })
            continue

        if abs(pos_logs[l]["time"] - pos_logs[r]["time"]) > max_gap:
            dropped += 1
            continue

        paired_readings.append({
            "time": time,
            "lower_pos": pos_logs[l],
            "upper_pos": pos_logs[r],
            "thickness": ut_log["val"]
        })

    return final_readings, paired_readings, 0


def interpolate_pairs(paired):

    final = []
    for paired_log in paired:

        pos1 = paired_log["lower_pos"]["val"]
        pos2 = paired_log["upper_pos"]["val"]
        time1 = paired_log["lower_pos"]["time"]
        time2 = paired_log["upper_pos"]["time"]
        time = paired_log["time"]

        m = (pos2 - pos1) / (time2 - time1)
        c = pos1 - (m * time1)

        pos = m * time + c

        final.append(
            {"time": paired_log["time"], "pos": pos, "thickness": paired_log["thickness"]})

    return final


def place_readings(log, max_gap):

    ut_logs, pos_logs, dropped = parse_logs(log)
    final, paired, dropped = pair_pos_ut(ut_logs, pos_logs, max_gap)

    final_2 = interpolate_pairs(paired)
    final = final + final_2

    print(final)
    pass


if __name__ == "__main__":
    print(place_readings(log, MAX_GAP))
