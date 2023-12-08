from math import floor
from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.modules = aoc.parse_input(puzzle_input, cast_to=int)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        fuel_sum: int = 0
        for module in self.modules:
            fuel_sum += floor(module / 3) - 2

        return f"Required Fuel: {fuel_sum}", fuel_sum


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        modules = self.modules.copy()

        fuel_sum: int = 0
        for mass in modules:
            while mass > 0:
                mass = floor(mass / 3) - 2

                if mass > 0:
                    fuel_sum += mass

        return f"Required Fuel: {fuel_sum}", fuel_sum