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
                value = max(bank[idx+1 :])
                if (second_digit < value):
                    second_digit = value

            joltages.append((first_digit * 10) + second_digit)

        total_joltage = sum(joltages)

        return f"The total joltage is {total_joltage}", total_joltage


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        joltages: list[int] = []

        for i, bank in enumerate(self.banks):
            if (self.verbose):
                print(f"Checking bank {i}...")

            first_digit, index = self.find_biggest_possible_joltage(bank, 0, 11)
            digits: list[int] = [first_digit]

            for end_idx in range(10, -1, -1):
                digit, new_index = self.find_biggest_possible_joltage(bank, index+1, end_idx)

                digits.append(digit)
                index = new_index

            joltages.append(sum([(10 ** i) * digit for i, digit in enumerate(reversed(digits))]))

            if (self.verbose):
                print(f"New joltage: {joltages[-1]}\n")

        total_joltage = sum(joltages)

        return f"The total joltage is {total_joltage}", total_joltage


    def find_biggest_possible_joltage(self, bank: list[int], start_idx: int, end_idx: int) -> tuple[int, int]:
        max_joltage: int = max(bank[start_idx : -end_idx if (end_idx > 0) else None])
        index: int = min([idx for idx, joltage in enumerate(bank[: -end_idx if (end_idx > 0) else None]) if (joltage == max_joltage) and (idx >= start_idx)])

        return max_joltage, index