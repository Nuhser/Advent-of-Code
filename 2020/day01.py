from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.entries = aoc.parse_input(puzzle_input, cast_to=int)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        for idx, entry1 in enumerate(self.entries):
            for entry2 in self.entries[idx+1 :]:
                if (entry1 + entry2 == 2020):
                    return f"Product of entries: {entry1 * entry2}", (entry1 * entry2)
                
        raise ValueError(f"ERROR: Couldn't find two matching entries.")


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        for i, entry1 in enumerate(self.entries):
            for j, entry2 in enumerate(self.entries[i+1 :]):
                for entry3 in self.entries[j+1 :]:
                    if (entry1 + entry2 + entry3 == 2020):
                        return f"Product of entries: {entry1 * entry2 * entry3}", (entry1 * entry2 * entry3)
                
        raise ValueError(f"ERROR: Couldn't find three matching entries.")