def parse_input(day: int, *delimiters: str, strip_lines: bool=True, cast_to: type=str, use_test: bool=False) -> list:
    with open(f"./input{day:02d}.txt" if not use_test else f"./test{day:02d}.txt", "r") as puzzle_input:
        if len(delimiters) == 0:
            return [cast_to(line.strip() if strip_lines else line) for line in puzzle_input.readlines()]
        else:
            return [recursive_split(line.strip() if strip_lines else line, delimiters, cast_to) for line in puzzle_input.readlines()]

def parse_input_with_blocks(day: int, *line_delimiters: str, block_delimiter: str="", strip_lines: bool=True, cast_to: type=str, use_test: bool=False) -> list[list]:
    blocks = [[]]
    with open(f"./input{day:02d}.txt" if not use_test else f"./test{day:02d}.txt", "r") as puzzle_input:
        for line in [line.strip() if strip_lines else line for line in puzzle_input.readlines()]:
            if line == block_delimiter:
                blocks.append([])
                continue

            if len(line_delimiters) == 0:
                blocks[-1].append(cast_to(line))
            else:
                blocks[-1].append([recursive_split(line, line_delimiters, cast_to) for line in puzzle_input.readlines()])

    return blocks

def recursive_split(item: str, delimiters: tuple, cast_to: type):
    if len(delimiters) <= 1:
        return [cast_to(subitem) for subitem in item.split(delimiters[0])]
    else:
        return [recursive_split(subitem, delimiters[1:], cast_to) for subitem in item.split(delimiters[0])]

def split_string_in_chunks(string: str, chunk_size: int, padding_size: int=0) -> list[str]:
    chunks = []
    for i in range(0, len(string), chunk_size + padding_size):
        chunks.append(string[i : i+chunk_size])

    return chunks