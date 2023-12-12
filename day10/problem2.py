from typing import List, Tuple, Dict

Point = Tuple[int, int]
Graph = Dict[Point, List[Point]]


def are_two_points_connected(p1: Point, p2: Point, graph: Graph) -> bool:
    n1 = graph.get(p1, [])
    n2 = graph.get(p2, [])
    return (p1 in n2) and (p2 in n1)


def test_are_two_points_connected():
    assert are_two_points_connected(
        (1, 2), (1, 3), {(1, 2): [(1, 1), (1, 3)], (1, 3): [(1, 2), (2, 3)]}
    )


def get_neighbors(graph: Graph, p: Point) -> List[Point]:
    return [n for n in graph[p] if are_two_points_connected(n, p, graph)]


def map_symbol(p: Point, ch: str) -> List[Point]:
    (i, j) = p
    mapping = {
        "|": [(i - 1, j), (i + 1, j)],
        "-": [(i, j - 1), (i, j + 1)],
        "L": [(i - 1, j), (i, j + 1)],
        "J": [(i, j - 1), (i - 1, j)],
        "7": [(i, j - 1), (i + 1, j)],
        "F": [(i, j + 1), (i + 1, j)],
        ".": [],
        "S": [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)],
    }
    return mapping[ch]


def test_build_graph():
    assert map_symbol((1, 1), "|") == [(0, 1), (2, 1)]
    assert map_symbol((1, 1), "J") == [(1, 0), (0, 1)]


def traverse_graph(graph: Graph, s: Point) -> List[Point]:
    prev_point = s
    cur_point = s
    cycle = []
    while True:
        cycle.append(cur_point)
        # print(prev_point, cur_point)
        p1 = get_neighbors(graph, cur_point)[0]
        if p1 == prev_point:
            p1 = get_neighbors(graph, cur_point)[1]
        prev_point = cur_point
        cur_point = p1
        if cur_point == s:
            break
    return cycle


def compress_row_cycle(row_cycle: List[Tuple[int, str]]) -> List[Tuple[int, str]]:
    compressed = []
    ix = 0
    while ix < len(row_cycle):
        col_id, ch = row_cycle[ix]
        if ch == "|":
            compressed.append((col_id, "|"))
        elif (ch == "L" and row_cycle[ix + 1][1] == "7") or (
            ch == "F" and row_cycle[ix + 1][1] == "J"
        ):
            compressed.append((col_id, "|"))
            ix += 1
        ix += 1
    return compressed


def test_compress_row_cycle():
    assert compress_row_cycle([(0, "F"), (2, "7")]) == []
    assert compress_row_cycle([(0, "L"), (2, "J")]) == []
    assert compress_row_cycle([(0, "L"), (2, "7"), (3, "|")]) == [
        (0, "|"),
        (3, "|"),
    ]
    assert compress_row_cycle([(0, "|"), (3, "|")]) == [
        (0, "|"),
        (3, "|"),
    ]


def count_area_inside_cycle(
    cycle: List[Point], symbols: Dict[Tuple[int, int], str]
) -> int:
    cycle.sort()
    min_row = min(cycle)[0]
    max_row = max(cycle)[0]
    cycle_id = 0
    num_inside_points = 0
    for row_id in range(min_row, max_row + 1):
        row_cycle = []
        while cycle_id < len(cycle) and cycle[cycle_id][0] == row_id:
            if symbols[cycle[cycle_id]] != "-":
                row_cycle.append((cycle[cycle_id][1], symbols[cycle[cycle_id]]))
            cycle_id += 1
        compressed_row_cycle = compress_row_cycle(row_cycle)
        for ix in range(0, len(compressed_row_cycle), 2):
            row_cycle_set = set(cycle)
            for col_id in range(
                compressed_row_cycle[ix][0] + 1, compressed_row_cycle[ix + 1][0]
            ):
                if (row_id, col_id) not in row_cycle_set:
                    num_inside_points += 1
    return num_inside_points


def solution(fname: str) -> int:
    graph = dict()
    s = (0, 0)
    symbols = dict()
    with open(fname) as f:
        for row_id, line in enumerate(f):
            for col_id, ch in enumerate(line.strip()):
                if ch == "S":
                    s = (row_id, col_id)
                graph[(row_id, col_id)] = map_symbol((row_id, col_id), ch)
                symbols[(row_id, col_id)] = ch
    for ch in "|-LJ7F":
        if set(get_neighbors(graph, s)) == set(map_symbol(s, ch)):
            symbols[s] = ch
    cycle = traverse_graph(graph, s)
    return count_area_inside_cycle(cycle, symbols)


if __name__ == "__main__":
    print(solution("./input.txt"))
