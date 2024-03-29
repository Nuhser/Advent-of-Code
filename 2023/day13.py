from typing import override
from utility.util import flip_list_of_string, get_diff_between_strings
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
        solution_sum: int = 0
        for pattern in self.patterns:
            # check for horizontal mirror
            mirror_idx: int | None = self.check_for_mirror(pattern, smudge_tolerance=1)
            if (mirror_idx != None):
                solution_sum += 100 * mirror_idx

            # check for vertical mirror
            flipped_pattern: list[str] = flip_list_of_string(pattern)
            mirror_idx = self.check_for_mirror(flipped_pattern, smudge_tolerance=1)
            if (mirror_idx != None):
                solution_sum += mirror_idx

        return f"Solution sum: {solution_sum}", solution_sum
    

    def check_for_mirror(self, pattern: list[str], smudge_tolerance: int=0) -> int | None:
        for idx in range(0, len(pattern) - 1):
            length: int = min(idx, len(pattern) - idx - 2)

            if (smudge_tolerance == 0):
                if (pattern[idx - length : idx + 1] == pattern[idx + 1 + length : idx : -1]):
                    return idx + 1
                
            else:
                if (smudge_tolerance == sum(get_diff_between_strings(pattern1, pattern2) for pattern1, pattern2 in zip(pattern[idx - length : idx + 1], pattern[idx + 1 + length : idx : -1]))):
                    return idx + 1