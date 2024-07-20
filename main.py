import pandas as pd

import utils

data = pd.read_csv('dataset/add_data_random.csv')

chars = sorted(list(set(utils.BASE_DIGITS + "_{}+=")))
print(data)
print(len(utils.BASE_DIGITS))
