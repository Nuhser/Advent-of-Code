from typing import override
import aoc_util as aoc
import math


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

        return f"The arrow is pointing {count} times at '0'.", count


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        count: int = 0
        position: int = 50

        for command in self.commands:
            started_on_zero = position == 0
            count += abs(command) // 100

            command = (abs(command) % 100) * (-1 if (command < 0) else 1)
            position += command

            if (not started_on_zero) and ((position <= 0) or (position >= 100)):
                count += 1

            position %= 100

        return f"The arrow passed '0' {count} times.", count