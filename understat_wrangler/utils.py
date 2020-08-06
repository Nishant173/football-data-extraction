import os
import joblib
import warnings
import time
import json
import datetime
import numpy as np
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


def get_timetaken_fstring(num_seconds):
    """ Returns formatted-string of time elapsed, given the number of seconds (int) elapsed """
    if num_seconds < 60:
        secs = num_seconds
        fstring_timetaken = f"{secs}s"
    elif 60 < num_seconds < 3600:
        mins, secs = divmod(num_seconds, 60)
        fstring_timetaken = f"{mins}m {secs}s"
    else:
        hrs, secs_remainder = divmod(num_seconds, 3600)
        mins, secs = divmod(secs_remainder, 60)
        fstring_timetaken = f"{hrs}h {mins}m {secs}s"
    return fstring_timetaken


def run_and_timeit(func):
    """
    Takes in function-name; then runs it, times it, and prints out the time taken.
    Parameters:
        - func (object): Object of the function you want to execute.
    """
    start = time.time()
    warnings.filterwarnings(action='ignore')
    func()
    end = time.time()
    timetaken_in_secs = int(np.ceil(end - start))
    timetaken_fstring = get_timetaken_fstring(num_seconds=timetaken_in_secs)
    print(f"\nDone! Time taken: {timetaken_fstring}")
    return None