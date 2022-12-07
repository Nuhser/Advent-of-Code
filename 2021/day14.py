import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.polymer_string = aoc.parse_input(puzzle_input[0:1])[0]
        self.polymer_mapping = {line[0]: line[1] for line in aoc.parse_input(puzzle_input[2:], " -> ")}

        if (self.verbose):
            print(f"Polymer template: {self.polymer_string}")

    def part1(self) -> tuple[str, (int | str)]:
        for step in range(10):
            new_polymer_string = self.polymer_string[0]
            for idx in range(len(self.polymer_string) - 1):
                if self.polymer_string[idx : idx+2] in self.polymer_mapping:
                    new_polymer_string += self.polymer_mapping[self.polymer_string[idx : idx+2]] + self.polymer_string[idx + 1]
                else:
                    new_polymer_string += self.polymer_string[idx + 1]

            self.polymer_string = new_polymer_string

            if self.verbose:
                print(f'Length after step {step + 1}: {len(self.polymer_string)}')

        polymer_counts = dict()
        for char in self.polymer_string:
            if char not in polymer_counts:
                polymer_counts[char] = self.polymer_string.count(char)

        if self.verbose:
            print(f'\nPolymer counts: {polymer_counts}\n')

        max_polymer = max(list(polymer_counts.values()))
        min_polymer = min(list(polymer_counts.values()))

        return f'Solution: {max_polymer} - {min_polymer} = {max_polymer - min_polymer}', max_polymer - min_polymer

    def part2(self) -> tuple[str, (int | str)]:
        polymer_counts = {char: self.polymer_string.count(char) for char in self.polymer_string}
        pair_counts = {self.polymer_string[idx : idx+2]: self.polymer_string.count(self.polymer_string[idx : idx+2]) for idx in range(len(self.polymer_string) - 1)}

        for step in range(40):
            for pair, count in pair_counts.copy().items():
                if pair in self.polymer_mapping:
                    insertion_polymer = self.polymer_mapping[pair]

                    polymer_counts[insertion_polymer] = polymer_counts[insertion_polymer] + count if insertion_polymer in polymer_counts else count
                    pair_counts[pair] -= count

                    new_polymer1 = pair[0] + insertion_polymer
                    new_polymer2 = insertion_polymer + pair[1]

                    pair_counts[new_polymer1] = pair_counts[new_polymer1] + count if new_polymer1 in pair_counts else count
                    pair_counts[new_polymer2] = pair_counts[new_polymer2] + count if new_polymer2 in pair_counts else count

        if self.verbose:
            print(f'Final Polymer counts: {polymer_counts}\n')

        max_polymer = max(list(polymer_counts.values()))
        min_polymer = min(list(polymer_counts.values()))

        return f'Solution: {max_polymer} - {min_polymer} = {max_polymer - min_polymer}', max_polymer - min_polymer
