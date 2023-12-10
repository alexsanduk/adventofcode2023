from typing import List, Dict, Tuple
import re


def read_mapping(
    line: str, mapping: List[Tuple[int, int, int]]
) -> List[Tuple[int, int, int]]:
    destination, source, range_val = map(int, line.split())
    mapping.append((source, source + range_val, destination - source))
    return mapping


def test_read_mapping():
    assert read_mapping("1 2 3", []) == [(2, 5, -1)]
    assert read_mapping("4 0 2", [(2, 4, -2)]) == [(2, 4, -2), (0, 2, 4)]


def read_seeds(line: str) -> List[int]:
    seeds = []
    r = re.search(r"seeds: (?P<seeds>[\d ]+)", line)
    seeds = []
    if r:
        seeds = r.group("seeds")
        seeds = list(map(int, seeds.split(" ")))
    return seeds


def test_read_seeds():
    assert read_seeds("seeds: 79 14 55 13") == [79, 14, 55, 13]
    assert read_seeds("seeds: 79") == [79]


def map_number(num: int, mapping: List[Tuple[int, int, int]]) -> int:
    for start, end, shift in mapping:
        if start <= num < end:
            return num + shift
    return num


def test_map_number():
    assert map_number(1, [(1, 3, 5)]) == 6
    assert map_number(2, [(1, 3, 5)]) == 7
    assert map_number(0, [(1, 3, 5)]) == 0


def get_locations(
    seeds: List[int], mapping: Dict[Tuple[str, str], List[Tuple[int, int, int]]]
) -> List[int]:
    source_dest_cats = [
        ("seed", "soil"),
        ("soil", "fertilizer"),
        ("fertilizer", "water"),
        ("water", "light"),
        ("light", "temperature"),
        ("temperature", "humidity"),
        ("humidity", "location"),
    ]
    locations = []
    for s in seeds:
        number = s
        for source_dest_categories in source_dest_cats:
            number = map_number(number, mapping[source_dest_categories])
        locations.append(number)
    return locations


def test_get_locations():
    assert get_locations(
        [0],
        {
            ("seed", "soil"): [(0, 1, 1)],
            ("soil", "fertilizer"): [(1, 2, 1)],
            ("fertilizer", "water"): [(2, 3, 1)],
            ("water", "light"): [(3, 4, 1)],
            ("light", "temperature"): [(4, 5, 1)],
            ("temperature", "humidity"): [(5, 6, 1)],
            ("humidity", "location"): [(6, 7, 1)],
        },
    ) == [7]


def solution(fname: str) -> int:
    mapping = dict()
    with open(fname) as f:
        seeds = read_seeds(f.readline())
        new_mapping = []
        for line in f:
            if line.strip() == "":
                continue
            r = re.search(r"(?P<source_cat>[\w]+)-to-(?P<dest_cat>[\w]+) map", line)
            if r:
                new_mapping = []
                mapping[(r.group("source_cat"), r.group("dest_cat"))] = new_mapping
            else:
                sorted(read_mapping(line, new_mapping))
                new_mapping.sort()
    locations = get_locations(seeds, mapping)
    return min(locations)


if __name__ == "__main__":
    print(solution("./input.txt"))
