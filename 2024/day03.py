from typing import override
import aoc_util as aoc
import re


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.puzzle_input = aoc.parse_input(puzzle_input)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        correct_instructions: list[str] = [match for line in self.puzzle_input for match in re.findall(r"mul\(\d{1,3},\d{1,3}\)", line)]

        sum: int = 0
        for instruction in correct_instructions:
            numbers = [int(n) for n in instruction.lstrip("mul(").rstrip(")").split(",")]
            sum += numbers[0] * numbers[1]

        return f"Sum: {sum}", sum


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        enabled_parts: list[str] = [
            match for group in re.findall(r"^(.*?)don't\(\)|((?:do\(\).*?)*?)don't\(\)|do\(\)(.*?)$", "".join(self.puzzle_input))
                for match in group
                if (match != "")
        ]

        if (self.verbose):
            print(f"Enabled Groups:\n{"\n".join(enabled_parts)}\n")

        correct_instructions: list[str] = [match for part in enabled_parts for match in re.findall(r"mul\(\d{1,3},\d{1,3}\)", part)]

        sum: int = 0
        for instruction in correct_instructions:
            numbers = [int(n) for n in instruction.lstrip("mul(").rstrip(")").split(",")]
            sum += numbers[0] * numbers[1]

        return f"Sum: {sum}", sum