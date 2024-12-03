from typing import override
import aoc_util as aoc
from utility.terminal_formatting import Color


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.reports = aoc.parse_input(puzzle_input, " ", cast_to=int)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        safe_reports: int = 0

        for report in self.reports:
            if (self.check_report_safeness(report)):
                safe_reports += 1

        return f"Number of safe reports: {safe_reports}", safe_reports


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        safe_reports: int = 0

        for idx, report in enumerate(self.reports):
            if (self.verbose):
                print(f"{Color.YELLOW}Analyzing report {idx}...{Color.DEFAULT}")

            is_safe: bool = self.check_report_safeness(report)

            if (is_safe):
                safe_reports += 1

            else:
                if (self.verbose):
                    print(f"{Color.YELLOW}Removing problematic levels...{Color.DEFAULT}")

                for i in range(len(report)):
                    new_report: list[int] = report[: i] + report[i+1 :]

                    if (self.check_report_safeness(new_report)):
                        safe_reports += 1
                        break

            if (self.verbose):
                print("")

        return f"Number of safe reports: {safe_reports}", safe_reports


    def check_level_safeness(self, level: int, last_level: int, is_increase: bool | None) -> tuple[bool, int, bool | None]:
        diff: int = level - last_level
        last_level = level

        if (diff == 0):
            return False, last_level, is_increase

        if (is_increase == None):
            is_increase = (diff > 0)
        elif (is_increase != (diff > 0)):
            return False, last_level, is_increase

        if abs(diff) > 3:
            return False, last_level, is_increase

        return True, last_level, is_increase
    

    def check_report_safeness(self, report: list[int]) -> bool:
        is_safe: bool = True
        last_level: int = report[0]
        is_increase: bool | None = None

        for idx, level in enumerate(report[1:]):
            is_safe, last_level, is_increase = self.check_level_safeness(level, last_level, is_increase)

            if (not is_safe):
                if (self.verbose):
                    print(f"{Color.RED}Level {idx} or {idx+1} is not safe.{Color.DEFAULT}")

                return False

        if (self.verbose):
            print(f"{Color.GREEN}All levels are safe.{Color.DEFAULT}")

        return True