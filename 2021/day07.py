import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        # get input
        self.crabs = dict()
        for position in aoc.parse_input(puzzle_input, ",", cast_to=int)[0]:
            self.crabs[position] = self.crabs[position] + 1 if position in self.crabs else 1

        self.max_position = max(self.crabs.keys())
        self.min_position = min(self.crabs.keys())

    def part1(self) -> tuple[str, (int | str)]:
        # find least required ammount of fuel
        least_fuel = None
        for curr_position in range(self.min_position, self.max_position + 1):
            fuel = 0
            for position in self.crabs:
                fuel += abs(curr_position - position) * self.crabs[position]

            if (least_fuel == None) or (fuel < least_fuel):
                least_fuel = fuel
                best_position = curr_position

        return f'Best Position: {best_position} (w/ {self.crabs[best_position] if best_position in self.crabs else 0} crabs starting there)\nRequired Fuel: {least_fuel}', str(least_fuel)

    def part2(self) -> tuple[str, (int | str)]:
        # find least required ammount of fuel
        least_fuel = None
        for curr_position in range(self.min_position, self.max_position + 1):
            fuel = 0
            for position in self.crabs:
                # First very slow idea
                # fuel += sum(list(range(1, abs(curr_position - position) + 1))) * crabs[position]

                # The smart way without sum
                diff = abs(curr_position - position)
                fuel += (((diff + 1) * (diff // 2)) + (((diff // 2) + 1) * (diff % 2))) * self.crabs[position]

            if (least_fuel == None) or (fuel < least_fuel):
                least_fuel = fuel
                best_position = curr_position

        return f'Best Position: {best_position} (w/ {self.crabs[best_position] if best_position in self.crabs else 0} crabs starting there)\nRequired Fuel: {least_fuel}', str(least_fuel)
