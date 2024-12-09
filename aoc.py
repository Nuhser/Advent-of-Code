import argparse
import glob
import importlib
import os
import shutil
import time
from typing import Type

from prettytable import PrettyTable

import aoc_util as aoc
from utility.terminal_formatting import Color, Formatting


def parse_args():
    # create parser and parse console arguments
    parser = argparse.ArgumentParser(
        prog="python aoc.py",
        description="This tool can be used to create new Advent of Code days from templates. You can run and test your solutions and even visualize them.",
        epilog="If you have problems or questions, contact me at mail@nuhser.com.",
    )
    subparsers = parser.add_subparsers(
        help="subcommands for running solution/tests, visualizing and creating a new blank day",
        dest="subcommand",
    )

    parser.add_argument("year", type=int, metavar="YEAR", help="year to use")
    parser.add_argument("day", type=int, metavar="DAY", help="day to use")
    parser.add_argument(
        "--param",
        action="append",
        dest="params",
        metavar="PARAM",
        help="additional parameter that may be used by some solutions",
    )
    parser.add_argument(
        "--time",
        action="store_true",
        dest="track_time",
        help="track the time it takes to parse the input and compute the solutions/visualization",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        dest="verbose",
        help="show more logs while running",
    )

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument(
        "-t",
        "--test",
        action="append",
        type=int,
        nargs="?",
        dest="test_numbers",
        metavar="TEST_NUMBER",
        help="run is a test and should use the test input and solution (add a number if you have multiple test files); you can use this argument multiple times per execution",
    )
    run_parser.add_argument(
        "-p",
        "--part",
        type=int,
        choices=[0, 1, 2],
        dest="part",
        help="which part of the task should be executed (default: both), use 0 to test only the parser",
    )

    visualization_parser = subparsers.add_parser("visualize")

    new_day_parser = subparsers.add_parser("new")
    new_day_parser.add_argument(
        "name", metavar="TASK_NAME", help="name of this day's chapter"
    )

    return parser.parse_args()


def create_new_day(args) -> None:
    print(f"Creating new blank day for {args.day:02d}.12.{args.year} '{args.name}'...")

    if not os.path.isdir(f"./{args.year}"):
        os.makedirs(f"./{args.year}")
        with open(f"./{args.year}/__init__.py", "w") as init_file:
            pass

    if not os.path.isfile(f"./{args.year}/README.md"):
        with open("./templates/README.md", "r") as readme_template_file:
            readme_template = readme_template_file.read()

        with open(f"./{args.year}/README.md", "w") as readme_file:
            readme_file.write(
                replace_placeholders(readme_template, args.year, args.day)
            )

    if os.path.isfile(f"./{args.year}/day{args.day:02d}.py"):
        print(
            f"{Color.RED}ERROR: A solution file already exists for day {args.day} of year {args.year}.{Formatting.RESET}"
        )
        return

    if os.path.isfile(f"./{args.year}/input{args.day:02d}.txt"):
        print(
            f"{Color.RED}ERROR: A input file already exists for day {args.day} of year {args.year}.{Formatting.RESET}"
        )
        return

    if (
        os.path.isfile(f"./{args.year}/test{args.day:02d}.txt")
        or os.path.isfile(f"./{args.year}/test{args.day:02d}-1.txt")
        or os.path.isfile(f"./{args.year}/test{args.day:02d}-2.txt")
    ):
        print(
            f"{Color.RED}ERROR: One or more test file(s) already exists for day {args.day} of year {args.year}.{Formatting.RESET}"
        )
        return

    with open(f"./{args.year}/README.md", "a") as readme_file:
        readme_file.write(
            f"{args.day}. [{args.name}](https://github.com/Nuhser/Advent-of-Code/blob/master/{args.year}/day{args.day:02d}.py) (*[original task](https://adventofcode.com/{args.year}/day/{args.day})*)\n"
        )

    shutil.copy("templates/day.py", f"./{args.year}/day{args.day:02d}.py")

    shutil.copy("templates/input.txt", f"./{args.year}/input{args.day:02d}.txt")

    shutil.copy("templates/test.txt", f"./{args.year}/test{args.day:02d}.txt")

    print(f"{Color.GREEN}Day creation successful!{Color.DEFAULT}")


def replace_placeholders(original_string: str, year: int, day: int) -> str:
    return original_string.replace("$$YEAR", str(year)).replace("$$DAY", str(day))


def parse_input(
    args, puzzle_input: list[str], run_is_test: bool
) -> tuple[aoc.AbstractSolution, float]:
    parse_time: float = 0

    if args.track_time:
        parse_time = time.time()

    # create solution object for given day and year
    try:
        solution: aoc.AbstractSolution = importlib.import_module(
            f"{args.year}.day{args.day:02d}"
        ).Solution(
            args.year,
            args.day,
            puzzle_input,
            args.params if args.params != None else [],
            is_test=run_is_test,
            verbose=args.verbose,
        )
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            f"There is no solution module for day {args.day} of year {args.year}! Create a module named '{args.year}/day{args.day:02d}.py'"
        )

    if args.track_time:
        parse_time = time.time() - parse_time
        print(
            Formatting.INVERTED
            + f"Parsing took {Formatting.ITALIC}{parse_time:.5f} seconds{Formatting.NOT_ITALIC} to complete"
            + Formatting.RESET
        )

    return solution, parse_time


def validate_expected_solutions(
    args, expected_results: dict[str, (str | None)]
) -> None:
    if expected_results == None:
        raise AttributeError(
            f"No expected results found in the test file ({args.year}/test{args.day:02d}.txt)! Make sure that the correct number of expected results is given at the start of the file (e.g.: #!part1:<RESULT>)."
        )
    elif (args.part == 1) and ("part1" not in expected_results):
        raise AttributeError(
            "No expected test result found in your test file for part 1 of the solution! Make sure that the correct number of expected results is given at the start of the file (e.g.: #!part1:<RESULT>)."
        )
    elif (args.part == 2) and ("part2" not in expected_results):
        raise AttributeError(
            "No expected test result found in your test file for part 2 of the solution! Make sure that the correct number of expected results is given at the start of the file (e.g.: #!part2:<RESULT>)."
        )
    elif args.part == None:
        if "part1" not in expected_results:
            print(
                f"\n{Color.YELLOW}Couldn't find an expected solution for test part 1. Therefore, only running part 2.{Color.DEFAULT}"
            )
            args.part = 2
        elif "part2" not in expected_results:
            print(
                f"\n{Color.YELLOW}Couldn't find an expected solution for test part 2. Therefore, only running part 1.{Color.DEFAULT}"
            )
            args.part = 1


def run(args) -> None:
    puzzle_input, expected_results = aoc.get_puzzle_input(args.year, args.day)
    solution, parse_time = parse_input(args, puzzle_input, False)
    run_time, _, _ = solve(args, solution, expected_results, False)

    if args.track_time:
        print(
            f"\n{Formatting.INVERTED}Total compute time: {Formatting.ITALIC}{(parse_time + run_time):.5f} seconds"
            + Formatting.RESET
        )


def test(args) -> None:
    original_part: int | None = args.part

    if args.test_numbers == [None]:
        test_files = glob.glob(f"./{args.year}/test{args.day:02d}-*.txt")

        if len(test_files) > 0:
            args.test_numbers = []
            for test_file in test_files:
                args.test_numbers.append(test_file.split("-")[-1].removesuffix(".txt"))

    test_results: list[list[str | int | float | None]] = []

    for test_number in args.test_numbers:
        if (len(args.test_numbers) > 1) and (test_number != None):
            print(
                f"\n{Color.YELLOW}Running test case #{test_number}...{Color.DEFAULT}",
                end="",
            )

        args.part = original_part
        puzzle_input, expected_results = aoc.get_test_input(
            args.year, args.day, test_number
        )
        validate_expected_solutions(
            args, expected_results
        )  # check if the correct test solutions are provided
        solution, parse_time = parse_input(args, puzzle_input, True)
        run_time, part1_solution, part2_solution = solve(
            args, solution, expected_results, True
        )

        if args.track_time:
            print(
                f"\n{Formatting.INVERTED}Total compute time: {Formatting.ITALIC}{(parse_time + run_time):.5f} seconds"
                + Formatting.RESET
            )

        if len(args.test_numbers) > 1:
            test_results.append(
                [test_number, part1_solution, part2_solution]
                + ([parse_time + run_time] if args.track_time else [])
            )

    if len(args.test_numbers) > 1:
        table = PrettyTable()
        table.field_names = ["Test #", "Part 1", "Part 2"] + (
            ["Compute Time"] if args.track_time else []
        )
        table.align = "r"
        table.float_format = "0.5"
        table.add_rows(test_results)

        print(f"\n{Formatting.UNDERLINE}Summary:{Formatting.NOT_UNDERLINE}\n{table}")


def solve(
    args,
    solution: aoc.AbstractSolution,
    expected_results: dict[str, (str | None)] | None,
    run_is_test: bool,
) -> tuple[float, (int | float | str | None), (int | float | str | None)]:
    part1_time, part2_time = 0, 0
    part1_solution, part2_solution = None, None

    # run part 1
    if (args.part == None) or (args.part == 1):
        print("\nPart 1:")

        if args.track_time:
            part1_time = time.time()

        try:
            solution_string, part1_solution = solution.part1()
        except (NotImplementedError, RuntimeError) as error:
            print(Color.RED + f"ERROR: {error}" + Formatting.RESET)
        else:
            print(Color.BLUE + solution_string + Formatting.RESET)

            # check if solutions equals the expected test result
            if run_is_test:
                assert expected_results != None

                if expected_results["part1"] == None:
                    print(
                        Color.YELLOW
                        + "Not testable. Expected solution is unknown."
                        + Formatting.RESET
                    )
                elif expected_results["part1"] == str(part1_solution):
                    print(Color.GREEN + "This solution is correct!" + Formatting.RESET)
                else:
                    print(
                        Color.RED
                        + "This solution is incorrect! Expected solution: "
                        + Formatting.UNDERLINE
                        + expected_results["part1"]
                        + Formatting.RESET
                    )

        if args.track_time:
            part1_time = time.time() - part1_time
            print(
                Formatting.INVERTED
                + f"Part 1 took {Formatting.ITALIC}{part1_time:.5f} seconds{Formatting.NOT_ITALIC} to complete"
                + Formatting.RESET
            )

    # run part 2
    if (args.part == None) or (args.part == 2):
        print("\nPart 2:")

        if args.track_time:
            part2_time = time.time()

        try:
            solution_string, part2_solution = solution.part2()
        except (NotImplementedError, RuntimeError) as error:
            print(Color.RED + f"ERROR: {error}" + Formatting.RESET)
        else:
            print(Color.BLUE + solution_string + Formatting.RESET)

            # check if solutions equals the expected test result
            if run_is_test:
                assert expected_results != None

                if expected_results["part2"] == None:
                    print(
                        Color.YELLOW
                        + "Not testable. Expected solution is unknown."
                        + Formatting.RESET
                    )
                elif expected_results["part2"] == str(part2_solution):
                    print(Color.GREEN + "This solution is correct!" + Formatting.RESET)
                else:
                    print(
                        Color.RED
                        + "This solution is incorrect! Expected solution: "
                        + Formatting.UNDERLINE
                        + expected_results["part2"]
                        + Formatting.RESET
                    )

        if args.track_time:
            part2_time = time.time() - part2_time
            print(
                Formatting.INVERTED
                + f"Part 2 took {Formatting.ITALIC}{part2_time:.5f} seconds{Formatting.NOT_ITALIC} to complete"
                + Formatting.RESET
            )

    return part1_time + part2_time, part1_solution, part2_solution


def visualize(args) -> None:
    print("Starting visualization...")

    visualization_time = 0
    puzzle_input, _ = aoc.get_puzzle_input(args.year, args.day)
    solution, parse_time = parse_input(args, puzzle_input, False)

    if args.track_time:
        visualization_time = time.time()

    solution.visualize()
    print("\nVisualization complete")

    if args.track_time:
        visualization_time = time.time() - visualization_time
        print(
            Formatting.INVERTED
            + f"Visualization took {Formatting.ITALIC}{visualization_time:.5f} seconds{Formatting.NOT_ITALIC} to complete"
            + Formatting.RESET
        )
        print(
            f"\n{Formatting.INVERTED}Total compute time: {Formatting.ITALIC}{(parse_time + visualization_time):.5f} seconds"
            + Formatting.RESET
        )


if __name__ == "__main__":
    args = parse_args()

    match args.subcommand:
        case "new":
            create_new_day(args)

        case "visualize":
            visualize(args)

        case "run":
            # check if run is test
            run_is_test = (args.subcommand == "run") and (args.test_numbers != None)

            print(
                f"{Formatting.UNDERLINE}{"Testing" if run_is_test else "Executing"} year {args.year} day {args.day}...{Formatting.NOT_UNDERLINE}"
            )

            # get puzzle/test input
            if run_is_test:
                test(args)
            else:
                run(args)

    print()
