import math

# ─────────────────────────────────────────────────────────────
# Geometry drills. Fill in each function, then run the file.
# ─────────────────────────────────────────────────────────────


# 1. WRAP-AROUND
# The crawler is at `angle` degrees and turns by `delta` (positive = CW, negative = CCW).
# Return its new angle in the range 0..359.
def new_angle(angle, delta):

    return (angle + delta) % 360


assert new_angle(350, 30) == 20
assert new_angle(10, -45) == 325
assert new_angle(0, 450) == 90


# 2. SHORTEST GAP BETWEEN TWO ANGLES
# Return the smallest number of degrees between angles a and b (always 0..180).
def angle_gap(a, b):

    angle = abs(a-b) % 360

    return min(360-angle, angle)
    print(angle)


assert angle_gap(350, 10) == 20
assert angle_gap(30, 60) == 30
assert angle_gap(90, 270) == 180


# 3. ARC LENGTH
# How far (mm) does the crawler travel going `degrees` around a pipe of `radius_mm`?
def arc_length(radius_mm, degrees):
    circum = (radius_mm * 2) * math.pi

    return (degrees/360)*circum


assert math.isclose(arc_length(150, 45), 117.81, abs_tol=0.01)
assert math.isclose(arc_length(200, 360), 1256.64, abs_tol=0.01)


# 4. WHICH GRID CELL
# The pipe is split into cells of `sector_deg` degrees around and `row_mm` mm along.
# Return (sector, row) for a position. A position at exactly the far end belongs in the last row.
def grid_cell(angle, z, sector_deg, row_mm, length_mm):

    # each sector is split into sector degrees from the circle face
    # and length ways its split into length/row_mm

    sectors = int(360 // sector_deg)
    row_cells = length_mm // row_mm

    # sector we fall into
    grid_sector = int(angle // sector_deg) % sectors
    row = min(int(z // row_mm), row_cells-1)

    print(row)
    return (grid_sector, row)


assert grid_cell(95, 430, 30, 100, 1000) == (3, 4)
assert grid_cell(359.9, 1000, 30, 100, 1000) == (11, 9)
assert grid_cell(0, 0, 30, 100, 1000) == (0, 0)


# 5. IS AN ANGLE INSIDE A REGION?
# A damaged region runs from `start` to `end` going CLOCKWISE. It may cross 0°.
# Return True if `angle` is inside it (edges included).
def in_arc(angle, start, end):

    if end > start:
        return start <= angle and angle <= end

    return angle >= start or angle <= end


assert in_arc(350, 330, 30) == True     # region wraps past 0°
assert in_arc(10, 330, 30) == True
assert in_arc(100, 330, 30) == False
assert in_arc(45, 30, 60) == True       # normal region, no wrap


# 6. FLAT PLANE: DISTANCE AND DIRECTION
# On a flat tank floor, return (distance, direction_deg) from (x1, y1) to (x2, y2).
# Direction is measured from the +x axis, anticlockwise, in the range 0..359.
def distance_and_direction(x1, y1, x2, y2):
    dist = ((x2-x1)**2 + (y2-y1)**2) ** (1/2)

    angle = math.degrees(math.atan2(y2-y1, x2-x1)) % 360
    return (dist, angle)


d, a = distance_and_direction(0, 0, 3, 4)
assert math.isclose(d, 5.0) and math.isclose(a, 53.13, abs_tol=0.01)
d, a = distance_and_direction(0, 0, -1, 0)
assert math.isclose(d, 1.0) and math.isclose(a, 180.0)
d, a = distance_and_direction(0, 0, 0, -2)
assert math.isclose(d, 2.0) and math.isclose(a, 270.0)


# BONUS: SHORTEST DISTANCE BETWEEN TWO POINTS ON A PIPE'S SURFACE
# Each point is (angle_deg, z_mm). Hint: unroll the pipe flat, and remember
# the shortest way around might cross 0°. Uses drills 2, 3 and 6 together.
def surface_distance(p1, p2, radius_mm):
    pass


assert math.isclose(surface_distance(
    (350, 100), (20, 500), 150), 407.64, abs_tol=0.01)
assert math.isclose(surface_distance(
    (0, 0), (180, 0), 100), 314.16, abs_tol=0.01)


print("All drills passed!")
