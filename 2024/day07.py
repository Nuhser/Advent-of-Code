from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.equations: list[tuple[int, list[int]]] = [
            (input[0][0], input[1])
            for input in aoc.parse_input(puzzle_input, ": ", " ", cast_to=int)
        ]

    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        possible_solutions: list[list[int]] = [
            self.get_possible_solutions(equation[1]) for equation in self.equations
        ]

        correct_solutions_sum: int = 0
        for idx, solutions in enumerate(possible_solutions):
            for solution in solutions:
                if self.equations[idx][0] == solution:
                    correct_solutions_sum += solution
                    break

        return (
            f"Total Calibration Result: {correct_solutions_sum}",
            correct_solutions_sum,
        )

    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        possible_solutions: list[list[int]] = [
            self.get_possible_solutions(equation[1], True)
            for equation in self.equations
        ]

        correct_solutions_sum: int = 0
        for idx, solutions in enumerate(possible_solutions):
            for solution in solutions:
                if self.equations[idx][0] == solution:
                    correct_solutions_sum += solution
                    break

        return (
            f"Total Calibration Result: {correct_solutions_sum}",
            correct_solutions_sum,
        )

    def get_possible_solutions(
        self, inputs: list[int], with_concatenation: bool = False
    ) -> list[int]:
        if len(inputs) == 1:
            return inputs

        return (
            [
                inputs[-1] + possible_solution
                for possible_solution in self.get_possible_solutions(
                    inputs[:-1], with_concatenation
                )
            ]
            + [
                inputs[-1] * possible_solution
                for possible_solution in self.get_possible_solutions(
                    inputs[:-1], with_concatenation
                )
            ]
            + (
                [
                    int(str(possible_solution) + str(inputs[-1]))
                    for possible_solution in self.get_possible_solutions(
                        inputs[:-1], with_concatenation
                    )
                ]
                if with_concatenation
                else []
            )
        )
