# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (mock #12: field of view)
# ─────────────────────────────────────────────────────────────
#
# "A crawler is parked on a flat tank floor. Its camera can see
#  defects that are in front of it, within a certain angle and
#  distance. Given the crawler's position and heading, and a list
#  of defects, which defects can the camera see? List them nearest
#  first."
#
# Coordinates in metres: x is to the RIGHT (east), y is UP (north).
# Heading is measured from NORTH, CLOCKWISE, in degrees
# (0 = north, 90 = east).
#
# Crawler: at (2, 3), heading 10°.
# Camera:  sees up to 30° either side of the heading, up to 5 m away.
#
# Each defect is "defect_id,x,y"
#
# ~30 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────
import math

crawler = {"x": 2, "y": 3, "heading_deg": 10}
camera = {"half_angle_deg": 30, "range_m": 5}

defects = [
    "D1,4,5",
    "D2,2,7",
    "D3,6,3",
    "D4,5,4",
    "D5,3,6",
    "D6,1,7",
    "D7,0,1",
    "D8,x,4",
    "D9,2,3",
    "D10,2,9",
    "D11,-1,6",
]


def angle_from_camera_point(x, y, start_x, start_y):

    angle = math.degrees(math.atan2(y-start_y, x-start_x))

    return (90-angle) % 360


def check_angle_in_view(bearing, heading, half_angle):

    start = (heading - half_angle) % 360
    end = (heading + half_angle) % 360

    if start <= end:
        return start <= bearing <= end

    return bearing >= start or bearing <= end


def check_defect_range(x, y, start_x, start_y, range):

    length = ((x-start_x)**2 + (y-start_y)**2) ** (1/2)

    return length <= range, length


def check_points_in_view(defects, crawler, camera):
    crawler_x = crawler["x"]
    crawler_y = crawler["y"]
    crawler_deg = crawler["heading_deg"]
    camera_half_ang = camera["half_angle_deg"]
    camera_range = camera["range_m"]

    defects_in_range = []

    for defect in defects:
        x, y = defect["x"], defect["y"]
        angle_from_camera = angle_from_camera_point(x, y, crawler_x, crawler_y)
        in_angle = check_angle_in_view(
            angle_from_camera, crawler_deg, camera_half_ang)
        in_range, range = check_defect_range(
            x, y, crawler_x, crawler_y, camera_range)

        can_see_defect = in_angle and in_range
        defect["in_range"] = can_see_defect
        defect["range"] = range

        if can_see_defect:
            defects_in_range.append(defect)

    defects_in_range.sort(key=lambda i: i["range"])

    return defects, defects_in_range


def parse_data(defects):

    parsed = []
    garb = []

    for defect in defects:
        try:
            id, x, y = defect.split(',')

            x = int(x)
            y = int(y)

            parsed.append({
                "id": id,
                "x": x,
                "y": y
            })
        except:
            garb.append(defect)

    return parsed, garb


def visible_defects(crawler, camera, defects):

    defects, garb = parse_data(defects)
    defects, defects_in_range = check_points_in_view(defects, crawler, camera)

    print(defects_in_range)


if __name__ == "__main__":
    visible_defects(crawler, camera, defects)
