# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (mock #6)
# ─────────────────────────────────────────────────────────────
#
# "A crawler scanned a pipe. Its navigation system logged WHERE it
#  was, and a separate thickness sensor logged WHAT it measured.
#  The two logs aren't in sync.
#  The reliability team wants to know which part of the pipe is
#  thinnest. Can you work that out?"
#
# Pipe: radius 150 mm, length 1000 mm.
# Angles are measured from the top of the pipe, clockwise, in degrees.
# z is the distance along the pipe from the start end, in mm.
#
# ~45 minutes. Ask clarifying questions first.
# Target: something running end to end by the 25-minute mark.
# ─────────────────────────────────────────────────────────────

from datetime import datetime
import math


crawler_log = [
    {"ts": "2026-11-09T10:00:08", "angle_deg": 90,  "z_mm": 200},
    {"ts": "2026-11-09T10:00:00", "angle_deg": 0,   "z_mm": 0},
    {"ts": "2026-11-09T10:00:16", "angle_deg": 350, "z_mm": 400},
    {"ts": "2026-11-09T10:00:04", "angle_deg": 0,   "z_mm": 200},
    {"ts": "2026-11-09T10:00:12", "angle_deg": 90,  "z_mm": 400},
]

# exported from the thickness sensor as "timestamp,thickness_mm"
sensor_log = [
    "2026-11-09 10:00:05,9.2",
    "2026-11-09 10:00:01,9.8",
    "2026-11-09 10:00:13,7.6",
    "bad",
    "2026-11-09 10:00:09,8.1",
    "2026-11-09 10:00:10,-1.0",
    "2026-11-09 10:00:15,7.9",
    "2026-11-09 10:00:30,9.0",
]


def parse_crawler(logs):

    garbage = []
    parsed = []

    for log in logs:
        log["ts"] = datetime.fromisoformat(log["ts"])

    return logs


def parse_sensor(logs):

    garbage = []
    parsed = []
    print('hi')
    for log in logs:
        try:
            ts, thickness = log.split(",")

            time = datetime.fromisoformat(ts)

            thick = float(thickness)
            if thick < 0:
                raise Exception("Thickness is negative")
        except Exception as e:
            garbage.append(log)
            continue

        parsed.append({"ts": time, "thickness": thick})

    return parsed, garbage


def time_difference(t1, t2):

    return abs(t1-t2).total_seconds()


def merge_logs(crawler, sensor):

    merged = []
    leftover = []

    thinnest = None
    for s_log in sensor:

        s_ts = s_log["ts"]

        closest, best_gap = None, float("inf")
        for c_log in crawler:
            gap = time_difference(s_ts, c_log["ts"])

            if gap < best_gap:
                closest = c_log
                best_gap = gap

        if best_gap > 3:
            leftover.append(s_log)
        else:
            merged.append(
                {**s_log, "angle_deg": closest["angle_deg"], "z_mm": closest["z_mm"]})

            if thinnest and thinnest["thickness"] >= s_log["thickness"]:
                thinnest = {
                    **s_log, "angle_deg": closest["angle_deg"], "z_mm": closest["z_mm"]}
            else:
                thinnest = {
                    **s_log, "angle_deg": closest["angle_deg"], "z_mm": closest["z_mm"]}

    return merged, leftover, thinnest


def find_group(angle_deg, z_mm):

    sector = (angle_deg // 30) % 12
    row = min(int(z_mm) // 100, 9)

    return sector, row


def thinnest_region(crawler_log, sensor_log, radius_mm, length_mm):
    crawler_parsed = parse_crawler(crawler_log)
    sensor_parsed, garbage = parse_sensor(sensor_log)

    merged, unmerged, thinnest = merge_logs(crawler_parsed, sensor_parsed)
    sector, row = find_group(thinnest["angle_deg"], thinnest["z_mm"])
    print(f"The thinnest is {thinnest} with sector and row {sector}, {row}")


if __name__ == "__main__":
    thinnest_region(crawler_log, sensor_log, 1, 2)
