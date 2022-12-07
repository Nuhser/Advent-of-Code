import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.blocks = aoc.parse_input_with_blocks(puzzle_input, cast_to=int)

    def part1(self) -> tuple[str, (int | str)]:
        max_sum = 0
        for block in self.blocks:
            max_sum = max(max_sum, sum(block))

        return f"Most Calories: {max_sum}", max_sum

    def part2(self) -> tuple[str, (int | str)]:
        max_elves = [0, 0, 0, 0]
        for block in self.blocks:
            max_elves.sort()
            max_elves[0] = sum(block)

        solution = sum(max_elves[1:])
        return f"Calories of Top Three Elves: {solution}", solution