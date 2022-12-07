import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.commands = [(direction, int(strength)) for direction, strength in aoc.parse_input(puzzle_input, " ")]

    def part1(self) -> tuple[str, (int | str)]:
        horizontal = 0
        depth = 0

        for command in self.commands:
            if command[0] == 'forward':
                horizontal += command[1]
            elif command[0] == 'up':
                depth -= command[1]
            elif command[0] == 'down':
                depth += command[1]
            else:
                raise RuntimeError(f'Unknown command "{command[0]}"')

        return f'Horizontal Position: {horizontal}\nDepth: {depth}\n\nSolution: {horizontal * depth}', horizontal * depth

    def part2(self) -> tuple[str, (int | str)]:
        horizontal = 0
        depth = 0
        aim = 0

        for command in self.commands:
            if command[0] == 'forward':
                horizontal += command[1]
                depth += aim * command[1]
            elif command[0] == 'up':
                aim -= command[1]
            elif command[0] == 'down':
                aim += command[1]
            else:
                raise RuntimeError(f'Unknown command "{command[0]}"')

        return f'Horizontal Position: {horizontal}\nDepth: {depth}\n\nSolution: {horizontal * depth}', horizontal * depth
