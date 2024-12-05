from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        blocks = aoc.parse_input_with_blocks_and_block_specific_line_delimiters(
            puzzle_input,
            ("|",),
            (",",),
            cast_to=int
        )

        self.ordering_rules: list[tuple[int, int]] = [(rule[0], rule[1]) for rule in blocks[0]]
        self.updates: list[list[int]] = blocks[1]


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        reverse_rules = {rule[1]: [page[0] for page in self.ordering_rules if (page[1] == rule[1])] for rule in self.ordering_rules}

        sum: int = 0
        for update in self.updates:
            update_is_correct: bool = True
            forbidden_pages: set[int] = set()

            for page in update:
                if (page in forbidden_pages):
                    update_is_correct = False
                    break

                if (not page in reverse_rules):
                    continue

                forbidden_pages |= set(reverse_rules[page])

            if (update_is_correct):
                sum += update[len(update) // 2]

        return f"The sum of middle pages of correct updates: {sum}", sum


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()