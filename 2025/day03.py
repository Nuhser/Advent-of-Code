from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.banks: list[list[int]] = [[int(c) for c in bank] for bank in aoc.parse_input(puzzle_input)]


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        joltages: list[int] = []

        for bank in self.banks:
            first_digit: int = max(bank[: -1])
            possible_first_indices: list[int] = [idx for idx, value in enumerate(bank[: -1]) if (value == first_digit)]

            second_digit: int = 0
            for idx in possible_first_indices:
                for value in bank[idx+1 :]:
                    if (second_digit < value):
                        second_digit = value

            joltages.append((first_digit * 10) + second_digit)

        total_joltage = sum(joltages)

        return f"The total joltage is {total_joltage}", total_joltage


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()