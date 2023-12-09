from typing import List


def check_all_equal(vals: List[int], left: int, right: int) -> bool:
    for ix in range(left, right):
        if vals[ix] != vals[left]:
            return False
    return True


assert check_all_equal([1, 2], 0, 1)
assert check_all_equal([1, 2, 2], 1, 3)
assert not check_all_equal([1, 1, 2], 0, 3)


# 45 30 21 16 13 10
# 45 -15 -9 -5 -3 -3
# 45 -15 6  4  2  0
# 45 -15 6 -2 -2 -2 -2
# 45 -15 6 4  2  0  -2
# 45 -15 -9 -5 -3 -3 -5
# 45 30 21 16 13 10 5


def predict_next_value(vals: List[int]) -> int:
    vals.reverse()
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


assert predict_next_value([10, 13, 16, 21, 30, 45]) == 5


def solution(fname: str) -> int:
    s = 0
    with open(fname) as f:
        for line in f:
            vals = list(map(int, line.split(" ")))
            s += predict_next_value(vals)
    return s


print(solution("./input.txt"))