from typing import override
import aoc_util as aoc
from utility.k_d_tree import KDTree


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.junction_boxes = [
            (pos[0], pos[1], pos[2])
            for pos in aoc.parse_input(puzzle_input, ",", cast_to=int)
        ]

    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        tree: KDTree = KDTree(self.junction_boxes)

        return super().part1()

    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()
