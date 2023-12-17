from typing import override
import aoc_util as aoc
from utility.mapping import generate_map_with_coordinates, get_map_dimensions, get_neighbors, print_map
from utility.path_finding import dijkstra
from utility.terminal_formatting import Color


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.map: dict[tuple[int, int], int] = generate_map_with_coordinates(aoc.parse_input(puzzle_input), int)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        x_len, y_len = get_map_dimensions(self.map)

        start: tuple[int, int] = (0, 0)
        end: tuple[int, int] = (x_len-1, y_len-1)

        neighbor_cost_map = {coords: get_neighbors(self.map, coords, diagonal=False) for coords in self.map.keys()}

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