from collections import defaultdict
from typing import override
import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.cards: list[tuple[defaultdict[int, bool], list[int]]] = []

        parsed_input = aoc.parse_input(puzzle_input, ": ", " | ", "")
        for card in parsed_input:
            winning_numbers: list[int] = [int(n.strip()) for n in card[1][0]]
            numbers: list[int] = [int(n.strip()) for n in card[1][1]]

            self.cards.append((defaultdict(lambda: False), numbers))

            for number in winning_numbers:
                self.cards[-1][0][number] = True


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        total_points: int = 0

        for card in self.cards:
            numbers_found: int = 0

            for number in card[1]:
                if (card[0][number]):
                    numbers_found += 1

            if (numbers_found > 0):
                total_points += 2 ** (numbers_found - 1)

        return f"Total points: {total_points}", total_points


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        raise NotImplementedError(f"Part 2 of the solution for day {self.day} of year {self.year} isn't implemented yet!")