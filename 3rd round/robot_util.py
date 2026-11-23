# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (Problem 8: Robot Utilisation)
# ─────────────────────────────────────────────────────────────
#
# "I've got three robots on this job and I'm paying for all of them
#  for the whole shift. I want to know how much of the shift each one
#  was actually scanning, when each one was sitting idle, and whether
#  there were stretches when NOTHING was scanning at all."
#
# Sessions: "robot_id,start_time,end_time"   (24h clock, HH:MM)
# The shift runs from SHIFT_START to SHIFT_END.
#
# Report:
#   - per robot: minutes scanning, utilisation %, and idle gaps as (start, end)
#   - an idle list: every idle gap of at least MIN_IDLE minutes, as
#     (robot, start, end, minutes), longest first
#   - the stretches when no robot at all was scanning, and the % of
#     the shift when at least one robot was
#
# Show times in the output as HH:MM.
#
# ~40 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────
from collections import defaultdict
from pprint import pprint

sessions = [
    "R1,08:00,10:00", "R1,09:30,11:00", "R1,13:00,12:00", "R1,15:00,16:30",
    "R2,07:30,08:45", "R2,08:45,10:15", "R2,10:30,10:40", "R2,14:00,15:00",
    "ERR", "R4,09:00,10:00", "R1,09:00,09:00", "R2,25:00,10:00",
    "R1,08:00,10:00",
]

ROBOTS = ["R1", "R2", "R3"]
SHIFT_START = "08:00"
SHIFT_END = "16:00"
MIN_IDLE = 30


def to_mins(time):
    hr, mins = time.split(":")
    h, m = int(hr), int(mins)
    if not (0 <= h < 24 and 0 <= m < 60):
        raise ValueError(f"bad time: {s}")

    return h * 60 + m


def parse_data(sessions):

    data = []
    dropped = 0

    for session in sessions:
        try:
            robot, start, end = session.split(',')
            start_mins = to_mins(start)
            end_mins = to_mins(end)

            if start_mins < to_mins(SHIFT_START) and end_mins < to_mins(SHIFT_START):
                dropped += 1
                continue

            if start_mins > to_mins(SHIFT_END) and end_mins > (SHIFT_END):
                dropped += 1
                continue

            if start_mins > end_mins:
                start_mins, end_mins = end_mins, start_mins

            start_mins = max(start_mins, to_mins(SHIFT_START))
            end_mins = min(end_mins, to_mins(SHIFT_END))

            if start_mins == end_mins:
                dropped += 1
                continue

            data.append({
                "start_min": start_mins,
                "end_mins": end_mins,
                "robot": robot,
                "start": start,
                "end": end
            })
        except Exception as e:
            print(e)
            dropped += 1

    return data, dropped


def group_sessions(sessions):

    robots = {robot: [] for robot in ROBOTS}
    for session in sessions:
        robot = session["robot"]
        if robot in robots:
            robots[robot].append(
                (session["start_min"], session["end_mins"], session["start"], session["end"]))

    print(robots)
    return robots


def merge_intervals(robots):

    robots_merged = {}
    for robot, robot_intervals in robots.items():
        robot_intervals.sort(key=lambda i: i[0])

        merged_intervals = []
        for interval in robot_intervals:
            start_mins, end_mins, start, end = interval

            if not merged_intervals:
                merged_intervals.append([start_mins, end_mins])
                continue

            if start_mins < merged_intervals[-1][1]:
                merged_intervals[-1][1] = max(merged_intervals[-1]
                                              [1], end_mins)
            else:
                merged_intervals.append([start_mins, end_mins])

        robots_merged[robot] = merged_intervals

    return robots_merged


def build_robot_report(robot_intervals):

    report = {}
    for robot, intervals in robot_intervals.items():

        missing_times = []
        total_time = 0

        prev_end = to_mins(SHIFT_START)
        for interval in intervals:
            start, end = interval
            total_time += abs(end - start)

            if prev_end == start:
                prev_end = end
                continue

            missing_times.append([prev_end, start])
            prev_end = end

        if prev_end < to_mins(SHIFT_END):
            missing_times.append([prev_end, to_mins(SHIFT_END)])

        perc_covered = (total_time / abs(to_mins(SHIFT_END) -
                        to_mins(SHIFT_START))) * 100
        report[robot] = {
            "covered": perc_covered,
            "total_time": total_time,
            "idle_gaps": missing_times
        }

    idle_list = []
    for r in ROBOTS:
        for start, end in report[r]["idle_gaps"]:
            minutes = end - start
            if minutes >= MIN_IDLE:
                idle_list.append((r, start, end, minutes))
    idle_list.sort(key=lambda il: - il[3])

    report["idle_gaps"] = idle_list

    return report


def utilisation_report(sessions):
    sessions, dropped = parse_data(sessions)
    robots = group_sessions(sessions)
    intervals = merge_intervals(robots)
    report = build_robot_report(intervals)

    pprint(report)


if __name__ == "__main__":
    print(utilisation_report(sessions))
