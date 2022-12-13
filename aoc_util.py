import heapq as heap

from collections import defaultdict
from typing import Any, Callable, TypeVar

# used for generics
T = TypeVar("T")

# ANSI escapes
ANSI_RESET = "\u001b[0m"

ANSI_ITALIC = "\u001b[3m"
ANSI_NOT_ITALIC = "\u001b[23m"
ANSI_UNDERLINE = "\u001b[4m"
ANSI_NOT_UNDERLINE = "\u001b[24m"
ANSI_STRIKEOUT = "\u001b[9m"
ANSI_NOT_STRIKEOUT = "\u001b[29m"
ANSI_DIM = "\u001b[2m"
ANSI_NOT_DIM = "\u001b[22m"
ANSI_INVERTED = "\u001b[7m"
ANSI_NOT_INVERTED = "\u001b[27m"

ANSI_COLOR = {
    "default": "\u001b[39;1m",
    "black": "\u001b[30;1m",
    "blue": "\u001b[34;1m",
    "cyan": "\u001b[36;1m",
    "green": "\u001b[32;1m",
    "magenta": "\u001b[35;1m",
    "red": "\u001b[31;1m",
    "yellow": "\u001b[33;1m",
    "white": "\u001b[37;1m"
}

ANSI_COLOR = {
    "default": "\u001b[39;1m",
    "black": "\u001b[30;1m",
    "blue": "\u001b[34;1m",
    "cyan": "\u001b[36;1m",
    "green": "\u001b[32;1m",
    "magenta": "\u001b[35;1m",
    "red": "\u001b[31;1m",
    "yellow": "\u001b[33;1m",
    "white": "\u001b[37;1m"
}

ANSI_BG_COLOR = {
    "default": "\u001b[49;1m",
    "black": "\u001b[40;1m",
    "blue": "\u001b[44;1m",
    "cyan": "\u001b[46;1m",
    "green": "\u001b[42;1m",
    "magenta": "\u001b[45;1m",
    "red": "\u001b[41;1m",
    "yellow": "\u001b[43;1m",
    "white": "\u001b[47;1m"
}

ANSI_UP = "\u001b[1A"
ANSI_DOWN = "\u001b[1B"
ANSI_RIGHT = "\u001b[1C"
ANSI_LEFT = "\u001b[1D"
ANSI_SCREEN_BEGINNING = "\u001b[H"
ANSI_LINE_BEGINNING = "\u001b[1F"

ANSI_CLEAR_LINE = "\u001b[2K"
ANSI_CLEAR_SCREEN = "\u001b[2J"

class AbstractSolution:
    def __init__(self, year: int, day: int, puzzle_input: list[str], verbose: bool=False) -> None:
        self.year = year
        self.day = day
        self.verbose = verbose

        if verbose:
            print("Start parsing input...\n")

        self.parse(puzzle_input)

        if verbose:
            print("Parsing complete.\n")

    def parse(self, puzzle_input: list[str]) -> None:
        raise NotImplementedError(f"The parser the puzzle input for day {self.day} of year {self.year} isn't implemented yet!")

    def part1(self) -> tuple[str, (int | float | str | None)]:
        raise NotImplementedError(f"Part 1 of the solution for day {self.day} of year {self.year} isn't implemented yet!")

    def part2(self) -> tuple[str, (int | float | str | None)]:
        raise NotImplementedError(f"Part 2 of the solution for day {self.day} of year {self.year} isn't implemented yet!")

    def visualize(self) -> None:
        raise NotImplementedError(f"The visualization for day {self.day} of year {self.year} isn't implemented yet!")

def get_puzzle_input(year: int, day: int) -> tuple[list[str], None]:
    with open(f"./{year}/input{day:02d}.txt", "r") as puzzle_input:
        return [line for line in puzzle_input.readlines()], None

def get_test_input(year: int, day: int, test_number: int) -> tuple[list[str], dict[str, (str | None)]]:
    with open(f"./{year}/test{day:02d}{f'-{test_number}' if (test_number > -1) else ''}.txt", "r") as test_input:
        expected_results = {}

        while (True):
            last_position = test_input.tell()
            line = test_input.readline()
            
            if (not line.strip().startswith("#!")):
                break

            line = line.strip().removeprefix("#!").split(":")

            expected_results[line[0]] = line[1] if not line[1] == "None" else None

        test_input.seek(last_position)

        return [line for line in test_input.readlines()], expected_results

def parse_input(puzzle_input: list[str], *delimiters: str, strip_lines: bool=True, cast_to: type=str) -> list:
    if len(delimiters) == 0:
        return [cast_to(line.strip() if strip_lines else line) for line in puzzle_input]
    else:
        return [recursive_split(line.strip() if strip_lines else line, delimiters, cast_to) for line in puzzle_input]

def parse_input_with_blocks(puzzle_input: list[str], *line_delimiters: str, block_delimiter: str="", strip_lines: bool=True, cast_to: type=str) -> list[list]:
    blocks = [[]]
    for line in [line.strip() if strip_lines else line for line in puzzle_input]:
        if line == block_delimiter:
            blocks.append([])
            continue

        if len(line_delimiters) == 0:
            blocks[-1].append(cast_to(line))
        else:
            blocks[-1].append(recursive_split(line, line_delimiters, cast_to))

    return blocks

def recursive_split(item: str, delimiters: tuple, cast_to: type) -> list:
    if len(delimiters) <= 1:
        return [cast_to(subitem) for subitem in (item.split(delimiters[0]) if delimiters[0] != "" else item.split())]
    else:
        return [recursive_split(subitem, delimiters[1:], cast_to) for subitem in (item.split(delimiters[0]) if delimiters[0] != "" else item.split())]

def split_string_in_chunks(string: str, chunk_size: int, padding_size: int=0, cast_to: type=str) -> list:
    chunks = []
    for i in range(0, len(string), chunk_size + padding_size):
        chunks.append(cast_to(string[i : i+chunk_size]))

    return chunks

def convert_hex_to_bin(hex_string: str) -> str:
    return str(bin(int(hex_string, base=16)))[2 :].zfill(4)

def calculate_dijkstra(map: dict[tuple[int, int], list[tuple[tuple[int, int], int]]], starting_point: tuple[int, int], end_point: (None | tuple[int, int])=None) -> tuple[dict[tuple[int, int], tuple[int,int]], defaultdict[tuple[int, int], (int | float)]]:
    """
    This method calculates the lowest cost to get to every point on a map starting at starting_point as well as every points parent on the cheapest path from the starting point to that point.

    Parameter
    ---------
    map : dict[tuple[int, int], list[tuple[tuple[int, int], int]]]
        A map of points where the key is a tuple of the points x- and y-coordinates and the value is a list of every adjacent point and the cost/weight to get to this point.

    starting_point : tuple[int, int]
        The x- and y-coordinates of the starting point of the cost calculations.

    Returns
    -------
    parent_map, costs
        Two dictionaries which both use the x- and y-coordinates of the points on the map as theier keys. parent_map has the parent of the individual point on the cheapest path beginning at the starting point as its value and costs the cost to get to this point.
    """

    visited = set()
    parents_map: dict[tuple[int, int], tuple[int,int]] = {}
    costs: defaultdict[tuple[int, int], (int | float)] = defaultdict(lambda: float("inf"))
    costs[starting_point] = 0
    priority_queue = []
    heap.heappush(priority_queue, (0, starting_point))

    while priority_queue:
        _, point = heap.heappop(priority_queue)
        visited.add(point)

        for adjacent_point, weight in map[point]:
            if adjacent_point in visited:
                continue

            new_cost = costs[point] + weight
            if new_cost < costs[adjacent_point]:
                parents_map[adjacent_point] = point
                costs[adjacent_point] = new_cost
                heap.heappush(priority_queue, (new_cost, adjacent_point))

        if (end_point != None) and (end_point == point):
            break

    return parents_map, costs

def bubble_sort(sorting_list: list[T], comparison_function: Callable[[T, T], (bool | None)]) -> list[T]:
    sorted_list = sorting_list.copy()

    swapped = False
    for i in range(len(sorted_list) - 1):
        for j in range(len(sorted_list) - 1 - i):
            if not comparison_function(sorted_list[j], sorted_list[j + 1]):
                swapped = True
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
        
        if not swapped:
            break

    return sorted_list