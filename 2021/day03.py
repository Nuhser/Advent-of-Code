import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.lines = aoc.parse_input(puzzle_input)

    def part1(self) -> str:
        # count 1s per digit
        counts = [int(d) for d in self.lines[0].strip()]
        for line in self.lines[1 :]:
            for i in range(len(counts)):
                counts[i] += int(line[i])

        gamma = ''
        epsilon = ''
        for count in counts:
            # get most common digit
            most_common_digit = int(count / (len(self.lines) / 2))

            # calculate gamma and epsilon
            gamma += str(most_common_digit)
            epsilon += str(0 if most_common_digit == 1 else 1)

        return f'Gamma: {gamma} -> {int(gamma, 2)}\nEpsilon: {epsilon} -> {int(epsilon, 2)}\n\nPower Consumption: {int(gamma, 2) * int(epsilon, 2)}'

    def part2(self) -> str:
        oxygen = self.lines
        for i in range(len(oxygen[0])):
            digit_counts = [0, 0]
            for value in oxygen:
                digit_counts[int(value[i])] += 1

            oxygen = [value for value in oxygen if (value[i] == '0')] \
                if digit_counts[0] > digit_counts[1] \
                else [value for value in oxygen if (value[i] == '1')]

            if len(oxygen) <= 1:
                break

        co2 = self.lines
        for i in range(len(co2[0])):
            digit_counts = [0, 0]
            for value in co2:
                digit_counts[int(value[i])] += 1

            co2 = [value for value in co2 if (value[i] == '0')] \
                if digit_counts[0] <= digit_counts[1] \
                else [value for value in co2 if (value[i] == '1')]

            if len(co2) <= 1:
                break

        return f'Oxygen:\t{oxygen[0]} -> {int(oxygen[0], 2)}\nCO2:\t{co2[0]} -> {int(co2[0], 2)}\n\nLife Support Rating: {int(oxygen[0], 2) * int(co2[0], 2)}'