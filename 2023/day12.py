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
        def is_record_valid(record: str, actual_group_sizes: list[int]) -> bool:
            groups = re.findall(r"#+", record)
            group_sizes: list[int] = [len(group) for group in groups]
            return group_sizes == actual_group_sizes


        total_solutions: int = 0

        for record in self.records:
            total_springs: int = sum(record.spring_groups)
            total_unassigned_springs: int = total_springs - record.record_string.count("#")

            unassigned_positions: list[int] = [idx for idx, char in enumerate(record.record_string) if char == "?"]

            for assignment in combinations(unassigned_positions, total_unassigned_springs):
                new_record: list[str] = [char for char in record.record_string]

                for position in assignment:
                    new_record[position] = "#"

                if is_record_valid("".join(new_record), record.spring_groups):
                    total_solutions += 1

        return f"Total number of solutions: {total_solutions}", total_solutions


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        """
        This solution was based on https://github.com/clrfl/AdventOfCode2023/blob/master/12/part2.py.
        """

        def count_solutions(record: str, group_sizes: list[int]) -> int:
            states: str = "."
            for n in group_sizes:
                states += "#" * n + "."

            states_dict: dict[int, int] = {0: 1}
            new_dict: dict[int, int] = {}
            for char in record:
                for state in states_dict:
                    if char == "?":
                        if state + 1 < len(states):
                            new_dict[state + 1] = new_dict.get(state + 1, 0) + states_dict[state]
                        if states[state] == ".":
                            new_dict[state] = new_dict.get(state, 0) + states_dict[state]

                    elif char == ".":
                        if state + 1 < len(states) and states[state + 1] == ".":
                            new_dict[state + 1] = new_dict.get(state + 1, 0) + states_dict[state]
                        if states[state] == ".":
                            new_dict[state] = new_dict.get(state, 0) + states_dict[state]

                    elif char == "#":
                        if state + 1 < len(states) and states[state + 1] == "#":
                            new_dict[state + 1] = new_dict.get(state + 1, 0) + states_dict[state]

                states_dict = new_dict
                new_dict = {}

            return states_dict.get(len(states) - 1, 0) + states_dict.get(len(states) - 2, 0)


        total_solutions: int = 0
        for record in self.records:
            record.record_string = "?".join([record.record_string] * 5)
            record.spring_groups = record.spring_groups * 5

            total_solutions += count_solutions(record.record_string, record.spring_groups)

        return f"Total number of solutions: {total_solutions}", total_solutions
    

    @dataclass
    class Record:
        record_string: str
        spring_groups: list[int]