from collections import defaultdict
from typing import override
from utility.path_finding import get_manhatten_distance
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.space_map: dict[tuple[int, int], str] = {}
        self.galaxies: list[tuple[int, int]] = []
        self.row_contains_galaxy: dict[int, bool] = {}
        self.column_contains_galaxy: defaultdict[int, bool] = defaultdict(lambda: False)

        image = aoc.parse_input(puzzle_input)
        for y, line in enumerate(image):
            self.row_contains_galaxy[y] = False

            for x, element in enumerate(line):
                self.space_map[x, y] = element
                self.column_contains_galaxy[x] |= False

                if (element == "#"):
                    self.galaxies.append((x, y))
                    self.row_contains_galaxy[y] = True
                    self.column_contains_galaxy[x] = True


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        distances: list[int] = []
        for idx, galaxy1 in enumerate(self.galaxies):
            for galaxy2 in self.galaxies[idx + 1 :]:
                # get basic manhatten distance
                distances.append(get_manhatten_distance(galaxy1, galaxy2))

                # add space for empty columns
                for x in range(min(galaxy1[0], galaxy2[0]) + 1, max(galaxy1[0], galaxy2[0])):
                    if not self.column_contains_galaxy[x]:
                        distances[-1] += 1

                # add spaces for empty rows
                for y in range(min(galaxy1[1], galaxy2[1]) + 1, max(galaxy1[1], galaxy2[1])):
                    if not self.row_contains_galaxy[y]:
                        distances[-1] += 1

        distances_sum: int = sum(distances)

        return f"Sum of shortest path distances: {distances_sum}", distances_sum


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()