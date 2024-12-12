import itertools
from typing import override

import aoc_util as aoc
from utility.mapping import Map


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.map = Map(aoc.parse_input(puzzle_input))
        self.antennas = Map.filtered(
            self.map.copy(), lambda _, value: value != "."
        ).get_inverted()

    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        antinodes: set[tuple[int, int]] = set()

        for _, coords in self.antennas.items():
            for pair in list(itertools.combinations(coords, 2)):
                vector = (pair[1][0] - pair[0][0], pair[1][1] - pair[0][1])

                antinodes.add((pair[0][0] - vector[0], pair[0][1] - vector[1]))
                antinodes.add((pair[1][0] + vector[0], pair[1][1] + vector[1]))

        number_of_antinodes = len(
            [antinode for antinode in antinodes if self.map.check_coords_in_bounds(antinode)]
        )

        return (
            f"Number of antinodes inside bounds: {number_of_antinodes}",
            number_of_antinodes,
        )

    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        antinodes: set[tuple[int, int]] = set()

        for _, coords in self.antennas.items():
            for coord in coords:
                antinodes.add(coord)

            for pair in list(itertools.combinations(coords, 2)):
                vector = (pair[1][0] - pair[0][0], pair[1][1] - pair[0][1])

                antinode = pair[0]
                while True:
                    antinode = (antinode[0] - vector[0], antinode[1] - vector[1])

                    if not self.map.check_coords_in_bounds(antinode):
                        break

                    antinodes.add(antinode)

                antinode = pair[0]
                while True:
                    antinode = (antinode[0] + vector[0], antinode[1] + vector[1])

                    if not self.map.check_coords_in_bounds(antinode):
                        break

                    antinodes.add(antinode)

        return f"There are {len(antinodes)} inside the bounds.", len(antinodes)
