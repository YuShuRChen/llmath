import numpy as np
import pandas as pd

import utils


# def _check_pr_score_targets(x, y_pred):
#     if not isinstance(x, list):
#         raise TypeError('x must be a list')
#     if not isinstance(y_pred, list) or not all(isinstance(i, list) for i in y_pred):
#         raise TypeError("y_pred must be a list of lists")
#     return x, y_pred


def pr_score(x, y_pred, calculate=utils.calculate, grade_process=utils.grade_process, pr_ratio=0.4):
    # x, y_pred = _check_pr_score_targets(x, y_pred)
    if not isinstance(x, list):
        raise TypeError('x must be a list')
    if not isinstance(y_pred, list) or not all(isinstance(i, list) for i in y_pred):
        raise TypeError("y_pred must be a list of lists")

    score = 0
    graded = {}
    for xi, yi in zip(x, y_pred):
        if len(yi) == 0:
            graded[xi] = {'y_process': {}, 'x_correctness': 0, 'y_correctness': 0, 'process_score': 0, f'pr_score({pr_ratio})': 0}
            continue
        y_graded = grade_process(yi)
        y_graded['x_correctness'] = int(yi[0] == xi)
        y_graded['y_correctness'] = int(yi[-1] == calculate(xi))
        y_graded['process_score'] = y_graded['y_process']['correctness'].sum() / len(y_graded['y_process'])
        y_graded[f'pr_score({pr_ratio})'] = y_graded['process_score'] * pr_ratio + y_graded['y_correctness'] * (1 - pr_ratio)
        score += y_graded[f'pr_score({pr_ratio})']
        graded[xi] = y_graded

    return score / len(x), graded
