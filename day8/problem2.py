from typing import Dict, Tuple, Set, List
import re


def build_tree(line, tree: Dict[str, Tuple[str, str]]) -> Dict[str, Tuple[str, str]]:
    res = re.search(
        r"(?P<node>[0-9A-Z]{3}) = \((?P<left>[0-9A-Z]{3}), (?P<right>[0-9A-Z]{3})\)",
        line,
    )
    if res:
        node, left, right = res.group("node"), res.group("left"), res.group("right")
    else:
        node, left, right = "", "", ""
    tree[node] = (left, right)
    return tree


def test_build_tree():
    assert build_tree("AAA = (BBB, CCC)", dict()) == {"AAA": ("BBB", "CCC")}
    assert build_tree("AAA = (BBB, CCC)", {"BBB": ("CCC", "ZZZ")}) == {
        "AAA": ("BBB", "CCC"),
        "BBB": ("CCC", "ZZZ"),
    }


def greatest_common_divisor(a: int, b: int) -> int:
    a, b = min(a, b), max(a, b)
    while b != 0:
        a, b = b, a % b
    return a


def test_greatest_common_divisor():
    assert greatest_common_divisor(1, 16) == 1
    assert greatest_common_divisor(12, 16) == 4


def least_common_denominator(a: int, b: int) -> int:
    g = greatest_common_divisor(a, b)
    return (a * b) // g


def test_least_common_denominator():
    assert least_common_denominator(4, 8) == 8


def least_common_denominator_list(vals: List[int]) -> int:
    lcm = least_common_denominator(vals[0], vals[1])
    for v in vals[2:]:
        lcm = least_common_denominator(v, lcm)
    return lcm


def test_least_common_denominator_list():
    assert least_common_denominator_list([1, 4, 6]) == 12
    assert least_common_denominator_list([2, 4]) == 4


def get_num_steps(
    tree: Dict[str, Tuple[str, str]],
    instructions: str,
    start_nodes: Set[str],
    end_nodes: Set[str],
) -> List[int]:
    num_steps = 0
    cur_nodes = start_nodes
    step_id = 0
    n = len(instructions)
    steps = dict()
    cycles = []
    total_end_nodes = len(end_nodes)
    while True:
        num_steps += 1
        new_cur_nodes = set()
        for node in cur_nodes:
            if instructions[step_id] == "L":
                new_cur_nodes.add(tree[node][0])
            else:
                new_cur_nodes.add(tree[node][1])
        intersection = new_cur_nodes.intersection(end_nodes)
        for node in intersection:
            if node in steps:
                cycles.append(num_steps - steps[node])
                new_cur_nodes.remove(node)
                end_nodes.remove(node)
            steps[node] = num_steps
        if len(cycles) == total_end_nodes:
            break
        cur_nodes = new_cur_nodes
        step_id = (step_id + 1) % n
    return cycles


def solution(fname: str) -> int:
    tree = dict()
    with open(fname) as f:
        instructions = f.readline().strip()
        f.readline()
        for line in f:
            tree = build_tree(line, tree)
    start_nodes = set([node for node in tree.keys() if node.endswith("A")])
    end_nodes = set([node for node in tree.keys() if node.endswith("Z")])
    cycles = get_num_steps(tree, instructions, start_nodes, end_nodes)
    return least_common_denominator_list(cycles)


if __name__ == "__main__":
    print(solution("./input.txt"))
