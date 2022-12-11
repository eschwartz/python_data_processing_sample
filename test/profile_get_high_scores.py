import json
import sys
from time import perf_counter
from highest_scores.get_high_scores import get_high_scores


@profile
def profile_high_score(file_path, max_results):
    start_time = perf_counter()

    with open(file_path) as f:
        # Get the top N scores
        results = get_high_scores(f, max_results)

        # Output results as JSON
        json.dumps(results, indent=2)

    duration = perf_counter() - start_time
    print(f"Complete in {round(duration, 2)}s")


def profile_large_result_set():
    start_time = perf_counter()

    file_path = './example_input_data_3.data'
    max_results = 1000

    with open(file_path) as f:
        # Get the top N scores
        results = get_high_scores(f, max_results)

        # Output results as JSON
        json.dumps(results, indent=2)

    duration = perf_counter() - start_time
    print(f"Complete in {round(duration, 2)}s")


if __name__ == '__main__':
    profile_high_score(sys.argv[1], int(sys.argv[2]))
