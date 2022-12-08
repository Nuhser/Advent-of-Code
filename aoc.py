import aoc_util as aoc
import argparse
import importlib
import time

if __name__ == "__main__":
    # create parser and parse console arguments
    parser = argparse.ArgumentParser(
        prog = "python3 run.py",
        description = "",
        epilog = "If you have problems or questions, contact me at mail@nuhser.com."
    )
    subparsers = parser.add_subparsers(help="subcommands for running solution/tests or visualizing", dest="subcommand")

    parser.add_argument("year", type=int, metavar="YEAR", help="year to use")
    parser.add_argument("day", type=int, metavar="DAY", help="day to use")
    parser.add_argument("--time", action="store_true", dest="track_time", help="track the time it takes to parse the input and compute the solutions/visualization")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="show more logs while running")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("-t", "--test", action="store_true", dest="run_is_test", help="run is a test and should use the test input and solutions")
    run_parser.add_argument("-p", "--part", type=int, dest="part", choices=[0, 1, 2], help="which part of the task should be executed (default: both), use 0 to test only the parser")

    visualization_parser = subparsers.add_parser("visualize")

    args = parser.parse_args()

    parse_time = 0
    part1_time = 0
    part2_time = 0
    visualization_time = 0

    # check if run is test
    run_is_test = (args.subcommand == "run") and args.run_is_test

    if (args.subcommand == "run"):
        print(f"{'Testing' if run_is_test else 'Executing'} year {args.year} day {args.day}...")
    else:
        print("Starting visualization...")

    # get puzzle/test input
    try:
        puzzle_input, expected_results = aoc.get_puzzle_input(args.year, args.day) if not run_is_test else aoc.get_test_input(args.year, args.day)
    except FileNotFoundError:
        if run_is_test:
            raise FileNotFoundError(f"There is no test input for day {args.day} of year {args.year}! Create a text file named '{args.year}/test{args.day:02d}.txt'")
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

    # create solution object for given day and year
    if args.track_time:
        parse_time = time.time()

    try:
        solution = importlib.import_module(f"{args.year}.day{args.day:02d}").Solution(args.year, args.day, puzzle_input, args.verbose)
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f"There is no solution module for day {args.day} of year {args.year}! Create a module named '{args.year}/day{args.day:02d}.py'")

    if args.track_time:
        parse_time = time.time() - parse_time
        print(f"\u001b[7mParsing took {parse_time:.5f} seconds to complete\u001b[0m")

    # start visualization and exit program if wanted
    if (args.subcommand == "visualize"):
        if args.track_time:
            visualization_time = time.time()

        solution.visualize()
        print("\nVisualization complete")

        if args.track_time:
            visualization_time = time.time() - visualization_time
            print(f"\u001b[7mVisualization took {visualization_time:.5f} seconds to complete\u001b[0m")

    # else start computation run
    else:
        # run part 1
        if (args.part == None) or (args.part == 1):
            print("\nPart 1:")

            if args.track_time:
                part1_time = time.time()

            try:
                solution_string, raw_solution = solution.part1()
            except (NotImplementedError, RuntimeError) as error:
                print(f"\u001b[31;1mERROR: {error}\u001b[0m")
            else:
                print("\u001b[34;1m" + solution_string + "\u001b[0m")

                # check if solutions equals the expected test result
                if run_is_test:
                    assert expected_results != None

                    if expected_results["part1"] == None:
                        print("\u001b[34;1mSolution not testable.\u001b[0m")
                    elif expected_results["part1"] == str(raw_solution):
                        print("\u001b[32;1mThis solution is correct!\u001b[0m")
                    else:
                        print("\u001b[31;1mThis solution is incorrect! Expected solution: \u001b[4m" + expected_results["part1"] + "\u001b[0m")

            if args.track_time:
                part1_time = time.time() - part1_time
                print(f"\u001b[7mPart 1 took {part1_time:.5f} seconds to complete\u001b[0m")

        # run part 2
        if (args.part == None) or (args.part == 2):
            print("\nPart 2:")

            if args.track_time:
                part2_time = time.time()

            try:
                solution_string, raw_solution = solution.part2()
            except (NotImplementedError, RuntimeError) as error:
                print(f"\u001b[31;1mERROR: {error}\u001b[0m")
            else:
                print("\u001b[34;1m" + solution_string + "\u001b[0m")

                # check if solutions equals the expected test result
                if run_is_test:
                    assert expected_results != None

                    if expected_results["part2"] == None:
                        print("\u001b[34;1mSolution not testable.\u001b[0m")
                    elif expected_results["part2"] == str(raw_solution):
                        print("\u001b[32;1mThis solution is correct!\u001b[0m")
                    else:
                        print("\u001b[31;1mThis solution is incorrect! Expected solution: \u001b[4m" + expected_results["part2"] + "\u001b[0m")

            if args.track_time:
                part2_time = time.time() - part2_time
                print(f"\u001b[7mPart 2 took {part2_time:.5f} seconds to complete\u001b[0m")

    if args.track_time:
        print(f"\n\u001b[7mTotal compute time: {(parse_time + part1_time + part2_time + visualization_time):.5f} seconds\u001b[0m")