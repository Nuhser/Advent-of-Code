from enum import Enum
from typing import override
import aoc_util as aoc
from utility.mapping import Map


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.map: Map['Solution.MapField'] = Map(aoc.parse_input(puzzle_input), cast_to=self.MapField)
        self.start = self.map.find_coords(self.MapField.START)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        coords_to_check: set[tuple[int, int]] = {self.start}

        splitters_hit: set[tuple[int, int]] = set()
        while(len(coords_to_check) > 0):
            for coords in coords_to_check.copy():
                coords_to_check.remove(coords)

                next_coords: tuple[int, int] = (coords[0], coords[1] + 1)
                if (self.map.check_coords_in_bounds(next_coords)):
                    if (self.map[next_coords] == self.MapField.EMPTY):
                        coords_to_check.add(next_coords)
                    else:
                        splitters_hit.add(next_coords)
                        coords_to_check.add((next_coords[0] - 1, next_coords[1]))
                        coords_to_check.add((next_coords[0] + 1, next_coords[1]))

        return f"The beams hit {len(splitters_hit)} splitters.", len(splitters_hit)


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()
    
    class MapField(Enum):
        START = 'S'
        EMPTY = '.'
        SPLITTER = '^'