from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.patterns = aoc.parse_input_with_blocks(puzzle_input)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        for pattern in self.patterns:
            # check for horizontal mirror
            for idx in range(0, len(pattern) - 1):
                top_part_size = idx + 1

                if (idx + top_part_size > len(pattern)):
                    bottom_part_size = top_part_size - (idx + top_part_size - len(pattern))

                if (pattern[ : top_part_size] == pattern[top_part_size : min(2*top_part_size, len(pattern)) : -1])


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()