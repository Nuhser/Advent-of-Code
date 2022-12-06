# Advent of Code

This repository is a collection of my solutions for the **Advent of Code** throughout the years.

There is one folder per year. Each folder contains my puzzle inputs and solutions. The solutions make use of the code from [aoc_util.py](https://github.com/Nuhser/Advent-of-Code/blob/master/aoc_util.py). This a utility script I use for parsing the puzzle inputs. It also contains an class which I use as the parent class of my daily solutions.

The solutions consist of a class which uses the method `parse` for parsing the puzzle input for both parts of the challenge and the methods `part1` and `part2` which contain the solutions for the parts and return them as strings. There can be other methods if needed. Those methods would then be called from within the other three methods.

You can run the solutions by using the `run.py` script in this directory it takes a few positional and optional parameters as input. The base call would be something like:

```
python3 run.py 2022 6
```

This would execute both parts of the solution of day 6 from 2022. If you would only like to execute the second part, you could use:

```
python3 run.py 2022 6 -p 2
```

To use the test input instead of the real one (if a test input exists) use something like (`--test` also works):

```
python3 run.py 2020 12 -t
```

Use `-h` or `--help` to see the full list of possible console parameters and their descriptions.

----

> *Advent of Code is designed by [Eric Wastl](https://twitter.com/ericwastl). I have no associations with him or his team. I'm only participating in his challenges and do not take credit for any of the puzzles or the explanations used in the notebooks.*
>
> *For more information visit his [website](https://adventofcode.com/2021/about).*