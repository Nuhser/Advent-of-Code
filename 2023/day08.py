from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        blocks = aoc.parse_input_with_blocks(puzzle_input, " = (", ", ")

        self.instructions: str = blocks[0][0][0][0]
        self.nodes: dict[str, dict[str, str]] = {}

        for line in blocks[1]:
            self.nodes[line[0][0]] = {"L": line[1][0], "R": line[1][1][:-1]}

        if self.verbose:
            print(f"Instructions: {self.instructions}")
            print(f"Nodes:\n{self.nodes}")


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        current_node = "AAA"
        step = 0
        found_destination = False

        while not found_destination:
            for instruction in self.instructions:
                if (current_node == "ZZZ"):
                    found_destination = True
                    break

                step += 1
                current_node = self.nodes[current_node][instruction]

        return f"Found destination after {step} steps.", step


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        raise NotImplementedError(f"Part 2 of the solution isn't implemented yet!")