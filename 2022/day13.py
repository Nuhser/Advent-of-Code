import aoc_util as aoc
import json

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.pairs: list[tuple[list, list]] = []
        for block in aoc.parse_input_with_blocks(puzzle_input):
            self.pairs.append((json.loads(block[0]), json.loads(block[1])))

    def part1(self) -> tuple[str, (int | float | str | None)]:
        correct_pairs: list[int] = []
        for pair_idx, (left, right) in enumerate(self.pairs):
            if self.compare_pair(left, right):
                correct_pairs.append(pair_idx + 1)

        solution = sum(correct_pairs)
        return f"Correct Pairs: {correct_pairs}\nThe sum is {aoc.ANSI_UNDERLINE + str(solution) + aoc.ANSI_NOT_UNDERLINE}", solution

    def compare_pair(self, left, right) -> bool | None:
        if len(left) == 0:
            return True

        for i in range(len(left)):
            if i > (len(right) - 1):
                return False

            if (type(left[i]) == int) and (type(right[i]) == int):
                if left[i] < right[i]:
                    return True
                elif left[i] > right[i]:
                    return False
                else:
                    continue
            
            elif (type(left[i]) == list) and (type(right[i]) == list):
                comparison = self.compare_pair(left[i], right[i])
                if (comparison == None):
                    continue
                else:
                    return comparison

            else:
                comparison = self.compare_pair(left[i] if type(left[i]) == list else [left[i]], right[i] if type(right[i]) == list else [right[i]])
                if (comparison == None):
                    continue
                else:
                    return comparison

        if len(right) > len(left):
            return True

        return None