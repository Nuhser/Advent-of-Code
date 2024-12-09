import itertools
from typing import override

import aoc_util as aoc
import utility.mapping as mapping


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.map = mapping.generate_map_with_coordinates(aoc.parse_input(puzzle_input))
        self.antennas = mapping.invert_map(
            {key: value for key, value in self.map.items() if value != "."}
        )

    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        antinodes: set[tuple[int, int]] = set()

        for _, coords in self.antennas.items():
            for pair in list(itertools.combinations(coords, 2)):
                vector = (pair[1][0] - pair[0][0], pair[1][1] - pair[0][1])

                antinodes.add((pair[0][0] - vector[0], pair[0][1] - vector[1]))
                antinodes.add((pair[1][0] + vector[0], pair[1][1] + vector[1]))

        number_of_antinodes = len(
            [
                antinode
                for antinode in antinodes
                if mapping.is_coord_in_map(self.map, antinode)
            ]
        )

        return (
            f"Number of antinodes inside bounds: {number_of_antinodes}",
            number_of_antinodes,
        )

    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()
