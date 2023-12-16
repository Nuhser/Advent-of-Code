from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.sequence = aoc.parse_input(puzzle_input, ",")[0]


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        total_sum:int = 0

        for code in self.sequence:
            test_sum:int = 0

            for char in code:
                test_sum += ord(char)
                test_sum *= 17
                test_sum %= 256

            total_sum += test_sum

        return f"The test sum is {total_sum}", total_sum


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()