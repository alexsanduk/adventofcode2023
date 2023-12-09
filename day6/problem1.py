from typing import List
import re


def is_valid_speed(speed, total_time, max_distance) -> bool:
    return (total_time - speed) * speed > max_distance


assert not is_valid_speed(0, 1, 1)
assert is_valid_speed(1, 3, 1)


def count_all_valid_speed(total_time, max_distance) -> int:
    count = 0
    for t in range(total_time + 1):
        if is_valid_speed(t, total_time, max_distance):
            count += 1
    return count


assert count_all_valid_speed(7, 9) == 4
assert count_all_valid_speed(15, 40) == 8


def read_numbers(line: str) -> List[int]:
    return list(map(int, re.findall(r"\d+", line)))


assert read_numbers("Time:      7  15   30") == [7, 15, 30]


def solution(fname: str) -> int:
    with open(fname) as f:
        times = read_numbers(f.readline())
        distances = read_numbers(f.readline())
    product = 1
    for total_time, max_distance in zip(times, distances):
        product *= count_all_valid_speed(total_time, max_distance)
    return product


print(solution("./input.txt"))
