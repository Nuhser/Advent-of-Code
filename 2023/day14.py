from enum import Enum
from typing import override
from utility.mapping import generate_map_with_coordinates
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.platform: dict[tuple[int, int], "Solution.RockType"] = generate_map_with_coordinates(aoc.parse_input(puzzle_input), self.RockType)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        most_north_rocks: list[int] = [-1 if (rock == self.RockType.NONE) else 0 for rock in self.platform]


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()
    

    class RockType(Enum):
        NONE = "."
        ROUND = "O"
        SQUARE = "#"