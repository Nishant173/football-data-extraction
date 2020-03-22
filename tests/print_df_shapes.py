import os
import pandas as pd

def get_filenames():
    """ Get list of CSV/Excel filenames present in the current working
    directory (also includes files present in the tree, going downwards) """
    filenames = list()
    cwd = os.getcwd()
    for (_, _, files) in os.walk(cwd):
        filenames.extend(files)
    filenames = [file for file in filenames if str(file).lower().strip()[-4:] in ['.csv', 'xlsx']]
    return filenames


if __name__ == "__main__":
    filenames = get_filenames()
    for index, filename in enumerate(filenames):
        try:
            df = pd.read_csv(filename, encoding='latin-1')
            print(f"Shape: {df.shape} --> File #{index+1}: '{filename}'")
        except pd.errors.EmptyDataError:
            print(f"EMPTY --> File #{index+1}: '{filename}'")
    input("\nPress 'Enter' or 'Return' to close window!")