# "Highest Scores" Code Challenge

_Submission by Edan Schwartz, Dec 2022_

> Take a data file containing scored samples and produce the N highest scores and sample ids, ordered by descending score.

This solution prioritizes memory efficiency and dev time efficiency. The script can process a file with **480,000 records using < 200kb of memory**. See [Profiler](#profiler) for details.

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
# Requires a data file at example_input_data_3.data
python3 -m memory_profiler ./test/profile_get_high_scores.py
```






## Performance

See example memory profiler results at [profile-480k.txt](./profile-480k.txt). You'll see here that processing the file uses ~190kb of memory. 

```
12   16.012 MiB    0.000 MiB           2       with open(file_path) as f:
13                                                 # Get the top N scores
14   16.008 MiB    0.184 MiB           1           results = get_high_scores(f, max_results)
15                                         
16                                                 # Output results as JSON
17   16.012 MiB    0.004 MiB           1           json.dumps(results, indent=2)
```

Processing a file with 480,000 records took ~10s on my MacBook Pro. I chose to focus on memory efficiency, as hinted in the instructions. 

Time complexity is something like `O(n * x^2)` where x is the value `MAX_RESULTS`. Worst case, this is `O(n^3)`. But if we assume that `MAX_RESULTS` is generally small (say, `3`), we may end up with something closer to `O(9n)`.


### Future Considerations

- test coverage
- time performance (vs memory & dev tim)