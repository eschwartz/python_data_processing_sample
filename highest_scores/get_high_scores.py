import json
from highest_scores.exceptions.InvalidDataException import InvalidDataException

def parse_score_result(score, json_data, line_no):
    """
    From a score (int) and a JSON string,
    generate a dict as {id, score}

    line_no is used for error messages
    """
    try:
        data = json.loads(json_data)
        id = data['id']
    except json.JSONDecodeError:
        raise InvalidDataException(line_no + 1, json_data)
    
    return { 'id': id, 'score': score }

def parse_line(line, line_no):
    """
    From a line of data
    return the score (int) and the json data (string)
    """
    try:
        # Split at the first ": "
        # to get score and JSON string
        score, json_data = line.split(': ', 1)
        score = int(score)
    except:
        raise InvalidDataException(line_no + 1, line)  # exits
    
    return score, json_data

def update_top_scores(
    top_scores, 
    score, 
    json_data, 
    max_results,
    line_no
):
    """
    Given a score and it's json data string,
    check if the score belongs in the top N scores,
    and update top_scores accordingly.

    This function mutates top_scores

    top_scores is assumed to be sorted, and will remain so.
    """

    # Loop through existing top_scores,
    # and add the new score if it belongs
    for ti, t_score in enumerate(top_scores):
        if score > t_score['score']:

            # Add the top score to the list
            # Note: we wait to parse JSON until here, to save some cycles
            score_result = parse_score_result(score, json_data, line_no)
            top_scores.insert(ti, score_result)
            found_top = True
            
            # Limit scores to max_results
            if (len(top_scores) > max_results):
                top_scores.pop()

            # We found a top score, and added it
            # so we're all done here
            return
    
    # This score isn't higher than any existing scores
    # But if room for more, add it to the end
    if len(top_scores) < max_results:
        score_result = parse_score_result(score, json_data, line_no)
        top_scores.append(score_result)

def get_high_scores(data, max_results):
    """
    Data is iterable of raw lines from a data file
    Generate a list of dicts, as {id, score}
    for the top N scores
    """
    # Sorted list of scores, as {id, score}
    top_scores = []

    # Read file line by line
    # Only one line is stored in memory at a time
    for line_no, line in enumerate(data):
        # Skip empty lines
        if len(line.strip()) == 0:
            continue

        # Parse the line into a score and json string
        score, json_data = parse_line(line, line_no)
        

        # Update top_scores
        # with this candidate score
        update_top_scores(
            top_scores,
            score,
            json_data,
            max_results,
            line_no
        ) 
    
    return top_scores