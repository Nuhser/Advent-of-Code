import aoc_util as aoc
import argparse
import importlib

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = "python3 run.py",
        description = "",
        epilog = "If you have problems or questions, contact me at mail@nuhser.com."
    )
    subparsers = parser.add_subparsers(help="subcommands for running solution/tests or visualizing", dest="subcommand")

    parser.add_argument("year", type=int, metavar="YEAR", help="year to use")
    parser.add_argument("day", type=int, metavar="DAY", help="day to use")
    parser.add_argument("--verbose", action="store_true", dest="verbose", help="show more logs while running")
    parser.add_argument("--version", action="version", version="v22.01.1", help="show the version of this program")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("-t", "--test", dest="expected_solutions", metavar="EXPECTATIONS", nargs="+", help="test solution with test input and compare to expected value")
    run_parser.add_argument("-p", "--part", type=int, dest="part", choices=[0, 1, 2], help="which part of the task should be executed (default: both), use 0 to test only the parser")

    visualization_parser = subparsers.add_parser("visualize")

    args = parser.parse_args()

    # check if run is test
    run_is_test = (args.subcommand == "run") and (args.expected_solutions != None)
    if run_is_test:
        if (args.part == None) and (len(args.expected_solutions) != 2):
            raise AttributeError("Two expected test results are needed when testing both parts of the solution.")
        elif (args.part != None) and (len(args.expected_solutions) != 1):
            raise AttributeError("Exactly one expected test result is needed when testing only one part of the solution.")

    # get puzzle/test input
    try:
        puzzle_input = aoc.get_puzzle_input(args.year, args.day) if not run_is_test else aoc.get_test_input(args.year, args.day)
    except FileNotFoundError:
        if run_is_test:
            raise FileNotFoundError(f"There is no test input for day {args.day} of year {args.year}! Create a text file named '{args.year}/test{args.day:02d}.txt'")
        else:
            raise FileNotFoundError(f"There is no puzzle input for day {args.day} of year {args.year}! Create a text file named '{args.year}/input{args.day:02d}.txt'")

    # create solution object for given day and year
    try:
        solution = importlib.import_module(f"{args.year}.day{args.day:02d}").Solution(args.year, args.day, puzzle_input, args.verbose)
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f"There is no solution module for day {args.day} of year {args.year}! Create a module named '{args.year}/day{args.day:02d}.py'")

    # start visualization and exit program if wanted
    if (args.subcommand == "visualize"):
        print("Starting visualization...")
        solution.visualize()
        raise SystemExit

    # else start normal run
    print(f"{'Testing' if run_is_test else 'Executing'} year {args.year} day {args.day}...")

    # run part 1
    if (args.part == None) or (args.part == 1):
        print("\nPart 1:")

        try:
            solution_string, raw_solution = solution.part1()
        except RuntimeError as error:
            print(f"ERROR: {error}")
        else:
            print(solution_string)

            if run_is_test:
                if args.expected_solutions[0] == str(raw_solution):
                    print("This solution is correct!")
                else:
                    print("This solution is incorrect! Expected solution: " + args.expected_solutions[0])

    # run part 2
    if (args.part == None) or (args.part == 2):
        print("\nPart 2:")

        try:
            solution_string, raw_solution = solution.part2()
        except RuntimeError as error:
            print(f"ERROR: {error}")
        else:
            print(solution_string)

            if run_is_test:
                if args.expected_solutions[-1] == str(raw_solution):
                    print("This solution is correct!")
                else:
                    print("This solution is incorrect! Expected solution: " + args.expected_solutions[-1])