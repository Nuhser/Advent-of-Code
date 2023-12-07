from math import ceil, floor, prod, sqrt
from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        lines = aoc.parse_input(puzzle_input, "")

        self.races: list[dict[str, int]] = []
        for idx in range(1, len(lines[0])):
            self.races.append({"time": int(lines[0][idx]), "record": int(lines[1][idx])})


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        number_of_wins: list[int] = []
        for race in self.races:
            x = sqrt(((-race["time"] / 2) ** 2) - (race["record"] + 1))

            x1 = floor((race["time"] / 2) + x)
            x2 = ceil((race["time"] / 2) - x)

            number_of_wins.append(abs(int(x1 - x2)) + 1)

        margin = prod(number_of_wins)

        return f"Number of wins: {number_of_wins}\nMargin: {margin}", margin


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        raise NotImplementedError(f"Part 2 of the solution isn't implemented yet!")