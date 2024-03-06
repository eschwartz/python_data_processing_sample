# Python Data Processing Code Sample

By Edan Schwartz, 2024

Given a data file containing scored records, this program outputs the N highest record IDs ordered by descending score as JSON

The input data file is a series of key-value pairs (one per line) with the format
```
<score> : <record>
```


In valid input files, the ``score`` is an integer and the ``record`` is a JSON dictionary.  The ``record`` can be any kind of well-formed JSON doc (with the exception of no line breaks).  The only constraint on the ``record`` is that a valid ``record`` will contain an ``id`` key that uniquely defines that record.  All scores and ids are unique.  A ``record`` that is not valid JSON or that does not contain an ``id`` field should be considered invalid and handled as described under **Exit Conditions**

An example input data file is:
```
8795136: {"id":"d2e257c282b54347ac14b2d8","x":"foo","payload":"someamountofdata"}
5317020: {"id":"619236365add4a0ca6e501fc","type":"purple","payload":"smalldata"}
.
.
.
2766123: {"id":"da9f77e6a0f076b000a6c0e0","payload":"reallyquitealotofdata"}
```

## Usage

**Requires Python 3.10.8**

This script has not been tested with other versions of Python. Consider [running in a docker container](#using-docker).

To run:

```
python highest.py FILE MAX_RESULTS
```

eg:

```
python highest.py ./example_input_data_1.data 5
```

For full usage instructions, run:

```
python highest.py -h
```


### Using Docker

To ensure a compatible version of python, consider running with docker:

```
docker run \
    --rm \
    -it \
    -w=/opt/app \
    -v $(pwd):/opt/app \
    python:3.10.8 \
    python /opt/app/highest.py ./example_input_data_1.data 5
```



### Generating data fixtures

Example data may be generated using the `gen.js` script:

```
npm install chance 
./gen.js
```

### Tests

This repo includes partial test coverage of the core logic. To run tests:

```
python -m unittest
```

### Profiler

This repo includes code to profile memory usage. To run the profiler:

```
pip3 install -U memory_profiler

# Generate a report for processing example_input_data_3.data, 
# with 5 max results
python3 -m memory_profiler ./test/profile_get_high_scores.py example_input_data_3.data 5
```

## Performance

See example memory profiler results at [profile-1M.txt](./profile-1M.txt). You'll see here that processing a file with 1,000,000 records uses ~120kb of memory, when asking for 5 max results.

```
    11   15.938 MiB    0.000 MiB           1       max_results = 5
    12                                         
    13   16.062 MiB    0.000 MiB           2       with open(file_path) as f:
    14                                                 # Get the top N scores
    15   16.055 MiB    0.117 MiB           1           results = get_high_scores(f, max_results)
    16                                         
    17                                                 # Output results as JSON
    18   16.062 MiB    0.008 MiB           1           json.dumps(results, indent=2)
```

Processing 1,000,000 records took ~23s on my 2020 MacBook Pro. I chose to focus on memory efficiency, as hinted at in the instructions. 


Time complexity could be improved by keeping all scores in memory, eg in a `{ score: id }` dict, and sorting at the end. But this would come at the cost of higher memory usage.


### Future Considerations

With more time I would prioritize:

- More comprehensive test coverage
- Time performance improvements