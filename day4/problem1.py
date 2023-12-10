from typing import List, Tuple


def get_matches(win_numbers: List[int], numbers: List[int]) -> int:
    return len(set(win_numbers).intersection(set(numbers)))


def test_get_matches():
    assert get_matches([1, 2, 3], [1]) == 1
    assert get_matches([1, 2, 3], [4]) == 0
    assert get_matches([1, 2, 3], [1, 2]) == 2
    assert get_matches([1, 2, 3], [1, 2, 3]) == 3
    assert get_matches([1, 2, 3], [1, 2, 2, 3]) == 3


def mypower(to: int):
    if to == 0:
        return 1
    elif to % 2 == 1:
        val = mypower((to - 1) // 2)
        return 2 * val * val
    else:
        val = mypower(to // 2)
        return val * val


def test_mypower():
    assert mypower(0) == 1
    assert mypower(1) == 2
    assert mypower(2) == 4
    assert mypower(3) == 8


def get_points(matches: int) -> int:
    if matches == 0:
        return 0
    else:
        return mypower(matches - 1)


def test_get_points():
    assert get_points(0) == 0
    assert get_points(1) == 1
    assert get_points(2) == 2
    assert get_points(3) == 4


def parse_line(line: str) -> Tuple[List[int], List[int]]:
    _, all_numbers = line.rsplit(":")
    win_numbers, numbers = all_numbers.split("|")
    win_numbers = list(map(int, win_numbers.strip().split()))
    numbers = list(map(int, numbers.strip().split()))
    return win_numbers, numbers


def test_parse_line():
    assert parse_line("Card 1: 41 | 83") == ([41], [83])
    assert parse_line("Card 1: 41 24 | 83") == ([41, 24], [83])
    assert parse_line("Card 1: 41 24 | 83 25") == ([41, 24], [83, 25])


def solution(fname: str) -> int:
    total_points = 0
    with open(fname) as f:
        for line in f:
            win_numbers, numbers = parse_line(line)
            matches = get_matches(win_numbers, numbers)
            total_points += get_points(matches)
    return total_points


if __name__ == "__main__":
    print(solution("./input.txt"))
