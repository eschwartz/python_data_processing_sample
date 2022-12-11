import sys
import json

from highest_scores.exceptions.DataProcessingException import DataProcessingException
from highest_scores.get_high_scores import get_high_scores
from highest_scores.parse_cli_args import parse_cli_args


if __name__ == '__main__':
    file_path, max_results = parse_cli_args(sys.argv)

    with open(file_path) as f:
        try:
            results = get_high_scores(f, max_results)

            print(json.dumps(results, indent=2))
        except DataProcessingException as err:
            print(err.message, file=sys.stderr)
            sys.exit(err.exit_code)
        except Exception as err:
            print(f"Process failed: {err}", file=sys.stderr)
            # error code not specified in requirements, 
            # but it may be useful if this is different than the others
            sys.exit(3)



# TODO
# [x] Test the solution
# [x] Add cli arg support
# - Organize and comment code
# - Test memory usage & performance
# - format nice (pip8?)