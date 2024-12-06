from typing import override
import aoc_util as aoc
import utility.sorting as sorting


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        blocks = aoc.parse_input_with_blocks_and_block_specific_line_delimiters(
            puzzle_input,
            ("|",),
            (",",),
            cast_to=int
        )

        rules: list[tuple[int, int]] = [(rule[0], rule[1]) for rule in blocks[0]]
        self.rules = {rule[0]: [page[1] for page in rules if (page[0] == rule[0])] for rule in rules}
        self.reverse_rules = {rule[1]: [page[0] for page in rules if (page[1] == rule[1])] for rule in rules}
        self.updates: list[list[int]] = blocks[1]


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        sum: int = 0
        for update in self.updates:
            if (self.check_if_update_is_in_order(update)):
                sum += update[len(update) // 2]

        return f"The sum of middle pages of correct updates: {sum}", sum


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        sum: int = 0
        for update in self.updates:
            if (not self.check_if_update_is_in_order(update)):
                sorting.heap_sort(
                    update,
                    lambda a, b:
                        ((a not in self.rules) and (b not in self.rules)) or
                        ((a in self.rules) and (b in self.rules[a])) or
                        ((b in self.rules) and (a not in self.rules[b]))
                )

                sum += update[len(update) // 2]

        return f"Sum of middle pages of incorrect updates after sorting: {sum}", sum
    

    def check_if_update_is_in_order(self, update: list[int]) -> bool:
        forbidden_pages: set[int] = set()

        for page in update:
            if (page in forbidden_pages):
                return False

            if (not page in self.reverse_rules):
                continue

            forbidden_pages |= set(self.reverse_rules[page])

        return True