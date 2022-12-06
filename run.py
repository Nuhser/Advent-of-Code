import aoc_util as aoc
import argparse
import importlib

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = "python3 run.py",
        description = "",
        epilog = "If you have problems or questions, contact me at mail@nuhser.com."
    )

    parser.add_argument("year", type=int, metavar="YEAR", help="year to use")
    parser.add_argument("day", type=int, metavar="DAY", help="day to use")
    parser.add_argument("-t", "--test", action="store_true", dest="use_test_input", help="use test input instead of real one")
    parser.add_argument("-p", "--part", type=int, dest="part", help="which part of the task should be executed (default: both)")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="show more logs while running")
    parser.add_argument("--version", action="version", version="v22.01.1", help="show the version of this program")

    args = parser.parse_args()

    print(f"Executing year {args.year} day {args.day}...\n")

    puzzle_input = aoc.get_puzzle_input(args.year, args.day) if not args.use_test_input else aoc.get_test_input(args.year, args.day)

    try:
        solution = importlib.import_module(f"{args.year}.day{args.day:02d}").Solution(args.year, args.day, puzzle_input, args.verbose)
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f"There is no solution module for day {args.day} of year {args.year}! Create a module named '{args.year}/day{args.day:02d}.py'")

    if (args.part == None) or (args.part == 1):
        print("Part 1:\n" + solution.part1() + "\n")
    
    if (args.part == None) or (args.part == 2):
        print("Part 2:\n" + solution.part2())
