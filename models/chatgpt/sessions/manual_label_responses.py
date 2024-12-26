#%%
import pandas as pd

#%%
file = 'trm0_gpt-3.5-turbo_10-2-17'
# df_answer = pd.read_csv('../../datasets/test_random_add_0.csv')
df_response = pd.read_csv(file + '/' + file + '.csv')
#%%
# desired_columns = [f'equation_{{{i}}}' for i in range(2, 17)] + [f'answer_{{{i}}}' for i in range(2, 17)]
#%%
df_formatted_response = df_response.copy()

for base in range(2, 17):
    for i in range(10):
        df_formatted_response.loc[i, f"answer_{{{base}}}"] = input(
            "equation: \n" + df_response[f"equation_{{{base}}}"][i] + "\n" +
            "response: \n" + df_response[f"answer_{{{base}}}"][i] + "\n")
        print(df_formatted_response[f"answer_{{{base}}}"][i])
#%%
df_formatted_response.to_csv(file + '/' + file + "_process_formatted.csv", index=False)
