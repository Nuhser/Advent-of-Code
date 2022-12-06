import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.depths = aoc.parse_input(puzzle_input, cast_to=int)

    def part1(self) -> str:
        n_increases = 0
        last_depth = self.depths[0]
        for depth in self.depths[1 :]:
            if last_depth < depth:
                n_increases += 1
            last_depth = depth

        return f"Total depth increases: {n_increases}"

    def part2(self) -> str:
        sliding_sums = [sum(self.depths[i : i+3]) for i in range(len(self.depths[: -2]))]

        n_increases = 0
        last_depth = sliding_sums[0]
        for depth in sliding_sums[1 :]:
            if last_depth < depth:
                n_increases += 1
            last_depth = depth

        return f"Total depth increases: {n_increases}"