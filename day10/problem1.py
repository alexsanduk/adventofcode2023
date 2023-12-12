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


def build_graph(graph: Graph, p: Point, ch: str) -> Graph:
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
    graph[(i, j)] = mapping[ch]
    return graph


def test_build_graph():
    assert build_graph(dict(), (1, 1), "|") == {(1, 1): [(0, 1), (2, 1)]}
    assert build_graph(dict(), (1, 1), "J") == {(1, 1): [(1, 0), (0, 1)]}


def traverse_graph(graph: Graph, s: Point) -> int:
    prev_point = s
    cur_point = s
    cycle_length = 0
    while True:
        print(prev_point, cur_point)
        p1 = get_neighbors(graph, cur_point)[0]
        if p1 == prev_point:
            p1 = get_neighbors(graph, cur_point)[1]
        prev_point = cur_point
        cur_point = p1
        cycle_length += 1
        if cur_point == s:
            break
    return cycle_length // 2


def solution(fname: str) -> int:
    graph = dict()
    s = (0, 0)
    with open(fname) as f:
        for row_id, line in enumerate(f):
            for col_id, ch in enumerate(line.strip()):
                if ch == "S":
                    s = (row_id, col_id)
                build_graph(graph, (row_id, col_id), ch)
    # for k, v in graph.items():
    #     print(k, v)
    return traverse_graph(graph, s)


if __name__ == "__main__":
    print(solution("./test.txt"))
