# ─────────────────────────────────────────────────────────────
# Mock #3: Crawler on a Pipe
# ─────────────────────────────────────────────────────────────
#
# Pipe: radius 150 mm, length 1000 mm.
# Crawler starts at the TOP of the pipe (angle 0°), at the START end (0 mm along).
#
# Commands:
#   "FWD x"  -> move x mm along the pipe, away from the start end
#   "BACK x" -> move x mm along the pipe, towards the start end
#   "CW x"   -> move x degrees around the pipe, clockwise (angle goes up)
#   "CCW x"  -> move x degrees around the pipe, counter-clockwise (angle goes down)
#
# Rules:
#   - Angles wrap: past 360 goes back to 0, below 0 goes to 359.
#   - If a FWD/BACK would go past either end, the crawler stops at the end.
#   - Command amounts are whole numbers.
#
# Return:
#   1. final angle (0-359) and final position along (mm)
#   2. total distance travelled over the surface (mm, 1 decimal place)
#        - along moves: the mm actually moved
#        - around moves: (degrees / 360) * circumference
#   3. % of pipe inspected (1 decimal place):
#        grid of 12 sectors around (30° each) x 10 rows along (100 mm each) = 120 cells.
#        A cell is inspected if the crawler passes through it (start cell counts).
#
# Test 1:
#   ["FWD 250", "CW 90", "BACK 400"]
#   -> angle 90, position 0, travelled 735.6, inspected 6.7
#
# Test 2:
#   ["CW 350", "FWD 120", "CCW 40", "FWD 2000"]
#   -> angle 310, position 1000, travelled 2021.0, inspected 18.3
# ─────────────────────────────────────────────────────────────

import math


class CommandMover:

    def __init__(self, radius_mm, length_mm):
        self.radius = radius_mm
        self.length = length_mm

    def move_along(self, starting, signed_distance):

        # so if we ever reach the end of the cylinder - clamp it to the end same for back

        if signed_distance < 0:
            location = max(0, starting + signed_distance)
            distance = abs(location - starting)

        else:
            location = min(starting + signed_distance, self.length)
            distance = abs(location - starting)

        return distance, location

    def move_around(self, angle, starting_angle):

        # lets work out the distance travelled first

        circumference_mm = math.pi * (self.radius * 2)
        factor = abs(angle) / 360  # how many rotations

        distance = factor * circumference_mm
        final_angle = (angle+starting_angle) % 360

        return (distance, final_angle)


def generate_grid(radius_mm, length_mm, coverage_mm):
    # we can treat it as a grid thats just rolled out our horizontal axis would just be our circumference
    # and our vertical is the distance.
    # whats an acceptable section for a sensor scan? is it like 1mm?
    horizontal_full = (radius_mm * 2) * math.pi
    vertical = length_mm

    for horizontal_v in range(0, coverage_mm, horizontal_full):
        print('hi')


def inspect_pipe(commands, radius_mm, length_mm):

    mover = CommandMover(radius_mm, length_mm)
    total_moved = 0
    generate_grid(radius_mm, length_mm, 1)
    position, angle = 0, 0
    for cmd in commands:
        command, dist = cmd.split(" ")
        dist = int(dist)
        if command == "FWD":
            moved, location = mover.move_along(position, dist)
            position = location
        elif command == "BACK":
            moved, location = mover.move_along(position, -dist)
            position = location
        elif command == "CW":
            moved, final_angle = mover.move_around(dist, angle)
            angle = final_angle
        elif command == "CCW":
            moved, final_angle = mover.move_around(-dist, angle)
            angle = final_angle
        total_moved += moved

    return total_moved, position, angle


print(inspect_pipe(["FWD 250", "CW 90", "BACK 400"], 150, 1000))
print(inspect_pipe(["CW 350", "FWD 120", "CCW 40", "FWD 2000"], 150, 1000))
