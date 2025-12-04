from enum import Enum
from typing import override
import aoc_util as aoc
import utility.mapping as mapping


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.map = mapping.Map(aoc.parse_input(puzzle_input), cast_to=self.GridCell)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        accessable_rolls: int = 0
        for coords in self.map.find_all_coords(self.GridCell.ROLL):
            neighbor_rolls = self.map.get_matching_neighbors(
                coords,
                lambda _, n: bool(n[1])
            )

            accessable_rolls += 1 if len(neighbor_rolls) < 4 else 0

        return f"There are {accessable_rolls} accessable rolls.", accessable_rolls


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        map = self.map.copy()
        removed_rolls: int = 0

        while(True):
            accessable_rolls: list[tuple[int, int]] = []
            for coords in map.find_all_coords(self.GridCell.ROLL):
                neighbor_rolls = map.get_matching_neighbors(
                    coords,
                    lambda _, n: bool(n[1])
                )

                if (len(neighbor_rolls) < 4):
                    accessable_rolls.append(coords)

            if (len(accessable_rolls) < 1):
                break

            for coords in accessable_rolls:
                map.set(coords, self.GridCell.EMPTY)

            removed_rolls += len(accessable_rolls)

        return f"{removed_rolls} rolls could be removed.", removed_rolls


    class GridCell(Enum):
        EMPTY = "."
        ROLL = "@"

        def __bool__(self) -> bool:
            return self == Solution.GridCell.ROLL