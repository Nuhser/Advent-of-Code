import aoc_util as aoc
import argparse
import importlib
import os
import sys
import time


def parse_args():
    # create parser and parse console arguments
    parser = argparse.ArgumentParser(
        prog = "python3 run.py",
        description = "",
        epilog = "If you have problems or questions, contact me at mail@nuhser.com."
    )
    subparsers = parser.add_subparsers(
        help="subcommands for running solution/tests, visualizing and creating a new blank day",
        dest="subcommand"
    )

    parser.add_argument(
        "year",
        type=int,
        metavar="YEAR",
        help="year to use"
    )
    parser.add_argument(
        "day",
        type=int,
        metavar="DAY",
        help="day to use"
    )
    parser.add_argument(
        "--params",
        metavar="PARAM",
        dest="params",
        nargs="+",
        help="additional parameter that may be used by some solutions"
    )
    parser.add_argument(
        "--time",
        action="store_true",
        dest="track_time",
        help="track the time it takes to parse the input and compute the solutions/visualization"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        dest="verbose",
        help="show more logs while running"
    )

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument(
        "-t", "--test",
        type=int,
        dest="test_number",
        const=-1,
        nargs="?",
        metavar="TEST_NUMBER",
        help="run is a test and should use the test input and solution (add a number if you have multiple test files)"
    )
    run_parser.add_argument(
        "-p", "--part",
        type=int,
        dest="part",
        choices=[0, 1, 2],
        help="which part of the task should be executed (default: both), use 0 to test only the parser"
    )

    visualization_parser = subparsers.add_parser("visualize")

    new_day_parser = subparsers.add_parser("new")
    new_day_parser.add_argument(
        "name",
        metavar="TASK_NAME",
        help="name of this day's chapter"
    )

    return parser.parse_args()


def create_new_day() -> None:
    print(f"Creating new blank day for {args.day:02d}.12.{args.year} '{args.name}'...")

    if not os.path.isdir(f"./{args.year}"):
        print(f"{aoc.ANSI_COLOR["red"]}ERROR: There isn't a directory for the year {args.year} yet. Please create one including a file named {aoc.ANSI_ITALIC}README.md{aoc.ANSI_NOT_ITALIC}.{aoc.ANSI_RESET}")
        return
    
    if not os.path.isfile(f"./{args.year}/README.md"):
        print(f"{aoc.ANSI_COLOR["red"]}ERROR: There isn't a {aoc.ANSI_ITALIC}README.md{aoc.ANSI_NOT_ITALIC} for the year {args.year} yet. Please create the file.{aoc.ANSI_RESET}")
        return
    
    if os.path.isfile(f"./{args.year}/day{args.day:02d}.py"):
        print(f"{aoc.ANSI_COLOR["red"]}ERROR: A solution file already exists for day {args.day} of year {args.year}.{aoc.ANSI_RESET}")
        return
    
    if os.path.isfile(f"./{args.year}/input{args.day:02d}.txt"):
        print(f"{aoc.ANSI_COLOR["red"]}ERROR: A input file already exists for day {args.day} of year {args.year}.{aoc.ANSI_RESET}")
        return
    
    if os.path.isfile(f"./{args.year}/test{args.day:02d}.txt") or os.path.isfile(f"./{args.year}/test{args.day:02d}-1.txt") or os.path.isfile(f"./{args.year}/test{args.day:02d}-2.txt"):
        print(f"{aoc.ANSI_COLOR["red"]}ERROR: One or more test file(s) already exists for day {args.day} of year {args.year}.{aoc.ANSI_RESET}")
        return
    
    with open(f"./{args.year}/README.md", "a") as readme_file:
        readme_file.write(
            f"{args.day}. [{args.name}](https://github.com/Nuhser/Advent-of-Code/blob/master/{args.year}/day{args.day:02d}.py) (*[original task](https://adventofcode.com/{args.year}/day/{args.day})*)\n"
        )
    
    with open(f"./{args.year}/day{args.day:02d}.py", "w") as solution_file:
        solution_file.write(
"""import aoc_util as aoc

from typing import override


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        pass
        
    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        raise NotImplementedError(f"Part 1 of the solution for day {self.day} of year {self.year} isn't implemented yet!")

    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        raise NotImplementedError(f"Part 2 of the solution for day {self.day} of year {self.year} isn't implemented yet!")
"""
        )

    with open(f"./{args.year}/input{args.day:02d}.txt", "w") as input_file:
        input_file.write("")

    with open(f"./{args.year}/test{args.day:02d}.txt", "w") as test_file:
        test_file.write(
"""#!part1:?
#!part2:?

"""
        )


def parse_input() -> tuple:
    parse_time = 0

    if args.track_time:
        parse_time = time.time()

    # create solution object for given day and year
    try:
        solution = importlib.import_module(f"{args.year}.day{args.day:02d}").Solution(
            args.year,
            args.day,
            puzzle_input,
            *args.params if args.params != None else [],
            is_test = run_is_test,
            verbose = args.verbose
        )
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f"There is no solution module for day {args.day} of year {args.year}! Create a module named '{args.year}/day{args.day:02d}.py'")

    if args.track_time:
        parse_time = time.time() - parse_time
        print(aoc.ANSI_INVERTED + f"Parsing took {aoc.ANSI_ITALIC}{parse_time:.5f} seconds{aoc.ANSI_NOT_ITALIC} to complete" + aoc.ANSI_RESET)

    return solution, parse_time


def run() -> float:
    part1_time = 0
    part2_time = 0

    # run part 1
    if (args.part == None) or (args.part == 1):
        print("\nPart 1:")

        if args.track_time:
            part1_time = time.time()

        try:
            solution_string, raw_solution = solution.part1()
        except (NotImplementedError, RuntimeError) as error:
            print(aoc.ANSI_COLOR["red"] + f"ERROR: {error}" + aoc.ANSI_RESET)
        else:
            print(aoc.ANSI_COLOR["blue"] + solution_string + aoc.ANSI_RESET)

            # check if solutions equals the expected test result
            if run_is_test:
                assert expected_results != None

                if expected_results["part1"] == None:
                    print(aoc.ANSI_COLOR["yellow"] + "Solution not testable." + aoc.ANSI_RESET)
                elif expected_results["part1"] == str(raw_solution):
                    print(aoc.ANSI_COLOR["green"] + "This solution is correct!" + aoc.ANSI_RESET)
                else:
                    print(aoc.ANSI_COLOR["red"] + "This solution is incorrect! Expected solution: " + aoc.ANSI_UNDERLINE + expected_results["part1"] + aoc.ANSI_RESET)

        if args.track_time:
            part1_time = time.time() - part1_time
            print(aoc.ANSI_INVERTED + f"Part 1 took {aoc.ANSI_ITALIC}{part1_time:.5f} seconds{aoc.ANSI_NOT_ITALIC} to complete" + aoc.ANSI_RESET)

    # run part 2
    if (args.part == None) or (args.part == 2):
        print("\nPart 2:")

        if args.track_time:
            part2_time = time.time()

        try:
            solution_string, raw_solution = solution.part2()
        except (NotImplementedError, RuntimeError) as error:
            print(aoc.ANSI_COLOR["red"] + f"ERROR: {error}" + aoc.ANSI_RESET)
        else:
            print(aoc.ANSI_COLOR["blue"] + solution_string + aoc.ANSI_RESET)

            # check if solutions equals the expected test result
            if run_is_test:
                assert expected_results != None

                if expected_results["part2"] == None:
                    print(aoc.ANSI_COLOR["yellow"] + "Solution not testable." + aoc.ANSI_RESET)
                elif expected_results["part2"] == str(raw_solution):
                    print(aoc.ANSI_COLOR["green"] + "This solution is correct!" + aoc.ANSI_RESET)
                else:
                    print(aoc.ANSI_COLOR["red"] + "This solution is incorrect! Expected solution: " + aoc.ANSI_UNDERLINE + expected_results["part2"] + aoc.ANSI_RESET)

        if args.track_time:
            part2_time = time.time() - part2_time
            print(aoc.ANSI_INVERTED + f"Part 2 took {aoc.ANSI_ITALIC}{part2_time:.5f} seconds{aoc.ANSI_NOT_ITALIC} to complete" + aoc.ANSI_RESET)

    return part1_time + part2_time


def visualize() -> float:
    visualization_time = 0

    if args.track_time:
        visualization_time = time.time()

    solution.visualize()
    print("\nVisualization complete")

    if args.track_time:
        visualization_time = time.time() - visualization_time
        print(aoc.ANSI_INVERTED + f"Visualization took {aoc.ANSI_ITALIC}{visualization_time:.5f} seconds{aoc.ANSI_NOT_ITALIC} to complete" + aoc.ANSI_RESET)

    return visualization_time


if __name__ == "__main__":
    args = parse_args()

    # check if run is test
    run_is_test = (args.subcommand == "run") and (args.test_number != None)

    # check which subparser is used
    match args.subcommand:
        case "run":
            print(f"{"Testing" if run_is_test else "Executing"} year {args.year} day {args.day}...")
        case "visualize":
            print("Starting visualization...")
        case "new":
            create_new_day()
            print()
            sys.exit()

    # get puzzle/test input
    try:
        puzzle_input, expected_results = aoc.get_puzzle_input(args.year, args.day) if not run_is_test else aoc.get_test_input(args.year, args.day, args.test_number)
    except FileNotFoundError:
        if run_is_test:
            raise FileNotFoundError(f"There is no test input for day {args.day} of year {args.year}! Create a text file named '{args.year}/test{args.day:02d}{f"-{args.test_number}" if (args.test_number > -1) else ""}.txt'")
        else:
            raise FileNotFoundError(f"There is no puzzle input for day {args.day} of year {args.year}! Create a text file named '{args.year}/input{args.day:02d}.txt'")

    # check if the correct test solutions are provided
    if run_is_test:
        if expected_results == None:
            raise AttributeError("No expected results found in the test file ({args.year}/test{args.day:02d}.txt)! Make sure that the correct number of expected results is given at the start of the file (e.g.: #!part1:<RESULT>).")
        elif (args.part == None) and (("part1" not in expected_results) or ("part2" not in expected_results)):
            raise AttributeError("Two expected test results are needed when testing both parts of the solution! Make sure that the correct number of expected results is given at the start of the file (e.g.: #!part1:<RESULT>).")
        elif (args.part == 1) and ("part1" not in expected_results):
            raise AttributeError("No expected test result found in your test file for part 1 of the solution! Make sure that the correct number of expected results is given at the start of the file (e.g.: #!part1:<RESULT>).")
        elif (args.part == 2) and ("part2" not in expected_results):
            raise AttributeError("No expected test result found in your test file for part 2 of the solution! Make sure that the correct number of expected results is given at the start of the file (e.g.: #!part2:<RESULT>).")

    parse_time = 0
    run_time = 0
    visualization_time = 0

    solution, parse_time = parse_input()

    match args.subcommand:
        # run visualization
        case "visualize":
            visualization_time = visualize()

        # run solutions and tests
        case "run":
            run_time = run()

    if args.track_time:
        print(f"\n{aoc.ANSI_INVERTED}Total compute time: {aoc.ANSI_ITALIC}{(parse_time + run_time + visualization_time):.5f} seconds" + aoc.ANSI_RESET)

    print()