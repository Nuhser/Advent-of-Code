from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        commands: list[str] = aoc.parse_input(puzzle_input)
        self.commands = [int(command.replace("R", "").replace("L", "-")) for command in commands]


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        count: int = 0
        position: int = 50

        for command in self.commands:
            position += command
            position %= 100

            if (position == 0):
                count += 1

        return f"The arrow is pointing {count} times at 0.", count


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()