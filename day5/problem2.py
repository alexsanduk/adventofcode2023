from typing import List, Dict, Tuple, Union
import re
import sys


def read_mapping(
    line: str, mapping: List[Tuple[int, int, int]]
) -> List[Tuple[int, int, int]]:
    destination, source, range_val = map(int, line.split())
    mapping.append((source, source + range_val, destination - source))
    return mapping


assert read_mapping("1 2 3", []) == [(2, 5, -1)]
assert read_mapping("4 0 2", [(2, 4, -2)]) == [(2, 4, -2), (0, 2, 4)]


def read_seed_ranges(line: str) -> List[Tuple[int, int]]:
    seeds = []
    r = re.search(r"seeds: (?P<seeds>[\d ]+)", line)
    seeds = []
    if r:
        seeds = r.group("seeds")
        seeds = list(map(int, seeds.split(" ")))
    return [(seeds[ix], seeds[ix] + seeds[ix + 1]) for ix in range(0, len(seeds), 2)]


assert read_seed_ranges("seeds: 79 14 55 13") == [(79, 93), (55, 68)]


def add_missing_segments(
    mapping: List[Tuple[int, int, int]]
) -> List[Tuple[int, int, int]]:
    end = 0
    mapping1 = mapping.copy()
    for left, right, _ in mapping1:
        if end != left:
            mapping.append((end, left, 0))
        end = right
    mapping.append((end, sys.maxsize, 0))
    return mapping


assert add_missing_segments([(1, 2, 3)]) == [(1, 2, 3), (0, 1, 0), (2, float("inf"), 0)]
assert add_missing_segments([]) == [(0, float("inf"), 0)]


def get_overlap(
    rng1: Tuple[int, int], rng2: Tuple[int, int]
) -> Union[Tuple[int, int], None]:
    rng1, rng2 = min(rng1, rng2), max(rng1, rng2)
    if rng2[0] < rng1[1]:
        return (rng2[0], min(rng1[1], rng2[1]))
    return


assert get_overlap((1, 3), (2, 4)) == (2, 3)
assert get_overlap((1, 3), (3, 4)) is None
assert get_overlap((1, 3), (2, 3)) == (2, 3)
assert get_overlap((1, 4), (2, 3)) == (2, 3)


def map_segment(
    rng: Tuple[int, int], mapping: List[Tuple[int, int, int]]
) -> List[Tuple[int, int]]:
    new_ranges = []
    for start, end, shift in mapping:
        overlap = get_overlap(rng, (start, end))
        if overlap:
            new_ranges.append((overlap[0] + shift, overlap[1] + shift))
    return new_ranges


assert map_segment((1, 2), [(0, 1, 0), (1, 2, 1), (2, 5, 10)]) == [(2, 3)]
assert map_segment((1, 3), [(0, 1, 0), (1, 2, 1), (2, 5, 10)]) == [
    (2, 3),
    (12, 13),
]


def map_seed_ranges(
    mapping: Dict[Tuple[str, str], List[Tuple[int, int, int]]],
    seed_ranges: List[Tuple[int, int]],
) -> List[Tuple[int, int]]:
    source_dest_cats = [
        ("seed", "soil"),
        ("soil", "fertilizer"),
        ("fertilizer", "water"),
        ("water", "light"),
        ("light", "temperature"),
        ("temperature", "humidity"),
        ("humidity", "location"),
    ]
    current_ranges = seed_ranges
    for t in source_dest_cats:
        m = mapping[t]
        new_ranges = []
        for rng in current_ranges:
            new_ranges.extend(map_segment(rng, m))
        current_ranges = new_ranges
    return current_ranges


def solution(fname: str) -> int:
    mapping = dict()
    with open(fname) as f:
        seed_ranges = read_seed_ranges(f.readline())
        new_mapping = []
        for line in f:
            if line.strip() == "":
                continue
            r = re.search(r"(?P<source_cat>[\w]+)-to-(?P<dest_cat>[\w]+) map", line)
            if r:
                new_mapping = []
                mapping[(r.group("source_cat"), r.group("dest_cat"))] = new_mapping
            else:
                new_mapping = read_mapping(line, new_mapping)
    for cat, m in mapping.items():
        m.sort()
        m = add_missing_segments(m)
        m.sort()
    location_ranges = map_seed_ranges(mapping, seed_ranges)
    return min(location_ranges)[0]


print(solution("./input.txt"))
