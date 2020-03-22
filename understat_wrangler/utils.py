import os
import joblib
import time
import json
import datetime
import pandas as pd

use_timestamp = True

if use_timestamp:
    current_timestamp = str(datetime.datetime.now()).replace('-', '_')\
                                                    .replace(' ', '_')\
                                                    .replace(':', '_')[:19]
    global_foldername = "results_{}".format(current_timestamp)
else:
    global_foldername = "results"



def create_global_results_folder():
    try:
        os.mkdir('../{}'.format(global_foldername))
    except FileExistsError:
        pass
    return None


def save_data_to_csv(dataframe, name):
    """
    Saves DataFrame to Excel/CSV file (in current working directory).
    Parameters:
        - dataframe (Pandas DataFrame): DataFrame to save
        - name (str): Storage name of Excel/CSV file
    """

    dataframe.to_csv("../{}/{}.csv".format(global_foldername, name),
                     index=False,
                     sep=',',
                     encoding='latin-1')
    return None


def pickle_load(filename):
    """ Loads data from pickle file, via joblib module """
    data_obj = joblib.load(filename=filename)
    return data_obj


def pickle_save(data_obj, filename):
    """ Stores data as pickle file, via joblib module """
    joblib.dump(value=data_obj, filename=filename)
    return None


def convert_dtypes(dataframe, columns, dtypes):
    """
    Converts datatypes of columns in DataFrame.
    Parameters:
        - dataframe (Pandas DataFrame): DataFrame to save
        - columns (list): List of column-names
        - dtypes (list): List of datatypes (in same order as columns)
    Usage example:
        - convert_dtypes(dataframe=df, columns=['age', 'name', 'gpa'], dtypes=['int', 'str', 'float'])
    Returns DataFrame with specified columns converted to appropriate datatype.
    """
    dataframe_altered = dataframe.copy()
    columns_in_dataframe = dataframe_altered.columns.tolist()
    for column, dtype in zip(columns, dtypes):
        if column in columns_in_dataframe:
            dataframe_altered[column] = dataframe_altered[column].astype(dtype)
    return dataframe_altered


def run_and_timeit(func):
    """ Takes in function name; runs it; and returns time taken in minutes """
    start = time.time()
    func()
    end = time.time()
    time_taken_in_minutes = round((end - start) / 60, 2)
    return time_taken_in_minutes