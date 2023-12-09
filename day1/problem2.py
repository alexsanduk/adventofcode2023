import sys
import re


def get_number(s: str) -> int:
    digits = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    r = re.compile(r"\d|" + "|".join(digits.keys()))
    first_digit = ""
    res = r.search(s)
    if res:
        first_digit = digits.get(res.group(), res.group())
    reversed_digits = dict()
    for d_name, d_val in digits.items():
        reversed_digits[d_name[::-1]] = d_val
    r = re.compile(r"\d|" + "|".join(reversed_digits.keys()))
    last_digit = ""
    res = r.search(s[::-1])
    if res:
        last_digit = reversed_digits.get(res.group(), res.group())
    return int(first_digit + last_digit)


def solution(input_file: str):
    s = 0
    with open(input_file) as f:
        for line in f:
            s += get_number(line)
            # print(get_number(line))
    print(s)


if __name__ == "__main__":
    solution(sys.argv[1])
