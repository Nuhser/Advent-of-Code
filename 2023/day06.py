from math import ceil, floor, prod, sqrt
from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        lines: list[str] = aoc.parse_input(puzzle_input, "")

        self.races: list[dict[str, int]] = []
        for idx in range(1, len(lines[0])):
            self.races.append({"time": int(lines[0][idx]), "record": int(lines[1][idx])})

        self.time_part_2: int = int(puzzle_input[0].strip().replace(" ", "").split(":")[1])
        self.record_part_2: int = int(puzzle_input[1].strip().replace(" ", "").split(":")[1])


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        number_of_wins: list[int] = []
        for race in self.races:
            number_of_wins.append(self.get_number_of_possible_wins(race["time"], race["record"]))

        margin = prod(number_of_wins)

        return f"Number of wins: {number_of_wins}\nMargin: {margin}", margin


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        number_of_wins: int = self.get_number_of_possible_wins(self.time_part_2, self.record_part_2)

        return f"Number of wins: {number_of_wins}", number_of_wins


    def get_number_of_possible_wins(self, time: int, record: int) -> int:
        x = sqrt(((-time / 2) ** 2) - (record + 1))

        x1 = floor((time / 2) + x)
        x2 = ceil((time / 2) - x)

        return abs(int(x1 - x2)) + 1