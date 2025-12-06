from math import prod
from typing import override
import aoc_util as aoc
import utility.util as util


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.puzzle_input = [line.replace('\n', '') for line in puzzle_input]


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        problems = [[int(s.strip()) for s in line if (not s.isspace() and s != '')] for line in aoc.parse_input(self.puzzle_input[: -1], ' ')]
        problems.append([s.strip() for s in aoc.parse_input(self.puzzle_input[-1 :], ' ')[0] if (not s.isspace() and s != '')])
        problems = util.flip_2d_list(problems)

        total: int = 0
        for problem in problems:
            total += sum(problem[: -1]) if problem[-1] == '+' else prod(problem[: -1])
        
        return f"The total is {total}", total


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        total: int = 0

        current_problem: list[int] = []
        current_operation: str = ''
        for i in range(len(self.puzzle_input[0])):
            column: list[int] = []

            for line in self.puzzle_input[: -1]:
                if (line[i] != ' '):
                    column.append(int(line[i]))

            if (self.puzzle_input[-1][i] != ' '):
                current_operation = self.puzzle_input[-1][i]

            # calculate current problem
            if (len(column) == 0):
                total += sum(current_problem) if current_operation == '+' else prod(current_problem)
                current_problem = []
                current_operation = ''
                continue

            current_problem.append(sum([(10 ** i) * digit for i, digit in enumerate(reversed(column))]))

        # add last problem
        total += sum(current_problem) if current_operation == '+' else prod(current_problem)

        return f"The total is {total}", total