import numpy as np
import pandas as pd

import utils


def _check_pr_score_targets(y_pred):
    if not isinstance(y_pred, list) or not all(isinstance(i, list) for i in y_pred):
        raise ValueError("y_pred should be a list of lists")

    for i in range(len(y_pred)):
        y = [(y_pred[i][j], y_pred[i][j+1]) for j in range(len(y_pred[i])-1)]
        y_pred[i] = pd.DataFrame(y, columns=['equation', 'result'], dtype=str)

    return y_pred


def pr_score(y_pred, scoring=utils.score_add, pr_ratio=0.4):
    y_pred = _check_pr_score_targets(y_pred)

    score = 0
    for i in range(len(y_pred)):
        y_pred[i]['score'] = y_pred[i].apply(lambda y: scoring(y['equation'], y['result']), axis=1)
        process_score = y_pred[i]['score'].sum() / len(y_pred[i])
        score = process_score * pr_ratio

    return score
