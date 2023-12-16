from collections import defaultdict
from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.sequence: list[str] = aoc.parse_input(puzzle_input, ",")[0]


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        total_sum: int = 0

        for step in self.sequence:
            total_sum += self.holiday_ascii_string_helper(step)

        return f"The test sum is {total_sum}", total_sum


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        boxes: defaultdict[int, list[tuple[str, int]]] = defaultdict(lambda: list())

        for step in self.sequence:
            if "=" in step:
                label: str = step.split("=")[0]
                focal_length: (int | None) = int(step.split("=")[1])
            else:
                label = step[: -1]
                focal_length = None

            box_idx: int = self.holiday_ascii_string_helper(label)

            if (focal_length == None):
                for lens in boxes[box_idx]:
                    if (lens[0] == label):
                        boxes[box_idx].remove(lens)
                        break

            else:
                lens_found: bool = False
                for lens_idx, lens in enumerate(boxes[box_idx]):
                    if (lens[0] == label):
                        boxes[box_idx][lens_idx] = label, focal_length
                        lens_found = True
                        break

                if not lens_found:
                    boxes[box_idx].append((label, focal_length))

        focusing_power: int = 0

        for box_idx, box in boxes.items():
            for lens_idx, (_, focal_length) in enumerate(box):
                focusing_power += (box_idx + 1) * (lens_idx + 1) * focal_length

        return f"Total focusing power: {focusing_power}", focusing_power


    def holiday_ascii_string_helper(self, string: str) -> int:
        output: int = 0

        for char in string:
            output += ord(char)
            output *= 17
            output %= 256

        return output