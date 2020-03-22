import utils
from pipeline import execute_pipeline


if __name__ == "__main__":
    time_taken = utils.run_and_timeit(func=execute_pipeline)
    print("Time taken: {} minutes".format(time_taken))
    print("Data has been extracted and wrangled!")