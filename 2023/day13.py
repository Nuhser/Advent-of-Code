from typing import override
from utility.util import flip_list_of_string
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.patterns = aoc.parse_input_with_blocks(puzzle_input)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        solution_sum: int = 0
        for pattern in self.patterns:
            # check for horizontal mirror
            mirror_idx: int | None = self.check_for_mirror(pattern)
            if (mirror_idx != None):
                solution_sum += 100 * mirror_idx

            # check for vertical mirror
            flipped_pattern: list[str] = flip_list_of_string(pattern)
            mirror_idx = self.check_for_mirror(flipped_pattern)
            if (mirror_idx != None):
                solution_sum += mirror_idx

        return f"Solution sum: {solution_sum}", solution_sum


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()
    

    def check_for_mirror(self, pattern: list[str]) -> int | None:
        for idx in range(0, len(pattern) - 1):
            length: int = min(idx, len(pattern) - idx - 2)

            if (pattern[idx - length : idx + 1] == pattern[idx + 1 + length : idx : -1]):
                return idx + 1