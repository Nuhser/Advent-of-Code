from typing import override
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
        return super().part2()