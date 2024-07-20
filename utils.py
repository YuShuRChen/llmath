import re

BASE_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _check_number_format(number):
    pattern = r"^[A-Z0-9]+_\{\d+\}$"
    if not re.fullmatch(pattern, number):
        raise ValueError(f"Number {number} does not match pattern {pattern}")


def _check_formula_format(formula):
    formula.split("_")
    return


def convert_base(n, base, base_digits=BASE_DIGITS, to_base=True):
    result = ""

    if base < 2 or len(base_digits) < base:
        raise ValueError(f"Base must be between 2 and length of base_digits: {len(base_digits)}")

    if to_base:
        n = int(n)
        if n == 0:
            return base_digits[0]
        while n > 0:
            result = base_digits[n % base] + result
            n //= base
    else:
        result = 0
        for i, digit in enumerate(n[::-1]):
            if digit not in base_digits[:base]:
                raise ValueError(f"Digit '{digit}' is not valid")
            result += base_digits.index(digit) * (base ** i)
        str(result)

    return result


def calculate(equation):
    return 0


def score_add(equation, result):
    return 0
