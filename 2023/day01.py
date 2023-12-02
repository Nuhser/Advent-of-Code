from tabnanny import verbose
import aoc_util as aoc

from typing import override


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.numbers: list[int] = []
        for line in puzzle_input:
            digits = [char for char in line if char.isdigit()]
            self.numbers.append(int(digits[0] + digits[-1]))

        if (self.verbose):
            print(f"Numbers: {", ".join(str(number) for number in self.numbers)}")
        
    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        return f"The sum of all the calibration values is {sum(self.numbers)}", sum(self.numbers)

    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        raise NotImplementedError(f"Part 2 of the solution for day {self.day} of year {self.year} isn't implemented yet!")