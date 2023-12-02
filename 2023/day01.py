from tabnanny import verbose
import aoc_util as aoc

from typing import override


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.puzzle_input = puzzle_input
        
    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        numbers: list[int] = []
        for line in self.puzzle_input:
            digits = [char for char in line if char.isdigit()]
            numbers.append(int(digits[0] + digits[-1]))

        if (self.verbose):
            print(f"Numbers: {", ".join(str(number) for number in numbers)}")

        return f"The sum of all the calibration values is {sum(numbers)}", sum(numbers)

    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        # left characters before and after every number in case of numbers sharing a letter in the input file
        digits_dict = {
            "one": "o1e",
            "two": "t2o",
            "three": "t3e",
            "four": "f4r",
            "five": "f5e",
            "six": "s6x",
            "seven": "s7n",
            "eight": "e8t",
            "nine": "n9e"
        }

        numbers = []
        for line in self.puzzle_input:
            for key in digits_dict:
                line = line.replace(key, str(digits_dict[key]))

            digits = [char for char in line if char.isdigit()]
            numbers.append(int(digits[0] + digits[-1]))

        if (self.verbose):
            print(f"Numbers: {", ".join(str(number) for number in numbers)}")

        return f"The sum of all the calibration values is {sum(numbers)}", sum(numbers)
