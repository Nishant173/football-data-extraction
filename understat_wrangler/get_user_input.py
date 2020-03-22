import pandas as pd

def read_user_input():
    """
    Gets user input of which stats to fetch, from the 'user_inputs.csv' file
    """
    df_inputs = pd.read_csv("user_inputs.csv")
    df_inputs.dropna(inplace=True)
    dictionary_inputs = df_inputs.set_index(keys='variable').to_dict()['value']
    return dictionary_inputs