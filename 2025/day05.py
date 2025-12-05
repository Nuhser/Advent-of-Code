from typing import override, Literal
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        database = aoc.parse_input_with_blocks_and_block_specific_line_delimiters(puzzle_input, ('-',), (), cast_to=int)
        self.ingredient_ranges: list[list[int]] = database[0]
        self.ingredient_ids: list[int] = database[1]


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        fresh_ingredients: int = 0
        for id in self.ingredient_ids:
            for range in self.ingredient_ranges:
                if (range[0] <= id) and (range[1] >= id):
                    fresh_ingredients += 1
                    break

        return f"There are {fresh_ingredients} fresh ingredients available.", fresh_ingredients


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        new_ranges = [(r[0], r[1]) for r in self.ingredient_ranges]
        merged = True

        while merged:
            new_ranges, merged = self.merge_ranges(new_ranges)

        if self.verbose:
            print("IDs:", new_ranges)

        total_fresh_ids: int = 0
        for range in new_ranges:
            total_fresh_ids += range[1] - range[0] + 1

        return f"There are {total_fresh_ids} IDs possible for fresh ingredients.", total_fresh_ids
    
    def merge_ranges(self, ranges: list[tuple[int, int]]) -> tuple[list[tuple[int, int]], bool]:
        new_ranges: list[tuple[int, int]] = [(ranges[0][0], ranges[0][1])]
        merged: bool = False

        for range in ranges[1:]:
            found: bool = False
            for idx, r in enumerate(new_ranges):
                lower_limit: Literal[-1, 0, 1] = -1 if (range[0] < r[0]) else 1 if (range[0] > r[1]) else 0
                upper_limit: Literal[-1, 0, 1] = -1 if (range[1] < r[0]) else 1 if (range[1] > r[1]) else 0

                if (lower_limit == upper_limit):
                    found = (lower_limit == 0)

                    if found:
                        break
                    else:
                        continue

                if (lower_limit == -1) or (upper_limit == 1):
                    new_ranges[idx] = ((range[0] if (lower_limit == -1) else r[0]), (range[1] if (upper_limit == 1) else r[1]))
                    merged = True
                    found = True
                    break

            if not found:
                new_ranges.append((range[0], range[1]))

        return new_ranges, merged