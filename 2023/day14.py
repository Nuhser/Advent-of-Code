from enum import Enum
from functools import cache, lru_cache
from typing import override
from utility.mapping import generate_map_with_coordinates, get_map_column, get_map_dimensions, get_map_row, print_map
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    """
    This solutioni uses the first param of the '--param'-terminal argument to determine the number of tilt cycles to run in part 2.
    """


    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.platform: dict[tuple[int, int], "Solution.RockType"] = generate_map_with_coordinates(aoc.parse_input(puzzle_input), self.RockType)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        platform: dict[tuple[int, int], "Solution.RockType"] = self.platform.copy()

        self.tilt_platform(platform, "north")

        if self.verbose:
            print("Platform after tilting north:")
            print_map(platform, end="\n")

        _, y_len = get_map_dimensions(platform)

        weight: int = 0
        for y in range(y_len):
            for _, rock in get_map_row(platform, y):
                if rock == self.RockType.ROUND:
                    weight += y_len - y

        return f"Total load on north support beams: {weight}", weight


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        tilt_cycles: int = int(self.params[0]) if (len(self.params) == 1) else 1_000_000_000
        platform: dict[tuple[int, int], "Solution.RockType"] = self.platform.copy()

        history: list[dict[tuple[int, int], "Solution.RockType"]] = [platform.copy()]

        for i in range(tilt_cycles):
            for direction in ["north", "west", "south", "east"]:
                self.tilt_platform(platform, direction)

            try:
                cycle_start_index = history.index(platform)
                cycle_end_index = i
                cycle_length: int = (cycle_end_index - cycle_start_index) + 1
            except ValueError:
                cycle_start_index = None

            if cycle_start_index != None:
                if self.verbose:
                    print(f"Cycle starts at {cycle_start_index} and ends at {cycle_end_index}.\nLength is {cycle_length}")

                break

            history.append(platform.copy())

        if cycle_start_index != None:
            platform = history[-1].copy()

            remaining_tilt_cycles: int = (tilt_cycles - cycle_start_index + 1) % cycle_length

            if self.verbose:
                print(f"Remaining tilt cycles: {remaining_tilt_cycles}")

            for i in range(remaining_tilt_cycles):
                for direction in ["north", "west", "south", "east"]:
                    self.tilt_platform(platform, direction)

        _, y_len = get_map_dimensions(platform)

        weight: int = 0
        for y in range(y_len):
            for _, rock in get_map_row(platform, y):
                if rock == self.RockType.ROUND:
                    weight += y_len - y

        return f"Total load on north support beams after {tilt_cycles:,} tilt cycles: {weight}", weight



    def tilt_platform(self, platform: dict[tuple[int, int], "Solution.RockType"], direction: str) -> None:
        x_len, y_len = get_map_dimensions(platform)

        match direction:
            case "north" | "south":
                edge_row: int = 0 if (direction == "north") else (y_len - 1)
                direction_int: int = 1 if (direction == "north") else -1

                last_rocks: list[int] = [(edge_row - direction_int) if (rock == self.RockType.NONE) else edge_row for _, rock in get_map_row(platform, edge_row)]

                for y in range(edge_row + direction_int, y_len if (direction == "north") else -1, direction_int):
                    for (x, _), rock in get_map_row(platform, y):
                        match rock:
                            case self.RockType.NONE:
                                continue
                            case self.RockType.SQUARE:
                                last_rocks[x] = y
                            case self.RockType.ROUND:
                                platform[x, y] = self.RockType.NONE
                                platform[x, last_rocks[x] + direction_int] = self.RockType.ROUND
                                last_rocks[x] += direction_int

            case "west" | "east":
                edge_column: int = 0 if (direction == "west") else (x_len - 1)
                direction_int: int = 1 if (direction == "west") else -1

                last_rocks: list[int] = [(edge_column - direction_int) if (rock == self.RockType.NONE) else edge_column for _, rock in get_map_column(platform, edge_column)]

                for x in range(edge_column + direction_int, x_len if (direction == "west") else -1, direction_int):
                    for (_, y), rock in get_map_column(platform, x):
                        match rock:
                            case self.RockType.NONE:
                                continue
                            case self.RockType.SQUARE:
                                last_rocks[y] = x
                            case self.RockType.ROUND:
                                platform[x, y] = self.RockType.NONE
                                platform[last_rocks[y] + direction_int, y] = self.RockType.ROUND
                                last_rocks[y] += direction_int

            case _:
                raise ValueError(f"ERROR: Incorect direction for tilting '{direction}'. Must be one of the following: 'north', 'west', 'south', 'east'")


    class RockType(Enum):
        NONE = "."
        ROUND = "O"
        SQUARE = "#"

        def __str__(self):
            return self.value