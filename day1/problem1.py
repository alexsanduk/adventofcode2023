import sys


def get_number(s: str) -> int:
    first_digit = ""
    for ix in range(len(s)):
        if ord("0") <= ord(s[ix]) <= ord("9"):
            first_digit = s[ix]
            break
    last_digit = ""
    for ix in range(len(s) - 1, -1, -1):
        if ord("0") <= ord(s[ix]) <= ord("9"):
            last_digit = s[ix]
            break
    return int(first_digit + last_digit)


def solution(input_file: str):
    s = 0
    with open(input_file) as f:
        for line in f:
            s += get_number(line)
    print(s)


if __name__ == "__main__":
    solution(sys.argv[1])
