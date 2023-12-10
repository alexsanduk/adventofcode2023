from typing import Dict, Tuple
import re


def build_tree(line, tree: Dict[str, Tuple[str, str]]) -> Dict[str, Tuple[str, str]]:
    res = re.search(
        r"(?P<node>[A-Z]{3}) = \((?P<left>[A-Z]{3}), (?P<right>[A-Z]{3})\)", line
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


def get_num_steps(tree: Dict[str, Tuple[str, str]], instructions: str) -> int:
    num_steps = 0
    cur_node = "AAA"
    step_id = 0
    n = len(instructions)
    while True:
        num_steps += 1
        if instructions[step_id] == "L":
            cur_node = tree[cur_node][0]
        else:
            cur_node = tree[cur_node][1]
        if cur_node == "ZZZ":
            break
        step_id = (step_id + 1) % n
    return num_steps


def solution(fname: str) -> int:
    tree = dict()
    with open(fname) as f:
        instructions = f.readline().strip()
        f.readline()
        for line in f:
            tree = build_tree(line, tree)
    return get_num_steps(tree, instructions)


if __name__ == "__main__":
    print(solution("./input.txt"))
