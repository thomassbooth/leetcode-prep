# Problem 5: Inspection Plan with Durations (medium)
#
# There are n inspection tasks, numbered 0 to n-1. Task i takes hours[i] hours.
# deps is a list of pairs (a, b), meaning task a must FINISH before task b can START.
# There are unlimited crews, so any number of tasks can run at the same time
# as long as their dependencies are done.
#
# Return the minimum total hours to finish every task,
# or -1 if the dependencies contain a cycle (so the tasks can never all be done).
#
# Example 1:
#   hours = [3, 2, 4, 1, 2]
#   deps  = [(0, 2), (1, 2), (2, 3), (1, 4)]
#   -> 8
#   (task 0 ends at 3, task 1 ends at 2;
#    task 2 waits for both, starts at 3, ends at 7;
#    task 3 starts at 7, ends at 8;  task 4 starts at 2, ends at 4)
#
# Example 2:
#   hours = [1, 2, 3, 4]
#   deps  = [(0, 1), (0, 2), (1, 3), (2, 3)]
#   -> 8
#   (0 ends at 1; 1 ends at 3; 2 ends at 4; 3 waits for the later of those -> starts at 4, ends at 8)
#
# Example 3:
#   hours = [5, 2, 7]
#   deps  = []
#   -> 7
#   (no dependencies, so everything runs at once; the longest task decides it)
#
# Example 4:
#   hours = [1, 1, 1]
#   deps  = [(0, 1), (1, 2), (2, 0)]
#   -> -1
#   (cycle)
#
# Constraints:
#   - 1 <= n <= 10,000
#   - 0 <= len(deps) <= 50,000
#   - 1 <= hours[i] <= 1,000
#
# Think about: when can a task START? It depends on its prerequisites' FINISH times.
# Your DFS topo sort can return a value per node. What should that value be here?


def min_total_hours(hours: list[int], deps: list[tuple[int, int]]) -> int:
    pass
