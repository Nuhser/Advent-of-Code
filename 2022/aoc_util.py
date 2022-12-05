def get_puzzle_input(day: int):
    with open(f"./input{day:02d}.txt", "r") as puzzle_input:
        return [line for line in puzzle_input.readlines()]

def get_test_input(day: int):
    with open(f"./test{day:02d}.txt", "r") as test_input:
        return [line for line in test_input.readlines()]

def parse_input(puzzle_input: list[str], *delimiters: str, strip_lines: bool=True, cast_to: type=str, use_test: bool=False) -> list:
    if len(delimiters) == 0:
        return [cast_to(line.strip() if strip_lines else line) for line in puzzle_input]
    else:
        return [recursive_split(line.strip() if strip_lines else line, delimiters, cast_to) for line in puzzle_input]

def parse_input_with_blocks(puzzle_input: list[str], *line_delimiters: str, block_delimiter: str="", strip_lines: bool=True, cast_to: type=str, use_test: bool=False) -> list[list]:
    blocks = [[]]
    for line in [line.strip() if strip_lines else line for line in puzzle_input]:
        if line == block_delimiter:
            blocks.append([])
            continue

        if len(line_delimiters) == 0:
            blocks[-1].append(cast_to(line))
        else:
            blocks[-1].append([recursive_split(line, line_delimiters, cast_to) for line in puzzle_input])

    return blocks

def recursive_split(item: str, delimiters: tuple, cast_to: type) -> list:
    if len(delimiters) <= 1:
        return [cast_to(subitem) for subitem in item.split(delimiters[0])]
    else:
        return [recursive_split(subitem, delimiters[1:], cast_to) for subitem in item.split(delimiters[0])]

def split_string_in_chunks(string: str, chunk_size: int, padding_size: int=0) -> list[str]:
    chunks = []
    for i in range(0, len(string), chunk_size + padding_size):
        chunks.append(string[i : i+chunk_size])

    return chunks