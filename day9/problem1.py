from typing import List


def check_all_equal(vals: List[int], left: int, right: int) -> bool:
    for ix in range(left, right):
        if vals[ix] != vals[left]:
            return False
    return True


def test_check_all_equal():
    assert check_all_equal([1, 2], 0, 1)
    assert check_all_equal([1, 2, 2], 1, 3)
    assert not check_all_equal([1, 1, 2], 0, 3)


# 1   3   6  10  15  21
# 1   2   3  4   5   6
# 1   2   1  1   1   1  1
# 1   2   3  4   5   6  7
# 1   3   6  10  15  21 28


def predict_next_value(vals: List[int]) -> int:
    shift = 0
    # go down
    while not check_all_equal(vals, shift, len(vals)):
        shift += 1
        for ix in range(len(vals) - 1, shift - 1, -1):
            vals[ix] = vals[ix] - vals[ix - 1]
    vals.append(vals[len(vals) - 1])
    # go up
    for s in range(shift, 0, -1):
        for ix in range(s, len(vals)):
            vals[ix] = vals[ix - 1] + vals[ix]
    return vals[len(vals) - 1]


def test_predict_next_value():
    assert predict_next_value([1, 3, 6, 10, 15, 21]) == 28
    assert predict_next_value([1, 1]) == 1


def solution(fname: str) -> int:
    s = 0
    with open(fname) as f:
        for line in f:
            vals = list(map(int, line.split(" ")))
            s += predict_next_value(vals)
    return s


if __name__ == "__main__":
    print(solution("./input.txt"))
