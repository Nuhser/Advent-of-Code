import aoc_util as aoc
import utility.neighbors as neighbors

from typing import override


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.schematic = dict()
        for y_idx, line in enumerate(puzzle_input):
            for x_idx, char in enumerate(line.strip()):
                if (char == "."):
                    self.schematic[x_idx, y_idx] = None
                elif (char.isdigit()):
                    self.schematic[x_idx, y_idx] = int(char)
                else:
                    self.schematic[x_idx, y_idx] = char


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        part_numbers = list()

        x_idx = y_idx = 0
        while (True):
            while (True):
                if (isinstance(self.schematic[x_idx, y_idx], int)):
                    is_part_number, consumed_chars = self.check_for_symbol_recursively(x_idx, y_idx)

                    if (is_part_number):
                        consumed_chars += self.check_for_more_digits(x_idx+consumed_chars+1, y_idx)

                        part_numbers.append(int("".join([str(self.schematic[x, y_idx]) for x in range(x_idx, x_idx+consumed_chars+1)])))

                    x_idx += consumed_chars

                x_idx += 1
                if ((x_idx, y_idx) not in self.schematic):
                    x_idx = 0
                    break

            y_idx += 1
            if ((x_idx, y_idx) not in self.schematic):
                break

        if (self.verbose):
            print(f"Found part numbers: {part_numbers}")
            
        part_number_sum = sum(part_numbers)
        return f"Parts found: {len(part_numbers)}\nSum of part numbers: {part_number_sum}", part_number_sum


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        raise NotImplementedError(f"Part 2 of the solution for day {self.day} of year {self.year} isn't implemented yet!")


    def check_for_symbol_recursively(self, x_idx: int, y_idx: int) -> tuple[bool, int]:
        if (neighbors.has_matching_neighbors(self.schematic, (x_idx, y_idx), (lambda n: isinstance(n, str)))):
            return True, 0
            
        if ((x_idx+1, y_idx) in self.schematic) and (isinstance(self.schematic[x_idx+1, y_idx], int)):
            is_part_number, consumed_chars = self.check_for_symbol_recursively(x_idx+1, y_idx)
            return is_part_number, 1 + consumed_chars
        
        else:
            return False, 0
        

    def check_for_more_digits(self, x_idx: int, y_idx: int) -> int:
        additional_digits = 0
        while(((x_idx, y_idx) in self.schematic) and (isinstance(self.schematic[x_idx, y_idx], int))):
            x_idx += 1
            additional_digits += 1

        return additional_digits