from pathlib import Path

from highest_scores.exceptions.DataFileNotFound import DataFileNotFound

help_text = """
highest.py

Usage: python3 highest.py FILE MAX_RESULTS

Description:
    Takes a data file containing scored samples 
    and produce the N highest scores and sample ids, 
    ordered by descending score.

Arguments:
    FILE            Path to the data file to process [required]
    MAX_RESULTS     Max number of scores to return

Input data file:
    An example input data file is:
    ```
    8795136: {"id":"d2e257c282b54347ac14b2d8","x":"foo","payload":"someamountofdata"}
    5317020: {"id":"619236365add4a0ca6e501fc","type":"purple","payload":"smalldata"}
    ```

Output:
    This script writes valid JSON to stdout, formatted as:

    [
        { "score":16774838, "id":"9ab7247c02044c65936a467016fff6b6" },
        { "score":16763774, "id":"c51a310f80604ef68a4cb2b83bffcb7e" }
    ]
"""

def parse_cli_args(args):
    # First arg is the name of the script
    # Cut this out.
    args = args[1:] 

    # Check for -h or --help
    if args[0] in ['-h', '--help']:
        print(help_text)
        sys.exit(0)

    # Check for invalid number of args
    # (expecting ['file.data', '5'])
    if len(args) != 2:
        print("ERROR: Invalid arguments for highest.py", file=sys.stderr)
        print(help_text, file=sys.stderr)
        sys.exit(1)
    
    # We've verified there are exactly 2 args
    file_path, max_results = args

    # Validate max_results is an int
    try:
        max_results = int(max_results)
    except:
        print(
            "ERROR: Invalid arguments for highest.py: MAX_RESULTS must be an integer", 
            file=sys.stderr
        )
        sys.exit(1)

    # Verify file exists
    if Path(file_path).is_file() is False:
        raise DataFileNotFound(file_path)



    return file_path, max_results