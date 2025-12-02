from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.ranges: list[str] = aoc.parse_input(puzzle_input, ",", "-")[0]


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        invalid_ids: list[int] = []

        for start, end in [(r[0], r[1]) for r in self.ranges]:
            if (len(start) % 2 != 0) and (len(end) % 2 != 0) and (len(start) == len(end)):
                continue

            for id in range(int(start), int(end) + 1):
                id = str(id)

                if (len(id) % 2 != 0):
                    continue
                
                if (id[: len(id)//2] == id[len(id)//2 :]):
                    invalid_ids.append(int(id))

        result = sum(invalid_ids)
        return f"Sum of all invalid IDs: {result}", result


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()