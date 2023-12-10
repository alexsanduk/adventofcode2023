from typing import Dict


def get_set_colors(s) -> Dict[str, int]:
    s = s.strip()
    d = dict()
    for num_with_color in s.split(","):
        num_with_color = num_with_color.strip()
        num, color = num_with_color.split(" ")
        num = int(num)
        color = color.strip()
        d[color] = num
    return d


def test_get_set_colors():
    assert get_set_colors("3 blue") == {"blue": 3}
    assert get_set_colors("3 blue, 4 red") == {"red": 4, "blue": 3}
    assert get_set_colors("3 blue, 4 red, 5 green") == {"red": 4, "blue": 3, "green": 5}


def update_colors(colors: Dict[str, int], new_colors: Dict[str, int]) -> Dict[str, int]:
    for col, val in new_colors.items():
        if col in colors:
            colors[col] = max(colors[col], val)
        else:
            colors[col] = val
    return colors


def test_update_colors():
    assert update_colors({"green": 7}, {"blue": 10, "green": 5}) == {
        "green": 7,
        "blue": 10,
    }
    assert update_colors({"green": 4}, {"blue": 10, "green": 5}) == {
        "green": 5,
        "blue": 10,
    }
    assert update_colors({"green": 4}, {"blue": 10}) == {"green": 4, "blue": 10}


def get_game_min_colors(sets) -> Dict[str, int]:
    sets = sets.strip()
    colors = dict()
    for s in sets.split(";"):
        new_colors = get_set_colors(s)
        colors = update_colors(colors, new_colors)
    return colors


def test_get_game_min_colors():
    assert get_game_min_colors("3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == {
        "blue": 6,
        "green": 2,
        "red": 4,
    }
    assert get_game_min_colors(
        "1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"
    ) == {
        "blue": 4,
        "green": 3,
        "red": 1,
    }


def mypower(colors: Dict[str, int]) -> int:
    power = 1
    for _, val in colors.items():
        power *= val
    return power


def test_mypower():
    assert mypower({"blue": 10}) == 10
    assert mypower({"blue": 10, "green": 2}) == 20
    assert mypower({"blue": 10, "green": 2, "red": 5}) == 100


def solution(input_file) -> int:
    sum_powers = 0
    with open(input_file) as f:
        for line in f:
            _, sets = line.split(":", 1)
            colors = get_game_min_colors(sets)
            sum_powers += mypower(colors)
    return sum_powers


if __name__ == "__main__":
    print(solution("./input.txt"))
