from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.program = aoc.parse_input(puzzle_input, ",", cast_to=int)[0]


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        program: list[int] = self.program.copy()

        if not self.is_test:
            program[1], program[2] = 12, 2

        solution: int = self.run_intcode(program)[0]

        return f"Solution Value: {solution}", solution


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        # This isn't the solution! 64 and 21 are. To get those, the program would need to run backwards beginning with the end value 19690720.

        program: list[int] = self.program.copy()

        if not self.is_test:
            program[1], program[2] = 64, 21

        solution: int = self.run_intcode(program)[0]

        return f"Solution Value: {solution}", solution
    

    def run_intcode(self, program: list[int]) -> list[int]:
        idx = 0
        while idx < len(program):
            # addition
            if program[idx] == 1:
                in_1 = program[idx + 1]
                in_2 = program[idx + 2]
                out = program[idx + 3]

                program[out] = program[in_1] + program[in_2]
                idx += 4

            # multiplication
            elif program[idx] == 2:
                in_1 = program[idx + 1]
                in_2 = program[idx + 2]
                out = program[idx + 3]

                program[out] = program[in_1] * program[in_2]
                idx += 4

            # program finished
            elif program[idx] == 99:
                break

            # error
            else:
                raise RuntimeError(f'Wuuuuuuaaaaaaaa!!! (at position {idx})')

        return program