# ─────────────────────────────────────────────────────────────
# Mock #5 (friend's version): merge two sensor logs
# ─────────────────────────────────────────────────────────────
#
# Two sensors log independently. Their timestamps differ by a
# few seconds. Produce ONE list, sorted by time, where each
# thickness reading is paired with the closest position reading.
#
# Rules (what the interviewer would tell you if you asked):
#   - Pair a thickness reading with the CLOSEST position reading
#     in time, but only if it's within 3 seconds. Otherwise its
#     position is None.
#   - Bad thickness rows: reject with a reason.
#   - Both lists may be out of order.
#
# Follow-up (verbal): how would you make the positions more accurate?
# ─────────────────────────────────────────────────────────────

from datetime import datetime

position_log = [
    {"ts": "2026-11-09T10:00:10", "pos_mm": 60},
    {"ts": "2026-11-09T10:00:00", "pos_mm": 0},
    {"ts": "2026-11-09T10:00:20", "pos_mm": 100},
    {"ts": "2026-11-09T10:00:05", "pos_mm": 20},
]

thickness_log = [
    "2026-11-09 10:00:02,9.8",
    "2026-11-09 10:00:11,9.1",
    "2026-11-09 10:00:15,9.4",
    "2026-11-09 10:00:21,8.4",
    "garbage,row",
    "2026-11-09 10:00:06,9.6",
]


def parse_position(pos_log):
    parsed = []
    garbage = []

    for log in pos_log:
        try:
            timestamp = datetime.fromisoformat(log["ts"])
        except ValueError as e:
            garbage.append(log)
            continue

        try:
            pos_mm = int(log["pos_mm"])
            if pos_mm < 0:
                raise ValueError()
        except:
            garbage.append(log)
            continue

        parsed.append({"timestamp": timestamp, "pos_mm": pos_mm})

    return parsed, garbage


def parse_thickness(thick_log):
    parsed, garbage = [], []

    for log in thick_log:
        time, thickness = log.split(",")

        try:
            timestamp = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        except:
            garbage.append(log)
            continue

        try:
            thicknes = float(thickness)
        except:
            garbage.append(log)
            continue

        parsed.append({"timestamp": timestamp, "thickness": thicknes})

    return parsed, garbage


def merge_lists(thickness_log, pos_log, sec_range):
    thickness_log.sort(key=lambda i: i["timestamp"])
    pos_log.sort(key=lambda i: i["timestamp"])

    pos_p = 0
    merged = []

    def time_gap(t1, t2):
        return abs(t1 - t2).total_seconds()

    for row in thickness_log:

        t = row["timestamp"]

        def gap(p): return abs((p["timestamp"] - t).total_seconds())

        # find closest time so we compare this one and the closest one
        while pos_p + 1 < len(pos_log) and time_gap(t, pos_log[pos_p]["timestamp"]) >= time_gap(t, pos_log[pos_p + 1]["timestamp"]):
            merged.append({"timestamp": t.isoformat(
            ), "thickness": None, "pos_mm": pos_log[pos_p]["pos_mm"]})
            pos_p += 1

        pos = pos_log[pos_p]["pos_mm"] if pos_log and gap(
            pos_log[pos_p]) <= sec_range else None
        merged.append({"timestamp": t.isoformat(),
                      "thickness": row["thickness"], "pos_mm": pos})

    return merged


def merge_logs(position_log, thickness_log):

    thickness_parsed, garbage_thick = parse_thickness(thickness_log)
    position_parsed, garbage_pos = parse_position(position_log)

    merged = merge_lists(thickness_parsed, position_parsed, 3)

    print(merged)


if __name__ == "__main__":
    merge_logs(position_log, thickness_log)
