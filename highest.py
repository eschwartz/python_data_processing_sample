import sys
import json
from pathlib import Path


# TODO exit conditions:
# - 2 for invalid input
# - 1 for missing file
# - ignore empty lines

"""
Option A:
    keep a list of [score:line no]
    loop through lines, and parse each as JSON
    sort by score
    take top five items
    re-read their line numbers from the file
        and write into dict, for JSON output

    Performance:
        Two iterating operations: file read, sorting
        https://stackoverflow.com/a/14434514/830030 <- sorted is O(nlogn) 
            O(n + nlogn)?
        Two file reads
        Parsing each JSON line
        
    memory: 
        keeping entire list of scores in memory, could be big

Option B:
    Keep a list of top 5 scores, as { score, id }
    loop through lines, and split into score / JSON string (no parsing)
    check if score is in the top 5, and update list

    Performance
        Technically O(n2)
            but really only if output count == data count
            ~ O(n*x)
            or O(n*x2) (with insert into list?)
        In practice, should be fast if output count is small
    
    Memory:
        only keeping the top 5, plus the one line being read

"""

class DataProcessingException(Exception):
    """
    Base exception for any errors from this
    data processing script.
    """
    def __init__(self, message, exit_code=1):
        self.exit_code = exit_code
        self.message = message
        super().__init__(message)

class InvalidDataException(DataProcessingException):
    """
    Indicates that some data is invalid, and cannot be parsed
    """
    
    def __init__(self, line_no, message):
        message = f"Invalid data at line {line_no}:\n{message}"
        super().__init__(message, exit_code=2)


class DataFileNotFound(DataProcessingException):
    """
    Indicates that the provided data file cannot be found
    """
    def __init__(self, file_path):
        message = f"Data file not found at {file_path}"
        super().__init__(message, exit_code=1)



def parse_score(score, json_data, line_no):
    try:
        data = json.loads(json_data)
        id = data['id']
    except:
        raise InvalidDataException(line_no + 1, json_data)
    
    return { 'id': id, 'score': score }

def get_high_scores(data, max_results):
    # List of dicts, as {id, score}
    top_scores = []

    # Read file line by line
    # Only one line is stored in memory at a time
    for line_no, line in enumerate(data):
        # Skip empty lines
        if len(line.strip()) == 0:
            continue

        try:
            # Split at the first ": "
            # to get score and JSON string
            score, json_data = line.split(': ', 1)
            score = int(score)
        except:
            raise InvalidDataException(line_no + 1, line)  # exits

        # Add first entry, if there are no top scores
        if len(top_scores) == 0:
            score_item = parse_score(score, json_data, line_no)
            top_scores.append(score_item)
            continue

        # Check for a top score
        found_top = False
        for ti, t_score in enumerate(top_scores):
            if score > t_score['score']:

                # Add the top score to the list
                # Note: we wait to parse JSON until here, to save some cycles
                score_item = parse_score(score, json_data, line_no)
                top_scores.insert(ti, score_item)
                found_top = True
                
                # Limit scores to max_results
                if (len(top_scores) > max_results):
                    top_scores.pop()

                # Stop searching
                break
        
        # If we didn't already add this score
        # and there room for more, add it to the end
        if found_top is False and len(top_scores) < max_results:
            score_item = parse_score(score, json_data, line_no)
            top_scores.append(score_item)
    
    return top_scores


    

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

    # Verify file exists
    if Path(file_path).is_file() is False:
        raise DataFileNotFound(file_path)

    return file_path, max_results

if __name__ == '__main__':
    file_path, max_results = parse_cli_args(sys.argv)
    # TODO get from CLI args
    file_path = "example_input_data_1.data"
    max_results = 5 

    with open(file_path) as f:
        try:
            results = get_high_scores(f, max_results)

            print(json.dumps(results, indent=2))
        except DataProcessingException as err:
            print(err.message, file=sys.stderr)
            sys.exit(err.exit_code)
        except:
            print(f"Process failed: {err.message}", file=sys.stderr)
            # error code not specified in requirements, 
            # but it may be useful if this is different than the others
            sys.exit(3)



# TODO
# [x] Test the solution
# - Add cli arg support
# - Organize and comment code
# - Test memory usage & performance
# - format nice (pip8?)