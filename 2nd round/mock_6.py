# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (mock #9)
# ─────────────────────────────────────────────────────────────
#
# "The customer has marked out inspection zones on a pipe. Our
#  scan found a list of defects. For each zone, they want to know
#  which defects fall inside it, and which defects aren't in any
#  zone at all."
#
# Angles are measured from the top of the pipe, clockwise, in degrees.
# z is the distance along the pipe from the start end, in mm.
#
# A zone covers the angles from angle_start CLOCKWISE to angle_end,
# and the stretch from z_start to z_end along the pipe.
#
# Zones:   "zone_id,angle_start,angle_end,z_start,z_end"
# Defects: "defect_id,angle_deg,z_mm"
#
# ~30 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────

zones = [
    "Z1,330,30,0,200",
    "Z2,90,180,100,400",
    "Z3,200,260,500,800",
]

defects = [
    "D1,350,150",
    "D2,10,250",
    "D3,120,300",
    "D4,95,100",
    "D5,330,0",
    "D6,270,600",
    "D7,x,10",
    "D8,-20,50",
    "D9,150,350",
]


def parse_zones(zones):

    parsed = {}
    garb = []

    for zone in zones:
        try:
            zone_id, angle_start, angle_end, z_start, z_end = zone.split(",")

            parsed[zone_id] = {
                "angle_start": int(angle_start),
                "angle_end": int(angle_end),
                "z_start": int(z_start),
                "z_end": int(z_end),
                "defects": []
            }
        except:
            garb.append(zone)

    return parsed, garb


def parse_defects(defects):
    parsed = []
    garb = []

    for log in defects:
        try:
            id, angle, z_mm = log.split(",")

            # we have negative values so -20 should be 340
            angle = int(angle) % 360
            z_mm = int(z_mm)

            parsed.append({"id": id, "angle": angle, "z_mm": z_mm})

        except:
            garb.append(log)

    return parsed, garb


def zone_collect(zones, defects):
    # we can just do a double loop here since the datasets are small

    matched = set()

    for zone in zones.values():
        angle_start = zone["angle_start"]
        angle_end = zone["angle_end"]
        length_start = zone["z_start"]
        length_end = zone["z_end"]

        for defect in defects:
            defect_angle = defect["angle"]
            defect_z_loc = defect["z_mm"]

            if angle_start > angle_end:
                if not (angle_start <= defect_angle <= 360 or 0 <= defect_angle <= angle_end):
                    continue
            else:
                if not (angle_start <= defect_angle <= angle_end):
                    continue

            if not (length_start <= defect_z_loc <= length_end):
                continue

            zone["defects"].append(defect)
            matched.add(defect["id"])

    # get unmatched
    unmatched = [defect for defect in defects if defect["id"] not in matched]
    return zones, unmatched


def defects_by_zone(zones, defects):

    zones, garb = parse_zones(zones)
    defects, garb_def = parse_defects(defects)

    collected, unmatched = zone_collect(zones, defects)

    print(
        f"Our zones with defects are: {collected}, our unmatched defects are {unmatched}")


if __name__ == "__main__":

    defects_by_zone(zones, defects)
