import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.notes = aoc.parse_input(puzzle_input, " | ", " ")

    def part1(self) -> tuple[str, (int | str)]:
        count = 0
        for note in self.notes:
            count += len([digit for digit in note[1] if len(digit) in [2, 3, 4, 7]])

        return f'Solution: {count}', count

    def part2(self) -> tuple[str, (int | str)]:
        solution = 0
        for note in self.notes:
            mapping = [None] * 10
            digits = [set(digit) for digit in note[0]]
            
            mapping[1] = next(d for d in digits if len(d) == 2)
            mapping[4] = next(d for d in digits if len(d) == 4)
            mapping[7] = next(d for d in digits if len(d) == 3)
            mapping[8] = next(d for d in digits if len(d) == 7)

            mapping[3] = next(d for d in digits if len(d) == 5 and d > mapping[1])
            mapping[9] = next(d for d in digits if len(d) == 6 and d > mapping[3])
            mapping[6] = next(d for d in digits if len(d) == 6 and not d > mapping[1])
            mapping[0] = next(d for d in digits if len(d) == 6 and d not in mapping)
            mapping[5] = next(d for d in digits if len(d) == 5 and d < mapping[6])
            mapping[2] = next(d for d in digits if len(d) == 5 and d not in mapping)

            solution += int(''.join(str(mapping.index(set(digit))) for digit in note[1]))

        return f'Solution: {solution}', solution
