import utils
from pipeline import execute_pipeline

if __name__ == "__main__":
    try:
        utils.run_and_timeit(func=execute_pipeline)
        print("Data has been extracted and wrangled!")
    except Exception as e:
        print("Failed! ErrorMsg: {}".format(e))