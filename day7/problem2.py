from typing import Tuple
from collections import Counter
import functools


Hand = Tuple[int, int, int, int, int]


def map_jokers_decorator(func):
    @functools.wraps(func)
    def wrapper(hand):
        c = Counter(hand)
        val, max_count = c.most_common(1)[0]
        if val == 1 and max_count == 5:
            val = 14
        elif val == 1:
            val = c.most_common(2)[1][0]
        new_hand = [val if c == 1 else c for c in hand]
        return func(tuple(new_hand))

    return wrapper


def map_hand(s: str) -> Hand:
    letter_to_val = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 1,
        "T": 10,
    }
    return (
        int(letter_to_val.get(s[0], s[0])),
        int(letter_to_val.get(s[1], s[1])),
        int(letter_to_val.get(s[2], s[2])),
        int(letter_to_val.get(s[3], s[3])),
        int(letter_to_val.get(s[4], s[4])),
    )


assert map_hand("AAAAA") == (14, 14, 14, 14, 14)
assert map_hand("AA8AA") == (14, 14, 8, 14, 14)


@map_jokers_decorator
def is_five_kind(p: Hand) -> bool:
    count = Counter(p)
    return count.most_common(1)[0][1] == 5


assert is_five_kind((14, 14, 14, 14, 14))
assert is_five_kind((1, 14, 14, 14, 14))
assert not is_five_kind((14, 14, 14, 14, 8))


@map_jokers_decorator
def is_four_kind(p: Hand) -> bool:
    count = Counter(p)
    return count.most_common(1)[0][1] == 4


assert is_four_kind((14, 14, 14, 14, 9))
assert not is_four_kind((14, 14, 14, 8, 9))
assert not is_four_kind((14, 14, 14, 14, 14))
assert is_four_kind((14, 1, 8, 14, 14))


@map_jokers_decorator
def is_full_house(p: Hand) -> bool:
    count = Counter(p)
    if len(count.keys()) == 1:
        return False
    t1, t2 = count.most_common(2)
    return t1[1] == 3 and t2[1] == 2


assert is_full_house((14, 14, 14, 13, 13))
assert not is_full_house((14, 14, 14, 8, 9))
assert not is_full_house((14, 14, 14, 14, 14))
assert not is_full_house((14, 14, 14, 14, 14))
assert is_full_house((14, 14, 1, 8, 8))


@map_jokers_decorator
def is_three_kind(p: Hand) -> bool:
    count = Counter(p)
    if len(count.keys()) == 1:
        return False
    t1, t2 = count.most_common(2)
    return t1[1] == 3 and t2[1] == 1


assert not is_three_kind((14, 14, 14, 13, 13))
assert is_three_kind((14, 14, 14, 8, 9))
assert not is_three_kind((14, 14, 14, 14, 14))
assert is_three_kind((14, 14, 1, 8, 9))


@map_jokers_decorator
def is_two_pair(p: Hand) -> bool:
    count = Counter(p)
    if len(count.keys()) == 1:
        return False
    t1, t2 = count.most_common(2)
    return t1[1] == 2 and t2[1] == 2


assert is_two_pair((13, 14, 14, 13, 12))
assert not is_two_pair((14, 14, 14, 13, 12))
assert not is_two_pair((14, 14, 14, 14, 14))


@map_jokers_decorator
def is_one_pair(p: Hand) -> bool:
    count = Counter(p)
    if len(count.keys()) == 1:
        return False
    t1, t2 = count.most_common(2)
    return t1[1] == 2 and t2[1] == 1


assert is_one_pair((2, 3, 2, 4, 5))
assert not is_one_pair((2, 3, 2, 3, 5))
assert not is_one_pair((14, 14, 14, 14, 14))
assert is_one_pair((2, 1, 3, 4, 5))


@map_jokers_decorator
def is_high_card(p: Hand) -> bool:
    count = Counter(p)
    return count.most_common(1)[0][1] == 1


assert is_high_card((14, 13, 12, 11, 10))
assert not is_high_card((14, 13, 10, 11, 10))
assert not is_high_card((14, 14, 14, 14, 14))
assert not is_high_card((14, 1, 12, 11, 10))


def solution(fname: str) -> int:
    hands = []
    with open(fname) as f:
        for line in f:
            hand_str, bid = line.strip().split(" ", 1)
            hand = map_hand(hand_str)
            bid = int(bid)
            hands.append(
                (
                    is_five_kind(hand),
                    is_four_kind(hand),
                    is_full_house(hand),
                    is_three_kind(hand),
                    is_two_pair(hand),
                    is_one_pair(hand),
                    is_high_card(hand),
                    hand,
                    hand_str,
                    bid,
                )
            )
    hands.sort()
    total_winnings = 0
    for rank, hand_info in enumerate(hands):
        total_winnings += (rank + 1) * hand_info[-1]
    return total_winnings


print(solution("./input.txt"))
