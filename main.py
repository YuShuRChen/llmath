import pandas as pd

import utils

data = pd.read_csv('datasets/add_data_random.csv')

chars = sorted(list(set(utils.DIGITS + "_{}+=")))
print(data)
print(len(utils.DIGITS))
