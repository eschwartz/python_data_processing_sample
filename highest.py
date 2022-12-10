import sys
import json

# TODO get from CLI args
file_name = "example_input_data_1.data"
max_records = 5

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

def handle_invalid_data(line_no, info):
    print(f"Invalid data at line {line_no}:\n{info}", file=sys.stderr)
    sys.exit(2)

# List of dicts, as {id, score}
top_scores = []
def parse_score(score, json_data, line_no):
    try:
        data = json.loads(json_data)
        id = data['id']
    except:
        handle_invalid_data(line_no, json_data)
    
    return { 'id': id, 'score': score }


with open(file_name) as f:
    # Read file line by line
    # Only one line is stored in memory at a time
    for line_no, line in enumerate(f):
        # Skip empty lines
        if len(line.strip()) == 0:
            continue

        try:
            # Split at the first ": "
            # to get score and JSON string
            score, json_data = line.split(': ', 1)
            score = int(score)
        except:
            handle_invalid_data(line_no, line)  # exits

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


print(json.dumps(top_scores, indent=2))


# TODO
# - Test the solution
# - Add cli arg support
# - Organize and comment code
# - Test memory usage & performance