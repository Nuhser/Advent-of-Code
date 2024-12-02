from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.reports = aoc.parse_input(puzzle_input, " ", cast_to=int)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        safe_reports: int = 0

        for report in self.reports:
            is_safe: bool = True
            last_level: int = report[0]
            is_increase: bool = None

            for level in report[1:]:
                diff: int = level - last_level

                if abs(diff) > 3:
                    is_safe = False
                    break

                if (diff == 0):
                    is_safe = False
                    break

                if (is_increase == None):
                    is_increase = (diff > 0)
                elif (is_increase != (diff > 0)):
                    is_safe = False
                    break

                last_level = level

            if (is_safe):
                safe_reports += 1

        return f"Number of safe reports: {safe_reports}", safe_reports


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()