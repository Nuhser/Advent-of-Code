from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.histories = aoc.parse_input(puzzle_input, " ", cast_to=int)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        predictions: list[int] = []
        for history in self.histories:
            differences: list[list[int]] = [history.copy()]
            current_values: list[int] = history.copy()

            while any(value != 0 for value in current_values):
                differences.append([])
                for i in range(len(current_values) - 1):
                    differences[-1].append(current_values[i+1] - current_values[i])

                current_values = differences[-1].copy()

            prediction: int = 0
            for difference in differences[-2 :: -1]:
                prediction += difference[-1]

            predictions.append(prediction)

        if self.verbose:
            print(f"Predictions for next numbers: {predictions}")

        predictions_sum: int = sum(predictions)

        return f"Sum of predictions: {predictions_sum}", predictions_sum


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()