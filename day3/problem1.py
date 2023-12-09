# numbers = [(467, 0, 2)]
# symbols = [(1, 3)]
# for s in symbols find numbers in
# (0, 2) intersects with (2, 4)
#
from collections import defaultdict
from typing import List, Tuple, Dict


def read_line(
    line_id: int,
    line: str,
    numbers: Dict[int, List[Tuple[int, int, int]]],
    symbols: List[Tuple[int, int]],
) -> Tuple[Dict[int, List[Tuple[int, int, int]]], List[Tuple[int, int]]]:
    ix = 0
    line = line.strip()
    n = len(line)
    while True:
        if ix >= n:
            break
        while ix < n and line[ix] == ".":
            ix += 1
        if ix < n and not (ord("0") <= ord(line[ix]) <= ord("9")):
            symbols.append((line_id, ix))
            ix += 1
            continue
        left = ix
        while ix < n and (ord("0") <= ord(line[ix]) <= ord("9")):
            ix += 1
        if left < n:
            numbers[line_id].append((int(line[left:ix]), left, ix - 1))
    return (numbers, symbols)


assert read_line(0, "467..114.*", defaultdict(list), []) == (
    {0: [(467, 0, 2), (114, 5, 7)]},
    [(0, 9)],
)
assert read_line(0, ".467..114.1", defaultdict(list), []) == (
    {0: [(467, 1, 3), (114, 6, 8), (1, 10, 10)]},
    [],
)


def has_intersection(segment1: Tuple[int, int], segment2: Tuple[int, int]) -> bool:
    segment1, segment2 = (min(segment1, segment2), max(segment1, segment2))
    return segment2[0] <= segment1[1]


assert has_intersection((0, 2), (2, 4))
assert has_intersection((2, 4), (0, 2))
assert not has_intersection((0, 2), (5, 7))
assert not has_intersection((5, 7), (0, 2))
assert has_intersection((1, 7), (2, 4))
assert has_intersection((2, 4), (1, 7))


def find_neighbors(
    numbers: Dict[int, List[Tuple[int, int, int]]],
    symbols: List[Tuple[int, int]],
):
    total_sum = 0
    for row, col in symbols:
        for n_row in (row - 1, row, row + 1):
            for num, left, right in numbers.get(n_row, []):
                if has_intersection((left, right), (col - 1, col + 1)):
                    total_sum += num
    return total_sum


assert find_neighbors({0: [(467, 0, 2)], 1: [], 2: [(35, 2, 4)]}, [(0, 3)]) == 467
assert find_neighbors({0: [(467, 0, 2)], 1: [], 2: [(35, 2, 4)]}, [(1, 0)]) == 467
assert find_neighbors({0: [(467, 0, 2)], 1: [], 2: [(35, 2, 4)]}, [(2, 0)]) == 0
assert find_neighbors({0: [(467, 0, 2)], 1: [], 2: [(35, 2, 4)]}, [(1, 2)]) == 502
assert find_neighbors({0: [(467, 0, 2)], 1: [], 2: [(35, 2, 4)]}, [(1, 1)]) == 502


def solution(fname: str):
    symbols = []
    numbers = defaultdict(list)
    with open(fname) as f:
        for line_id, line in enumerate(f):
            numbers, symbols = read_line(line_id, line, numbers, symbols)
        # print(numbers)
        # print(symbols)
    return find_neighbors(numbers, symbols)


print(solution("./input.txt"))
