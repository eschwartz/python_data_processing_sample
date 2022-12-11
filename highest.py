import sys
import json

from highest_scores.exceptions.DataProcessingException import DataProcessingException
from highest_scores.get_high_scores import get_high_scores
from highest_scores.parse_cli_args import parse_cli_args


if __name__ == '__main__':
    # Get the data file path and max results from the CLI args
    file_path, max_results = parse_cli_args(sys.argv)

    # Open the data file
    with open(file_path) as f:
        try:
            # Get the top N scores
            results = get_high_scores(f, max_results)

            # Output results as JSON
            print(json.dumps(results, indent=2))
        except DataProcessingException as err:
            # Handle data processing errors and exit
            print(err.message, file=sys.stderr)

            # Exceptions define their own exit code
            # according to the type of failure
            sys.exit(err.exit_code)
        except Exception as err:
            # Handle other errors (eg. script failure)
            print(f"Process failed: {err}", file=sys.stderr)
            sys.exit(1)
