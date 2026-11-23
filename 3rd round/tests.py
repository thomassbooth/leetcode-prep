import sys
import importlib
import traceback
mod = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else "problems")

ROWS = ["10.1,9.8,4.2,4.0",
        "10.0,,4.1,9.9",
        "3.9,10.2,10.0,9.7"]
PIPE = ["4.0,10,10,4.5",
        "10,10,10,10",
        "10,4.4,10,10",
        "10,10,4.3,10"]
GRID = ["..#....",
        "..#.##.",
        "....#..",
        "##.#...",
        "......."]
BGRID = ["....C....",
         "#######.#",
         "........."]
LOG = ["1.0,pos,10.0", "0.0,pos,0.0", "0.5,ut,9.8", "0.5,ut,9.8", "", "garbage",
       "1.0,ut,9.5", "1.5,ut,9.1", "2.0,pos,20.0", "2.5,ut,8.0", "9.0,pos,90.0",
       "6.0,ut,7.0", "-1,ut,9.9", "3.0,ut,abc"]
EDGES = [" Tank -> Pump1", "Pump1->Valve1", "Valve1->HX1", "HX1->Drum",
         "Drum->Pump1", "Pump2->Valve2", "Valve2->HX1", "Drum->Flare"]
DAG = ["Tank->Pump1", "Pump1->Valve1",
       "Tank->Pump2", "Pump2->Valve1", "Valve1->HX"]
READ = [("T1", 0, 10.0), ("T1", 100, 9.0), ("T1", 200, 8.0),
        ("T2", 0, 12.0), ("T2", 365, 11.9),
        ("T3", 0, 6.0), ("T3", 50, 5.0),
        ("T4", 0, 8.0), ("T4", 10, 8.5),
        ("T5", 0, 9.0)]
HIST = [(0, 10.0), (30, 9.5), (60, 9.5), (90, 8.0), (120, 7.9)]

T = {
    "1A corrosion basic": lambda: mod.corrosion_patches(ROWS, 5.0) == [(3, 4.0), (1, 3.9)],
    "1B diagonal": lambda: mod.corrosion_patches(PIPE, 5.0, diag=True) == [(2, 4.3), (1, 4.0), (1, 4.5)],
    "1B wrap (pipe)": lambda: mod.corrosion_patches(PIPE, 5.0, wrap=True) == [(2, 4.0), (1, 4.3), (1, 4.4)],
    "1B min_area": lambda: mod.corrosion_patches(ROWS, 5.0, min_area=2) == [(3, 4.0)],
    "2A path": lambda: mod.robot_path(GRID, (0, 0), (0, 6)) == 10,
    "2A blocked": lambda: mod.robot_path([".#.", "##.", "..."], (0, 0), (2, 2)) == -1,
    "2A start==goal": lambda: mod.robot_path(GRID, (0, 0), (0, 0)) == 0,
    "2B battery ok": lambda: mod.robot_path_battery(BGRID, (0, 0), (2, 8), 6) == 10,
    "2B battery too small": lambda: mod.robot_path_battery(BGRID, (0, 0), (2, 8), 5) == -1,
    "3A align": lambda: mod.align_streams(LOG, 3.0) == [(0.5, 9.8, 5.0), (1.0, 9.5, 10.0), (1.5, 9.1, 15.0)],
    "3A gap allowed": lambda: mod.align_streams(LOG, 10.0)[-1] == (6.0, 7.0, 60.0),
    "3B clock offset": lambda: mod.align_streams(["1.0,pos,0", "3.0,pos,20", "1.5,ut,5"], 5.0, pos_offset=1.0) == [(1.5, 5.0, 15.0)],
    "4A downstream (cycle)": lambda: mod.downstream(EDGES, "Valve1") == ["Drum", "Flare", "HX1", "Pump1"],
    "4A leaf": lambda: mod.downstream(EDGES, "Flare") == [],
    "4B topo order": lambda: mod.inspection_order(DAG) == ["Tank", "Pump1", "Pump2", "Valve1", "HX"],
    "5 gaps": lambda: mod.uncovered([(50, 70), (-10, 20), (15, 30), (65, 80), (95, 130)], 100) == [(30, 50), (80, 95)],
    "5 touching/none": lambda: mod.uncovered([(0, 50), (50, 100)], 100) == [],
    "5 empty": lambda: mod.uncovered([], 100) == [(0, 100)],
    "6A riskiest": lambda: mod.riskiest(READ, 5.5, 2) == [("T3", 0.0), ("T1", 250.0)],
    "6A all": lambda: [a for a, _ in mod.riskiest(READ, 5.5, 10)] == ["T3", "T1", "T2"],
    "6B binary search": lambda: mod.first_below(HIST, 9.5) == 90 and mod.first_below(HIST, 7.0) is None and mod.first_below(HIST, 11) == 0,
}


def cycle_raises():
    try:
        mod.inspection_order(EDGES)
        return False
    except ValueError:
        return True


T["4B cycle -> ValueError"] = cycle_raises

passed = 0
for name, fn in T.items():
    try:
        ok = fn()
    except NotImplementedError:
        ok = None
    except Exception:
        ok = False
        traceback.print_exc()
    print(f"{'PASS' if ok else 'TODO' if ok is None else 'FAIL'}  {name}")
    passed += bool(ok)
print(f"\n{passed}/{len(T)} passed")
