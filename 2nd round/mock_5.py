# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (mock #8)
# ─────────────────────────────────────────────────────────────
#
# "A crawler made several passes along a 1000 mm pipe. Each pass
#  scanned a stretch of it. The customer wants to know which parts
#  of the pipe were never scanned, and how much of it was covered."
#
# Each pass is logged as "pass_id,start_mm,end_mm"
#
# ~30 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────

passes = [
    "P1,0,250",
    "P2,200,400",
    "P3,650,500",
    "P4,900,1100",
    "P5,abc,300",
    "P6,380,420",
    "P7,450,450",
    "P8,-50,30",
]


def parse_data(passes, length_mm):

    parsed = []
    garb = []
    for log in passes:
        try:
            pass_id, start_mm, end_mm = log.split(',')

            a, b = int(start_mm), int(end_mm)
            lo, hi = min(a, b), max(a, b)

            start_mm = max(0, lo)
            end_mm = min(length_mm, hi)

            if start_mm == end_mm:             # P7 (450, 450): covers nothing
                garb.append(log)
                continue

            parsed.append({
                "pass_id": pass_id,
                "start_mm": start_mm,
                "end_mm": end_mm
            })
        except:
            garb.append(log)

    return parsed, garb


def merge_intervals(intervals, length_mm):
    intervals.sort(key=lambda i: i["start_mm"])

    res = [intervals[0]]
    missing_dist = 0
    gaps = []
    if res[0]["start_mm"] > 0:
        gaps.append([0, res[0]["start_mm"]])

    for i, interval in enumerate(intervals):
        if i == 0:
            continue
        # if the end time of the last is above the start of this then merge them else just push it on
        if res[-1]["end_mm"] > interval["start_mm"]:
            res[-1]["end_mm"] = max(res[-1]["end_mm"], interval["end_mm"])

        else:
            missing_dist += abs(interval["start_mm"] - res[-1]["end_mm"])
            gaps.append([res[-1]["end_mm"], interval["start_mm"]])
            res.append(interval)

    if intervals[-1]["end_mm"] < length_mm:
        gaps.append([intervals[-1]["end_mm"], length_mm])

    return res, missing_dist, gaps


def scan_coverage(passes, length_mm):

    parsed, garbage = parse_data(passes, length_mm)
    res, missing_dist, gaps = merge_intervals(parsed, length_mm)

    print(
        f"Result is {res}, total missing distance {missing_dist}, gaps that are missing {gaps}")


if __name__ == "__main__":
    scan_coverage(passes, 1000)
