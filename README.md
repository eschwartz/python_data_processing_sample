# "Highest Scores" Code Challenge

_Submission by Edan Schwartz, Dec 2022_

> Take a data file containing scored samples and produce the N highest scores and sample ids, ordered by descending score.

This solution prioritizes memory efficiency and dev time efficiency. The script can process a file with **1,000,000 records in 23s using < 200kb of memory**. See [Profiler](#profiler) for details.

## Usage

To run:

```
python highest.py FILE MAX_RESULTS
```

eg:

```
python highest.py ./example_input_data_1.data 5
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


### Requirements

- Python 3.10.8

This script has not been tested with other versions of Pythons. Consider [running in a docker container](#using-docker)


### Generating data fixtures

Example data may be generated using the `gen.js` script:

```
npm install chance 
./gen.js
```

### Tests

This submission includes partial test coverage of the core logic. To run test:

```
python -m unittest
```

### Profiler

This submission includes code to profile memory usage. To run the profiler:

```
pip3 install -U memory_profiler
# Create profile for processing example_input_data_3.data, with 5 max results
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

Processing 1,000,000 records took ~23s on my MacBook Pro. I chose to focus on memory efficiency, as hinted in the instructions. 

Time complexity is something like `O(n * x^2)` where x is the value `MAX_RESULTS`. Worst case, this is `O(n^3)`. But if we assume that `MAX_RESULTS` is generally small (say, `3`), we may end up with something closer to `O(9n)`.

As a case in point, increasing the max results from 5 to 100 results [increases run time from 23s to 160s](./profile-1M-100.txt), for a dataset with 1M records.


### Future Considerations

With more time I would prioritize:

- More comprehensive test coverage
- Time performance improvements