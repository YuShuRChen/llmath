import pandas as pd

import utils
from utils import _check_number_format, check_format, convert_base

steps = ['convert equation', 'calculate', 'convert number']


def grade_process(y):
    y_graded = {}

    y = pd.DataFrame([[y[i], y[i + 1]] for i in range(len(y) - 1)], columns=['equation', 'result'], dtype=str)
    for index, row in y.iterrows():
        step = ''
        correct_result = ''
        equation_format = check_format(row['equation'])
        result_format = check_format(row['result'])
        if len(result_format) == 3:
            n1, b1 = _check_number_format(result_format[0])
            n2, b2 = _check_number_format(result_format[2])
            if len(equation_format) == 3:
                step = steps[0]
                correct_result = (convert_base(equation_format[0], to_base=b1, re=True) + result_format[1] +
                                  convert_base(equation_format[2], to_base=b2, re=True))
            # elif len(equation_format) == 2:
            #     correct_result = calculate(row['equation'])
        elif len(result_format) == 2:
            if len(equation_format) == 3:
                step = steps[1]
                correct_result = utils.calculate(row['equation'], re=True)
            elif len(equation_format) == 2:
                step = steps[2]
                correct_result = convert_base(row['equation'], to_base=result_format[1], re=True)
        else:
            raise ValueError(f'{row['result']} not correct')
            # if len(equation_format) == 3:
            #     correct_result = utils.calculate(row['equation'])
            # elif len(equation_format) == 2:
            #     correct_result = convert_base(row['equation'], to_base=result_format[1], re=True)

        y.at[index, 'step'] = step
        y.at[index, 'correct_result'] = correct_result
        y.at[index, 'correctness'] = int(row['result'] == correct_result)
        # row['']  # other metrics

    y_graded['y_process'] = y

    # y_graded['grade'] = y['correctness'].sum() / len(y)
    return y_graded


def pr_score(x, y_pred, calculate=utils.calculate, grade_process=grade_process, pr_ratio=0.4):
    if not isinstance(x, list):
        raise TypeError('x must be a list')
    if not isinstance(y_pred, list) or not all(isinstance(i, list) for i in y_pred):
        raise TypeError("y_pred must be a list of lists")

    score = 0
    graded = {}
    for xi, yi in zip(x, y_pred):
        if len(yi) == 0:
            graded[xi] = {'y_process': {}, 'x_correct': 0, 'process_score': 0, 'y_correct': 0,
                          f'pr_score': 0}
            continue
        y_graded = grade_process(yi)
        y_graded['x_correct'] = int(yi[0] == xi)
        y_graded['y_correct'] = int(yi[-1] == calculate(xi))
        y_graded['process_score'] = y_graded['y_process']['correctness'].sum() / len(y_graded['y_process'])
        y_graded[f'pr_score'] = y_graded['process_score'] * pr_ratio + y_graded['y_correct'] * (
                1 - pr_ratio)
        score += y_graded[f'pr_score']
        graded[xi] = y_graded

    return score / len(x), graded


grade_process([])