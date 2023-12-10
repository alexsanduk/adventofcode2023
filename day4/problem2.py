from typing import List, Tuple


def get_matches(win_numbers: List[int], numbers: List[int]) -> int:
    return len(set(win_numbers).intersection(set(numbers)))


def test_get_matches():
    assert get_matches([1, 2, 3], [1]) == 1
    assert get_matches([1, 2, 3], [4]) == 0
    assert get_matches([1, 2, 3], [1, 2]) == 2
    assert get_matches([1, 2, 3], [1, 2, 3]) == 3
    assert get_matches([1, 2, 3], [1, 2, 2, 3]) == 3


def update_cards(matches: List[int], cards: List[int]) -> List[int]:
    n = len(cards)
    for card_id in range(n - 1, -1, -1):
        for next_card_id in range(card_id + 1, min(card_id + 1 + matches[card_id], n)):
            cards[card_id] += cards[next_card_id]
    return cards


def test_update_cards():
    assert update_cards([0], [1]) == [1]
    assert update_cards([1, 0], [1, 1]) == [2, 1]
    assert update_cards([1, 1, 1], [1, 1, 1]) == [3, 2, 1]


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
    matches = []
    with open(fname) as f:
        for line in f:
            win_numbers, numbers = parse_line(line)
            matches.append(get_matches(win_numbers, numbers))
    cards = [1] * len(matches)
    cards = update_cards(matches, cards)
    return sum(cards)


if __name__ == "__main__":
    print(solution("./input.txt"))
