from typing import override

import aoc_util as aoc
from utility.mapping import Map
from utility.path_finding import dijkstra
from utility.terminal_formatting import Color


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.map = Map[int](aoc.parse_input(puzzle_input))


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        x_len, y_len = self.map.get_dimensions()

        start: tuple[int, int] = (0, 0)
        end: tuple[int, int] = (x_len-1, y_len-1)

        neighbor_cost_map = {coords: self.map.get_neighbors(coords, diagonal=False) for coords in self.map.get_all_coords()}

        parents, costs = dijkstra(neighbor_cost_map, start, end, 3)

        point = end
        self.map[point] = Color.GREEN + "♦" + Color.DEFAULT
        while (point in parents):
            point = parents[point]
            self.map[point] = Color.GREEN + "♦" + Color.DEFAULT

        print_map(self.map)

        return f"The shortest path from {start} to {end} incurs a heat loss of {costs[end]}", costs[end]


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()