def parse_input(day: int, delimiter: str="", cast_to: type=str) -> list:
    with open(f"./input{day:02d}.txt", "r") as puzzle_input:
        if delimiter == "":
            return [cast_to(line.strip()) for line in puzzle_input.readlines()]
        else:
            return [[cast_to(element) for element in line.strip().split(delimiter)] for line in puzzle_input.readlines()]

def parse_input_with_blocks(day: int, line_delimiter: str="", block_delimiter: str="", cast_to: type=str) -> list[list]:
    blocks = [[]]
    with open(f"./input{day:02d}.txt", "r") as puzzle_input:
        for line in [line.strip() for line in puzzle_input.readlines()]:
            if line == block_delimiter:
                blocks.append([])
                continue

            if line_delimiter == "":
                blocks[-1].append(cast_to(line))
            else:
                blocks[-1].append([cast_to(element) for element in line.split(line_delimiter)])

    return blocks