# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (mock #11: geometry)
# ─────────────────────────────────────────────────────────────
#
# "A ring of ultrasonic sensors was clamped around a pipe. Each
#  reading gives the sensor's position on the pipe's cross-section
#  as (x, y), measured from the centre of the pipe, plus the wall
#  thickness it measured. The team wants to know which part of the
#  pipe's circumference is thinnest, as a clock position."
#
# Pipe outer radius: 150 mm.
# Coordinates: x is to the RIGHT, y is UP, (0, 0) is the pipe's centre.
#
# Each reading is "x_mm,y_mm,thickness_mm"
#
# ~30 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────

import math

readings = [
    "0,150,9.5",
    "150,0,9.2",
    "0,-150,9.4",
    "-150,0,7.1",
    "106,106,8.8",
    "-106,106,7.6",
    "-130,-75,7.3",
    "75,-130,9.0",
    "-148,25,6.9",
    "40,40,5.0",
    "abc,10,9.0",
    "0,151,-2.0",
]


def find_angle_from_vertical(x, y):

    angle = math.degrees(math.atan2(y, x))

    angle = (90 - angle) % 360

    return angle


def parse_readings(readings):

    parsed = []
    garb = []
    for reading in readings:
        try:
            x, y, thickness = reading.split(",")

            thickness = float(thickness)

            x = float(x)
            y = float(y)

            if thickness < 0:
                continue

            dist_from_centre = ((x)**2 + (y)**2) ** (1/2)

            if not abs(dist_from_centre - 150) <= 5:
                continue

            parsed.append({
                "x": x,
                "y": y,
                "thickness": thickness
            })
        except:
            garb.append(reading)

    return parsed, garb


def find_thinnest(readings):

    sector_size = 30
    no_sectors = 360 // 30

    thinnest = readings[0]

    for reading in readings:
        angle = find_angle_from_vertical(reading["x"], reading["y"])
        sector = (angle // sector_size) % no_sectors
        reading["sector"] = sector

        if reading["thickness"] < thinnest["thickness"]:
            thinnest = reading

    return readings, thinnest


def thinnest_clock_position(readings, radius_mm):
    readings, garbage = parse_readings(readings)
    readings, thinnest = find_thinnest(readings)

    print(
        f"This is our readings with their sectors: {readings}, this is the thinnest: {thinnest}")


if __name__ == "__main__":
    thinnest_clock_position(readings, 150)
