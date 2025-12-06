from math import prod
from typing import override
import re
import aoc_util as aoc
import utility.util as util


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.problems = [[int(i.strip()) for i in line if (not i.isspace() and i != '')] for line in aoc.parse_input(puzzle_input[: -1], ' ')]
        self.problems.append([s.strip() for s in aoc.parse_input(puzzle_input[-1 :], ' ')[0] if not s.isspace() and s != ''])
        self.problems = util.flip_2d_list(self.problems)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        total: int = 0
        for problem in self.problems:
            total += sum(problem[: -1]) if problem[-1] == '+' else prod(problem[: -1])
        
        return f"The total is {total}", total


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()