import json
from highest_scores.exceptions.InvalidDataException import InvalidDataException

def parse_score(score, json_data, line_no):
    try:
        data = json.loads(json_data)
        id = data['id']
    except json.JSONDecodeError:
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