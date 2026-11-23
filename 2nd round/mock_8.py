# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (mock #13: sensor merge)
# ─────────────────────────────────────────────────────────────
#
# "Our ultrasonic thickness readings drift with temperature, so
#  the crawler also carries a temperature probe. The two log
#  separately and their timestamps don't line up. We need one
#  sorted list where each thickness reading has the temperature
#  at (roughly) the moment it was taken."
#
# Thickness log:   "timestamp,thickness_mm"
# Temperature log: "timestamp|temperature"   (exported by a different system)
#
# Talk through your thinking, then a short discussion at the end.
# ─────────────────────────────────────────────────────────────

from datetime import datetime

thickness_log = [
    "2026-11-09T08:00:03,9.6",
    "2026-11-09T08:00:12,9.4",
    "2026-11-09T08:00:07,9.5",
    "2026-11-09T08:00:21,9.1",
    "2026-11-09T08:00:12,9.4",
    "2026-11-09T08:00:30,bad",
    "2026-11-09T08:00:41,8.9",
]

temperature_log = [
    "09/11/2026 08:00:05|41.2C",
    "09/11/2026 08:00:00|41.0C",
    "09/11/2026 08:00:14|105.8F",
    "09/11/2026 08:00:19|41.5C",
    "09/11/2026 08:00:35|42.0C",
    "broken",
]


def convert_far_to_cel(f):
    return (f-32)*5/9


def parse_thickness_log(logs):

    parsed = []
    garbage = []
    seen_ts = set()

    for log in logs:
        try:
            timestamp, thickness = log.split(',')

            timestamp = datetime.fromisoformat(timestamp)

            if (timestamp, thickness) in seen_ts:
                garbage.append(log)
                continue

            seen_ts.add((timestamp, thickness))
            thickness = float(thickness)

            parsed.append({
                "ts": timestamp,
                "thickness": thickness
            })
        except:
            garbage.append(log)

    return parsed, garbage


def parse_temp_log(logs):
    parsed, garbage = [], []
    for log in logs:
        try:
            timestamp, temp = log.split('|')

            timestamp = datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S")

            temp, unit = float(temp[0:-1]), temp[-1]
            if unit == "F":
                temp = convert_far_to_cel(temp)

            parsed.append({
                "ts": timestamp,
                "temperature": temp
            })

        except ValueError as e:
            garbage.append(log)

    return parsed, garbage


def total_seconds_between_timestamps(t1: datetime, t2: datetime):

    return abs(t1-t2).total_seconds()


def merge_logs(temp_logs, thickness_logs, max_time_diff):
    # since the lists are short we can just do a double for loop

    temp_logs.sort(key=lambda i: i["ts"])
    thickness_logs.sort(key=lambda i: i["ts"])

    for thick_log in thickness_logs:
        thick_ts = thick_log["ts"]
        closest = (float("inf"), None)
        for temp_log in temp_logs:

            temp_ts = temp_log["ts"]
            time_diff = total_seconds_between_timestamps(temp_ts, thick_ts)
            if time_diff < closest[0]:
                closest = (time_diff, temp_log)

        if closest[0] <= max_time_diff:
            thick_log["temp"] = closest[1]["temperature"]
        else:
            thick_log["temp"] = None

    return thickness_logs


def merge_thickness_temperature(thickness_log, temperature_log):
    thickness, garb_thick = parse_thickness_log(thickness_log)
    temp, garb = parse_temp_log(temperature_log)
    temp_merged = merge_logs(temp, thickness, 5)

    print(temp_merged)


if __name__ == "__main__":
    merge_thickness_temperature(thickness_log, temperature_log)
