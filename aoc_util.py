class AbstractSolution:
    def __init__(self, year: int, day: int, puzzle_input: list[str], *params, is_test: bool=False, verbose: bool=False) -> None:
        self.year = year
        self.day = day
        self.is_test = is_test
        self.verbose = verbose
        self.params = params

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