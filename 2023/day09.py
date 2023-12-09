from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        histories = aoc.parse_input(puzzle_input, " ", cast_to=int)
        self.history_diffs: list[list[list[int]]] = []

        for history in histories:
            differences: list[list[int]] = [history.copy()]
            current_values: list[int] = history.copy()

            while any(value != 0 for value in current_values):
                differences.append([])
                for i in range(len(current_values) - 1):
                    differences[-1].append(current_values[i+1] - current_values[i])

                current_values = differences[-1].copy()

            self.history_diffs.append(differences)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        predictions: list[int] = []
        for differences in self.history_diffs:
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
        predictions: list[int] = []
        for differences in self.history_diffs:
            prediction: int = 0
            for difference in differences[-2 :: -1]:
                prediction = difference[0] - prediction

            predictions.append(prediction)

        if self.verbose:
            print(f"Predictions for first numbers: {predictions}")

        predictions_sum: int = sum(predictions)

        return f"Sum of predictions: {predictions_sum}", predictions_sum