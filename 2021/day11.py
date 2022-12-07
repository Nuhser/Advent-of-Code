import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.octopuses = {(x, y): [energy_level, True] for y, line in enumerate(aoc.parse_input(puzzle_input)) for x, energy_level in enumerate(aoc.split_string_in_chunks(line, 1, cast_to=int))}

    def part1(self) -> tuple[str, (int | str)]:
        flash_counter = 0
        for step in range(100):
            # increase all energy levels by 1
            self.octopuses = {octopus: [self.octopuses[octopus][0] + 1, True] for octopus in self.octopuses}

            # flash high energy octopuses recursively
            for octopus in filter(lambda octopus: (self.octopuses[octopus][0] > 9) and self.octopuses[octopus][1], self.octopuses):
                flash_counter += self.flash(octopus)

            # reset flashed octopuses
            for octopus in filter(lambda octopus: not self.octopuses[octopus][1], self.octopuses):
                self.octopuses[octopus][0] = 0

        return f'Total Flashes: {flash_counter}', flash_counter

    def part2(self) -> tuple[str, (int | str)]:
        step = 0
        while True:
            step += 1
            flash_counter = 0

            # increase all energy levels by 1
            self.octopuses = {octopus: [self.octopuses[octopus][0] + 1, True] for octopus in self.octopuses}

            # flash high energy octopuses recursively
            for octopus in filter(lambda octopus: (self.octopuses[octopus][0] > 9) and self.octopuses[octopus][1], self.octopuses):
                flash_counter += self.flash(octopus)

            # reset flashed octopuses
            for octopus in filter(lambda octopus: not self.octopuses[octopus][1], self.octopuses):
                self.octopuses[octopus][0] = 0

            if flash_counter == 100:
                break

        return f'All octopuses flashed simultaneously at step {step}', step

    def get_neighbours(self, x, y):
        return filter(lambda octopus: octopus in self.octopuses, [(x-1, y), (x-1, y-1), (x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1)])

    def flash(self, octopus):
        flash_counter = 1
        self.octopuses[octopus][1] = False
        
        for neighbour in self.get_neighbours(*octopus):
            self.octopuses[neighbour][0] += 1
            if self.octopuses[neighbour][0] > 9 and self.octopuses[neighbour][1]:
                flash_counter += self.flash(neighbour)
        
        return flash_counter
