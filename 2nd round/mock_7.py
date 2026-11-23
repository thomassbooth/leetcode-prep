# ─────────────────────────────────────────────────────────────
# Gecko FDE — Applied Coding Round (mock #10)
# ─────────────────────────────────────────────────────────────
#
# "A crawler is inspecting the flat floor of a storage tank. The
#  floor is mapped as a grid of 1 m squares. The crawler starts at
#  (0, 0) facing north and follows a list of commands. We want to
#  know where it ended up, and whether it ever drove over a square
#  it had already inspected (that's wasted battery)."
#
# Commands:
#   "L"    -> turn left 90°  (stays in the same square)
#   "R"    -> turn right 90° (stays in the same square)
#   "F n"  -> drive forward n squares in the direction it's facing
#
# Some squares have supports bolted to the floor, which the crawler
# can't drive into.
#
# ~30 minutes for the code, then a short discussion.
# ─────────────────────────────────────────────────────────────

commands = ["F 3", "R", "F 2", "R", "F 4", "L",
            "F 1", "L", "L", "F 3", "X", "F -2", "R", "F 2"]

obstacles = {(2, 1), (5, 5)}


def parse_commands(commands):

    parsed = []
    garb = []

    for command in commands:
        cmds = command.split(" ")
        try:
            if len(cmds) == 1:
                if cmds[0] not in ("R", "L"):
                    garb.append(command)
                    continue
                else:
                    parsed.append({"cmd": cmds[0]})
            elif len(cmds) == 2:
                cmd, dist = cmds[0], int(cmds[1])

                if dist < 0:
                    garb.append(command)
                    continue

                parsed.append({"cmd": cmd, "dist": dist})

        except:
            garb.append(command)

    return parsed, garb


class CrawlerTraverse:

    ROTATION_MAP = {
        "R": 1,
        "L": -1
    }

    def __init__(self, commands, obstacles):
        self._commands = commands
        self.visited = set()
        self.visited.add((0, 0))
        self.revisited = set()
        self.obstacles = obstacles

        # here we have up, right, down, left
        self.dirs = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.dir_facing = 0

        self.x = 0
        self.y = 0

    def __move_along(self, dist):

        dir = self.dirs[self.dir_facing]
        dx = dir[0]
        dy = dir[1]
        for _ in range(dist):

            if (self.x+dx, self.y+dy) in self.obstacles:
                break

            if (self.x+dx, self.y+dy) in self.visited:
                self.revisited.add((self.x+dx, self.y+dy))

            self.x = self.x+dx
            self.y = self.y+dy

            self.visited.add((self.x, self.y))

    def __rotate(self, letter):
        dr = self.ROTATION_MAP[letter]
        self.dir_facing = (self.dir_facing + dr) % 4

    def traverse(self):

        for command in self._commands:
            letter = command["cmd"]
            if letter in ("L", "R"):
                self.__rotate(letter)
            else:
                self.__move_along(command["dist"])

        return self.visited, self.revisited, (self.x, self.y)


def run_crawler(commands, obstacles):

    commands, garb = parse_commands(commands)

    traverser = CrawlerTraverse(commands, obstacles)

    visited, revisisted, final_pos = traverser.traverse()

    print(
        f"Final position {final_pos}, visisted: {visited}, revisisted: {revisisted}, wasted: {len(revisisted) > 0}")


if __name__ == "__main__":
    run_crawler(commands, obstacles)
