import re

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
OPERATORS = ["+", "-", "*", "/"]


def _check_number_format(number):
    pattern = r"^(-?[0-9A-Z]+(?:\.[0-9A-Z]+)?)_{([0-9]+)}$"
    match = re.fullmatch(pattern, number)
    if match is None:
        raise ValueError(f"Number {number} does not match pattern {pattern}")
    number, base = match.groups()
    return number, int(base)


def _check_formula_format(formula):
    for operator in OPERATORS:
        if operator in formula:
            number1, number2 = formula.split(operator)
            _check_number_format(number1)
            _check_number_format(number2)
            return number1, operator, number2
    raise ValueError(f"Formula {formula} does not contain a valid operator")


def convert_base(number, to_base=10):  # , base_digits=BASE_DIGITS):
    base_digits = DIGITS

    number, from_base = _check_number_format(number)
    if from_base < 2 or len(base_digits) < from_base:
        raise ValueError(f"Base must be between 2 and length of base_digits ({len(base_digits)})")

    negative = False
    if number[0] == '-':
        negative = True
        number = number[1:]

    n = 0
    if from_base == 10:
        n = int(number)
    # from_base to base 10
    else:
        for i, digit in enumerate(number[::-1]):
            if digit not in base_digits[:from_base]:
                raise ValueError(f"Digit '{digit}' is not valid")
            n += base_digits.index(digit) * (from_base ** i)

    result = ""
    if to_base == 10:
        result = str(n)
    # from base 10 to_base
    elif n == 0:
        result = "0"
    else:
        while n > 0:
            result = base_digits[n % to_base] + result
            n //= to_base

    return ("-" if negative else "") + result + f"_{{{to_base}}}"


def calculate(equation):
    number1, operator, number2 = _check_formula_format(equation[:-1])
    _, base1 = _check_number_format(number1)
    _, base2 = _check_number_format(number2)

    number1 = convert_base(number1)
    number2 = convert_base(number2)

    to_base = 10
    if base1 == base2:
        to_base = base1

    if operator == "+":
        return convert_base(str(int(number1.split("_")[0]) + int(number2.split("_")[0])) + "_{10}", to_base=to_base)
    elif operator == "-":
        return convert_base(str(int(number1.split("_")[0]) - int(number2.split("_")[0])) + "_{10}", to_base=to_base)
    elif operator == "*":
        return convert_base(str(int(number1.split("_")[0]) * int(number2.split("_")[0])) + "_{10}", to_base=to_base)
    else:
        return convert_base(str(int(number1.split("_")[0]) / int(number2.split("_")[0])) + "_{10}", to_base=to_base)


def score_add(equation, result):
    return 0
