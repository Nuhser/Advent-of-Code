# Advent of Code

This repository is a collection of my solutions for the **Advent of Code** throughout the years.

There is one folder per year. Each folder contains my puzzle inputs and solutions. The solutions make use of the code from [aoc_util.py](https://github.com/Nuhser/Advent-of-Code/blob/master/aoc_util.py). This a utility script I use for parsing the puzzle inputs. It also contains an class which I use as the parent class of my daily solutions.

The solutions consist of a class which uses the method `parse` for parsing the puzzle input for both parts of the challenge and the methods `part1` and `part2` which contain the solutions for the parts and return them as strings. Some classes may have an implementation of the method `visualize`. This method can be used to visualize the task. There can be other methods if needed. Those methods would then be called from within the other three methods.

You can run the solutions by using the `aoc.py` script in this directory it takes a few positional and optional parameters as input. The base call would be something like:

```
python aoc.py run 2022 6
```

This would execute both parts of the solution of day 6 from 2022. If you would only like to execute the second part, you could use:

```
python aoc.py run -p 2 2022 6
```

To use the test input instead of the real one (if a test input exists) use something like (`--test` also works):

```
python aoc.py run -t 2020 12
```

To test your solution add the expected results at the top of the test file. To add a expected solution for part 1 add the following line at the beginning:

```
#!part1:<RESULT>
```

Replace `<RESULT>`with your expected result. You can do the same for part 2. The order shouldn't matter. You can have multiple test inputs per day by naming them like `test03-1.txt`, `test03-2.txt`, ... To use a specific test file add the number of that file after the `-t`/`--test` parameter of the command.

To start the visualization use:

```
python aoc.py visualize
```

You can add `--time` to the end of every run to get the time it took to complete the parsing, solving or visualization.

Use `-h` or `--help` either directly or with `run` and `visualize` to see the full list of possible console parameters and their descriptions.

----

> *Advent of Code is designed by [Eric Wastl](https://twitter.com/ericwastl). I have no associations with him or his team. I'm only participating in his challenges and do not take credit for any of the puzzles or the explanations used in the notebooks.*
>
> *For more information visit his [website](https://adventofcode.com/2021/about).*
