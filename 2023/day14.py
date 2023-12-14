from enum import Enum
from typing import override
from utility.mapping import generate_map_with_coordinates, get_map_dimensions, get_row_of_map, print_map
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.platform: dict[tuple[int, int], "Solution.RockType"] = generate_map_with_coordinates(aoc.parse_input(puzzle_input), self.RockType)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        most_north_rocks: list[int] = [-1 if (rock == self.RockType.NONE) else 0 for _, rock in get_row_of_map(self.platform, 0)]
        _, y_len = get_map_dimensions(self.platform)

        for y in range(1, y_len):
            for (x, _), rock in get_row_of_map(self.platform, y):
                match rock:
                    case self.RockType.NONE:
                        continue
                    case self.RockType.SQUARE:
                        most_north_rocks[x] = y
                    case self.RockType.ROUND:
                        self.platform[x, y] = self.RockType.NONE
                        self.platform[x, most_north_rocks[x] + 1] = self.RockType.ROUND
                        most_north_rocks[x] += 1

        if self.verbose:
            print("Platform after tilting north:")
            print_map(self.platform, end="\n")

        weight: int = 0
        for y in range(y_len):
            for _, rock in get_row_of_map(self.platform, y):
                if rock == self.RockType.ROUND:
                    weight += y_len - y

        return f"Total load on north support beams: {weight}", weight


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()
    

    class RockType(Enum):
        NONE = "."
        ROUND = "O"
        SQUARE = "#"

        def __str__(self):
            return self.value