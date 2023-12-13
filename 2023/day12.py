from dataclasses import dataclass
from itertools import combinations
from typing import override
import aoc_util as aoc
import re


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        lines = aoc.parse_input(puzzle_input, " ", ",")

        self.records: list["Solution.Record"] = []
        for line in lines:
            self.records.append(self.Record(line[0][0], [int(n) for n in line[1]]))

        if self.verbose:
            print(f"Records:\n{"\n".join(str(record) for record in self.records)}\n")


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        total_solutions: int = 0

        for record in self.records:
            total_springs: int = sum(record.spring_groups)
            total_unassigned_springs: int = total_springs - record.record_string.count("#")

            unassigned_positions: list[int] = [idx for idx, char in enumerate(record.record_string) if char == "?"]

            for assignment in combinations(unassigned_positions, total_unassigned_springs):
                new_record: list[str] = [char for char in record.record_string]

                for position in assignment:
                    new_record[position] = "#"

                if self.is_record_valid("".join(new_record), record.spring_groups):
                    total_solutions += 1

        return f"Total number of solutions: {total_solutions}", total_solutions


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()
    

    @dataclass
    class Record:
        record_string: str
        spring_groups: list[int]

    
    def is_record_valid(self, record: str, actual_group_sizes: list[int]) -> bool:
        groups = re.findall(r"#+", record)
        group_sizes: list[int] = [len(group) for group in groups]
        return group_sizes == actual_group_sizes