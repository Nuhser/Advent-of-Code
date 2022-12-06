import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.initial_fish = aoc.parse_input(puzzle_input, ",", cast_to=int)[0]

    def part1(self) -> str:
        days = 80
        return f'Initial Population: {len(self.initial_fish)}\nFinal Population afters {days} days: {self.calculate_population(self.initial_fish, days)}'

    def part2(self) -> str:
        days = 256
        return f'Initial Population: {len(self.initial_fish)}\nFinal Population afters {days} days: {self.calculate_population(self.initial_fish, days)}'

    def calculate_population(self, initial_fish: list, days: int) -> int:
        fish = [0] * 9
        for f in initial_fish:
            fish[f] += 1

        for _ in range(days):
            tmp = fish[0]
            for i in range(8):
                fish[i] = fish[i + 1]
            fish[8] = tmp
            
            fish[6] += tmp

        return sum(fish)
