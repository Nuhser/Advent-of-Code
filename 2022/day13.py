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
            if self.compare_pairs(left, right):
                correct_pairs.append(pair_idx + 1)

        solution = sum(correct_pairs)
        return f"Correct Pairs: {correct_pairs}\nThe sum is {aoc.ANSI_UNDERLINE + str(solution) + aoc.ANSI_NOT_UNDERLINE}", solution

    def part2(self) -> tuple[str, (int | float | str | None)]:
        # TODO: Insertion, Selection, Quick, Merge, Shell, Heap

        packets = [packet for pair in self.pairs for packet in pair] + [[[2]], [[6]]]
        ordered_packets = aoc.bubble_sort(packets, lambda a, b: self.compare_pairs(a, b))

        divider_packets = [-1, -1]
        for idx, packet in enumerate(ordered_packets):
            if packet == [[2]]:
                divider_packets[0] = idx + 1
            if packet == [[6]]:
                divider_packets[1] = idx + 1

        if divider_packets[0] == -1:
            raise RuntimeError("First divider packet '[[2]]' wasn't found in ordered packets!")
        elif divider_packets[1] == -1:
            raise RuntimeError("Second divider packet '[[6]]' wasn't found in ordered packets!")

        return f"Decoder Key: {divider_packets[0] * divider_packets[1]}", divider_packets[0] * divider_packets[1]

    def compare_pairs(self, left, right) -> bool | None:
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
                comparison = self.compare_pairs(left[i], right[i])
                if (comparison == None):
                    continue
                else:
                    return comparison

            else:
                comparison = self.compare_pairs(left[i] if type(left[i]) == list else [left[i]], right[i] if type(right[i]) == list else [right[i]])
                if (comparison == None):
                    continue
                else:
                    return comparison

        if len(right) > len(left):
            return True

        return None