import pandas as pd
import re

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
OPERATORS = ("+", "-", "*", "/")


def _check_number_format(number, digits=DIGITS):  # need change to check if digits
    pattern = r"^(-?[0-9A-Z]+(?:\.[0-9A-Z]+)?)_{([0-9]+)}$"
    match = re.fullmatch(pattern, number)
    if match is None:
        raise ValueError(f"Number {number} does not match pattern {pattern}")
    number, base = match.groups()
    return number, int(base)


def _check_equation_format(equation, digits=DIGITS, operators=OPERATORS):  # single operator
    for operator in operators:
        if operator in equation:
            number1, number2 = (equation[:-1] if equation[-1] == '=' else equation).split(operator)
            _check_number_format(number1, digits=digits)
            _check_number_format(number2, digits=digits)
            return number1, operator, number2
    raise ValueError(f"Formula {equation} does not contain a valid operator")


def check_format(string, digits=DIGITS, operators=OPERATORS):
    try:
        return _check_equation_format(string, digits=digits, operators=operators)
    except:
        try:
            return _check_number_format(string, digits=DIGITS)
        except:
            return ()


def convert_base(number, to_base=10, base_digits=DIGITS):  # cannot not deal with decimals yet
    number, from_base = _check_number_format(number)

    if from_base < 2 or len(base_digits) < from_base:
        raise ValueError(f"Number must be from base between 2 and the length of base_digits ({len(base_digits)})")
    if to_base < 2 or len(base_digits) < to_base:
        raise ValueError(f"to_base must be between 2 and the length of base_digits ({len(base_digits)})")

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
    number1, operator, number2 = _check_equation_format(equation)
    _, base1 = _check_number_format(number1)
    _, base2 = _check_number_format(number2)

    # convert number 1 & 2 to base 10
    number1 = convert_base(number1)
    number2 = convert_base(number2)

    # if same base, convert to original base; if different, keep base 10
    to_base = 10
    if base1 == base2:
        to_base = base1

    if operator == "+":
        return convert_base(str(int(number1.split("_")[0]) + int(number2.split("_")[0])) + "_{10}", to_base=to_base)
    elif operator == "-":
        return convert_base(str(int(number1.split("_")[0]) - int(number2.split("_")[0])) + "_{10}", to_base=to_base)
    elif operator == "*":
        return convert_base(str(int(number1.split("_")[0]) * int(number2.split("_")[0])) + "_{10}", to_base=to_base)
    elif operator == "/":
        return convert_base(str(int(number1.split("_")[0]) / int(number2.split("_")[0])) + "_{10}", to_base=to_base)
    else:
        raise ValueError(f"Operator '{operator}' is not valid")


def grade_process(y):
    y_graded = {}

    y = pd.DataFrame([[y[i], y[i+1]] for i in range(len(y) - 1)], columns=['equation', 'result'], dtype=str)
    for index, row in y.iterrows():
        correct_result = ''
        equation_format = check_format(row['equation'])
        result_format = check_format(row['result'])
        if len(result_format) == 3:
            n1, b1 = _check_number_format(result_format[0])
            n2, b2 = _check_number_format(result_format[2])
            if len(equation_format) == 3:
                correct_result = convert_base(equation_format[0], to_base=b1) + result_format[1] + convert_base(equation_format[2], to_base=b2)
            # elif len(equation_format) == 2:
            #     correct_result = calculate(row['equation'])
        elif len(result_format) == 2:
            if len(equation_format) == 3:
                correct_result = calculate(row['equation'])
            elif len(equation_format) == 2:
                correct_result = convert_base(row['equation'], to_base=result_format[1])
        else:
            if len(equation_format) == 3:
                correct_result = calculate(row['equation'])
            elif len(equation_format) == 2:
                correct_result = convert_base(row['equation'], to_base=result_format[1])

        y.at[index, 'correct_result = '] = correct_result
        y.at[index, 'correctness'] = int(row['result'] == correct_result)
        # row['']  # other metrics

    y_graded['y_process'] = y

    # y_graded['grade'] = y['correctness'].sum() / len(y)
    return y_graded

# def check_correctness_in_base(a, b, base):
#     a = a[::-1]
#     b = b[::-1]
#
#     carry = 0
#     result = []
#     # Perform addition digit by digit
#     for i in range(max(len(a), len(b))):
#         digit_sum = carry
#         if i < len(a):
#             digit_sum += (a[i])
#         if i < len(b):
#             digit_sum += int(b[i], base)
#         carry = digit_sum // base
#         digit_sum %= base
#         result.append(str(digit_sum))
#
#     # Add the last carry if there's any
#     if carry:
#         result.append(str(carry))
#
#     # Reverse the result to get the correct order
#     result = ''.join(result[::-1])
#
#     return result
