# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (Problem 6: Scan Coverage)
# ─────────────────────────────────────────────────────────────
#
# "Before I trust any thickness numbers I need to know what we
#  actually scanned. The robot crawls the wall in horizontal lanes,
#  and sometimes it slips, stops early, or gets sent back over the
#  same stretch. Tell me how much of each lane we covered, where the
#  gaps are, and give me a list of stretches to send the robot back
#  to, biggest first."
#
# Passes: "pass_id,lane,x_start_mm,x_end_mm"
# The wall is 1000 mm wide and has 4 lanes (0-3).
#
# Report:
#   - per lane: covered length (mm), coverage %, and the gaps as (start, end)
#   - overall coverage % for the wall
#   - a rescan list: every gap of at least MIN_GAP mm, as
#     (lane, start, end, length), biggest first
#
# ~40 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────
from collections import defaultdict

passes = [
    "P1,0,0,400",    "P2,0,350,700",  "P3,0,700,1000",
    "P4,1,600,200",  "P5,1,250,300",  "P6,1,800,1050",
    "P7,2,0,480",    "P8,2,520,1000",
    "ERR", "P9,5,0,100", "P10,2,300,300", "P1,0,0,400",
    "P11,1,abc,500", "P12,0,-50,100",
]

WALL_WIDTH = 1000
NUM_LANES = 4
MIN_GAP = 50


def parse_data(passes):

    parsed = []
    dropped = 0

    for data in passes:

        try:
            p_id, lane, x_start, x_end = data.split(",")

            lane = int(lane)
            x_start = float(x_start)
            x_end = float(x_end)

            if lane < 0 or lane >= NUM_LANES:
                dropped += 1
                continue

            if x_start > x_end:                     # robot drove backwards
                x_start, x_end = x_end, x_start

            x_start = max(0, x_start)
            x_end = min(WALL_WIDTH, x_end)

            if x_start >= x_end:                    # zero length, or entirely off the wall
                dropped += 1
                continue

            parsed.append({
                "x_start": x_start,
                "x_end": x_end,
                "p_id": p_id,
                "lane": lane
            })

        except Exception as e:
            dropped += 1
            print(e)

    return parsed, dropped


def group_by_lane(passes):

    lanes = defaultdict(list)

    for data in passes:
        lane = data["lane"]
        lanes[lane].append(data)

    lanes = {lane: sorted(readings, key=lambda r: r["x_start"])
             for lane, readings in lanes.items()}

    return lanes


def merge_lanes(lanes):

    merged = {}

    for lane, readings in lanes.items():
        res = []
        for reading in readings:
            start = reading["x_start"]
            end = reading["x_end"]

            if res and start <= res[-1][1]:
                res[-1][1] = max(end, res[-1][1])
            else:
                res.append([start, end])

        merged[lane] = res

    return merged


def collect_results(merged):
    final_res = {}

    for lane in range(NUM_LANES):
        ranges = merged.get(lane, [])
        covered = 0
        missing = []
        prev = 0                      # how far along the wall we've accounted for

        for start, end in ranges:
            if start > prev:
                missing.append((prev, start))
            covered += end - start
            prev = end

        # weve looked at all the results where the last one ends up will be this
        if prev < WALL_WIDTH:
            missing.append([prev, WALL_WIDTH])

        final_res[lane] = {
            "total_covered": covered,
            "perc_covered": covered / WALL_WIDTH * 100,
            "missing_intervals": missing,
        }

    return final_res


def make_final_report(results):
    area = WALL_WIDTH * NUM_LANES
    total_covered_area = 0
    rescan_list = []

    for lane, res in results.items():
        total_covered_area += res["total_covered"]

        for start, end in res["missing_intervals"]:
            length = end-start
            if length >= MIN_GAP:
                rescan_list.append((lane, start, end, length))

    rescan_list.sort(key=lambda g: -g[3])

    return {
        "overall_coverage": (total_covered_area / area) * 100,
        "lane_results": results,
        "rescan_list": rescan_list
    }


def coverage_report(passes):
    parsed, dropped = parse_data(passes)
    lanes = group_by_lane(parsed)
    lanes = merge_lanes(lanes)
    results = collect_results(lanes)

    final_report = make_final_report(results)
    return final_report


if __name__ == "__main__":
    report = coverage_report(passes)

    print(report)
