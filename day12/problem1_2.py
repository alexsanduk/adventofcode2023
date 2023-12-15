from typing import Tuple
from functools import cache
import time


@cache
def count(code: str, blocks: Tuple[int, ...]) -> int:
    new_blocks = list(blocks)
    code = ".".join(b for b in code.split(".") if b)
    if code[:2] == "#.":
        if len(new_blocks) == 0 or new_blocks[0] != 1:
            return 0
        else:
            return count(code[2:], tuple(new_blocks[1:]))
    elif code[:2] == "#?" or code[:1] == "?":
        return count(code.replace("?", ".", 1), blocks) + count(
            code.replace("?", "#", 1), blocks
        )
    elif code[:1] == "#":
        if len(new_blocks) == 0 or new_blocks[0] <= 0:
            return 0
        else:
            new_blocks[0] -= 1
            return count(code[1:], tuple(new_blocks))
    else:
        return int(all(b == 0 for b in blocks))


def test_count():
    assert count("??", (1,)) == 2
    assert count("???", (1,)) == 3
    assert count("?.", (1,)) == 1
    assert count(".?", (1,)) == 1
    assert count("#?", (2,)) == 1
    assert count("?#", (2,)) == 1
    assert count("#?.#", (1, 1)) == 1


def read_input(line: str, multiplier) -> Tuple[str, Tuple[int, ...]]:
    code, blocks = line.strip().split(" ")
    code = "?".join([code] * multiplier)
    blocks = list(map(int, blocks.split(",")))
    blocks = blocks * multiplier
    return code, tuple(blocks)


def test_read_input():
    assert read_input("# 1,1", 1) == ("#", (1, 1))
    assert read_input("# 1,1", 2) == ("#?#", (1, 1, 1, 1))


def solution(fname: str, multiplier=1):
    total_count = 0
    with open(fname) as f:
        for line in f:
            code, blocks = read_input(line, multiplier)
            cur_count = count(code, blocks)
            total_count += cur_count
    return total_count


if __name__ == "__main__":
    start = time.time()
    print(solution("input.txt", multiplier=5))
    end = time.time()
    print(end - start)
