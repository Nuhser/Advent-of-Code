import aoc_util as aoc
import utility.util

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.instructions = aoc.parse_input(puzzle_input, " ")

        if self.verbose:
            print(self.instructions)

    def part1(self) -> tuple[str, (int | str | None)]:
        X = 1
        cycle = 0
        signal_strengths = []

        for instruction in self.instructions:
            cycle += 1

            if (cycle - 20) % 40 == 0:
                if self.verbose:
                    print(f"Cycle {cycle}, Register X: {X}, Signal Strength: {cycle * X}")

                signal_strengths.append(cycle * X)

            if instruction[0] != "noop":
                cycle += 1

                if (cycle - 20) % 40 == 0:
                    if self.verbose:
                        print(f"Cycle {cycle}, Register X: {X}, Signal Strength: {cycle * X}")

                    signal_strengths.append(cycle * X)

                X += int(instruction[1])

        solution = sum(signal_strengths)
        return f"Sum of Signal Strengths after all {cycle} cycles: {solution}", solution

    def part2(self) -> tuple[str, (int | str | None)]:
        display = ""
        X = 1
        cycle = 0

        for instruction in self.instructions:
            cycle += 1
            display += ("█" if (cycle-1) % 40 in range(X-1, X+2) else " ")

            if instruction[0] != "noop":
                cycle += 1
                display += ("█" if (cycle-1) % 40 in range(X-1, X+2) else " ")

                X += int(instruction[1])

        return "\n".join([line for line in utility.util.split_string_in_chunks(display, 40)]), None
