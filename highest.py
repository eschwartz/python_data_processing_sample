import sys
import json


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

class InvalidDataException(Exception):
    """
    Indicates that some data is invalid, and cannot be parsed
    """
    
    def __init__(self, line_no, message):
        self.message = f"Invalid data at line {line_no}:\n{message}"
        super().__init__(self.message)

class DataFileNotFound(Exception):
    """
    Indicates that the provided data file cannot be found
    """
    pass



def parse_score(score, json_data, line_no):
    try:
        data = json.loads(json_data)
        id = data['id']
    except:
        raise InvalidDataException(line_no, json_data)
    
    return { 'id': id, 'score': score }

def get_high_scores(data, max_records):
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
            raise InvalidDataException(line_no, line)  # exits

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
                
                # Limit scores to max_records
                if (len(top_scores) > max_records):
                    top_scores.pop()

                # Stop searching
                break
        
        # If we didn't already add this score
        # and there room for more, add it to the end
        if found_top is False and len(top_scores) < max_records:
            score_item = parse_score(score, json_data, line_no)
            top_scores.append(score_item)
    
    return top_scores


    



if __name__ == '__main__':
    # TODO get from CLI args
    file_name = "example_input_data_1.data"
    max_records = 5 

    with open(file_name) as f:
        try:
            results = get_high_scores(f, max_records)

            print(json.dumps(results, indent=2))
        except DataFileNotFound as err:
            print(err.message, file=sys.stderr)
            sys.exit(1)
        except InvalidDataException as err:
            print(err.message, file=sys.stderr)
            sys.exit(2)
        except:
            print(f"Process failed: {err.message}", file=sys.stderr)
            # error code not specified in requirements, 
            # but it may be useful if this is different than the others
            sys.exit(3)



# TODO
# - Test the solution
# - Add cli arg support
# - Organize and comment code
# - Test memory usage & performance