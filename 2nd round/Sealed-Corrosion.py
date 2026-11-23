# A grid scan shows 1 for damaged steel and 0 for healthy. A damaged patch (4-directional) is
# sealed if none of its cells touch the edge of the scan, because a patch touching the edge might
# continue beyond what the robot saw.
# returns (number_of_sealed_patches, total_area_of_sealed_patches)


def sealed_patches(grid: list[list[int]]) -> tuple[int, int]:

    # im gunna start on the border and dfs of any i find that are dmged -> mark all as visited
    # these are
    rows = len(grid)
    cols = len(grid[0])

    area = 0
    patches = 0
    visited = set()

    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    def dfs_edge(row, col):

        if row < 0 or row >= rows:
            return

        if col < 0 or col >= cols:
            return

        if grid[row][col] == 0:
            return

        if (row, col) in visited:
            return

        visited.add((row, col))
        for dr, dc in dirs:
            dfs_edge(dr+row, dc+col)

    def dfs_main(row, col):
        nonlocal area

        if row < 0 or row >= rows:
            return 0

        if col < 0 or col >= cols:
            return 0

        if grid[row][col] == 0:
            return 0

        if (row, col) in visited:
            return 0

        visited.add((row, col))
        res = 1
        for dr, dc in dirs:
            res += dfs_main(dr+row, dc+col)

        return res

    # border check
    # top / bot row
    for col in range(cols):
        if grid[0][col] == 1:
            dfs_edge(0, col)

        if grid[rows-1][col] == 1:
            dfs_edge(rows-1, col)

    for row in range(rows):
        if grid[row][0] == 1:
            dfs_edge(row, 0)

        if grid[row][cols-1] == 1:
            dfs_edge(row, cols-1)

    for row in range(rows):
        for col in range(cols):
            area_size = dfs_main(row, col)
            if area_size > 0:
                patches += 1
                area += area_size

    return (patches, area_size)
