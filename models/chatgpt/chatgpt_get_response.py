import pandas as pd
from openai import OpenAI

client = OpenAI()


def get_response(equation):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # "gpt-4o",
        messages=[
            {"role": "system",
             "content": "You will be provided with an equation, and your task is to compute its correct answer. At the last line of your response, summarize your response by showing the original equation, the intermediate steps, and the final result, in one line in text with each number followed by its base in the format number_{base}."},
            {"role": "user", "content": equation}
        ]
    )
    # completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system",
    #          "content": "You will be provided with an equation, and your task is to return its correct answer."},
    #         {"role": "user", "content": equation}
    #     ]
    # )
    return completion.choices[0].message.content


data = pd.read_csv('../../datasets/test_random_subtract_0.csv')

for idx, row in data.head(10).iterrows():
    for base in range(2, 17):
        equation = row[f'equation_{{{base}}}']
        response = get_response(equation)
        data.at[idx, f'answer_{{{base}}}'] = response
    print(idx)

data.to_csv('sessions/trs0_gpt-3.5-turbo_10-2-17.csv', index=False)
