# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (Problem 10: Sensor Health)
# ─────────────────────────────────────────────────────────────
#
# "Before I look at thickness I want to know if the gauge was
#  behaving. Three things go wrong with these: it stops reporting
#  for a while, it freezes and repeats the same number, or it throws
#  out one crazy reading. Go through the feed and tell me where each
#  of those happened."
#
# Feed lines: "time_s,thickness_mm"   (nominally one reading per second)
#
# Report:
#   - dropouts: gaps of more than MAX_GAP seconds between consecutive
#     readings, as (last_time_before, first_time_after, seconds)
#   - stuck runs: the same value STUCK_COUNT or more times in a row,
#     as (start_time, end_time, value, count)
#   - spikes: a reading more than SPIKE_MM away from the average of
#     the WINDOW readings before it, as (time, value, expected)
#   - the number of valid readings
#
# ~40 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────
from collections import deque

feed = [
    "0,9.5", "1,9.4", "2,9.5", "3,9.3",
    "5,3.1", "6,9.3", "7,9.2",
    "ERR", "9,", "10,-1.0",
    "11,9.2", "12,9.1", "13,9.1", "14,9.1", "15,9.1", "16,9.1",
    "4,9.4",
    "17,9.0", "18,8.9", "6,9.3",
    "19,8.8", "20,8.8", "21,8.8", "22,8.8",
]

MAX_GAP = 3
STUCK_COUNT = 4
SPIKE_MM = 2.0
WINDOW = 3


def parse_data(feed):
    parsed = []
    dropped = 0
    seen_times = set()
    for item in feed:
        try:
            time, thickness = item.split(',')

            time = int(time)
            thickness = float(thickness)

            if time in seen_times:
                dropped += 1          # or count duplicates separately
                continue
            if thickness <= 0:
                dropped += 1
                continue

            seen_times.add(time)
            parsed.append({
                "time": time,
                "thickness": thickness
            })
        except ValueError as e:
            dropped += 1

    return parsed, dropped


def collect_results(data):
    data.sort(key=lambda d: d["time"])

    stuck_count = 0
    stuck_val = 0

    window = deque()
    window_total = 0

    spikes = []
    stuck_readings = []
    gaps = []

    for i, reading in enumerate(data):
        no = i + 1
        time = reading["time"]
        thickness = reading["thickness"]

        if i == 0:
            stuck_count += 1
            stuck_val = thickness
            running_average = thickness
            total += thickness
            continue

        # thickness
        if stuck_val == thickness:
            stuck_count += 1
        elif stuck_count >= STUCK_COUNT:
            stuck_readings.append((
                data[i-stuck_count]["time"], data[i-1]["time"], stuck_val, stuck_count))
            stuck_count = 1
            stuck_val = thickness
        else:
            stuck_count = 1
            stuck_val = thickness

        if abs(time - data[i-1]["time"]) > MAX_GAP:
            gaps.append((data[i-1]["time"], time,
                        abs(data[i-1]["time"] - time)))
        # spikes
        if abs(running_average-thickness) > SPIKE_MM:
            spikes.append((time, thickness, running_average))

        total += thickness
        running_average = (total / no)

    return spikes, stuck_readings, gaps


def sensor_health(feed):
    data, drop = parse_data(feed)
    spikes, stuck, gaps = collect_results(data)

    return {
        "spikes": spikes,
        "stuck": stuck,
        "gaps": gaps
    }


if __name__ == "__main__":
    print(sensor_health(feed))
