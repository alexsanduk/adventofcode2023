import re


def is_valid_speed(speed, total_time, max_distance) -> bool:
    return (total_time - speed) * speed > max_distance


def test_is_valid_speed():
    assert not is_valid_speed(0, 1, 1)
    assert is_valid_speed(1, 3, 1)


def read_number(line: str) -> int:
    return int("".join(re.findall(r"\d+", line)))


def test_read_number():
    assert read_number("Time:      7  15   30") == 71530
    assert read_number("Time:      7") == 7


def find_good_speed(total_time: int, max_distance: int, left: int, right: int) -> int:
    if left < right:
        mid = left + (right - left) // 2
        if is_valid_speed(mid, total_time, max_distance):
            return mid
        ret = find_good_speed(total_time, max_distance, left, mid)
        if ret > 0:
            return ret
        else:
            return find_good_speed(total_time, max_distance, mid + 1, right)
    return -1


def test_find_good_speed():
    assert find_good_speed(7, 9, 0, 7) == 3


def find_most_left(total_time: int, max_distance: int, left: int, right: int) -> int:
    while left < right:
        mid = left + (right - left) // 2
        if is_valid_speed(mid, total_time, max_distance):
            right = mid
        else:
            left = mid + 1
    return left


def test_find_most_left():
    assert find_most_left(7, 9, 0, 3) == 2


def find_most_right(total_time: int, max_distance: int, left: int, right: int) -> int:
    while left < right:
        mid = left + (right - left) // 2
        if is_valid_speed(mid, total_time, max_distance):
            left = mid + 1
        else:
            right = mid
    return left - 1


def test_find_most_right():
    assert find_most_right(7, 9, 3, 7) == 5


def solution(fname: str) -> int:
    with open(fname) as f:
        total_time = read_number(f.readline())
        max_distance = read_number(f.readline())
    mid = find_good_speed(total_time, max_distance, 0, total_time)
    most_left = find_most_left(total_time, max_distance, 0, mid)
    most_right = find_most_right(total_time, max_distance, mid, total_time)
    return most_right - most_left + 1


if __name__ == "__main__":
    print(solution("./input.txt"))
