from math import lcm
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
            print(f"Instructions:\n{self.instructions}")
            print(f"Nodes:\n{self.nodes}")


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        current_node: str = "AAA"
        step: int = 0
        found_destination: bool = False

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
        start_nodes: list[str] = [node for node in self.nodes.keys() if node[-1] == "A"]
        steps: list[int] = []

        for start_node in start_nodes:
            current_node: str = start_node
            step: int = 0
            found_destination: bool = False

            while not found_destination:
                for instruction in self.instructions:
                    if (current_node[-1] == "Z"):
                        found_destination = True
                        break

                    step += 1
                    current_node = self.nodes[current_node][instruction]

            steps.append(step)

        if self.verbose:
            print(f"Steps to Destinations: {steps}")

        final_step = lcm(*steps)

        return f"Found all destinations at the same time after {final_step} steps.", final_step