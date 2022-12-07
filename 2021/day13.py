import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.dots, self.folds = aoc.parse_input_with_blocks(puzzle_input)

        self.dots = [(int(x), int(y)) for x, y in [dot.split(",") for dot in self.dots]]
        self.folds = [(axis, int(n)) for axis, n in [fold.removeprefix("fold along ").split("=") for fold in self.folds]]

        self.original_dots = self.dots.copy()

        if self.verbose:
            print(f"Starting with {len(self.dots)} dots...")

    def part1(self) -> tuple[str, (int | str)]:
        for axis, n in self.folds:
            new_dots = []
            if axis == 'x':
                for dot in self.dots:
                    if dot[0] < n:
                        new_dots.append(dot)
                    else:
                        new_x = dot[0] - (2 * abs(dot[0] - n))
                        if (new_x, dot[1]) not in self.dots:
                            new_dots.append((new_x, dot[1]))
            elif axis == 'y':
                for dot in self.dots:
                    if dot[1] < n:
                        new_dots.append(dot)
                    else:
                        new_y = dot[1] - (2 * abs(dot[1] - n))
                        if (dot[0], new_y) not in self.dots:
                            new_dots.append((dot[0], new_y))

            self.dots = new_dots

            if self.verbose:
                print(f'After folding along {axis}={str(n).rjust(3)}: {str(len(self.dots)).rjust(3)} dots remaining')

        if self.verbose:
            print("")

        return f"{len(self.dots)} dots remaining after all folds", len(self.dots)

    def part2(self) -> tuple[str, (int | str | None)]:
        if self.dots == self.original_dots:
            self.part1()

        max_x = max(x for x, _ in self.dots)
        max_y = max(y for _, y in self.dots)

        output = ['░' * (max_x + 1)] * (max_y + 1)

        for (x, y) in self.dots:
            output[y] = output[y][: x] + '▓' + output[y][x + 1 :]

        return "\n".join(output), None
