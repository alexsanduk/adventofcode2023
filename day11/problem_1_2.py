from typing import Tuple, Set

Point = Tuple[int, int]

expansion_factor = 2  # 1000000


def dist(p1: Point, p2: Point, normal_rows: Set[int], normal_cols: Set[int]) -> int:
    row_min, row_max = min(p1[0], p2[0]), max(p1[0], p2[0])
    col_min, col_max = min(p1[1], p2[1]), max(p1[1], p2[1])
    all_rows = set(range(row_min, row_max))
    all_cols = set(range(col_min, col_max))
    return 1 * (
        len(all_rows.intersection(normal_rows))
        + len(all_cols.intersection(normal_cols))
    ) + expansion_factor * (
        len(all_rows.difference(normal_rows)) + len(all_cols.difference(normal_cols))
    )


def test_dist():
    assert dist((0, 0), (1, 1), set([0, 1]), set([0, 1])) == 2
    assert dist((1, 1), (1, 1), set([0, 1]), set([0, 1])) == 0
    assert dist((1, 1), (0, 0), set([0, 1]), set([0, 1])) == 2
    assert dist((2, 2), (0, 0), set([0, 1, 2]), set([0, 2])) == 5
    assert dist((2, 2), (0, 0), set([0, 2]), set([0, 1, 2])) == 5


def solution(fname: str) -> int:
    normal_rows = set()
    normal_cols = set()
    galaxies = []
    with open(fname) as f:
        for row_id, line in enumerate(f):
            for col_id, ch in enumerate(line):
                if ch == "#":
                    galaxies.append((row_id, col_id))
                    normal_rows.add(row_id)
                    normal_cols.add(col_id)

    total_distance = 0
    for galaxy_id1 in range(len(galaxies)):
        for galaxy_id2 in range(galaxy_id1 + 1, len(galaxies)):
            total_distance += dist(
                galaxies[galaxy_id1], galaxies[galaxy_id2], normal_rows, normal_cols
            )
    return total_distance


if __name__ == "__main__":
    print(solution("./input.txt"))
