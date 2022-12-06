import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.puzzle_input = puzzle_input

    def part1(self) -> str:
        wrong_items = []
        for line in aoc.parse_input(self.puzzle_input):
            pivot = int(len(line) / 2)
            compartments = (set(line[: pivot]), set(line[pivot :]))

            for item in compartments[0]:
                if item in compartments[1]:
                    wrong_items.append(item)
                    break

        return f"Total priority sum of wrong items: {self.get_priority_sum(wrong_items)}"

    def part2(self) -> str:
        badges = []
        backpacks = aoc.parse_input(self.puzzle_input, cast_to=set)
        for i in range(0, len(backpacks), 3):
            for item in backpacks[i]:
                if (item in backpacks[i+1]) and (item in backpacks[i+2]):
                    badges.append(item)
                    break

        return f"Total priority sum of badges: {self.get_priority_sum(badges)}"

    def get_priority_sum(self, items: list):
        priority_sum = 0
        for item in items:
            if item.islower():
                priority_sum += 1 + ord(item) - ord("a")
            else:
                priority_sum += 27 + ord(item) - ord("A")

        return priority_sum
