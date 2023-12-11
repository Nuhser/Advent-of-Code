from typing import override
import aoc_util as aoc
from utility.neighbors import get_matching_neighbors
from utility.terminal_formatting import Navigation


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.pipe_map: dict[tuple[int, int], str] = {}
        for y, line in enumerate(aoc.parse_input(puzzle_input)):
            for x, symbol in enumerate(line):
                self.pipe_map[x, y] = symbol

                if (symbol == "S"):
                    self.start_coords: tuple[int, int] = (x, y)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        # find starting direction
        current_pipe = get_matching_neighbors(self.pipe_map, self.start_coords, self.is_pointing_to_current_pipe, diagonal=False)[0]
        current_direction = (current_pipe[0][0] - self.start_coords[0], current_pipe[0][1] - self.start_coords[1])
        pipes_number: int = 2

        while(True):
            if self.verbose:
                print(f"Looking at pipe #{pipes_number} '{current_pipe[1]}' (Direction: {current_direction})")

            new_pipe: tuple[int, int]

            match current_pipe[1]:
                case "-" | "|":
                    new_pipe = (current_pipe[0][0] + current_direction[0], current_pipe[0][1] + current_direction[1])
                case "L":
                    if (current_direction == (0, 1)):
                        new_pipe = (current_pipe[0][0] + 1, current_pipe[0][1])
                    else:
                        new_pipe = (current_pipe[0][0], current_pipe[0][1] - 1)
                case "F":
                    if (current_direction == (0, -1)):
                        new_pipe = (current_pipe[0][0] + 1, current_pipe[0][1])
                    else:
                        new_pipe = (current_pipe[0][0], current_pipe[0][1] + 1)
                case "J":
                    if (current_direction == (0, 1)):
                        new_pipe = (current_pipe[0][0] - 1, current_pipe[0][1])
                    else:
                        new_pipe = (current_pipe[0][0], current_pipe[0][1] - 1)
                case "7":
                    if (current_direction == (0, -1)):
                        new_pipe = (current_pipe[0][0] - 1, current_pipe[0][1])
                    else:
                        new_pipe = (current_pipe[0][0], current_pipe[0][1] + 1)

            current_direction = (new_pipe[0] - current_pipe[0][0], new_pipe[1] - current_pipe[0][1])
            current_pipe = (new_pipe, self.pipe_map[new_pipe])

            if (current_pipe[1] == "S"):
                break
            
            pipes_number += 1

        return f"Loop consists of {pipes_number} pipes. Furthest distance to start a position {int(pipes_number / 2)}.", int(pipes_number / 2)


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()
    

    def is_pointing_to_current_pipe(self, current_coords: tuple[int, int], other_pipe: tuple[tuple[int, int], str]) -> bool:
        if (current_coords[0] > other_pipe[0][0]):
            return other_pipe[1] in ["-", "L", "F"]

        elif (current_coords[0] < other_pipe[0][0]):
            return other_pipe[1] in ["-", "J", "7"]

        elif (current_coords[1] > other_pipe[0][1]):
            return other_pipe[1] in ["|", "F", "7"]

        elif (current_coords[1] < other_pipe[0][1]):
            return other_pipe[1] in ["|", "L", "J"]

        else:
            raise ValueError(f"ERROR: No neighboring pipes are pointing into current pipe at X={current_coords[0]} & Y={current_coords[1]}.")