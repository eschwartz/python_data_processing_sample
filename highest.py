file_name = "example_input_data_1.data"

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
        Technically O(n2), as there's a nested loop
            but really only if output count == data count
        In practice, should be fast if output count is small
    
    Memory:
        only keeping the top 5, plus the one line being read

"""

with open(file_name) as f:
    # Read file line by line
    # Only one line is stored in memory at a time
    for line in f:
        print(f"line is {line}")
