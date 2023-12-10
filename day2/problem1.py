from typing import Dict


def is_valid_set(s, colors: Dict[str, int]) -> bool:
    s = s.strip()
    for num_with_color in s.split(","):
        num_with_color = num_with_color.strip()
        num, color = num_with_color.split(" ")
        num = int(num)
        color = color.strip()
        if colors[color] < num:
            return False
    return True


colors = {"red": 12, "green": 13, "blue": 14}


def test_is_valid_set():
    assert is_valid_set("3 blue, 4 red", colors)
    assert is_valid_set("14 blue, 4 red", colors)
    assert not is_valid_set("15 blue, 4 red", colors)
    assert not is_valid_set("1 blue, 13 red", colors)


def is_valid_game(sets, colors: Dict[str, int]) -> bool:
    sets = sets.strip()
    for s in sets.split(";"):
        if not is_valid_set(s, colors):
            return False
    return True


def test_is_valid_game():
    assert is_valid_game(" 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", colors)
    assert not is_valid_game(" 15 red", colors)
    assert not is_valid_game(
        "8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", colors
    )


def solution(input_file) -> int:
    sum_ids = 0
    colors = {"red": 12, "green": 13, "blue": 14}
    with open(input_file) as f:
        for line in f:
            game_id, sets = line.split(":", 1)
            if is_valid_game(sets, colors):
                sum_ids += int(game_id.rsplit(" ", 1)[-1])
    return sum_ids


if __name__ == "__main__":
    print(solution("input.txt"))
