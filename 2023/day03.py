from collections import defaultdict
from typing import Any, Callable, override

import aoc_util as aoc
from utility.mapping import Map


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        schematic: dict[tuple[int, int], Any] = {}
        for y_idx, line in enumerate(puzzle_input):
            for x_idx, char in enumerate(line.strip()):
                if char == ".":
                    schematic[x_idx, y_idx] = None
                elif char.isdigit():
                    schematic[x_idx, y_idx] = int(char)
                else:
                    schematic[x_idx, y_idx] = char

        self.schematic = Map.from_dict(schematic)

    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        part_numbers: list[int] = []

        x_idx = y_idx = 0
        while True:
            while True:
                if isinstance(self.schematic[x_idx, y_idx], int):
                    is_part_number, consumed_chars, _ = (
                        self.check_for_symbol_recursively(
                            x_idx, y_idx, (lambda _, n: isinstance(n[1], str))
                        )
                    )

                    if is_part_number:
                        consumed_chars += self.check_for_more_digits(
                            x_idx + consumed_chars + 1, y_idx
                        )

                        part_numbers.append(
                            int(
                                "".join(
                                    [
                                        str(self.schematic[x, y_idx])
                                        for x in range(
                                            x_idx, x_idx + consumed_chars + 1
                                        )
                                    ]
                                )
                            )
                        )

                    x_idx += consumed_chars

                x_idx += 1
                if not self.schematic.contains_coords((x_idx, y_idx)):
                    x_idx = 0
                    break

            y_idx += 1
            if not self.schematic.contains_coords((x_idx, y_idx)):
                break

        if self.verbose:
            print(f"Found part numbers: {part_numbers}")

        part_number_sum = sum(part_numbers)
        return (
            f"Parts found: {len(part_numbers)}\nSum of part numbers: {part_number_sum}",
            part_number_sum,
        )

    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        gears: defaultdict[tuple[int, int], tuple[int, int]] = defaultdict(
            lambda: (1, 0)
        )

        x_idx = y_idx = 0
        while True:
            while True:
                if isinstance(self.schematic[x_idx, y_idx], int):
                    has_gear, consumed_chars, gear_coords = (
                        self.check_for_symbol_recursively(
                            x_idx, y_idx, (lambda _, n: n[1] == "*")
                        )
                    )

                    if has_gear:
                        consumed_chars += self.check_for_more_digits(
                            x_idx + consumed_chars + 1, y_idx
                        )
                        part_number = int(
                            "".join(
                                [
                                    str(self.schematic[x, y_idx])
                                    for x in range(x_idx, x_idx + consumed_chars + 1)
                                ]
                            )
                        )

                        for gear in gear_coords:
                            gears[gear] = (
                                gears[gear][0] * part_number,
                                gears[gear][1] + 1,
                            )

                    x_idx += consumed_chars

                x_idx += 1
                if not self.schematic.contains_coords((x_idx, y_idx)):
                    x_idx = 0
                    break

            y_idx += 1
            if not self.schematic.contains_coords((x_idx, y_idx)):
                break

        if self.verbose:
            print(
                f"Found gear: {[gear[0] for gear in gears.items() if gear[1][1] == 2]}"
            )

        gear_ratio_sum = sum([value[0] for value in gears.values() if value[1] == 2])
        return (
            f"Gears found: {len(gears)}\nSum of gear ratios: {gear_ratio_sum}",
            gear_ratio_sum,
        )

    def check_for_symbol_recursively(
        self, x_idx: int, y_idx: int, matching_function: Callable[[Any, Any], bool]
    ) -> tuple[bool, int, list[tuple[int, int]]]:
        matching_neighbors = self.schematic.get_matching_neighbors(
            (x_idx, y_idx), matching_function
        )

        if len(matching_neighbors) > 0:
            return True, 0, [coords for coords, _ in matching_neighbors]

        if (self.schematic.contains_coords((x_idx + 1, y_idx))) and (
            isinstance(self.schematic[x_idx + 1, y_idx], int)
        ):
            is_part_number, consumed_chars, coords = self.check_for_symbol_recursively(
                x_idx + 1, y_idx, matching_function
            )
            return is_part_number, 1 + consumed_chars, coords

        else:
            return False, 0, []

    def check_for_more_digits(self, x_idx: int, y_idx: int) -> int:
        additional_digits = 0
        while (self.schematic.contains_coords((x_idx, y_idx))) and (
            isinstance(self.schematic[x_idx, y_idx], int)
        ):
            x_idx += 1
            additional_digits += 1

        return additional_digits
