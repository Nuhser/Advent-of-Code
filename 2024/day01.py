from turtle import right
from typing import override
import aoc_util as aoc
import utility.util as util
import utility.sorting as sorting


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.puzzle_input = aoc.parse_input(puzzle_input, "   ", cast_to=int)
        self.puzzle_input = util.flip_2d_list(self.puzzle_input)

        if (self.verbose and self.is_test):
            print(f"Lists: {self.puzzle_input}")


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        right_list = self.puzzle_input[0].copy()
        sorting.heap_sort(
            right_list,
            lambda a, b: a <= b
        )

        left_list = self.puzzle_input[1].copy()
        sorting.heap_sort(
            left_list,
            lambda a, b: a <= b
        )

        diff: int = 0
        for r, l in [(right_list[i], left_list[i]) for i in range(len(right_list))]:
            diff += abs(r - l)

        return f"The total distance of the two lists is {diff}", diff


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()